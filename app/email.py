
# coding:utf8

from . import mail

from flask_mail import Message
from flask import render_template,current_app

from threading import Thread

def asyncSendMail(app,msg):
    with app.app_context():
        mail.send(msg)


def sendMail(to,subject,template,**kwargs):
    app = current_app._get_current_object()
    msg = Message(
        subject=subject,
        sender='python7456@163.com',
        recipients=[to]
    )
    msg.body = render_template(template+'.txt',**kwargs) # 纯文本内容
    msg.html = render_template(template+'.html',**kwargs) # 富文本内容
    thr = Thread(target=asyncSendMail,args=(app,msg))
    thr.start()
    return thr