from flask_wtf import FlaskForm
from wtforms import StringField, BooleanField, IntegerField
from wtforms.validators import DataRequired

class AnonymousFilterForm(FlaskForm):
    beginDate = IntegerField('beginDate',[DataRequired()])
    endDate =  IntegerField('endDate',[DataRequired()])
