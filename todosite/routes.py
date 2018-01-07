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

c2.execute(""" CREATE TABLE IF NOT EXISTS todonelist (
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
def table():
	c.execute("SELECT * FROM todolist")
	todolist = [i[0] for i in c.fetchall()]
	todoliststr = "".join(todolist) # for testing
	conn.commit()
	
	c2.execute("SELECT * FROM todonelist")
	donelist = [i[0] for i in c2.fetchall()]
	conn2.commit()
	return render_template('todolist.html', todolist=todolist, donelist=donelist),  # todoliststr


@app.route('/delete_entry', methods=['POST'])
def delete_entry():
	entryname = request.form['deleteEntry']
	print(entryname)
	c.execute("DELETE FROM todolist WHERE entry = :entry", {"entry": entryname})
	return redirect(url_for('table'))

@app.route('/done_entry', methods=['POST'])
def done_entry():
	entryname = request.form['doneEntry']
	c.execute("DELETE FROM todolist WHERE entry = :entry", {"entry": entryname})
	c2.execute("INSERT INTO todonelist VALUES (:entry)", {'entry': entryname})
	return redirect(url_for('table'))

@app.route('/aFunction')
def aFunction():
	aVar = request.args.get('aVar')
	print(aVar)
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