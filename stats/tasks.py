# from __future__ import absolute_import, unicode_literals

from stats.models import Record, Country, Unemployment
from news.models import TrendingArticle, Article
import requests
import praw 
from newspaper import Article as art
from geopy.geocoders import MapBox
import json 
from geojson import Point, Feature, FeatureCollection, dump
from celery import task
# from redis import Redis
# from django_rq import job
# import django_rq

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
        record = Record(total_death=total_death, total_confirmed=total_confirmed, total_recovered=total_recovered, 
                        new_death=new_death, new_confirmed=new_confirmed, new_recovered=new_recovered, death_percentage=death_percentage,
                        confirmed_percentage=confirmed_percentage, recovered_percentage=recovered_percentage)
        
        numbers = Record.objects.all()
        for obj in numbers:
            obj.delete()

        record.save()
        return record
    else: 
        print('No more requests(stats)!')

@task(name='countries')
def get_countries():     
    countries = Country.objects.all()
    for obj in countries:
        obj.delete()
    
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
            create_country(name, death_count, confirmed_count, recovered_count, new_death, new_confirmed, new_recovered, death_percentage, confirmed_percentage, recovered_percentage, flag)
    else:
        print('No more requests(countries)!')


def create_country(name, death_count, confirmed_count, recovered_count, new_death, new_confirmed, new_recovered, death_percentage, confirmed_percentage, recovered_percentage, flag):
    country = Country(name=name, death_count=death_count, confirmed_count=confirmed_count, recovered_count=recovered_count, 
                        new_death=new_death, new_confirmed=new_confirmed, new_recovered=new_recovered, death_percentage=death_percentage, 
                        confirmed_percentage=confirmed_percentage, recovered_percentage=recovered_percentage, flag=flag)
    country.save()
    return country

@task(name='trending')
def get_top():
    trending = TrendingArticle.objects.all()
    for obj in trending:
        obj.delete()
        
    reddit = get_reddit()
    top_subs = reddit.subreddit('Coronavirus').top('day', limit=6)

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

@task(name='new')
def get_new():
    articles = Article.objects.all()
    for obj in articles:
        obj.delete()
        
    reddit = get_reddit()
    new_subs = reddit.subreddit('Coronavirus').new(limit=16)

    for sub in new_subs:
        try:
            title = sub.title
            link = sub.url
            create_new(title, link)
        except Exception:
            continue

def create_new(title, link):
    new = Article(title=title, link=link)
    new.save()
    return new

def get_reddit():
    return praw.Reddit(client_id='c8i9Dx-OesYKww',
                        client_secret='4JIEJxvxDtU4jDd-RwIG8Srlfss',
                        grant_type='client_credentials',
                        user_agent='mytestscript/1.0')

@task(name='rate')
def get_rate():
    rates = Unemployment.objects.all()
    for obj in rates:
        obj.delete()

    response = requests.get('https://api.bls.gov/publicAPI/v2/timeseries/data/LNS14000000?latest=true')
    data = response.json()

    rate = data['Results']['series'][0]['data'][0]['value']
    unemployment_rate = Unemployment(rate=rate)
    unemployment_rate.save()
    return unemployment_rate                       

@task(name='states')
def state_stats():
    geolocator = MapBox('pk.eyJ1IjoiZGxlZTM0NTgiLCJhIjoiY2thbm44bmdoMXJoMjMwcWhwYnl2b2tyeCJ9.A6LbEzv-FlxtLfgT0tY_9Q', user_agent='covid19')
    country_r = requests.get("https://api-corona.azurewebsites.net/country").json()
    countries = []
    features = []
    
    for country in country_r:
        countries.append(country["Slug"])

    data = requests.get("https://api-corona.azurewebsites.net/country/us").json()
    for name in countries:
        url = "https://api-corona.azurewebsites.net/country/{}".format(name.lower())
        data = requests.get(url).json()

        if "State" in data:
            for state in data['State']:
                state_name = state['Province_State']
                
                try:
                    location = geolocator.geocode(state['Province_State'], timeout=20000)
                except:
                    print(state['Province_State'])
                    continue
                
                try:
                    confirmed = "{:,}".format(state['Confirmed'])
                except KeyError:
                    print(state['Province_State'])
                    continue
                
                recovered = "{:,}".format(state['Recovered'])
                deaths = "{:,}".format(state['Deaths'])
                point = Point((location.longitude, location.latitude))


                try:
                    features.append(Feature(geometry=point, properties={
                                                                    "State": state_name,
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