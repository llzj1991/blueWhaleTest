# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2019-06-06 13:33
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home_application', '0002_diskusage'),
    ]

    operations = [
        migrations.AlterField(
            model_name='diskusage',
            name='add_time',
            field=models.DateTimeField(auto_now=True, max_length=0, verbose_name='录入时间'),
        ),
    ]