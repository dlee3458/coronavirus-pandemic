from django.contrib import admin
from .models import Article, TrendingArticle

admin.site.register(Article)
admin.site.register(TrendingArticle)
