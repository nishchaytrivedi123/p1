# Generated by Django 3.0.2 on 2025-02-02 03:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('p1', '0004_weddingguest_last_login'),
    ]

    operations = [
        migrations.AddField(
            model_name='weddingguest',
            name='message',
            field=models.CharField(blank=True, max_length=250, null=True),
        ),
    ]
