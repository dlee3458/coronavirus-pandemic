# Generated by Django 3.1 on 2021-06-15 09:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('stats', '0021_record_vaccination_count'),
    ]

    operations = [
        migrations.AlterField(
            model_name='record',
            name='vaccination_count',
            field=models.BigIntegerField(default=0),
        ),
    ]
