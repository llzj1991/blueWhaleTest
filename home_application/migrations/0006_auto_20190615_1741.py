# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2019-06-15 17:41
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home_application', '0005_auto_20190614_1604'),
    ]

    operations = [
        migrations.AlterField(
            model_name='diskusage',
            name='disk',
            field=models.CharField(default='usr/', max_length=16, verbose_name='磁盘'),
        ),
    ]