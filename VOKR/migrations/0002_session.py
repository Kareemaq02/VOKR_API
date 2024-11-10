# Generated by Django 5.0.3 on 2024-11-02 15:14

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('vokr_app', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Session',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('session_id', models.CharField(max_length=255, unique=True)),
                ('created_at', models.DateTimeField(default=django.utils.timezone.now)),
                ('last_accessed_at', models.DateTimeField(auto_now=True)),
            ],
        ),
    ]