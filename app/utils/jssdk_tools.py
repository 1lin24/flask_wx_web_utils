from datetime import datetime, timedelta
import hashlib
import random
import string
import os

from flask_login import login_user
from flask import current_app
import requests as http

from ..models import db, JSAPITicket, AccessToken, User
from .id_generator import generate_id

class JSSDKSign:
    def __init__(self, jsapi_ticket, url):
        self.material = dict(
                nonceStr = self.__create_nonce_str(),
                jsapi_ticket = jsapi_ticket,
                timestamp = self.__create_timestamp(),
                url = url)

    def __create_nonce_str(self):
        return ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(15))

    def __create_timestamp(self):
        return int(datetime.now().timestamp())

    def sign(self):
        string = '&'.join(['%s=%s' % (key.lower(), self.material[key]) for key in sorted(self.material)])
        self.material['signature'] = hashlib.sha1(string.encode('utf-8')).hexdigest()
        return self.materia

def _get_access_token():
    """获取 access_token, 用于jsapi
    """
    access_token = AccessToken.query.first()
    if access_token and access_token.is_valid():
        return access_token.token
    else:
        app_id = current_app.config.get('APP_ID')
        app_secret = current_app.config.get('APP_SECRET')
        #print('secret = ', app_secret)
        url = 'https://api.weixin.qq.com/cgi-bin/token?grant_type=client_credential&appid={}&secret={}'.format(app_id, app_secret)
        res = http.get(url, timeout=(3.05, 3))
        res_data = res.json()
        print('access_token {}'.format(res_data))
        token, expire_in = res_data.get('access_token'), res_data.get('expires_in')
        if not access_token:
            access_token = AccessToken(id=generate_id('a'))
        access_token.token = token
        access_token.expire_time = datetime.now() - timedelta(seconds=(expire_in+60))
        db.session.add(access_token)
        db.session.commit()
        return access_token.token

def _get_api_ticket(access_token):
    ticket_obj = JSAPITicket.query.first()
    if ticket_obj and ticket_obj.is_valid():
        return ticket_obj.ticket
    else:
        url = 'https://api.weixin.qq.com/cgi-bin/ticket/getticket?access_token={}&type=jsapi'.format(access_token)
        res = http.get(url, timeout=(3.05, 3))
        res.encoding = 'utf-8'
        res_data = res.json()
        #print('jsapi_ticket = {}'.format(res_data))
        if not ticket_obj:
            ticket_obj = JSAPITicket(id=generate_id('t'))
        ticket_obj.ticket = res.json().get('ticket')
        ticket_obj.expire_time = datetime.now() + timedelta(seconds=(int(res.json().get('expires_in')+60)))
        db.session.add(ticket_obj)
        db.session.commit()
        return ticket_obj.ticket
        
def get_access_token4login(code):
    """通过code获取 access_token, 用于获取用户信息

    用户访问形如下方的链接，跳转到 REDIRECT_URI
    https://open.weixin.qq.com/connect/oauth2/authorize?appid=APPID&redirect_uri=REDIRECT_URI&response_type=code&scope=SCOPE&state=STATE#wechat_redirect
    (注：授权回调的方式只适用于认证服务号)

    在 REDIRECT_URI 对应的view 当中，可以使用以下方式获得 code 和 state ( state 可以用于传参)
    code = request.args.get('code')
    state = request.args.get('state')
    由此获得 code， 再通过下面的方式换取 微信用户的 openid 和access_token
    最后使用 openid 和access_token 换取用户信息
    """
    app_id = current_app.config.get('APP_ID')
    app_secret = current_app.config.get('APP_SECRET')
    #print('secret = ', app_secret)
    url = 'https://api.weixin.qq.com/sns/oauth2/access_token?appid={}&secret={}&code={}&grant_type=authorization_code'.format(app_id, app_secret, code)
    res = http.get(url, timeout=(3.05, 3))
    res_data = res.json()
    openid, access_token = res_data.get('openid'), res_data.get('access_token')
    return openid, access_token

def get_user_info(openid, access_token):
    url = 'https://api.weixin.qq.com/sns/userinfo?access_token={}&openid={}&lang=zh_CN'.format(access_token, openid)
    res = http.get(url, timeout=(3.05, 3))
    res.encoding = 'utf-8'
    user_info = res.json()
    return user_info

def wx_jssdk_config(url):
    app_id = current_app.config.get('APP_ID')
    access_token = _get_access_token()
    ticket = _get_api_ticket(access_token)
    sign = JSSDKSign(ticket, url)
    sign.sign()
    conf = dict(
            appId=app_id,
            timestamp=sign.material['timestamp'],
            nonceStr=sign.material['nonceStr'],
            signature=sign.material['signature'])
    return conf

def login(user_info):
    openid = user_info.get('openid')
    user = User.query.filter(User.openid==openid).first()

    nickname = user_info.get('nickname')
    sex = user_info.get('sex')
    province = user_info.get('province')
    city = user_info.get('city')
    country = user_info.get('country')
    headimgurl = user_info.get('headimgurl')

    if not user:
        user = User()
        user.openid = openid
    user.nickname = nickname
    user.sex = sex
    user.province = province
    user.city = city
    user.country = country
    user.headimgurl = headimgurl
    db.session.add(user)
    db.session.commit()
    login_user(user)
