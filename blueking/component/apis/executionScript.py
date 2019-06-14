# -*- coding: utf-8 -*-
from ..base import ComponentAPI

class CollectionsGetExecutionScript(object):
    """Collections of get_dfusage_bay1 APIS"""

    def __init__(self, client):
        self.client = client

        self.get_execution_script = ComponentAPI(
            client=self.client, method='GET',
            path='/api/c/bluewhaletest/api/get_execution_script/',
            description=u'获取指定脚本的执行结果'
        )