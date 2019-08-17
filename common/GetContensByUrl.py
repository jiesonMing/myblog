#!/usr/bin/env python
# -*- coding:utf-8 -*-
from time import sleep
import requests
from django.http import HttpResponse

class GetContensByUrl:
    def getContents(self):
        
        data = {
            "reqType":0,
            "perception": {
                "inputText": {
                    "text": '你好'
                }
            },
            "userInfo": {
                "apiKey": "d1375188443743699e7d3b73f4040e2b",
                "userId": "441c7926f4c8da1d"
            }
        }
        res = requests.post("http://openapi.tuling123.com/openapi/api/v2",json=data)
        sleep(3)
        return HttpResponse(res)