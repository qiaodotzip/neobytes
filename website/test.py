from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from .models import User


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///Neobytes.db'
db = SQLAlchemy(app)

@app.route('/display_data')
def display_data():
    data = User.query.all()  # Replace YourModel with your actual model class
    return render_template('login.html', data=data)