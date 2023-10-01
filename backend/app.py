from flask import Flask, render_template, json, request, jsonify, redirect, url_for, flash
from models import Consumer, Cargo, CostPlan, DynamicPricing, HistoricalPricing
from plan_algorithm import calc_preference_with_feedback
from price_algorithm import update_dynamic_pricing
from settings import SQLALCHEMY_DATABASE_URI
from database import db
import secrets

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = SQLALCHEMY_DATABASE_URI
secret_key = secrets.token_hex(16)
app.config['SECRET_KEY'] = secret_key
db.init_app(app)

@app.route("/")
def main():
    return render_template('index.html')

def get_average_historical_price(cargo_id, price_type):
    # Query the HistoricalPricing table for prices
    prices = [price.price for price in HistoricalPricing.query.filter_by(cargo_id=cargo_id, price_type=price_type).all()]
    if not prices:
        return None  # Return None if there are no price records
    # Calculate and round the average
    average_price = sum(prices) / len(prices)
    return round(average_price, 2)

@app.route("/search_containers", methods=['POST'])

def search_containers():
    volume = request.form['volume']
    location = request.form['location']
    pricing_pref = request.form['pricing']
    selected_price_type = request.form.get('selected_price_type', 'market_price')

    form_data = {
    'volume': volume,
    'location': location,
    'pricing': pricing_pref
    }

    # Update dynamic pricing before searching
    update_dynamic_pricing()

    # Get all cargos at the location
    query = Cargo.query

    # Apply filters if they exist
    if location:
        query = query.filter_by(port_location=location)
    if volume:
        query = query.filter(Cargo.volume_available >= float(volume))
    
    cargos = query.all()
    
    def calculate_price_for_cargo(cargo):
        dynamic_pricing = DynamicPricing.query.filter_by(cargo_id=cargo.id).first()
        return cargo.base_price * dynamic_pricing.demand_multiplier * dynamic_pricing.supply_multiplier * dynamic_pricing.season_multiplier

    if pricing_pref == 'lowest':
        cargos.sort(key=calculate_price_for_cargo)
    elif pricing_pref == 'highest':
        cargos.sort(key=calculate_price_for_cargo, reverse=True)


    market_prices = {cargo.id: cargo.base_price * DynamicPricing.query.filter_by(cargo_id=cargo.id).first().demand_multiplier * DynamicPricing.query.filter_by(cargo_id=cargo.id).first().supply_multiplier * DynamicPricing.query.filter_by(cargo_id=cargo.id).first().season_multiplier for cargo in cargos}

    average_prices = {cargo.id: get_average_historical_price(cargo.id, 'market_price') for cargo in cargos}
    seasonal_prices = {cargo.id: cargo.base_price * DynamicPricing.query.filter_by(cargo_id=cargo.id).first().season_multiplier for cargo in cargos}

    return render_template('index.html', cargos=cargos, market_prices=market_prices, average_prices=average_prices, seasonal_prices=seasonal_prices, selected_price_type=selected_price_type, form_data=form_data)

@app.route("/get_recommendations", methods=['GET'])
def get_recommendations():
    plan_preference = request.args.get('planPreference')
    
    best_rental_duration = calc_preference_with_feedback(plan_preference, 'rental_duration')
    best_transport = calc_preference_with_feedback(plan_preference, 'transport')
    best_load_type = calc_preference_with_feedback(plan_preference, 'load_type')

    calculated_values = {
        'rental_duration': best_rental_duration,
        'transport': best_transport,
        'load_type': best_load_type
    }

    return jsonify(calculated_values)

@app.route("/cost_plan", methods=['POST'])
def insert_plan():
    # Retrieve data from form
    container_type = request.form.get('container_type')
    rental_duration = request.form.get('rental_duration')
    transport = request.form.get('transport')
    load_type = request.form.get('load_type')

    # Create a new CostPlan instance
    cost_plan = CostPlan(
        container_type=container_type,
        rental_duration=rental_duration,
        transport_fee=transport,
        kd_cfs_service_fee=load_type
        #Need to add consumer_id and location from Cargo
    )

    # Insert the record into the database
    db.session.add(cost_plan)
    db.session.commit()

    # Redirect to a success page or back to the form, whatever you'd like
    return redirect(url_for('success_page'))

if __name__ == "__main__":
    app.run(debug=True)
    



