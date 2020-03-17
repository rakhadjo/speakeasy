from flask_login import current_user
from app import db
from app.models import User, UserKeyboard, Keyboard

def add_user(username, email, password):
    user = User(username=username, email=email)
    user.set_password(password)
    db.session.add(user)
    db.session.commit()

def zip_extend(a, b):
    """Extended zip for a niche application"""
    a = iter(a)
    b = iter(b)
    while True:
        try:
            next_a = next(a)
        except StopIteration:
            next_a = (None, None)
        try:
            next_b = next(b)
        except StopIteration:
            next_b = None
        if next_a == (None, None) and next_b is None:
            return
        yield next_a, next_b

def update_keyboards_db(keyboards, user_id = None):
    if user_id is None:
        user_id = current_user.id
    keyboard_ids = [k.keyboard_id for k in UserKeyboard.query.filter_by(user_id=user_id)]
    pos_from_keyboard_id = lambda id: Keyboard.query.filter_by(id=id).first().position
    keyboard_ids = sorted(keyboard_ids, key = pos_from_keyboard_id)
    new_keyboards = 0
    phrase_attrs = ("phrase1", "phrase2", "phrase3")
    for i, ((icon, phrases), id) in enumerate(zip_extend(keyboards.items(), keyboard_ids)):
        if icon is None:
            Keyboard.query.filter_by(id=id).delete()
            continue
        if id is None:
            db.session.add(Keyboard(
                icon=icon,
                position=i,
                **{attr:val for attr, val in zip(phrase_attrs, phrases)}))
            new_keyboards += 1
        else:
            k = Keyboard.query.filter_by(id=id).first()
            k.icon = icon
            k.phrase1, k.phrase2, k.phrase3 = phrases
    db.session.commit()
    if new_keyboards:
        first_keyboard_id = Keyboard.query.order_by(Keyboard.id).all()[-1].id - (new_keyboards - 1)
        keyboard_ids = (first_keyboard_id + i for i in range(new_keyboards))
        for keyboard_id in keyboard_ids:
            db.session.add(UserKeyboard(user_id=user_id, keyboard_id=keyboard_id))
        db.session.commit()

def update_accent_db(accent, gender, speed):
    user = User.query.filter_by(id=current_user.id).first()
    user.accent = accent
    user.gender = gender
    user.speed = 1 + ((speed-50)/100)
    db.session.commit()

def update_password_db(password, new_password):
    user = User.query.filter_by(id=current_user.id).first()
    user.set_password(new_password)
    db.session.commit()

def update_email_db(email):
    user = User.query.filter_by(id=current_user.id).first()
    user.email = email
    db.session.commit()

def get_user_keyboards():
    user_keyboards = UserKeyboard.query.filter_by(user_id=current_user.id)
    keyboard_ids = (uk.keyboard_id for uk in user_keyboards)
    keyboard_list = (Keyboard.query.filter_by(id=id).first() for id in keyboard_ids)
    keyboard_list = sorted(keyboard_list, key = lambda k: k.position)
    keyboards = {k.icon:[k.phrase1, k.phrase2, k.phrase3] for k in keyboard_list}
    return keyboards
