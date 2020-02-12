from datetime import datetime
from app import db, login
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, index=True, nullable=False)
    email = db.Column(db.String(120), index=True, unique=True, nullable=False)
    password_hash = db.Column(db.String(128))

    def __repr__(self):
        return "<User {}>".format(self.username)
    
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

@login.user_loader
def load_user(id):
    return User.query.get(int(id))

class Keyboard(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    phrase1 = db.Column(db.String(255), nullable=False)
    phrase2 = db.Column(db.String(255), nullable=False)
    phrase2 = db.Column(db.String(255), nullable=False)

    def __repr__(self):
        return "<Keyboard:\n{}\n{}\n{}\n>".format(phrase1, phrase2, phrase3)

class UserKeyboard(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    keyboard_id = db.Column(db.Integer, db.ForeignKey("keyboard.id"), nullable=False)
