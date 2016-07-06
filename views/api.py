# coding: utf-8

import os
import re
import requests
import json
from leancloud import Object
# from leancloud import Query
# from leancloud import User
# from leancloud import LeanCloudError
from flask import Blueprint
from flask import request
# from flask import redirect
# from flask import url_for


class _User(Object):
    pass


api_view = Blueprint('api', __name__)


@api_view.route('/github')
def github():
    github_code = request.args.get('code')
    callback = request.args.get('callback')
    payload = {
        'client_id': '66d71e5c5d53bb41fa0a',
        'client_secret': os.environ['G_CLIENT_SECRET'],
        'redirect_uri': os.environ['REDIRECT_URI'],
        'state': 'Jalpclogin',
        'code': github_code
    }
    r = requests.post("https://github.com/login/oauth/access_token", params=payload)
    access_token = re.findall('access_token=(\w+)&scope=.*', r.text, re.S)
    if access_token:
        print access_token[0]
        payload = {
            'access_token': access_token[0]
        }
        r = requests.get("https://api.github.com/user", params=payload)
        user_info = json.loads(r.text)
        user_info['status'] = 200
        return '{0}({1})'.format(callback, json.dumps(user_info))
    else:
        return '{0}({1})'.format(callback, json.dumps({'ERROR': 'Login error, please login again.', 'status': '500'}))


@api_view.route('/surl')
def surl():
    url = request.args.get('url')
    callback = request.args.get('callback')
    payload = {
        'url': url
    }
    r = requests.post("http://vurl.cn/create.php", data=payload)
    return '{0}({1})'.format(callback, json.dumps({'surl': json.loads(r.text)['tinyurl'], 'status': '200'}))
