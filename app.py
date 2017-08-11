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
    sectione = executeQuery('SELECT DISTINCT section FROM anon ORDER BY section')
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
        beginDate = form.beginDate.data 
        endDate =  form.endDate.data
        # section choices
        sectionChoices = form.sectionMenu.data
        # scale choice 
        scaleG = form.scale.data
        # passing variables to the next route 
        session['sectionChoices'] = sectionChoices 
        session['sectionList'] = sectionL
        session['scaleGraph'] = scaleG

        return redirect(url_for('output',begin = beginDate,end = endDate))

    return render_template('main.html',title='Sign In',form=form)


def executeQuery(*query):
    if len(query)==1:
        return db.session.execute(query[0])
    if len(query)==2:
        return db.session.execute(query[0],query[1])

def xScale(start, end, filter):
    result = OrderedDict(((start + timedelta(_)).strftime(filter), None) for _ in xrange((end - start).days)).keys()
    return result

@app.route('/result/<begin>/<end>',methods = ['GET','POST'])
def output(begin,end):
    # import variables from previous pages
    scaleG = session.get('scaleGraph',None)
    section_choices = session.get('sectionChoices',None)
    section_L= session.get('sectionList',None)
    section_name_Chosen = [section_L[i] for i in section_choices]   # get the actual list of section names chosen
    section_name_Chosen_quote = [ "'"+sec+"'" for sec in section_name_Chosen]
    beginDate = datetime.strptime(begin, '%Y-%m-%d')
    endDate = datetime.strptime(end,'%Y-%m-%d')

    if len(section_name_Chosen)!= 0:
        query = "SELECT * FROM anon WHERE pdate >=" + "'"+begin+"'" +" AND pdate <=" + "'"+end+"'" +" AND section IN (" + ",".join(section_name_Chosen_quote) + ")"
        query_count = "SELECT COUNT(*) FROM anon WHERE pdate >=" + "'"+begin+"'" +" AND pdate <=" + "'"+end+"'" +" AND section IN (" + ",".join(section_name_Chosen_quote) + ")"
    else:   
        query = "SELECT * FROM anon WHERE pdate >=" + "'"+begin+"'" +" AND pdate <=" + "'"+end+"'"
        query_count = "SELECT COUNT(*) FROM anon WHERE pdate >=" + "'"+begin+"'" +" AND pdate <=" + "'"+end + "'"
    count = executeQuery(query_count).first()[0]
    # get the graph data
    if (beginDate.year == endDate.year) and (beginDate.month == endDate.month): # less than a month 
        graph = pygal.Bar(height = 200,width = 500)
        graph.title = str(begin) +" to " +str(end)
        graph.x_labels = ['NYT'] if (len(section_name_Chosen) == 0) else [] # the name of section or no name 
        # adding y values into the bar graph
        if len(section_name_Chosen) == 0: 
            countD=executeQuery('SELECT COUNT(*) FROM anon WHERE :beginDate <= pdate AND pdate <= :endDate',{'beginDate':beginDate, 'endDate':endDate}).first()[0]
            graph.add('NYT',countD) 
        else:
            for sectionName in section_name_Chosen:
                # cuztomize for each section 
                countD=executeQuery('SELECT COUNT(*) FROM anon WHERE :beginDate <= pdate AND pdate <= :endDate AND section =:sectionName',{'beginDate':beginDate, 'endDate':endDate,'sectionName':sectionName}).first()[0]
                # add to graph  for that section 
                graph.add('NYT-' + sectionName,countD) 
    else: # when dates are different in months
        graph=pygal.Line(height = 400)
        graph.title = str(begin) +" to "+str(end)
        if scaleG==1:
            months = xScale(beginDate,endDate, "%b-%Y") #list of strings of month-year 
            # add x values in the graph
            if len(section_name_Chosen) == 0: 
                q= 'SELECT COUNT(*) FROM anon WHERE :beginDate <= pdate AND pdate <= :endDate AND month=:monthInt AND year=:yearInt'
                constructGraph('%b-%Y',months,q,{'beginDate':beginDate, 'endDate':endDate},'NYT',graph) 
            else:
                for sectionName in section_name_Chosen:
                    q='SELECT COUNT(*) FROM anon WHERE :beginDate <= pdate AND pdate<= :endDate AND month=:monthInt AND year=:yearInt AND section =:sectionName'
                    constructGraph('%b-%Y',months,q,{'beginDate':beginDate, 'endDate':endDate,'sectionName':sectionName},'NYT-' + sectionName,graph)
        else:
            # x values 
            years = xScale(beginDate,endDate, "%Y")
            if len(section_name_Chosen) == 0: 
                constructGraph("%Y", years, "SELECT COUNT(*) FROM anon WHERE :beginDate <= pdate AND pdate <= :endDate AND year=:yearInt",{'beginDate':beginDate, 'endDate':endDate},'NYT',graph)
            else:
                for sectionName in section_name_Chosen:
                    constructGraph("%Y", years, "SELECT COUNT(*) FROM anon WHERE :beginDate <= pdate AND pdate <= :endDate AND year=:yearInt AND section =:sectionName",{'beginDate':beginDate, 'endDate':endDate,'sectionName':sectionName},'NYT-' + sectionName,graph)
    graph_data = graph.render_data_uri()
    return render_template('visualization.html', count = count, graph_data=graph_data, query=query)

def constructGraph(scale, x_labels, query,params,Sname, graph):
    count= counter(scale, x_labels, query,params)
    graph.x_labels= x_labels
    graph.add(Sname,count)


def counter(scale, x_labels, query,params):
    counter=[]
    for x in x_labels:
        date=datetime.strptime(x, scale)
        params['monthInt']=date.month
        params['yearInt']=date.year
        count=executeQuery(query,params).first()[0]
        counter.append(count)
    return counter

@app.route("/getPlotCSV/<query>")
def get_branch_data_file(query):
    data = db.session.execute(query)
    datal = list(data.fetchall())
    return render_template('csvoutput.html', data=datal)

@app.template_filter('pluralize')
def pluralize(number, singular='', plural='s'):
    return singular if number in (0, 1) else plural

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
