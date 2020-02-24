from flask_wtf import FlaskForm
from wtforms import (
        StringField,
        PasswordField,
        BooleanField,
        SubmitField,
        SelectField,
        FormField,
        )
from wtforms.fields.html5 import DecimalRangeField
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo, Length
from app.models import User
from app import speech_client

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Sign In')

class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(3,10)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired(), Length(6,20)])
    password2 = PasswordField(
            "Repeat password", validators=[DataRequired(), EqualTo("password")])
    submit = SubmitField("Register")

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user is not None:
            raise ValidationError('Please use a different username.')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is not None:
            raise ValidationError('Please use a different email address.')

class AccentProfileForm(FlaskForm):
    accents = (voice.name for voice in speech_client.list_voices().voices)
    accents = (name for name in accents if name[:2] == "en")
    accents = [(name, name) for name in accents]
    accent_dropdown = SelectField('Speaking Accent',
            choices = accents,
            validators = [DataRequired()])
    genders = [(g,g) for g in ("MALE", "FEMALE", "NEUTRAL")]
    gender_dropdown = SelectField("Voice Gender",
            choices = genders,
            validators = [DataRequired()])
    speed = DecimalRangeField("Speaking Speed", default = 50)

class PasswordProfileForm(FlaskForm):
    password = PasswordField("Current Password", validators=[DataRequired()])
    new_password = PasswordField("Change Password", validators=[DataRequired()])
    new_password2 = PasswordField(
            "Repeat password", validators=[DataRequired(), EqualTo("password")])

class EmailProfileForm(FlaskForm):
    email = StringField("Email", validators=[DataRequired(), Email()])

class ProfileForm(FlaskForm):
    accent_form = FormField(AccentProfileForm)
    password_form = FormField(PasswordProfileForm)
    email_form = FormField(EmailProfileForm)
    accent_submit = SubmitField("Save")
    password_submit = SubmitField("Change Password")
    email_submit = SubmitField("Change Email")
