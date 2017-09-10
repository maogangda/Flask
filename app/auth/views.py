# coding:utf8

from flask import render_template,redirect,url_for,request,flash

from flask_login import login_required,login_user,logout_user,current_user

from . import auth

from ..models import User
from ..email import sendMail

from .. import db

from forms import LoginForm,RegisterForm,ChangePasswordForm,PasswordResetForm,PasswordResetRequestForm

@auth.route('/secret/')
@login_required
def secret():
    return 'only login'

@auth.route('/login/',methods=['GET','POST']) # 127.0.0.1:5000/login/ ->127.0.0.1:5000/auth/login/
def login(): # auth.login
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user is not None and user.verify_password(form.password.data):
            login_user(user,form.remember.data)
            return redirect(request.args.get('next') or url_for('main.index'))
        flash('Invalid username or password')
    return render_template('auth/login.html',form=form)

@auth.route('/logout/')
@login_required
def logout():
    logout_user()
    return redirect(url_for('main.index'))

@auth.route('/register/',methods=['GET','POST']) # http://127.0.0.1:5000/register/
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        user = User(
            email=form.email.data,
            username=form.username.data,
            password=form.password.data
        )
        db.session.add(user)
        db.session.commit()
        token = user.generate_confirmation_token(3600)
        sendMail(user.email,'Confirm','auth/mail/confirm',user=user,token=token)
        flash('you can now login')
        return redirect(url_for('auth.login'))
    return render_template('auth/register.html',form=form)

@auth.route('/confirm/<token>')
@login_required
def confirm(token):
    if current_user.confirmed:
        return redirect(url_for('main.index'))
    if current_user.confirm(token):
        flash('you have confirmed your account')
    else:
        flash('invalid token')
    return redirect(url_for('main.index'))

@auth.route('/change-password/',methods=['GET','POST'])
@login_required
def change_password():
    form = ChangePasswordForm()
    if form.validate_on_submit():
        if current_user.verify_password(form.old_password.data):
            current_user.password = form.new_password.data
            db.session.add(current_user)
            flash('your password has been updated')
            return redirect(url_for('main.index'))
        else:
            flash('invalid password')
    return render_template('auth/change_password.html',form=form)

@auth.route('/reset/',methods=['GET','POST'])
def password_reset_request():
    if not current_user.is_anonymous:
        return redirect(url_for('main.index'))
    form = PasswordResetRequestForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user:
            token = user.generate_reset_token()
            sendMail(user.email,'Reset Password','auth/mail/reset_password',user=user,token=token)
            flash('An email has been sent to you')
            return redirect(url_for('auth.login'))
    return render_template('auth/reset_password.html',form=form)

@auth.route('/reset/<token>',methods=['GET','POST'])
def password_reset(token):
    if not current_user.is_anonymous:
        return redirect(url_for('main.index'))
    form = PasswordResetForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user.reset_password(token,form.new_password.data):
            flash('your password has been updated')
            return redirect(url_for('auth.login'))
        else:
            flash('invalid token')
            return redirect(url_for('main.index'))
    return render_template('auth/reset_password.html',form=form)


@auth.before_app_request
def before_request():
    if current_user.is_authenticated:
        current_user.ping()