from flask import render_template, request, jsonify, url_for, redirect
from app import app, db, DEFAULT_KEYBOARDS
from flask_login import current_user, login_user, logout_user, login_required
from werkzeug.urls import url_parse
from app.models import User, UserKeyboard, Keyboard
from app.forms import LoginForm, RegistrationForm

@app.route("/")
def index():
    if current_user.is_authenticated:
        user_keyboards = UserKeyboard.query.filter_by(user_id=current_user.id)
        keyboard_ids = (uk.keyboard_id for uk in user_keyboards)
        keyboard_list = (Keyboard.query.filter_by(id=id).first() for id in keyboard_ids)
        keyboards = {k.icon:[k.phrase1, k.phrase2, k.phrase3] for k in keyboard_list}
    else:
        keyboards = DEFAULT_KEYBOARDS
    print(keyboards)
    return render_template("index.html", keyboards=keyboards)

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
        if user is None or not user.check_password(form.password.data):
            return redirect(url_for('login'))
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
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        phrase_attrs = ("phrase1", "phrase2", "phrase3")
        for icon, phrases in DEFAULT_KEYBOARDS.items():
            db.session.add(
                    Keyboard(icon=icon, **{attr:val for attr, val in zip(phrase_attrs, phrases)}))
        db.session.commit()
        first_keyboard_id = Keyboard.query.order_by(Keyboard.id).all()[-1].id - 2
        keyboard_ids = (first_keyboard_id + i for i in range(3))
        user_id = User.query.filter_by(username=form.username.data).first().id
        for keyboard_id in keyboard_ids:
            db.session.add(UserKeyboard(user_id=user_id, keyboard_id=keyboard_id))
        db.session.commit()
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)

@app.route("/profile")
@login_required
def profile():
    return render_template("profile.html")
