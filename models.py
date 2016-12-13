from sqlalchemy import sql, orm
from app import db


class BigTable(db.Model):
    __tablename__ = 'anon'
    title = db.Column('title', db.Text) 
    link = db.Column('link', db.Text, primary_key=True)
    agency = db.Column('agency',db.Text)
    day  = db.Column('day', db.Integer)
    month = db.Column('month', db.Integer)
    year = db.Column('year', db.Integer)
    phrase = db.Column('phrase',db.Text)
    section = db.Column('section',db.Text)
    snip = db.Column('snip',db.Text, primary_key=True)
    pdate = db.Column('pdate',db.Date)

    

