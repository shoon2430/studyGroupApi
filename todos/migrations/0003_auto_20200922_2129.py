# Generated by Django 3.0.4 on 2020-09-22 12:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('todos', '0002_auto_20200918_2007'),
    ]

    operations = [
        migrations.AddField(
            model_name='todo',
            name='end',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='todo',
            name='start',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='todogroup',
            name='end',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='todogroup',
            name='start',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]
