import sqlite3
from flask import render_template, request, redirect, url_for, flash
from todosite import app
from .forms import LoginForm, RegistrationForm
from flask_login import current_user, login_user, logout_user, login_required
from .models import User
from todosite import db
from werkzeug.urls import url_parse

conn = sqlite3.connect('todoList.db')
conn.text_factory = str
c = conn.cursor()

c.execute(""" CREATE TABLE IF NOT EXISTS todoList (
                entry text NOT NULL,
                username text NOT NULL,
                done integer NOT NULL
    ) """)
conn.commit()

@app.route('/')
@login_required
def index():
    c.execute("SELECT rowid, entry FROM todoList WHERE done = 0 AND username = :username", {'username':current_user.username})
    todoList = c.fetchall()
    conn.commit()

    c.execute("SELECT rowid, entry FROM todoList WHERE done = 1 AND username = :username", {'username':current_user.username})
    doneList = c.fetchall()
    conn.commit()

    return render_template('index.html', todoList=todoList, doneList=doneList)

@app.route('/handleData', methods=['POST'])
def handleData():
    idea = request.form['ideaInput']
    if idea:
        c.execute("INSERT INTO todoList VALUES (:entry, :done, :username)", {'entry': idea, 'done': 0, 'username':current_user.username})
        conn.commit()
    return redirect(url_for('index'))

@app.route('/deleteEntry', methods=['POST'])
def deleteEntry():
    entryId = request.form['deleteId']
    c.execute("DELETE FROM todoList WHERE rowid = :Id", {"Id": entryId})
    conn.commit()
    return redirect(url_for('index'))

@app.route('/doneEntry', methods=['POST'])
def doneEntry():
    entryId = request.form['doneId']

    c.execute("UPDATE todoList SET done = :done WHERE rowid = :Id", {"done": 1, "Id": entryId})
    conn.commit()

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