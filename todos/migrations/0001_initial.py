# Generated by Django 3.0.4 on 2020-09-02 13:56

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('core', '0002_auto_20200902_2254'),
    ]

    operations = [
        migrations.CreateModel(
            name='Subject',
            fields=[
                ('timestampmodel_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='core.TimeStampModel')),
                ('time', models.IntegerField(default=1)),
                ('title', models.CharField(max_length=300)),
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
                ('subject_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='todos.Subject')),
            ],
            bases=('core.timestampmodel',),
        ),
    ]