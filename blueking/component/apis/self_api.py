# -*- coding: utf-8 -*-
from ..base import ComponentAPI

class CollectionsGetDiskUsage(object):
    """Collections of get_dfusage_bay1 APIS"""

    def __init__(self, client):
        self.client = client

        self.get_disk_usage = ComponentAPI(
            client=self.client, method='GET',
            path='api/c/self-service-api/bluewhaletest/api/get_disk_usage/',
            description=u'查询指定的磁盘使用率'
        )