from flask import render_template
from app import app

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/about_us")
def about_us():
    return render_template("about_us.html")

@app.route("/login_page")
def login_page():
    return render_template("login_page.html")

@app.route("/profile")
def profile():
    return render_template("profile.html")

@app.route("/newspeak")
def newspeak():
    return render_template("speak.html")
