from flask import Blueprint, render_template, request, flash, redirect, url_for
from .models import User
from werkzeug.security import generate_password_hash, check_password_hash
from . import db   ##means from __init__.py import db
from flask_login import login_user, login_required, logout_user, current_user

auth = Blueprint('auth', __name__)

@auth.route('/login.html', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        user = User.query.filter_by(username=username).first()
        if user:
            if check_password_hash(user.password, password):
                flash('Logged in successfully!', category='success')
                login_user(user, remember=True)
                return redirect(url_for('views.index'))
            else:
                flash('Incorrect password, try again.', category='error')
        else:
            flash('Username does not exist.', category='error')

    return render_template("login.html", user=current_user)


@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('views.index'))


@auth.route('/sign_up.html', methods=['GET', 'POST'])
def sign_up():
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        role = request.form.get('role')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')

        user = User.query.filter_by(email=email).first()
        if user:
            flash('Email already exists.', category='error')
        elif len(email) < 4:
            flash('Email must be greater than 3 characters.', category='error')
        elif len(username) < 2:
            flash('Username must be greater than 1 character.', category='error')
        elif password1 != password2:
            flash("Passwords don't match.", category='error')
        elif len(password1) < 7:
            flash('Password must be at least 7 characters.', category='error')
        else:
            new_user = User(username=username, email=email,role=role, password=generate_password_hash(
                password1, method='sha256'))
            dummy123 = User(username="dummy123" , email="dummy123@gmail.com" , role="User", password=generate_password_hash(
                "dummy123", method='sha256'))
            dummyPort = User(username="dummyPort" , email="dummyPort@gmail.com" ,role="Port_Staff", password=generate_password_hash(
                "dummyPort", method='sha256'))
            dummySupplier =  User(username="dummySupplier", email="dummySupplier@gmail.com",role="Supplier", password=generate_password_hash(
                "dummySupplier", method='sha256'))
            
           

            db.session.add(new_user,dummy123,dummyPort,dummySupplier)
            db.session.commit()
            # Log in the desired dummy user (e.g., dummy123)
            user_to_login = dummy123  # Change this to the desired user
            login_user(user_to_login, remember=True)
            
            flash('Account created!', category='success')
            return redirect(url_for('views.index'))

    return render_template("sign_up.html", user=current_user)
