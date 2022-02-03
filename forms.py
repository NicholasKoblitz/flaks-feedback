from ast import Str
from tkinter import E
from tkinter.tix import InputOnly
from tokenize import String
from wsgiref.types import InputStream
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField
from wtforms.validators import InputRequired, Email, Length


class CreateUserForm(FlaskForm):

    username = StringField('Username', validators=[InputRequired(), Length(min=1, max=20)])
    password = PasswordField("Password", validators=[InputRequired()])
    email = StringField("Email", validators=[InputRequired(), Length(min=1, max=50), Email()])
    first_name = StringField("First Name", validators=[InputRequired(), Length(min=1, max=30)])
    last_name = StringField("Last Name", validators=[InputRequired(), Length(min=1, max=30)])