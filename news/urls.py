from django.urls import path
from .views import HomeListView, NewsListView, json_list
from . import views

urlpatterns = [
    # path('', IndexListView.as_view(), name='news-home'),
    path('about/', views.about, name='about'),
    path('', views.HomeListView.as_view(), name='home'),
    path('news/', views.NewsListView.as_view(), name='news'),
    path('worldstats.json/', views.json_list, name='json_list')
]
