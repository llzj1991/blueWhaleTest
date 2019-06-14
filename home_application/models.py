# -*- coding: utf-8 -*-
from django.db import models
# Create your models here.
class Computer(models.Model):
    name = models.CharField(max_length=64)  # 主机名
    ipCode = models.CharField(max_length=32) #I P地址
    systemType = models.CharField(max_length=16)  # 系统类型
    disk = models.CharField(max_length=16)  # 磁盘
    proportion = models.CharField(max_length=16)  # 使用率
    remarks = models.CharField(max_length=256, null=True)   #备注
    creat_at = models.DateTimeField(auto_now_add=False)
    update_at = models.DateTimeField(auto_now = True)

    # def __unicode__(self):
    #     return self.name

class DiskUsage(models.Model):
    ip = models.CharField('ip地址',default='10.0.1.80',max_length=32)
    system  = models.CharField('系统',max_length=16,default='linux')  # 系统类型
    disk = models.CharField('磁盘',max_length=16,default='/usr/')  # 磁盘
    file_system = models.CharField('系统文件', max_length=64)
    disk_capacity = models.CharField('磁盘容量', max_length=64)
    disk_used = models.CharField('磁盘已用', max_length=64)
    disk_able = models.CharField('磁盘可用', max_length=64)
    disk_rate = models.CharField('磁盘使用率', max_length=64)
    disk_mount = models.CharField('挂载点', max_length=64)
    add_time = models.DateTimeField('录入时间', auto_now=True, max_length=0)

