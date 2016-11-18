from sqlalchemy import sql, orm
from app import db

class AnonymousSource(db.Model):
    __tablename__ = 'anonymoussource'
    quote = db.Column('SOURCE', db.String(20))
    link = db.Column('LINK', db.String(20), primary_key=True)

class Date(db.Model):
    __tablename__ = 'date'
    date = db.Column('SOURCE', db.String(20))
    year = db.Column('YEAR', db.String(20))
    link = db.Column('LINK', db.String(20), primary_key=True)

class Properties(db.Model):
    __tablename__ = 'properties'
    Link = db.Column('LINK', db.String(20), primary_key=True)
    Section = db.Column('SECTION', db.String(20))


#Year ==> Section ==> (phrase, count, url)