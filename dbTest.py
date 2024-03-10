from flask import *
from flask_wtf import *
from wtforms import *
from wtforms.validators import DataRequired
from flask_sqlalchemy import SQLAlchemy
import requests
import os
# make sure the database username, database password and
# database name are correct
username = 'NotSilent'
password = 'Password123'
userpass = 'mysql+pymysql://' + username + ':' + password + '@'
# keep this as is for a hosted website
server  = '127.0.0.1'
# CHANGE to YOUR database name, with a slash added as shown
dbname   = '/concertchronicles'

# CHANGE NOTHING BELOW
# put them all together as a string that shows SQLAlchemy where the database is
app.config['SQLALCHEMY_DATABASE_URI'] = userpass + server + dbname

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True

db = SQLAlchemy()

# initialize the app with Flask-SQLAlchemy
db.init_app(app)

# NOTHING BELOW THIS LINE NEEDS TO CHANGE
# this route will test the database connection - and nothing more
# https://python-adv-web-apps.readthedocs.io/en/latest/flask_db2.html
@app.route('/')
def testdb():
    try:
        myAccounts = db.session.execute(db.select(Accounts).order_by(Accounts.fname)).scalars()
        allAccounts = ''
        for x in myAccounts:
            allAccounts += x.fname + ' ' + x.lname + ', Username: ' + x.username + '<br>'
        return allAccounts
    except Exception as e:
        # e holds description of the error
        error_text = "<p>The error:<br>" + str(e) + "</p>"
        hed = '<h1>Something is broken.</h1>'
        return hed + error_text

class Accounts(db.Model):
    __tablename__ = 'accounts'
    id = db.Column(db.Integer, primary_key=True)
    fname = db.Column(db.String)
    lname = db.Column(db.String)
    username = db.Column(db.String)
    password = db.Column(db.String)
    email = db.Column(db.String)

if __name__ == "__main__":
    # to run me from the command line: <flask --app main run> or <python app.py>
    #                             
    app.run(host='0.0.0.0', port=5000, debug=True)
    