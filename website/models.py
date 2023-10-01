from . import db
from flask_login import UserMixin
from sqlalchemy.sql import func
from sqlalchemy import create_engine, Column, Integer, String, Float, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy

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

class Consumer(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))
    location = db.Column(db.String(100)) # Preferred location or port of the consumer.
    selected_provider = db.Column(db.Integer, db.ForeignKey('cargo.id', name='consumer_selected_provider_fk'))
    selected_plan = db.Column(db.Integer, db.ForeignKey('cost_plan.id', name='consumer_selected_plan_fk'))
    current_demand_status = db.Column(db.String(10))

class Cargo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    supplier = db.Column(db.String(50))
    container_type_available = db.Column(db.String(50))
    volume_available = db.Column(db.Float)
    weight_limit = db.Column(db.Float)
    size = db.Column(db.String(50))
    base_price = db.Column(db.Float)
    port_location = db.Column(db.String(100))
    status = db.Column(db.String(50))
    current_demand = db.Column(db.Float)

class Pricing(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    cargo_id = db.Column(db.Integer, db.ForeignKey('cargo.id'))
    market_price = db.Column(db.Float)
    historical_price = db.Column(db.Float)
    seasonal_price = db.Column(db.Float)

class DynamicPricing(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    cargo_id = db.Column(db.Integer, db.ForeignKey('cargo.id'))
    demand_multiplier = db.Column(db.Float, default=1.0)
    supply_multiplier = db.Column(db.Float, default=1.0)
    season_multiplier = db.Column(db.Float, default=1.0)
    last_updated = db.Column(db.DateTime, default=datetime.utcnow)

class CostPlan(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    location = db.Column(db.String(100))
    consumer_id = db.Column(db.Integer, db.ForeignKey('consumer.id', name='cost_plan_consumer_id_fk'))
    container_id = db.Column(db.Integer, db.ForeignKey('cargo.id', name='cost_plan_cargo_id_fk'))
    container_type = db.Column(db.String(50))
    rental_duration = db.Column(db.String(50))
    transport = db.Column(db.String(50))
    load_type = db.Column(db.String(50))
    LCL_Volume = db.Column(db.String(50))

class ServiceOptions(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    service_name = db.Column(db.String(100))
    service_type = db.Column(db.String(50))
    service_price = db.Column(db.Float)
    service_location = db.Column(db.String(100))

class HistoricalPricing(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    cargo_id = db.Column(db.Integer, db.ForeignKey('cargo.id'))
    date = db.Column(db.DateTime, default=datetime.utcnow)
    price = db.Column(db.Float)
    price_type = db.Column(db.String(50))





    




