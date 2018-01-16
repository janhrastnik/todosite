from todosite import db
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from todosite import login

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    groups = db.Column

    def __repr__(self):
        return '<User {}>'.format(self.username)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

class Group(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    groupname = db.Column(db.String(64), index=True, unique=True)

class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    entry = db.Column(db.String())
    user = db.Column(db.String(), index=True)
    group = db.Column(db.String())
    done = db.Column(db.Boolean())

    def __repr__(self):
        return '<Post {} {} {} {} {}>'.format(self.id, self.entry, self.user, self.group, self.done)

@login.user_loader
def load_user(id):
    return User.query.get(int(id))