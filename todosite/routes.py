import sqlite3
from flask import render_template, request, redirect, url_for
from todosite import app

conn = sqlite3.connect('todolist.db')
conn.text_factory = str
c = conn.cursor()

conn2 = sqlite3.connect('todonelist.db')
conn2.text_factory = str
c2 = conn2.cursor()

c.execute(""" CREATE TABLE IF NOT EXISTS todolist (
				entry text
	) """)
conn.commit()

c2.execute(""" CREATE TABLE IF NOT EXISTS todolist (
				entry text
	) """)
conn2.commit()




@app.route('/handle_data', methods=['POST'])
def handle_data():
	idea = request.form['ideaInput']
	c.execute("INSERT INTO todolist VALUES (:entry)", {'entry': idea})
	conn.commit()
	return redirect(url_for('table'))


@app.route('/')
@app.route('/index')
def table():
	c.execute("SELECT * FROM todolist")
	todolist = [i[0] for i in c.fetchall()]
	todoliststr = "".join(todolist)
	conn.commit()
	return render_template('todolist.html', todolist=todolist),  # todoliststr


@app.route('/delete_entry', methods=['POST'])
def delete_entry():
	entryid = request.form['deleteEntry']
	c.execute("DELETE FROM todolist WHERE entry = :entryid", {"entryid": entryid})
	return redirect(url_for('table'))
"""

@app.route('/test', methods=['POST'])
def test():
	testentry = request.form['test']
	return testentry


@app.teardown_appcontext
def close_db(error):
	conn.close()
"""
