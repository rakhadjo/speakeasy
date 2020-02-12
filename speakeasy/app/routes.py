from flask import render_template, request, jsonify
from app import app
import mysql.connector
from app.forms import LoginForm

@app.route("/")
def index():
    '''
    # data = db.magic #GET THE KEYBOARD DATA WITH 3 PHRASES BASED ON THE CURRENT USER
    sql_1 = "SELECT keyboard_id "
    keyboards = {}
    '''
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
        keyboards = {
            "phrases_0": ["Hello world", "How are you", "This is rakhadjo"]
        }
    return render_template("index.html", keyboards=keyboards)

@app.route("/about_us")
def about_us():
    return render_template("about_us.html")

@app.route("/login_page")
def login_page():
    return render_template("login_page.html")

#Temporary for testing
@app.route("/login")
def login():
    form = LoginForm()
    return render_template("login.html", title="Sign in", form=form)

@app.route("/profile")
def profile():
    return render_template("profile.html")

@app.route("/newspeak")
def newspeak():
    return render_template("speak.html")
