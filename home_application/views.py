# -*- coding: utf-8 -*-
import subprocess, time, json
from django.shortcuts import render,redirect,reverse,HttpResponse
from django.core import serializers
from django.http import JsonResponse
from django.utils import timezone
from blueapps.account.decorators import login_exempt
from blueking.component.shortcuts import get_client_by_request
from home_application import models

# dev.class.o.qcloud.com
# 开发框架中通过中间件默认是需要登录态的，如有不需要登录的，可添加装饰器login_exempt
# 装饰器引入 from blueapps.account.decorators import login_exempt

@login_exempt
def home(request):
    """首页"""
    return render(request, 'home_application/home.html')

@login_exempt
def modelsData(request):
    """"""
    return render(request, 'home_application/modelsData.html')

@login_exempt
def getModelsData(request):
    """helloworld"""
    if request.method == 'POST':  # 当提交post时
        name = request.POST.get('name',None)
        ipCode = request.POST.get('ipCode', None)
        systemType = request.POST.get('optionsRadios', None)
        disk = request.POST.get('disk', None)
        proportion = request.POST.get('proportion', None)
        remarks = request.POST.get('remarks', None)
        creat_at = timezone.now().strftime("%Y-%m-%d %H:%M")
        update_at = timezone.now().strftime("%Y-%m-%d %H:%M")
        obj = models.Computer.objects.create(name=name,ipCode=ipCode,systemType=systemType,disk=disk,proportion=proportion,remarks=remarks,creat_at=creat_at,update_at=update_at)
        obj.save()
    data = {}
    data["catalogues"]={"id":"编号","name":"主机名字","ipCode":"IP地址","systemType":"系统类型","disk":"磁盘信息","proportion":"使用率","remarks":"备注","update_at":"更新时间","creat_at":"创建时间",}
    book = models.Computer.objects.values()
    data["items"] = list(book)
    items = list(book)
    for item in items:
        item["creat_at"] = str(item["creat_at"].strftime("%Y-%m-%d %H:%M"))
        item["update_at"] = str(item["update_at"].strftime("%Y-%m-%d %H:%M"))
    return JsonResponse(data,safe=False)

@login_exempt
def helloworld(request):
    """helloworld"""
    return render(request,'home_application/helloworld.html')

@login_exempt
def helloBlueking(request):
    """helloBlueking"""
    if request.method == 'POST':  # 当提交表单时
        inputText = request.POST.get('inputText',None)
        if inputText == "Hello Blueking":
            return render(request,'home_application/helloBlueking.html',{'inputText': 'Congratulation'})
        else:
            return render(request,'home_application/helloBlueking.html', {'error': True})
    else:
        return render(request, 'home_application/helloBlueking.html')

@login_exempt
def diskListenerHtml(request):
    """磁盘使用率html"""
    return render(request, 'home_application/diskListener.html')

@login_exempt
def diskListenerData(request):
    """磁盘使用率数据"""
    disks = models.DiskUsage.objects.values("disk_rate","add_time").order_by("id")
    diskLists = list(disks)
    add_times = []
    disk_rates = []
    for diskList in diskLists:
        add_times.append(str(diskList["add_time"].strftime("%Y-%m-%d %H:%M")))
        disk_rates.append(diskList["disk_rate"])
    data = {
        "code": 0,
        "result": True,
        "messge": "success",
        "data": {
            "title": "标题",
            "series": [
                {
                    "color": "#f9ce1d",
                    "name": "X轴：日期，Y轴：百分比",
                    "data": disk_rates
                }
            ],
            "categories": add_times
        }
    }

    return JsonResponse(data, safe=False)

@login_exempt
def api_disk_usage(request):
    """查询磁盘使用率API接口"""
    ip = request.GET.get('ip', '')
    system = request.GET.get('system', '')
    disk = request.GET.get('disk', '')
    if ip and system and disk:
        computers = models.DiskUsage.objects.filter(ip=ip, system=system, disk=disk).order_by("id")
    else:
        return JsonResponse({
            "code": -1,
            "result": False,
            "data": [],
            "message": '参数不完整'
        })
    diskList = list(computers)

    return JsonResponse({
        "code": 0,
        "result": True,
        "data": diskList,
        "message": 'success'
    })

@login_exempt
def get_usage_data(request):
    """调用自主接入接口api"""
    if request.method == 'POST':
        client = get_client_by_request(request)
        ip = request.POST.get('ip', '')
        system = request.POST.get('system', '')
        disk = request.POST.get('disk', '')
        kwargs = {
            "ip": ip,
            "system": system,
            "disk": disk
        }
        usage = client.self_api.get_disk_usage(kwargs)
        add_times = []
        disk_rates = []
        lists = usage["data"]
        if usage["result"]:
            for diskList in lists:
                add_times.append(str(diskList["add_time"].strftime("%Y-%m-%d %H:%M")))
                disk_rates.append(diskList["disk_rate"])
            data = {
                "code": 0,
                "result": True,
                "messge": "success",
                "data": {
                    "title": "标题",
                    "series": [
                        {
                            "color": "#f9ce1d",
                            "name": "X轴：日期，Y轴：百分比",
                            "data": disk_rates
                        }
                    ],
                    "categories": add_times
                }
            }
            return JsonResponse(data)
        else:
            return JsonResponse(usage)
    else:
        return render(request, 'home_application/getDiskUsage.html')




