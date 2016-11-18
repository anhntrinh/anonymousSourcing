from flask import Flask, render_template, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
import models
import forms

app = Flask(__name__)
app.secret_key = 's3cr3t'
app.config.from_object('config')
db = SQLAlchemy(app, session_options={'autocommit': False})

@app.route('/')
def year():
    year = db.session.query(models.Date).all()
    return render_template('all-drinkers.html', drinkers=drinkers)

@app.route('/year/<name>')
def phrase(name):
    drinker = db.session.query(models.anonymoussource)\
        .filter(models.anonymoussource.name == name).one()
    return render_template('drinker.html', drinker=drinker)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
