# Generated by Django 3.0.2 on 2020-06-01 09:13

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('stats', '0006_unemployment'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='country',
            options={'ordering': ['-confirmed_count', '-death_count', '-recovered_count']},
        ),
    ]
