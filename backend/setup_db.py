# setup_db.py
from app import app, db
from models import Cargo

with app.app_context():
    db.drop_all()
    db.create_all()  
    
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
    ]

    for c_data in cargo_data:
        cargo = Cargo(**c_data)
        db.session.add(cargo)
        db.session.commit()

print("Database initialized with sample data.")