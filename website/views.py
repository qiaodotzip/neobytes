from flask import Blueprint, render_template, request, flash, jsonify
from flask_login import login_required, current_user
from website import db
import json
from flask import Flask, render_template, json, request, jsonify, redirect, url_for, flash
from .models  import Consumer, Cargo, CostPlan, DynamicPricing, HistoricalPricing
from .plan_algorithm import calc_preference_with_feedback
from .price_algorithm import update_dynamic_pricing
from .profit import calculate_profit_insights

views = Blueprint('views', __name__)

@views.route('/')
def index():
    return render_template('home.html', user=current_user)

@views.route('/about.html')
def about():
    return render_template('about.html', user=current_user)

@views.route('/contact.html')
def contact():
    return render_template('contact.html', user=current_user)

@views.route('/get-a-quote.html')
def quote():
    return render_template('get-a-quote.html', user=current_user)

@views.route('/FreightMarket.html')
@login_required
def price():
    return render_template('FreightMarket.html', user=current_user)

@views.route('/sample-inner-page.html')
def inner():
    return render_template('sample-inner-page.html', user=current_user)

@views.route('/service-details.html')
def serviceDetails():
    return render_template('service-details.html', user=current_user)

@views.route('/services.html')
def services():
    return render_template('services.html', user=current_user)

@views.route('/Private.html')
@login_required
def private():
    return render_template('Private.html', user=current_user)

@views.route("/rentTest.html")
def rentTest():
    return render_template('rentTest.html', user=current_user)

def get_average_historical_price(cargo_id, price_type):
    # Query the HistoricalPricing table for prices
    prices = [price.price for price in HistoricalPricing.query.filter_by(cargo_id=cargo_id, price_type=price_type).all()]
    if not prices:
        return None  # Return None if there are no price records
    # Calculate and round the average
    average_price = sum(prices) / len(prices)
    return round(average_price, 2)

@views.route("/search_containers", methods=['POST'])

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

    return render_template('rentTest.html', cargos=cargos, market_prices=market_prices, average_prices=average_prices, seasonal_prices=seasonal_prices, selected_price_type=selected_price_type, form_data=form_data, user=current_user)

@views.route("/get_recommendations", methods=['GET'])
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

@views.route("/cost_plan", methods=['POST'])
def insert_db():
    # Retrieve data from form
    container_type = request.form.get('container_type')
    rental_duration = request.form.get('rental_duration')
    transport = request.form.get('transport')
    load_type = request.form.get('load_type')

    # Create a new CostPlan instance
    cost_plan = CostPlan(
        container_type=container_type,
        rental_duration=rental_duration,
        transport=transport,
        load_type=load_type
        #Need to add consumer_id and location from Cargo
    )

    # Insert the record into the database
    db.session.add(cost_plan)
    db.session.commit()

    # Redirect to a success page or back to the form, whatever you'd like
    return redirect(url_for('views.insert_plan'))

@views.route("/manage.html", methods=['GET'])
def insert_plan():

    costPlans = CostPlan.query.all()
    
    latest_cost_plan = CostPlan.query.order_by(CostPlan.id.desc()).first()  # Fetch the latest added cost_plan

    # Check if there's a cost_plan available
    if latest_cost_plan:
        container_type = latest_cost_plan.container_type
        rental_duration = latest_cost_plan.rental_duration
        transport = latest_cost_plan.transport
        load_type = latest_cost_plan.load_type
    else:
        container_type = None
        rental_duration = None
        transport = None
        load_type = None

    # Render the template with the fetched data
    return render_template("manage.html", user=current_user, costPlan=costPlans, container_type=container_type,
        rental_duration=rental_duration,
        transport=transport,
        load_type=load_type)

@views.route('/dashboard.html')
def dashboard():
    cost_plans = CostPlan.query.all()
    gain_loss, space_sold = calculate_profit_insights()
    return render_template('dashboard.html', user=current_user, cost_plans=cost_plans, gain_loss=gain_loss, space_sold=space_sold)





