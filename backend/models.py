from flask_sqlalchemy import SQLAlchemy
from database import db
from datetime import datetime

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
    rental_duration = db.Column(db.Float)
    transport_fee = db.Column(db.Float)
    kd_cfs_service_fee = db.Column(db.Float)
    LCL_Volume = db.Column(db.Float)

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





    

