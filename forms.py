from typing import Text
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, TextField


class UserRegisterForm(FlaskForm):
    """Form for registring a user"""
    username = StringField("Username:")
    password = PasswordField("Password:")
    email = StringField("Email:")
    first_name = StringField("First name:")
    last_name = StringField("Last name:")


class UserLoginForm(FlaskForm):
    """Form for User login"""
    username = StringField("Username:")
    password = PasswordField("Password:")


class AddFeedbackForm(FlaskForm):
    """Form for adding feedback"""
    title = StringField("Feedback Title:")
    content = TextField("Feedback Content:")


class EditFeedbackForm(FlaskForm):
    title = StringField("Feedback Title:")
    content = TextField("Feedback Content:")
