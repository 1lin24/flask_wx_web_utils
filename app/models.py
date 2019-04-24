from . import db
from .utils.id_generator import generate_id
from datetime import datetime
from flask_login import UserMixin
from . import login_manager

class User(UserMixin, db.Model):
    __tablename__ = 'users'

    id = db.Column(db.String(32), primary_key=True)
    order_idx = db.Column(db.Integer, default=50000)
    create_time = db.Column(db.DateTime, default=datetime.now)
    openid = db.Column(db.Text)
    nickname = db.Column(db.Text)
    sex = db.Column(db.SmallInteger)
    province = db.Column(db.Text)
    city = db.Column(db.Text)
    country = db.Column(db.Text)
    headimgurl = db.Column(db.Text)

    def __init__(self):
        self.id = generate_id('user')

    @login_manager.user_loader
    def load_user(id):
        return User.query.filter_by(id=id).first()

class AccessToken(db.Model):
    __tablename__ = 'access_token'

    id = db.Column(db.String(32), primary_key=True)
    token = db.Column(db.Text)
    expire_time = db.Column(db.DateTime)

    def is_valid(self):
        now = datetime.now()
        expire_time = self.expire_time
        print('now = {}, expire_time = {}'.format(now, expire_time))

        return self.expire_time > datetime.now()

class JSAPITicket(db.Model):
    __tablename__ = 'jsapi_ticket'

    id = db.Column(db.String(32), primary_key=True)
    ticket = db.Column(db.Text)
    expire_time = db.Column(db.DateTime)

    def is_valid(self):
        return self.expire_time > datetime.now()
