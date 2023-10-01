from flask import Blueprint, render_template, request, flash, jsonify
from flask_login import login_required, current_user
from . import db
import json

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



