# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2017-11-07 12:59
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0005_fbapplication'),
    ]

    operations = [
        migrations.AddField(
            model_name='eventworker',
            name='page_id',
            field=models.CharField(default='', max_length=200),
            preserve_default=False,
        ),
    ]