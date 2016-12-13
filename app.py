from flask import Flask, render_template, redirect, url_for, session
from flask_sqlalchemy import SQLAlchemy
import models
import forms
import pygal
from datetime import datetime, timedelta
from datetime import date
from sqlalchemy import distinct
from collections import OrderedDict



app = Flask(__name__)
app.secret_key = 's3cr3t'
app.config.from_object('config')
db = SQLAlchemy(app, session_options={'autocommit': False})


@app.route('/',methods =['GET','POST'])
def section():   
    # all unique sections from table 
    sectionL = db.session.query(distinct(models.BigTable.section)).all()
    i = 0
    sec=[]
    for s in sectionL: 
        sec.append((i,s))
        i = i + 1 


    #form = forms.AnonymousFilterForm()
    form = forms.AnonymousFilterForm(sec)
    # initiate all possible choces for section box
    form.sectionMenu.choices = sec
    
    secd = dict(sec)
    
    if form.validate_on_submit():
        print "validated"
    
        beginDate = form.beginDate.data 
        endDate =  form.endDate.data


        # section choices
        sectionChoices = form.sectionMenu.data # list of int 
        # scale choice 
        scaleG = form.scale.data

        # passing variables to the next route 
        session['sectionChoices'] = sectionChoices 
        session['sectionList'] = sectionL
        session['scaleGraph'] = scaleG

    	return redirect(url_for('output',begin = beginDate, end = endDate))
    return render_template('edit-drinker.html',title='Sign In',form=form)

                       
def monthScale(start, end, filter):
    result = OrderedDict(((start + timedelta(_)).strftime(filter), None) for _ in xrange((end - start).days)).keys()
    return result


@app.route('/result/<begin>/<end>',methods = ['GET','POST'])
def output(begin,end):
    
    print "output"
    count = 0 
    # import variables from previous pages
    scaleG = session.get('scaleGraph',None)
    section_choices = session.get('sectionChoices',None)
    section_L= session.get('sectionList',None)
    #pos = section_choices[0] # get the index of the selected section in the section list 

    #count = db.session.execute('SELECT COUNT(*) FROM anon WHERE section = :sect',{'sect':section_L[pos]}).first()[0]
    

    beginDate = datetime.strptime(begin, '%Y-%m-%d')
    endDate = datetime.strptime(end,'%Y-%m-%d')
   
   
    #count = db.session.execute('SELECT COUNT(*) FROM anon WHERE pdate > :beginD',{'beginD':beginDate}).first()[0]    
    #print count 


    #entries= db.session.query(models.BigTable).filter(models.BigTable.year >= beginYear, models.BigTable.year <= endYear).all()
    #count = len(db.session.query(models.BigTable).all())#len(entries)
    #count = len(entries)
    #count = db.session.execute('SELECT COUNT(*) FROM anon WHERE year >= :beg and year <= :end',{'beg':beginYear, 'end':endYear}).first()[0]
    

    #filter 
    #tableBeginDate = db.session.execute('SELECT * FROM anon WHERE day > :beginDay AND month  ') need pdate format



    graph=pygal.Line()
    graph.title = "Anonymous Sourcing"
    if scaleG==1:
        months = monthScale(beginDate,endDate, "%b-%Y") #list of strings of month-year 

        monthCount=[]
        for monthInt in months:
            date= datetime.strptime(monthInt, '%b-%Y')
            cMonth=db.session.execute('SELECT COUNT(*) FROM anon WHERE :beginDate <pdate AND pdate <:endDate AND month=:monthInt AND year=:yearInt',{'monthInt':date.month,'yearInt':date.year, 'beginDate':beginDate, 'endDate':endDate}).first()[0]
            monthCount.append(cMonth)
        print monthCount
        graph.x_labels= months  
        graph.add('NYT', monthCount)  

    else:
        years = monthScale(beginDate,endDate, "%Y")
        yearCount=[]
        for year in years:
            date=datetime.strptime(year, '%Y')
            cYear=db.session.execute('SELECT COUNT(*) FROM anon WHERE :beginDate>pdate AND pdate<:endDate AND year=:yearInt',{'yearInt':date.year,'beginDate':beginDate, 'endDate':endDate}).first()[0]
            yearCount.append(cYear)
        print yearCount
        graph.x_labels= years
        graph.add('NYT', yearCount)

    graph_data = graph.render_data_uri()

    return render_template('drinker.html', count = count, graph_data=graph_data)

@app.template_filter('pluralize')
def pluralize(number, singular='', plural='s'):
    return singular if number in (0, 1) else plural

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
