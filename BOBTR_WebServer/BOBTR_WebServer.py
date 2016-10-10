import requests
import os 
import click
from sqlite3 import dbapi2 as sqlite3
from flask import Flask, request, session, g, redirect, url_for, abort, render_template, flash

app = Flask(__name__)
app.config.from_object(__name__)

app.config.update(dict(
    DATABASE=os.path.join(app.root_path, 'BOBTR.db'),
    SECRET_KEY='development key',
    USERNAME='admin',
    PASSWORD='default'
))

app.config.from_envvar('BOBTR_WEBSERVER_SETTINGS', silent=True)

def connect_db():
    """connects to the specific database and allows rows to be stored as objects for dictionary manipulation."""
    rv = sqlite3.connect(app.config['DATABASE'])
    rv.row_factory = sqlite3.Row
    return rv

def init_db():
    r = requests.get('https://titanic.businessoptics.biz/survival/')
    data = r.json() 
    
    db = get_db()
    with app.open_resource('schema.sql', mode='r') as f:
        db.cursor().executescript(f.read())
    for row in data:
        embarked = row['Embarked']
        sex = row['sex']
        survived = int(row['survived'])
        siblings_and_spouses= int(row['number_of_siblings_and_spouses_aboard'])
        passenger_id = int(row['passenger_id'])
        class_= int(row['class'])
        cabin = row['Cabin']
        if row['Fare'] != '':
            fare = float(row['Fare'])
        else:
            fare=None            
        name = row['name']
        if row['age'] != '':
            age = float(row['age'])
        else:
            age=None
        parents_and_children= int(row['number_of_parents_and_children_aboard'])
        ticket_number = row['ticket_number']
        db.execute('insert into entries (Embarked, Sex, Survived, Number_of_siblings_and_spouses_aboard, Passenger_id, Class, Cabin, Fare, Name, Age, Number_of_parents_and_children_aboard, Ticket_number) values (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)', (embarked, sex, survived, siblings_and_spouses, passenger_id, class_, cabin, fare, name, age, parents_and_children, ticket_number))
    db.commit()
        
@app.cli.command('initdb')
def initdb_command():
    """Initializes the database."""
    init_db()
    print('Initialized the database')

def get_db():
    """ opens a new database connection if there is none yet (application context)."""
    if not hasattr(g, 'sqlite_db'):
        g.sqlite_db = connect_db()
    return g.sqlite_db
    
@app.teardown_appcontext
def close_db(error):
    """close the database again at the end of the request."""
    if hasattr(g, 'sqlite_db'):
        g.sqlite_db.close()
        
@app.route('/')
def show_entries():
    db = get_db()
    cur = db.execute('select Embarked, Sex, Survived, Number_of_siblings_and_spouses_aboard, Passenger_id, Class, Cabin, Fare, Name, Age, Number_of_parents_and_children_aboard, Ticket_number from entries order by Name desc')
    entries = cur.fetchall()
    return render_template('show_entries.html', entries=entries)

@app.route('/add', methods=['POST'])
def add_entry():
    if not session.get('logged_in'):
        abort(401)
    db = get_db()
    db.execute('insert into entries (Embarked, Sex, Survived, Number_of_siblings_and_spouses_aboard, Passenger_id, Class, Cabin, Fare, Name, Age, Number_of_parents_and_children_aboard, Ticket_number) values (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)', [request.form['Embarked'], request.form['Sex'], int(request.form['Surived']), int(request.form['Number_Siblings_and_spouses']), int(request.form['ID']), int(request.form['Class']), request.form['Cabin'], float(request.form['Fare']), request.form['Name'], int(request.form['Age']), int(request.form['Number_Parents_and_children']), request.form['Ticket_number']])
    db.commit()
    flash('New entry was successfully posted')
    return redirect(url_for('show_entries'))
@app.route('/sex_query', methods=['GET','POST'])
def sex_query():
    db = get_db()
    cur = db.execute('select Sex, (count(Survived)*100/(select count(Sex) from entries)) as Survival_Rate_Percentage from entries where Survived=1 group by Sex')
    entries = cur.fetchall()
    return render_template('show_entries.html', entries=entries)  
@app.route('/age_query', methods=['GET','POST'])
def age_query():
    db = get_db()
    cur = db.execute('select Age, (count(Survived)*100/(select count(Age) from entries)) as Survival_Rate_Percentage from entries where Survived=1 group by Age')
    entries = cur.fetchall()
    return render_template('show_entries.html', entries=entries)
@app.route('/class_query', methods=['GET','POST'])
def class_query():
    db = get_db()
    cur = db.execute('select Class, (count(Survived)*100/(select count(Class) from entries)) as Survival_Rate_Percentage from entries where Survived=1 group by Class')
    entries = cur.fetchall()
    return render_template('show_entries.html', entries=entries)
@app.route('/jack_query', methods=['GET','POST'])
def jack_query():
    db = get_db()
    cur = db.execute('select Name, (count(Survived)*100/(select count(Name) from entries)) as Survival_Rate_Percentage from entries where Survived=1 and Name like ?', ['Jack'] )
    entries = cur.fetchall()
    return render_template('show_entries.html', entries=entries)
@app.route('/rose_query', methods=['GET','POST'])
def rose_query():
    db = get_db()
    cur = db.execute('select Name, (count(Survived)*100/(select count(Name) from entries)) as Survival_Rate_Percentage from entries where Survived=1 and Name like ?', ['Rose'])
    entries = cur.fetchall()
    return render_template('show_entries.html', entries=entries)
@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        if request.form['username'] != app.config['USERNAME']:
            error = 'Invalid username'
        elif request.form['password'] != app.config['PASSWORD']:
            error = 'Invalid password'
        else:
            session['logged_in'] = True
            flash('You were logged in')
            return redirect(url_for('show_entries'))
    return render_template('login.html', error=error)

@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    flash('You were logged out')
    return redirect(url_for('show_entries'))