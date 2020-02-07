from flask import render_template, request, jsonify
from app import app
import mysql.connector

@app.route("/")
def index():
    data = db.magic #GET THE KEYBOARD DATA WITH 3 PHRASES BASED ON THE CURRENT USER
    keyboards = {}
    return render_template("index.html", keyboards=keyboards)

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
