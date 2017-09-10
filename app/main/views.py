# coding:utf8

from flask import render_template,session,redirect,url_for,flash
from flask_login import login_required,current_user

from .. import db
from ..models import User,Permission
from ..email import sendMail
from ..decorators import permission_required,admin_required
from . import main
from .forms import NameForm,EditProfileForm

@main.route('/',methods=['GET','POST'])
def index():
    form = NameForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.name.data).first()
        if user is None:
            user = User(username=form.name.data)
            db.session.add(user)
            session['known'] = False
            sendMail('nanfengpo','New user','mail/new_user',user=user)
        else:
            session['known'] = True
        session['name'] = form.name.data
        return redirect(url_for('main.index'))
    return render_template('index.html',form = form,
                           name=session.get('name'),
                           known=session.get('known'))

@main.route('/admin/')
@login_required
@admin_required
def for_admin_only():
    return '<h1>for administrator</h1>'

@main.route('/moderate/')
@login_required
@permission_required(Permission.MODERATE_COMMENT)
def for_moderator_only():
    return '<h1>for moderator</h1>'

@main.route('/user/<username>')
def user(username):
    user = User.query.filter_by(username=username).first_or_404()
    return render_template('user.html',user=user)

@main.route('/edit-profile/',methods=['GET','POST'])
@login_required
def edit_profile():
    form = EditProfileForm()
    if form.validate_on_submit():
        current_user.name = form.name.data
        current_user.location = form.location.data
        current_user.about_me = form.about_me.data
        db.session.add(current_user)
        flash('your profile has been updated')
        return redirect(url_for('main.user',username=current_user.username))
    form.name.data = current_user.name
    form.location.data = current_user.location
    form.about_me.data = current_user.about_me
    return render_template('edit_profile.html',form=form)
