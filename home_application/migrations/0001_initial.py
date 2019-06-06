# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2019-05-30 14:26
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Computer',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=64)),
                ('ipCode', models.CharField(max_length=32)),
                ('systemType', models.CharField(max_length=16)),
                ('disk', models.CharField(max_length=16)),
                ('proportion', models.CharField(max_length=16)),
                ('remarks', models.CharField(max_length=256, null=True)),
                ('creat_at', models.DateTimeField()),
                ('update_at', models.DateTimeField(auto_now=True)),
            ],
        ),
    ]