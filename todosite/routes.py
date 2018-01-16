import sqlite3
from flask import render_template, request, redirect, url_for, flash
from todosite import app
from .forms import LoginForm, RegistrationForm
from flask_login import current_user, login_user, logout_user, login_required
from .models import User, Post
from todosite import db
from werkzeug.urls import url_parse

@app.route('/')
@login_required
def index():

    todoList = []
    todoListObj = db.session.query(Post).filter_by(user=current_user.username, done=False)
    db.session.commit()
    for entry in todoListObj:
            lst = []
            lst.append(entry.id)
            lst.append(entry.entry)
            todoList.append(lst)
    
    doneList = []
    doneListObj = db.session.query(Post).filter_by(user=current_user.username, done=True)
    db.session.commit()
    for entry in doneListObj:
            lst = []
            lst.append(entry.id)
            lst.append(entry.entry)
            doneList.append(lst)
            print(doneList)
            print(entry.done)

    return render_template('index.html', todoList=todoList, doneList=doneList)

@app.route('/handleData', methods=['POST'])
def handleData():
    idea = request.form['ideaInput']
    if idea:
        entry = Post(entry=idea, user=current_user.username, group="default", done=False)
        db.session.add(entry)
        db.session.commit()
    return redirect(url_for('index'))

@app.route('/deleteEntry', methods=['POST'])
def deleteEntry():
    entryId = request.form['deleteId']
    Post.query.filter_by(id=entryId).delete()
    db.session.commit()
    return redirect(url_for('index'))

@app.route('/doneEntry', methods=['POST'])
def doneEntry():
    entryId = request.form['doneId']

    entry = db.session.query(Post).filter_by(id=entryId).first()
    entry.done = True
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