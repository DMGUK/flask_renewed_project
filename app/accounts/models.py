from datetime import datetime

from flask_login import UserMixin

from app import db, login_manager, bcrypt


@login_manager.user_loader
def user_loader(user_id):
    return Users.query.get(int(user_id))


class Users(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    image_file = db.Column(db.String(40), nullable=False, default='default.jpg')
    password = db.Column(db.String(200), nullable=False)
    bio = db.Column(db.Text, nullable=True)
    last_seen = db.Column(db.DateTime, default=datetime.now().replace(microsecond=0))

    def __init__(self, username, email, password, image_file='default.jpg'):
        self.username = username
        self.email = email
        self.image_file = image_file
        self.password = bcrypt.generate_password_hash(password).decode('utf-8')

    def validate_password(self, form_password):
        return bcrypt.check_password_hash(self.password, form_password)

    def __repr__(self):
        return f"User('{self.username}', '{self.email}')"
