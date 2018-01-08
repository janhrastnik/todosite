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
				entry text
	) """)
conn.commit()

c2.execute(""" CREATE TABLE IF NOT EXISTS todoneList (
				entry text
	) """)
conn2.commit()

@app.route('/')
def index():
	c.execute("SELECT * FROM todoList")
	todoList = [i[0] for i in c.fetchall()]
	todoListStr = "".join(todoList) # for testing
	conn.commit()
	
	c2.execute("SELECT * FROM todoneList")
	doneList = [i[0] for i in c2.fetchall()]
	conn2.commit()
	return render_template('index.html', todoList=todoList, doneList=doneList),  # todoListStr

@app.route('/handleData', methods=['POST'])
def handleData():
	idea = request.form['ideaInput']
	c.execute("INSERT INTO todoList VALUES (:entry)", {'entry': idea})
	conn.commit()
	return redirect(url_for('index'))

@app.route('/deleteEntry')
def deleteEntry():
	entryName = request.args.get('entryName')
	c.execute("DELETE FROM todoList WHERE entry = :entry", {"entry": entryName})
	return redirect(url_for('index'))

@app.route('/doneEntry')
def doneEntry():
	entryName = request.args.get('entryName')
	c.execute("DELETE FROM todoList WHERE entry = :entry", {"entry": entryName})
	c2.execute("INSERT INTO todoneList VALUES (:entry)", {'entry': entryName})
	return redirect(url_for('index'))

@app.route('/aFunction')
def aFunction():
	aVar = request.args.get('aVar')
	print(aVar)
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