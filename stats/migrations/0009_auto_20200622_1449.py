# Generated by Django 3.0.2 on 2020-06-22 14:49

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('stats', '0008_auto_20200618_0739'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='country',
            name='latitude',
        ),
        migrations.RemoveField(
            model_name='country',
            name='longitude',
        ),
    ]
