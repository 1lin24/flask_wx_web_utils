import os

class Config(object):
    APP_ID = os.environ.get('')
    APP_SECRET = os.environ.get('')
    SECRET_KEY = '1lin24'

class DevConfig(Config):
    BASE_URL = 'your_ip_address_for_dev'
    # 数据库信息从环境变量取
    #SQLALCHEMY_DATABASE_URI = os.environ.get('key')
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://demo:demo_pwd@localhost:3306/demo'
    SCHEDULER_API_ENABLED = True
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    SQLALCHEMY_POOL_SIZE = 50
    SQLALCHEMY_POOL_TIMEOUT = 10
    SQLALCHEMY_POOL_RECYCLE = 50
    SQLALCHEMY_MAX_OVERFLOW = 50
    DEBUG = True

class ProConfig(Config):
    BASE_URL = 'your_ip_address_for_pro'
    # 数据库信息从环境变量取
    #SQLALCHEMY_DATABASE_URI = os.environ.get('key')
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://demo:demo_pwd@localhost:3306/demo'
    SCHEDULER_API_ENABLED = True
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    SQLALCHEMY_POOL_SIZE = 50
    SQLALCHEMY_POOL_TIMEOUT = 10
    SQLALCHEMY_POOL_RECYCLE = 50
    SQLALCHEMY_MAX_OVERFLOW = 50
    DEBUG = False

config = {
            'dev' : DevConfig,
            'pro' : ProConfig,
            'default' : DevConfig
         }

