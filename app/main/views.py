from flask import request, current_app, jsonify, render_template, redirect
from . import main
import requests as http
from ..models import * 
from ..response import Response
import random
import string

from datetime import datetime, timedelta
from flask_login import current_user
from ..utils.id_generator import generate_id
import os
from ..utils.jssdk_tools import get_access_token4login, get_user_info, wx_jssdk_config, login

@main.route('')
def home():
    """ 分享地址

    所有的分享都分享这个地址，传入参数
    通过该地址，跳转到微信授权，授权成功后才真正跳转到目标页面

    base_url?page=page_name&params=param0|param1|params2
    """
    try:
        base_url = current_app.config.get('BASE_URL')
        app_id = current_app.config.get('APP_ID')
        target = os.path.join(base_url, 'red')
        print('args = {}'.format(request.args))
        page = request.args.get('page')
        # 改进一下，希望可以获得多个参数
        params = request.args.get('params')
        state = '{}_{}'.format(page, params)
        print('state = {}'.format(state))
        wx_url = 'https://open.weixin.qq.com/connect/oauth2/authorize?appid={}&redirect_uri={}&response_type=code&scope=snsapi_userinfo&state={}#wechat_redirect'.format(app_id, target, state)
        print('跳转到微信')
        return redirect(wx_url)
    except Exception as e:
        print('[GET /] error --> {}'.format(e))
        return Response(0).json()

@main.route('red')
def redirect_from_wx():
    """ 来自微信生定向，用于获取 code

    由型如下方的链接生定向而来
    https://open.weixin.qq.com/connect/oauth2/authorize?appid=APPID&redirect_uri=REDIRECT_URI&response_type=code&scope=SCOPE&state=STATE#wechat_redirect

    1. 重定向之后，可以获得 code 和 state
    2. 使用 code 获取 access_token 和 openid
    3. 通过 access_token 和 openid 获取用户信息 user_info
    4. 根据 user_info 登录（新用户需要再登记）
    5. 根据 state 跳转到目标页面
    """

    try:
        code = request.args.get('code')
        state = request.args.get('state') # page_param
        # print('code = ', code, 'state = ', state)
        args = state.split('_')
        openid, access_token = get_access_token4login(code)
        user_info = get_user_info(openid, access_token)
        login(user_info)

        base_url = current_app.config.get('BASE_URL')

        page = args[0]
        params = args[1]
        return redirect('{}/{}?param={}'.format(base_url, page, params))
    except Exception as e:
        print(e)
        return Response(0).json()

@main.route('index')
def index():
    try:
        base_url = current_app.config.get('BASE_URL')
        url = os.path.join(base_url, 'index')
        conf = wx_jssdk_config(url)

        # 将形如 'a|b|c' 转换成 ['a', 'b', 'c']
        params = request.args.get('param').split('|')
        return render_template('index.html', user=current_user, params=params)
    except Exception as e:
        print('[GET: index] error --> {}'.format(e))
        return Response(0).json()

