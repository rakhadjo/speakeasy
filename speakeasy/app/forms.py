from flask_wtf import FlaskForm
from wtforms import (
        StringField,
        PasswordField,
        BooleanField,
        SubmitField,
        SelectField,
        FormField,
        )
from wtforms.fields.html5 import IntegerRangeField
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo, Length
from app.models import User
from app import speech_client
from flask_login import current_user

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Sign In')

    def validate_username(self,field):
        user = User.query.filter_by(username=self.username.data).first()
        if user is None:
            raise ValidationError('User does not exist')

    def validate_password(self,field):
        user = User.query.filter_by(username=self.username.data).first()
        if user is not None and not user.check_password(self.password.data):
            raise ValidationError('Password incorrect')

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
            raise ValidationError('This username is already taken.')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is not None:
            raise ValidationError('This email is already taken')

class AccentProfileForm(FlaskForm):
    countries = ("AU", "US", "IN", "GB")
    accents = (f"en-{country}-Wavenet-A" for country in countries)
    accents = [(accent, country) for accent, country in zip(accents, countries)]
    accent_dropdown = SelectField('Speaking Accent',
            choices = accents,
            validators = [DataRequired()])
    genders = [(g,g) for g in ("MALE", "FEMALE", "NEUTRAL")]
    gender_dropdown = SelectField("Voice Gender",
            choices = genders,
            validators = [DataRequired()])
    speed = IntegerRangeField("Speaking Speed", default=50)

class PasswordProfileForm(FlaskForm):
    password = PasswordField("Current Password", validators=[DataRequired()])
    new_password = PasswordField("Change Password", validators=[DataRequired(), Length(6,20)])
    new_password2 = PasswordField(
            "Repeat password", validators=[DataRequired(), EqualTo("new_password")])

    def validate_password(self, password):
        user = User.query.filter_by(id=current_user.id).first()
        if not user.check_password(password.data):
            raise ValidationError("The password is incorrect")


class EmailProfileForm(FlaskForm):
    email = StringField("Email", validators=[DataRequired(), Email()])

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is not None:
            raise ValidationError("This email is already taken.")

class ProfileForm(FlaskForm):
    accent_form = FormField(AccentProfileForm)
    password_form = FormField(PasswordProfileForm)
    email_form = FormField(EmailProfileForm)
    accent_submit = SubmitField("Save")
    password_submit = SubmitField("Change Password")
    email_submit = SubmitField("Change Email")
