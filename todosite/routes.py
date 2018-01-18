from flask import render_template, request, redirect, url_for, flash
from todosite import app
from .forms import LoginForm, RegistrationForm, InputForm
from flask_login import current_user, login_user, logout_user, login_required
from .models import User, Post, Group
from todosite import db
from werkzeug.urls import url_parse
import re

@app.route('/')
@login_required
def index():

    todoList = [(post.id, post.entry, post.group) for post in db.session.query(Post).filter_by(done=False).all()]
    doneList = [(post.id, post.entry, post.group) for post in db.session.query(Post).filter_by(done=True).all()]
    
    user = db.session.query(User).filter_by(username=current_user.username).first()
    groups = [(group.id, group.name) for group in user.groupsOfUser]

    form = InputForm()

    return render_template('index.html', todoList=todoList, doneList=doneList, allGroupsOfCurentUser=groups, form=form)

@app.route('/handleData', methods=['POST'])
def handleData():
    print(request.form)
    print(request.form['group'])
    data = request.form
    print(str(data))

    idea = request.form['entry']
    groupname = request.form['group']
    if idea and groupname:
        db.session.add(Post(entry=idea, user=current_user.username, group=groupname, done=False))
        db.session.commit()
    return redirect(url_for('index'))

@app.route('/deleteEntry', methods=['POST'])
def deleteEntry():
    entryId = request.form['deleteId']
    db.session.query(Post).filter_by(id=entryId).delete()
    db.session.commit()
    return redirect(url_for('index'))

@app.route('/doneEntry', methods=['POST'])
def doneEntry():
    entryId = request.form['doneId']

    db.session.query(Post).filter_by(id=entryId).first().done = True
    db.session.commit()

    return redirect(url_for('index'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('index')

        return redirect(next_page)
    return render_template('login.html', title='Sign In', form=form)

@app.route('/test')
def test():
    print(current_user.username)
    return redirect(url_for('index'))

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))


@app.route('/register', methods=['GET', 'POST'])
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

@app.route('/makeGroup', methods=['POST'])
def makeGroup():
    groupName = Group(name=request.form['groupNameInput'])
    print(groupName)
    if groupName:
        user = User.query.filter_by(username=current_user.username).first()
        groupName.usersInGroup.append(user)
        db.session.commit()
    return redirect(url_for('index'))

@app.route('/addUser', methods=['POST'])
def addUser():
    group = request.form['groupName']
    pattern = re.compile(r"'(.*)\'")
    matches = pattern.finditer(group)
    for match in matches:
        group = match.group(0)[1:-1]
    groupName = Group.query.filter_by(name=group).first()
    newuser = User.query.filter_by(username=request.form['addUserInput']).first()
    groupName.usersInGroup.append(newuser)
    db.session.commit()
    return redirect(url_for('index'))