# all the imports
from __future__ import with_statement
import sqlite3
from flask import Flask, request, session, g, redirect, url_for, \
    abort, render_template, flash
from contextlib import closing


# configuration
DATABASE = '/tmp/flaskr.db'
DEBUG = True
SECRET_KEY = 'development key' #TODO change this!!!!
CURRENT_USER = None
# create our little application :)
app = Flask(__name__)
app.config.from_object(__name__)

app.config.from_envvar('FLASKR_SETTINGS', silent=True)


def connect_db():
    return sqlite3.connect(app.config['DATABASE'])

def init_db():
    with closing(connect_db()) as db:
        with app.open_resource('schema.sql') as f:
            db.cursor().executescript(f.read())
        db.commit()

@app.before_request
def before_request():
    g.db = connect_db()

@app.after_request
def after_request(response):
    g.db.close()
    return response


@app.route('/')
def index():
    try:
        print session['logged_in']
        return redirect(url_for('show_entries'))
    except:
        return redirect(url_for('login'))

@app.route('/show')
def show_entries():
    cur = g.db.execute('select title, text, users_id from entries order by id desc')
    entries = [dict(title=row[0], text=row[1], users_id=row[2]) for row in cur.fetchall()]
    try:
        return render_template('show_entries.html', entries=entries, cur_user=session['CURRENT_USER'])
    except:
        return redirect(url_for('login'))

@app.route('/add', methods=['POST'])
def add_entry():
    if not session.get('logged_in'):
        abort(401)
    g.db.execute('insert into entries (title, text, users_id) values (?, ?, ?)',
        [request.form['title'], request.form['text'], session['CURRENT_USER']])
    g.db.commit()
    flash('New entry was successfully posted')
    return redirect(url_for('show_entries'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    user = g.db.execute('select username, password, id from users')
    user_info = [dict(username=row[0],  password=row[1], users_id=row[2]) for row in user.fetchall()]
    error = None
    if request.method == 'POST':
        for i in xrange(len(user_info)):
            if request.form['username'] != user_info[i-1]['username']:
                error = 'Invalid username'
            elif request.form['password'] != user_info[i-1]['password']:
                error = 'Invalid password'
            else:
                session['CURRENT_USER'] = user_info[i-1]['users_id']
                session['logged_in'] = True
                flash('You were logged in')
                return redirect(url_for('show_entries'))
                break
    return render_template('login.html', error=error)

@app.route('/newuser', methods=['GET', 'POST'])
def new_user():
    error = None
    user_name = g.db.execute('select username from users')
    user_name_info = [str(h[0]) for h in user_name.fetchall()]
    if request.method == 'POST':
        try:
            user_name_info[user_name_info.index(request.form['username'])] # just to see if it brakes
            error = "User already exists"
            return render_template('new_user.html', error=error)
        except:
            if request.form['password'] == request.form['confpassword']:
                g.db.execute('insert into users (username, password) values (?, ?)',
                    [request.form['username'], request.form['password']])
                g.db.commit()
                flash('Your account has been created!')
                return redirect(url_for('login'))
            else:
                error = "Passwords didn't match"
                return render_template('new_user.html', error=error)
    else:
        return render_template("new_user.html")

@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    session.pop('CURRENT_USER', None)
    flash('You were logged out')
    return redirect(url_for('show_entries'))

if __name__ == '__main__':
    app.run()

