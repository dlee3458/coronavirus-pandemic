# Generated by Django 3.1 on 2021-06-16 01:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('stats', '0025_auto_20210615_0933'),
    ]

    operations = [
        migrations.AlterField(
            model_name='record',
            name='new_vaccination_count',
            field=models.BigIntegerField(default=0, null=True),
        ),
    ]
