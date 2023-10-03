# Generated by Django 4.2.4 on 2023-10-03 11:22

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Review',
            fields=[
                ('review_id', models.AutoField(primary_key=True, serialize=False)),
                ('stars', models.IntegerField()),
                ('contents', models.CharField(blank=True, max_length=500, null=True)),
                ('created_at', models.DateTimeField(blank=True, null=True)),
                ('updated_at', models.DateTimeField(blank=True, null=True)),
            ],
            options={
                'db_table': 'Review',
                'managed': False,
            },
        ),
    ]
