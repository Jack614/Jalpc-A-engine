# coding: utf-8

import os
import re
import requests
import json
import random
import string
from leancloud import Object
from leancloud import Query
from leancloud import User
from leancloud import LeanCloudError
from flask import Blueprint
from flask import request
from flask import jsonify
from flask import redirect
from flask import url_for
from flask import render_template


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
        payload = {
            'access_token': access_token[0]
        }
        r = requests.get("https://api.github.com/user", params=payload)
        user_info = json.loads(r.text)
        user = User()
        user.set_username('gh_' + user_info['login'])
        user.set_email(user_info['email'])
        user.set_password(string.join(random.sample(
                ['z', 'y', 'x', 'w', 'v', 'u', 't', 's', 'r', 'q', 'p', 'o', 'n', 'm', 'l', 'k', 'j', 'i', 'h', 'g',
                 'f', 'e', 'd', 'c', 'b', 'a'], 8)).replace(' ', ''))
        try:
            user.sign_up()
        except LeanCloudError as e:
            return '{0}({1})'.format(callback, json.dumps({'Error': e.error, 'status': '502'}))
        else:
            the_user = _User.create_without_data(user.id)
            the_user.set('emailVerified', True)
            the_user.save()
            return '{0}({1})'.format(callback, json.dumps(
                    {'sessionToken': user._session_token, 'username': user.attributes['username'], 'status': '200'}))
    else:
        return '{0}({1})'.format(callback, json.dumps({'ERROR': 'Login error, please login again.', 'status': '500'}))
