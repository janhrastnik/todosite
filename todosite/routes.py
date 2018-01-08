import sqlite3
from flask import render_template, request, redirect, url_for
from todosite import app

conn = sqlite3.connect('todoList.db')
conn.text_factory = str
c = conn.cursor()

conn2 = sqlite3.connect('todoneList.db')
conn2.text_factory = str
c2 = conn2.cursor()

c.execute(""" CREATE TABLE IF NOT EXISTS todoList (
				entry text NOT NULL
	) """)
conn.commit()

c2.execute(""" CREATE TABLE IF NOT EXISTS todoneList (
				entry text NOT NULL
	) """)
conn2.commit()

@app.route('/')
def index():
	c.execute("SELECT rowid,* FROM todoList")
	conn.commit()

	c2.execute("SELECT * FROM todoneList")
	conn2.commit()

	return render_template('index.html', todoList=c.fetchall(), doneList=c2.fetchall()),

@app.route('/handleData', methods=['POST'])
def handleData():
	idea = request.form['ideaInput']
	if idea:
		c.execute("INSERT INTO todoList VALUES (:entry)", {'entry': idea})
		conn.commit()
	return redirect(url_for('index'))

@app.route('/deleteEntry')
def deleteEntry():
	entryId = request.args.get('entryId')
	c.execute("DELETE FROM todoList WHERE rowid = :Id", {"Id": entryId})
	conn.commit()
	return redirect(url_for('index'))

@app.route('/doneEntry')
def doneEntry():
	entryId = request.args.get('entryId')

	c.execute("SELECT entry FROM todoList WHERE rowid = :Id", {"Id": entryId})
	entryToInsert = c.fetchall()[0][0]
	conn.commit()

	c.execute("DELETE FROM todoList WHERE rowid = :Id", {"Id": entryId})
	conn.commit()

	c2.execute("INSERT INTO todoneList VALUES (:entryToInsert)", {'entryToInsert': entryToInsert})
	conn2.commit()
	return redirect(url_for('index'))

"""
@app.route('/test', methods=['POST'])
def test():
	testentry = request.form['test']
	return testentry


@app.teardown_appcontext
def close_db(error):
	conn.close()
"""