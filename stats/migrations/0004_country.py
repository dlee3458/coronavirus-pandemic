# Generated by Django 3.0.2 on 2020-05-27 08:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('stats', '0003_record'),
    ]

    operations = [
        migrations.CreateModel(
            name='Country',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=150)),
                ('death_count', models.IntegerField()),
                ('confirmed_count', models.IntegerField()),
                ('recovered_count', models.IntegerField()),
            ],
        ),
    ]
