# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2017-11-22 09:26
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0011_auto_20171122_1056'),
    ]

    operations = [
        migrations.AlterField(
            model_name='event',
            name='attending_count',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]