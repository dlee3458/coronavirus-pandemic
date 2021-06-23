# Generated by Django 3.1 on 2021-06-15 09:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('stats', '0022_auto_20210615_0907'),
    ]

    operations = [
        migrations.AddField(
            model_name='country',
            name='new_vaccination_count',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='country',
            name='vaccination_percentage',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=5),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='record',
            name='new_vaccination_count',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='record',
            name='vaccination_percentage',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=5),
            preserve_default=False,
        ),
    ]
