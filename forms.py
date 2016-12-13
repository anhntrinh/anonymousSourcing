from flask_wtf import FlaskForm
from wtforms import StringField, BooleanField, IntegerField, SelectMultipleField, SelectField, DateField
from wtforms.validators import DataRequired

import datetime

class AnonymousFilterForm(FlaskForm):
    beginDate = DateField('Start Date', format='%m/%d/%Y', default=datetime.date(2000,1,1))
    endDate = DateField('End Date', format='%m/%d/%Y',default = datetime.date.today())
    sectionMenu = SelectMultipleField('sectionMenu',choices=[],coerce = int)
    
    def __init__(self,sectionQuery):
        super(AnonymousFilterForm, self).__init__()
        self.sectionMenu.choices = sectionQuery
    
