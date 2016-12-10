from flask import Flask, render_template, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
import models
import forms

app = Flask(__name__)
app.secret_key = 's3cr3t'
app.config.from_object('config')
db = SQLAlchemy(app, session_options={'autocommit': False})


@app.route('/')
def section():
    #section = db.session.query(models.BigTable.section).all()
    agency = db.session.query(models.BigTable.agency).all()
    section = db.session.query(models.BigTable.section).all()
    #form = forms.DrinkerEditFormFactory.form(agency,section)
    #return render_template('edit-drinker.html', form = form)
    return render_template('all-drinkers.html', section = section)

@app.template_filter('pluralize')
def pluralize(number, singular='', plural='s'):
    return singular if number in (0, 1) else plural

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
