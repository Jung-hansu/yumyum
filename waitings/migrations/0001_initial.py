# Generated by Django 4.2.4 on 2023-10-16 11:19

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='WaitingUser',
            fields=[
                ('waiting_user_id', models.IntegerField(primary_key=True, serialize=False)),
                ('position', models.IntegerField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
            options={
                'db_table': 'Waiting_User',
                'managed': False,
            },
        ),
    ]
