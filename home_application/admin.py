# -*- coding: utf-8 -*-
from django.contrib import admin

# Register your models here.

from home_application.models import Computer,DiskUsages

admin.site.register(Computer)
admin.site.register(DiskUsages)