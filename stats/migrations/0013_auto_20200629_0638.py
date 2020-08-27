# Generated by Django 3.0.2 on 2020-06-29 06:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('stats', '0012_auto_20200629_0611'),
    ]

    operations = [
        migrations.AlterField(
            model_name='country',
            name='confirmed_percentage',
            field=models.DecimalField(decimal_places=2, max_digits=5),
        ),
        migrations.AlterField(
            model_name='country',
            name='death_percentage',
            field=models.DecimalField(decimal_places=2, max_digits=5),
        ),
        migrations.AlterField(
            model_name='country',
            name='recovered_percentage',
            field=models.DecimalField(decimal_places=2, max_digits=5),
        ),
        migrations.AlterField(
            model_name='record',
            name='confirmed_percentage',
            field=models.DecimalField(decimal_places=2, max_digits=5),
        ),
        migrations.AlterField(
            model_name='record',
            name='death_percentage',
            field=models.DecimalField(decimal_places=2, max_digits=5),
        ),
        migrations.AlterField(
            model_name='record',
            name='recovered_percentage',
            field=models.DecimalField(decimal_places=2, max_digits=5),
        ),
    ]
