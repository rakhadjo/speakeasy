from flask import render_template, request, jsonify, url_for, redirect
from app import app, db, DEFAULT_KEYBOARDS
from flask_login import (
        current_user,
        login_user,
        logout_user,
        login_required,
        )
from werkzeug.urls import url_parse
from app.models import User, UserKeyboard, Keyboard
from app.forms import (
        LoginForm,
        RegistrationForm,
        ProfileForm,
        )
from app.db_functions import (
        get_user_keyboards,
        update_keyboards_db,
        update_accent_db,
        update_password_db,
        update_email_db,
        add_user,
        )

@app.route("/")
def index():
    if current_user.is_authenticated:
        keyboards = get_user_keyboards()
        audio_speed = User.query.filter_by(id=current_user.id).first().speed
    else:
        keyboards = DEFAULT_KEYBOARDS
        audio_speed = 1
    return render_template("index.html", keyboards=keyboards, audio_speed=audio_speed)

@app.route("/about_us")
def about_us():
    return render_template("about_us.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for("index"))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        login_user(user)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('index')
        return redirect(next_page)
    return render_template("login.html", title="Sign in", form=form)

@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for("index"))

@app.route("/register", methods=["GET", "POST"])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        add_user(form.username.data, form.email.data, form.password.data)
        user_id = User.query.filter_by(username=form.username.data).first().id
        update_keyboards_db(DEFAULT_KEYBOARDS, user_id)
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)

@app.route("/profile", methods=["GET", "POST"])
@login_required
def profile():
    user = User.query.filter_by(id=current_user.id).first()
    data = {
        "accent_dropdown": user.accent,
        "gender_dropdown": user.gender,
        "speed": int((user.speed - 1)*100 + 50)
    }
    form = ProfileForm(accent_form=data)
    if form.accent_submit.data:
        if form.accent_form.validate(form):
            accent = form.accent_form.accent_dropdown.data
            gender = form.accent_form.gender_dropdown.data
            speed = form.accent_form.speed.data
            update_accent_db(accent, gender, speed)
    if form.password_submit.data:
        if form.password_form.validate(form):
            password = form.password_form.password.data
            new_password = form.password_form.new_password.data
            update_password_db(password, new_password)
            logout_user()
            return redirect(url_for("login"))
    if form.email_submit.data:
        if form.email_form.validate(form):
            email = form.email_form.email.data
            update_email_db(email)
    keyboards = get_user_keyboards()
    return render_template("profile.html", form=form, keyboards=keyboards)
