from flask import Flask, render_template, redirect, url_for, session
from flask_sqlalchemy import SQLAlchemy
import models
import forms
from datetime import datetime
from datetime import date
from sqlalchemy import distinct


app = Flask(__name__)
app.secret_key = 's3cr3t'
app.config.from_object('config')
db = SQLAlchemy(app, session_options={'autocommit': False})


@app.route('/',methods =['GET','POST'])
def section():   
    # get all the sections 
    sectionL = db.session.query(distinct(models.BigTable.section)).all()
    i = 0
    sec=[]
    for s in sectionL: 
        sec.append((i,s))
        i = i + 1 #use index instead


    #form = forms.AnonymousFilterForm()
    form = forms.AnonymousFilterForm(sec)
    form.sectionMenu.choices = sec
    
    secd = dict(sec)
    if form.validate_on_submit():
        print "validated"
        beginDate = form.beginDate.data
        endDate = form.endDate.data
        #choice = dict(sec).get(form.sectionMenu.data)
        sectionChoices = form.sectionMenu.data # list of int 
        # passing variables to the next route 
        session['sectionChoices'] = sectionChoices 
        session['sectionList'] = sectionL

        print sectionChoices
        print secd.get(sectionChoices[0])


    	return redirect(url_for('output',begin = beginDate, end = endDate, secs = sectionChoices))
    return render_template('edit-drinker.html',title='Sign In',form=form)

                           
@app.route('/result/<begin>/<end>/<secs>',methods = ['GET','POST'])
def output(begin,end,secs):
    count = 0 
    #test
    print "output"
    section_choices = session.get('sectionChoices',None)
    section_L= session.get('sectionList',None)
    print section_choices
    pos = section_choices[0]
    print section_L[pos]
    count = db.session.execute('SELECT COUNT(*) FROM anon WHERE section = :sect',{'sect':section_L[pos]}).first()[0]

    beginDate = datetime.strptime(begin, '%Y-%m-%d')
    endDate = datetime.strptime(end, '%Y-%m-%d')
    print len(db.session.query(models.BigTable).all())
    entries= db.session.query(models.BigTable).filter(models.BigTable.year >= beginYear, models.BigTable.year <= endYear).all()
    #count = len(db.session.query(models.BigTable).all())#len(entries)
    #count = len(entries)
    #count = db.session.execute('SELECT COUNT(*) FROM anon WHERE year >= :beg and year <= :end',{'beg':beginYear, 'end':endYear}).first()[0]
    return render_template('drinker.html', count = count)

@app.template_filter('pluralize')
def pluralize(number, singular='', plural='s'):
    return singular if number in (0, 1) else plural

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
