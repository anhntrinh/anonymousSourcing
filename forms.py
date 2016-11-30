from flask_wtf import FlaskForm
from wtforms import StringField, BooleanField, IntegerField
from wtforms.validators import DataRequired

class DrinkerEditFormFactory:
    @staticmethod
    def form(Agencies, Sections):
        class F(FlaskForm):
            @staticmethod
            def agency_field_name(index):
                return 'agency_{}'.format(index)
            def agency_fields(self):
                for i, agency in enumerate(Agencies):
                    yield agency, getattr(self, F.agency_field_name(i))
            def get_agencies_liked(self):
                for agency, field in self.organization_fields():
                    if field.data:
                        yield agency

        return F()
