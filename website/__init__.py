from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from os import path
from flask_login import LoginManager
import secrets


db = SQLAlchemy()
DB_NAME = "Neobytes.db"

def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'
    secret_key = secrets.token_hex(16)
    app.config['SECRET_KEY'] = secret_key
    db.init_app(app)

    from .views import views
    from .auth import auth
    from .objects import objects
    from .models import User

    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')
    app.register_blueprint(objects, url_prefix='/')

    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(id):
        return User.query.get(int(id))

    return app

# Function to create the database schema (tables)
def create_database(app):
    with app.app_context():
        db.drop_all()
        db.create_all()
        print('Created Database!')
        from .models import Cargo

        # Sample Supplier Data
        cargo_data = [
            {
                "supplier": "AlphaCargo",
                "container_type_available": "Standard",
                "volume_available": 8000.0,
                "weight_limit": 500.0,
                "size": "20x20x20",
                "status": "Fully Available",
                "base_price": 80.0,
                "port_location": "Tanjong Pagar",
                "current_demand": 1
            },
            {
                "supplier": "BetaLogistics",
                "container_type_available": "Refrigerated",
                "volume_available": 600.0,
                "weight_limit": 600.0,
                "size": "10x10x10",
                "status": "LCL (Partial)",
                "base_price": 150.0,
                "port_location": "Tanjong Pagar",
                "current_demand": 1
            },
            {
                "supplier": "CargoExpress",
                "container_type_available": "Standard",
                "volume_available": 1200.0,
                "weight_limit": 700.0,
                "size": "20x10x15",
                "status": "LCL (Partial)",
                "base_price": 100.0,
                "port_location": "Brani",
                "current_demand": 1
            },
            {
                "supplier": "GlobalTransit",
                "container_type_available": "Dangerous",
                "volume_available": 3375.0,
                "weight_limit": 550.0,
                "size": "15x15x15",
                "status": "Fully Available",
                "base_price": 120.0,
                "port_location": "Pasir Panjang",
                "current_demand": 1
            },
            {
                "supplier": "ContainerOne",
                "container_type_available": "Standard",
                "volume_available": 2880.0,
                "weight_limit": 950.0,
                "size": "40x8x9",
                "status": "Fully Available",
                "base_price": 130.0,
                "port_location": "Tuas",
                "current_demand": 1
            },
            {
                "supplier": "ContainerOne",
                "container_type_available": "Dangerous",
                "volume_available": 1280.0,
                "weight_limit": 605.0,
                "size": "20x8x8",
                "status": "Fully Available",
                "base_price": 560.0,
                "port_location": "Tuas",
                "current_demand": 1
            },
            {
                "supplier": "Sea Box",
                "container_type_available": "Dangerous",
                "volume_available": 854.0,
                "weight_limit": 356.0,
                "size": "20x8x10",
                "status": "LCL (Partial)",
                "base_price": 268.0,
                "port_location": "Pasir Panjang",
                "current_demand": 1
            },
            {
                "supplier": "Sea Box",
                "container_type_available": "Dangerous",
                "volume_available": 3200.0,
                "weight_limit": 1964.0,
                "size": "40x8x10",
                "status": "Fully Available",
                "base_price": 754.0,
                "port_location": "Brani",
                "current_demand": 1
            },
        ]

        for c_data in cargo_data:
            cargo = Cargo(**c_data)
            db.session.add(cargo)
            db.session.commit()

    print("Database initialized with sample data.")
