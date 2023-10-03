# Generated by Django 4.2.4 on 2023-10-03 11:22

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Manager',
            fields=[
                ('manager_id', models.AutoField(primary_key=True, serialize=False)),
                ('restaurant_id', models.IntegerField(unique=True)),
                ('created_at', models.DateTimeField(blank=True, null=True)),
                ('updated_at', models.DateTimeField(blank=True, null=True)),
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
                ('restaurant_id', models.IntegerField(unique=True)),
                ('day_of_week', models.IntegerField(blank=True, null=True)),
                ('start_time', models.DateTimeField(blank=True, null=True)),
                ('end_time', models.DateTimeField(blank=True, null=True)),
                ('etc_reason', models.TextField(blank=True, null=True)),
                ('created_at', models.DateField()),
                ('updated_at', models.DateField()),
            ],
            options={
                'db_table': 'Operating_hours',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Restaurant',
            fields=[
                ('restaurant', models.OneToOneField(on_delete=django.db.models.deletion.DO_NOTHING, primary_key=True, serialize=False, to='restaurants.operatinghours')),
                ('name', models.CharField(max_length=30)),
                ('category', models.CharField(max_length=30)),
                ('longitude', models.DecimalField(decimal_places=65535, max_digits=65535)),
                ('latitude', models.DecimalField(decimal_places=65535, max_digits=65535)),
                ('waiting', models.IntegerField(blank=True, null=True)),
                ('created_at', models.DateTimeField(blank=True, null=True)),
                ('updated_at', models.DateTimeField(blank=True, null=True)),
            ],
            options={
                'db_table': 'Restaurant',
                'managed': False,
            },
        ),
    ]
