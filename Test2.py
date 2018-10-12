import requests
import json
import  os
import base64
import pickle

def getAccessToken():
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded',
    }
    data={'name':'gaochao','pass':'123456'}

    r=requests.post('http://127.0.0.1:8000/myserver/_index', headers=headers,data=data)


    return r.content


class A:
    print("dfef")

