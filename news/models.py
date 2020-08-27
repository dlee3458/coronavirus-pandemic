from django.db import models
import praw
import requests
from newspaper import Article as art
    
class Article(models.Model):
    title = models.CharField(max_length=200)
    link = models.URLField()
    # image = models.ImageField(default="")

    def __str__(self):
        return self.title

class TrendingArticle(models.Model):
    title = models.CharField(max_length=200)
    link = models.URLField()
    # image = models.ImageField(default="")

    def __str__(self):
        return self.title

