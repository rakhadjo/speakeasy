from datetime import datetime
from app import db, login
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, index=True, nullable=False)
    email = db.Column(db.String(120), index=True, unique=True, nullable=False)
    password_hash = db.Column(db.String(128))
    accent = db.Column(db.String(20), default="en-US-Wavenet-A")
    gender = db.Column(db.String(20), default="MALE")
    speed = db.Column(db.Float, default=1.0)

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
    icon = db.Column(db.String(10), nullable=False)
    phrase1 = db.Column(db.String(255), nullable=False)
    phrase2 = db.Column(db.String(255), nullable=False)
    phrase3 = db.Column(db.String(255), nullable=False)
    position = db.Column(db.Integer, nullable=False)

    def __repr__(self):
        return str({self.icon: [self.phrase1, self.phrase2, self.phrase3]})

class UserKeyboard(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    keyboard_id = db.Column(db.Integer, db.ForeignKey("keyboard.id"), nullable=False)

    def __repr__(self):
        return "<Keyboard user_id={} keyboard_id={}>".format(self.user_id, self.keyboard_id)
