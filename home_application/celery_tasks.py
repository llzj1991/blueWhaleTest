# -*- coding:utf-8 -*-

from celery import task
from celery.task import periodic_task
from blueking.component.shortcuts import get_client_by_user
from home_application import models
import base64
import logging
import datetime,time,json,re

from blueking.component.shortcuts import get_client_by_request
# # 默认从django settings中获取APP认证信息：应用ID和安全密钥
# # 默认从django request中获取用户登录态bk_token

logger = logging.getLogger('celery')


def base64_encode(string):
    """对字符串进行base64编码"""
    return base64.b64encode(string).decode("utf-8")

client = get_client_by_user('277301587')  # 这里是周期任务，不能通过request请求client
script_content = base64_encode(b"df -h /usr/")
ip = '10.0.1.80'

def fast_execute_script(client, script_content, ip):
    """快速执行脚本函数"""
    kwargs = {
        "bk_app_code": "bluewhaletest",
        "bk_app_secret": "295ee595-b518-4736-a0a3-58c9d6eba539",
        "bk_biz_id": 4,
        "script_content": script_content,
        "script_timeout": 1000,
        "account": "root",
        "is_param_sensitive": 0,
        "script_type": 1,
        "ip_list": [
            {
                "bk_cloud_id": 0,
                "ip": ip  # 10.0.1.80
            }
        ],
        "custom_query_id": [
            "3"
        ]
    }
    return client.job.fast_execute_script(kwargs)

@task()
def get_capacity_task():
    """定义一个获取磁盘使用率异步任务"""
    fast_execute_script_result = fast_execute_script(client, script_content, ip)
    if fast_execute_script_result['message'] == 'success':
        job_instance_id = fast_execute_script_result['data']['job_instance_id']
        get_job_instance_log_result = get_job_instance_log(client, job_instance_id)

        # 如果日志查询成功，提取内容
        if get_job_instance_log_result['message'] == 'success':
            # 匹配log_content规则
            dataJson = get_job_instance_log_result["data"][0]["step_results"][0]["ip_logs"][0]["log_content"]
            dataStr = re.findall("Filesystem      Size  Used Avail Use% Mounted on\n(.*?)\n", dataJson, re.S)[0]
            diskStr = ' '.join(dataStr.split()).split(" ")
            file_system = diskStr[0]
            disk_capacity = diskStr[1]
            disk_used = diskStr[2]
            disk_able = diskStr[3]
            disk_rate = diskStr[4].replace("%", "")
            disk_mount = diskStr[5]
            obj = models.DiskUsage.objects.create(file_system=file_system, disk_capacity=disk_capacity,
                                                  disk_used=disk_used, disk_able=disk_able, disk_rate=disk_rate,
                                                  disk_mount=disk_mount)
            obj.save()


@periodic_task(run_every=datetime.timedelta(seconds=3600))
def get_disk_periodic():
    """获取磁盘使用率周期执行定义"""
    get_capacity_task.delay()

def get_job_instance_log(client, job_instance_id):
    """
    对作业执行具体日志查询函数
    """
    kwargs = {
        "bk_app_code": "bluewhaletest",
        "bk_app_secret": "295ee595-b518-4736-a0a3-58c9d6eba539",
        "bk_username": "277301587",
        "bk_biz_id": 4,
        "job_instance_id": job_instance_id
    }
    time.sleep(2)  # todo 延时2s, 快速执行脚本需要一定的时间， 后期可以用celery串行两个函数
    return client.job.get_job_instance_log(kwargs)
