from flask import Flask, render_template, redirect, url_for, session, make_response
from flask_sqlalchemy import SQLAlchemy
import models
import forms
import pygal
from datetime import datetime,timedelta,date
from sqlalchemy import distinct
from collections import OrderedDict
import csv


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

    
    # import variables from previous pages
    scaleG = session.get('scaleGraph',None)
    section_choices = session.get('sectionChoices',None)
    section_L= session.get('sectionList',None)

    section_name_Chosen = [section_L[i] for i in section_choices]   # get the actual list of section names chosen
    print section_name_Chosen

    section_name_Chosen_quote = [ "'"+sec+"'" for sec in section_name_Chosen]

    beginDate = datetime.strptime(begin, '%Y-%m-%d')
    endDate = datetime.strptime(end,'%Y-%m-%d')

    count = 0 
    #  count of total number of anon cites in the time period 
    count = db.session.execute('SELECT COUNT(*) FROM anon WHERE pdate >= :beginDate AND pdate <= :endDate',{'beginDate': beginDate,'endDate':endDate}).first()[0]
    


    # query for csv output
    query = ""
    if len(section_name_Chosen)!= 0:
        query = "SELECT * FROM anon WHERE pdate >=" + "'"+begin+"'" +" AND pdate <=" + "'"+end+"'" +" AND section IN (" + ",".join(section_name_Chosen_quote) + ")"
    else:   
        query = "SELECT * FROM anon WHERE pdate >=" + "'"+begin+"'" +" AND pdate <=" + "'"+end+"'"
    print("query " + query)

    # get the csv data
    
 
    '''
    if len(section_name_Chosen)>0:
        queryResult = db.session.execute('SELECT * FROM anon WHERE pdate >= :beginDate AND pdate <= :endDate AND section IN :sections',{'beginDate': beginDate,'endDate':endDate,'sections':section_name_Chosen})
    else:
        queryResult = db.session.execute('SELECT * FROM anon WHERE pdate >= :beginDate AND pdate <= :endDate',{'beginDate': beginDate,'endDate':endDate})
'''
    queryResult = db.session.execute('SELECT * FROM anon WHERE pdate >= :beginDate AND pdate <= :endDate',{'beginDate': beginDate,'endDate':endDate})
    
    #result = get_branch_data_file(queryResult)

    # get the graph data
    if (beginDate.year == endDate.year) and (beginDate.month == endDate.month): # less than a month 
        graph = pygal.Bar(height = 200,width = 500)
        graph.title = str(begin) +" to " +str(end)
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
        graph.title = str(begin) +" to "+str(end)
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

    return render_template('drinker.html', count = count, graph_data=graph_data, query=query)

@app.route("/getPlotCSV/<query>")
def get_branch_data_file(query):
    data = db.session.execute(query)
    print "number of rows " + str(data.rowcount)
    datal = list(data.fetchall())
    return render_template('csvoutput.html', data=datal)

    '''
    (file_basename, server_path, file_size) = create_csv(data)
    return_file = open(server_path+file_basename, 'r')
    response = make_response(return_file,200)
    response.headers['Content-Description'] = 'File Transfer'
    response.headers['Cache-Control'] = 'no-cache'
    response.headers['Content-Type'] = 'text/csv'
    response.headers['Content-Disposition'] = 'attachment; filename=%s' % file_basename
    response.headers['Content-Length'] = file_size
    return response

## function to create csv from the SQLAlchemy query response object


def create_csv(data):
    """ returns (file_basename, server_path, file_size) """
    file_basename = 'output.csv'
    server_path = '/'
    #w_file = open(server_path+file_basename,'w+')
    w_file =open(r"/output.csv","w+")
    w_file.write('title,link,agency,day,month,year,phrase,section,snip,pdate \n')
    
    for row in data:
        row_as_string = str(row)
        w_file.write(row_as_string[1:-1] + '\n') ## row_as_string[1:-1] because row is a tuple

    w_file.close()

    w_file = open(server_path+file_basename,'r')
    file_size = len(w_file.read())
    return file_basename, server_path, file_size

'''
@app.template_filter('pluralize')
def pluralize(number, singular='', plural='s'):
    return singular if number in (0, 1) else plural

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
