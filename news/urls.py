from django.urls import path
from .views import HomeListView, NewsListView, json_list
from . import views

urlpatterns = [
    # path('', IndexListView.as_view(), name='news-home'),
    path('about/', views.about, name='about'),
    path('', views.HomeListView.as_view(), name='home'),
    path('news/', views.NewsListView.as_view(), name='news'),
    path('worldstats.json/', views.json_list, name='json_list'),
    path('stats/<str:country>/', views.get_country_stats, name='get-country-stats'),
    path('global_stats/', views.get_global_stats, name='get-global-stats'),
    path('chart/<str:country>/', views.get_country_chart, name='get-country-chart'),
    path('global_chart', views.get_global_chart, name='get-global-chart'),
]
