from flask_wtf import FlaskForm
from wtforms import IntegerField, SelectMultipleField, SelectField, DateField
from wtforms.validators import DataRequired, optional
from datetime import datetime,date

class AnonymousFilterForm(FlaskForm):

    beginDate  = DateField('beginDate', format = '%m/%d/%Y', default = date(2000,01,01))
    endDate = DateField('endDate', format='%m/%d/%Y',default = date(2016,10,10))
    sectionMenu = SelectMultipleField('sectionMenu',choices=[],coerce = int)
    scale = SelectField('scale',[optional()],choices=[(1,'Month'), (2,'Year')],coerce = int,default = [1])

    
    def __init__(self,sectionQuery):
        super(AnonymousFilterForm, self).__init__()
        self.sectionMenu.choices = sectionQuery
    
