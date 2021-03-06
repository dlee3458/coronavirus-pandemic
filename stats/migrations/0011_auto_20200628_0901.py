# Generated by Django 3.0.2 on 2020-06-28 09:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('stats', '0010_country_flag'),
    ]

    operations = [
        migrations.AddField(
            model_name='country',
            name='new_confirmed',
            field=models.IntegerField(default=0),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='country',
            name='new_death',
            field=models.IntegerField(default=0),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='country',
            name='new_recovered',
            field=models.IntegerField(default=0),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='record',
            name='new_confirmed',
            field=models.IntegerField(default=0),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='record',
            name='new_death',
            field=models.IntegerField(default=0),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='record',
            name='new_recovered',
            field=models.IntegerField(default=0),
            preserve_default=False,
        ),
    ]
