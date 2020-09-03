from django.shortcuts import render
from django.views.generic import ListView
from .models import Article, TrendingArticle
import requests
import json
import geojson
from stats.models import Record, Country, Unemployment
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
