# Generated by Django 3.0.4 on 2020-09-12 13:13

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('todos', '0002_auto_20200911_2308'),
    ]

    operations = [
        migrations.RenameField(
            model_name='subject',
            old_name='master',
            new_name='group_id',
        ),
        migrations.RenameField(
            model_name='todo',
            old_name='master',
            new_name='todoGroup_id',
        ),
        migrations.RenameField(
            model_name='todogroup',
            old_name='master',
            new_name='subject_id',
        ),
    ]
