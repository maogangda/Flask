# coding:utf8

from . import db

from werkzeug.security import generate_password_hash,check_password_hash

from itsdangerous import TimedJSONWebSignatureSerializer as Serializer

from flask import current_app

from datetime import datetime

from flask_login import UserMixin,AnonymousUserMixin
from . import login_manager

class Permission:
    FOLLOW = 0x01
    COMMENT = 0x02
    WRITE = 0x04
    MODERATE_COMMENT = 0x08
    ADMINISTER = 0x80

class Role(db.Model):
    __tablename__ = 'roles'
    id = db.Column(db.Integer,primary_key = True)
    name = db.Column(db.String(64),unique=True)
    users = db.relationship('User',backref='role')

    default = db.Column(db.Boolean,default=False,index=True)
    permissions = db.Column(db.Integer)

    @staticmethod
    def insert_roles():
        roles = {
            'User':(Permission.FOLLOW|
                    Permission.COMMENT|
                    Permission.WRITE,True),
            'Moderator':(Permission.FOLLOW|
                         Permission.COMMENT|
                         Permission.WRITE|
                         Permission.MODERATE_COMMENT,False),
            'Administrator':(0xff,False)

        }
        for r in roles:
            role = Role.query.filter_by(name=r).first()
            if role is None:
                role = Role(name=r)
            role.permissions = roles[r][0]
            role.default = roles[r][1]
            db.session.add(role)
        db.session.commit()

    def __repr__(self):
        return '<Role %r>' % self.name

class User(UserMixin,db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer,primary_key=True)
    username = db.Column(db.String(64),unique=True,index=True)
    email = db.Column(db.String(64),unique=True)
    # password = db.Column(db.String(64))
    role_id = db.Column(db.Integer,db.ForeignKey('roles.id'))
    # role

    password_hash = db.Column(db.String(128))

    confirmed = db.Column(db.Boolean,default=False)

    name = db.Column(db.String(64))
    location = db.Column(db.String(64))
    about_me = db.Column(db.Text())
    member_since = db.Column(db.DateTime(),default=datetime.utcnow)
    last_seen = db.Column(db.DateTime(),default=datetime.utcnow)

    def __init__(self,**kwargs):
        super(User,self).__init__(**kwargs)
        if self.email == 'python7456@163.com':
            self.role=Role.query.filter_by(permissions=0xff).first()
        else:
            self.role = Role.query.filter_by(default=True).first()


    @property
    def password(self):
        raise AttributeError('Password is not a readable attribute')

    @password.setter
    def password(self,password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self,password):
        return check_password_hash(self.password_hash,password)

    def generate_confirmation_token(self,expiration=3600):
        s = Serializer(current_app.config['SECRET_KEY'],expires_in=expiration)
        return s.dumps({'confirm':self.id})

    def confirm(self,token):
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            data = s.loads(token)
        except:
            return False
        if data.get('confirm') != self.id:
            return False
        self.confirmed=True
        db.session.add(self)
        return True

    def generate_reset_token(self,expiration=3600):
        s = Serializer(current_app.config['SECRET_KEY'],expires_in=expiration)
        return s.dumps({'reset':self.id})

    def reset_password(self,token,new_password):
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            data = s.loads(token)
        except:
            return False
        if data.get('reset') != self.id:
            return False
        self.password = new_password
        db.session.add(self)
        return True

    def can(self,permissions):
        return (self.role.permissions & permissions) == permissions

    def is_administrator(self):
        return self.can(Permission.ADMINISTER)

    def ping(self):
        self.last_seen = datetime.utcnow()
        db.session.add(self)

    def __repr__(self):
        return '<User %r>' % self.username

class AnonymousUser(AnonymousUserMixin):
    def can(self,permissions):
        return False

    def is_administrator(self):
        return False

login_manager.anonymous_user = AnonymousUser

# 回调函数
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))