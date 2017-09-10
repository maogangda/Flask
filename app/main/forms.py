from flask_wtf import FlaskForm
from wtforms import StringField,SubmitField,TextAreaField
from wtforms.validators import DataRequired,Length

class NameForm(FlaskForm):
    name = StringField('Input your name: ',validators=[DataRequired(),Length(1,10)])
    submit = SubmitField('Submit')

class EditProfileForm(FlaskForm):
    name = StringField('Input your real name: ',validators=[Length(0,64)])
    location = StringField('Input your location: ',validators=[Length(0,64)])
    about_me = TextAreaField('About me')
    submit = SubmitField('Submit')