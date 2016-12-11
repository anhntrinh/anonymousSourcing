from flask import Flask, render_template, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
import models
import forms
from datetime import datetime
from datetime import date

app = Flask(__name__)
app.secret_key = 's3cr3t'
app.config.from_object('config')
db = SQLAlchemy(app, session_options={'autocommit': False})

@app.route('/',methods =['GET','POST'])
def section():
    form = forms.AnonymousFilterForm()
    count = 0
    if form.validate_on_submit():
        beginDay = form.beginDay.data
        endDay = form.endDay.data
        beginMonth = form.beginMonth.data
        endMonth = form.endMonth.data
        beginYear = form.beginYear.data
        endYear = form.endYear.data

        beginDate = date(beginYear, beginMonth, beginDay)
        print beginDate
        endDate = date(endYear, endMonth, endDay)
        print endDate
    	return redirect(url_for('output',begin = beginDate, end = endDate))
    return render_template('edit-drinker.html',title='Sign In',form=form, count=0)
                           
@app.route('/result/<begin>/<end>',methods = ['GET','POST'])
def output(begin,end):
    count = 0 
    beginDate = datetime.strptime(begin, '%Y-%m-%d')
    endDate = datetime.strptime(end, '%Y-%m-%d')
    beginYear = beginDate.year
    endYear = endDate.year
    print len(db.session.query(models.BigTable).all())
    entries= db.session.query(models.BigTable).filter(models.BigTable.year >= beginYear, models.BigTable.year <= endYear).all()
    count = len(db.session.query(models.BigTable).all())#len(entries)
    #count = db.session.execute('SELECT COUNT(*) FROM anon WHERE year > :beg',{'beg':beginYear}).first()[0]
    return render_template('drinker.html', count = count)

@app.template_filter('pluralize')
def pluralize(number, singular='', plural='s'):
    return singular if number in (0, 1) else plural

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
