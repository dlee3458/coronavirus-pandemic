import os
from stats.models import Record, Country, Unemployment, ChartConfirmedData, ChartDeathData, ChartVaccinationData, HistoricalConfirmedData, HistoricalDeathData, HistoricalVaccinationData
from news.models import TrendingArticle, Article
import requests
import praw
from newspaper import Article as art
from geopy.geocoders import MapBox
from django.shortcuts import get_object_or_404
import json
import csv, urllib.request
from geojson import Point, Feature, FeatureCollection, dump
from celery import task

client_id = os.environ.get('client_id')
client_secret = os.environ.get('client_secret')
mapbox_key = os.environ.get('mapbox_key')

# Retrieves global stats
@task(name='stats')
def get_stats():
    response = requests.get('https://api.covid19api.com/summary')
    if response.status_code == 200:
        data = response.json()
        total_death = data['Global']['TotalDeaths']
        total_confirmed = data['Global']['TotalConfirmed']
        total_recovered = data['Global']['TotalRecovered']
        new_death = data['Global']['NewDeaths']
        new_confirmed = data['Global']['NewConfirmed']
        new_recovered = data['Global']['NewRecovered']
        death_var = total_death - (total_death - new_death)
        confirmed_var = total_confirmed - (total_confirmed - new_confirmed)
        recovered_var = total_recovered - (total_recovered - new_recovered)
        death_percentage = (death_var / (total_death - new_death)) * 100
        confirmed_percentage = (confirmed_var / (total_confirmed - new_confirmed)) * 100
        recovered_percentage = (recovered_var / (total_recovered - new_recovered)) * 100
        
        for record in Record.objects.all():
            stat_id = record.id

        obj, created = Record.objects.update_or_create(id=stat_id, defaults={
                                                                        'total_death': total_death,
                                                                        'total_confirmed': total_confirmed,
                                                                        'total_recovered': total_recovered,
                                                                        'new_death': new_death,
                                                                        'new_confirmed': new_confirmed,
                                                                        'new_recovered': new_recovered,
                                                                        'death_percentage': death_percentage,
                                                                        'confirmed_percentage': confirmed_percentage,
                                                                        'recovered_percentage': recovered_percentage
                                                                    })
    else:
        print('No more requests(stats)!')


# Retrieves stats for each country
@task(name='countries')
def get_countries():
    response = requests.get('https://api.covid19api.com/summary')
    if response.status_code == 200:
        data = response.json()

        for country in data['Countries']:
            if country['Country'] == 'United States of America':
                name = 'United States'
            elif country['Country'] == "Iran, Islamic Republic of":
                name = 'Iran'
            elif country['Country'] == "Korea (South)":
                name = 'South Korea'
            elif country['Country'] == "Macedonia, Republic of":
                name = 'Macedonia'
            elif country['Country'] == "Venezuela (Bolivarian Republic)":
                name = 'Venezuela'
            elif country['Country'] == "Tanzania, United Republic of":
                name = 'Tanzania'
            elif country['Country'] == "Russian Federation":
                name = 'Russia'
            else:
                name = country['Country']

            death_count = country['TotalDeaths']
            confirmed_count = country['TotalConfirmed']
            recovered_count = country['TotalRecovered']
            new_death = country['NewDeaths']
            new_confirmed = country['NewConfirmed']
            new_recovered = country['NewRecovered']

            try:
                death_var = death_count - (death_count - new_death)
                death_percentage = (death_var / (death_count - new_death)) * 100

            except ZeroDivisionError:
                death_percentage = 0

            try:
                confirmed_var = confirmed_count - (confirmed_count - new_confirmed)
                confirmed_percentage = (confirmed_var / (confirmed_count - new_confirmed)) * 100
            except ZeroDivisionError:
                confirmed_percentage = 0

            try:
                recovered_var = recovered_count - (recovered_count - new_recovered)
                recovered_percentage = (recovered_var / (recovered_count - new_recovered)) * 100
            except ZeroDivisionError:
                recovered_percentage = 0

            flag = country['CountryCode']
            obj, created = Country.objects.update_or_create(name=name, defaults={
                                                                            'death_count': death_count, 
                                                                            'confirmed_count': confirmed_count,
                                                                            'recovered_count': recovered_count, 
                                                                            'new_death': new_death, 
                                                                            'new_confirmed': new_confirmed,
                                                                            'new_recovered': new_recovered, 
                                                                            'death_percentage': death_percentage,
                                                                            'confirmed_percentage': confirmed_percentage, 
                                                                            'recovered_percentage': recovered_percentage,
                                                                            'flag': flag,
                                                                        })
    else:
        print('No more requests(countries)!')


def create_country(
                    name, death_count, confirmed_count,
                    recovered_count, new_death, new_confirmed,
                    new_recovered, death_percentage,
                    confirmed_percentage, recovered_percentage,
                    flag
):
    country = Country(
                        name=name,
                        death_count=death_count,
                        confirmed_count=confirmed_count,
                        recovered_count=recovered_count,
                        new_death=new_death,
                        new_confirmed=new_confirmed,
                        new_recovered=new_recovered,
                        death_percentage=death_percentage,
                        confirmed_percentage=confirmed_percentage,
                        recovered_percentage=recovered_percentage,
                        flag=flag
              )
    country.save()
    return country


# Retrieves trending news
@task(name='trending')
def get_top():
    trending = TrendingArticle.objects.all()
    for obj in trending:
        obj.delete()

    reddit = get_reddit()
    top_subs = reddit.subreddit('Coronavirus').top('day', limit=10)

    for sub in top_subs:
        try:
            title = sub.title
            link = sub.url
            create_top(title, link)
        except Exception:
            continue


def create_top(title, link):
    top = TrendingArticle(title=title, link=link)
    top.save()
    return top

def get_reddit():
    return praw.Reddit(
                        client_id=client_id,
                        client_secret=client_secret,
                        grant_type='client_credentials',
                        user_agent='mytestscript/1.0'
           )

# Save vaccination data
@task(name="vaccinations")
def vaccination_stats():
    url = 'https://raw.githubusercontent.com/govex/COVID-19/master/data_tables/vaccine_data/global_data/vaccine_data_global.csv'
    response = urllib.request.urlopen(url)
    lines = [l.decode('utf-8') for l in response.readlines()]
    cr = csv.reader(lines)

    for row in cr:
        if row[0] == "":
            if row[1] == "US":
                stat = row[3]
                set_vaccination_stat('United States', stat)
            elif row[1] == "World":
                stat = row[3]
                global_vaccination_stat(stat)
            else:
                country = row[1]
                stat = row[3]
                set_vaccination_stat(country, stat)
        else:
            continue

def set_vaccination_stat(country, stat):
    try:
        selected_country = get_object_or_404(Country, name=country)

        previous_stat = selected_country.vaccination_count
        try:
            vaccination_var = int(stat) - int(previous_stat)
            vaccination_percentage = (vaccination_var / previous_stat) * 100
        except ZeroDivisionError:
            vaccination_percentage = 0

        selected_country.vaccination_count = stat
        selected_country.new_vaccination_count = vaccination_var
        selected_country.vaccination_percentage = vaccination_percentage
        selected_country.save()
    
    except Exception:
        pass

def global_vaccination_stat(stat):
    records = Record.objects.all()
    for record in records:
        previous_stat = record.vaccination_count
        try:
            vaccination_var = int(stat) - int(previous_stat)
            vaccination_percentage = (vaccination_var / previous_stat) * 100
        except ZeroDivisionError:
            vaccination_percentage = 0

        record.vaccination_count = stat
        record.new_vaccination_count = vaccination_var
        record.vaccination_percentage = vaccination_percentage
        record.save()


# Retrieves stats for states
@task(name='states')
def state_stats():
    features = []
    geolocator = MapBox(mapbox_key, user_agent='covid19')
    url = 'https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_daily_reports/06-15-2021.csv'
    response = urllib.request.urlopen(url)
    lines = [l.decode('utf-8') for l in response.readlines()]
    cr = csv.reader(lines)

    for row in cr:
        if row[0] == "" and row[1] == "" and row[2] != "":
            state_name = row[2]
            confirmed = row[7]
            deaths = row[8]
            recovered = row[9]
            try:
                location = geolocator.geocode(row[2], timeout=20000)
            except:
                print(row[2])
                continue
            point = Point((location.longitude, location.latitude))
            
            try:
                features.append(Feature(geometry=point,
                                        properties={
                                                "Place": state_name,
                                                "Confirmed": confirmed,
                                                "Recovered": recovered,
                                                "Deaths": deaths,
                                            }))
            except ValueError:
                print(state_name + "ERROR")
                continue
        elif row[0] != "":
            city_name = row[2]
            confirmed = row[7]
            deaths = row[8]
            recovered = row[9]
            try:
                location = geolocator.geocode(row[2], timeout=20000)
            except:
                print(row[2])
                continue
            point = Point((location.longitude, location.latitude))
            
            try:
                features.append(Feature(geometry=point,
                                        properties={
                                                "Place": city_name,
                                                "Confirmed": confirmed,
                                                "Recovered": recovered,
                                                "Deaths": deaths,
                                            }))
            except ValueError:
                print(state_name + "ERROR")
                continue
        else:
            continue

    feature_collection = FeatureCollection(features)
    with open('covid19.json', 'w') as f:
        json.dump(feature_collection, f)

# Create json file with world's historical data
@task(name='global-historical-data')
def get_historical_data():
    url = "https://covid-193.p.rapidapi.com/history"
    querystring = {"country":"All"}
    headers = {
        'x-rapidapi-key': "4652b15facmshd13fc1cecd67653p17373fjsn8b3a699c6a28",
        'x-rapidapi-host': "covid-193.p.rapidapi.com"
    }

    response = requests.request("GET", url, headers=headers, params=querystring)
    data = response.json()

    with open('historical_data.json', 'w') as f:
        json.dump(data, f)

# Save world's historical data into database
@task(name='save-global-historical-data')
def save_global_historical_data():
    file = open('historical_data.json')
    data = json.load(file)

    date = ''
    for stat in data['response']:
        if date == stat['day']:
            continue
        else:
            if "+" in stat['deaths']['new']:
                death_count = stat['deaths']['new']
                new_deaths = death_count.replace("+", "")
            else:
                new_deaths = stat['deaths']['new']

            if "+" in stat['cases']['new']:
                confirmed_count = stat['cases']['new']
                new_cases = confirmed_count.replace("+", "")
            else:
                new_cases = stat['cases']['new']

            death_data = ChartDeathData(date=date, total_death=new_deaths)
            confirmed_data = ChartConfirmedData(date=date, total_confirmed=new_cases)
            death_data.save()
            confirmed_data.save()

            date = stat['day']
            
# Save historical vaccination count for world
@task(name="save-global-vaccination-data")
def save_global_vaccination_data():
    url = 'https://raw.githubusercontent.com/govex/COVID-19/master/data_tables/vaccine_data/global_data/time_series_covid19_vaccine_global.csv'
    response = urllib.request.urlopen(url)
    lines = [l.decode('utf-8') for l in response.readlines()]
    cr = csv.reader(lines)

    for row in cr:
        if row[0] == "World":
            date = row[1]
            vaccination_count = row[2]

            chart_data = ChartVaccinationData(date=date, total_vaccination=vaccination_count)
            chart_data.save()

# Save historical confirmed and death cases for every country
@task(name="save-country-historical-data")
def save_country_historical_data():
    with open('global-data.csv', 'r') as file:
        reader = csv.reader(file)
        next(reader)
        for row in reader:
            country = row[2]
            date = row[0]
            new_cases = row[4]
            new_deaths = row[6]
            
            historical_case = HistoricalConfirmedData(country=country, date=date, total_confirmed=new_cases)
            historical_death = HistoricalDeathData(country=country, date=date, total_death=new_deaths)

            historical_case.save()
            historical_death.save()

# Save historical vaccination data for every country
@task(name="save-country-vaccination-data")
def save_country_vaccination_data():
    url = 'https://raw.githubusercontent.com/govex/COVID-19/master/data_tables/vaccine_data/global_data/time_series_covid19_vaccine_global.csv'
    response = urllib.request.urlopen(url)
    lines = [l.decode('utf-8') for l in response.readlines()]
    cr = csv.reader(lines)
    next(cr)

    for row in cr:
        if row[0] != "World":
            country = row[0]
            date = row[1]
            vaccination_count = row[2]

            chart_data = HistoricalVaccinationData(country=country, date=date, total_vaccination=vaccination_count)
            chart_data.save()
        else:
            continue