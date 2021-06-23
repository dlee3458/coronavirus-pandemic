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
    vaccination_count = models.BigIntegerField(default=0,null=True)
    new_vaccination_count = models.BigIntegerField(default=0, null=True)
    vaccination_percentage = models.DecimalField(max_digits=5, decimal_places=2, null=True)


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
    vaccination_count = models.IntegerField(default=0, null=True)
    new_vaccination_count = models.IntegerField(default=0, null=True)
    vaccination_percentage = models.DecimalField(max_digits=5, decimal_places=2, null=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['-confirmed_count', '-death_count', '-recovered_count']


class Unemployment(models.Model):
    rate = models.CharField(max_length=200)


class ChartConfirmedData(models.Model):
    date = models.CharField(max_length=200)
    total_confirmed = models.BigIntegerField()

    def __str__(self):
        return self.date

class ChartDeathData(models.Model):
    date = models.CharField(max_length=200)
    total_death = models.BigIntegerField()

    def __str__(self):
        return self.date

class ChartVaccinationData(models.Model):
    date = models.CharField(max_length=200)
    total_vaccination = models.BigIntegerField()

    def __str__(self):
        return self.date

class HistoricalConfirmedData(models.Model):
    country = models.CharField(max_length=200)
    date = models.CharField(max_length=200)
    total_confirmed = models.BigIntegerField()

    def __str__(self):
        return(self.country + ' ' + self.date)

class HistoricalDeathData(models.Model):
    country = models.CharField(max_length=200)
    date = models.CharField(max_length=200)
    total_death = models.BigIntegerField()

    def __str__(self):
        return(self.country + ' ' + self.date)

class HistoricalVaccinationData(models.Model):
    country = models.CharField(max_length=200)
    date = models.CharField(max_length=200)
    total_vaccination = models.BigIntegerField()

    def __str__(self):
        return(self.country + ' ' + self.date)
