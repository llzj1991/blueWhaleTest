# -*- coding: utf-8 -*-
from blueapps.account.models import User
from blueking.component.shortcuts import get_client_by_user
import base64

def base64_encode(string):
    """对字符串进行base64编码"""
    return base64.b64encode(string).decode("utf-8")


def fast_execute_script(client, script_content, ip):
    """快速执行脚本函数"""
    kwargs = {
        "bk_app_code": "bluewhaletest",
        "bk_app_secret": "295ee595-b518-4736-a0a3-58c9d6eba539",
        "bk_biz_id": 1,
        "script_content": script_content,
        "script_timeout": 1000,
        "account": "root",
        "is_param_sensitive": 0,
        "script_type": 1,
        "ip_list": [
            {
                "bk_cloud_id": 0,
                "ip": ip
            }
        ],
        "custom_query_id": [
            "3"
        ]
    }
    return client.job.fast_execute_script(kwargs)

def get_capacity_task():
    """
    定义一个获取磁盘使用率异步任务
    """
    user = User.objects.get(username='277301587')
    client = get_client_by_user(user.username)  # 这里是周期任务，不能通过request请求client
    script_content = base64_encode(b"df -h /usr/'")
    ip = '10.0.1.192'

    return fast_execute_script(client, script_content, ip)

print(get_capacity_task())