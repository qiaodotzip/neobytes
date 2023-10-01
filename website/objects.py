from .models import Object
from flask import render_template, Blueprint, request, flash, redirect, url_for
from . import db
from flask_login import login_required, current_user

objects = Blueprint('objects', __name__)

@objects.route('/rent.html')
def rent():
    data1 = Object(cid=1000 , uid=1 ,time="08:00", destination="Singapore", volume=100, weight=500.0)
    data2 = Object(cid=2000 , uid=1 , time="9:00", destination="Australia", volume=75, weight=300.0)
    data3 = Object(cid=3000 , uid=2 , time="10:00", destination="America", volume=85, weight=200.0)
    data4 = Object(cid=4000 , uid=3 , time="11:00", destination="Thailand", volume=90, weight=100.0)
    data5 = Object(cid=5000 , uid=4 , time="12:00", destination="Vietnam", volume=70, weight=400.0)
    data6 = Object(cid=6000 , uid=5 , time="01:00", destination="Korea", volume=110, weight=250.0)

    data = [data1, data2, data3, data4, data5, data6]

    db.session.add_all(data)
    db.session.commit()
    return render_template('rent.html', data=data, user=current_user)

@objects.route('/manage.html')
@login_required
def manage():
    rent_button_pressed = request.args.get('rent_button')
    
    if rent_button_pressed == '1':
        flash('Successfully rented!', 'success')  # use flash to display a message
        return redirect(url_for('objects.manage'))  # Redirect back to the manage page
    
    
    return render_template('manage.html', user=current_user, rent_button_pressed=rent_button_pressed)