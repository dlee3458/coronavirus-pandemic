# Generated by Django 3.1 on 2021-06-22 02:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('stats', '0029_chartvaccinationdata'),
    ]

    operations = [
        migrations.CreateModel(
            name='HistoricalConfirmedData',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('country', models.CharField(max_length=200)),
                ('date', models.CharField(max_length=200)),
                ('total_confirmed', models.BigIntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='HistoricalDeathData',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('country', models.CharField(max_length=200)),
                ('date', models.CharField(max_length=200)),
                ('total_death', models.BigIntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='HistoricalVaccinationData',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('country', models.CharField(max_length=200)),
                ('date', models.CharField(max_length=200)),
                ('total_vaccination', models.BigIntegerField()),
            ],
        ),
    ]