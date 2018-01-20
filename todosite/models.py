from . import db
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from . import login

groupUserAssociationTable = db.Table('gpAssociation',
    db.Column('groupId', db.Integer, db.ForeignKey('groupTable.id'), primary_key=True),
    db.Column('userId', db.Integer, db.ForeignKey('userTable.id'), primary_key=True),
)

class User(UserMixin, db.Model):
    __tablename__ = "userTable"
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    groups  =db.Column
    groupsOfUser = db.relationship('Group', secondary=groupUserAssociationTable, backref=db.backref('usersInGroup'))

    def __repr__(self):
        return '<User {}>'.format(self.username)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)


class Group(db.Model):
    __tablename__ = 'groupTable'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), index=True, unique=True)

    def __repr__(self):
        return '<Group: {} {}>'.format(self.name, self.usersInGroup)
    
class Post(db.Model):
    __tablename__ = 'PostTable'
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