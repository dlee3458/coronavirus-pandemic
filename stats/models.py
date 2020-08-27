from django.db import models
from django.utils import timezone
import requests 
from django_countries.fields import CountryField

class Record(models.Model):
    total_death = models.IntegerField()
    total_confirmed = models.IntegerField()
    total_recovered = models.IntegerField()
    new_death = models.IntegerField()
    new_confirmed = models.IntegerField()
    new_recovered = models.IntegerField()
    last_updated = models.DateTimeField(default=timezone.now)
    death_percentage = models.DecimalField(max_digits=5, decimal_places=2)
    confirmed_percentage = models.DecimalField(max_digits=5, decimal_places=2)
    recovered_percentage = models.DecimalField(max_digits=5, decimal_places=2)

class Country(models.Model):
    name = models.CharField(max_length=150)
    death_count = models.IntegerField()
    confirmed_count = models.IntegerField()
    recovered_count = models.IntegerField()
    new_death = models.IntegerField()
    new_confirmed = models.IntegerField()
    new_recovered = models.IntegerField()
    death_percentage = models.DecimalField(max_digits=5, decimal_places=2)
    confirmed_percentage = models.DecimalField(max_digits=5, decimal_places=2)
    recovered_percentage = models.DecimalField(max_digits=5, decimal_places=2)
    flag = CountryField()
    
    def __str__(self):
        return self.name

    class Meta:
        ordering = ['-confirmed_count', '-death_count', '-recovered_count']

class Unemployment(models.Model):
    rate = models.CharField(max_length=200)

    