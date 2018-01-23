from flask import render_template, request, redirect, url_for, flash
from todosite import app
from .forms import LoginForm, RegistrationForm, InputForm
from flask_login import current_user, login_user, logout_user, login_required
from .models import User, Post, Group
from todosite import db
from werkzeug.urls import url_parse

def indexDataGenerator():
    todoList = [(post.id, post.entry, post.group) for post in db.session.query(Post).filter_by(done=False).all()]
    doneList = [(post.id, post.entry, post.group) for post in db.session.query(Post).filter_by(done=True).all()]
    
    user = db.session.query(User).filter_by(username=current_user.username).first()
    groups = [group for group in user.groupsOfUser]    
    return todoList, doneList, groups


@app.route('/')
@login_required
def index():
    form = InputForm()
    todoList, doneList, groups = indexDataGenerator()
    return render_template('index.html', todoList=todoList, doneList=doneList, allGroupsOfCurentUser=groups, form=form)

@app.route('/handleData', methods=['POST'])
@login_required
def handleData():
    idea = request.form['entry']
    groupname = request.form['hidden']
    if InputForm(request.form).validate_on_submit():
        db.session.add(Post(entry=idea, user=current_user.username, group=groupname, done=False))
        db.session.commit()
    else:
        flash("Your idea can't be empty!")
    return redirect(url_for('index'))

@app.route('/deleteEntry', methods=['POST'])
@login_required
def deleteEntry():
    entryId = request.form['hidden']
    db.session.query(Post).filter_by(id=entryId).delete()
    db.session.commit()
    return redirect(url_for('index'))

@app.route('/doneEntry', methods=['POST'])
@login_required
def doneEntry():
    entryId = request.form['hidden']

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
            flash("Wrong credentials. Please try again.")
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('index')
        return redirect(next_page)
    return render_template('login.html', title='Sign In', form=form)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

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
        return redirect(url_for('index'))
    return render_template('register.html', title='Register', form=form)

@app.route('/makeGroup', methods=['POST'])
@login_required
def makeGroup():
    form = InputForm(request.form)
    if form.validate_on_submit():
        try:
            group = Group(name=request.form['entry'])
            db.session.add(group)
            db.session.commit()

            group.usersInGroup.append(User.query.filter_by(username=current_user.username).first())
            db.session.commit()
        except:
            flash("Group already exists!")
    else:
        flash("Group name can't be empty.")
    return redirect(url_for('index'))

@app.route('/addUser', methods=['POST'])
@login_required
def addUser():
    form = InputForm(request.form)
    if form.validate_on_submit():    
        try:
            group = Group.query.filter_by(name=request.form['hidden']).first()
            newuser = User.query.filter_by(username=request.form['entry']).first()
            group.usersInGroup.append(newuser)
            db.session.commit()
        except:
            flash("User does not exist!")
    else:
        flash("User name can't be empty!")
    return redirect(url_for('index'))

@app.route('/deleteGroup', methods=['POST'])
@login_required
def deleteGroup(groupToDelete=False):
    group = groupToDelete or Group.query.filter_by(id=request.form['hidden']).first()
    group.usersInGroup = []

    Post.query.filter_by(group=group.name).delete()
    db.session.delete(group)
    db.session.commit()

    return redirect(url_for('index'))

@app.route('/deleteUser', methods=['POST'])
@login_required
def deleteUser():
    form = InputForm(request.form)
    
    userId, groupId = tuple(form.hidden.data)
    group = Group.query.filter_by(id=groupId).first()
    user = User.query.filter_by(id=userId).first()

    group.usersInGroup.remove(user)
    db.session.commit()

    if not group.usersInGroup:
        deleteGroup(group)

    return redirect(url_for('index'))