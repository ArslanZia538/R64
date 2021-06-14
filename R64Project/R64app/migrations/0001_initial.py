# Generated by Django 2.1.7 on 2021-06-02 19:39

import datetime
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Cash',
            fields=[
                ('cash_id', models.AutoField(primary_key=True, serialize=False)),
                ('amount', models.IntegerField()),
                ('event', models.CharField(max_length=255)),
                ('date', models.DateField(default=datetime.date.today)),
                ('status', models.BooleanField(default=False)),
                ('giver', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='cash_giver', to=settings.AUTH_USER_MODEL)),
                ('receiver', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='cash_receiver', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='History',
            fields=[
                ('history_id', models.AutoField(primary_key=True, serialize=False)),
                ('amount', models.IntegerField()),
                ('event', models.CharField(max_length=255)),
                ('date', models.DateField(default=datetime.date.today)),
                ('status', models.BooleanField(default=True)),
                ('giver', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='history_giver', to=settings.AUTH_USER_MODEL)),
                ('receiver', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='history_receiver', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
