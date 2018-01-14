import sqlite3
from flask import render_template, request, redirect, url_for
from todosite import app

conn = sqlite3.connect('todoList.db')
conn.text_factory = str
c = conn.cursor()

c.execute(""" CREATE TABLE IF NOT EXISTS todoList (
				entry text NOT NULL,
				done integer NOT NULL
	) """)
conn.commit()

@app.route('/')
def index():
	c.execute("SELECT rowid,* FROM todoList WHERE done = 0")
	todoList = c.fetchall()
	conn.commit()

	c.execute("SELECT rowid,* FROM todoList WHERE done = 1")
	doneList = c.fetchall()
	conn.commit()

	return render_template('index.html', todoList=todoList, doneList=doneList)

@app.route('/handleData', methods=['POST'])
def handleData():
	idea = request.form['ideaInput']
	if idea:
		c.execute("INSERT INTO todoList VALUES (:entry, :done)", {'entry': idea, 'done': 0})
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


@app.route('/test')
def test():
	c.execute("SELECT * FROM todoList")
	return str(c.fetchall())