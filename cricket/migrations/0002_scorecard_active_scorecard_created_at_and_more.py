# Generated by Django 5.0.7 on 2025-01-06 08:01

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cricket', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='scorecard',
            name='active',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='scorecard',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='scorecard',
            name='updated_at',
            field=models.DateTimeField(auto_now=True),
        ),
    ]
