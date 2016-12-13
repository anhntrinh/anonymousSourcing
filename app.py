from flask import Flask, render_template, redirect, url_for, session
from flask_sqlalchemy import SQLAlchemy
import models
import forms
import pygal
from datetime import datetime,timedelta,date
from sqlalchemy import distinct
from collections import OrderedDict

app = Flask(__name__)
app.secret_key = 's3cr3t'
app.config.from_object('config')
db = SQLAlchemy(app, session_options={'autocommit': False})

@app.route('/',methods =['GET','POST'])
def section():   
    # all unique sections from table 
    #sectionL = db.session.query(distinct(models.BigTable.section)).all()
    sectione = db.session.execute('SELECT DISTINCT section FROM anon ORDER BY section')
    sectionL = [r for r, in sectione]
    i = 0
    sec=[]
    for s in sectionL: 
        sec.append((i,s))
        i = i + 1 


    form = forms.AnonymousFilterForm(sec)
    # initiate all possible choces for section box
    form.sectionMenu.choices = sec
    

    if form.validate_on_submit():
        print "validated"
        

        beginDate = form.beginDate.data 
        endDate =  form.endDate.data


        # section choices
        sectionChoices = form.sectionMenu.data # list of int 
        print sectionChoices
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

    section_name_Chosen = [section_L[i] for i in section_choices]   # get the actual list of section names chosen
    print section_name_Chosen

    beginDate = datetime.strptime(begin, '%Y-%m-%d')
    endDate = datetime.strptime(end,'%Y-%m-%d')


    #  count of total number of anon cites in the time period 
    count = db.session.execute('SELECT COUNT(*) FROM anon WHERE pdate >= :beginDate AND pdate <= :endDate',{'beginDate': beginDate,'endDate':endDate}).first()[0]
    
    
    if (beginDate.year == endDate.year) and (beginDate.month == endDate.month): # less than a month 
        graph = pygal.Bar(height = 200,width = 500)
        graph.title = "Anonymous Sourcing"
        graph.x_labels = ['NYT'] if (len(section_name_Chosen) == 0) else [] # the name of section or no name 
        # adding y values into the bar graph

        if len(section_name_Chosen) == 0: 
            countD=db.session.execute('SELECT COUNT(*) FROM anon WHERE :beginDate <= pdate AND pdate <= :endDate',{'beginDate':beginDate, 'endDate':endDate}).first()[0]
            graph.add('NYT',countD) 
        else:
            for sectionName in section_name_Chosen:
                Sname = 'NYT-' + sectionName # cuztomize for each section 
                countD=db.session.execute('SELECT COUNT(*) FROM anon WHERE :beginDate <= pdate AND pdate <= :endDate AND section =:sectionName',{'beginDate':beginDate, 'endDate':endDate,'sectionName':sectionName}).first()[0]
                # add to graph  for that section 

                graph.add(Sname,countD) 


    else: # when dates are different in months 

        graph=pygal.Line(height = 400)
        graph.title = "Anonymous Sourcing"
        if scaleG==1:
            months = monthScale(beginDate,endDate, "%b-%Y") #list of strings of month-year 
            # add x values in the graph 
            graph.x_labels= months
            if len(section_name_Chosen) == 0: 
                Sname = 'NYT'
                monthCount=[]
                for month_year in months:
                    date= datetime.strptime(month_year, '%b-%Y')
                    cMonth=db.session.execute('SELECT COUNT(*) FROM anon WHERE :beginDate <= pdate AND pdate <= :endDate AND month=:monthInt AND year=:yearInt',{'monthInt':date.month,'yearInt':date.year, 'beginDate':beginDate, 'endDate':endDate}).first()[0]
                    monthCount.append(cMonth) 
                graph.add(Sname, monthCount) 
            else:
                for sectionName in section_name_Chosen:
                    Sname = 'NYT-' + sectionName # cuztomize for each section 
                    monthCount=[]
                    for month_year in months:
                        date= datetime.strptime(month_year, '%b-%Y')
                        cMonth=db.session.execute('SELECT COUNT(*) FROM anon WHERE :beginDate <= pdate AND pdate <= :endDate AND month=:monthInt AND year=:yearInt AND section =:sectionName',{'monthInt':date.month,'yearInt':date.year, 'beginDate':beginDate, 'endDate':endDate,'sectionName':sectionName}).first()[0]
                        monthCount.append(cMonth)
               
                    # add to graph the line for that section 
                    graph.add(Sname, monthCount) 
              
             
        else:
            years = monthScale(beginDate,endDate, "%Y")
            # x values 
            graph.x_labels= years
            if len(section_name_Chosen) == 0: 
                Sname = 'NYT'
                monthCount=[]
                for year in years:
                    date= datetime.strptime(year,'%Y')
                    cMonth=db.session.execute('SELECT COUNT(*) FROM anon WHERE :beginDate <= pdate AND pdate <= :endDate AND year=:yearInt',{'yearInt':date.year, 'beginDate':beginDate, 'endDate':endDate}).first()[0]
                    monthCount.append(cMonth) 
                graph.add(Sname, monthCount) 


            for sectionName in section_name_Chosen:
                Sname = 'NYT-' + sectionName
                yearCount=[]
                for year in years:
                    date=datetime.strptime(year, '%Y')
                    cYear=db.session.execute('SELECT COUNT(*) FROM anon WHERE :beginDate <= pdate AND pdate <= :endDate AND year=:yearInt AND section =:sectionName',{'yearInt':date.year,'beginDate':beginDate, 'endDate':endDate,'sectionName':sectionName}).first()[0]
                    yearCount.append(cYear)
                
                # adding y values 
                graph.add(Sname, yearCount)
    
        

    graph_data = graph.render_data_uri()

    return render_template('drinker.html', count = count, graph_data=graph_data)

@app.template_filter('pluralize')
def pluralize(number, singular='', plural='s'):
    return singular if number in (0, 1) else plural

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
