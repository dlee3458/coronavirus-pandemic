from django.shortcuts import get_object_or_404, render
from django.template.loader import render_to_string
from django.views.generic import ListView
from .models import Article, TrendingArticle
import requests
import json
import geojson
from stats.models import Record, Country, Unemployment, ChartConfirmedData, ChartDeathData, ChartVaccinationData, HistoricalConfirmedData, HistoricalDeathData, HistoricalVaccinationData
from django.http import JsonResponse


def about(request):
    return render(request, 'news/about.html')


def json_list(request):
    with open('covid19.json') as json_file:
        data_reader = json.load(json_file)
        data = json.dumps(data_reader, ensure_ascii=False)

        # data2 = data.decode()
    context = {
        'data': data
    }
    return render(request, 'news/worldstats_geojson.html', context)

def get_country_stats(request, country):
     if request.is_ajax():
        if request.method == "GET":
            context = {}
            country = get_object_or_404(Country, id=country)
            context['country'] = country
            
            html = render_to_string('news/country_stats_ajax.html', context, request=request)
            return JsonResponse({'stats': html})

def get_global_stats(request):
    if request.is_ajax():
        if request.method == 'GET':
            context = {}
            global_stats = Record.objects.all()
            context['global_stats'] = global_stats

            html = render_to_string('news/global_stats_ajax.html', context, request=request)
            return JsonResponse({'stats': html})

class NewsListView(ListView):
    model = Article
    template_name = 'news/news.html'
    context_object_name = 'articles'

    def get_context_data(self, **kwargs):
        context = super(NewsListView, self).get_context_data(**kwargs)
        context['trending'] = TrendingArticle.objects.all()
        return context


class HomeListView(ListView):
    model = Country
    template_name = 'news/home.html'
    context_object_name = 'countries'

    def get_context_data(self, **kwargs):
        context = super(HomeListView, self).get_context_data(**kwargs)
        context['stats'] = Record.objects.all()
        context['rates'] = Unemployment.objects.all()
        context['trending'] = TrendingArticle.objects.all()
        context['articles'] = Article.objects.all()
        return context

def get_global_chart(request):
    if request.is_ajax():
        if request.method == 'GET':
            confirmed_dates = []
            death_dates = []
            vaccination_dates = []
            confirmed_count = []
            death_count = []
            vaccination_count = []

            confirmed_data = ChartConfirmedData.objects.all()
            death_data = ChartDeathData.objects.all()
            vaccination_data = ChartVaccinationData.objects.all()

            for confirmed in confirmed_data:
                confirmed_dates.insert(0, confirmed.date)
                confirmed_count.insert(0, confirmed.total_confirmed)

            for death in death_data:
                death_dates.insert(0, death.date)
                death_count.insert(0, death.total_death)

            for vaccination in vaccination_data:
                vaccination_dates.append(vaccination.date)
                vaccination_count.append(vaccination.total_vaccination)

            html = render_to_string('news/charts_ajax.html', request=request)

            return JsonResponse({
                'data': {
                    'confirmed_labels': confirmed_dates,
                    'death_labels': death_dates,
                    'vaccination_labels': vaccination_dates,
                    'confirmed_data': confirmed_count,
                    'death_data': death_count,
                    'vaccination_data': vaccination_count,
                    'html': html
                }
            })

def get_country_chart(request, country):
    if request.is_ajax():
        if request.method == 'GET':
            date_cases = []
            date_deaths = []
            date_vaccination = []
            confirmed_count = []
            death_count = []
            vaccination_count = []

            confirmed_data = HistoricalConfirmedData.objects.filter(country=country)
            death_data = HistoricalDeathData.objects.filter(country=country)
            vaccination_data = HistoricalVaccinationData.objects.filter(country=country)

            for confirmed in confirmed_data:
                if confirmed.date in date_cases:
                    continue
                else:
                    date_cases.append(confirmed.date)
                    confirmed_count.append(confirmed.total_confirmed)

            for death in death_data:
                if death.date in date_deaths:
                    continue
                else:
                    date_deaths.append(death.date)
                    death_count.append(death.total_death)

            for vaccination in vaccination_data:
                if vaccination.date in date_vaccination:
                    continue
                else:
                    date_vaccination.append(vaccination.date)
                    vaccination_count.append(vaccination.total_vaccination)

            html = render_to_string('news/charts_ajax.html', request=request)

            return JsonResponse({
                'data': {
                    'confirmed_labels': date_cases,
                    'death_labels': date_deaths,
                    'vaccination_labels': date_vaccination,
                    'confirmed_data': confirmed_count,
                    'death_data': death_count,
                    'vaccination_data': vaccination_count,
                    'html': html
                }
            })
