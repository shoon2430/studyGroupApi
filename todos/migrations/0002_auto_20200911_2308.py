# Generated by Django 3.0.4 on 2020-09-11 14:08

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('groups', '0002_auto_20200911_2308'),
        ('todos', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='todogroup',
            name='leader',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='todo_Leader', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='todogroup',
            name='master',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='subject', to='todos.Subject'),
        ),
        migrations.AddField(
            model_name='todogroup',
            name='members',
            field=models.ManyToManyField(blank=True, related_name='todo_members', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='todo',
            name='master',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='todo_group', to='todos.TodoGroup'),
        ),
        migrations.AddField(
            model_name='todo',
            name='writer',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='todo_writer', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='subject',
            name='master',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='group', to='groups.Group'),
        ),
        migrations.AddField(
            model_name='subject',
            name='writer',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='subject_writer', to=settings.AUTH_USER_MODEL),
        ),
    ]
