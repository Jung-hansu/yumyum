# Generated by Django 4.2.4 on 2023-10-16 11:19

import django.contrib.gis.db.models.fields
import django.contrib.postgres.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Manager',
            fields=[
                ('manager_id', models.AutoField(primary_key=True, serialize=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
            options={
                'db_table': 'Manager',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='OperatingHours',
            fields=[
                ('operating_id', models.AutoField(primary_key=True, serialize=False)),
                ('day_of_week', models.IntegerField(blank=True, null=True)),
                ('start_time', models.DateTimeField(blank=True, null=True)),
                ('end_time', models.DateTimeField(blank=True, null=True)),
                ('etc_reason', models.TextField(blank=True, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
            options={
                'db_table': 'Operating_hours',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Restaurant',
            fields=[
                ('restaurant_id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=30)),
                ('category', django.contrib.postgres.fields.ArrayField(base_field=models.IntegerField(), size=None)),
                ('longitude', models.DecimalField(decimal_places=7, max_digits=10)),
                ('latitude', models.DecimalField(decimal_places=7, max_digits=10)),
                ('location', django.contrib.gis.db.models.fields.PointField(null=True)),
                ('waiting', models.IntegerField(blank=True, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
            options={
                'db_table': 'Restaurant',
                'managed': False,
            },
        ),
    ]
