from . import db 
#since we are under the websites directory
#we can use from .
#if we are outside, we write it as from website import db instead.
#db is from thevariable created inside __init__.py  jn
from flask_login import UserMixin
#a module that helps us log users in
from sqlalchemy.sql import func

#when storing objects,define name+inherit
#db.Model islike a bluepint or guidelines
#all users need to look like this(the columns)

class Note(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    data = db.Column(db.String(10000))
    date=db.Column(db.DateTime(timezone=True), default=func.now())
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))


    
class User(db.Model,UserMixin):
    id = db.Column(db.Integer,primary_key=True)
    email=db.Column(db.String(150), unique=True)
    password=db.Column(db.String(150))
    first_name=db.Column(db.String(150))
    notes = db.relationship('Note')