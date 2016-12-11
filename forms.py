from flask_wtf import FlaskForm
from wtforms import StringField, BooleanField, IntegerField
from wtforms.validators import DataRequired

class AnonymousFilterForm(FlaskForm):
    beginDay = IntegerField('beginDay',[DataRequired()],default = 1)
    endDay =  IntegerField('endDay',[DataRequired()],default = 28)
    beginMonth = IntegerField('beginMonth',[DataRequired()],default = 1)
    endMonth =  IntegerField('endMonth',[DataRequired()],default = 12)
    beginYear = IntegerField('beginYear',[DataRequired()],default = 2000)
    endYear =  IntegerField('endYear',[DataRequired()],default = 2016)
