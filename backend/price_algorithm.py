from models import Consumer, Cargo, DynamicPricing, HistoricalPricing, CostPlan
from datetime import datetime
from database import db
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import func

def compute_demand_multiplier(container_type, location):
    # Count the number of CostPlan entries that have the specified container type and location
    num_plans = CostPlan.query.filter_by(container_type=container_type, location=location).count()
    
    # Determine demand multiplier based on the number of CostPlan entries
    if num_plans > 10:
        return 1.2
    elif num_plans < 5:
        return 0.8
    else:
        return 1.0

def compute_supply_multiplier(container_type, location):
    # Get the total available volume of the specified container type in the location
    total_volume = db.session.query(func.sum(Cargo.volume_available)).filter_by(container_type_available=container_type, port_location=location).scalar()
    
    # Determine supply multiplier based on the total available volume
    if total_volume > 5000:  # Assuming cubic feet or similar unit. Adjust thresholds as needed.
        return 0.8
    elif total_volume < 1000:  # Adjust threshold as per your data.
        return 1.2
    else:
        return 1.0


def compute_season_multiplier():
    current_month = datetime.now().month
    if 6 <= current_month <= 10:  # Southwest Monsoon, Originally 9
        return 0.9
    elif 11 <= current_month or current_month <= 3:  # Northeast Monsoon
        return 1.2
    else:  # Inter-Monsoon
        return 1.0
    
def add_to_historical_pricing(cargo_id, price, price_type):
    last_price_entry = HistoricalPricing.query.filter_by(cargo_id=cargo_id, price_type=price_type).order_by(HistoricalPricing.date.desc()).first()
    if not last_price_entry or round(last_price_entry.price, 2) != round(price, 2):
        historical_price = HistoricalPricing(cargo_id=cargo_id, price=price, price_type=price_type, date=datetime.utcnow())
        db.session.add(historical_price)
        db.session.commit()
    
def update_dynamic_pricing():
    cargos = Cargo.query.all()
    for cargo in cargos:
        base_price = cargo.base_price
        demand_multiplier = compute_demand_multiplier(cargo.container_type_available, cargo.port_location)
        supply_multiplier = compute_supply_multiplier(cargo.container_type_available, cargo.port_location)
        season_multiplier = compute_season_multiplier()

        dynamic_price = DynamicPricing.query.filter_by(cargo_id=cargo.id).first()
        if not dynamic_price:
            dynamic_price = DynamicPricing(cargo_id=cargo.id)

        dynamic_price.demand_multiplier = demand_multiplier
        dynamic_price.supply_multiplier = supply_multiplier
        dynamic_price.season_multiplier = season_multiplier
        dynamic_price.last_updated = datetime.utcnow()

        dynamic_price_value = base_price * demand_multiplier * supply_multiplier * season_multiplier
        add_to_historical_pricing(cargo.id, dynamic_price_value, 'market_price')

        print(f"cargo: {cargo.id}, Base Price: {base_price}, Demand Multiplier: {demand_multiplier}, Supply Multiplier: {supply_multiplier}, Season Multiplier: {season_multiplier}, Dynamic Price: {dynamic_price_value}")

        db.session.add(dynamic_price)
        db.session.commit()

# You can run the function update_dynamic_pricing() at regular intervals or trigger it when certain events occur.
