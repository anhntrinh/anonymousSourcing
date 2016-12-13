from flask_wtf import FlaskForm
from wtforms import IntegerField, SelectMultipleField, SelectField, DateField
from wtforms.validators import DataRequired
from datetime import datetime,date



class AnonymousFilterForm(FlaskForm):
    '''
    beginDay = IntegerField('beginDay',[DataRequired()],default = 1)
    endDay =  IntegerField('endDay',[DataRequired()],default = 28)
    beginMonth = IntegerField('beginMonth',[DataRequired()],default = 1)
    endMonth =  IntegerField('endMonth',[DataRequired()],default = 12)
    beginYear = IntegerField('beginYear',[DataRequired()],default = 2000)
    endYear =  IntegerField('endYear',[DataRequired()],default = 2016)
    '''

    beginDate = DateField('beginDate', format='%Y-%m-%d', default=date(2000,01,01))
    endDate = DateField('endDate', format='%Y-%m-%d',default = date(2016,10,10))
    sectionMenu = SelectMultipleField('sectionMenu',choices=[],coerce = int)
    scale = SelectField('scale',choices=[(1,'Month'), (2,'Year')],coerce = int,default = [1])

    
    def __init__(self,sectionQuery):
        super(AnonymousFilterForm, self).__init__()
        self.sectionMenu.choices = sectionQuery
    
