from flask_wtf import FlaskForm
from wtforms import SubmitField,StringField,PasswordField,BooleanField
from wtforms.validators import DataRequired,EqualTo,Length,Regexp # regular expression
from wtforms.validators import ValidationError

from ..models import User

class LoginForm(FlaskForm):
    email = StringField('Email: ',validators=[DataRequired()])
    password = PasswordField('Password: ',validators=[DataRequired(),Length(6,20)])
    remember = BooleanField('Remember me')
    submit = SubmitField('Log IN')


class RegisterForm(FlaskForm):
    email = StringField('Email: ',validators=[DataRequired()])
    username = StringField('username: ',
                           validators=[DataRequired(),
                                       Length(1,10),Regexp('^[A-Za-z][A-Za-z0-9_.]*$')]
                           )
    password = PasswordField('Password: ',validators=[DataRequired(),Length(6,20)])
    password2 = PasswordField('Confirm your password: ',
                              validators=[DataRequired(),
                                          EqualTo('password',message='Passwords must match.')])
    submit = SubmitField('Register')

    def validate_email(self,field):
        if User.query.filter_by(email=field.data).first():
            raise ValidationError('email already existed')

    def validate_username(self,field):
        if User.query.filter_by(username=field.data).first():
            raise ValidationError('username already in use')

class ChangePasswordForm(FlaskForm):
    old_password = PasswordField('Old password: ',validators=[DataRequired()])
    new_password = PasswordField('New password: ',validators=[DataRequired(),Length(6,20)])
    new_password2 = PasswordField('Confirm password: ',
                                  validators=[DataRequired(),EqualTo('new_password',
                                                                     message='passwords must match')])
    submit = SubmitField('Change password')

class PasswordResetRequestForm(FlaskForm):
    email = StringField('email: ',validators=[DataRequired()])
    submit = SubmitField('reset password')

    def validate_email(self,field):
        if User.query.filter_by(email=field.data).first() is None:
            raise ValidationError('unknown email')

class PasswordResetForm(FlaskForm):
    email = StringField('email: ',validators=[DataRequired()])
    new_password = PasswordField('New password: ',validators=[DataRequired(),Length(6,20)])
    new_password2 = PasswordField('Confirm password: ',
                                  validators=[DataRequired(),EqualTo('new_password',
                                                                     message='passwords must match')])
    submit = SubmitField('reset password')

    def validate_email(self,field):
        if User.query.filter_by(email=field.data).first() is None:
            raise ValidationError('unknown email')