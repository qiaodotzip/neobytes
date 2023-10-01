from . import db
from flask_login import UserMixin
from sqlalchemy.sql import func
from sqlalchemy import create_engine, Column, Integer, String, Float, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime

class Container_Rental(db.Model):
    oid = db.Column(db.Integer, primary_key=True)
    cid = db.Column(db.Integer, db.ForeignKey("container.cid"))
    sid = db.Column(db.Integer, db.ForeignKey("user.id"))
    rentalDuration = db.Column(db.Integer)
    pricePaid = db.Column(db.Float(20,2))

class Container(db.Model):
    cid = db.Column(db.Integer, primary_key=True)
    uid = db.Column(db.Integer, db.ForeignKey("user.id"))
    type = db.Column(db.String(60))
    cost = db.Column(db.Float(20,2))
    available = db.Column(db.Integer)
    unavailable = db.Column(db.Integer, default=0)
    # Available is the number of containers available for rental
    # Unavailable is the number of containers currently rented out
    # When a container is rented out, available - 1, unavailable +1

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(60), unique=True)
    password = db.Column(db.String(30))
    email = db.Column (db.String(60), unique=True)
    role = db.Column(db.String(30), )

    # if role == "Supplier":
    #     containers = db.relationship('Container')
    # elif role == "Renter":
    #     containers = db.relationship('Container_Rental')

# sid = supplier ID (same as user id but points specifically on container suppliers)
# oid = order ID
# cid = container ID
# uid = user ID


class Object(db.Model, BaseException):
    __tablename__ = 'data_objects'

    id = db.Column(db.Integer, primary_key=True)
    uid = db.Column(db.Integer, db.ForeignKey("user.id"))
    cid = db.Column(db.Integer)
    

    date = db.Column(db.DateTime, default=datetime.utcnow)
    time = db.Column(db.String)
    destination = db.Column(db.String)
    volume = db.Column(db.Float)
    weight = db.Column(db.Float)
    status = db.Column(db.String)


