# coding:utf8

import os
basedir = os.path.abspath(os.path.dirname(__file__)) # basedir=/home/nanfengpo/Documents/flasky

# 定义基类:里面包含所有环境共用的配置选项
class Config:
    SQLALCHEMY_COMMIT_ON_TEARDOWN = True
    SECRET_KEY = 'hard to guess string'

    MAIL_SERVER = 'smtp.163.com'
    MAIL_PORT = 25
    MAIL_USE_TLS = True
    MAIL_USERNAME = 'python7456' # python7456@163.com
    MAIL_PASSWORD = 'python'

    @staticmethod
    def init_app(app):
        pass


'''
    3个不同的环境
'''
class DevelopmentConfig(Config):
    DEBUG=True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///'+os.path.join(basedir,'data-dev.sqlite')

class TestingConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///'+os.path.join(basedir,'data-test.sqlite')

class ProductionConfig(Config):
    SQLALCHEMY_DATABASE_URI = 'sqlite:///'+os.path.join(basedir,'data.sqlite')

config = {
    'development':DevelopmentConfig,
    'testing':TestingConfig,
    'production':ProductionConfig,

    'default':DevelopmentConfig
}