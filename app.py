# coding: utf-8

from datetime import datetime

from flask import Flask, jsonify, request
from flask import render_template
from flask_sockets import Sockets

from views.todos import todos_view
from views.api import api_view

app = Flask(__name__)
sockets = Sockets(app)

# 动态路由
app.register_blueprint(todos_view, url_prefix='/todos')
app.register_blueprint(api_view, url_prefix='/api')


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/time')
def time():
    return str(datetime.now())


@sockets.route('/echo')
def echo_socket(ws):
    while True:
        message = ws.receive()
        ws.send(message)


@app.route('/api')
def api():
    github_code = request.args.get('code')
    return jsonify({'code': github_code})
