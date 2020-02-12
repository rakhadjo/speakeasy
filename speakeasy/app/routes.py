from flask import render_template, request, jsonify, url_for, redirect
from app import app, db
from flask_login import current_user, login_user, logout_user, login_required
from werkzeug.urls import url_parse
from app.models import User
from app.forms import LoginForm, RegistrationForm

@app.route("/")
def index():
    '''
    # data = db.magic #GET THE KEYBOARD DATA WITH 3 PHRASES BASED ON THE CURRENT USER
    sql_1 = "SELECT keyboard_id "
    keyboards = {}
    '''
    """
    username = "rakhadjo" #username=None
    if username: #session["username"]
        sql_1 = "SELECT user_id FROM users WHERE username = '" + username + "';"
        cursor.execute(sql_1)
        result = cursor.fetchall()[0]
        user_id = str(result[0])
        sql_2 = "SELECT keyboard_id FROM user_keyboards WHERE user_id = " + user_id + " ;"
        cursor.execute(sql_2)
        result = cursor.fetchall()
        keyboards = {}
        idx = -1
        for x in result:
            sql_4 = "SELECT phrase1, phrase2, phrase3 FROM keyboards WHERE keyboard_id = " + str(x[0]) + ";"
            cursor.execute(sql_4)
            result2 = cursor.fetchall()[0]
            phrase_list = [result2[0], result2[1], result2[2]]
            idx = idx + 1
            keyboards.update( {"phrases_" + str(idx) : phrase_list} )
    else:
    """
    keyboards = {
        "phrases_0": ["Hello world", "How are you", "This is rakhadjo"]
    }
    return render_template("index.html", keyboards=keyboards)

@app.route("/about_us")
def about_us():
    return render_template("about_us.html")

@app.route("/login_page")
def login_page():
    #This is to be removed
    return render_template("login_page.html")

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
        db.session.commit()
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)

@app.route("/profile")
@login_required
def profile():
    return render_template("profile.html")

@app.route("/newspeak")
def newspeak():
    return render_template("speak.html")
