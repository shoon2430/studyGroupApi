# Generated by Django 3.0.4 on 2020-09-18 11:07

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Subject',
            fields=[
                ('timestampmodel_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='core.TimeStampModel')),
                ('time', models.IntegerField(default=1)),
                ('title', models.CharField(max_length=300)),
                ('description', models.TextField(blank=True, max_length=1000, null=True)),
            ],
            bases=('core.timestampmodel',),
        ),
        migrations.CreateModel(
            name='Todo',
            fields=[
                ('timestampmodel_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='core.TimeStampModel')),
                ('time', models.IntegerField(default=1)),
                ('title', models.CharField(max_length=300)),
                ('progress', models.CharField(choices=[('CREATE', 'Create'), ('DOING', 'Doing'), ('COMPLETED', 'Completed')], max_length=20)),
            ],
            bases=('core.timestampmodel',),
        ),
        migrations.CreateModel(
            name='TodoGroup',
            fields=[
                ('timestampmodel_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='core.TimeStampModel')),
                ('time', models.IntegerField(default=1)),
                ('title', models.CharField(max_length=300)),
                ('progress', models.CharField(choices=[('CREATE', 'Create'), ('DOING', 'Doing'), ('COMPLETED', 'Completed')], default='CREATE', max_length=20)),
            ],
            bases=('core.timestampmodel',),
        ),
    ]
