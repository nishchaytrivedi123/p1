# Generated by Django 3.0.2 on 2025-01-13 04:09

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('p1', '0003_auto_20250105_1706'),
    ]

    operations = [
        migrations.AddField(
            model_name='weddingguest',
            name='last_login',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
    ]
