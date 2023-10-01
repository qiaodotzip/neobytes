def calculate_score(option_data, preference_weights):
    score = 0
    for key, weight in preference_weights.items():
        score += option_data.get(key, 0) * weight
    return score

def calc_preference(preference, option_category):
    # These weights can be fine-tuned based on business requirements
    preference_weights = {
        'cost-effective': {'cost': -1, 'time': 1, 'eco': 0.5},
        'time-effective': {'cost': 0, 'time': -1, 'eco': 0.5},
        'balanced': {'cost': -0.5, 'time': -0.5, 'eco': 1},
        'eco-friendly': {'cost': 0, 'time': 0.5, 'eco': -1}
    }

    print(f"Preference received: {preference}")
    print(f"Option category received: {option_category}")

    # Rental durations
    rental_duration_options = {
        'short_rental': {'cost': 100, 'time': 1, 'eco': 0},
        'long_rental': {'cost': 200, 'time': 7, 'eco': 0},
        'special_rental': {'cost': 300, 'time': 10, 'eco': 0}
    }

    # Transport options
    transport_options = {
        'local_delivery': {'cost': 100, 'time': 5, 'eco': 3},
        'foreign_delivery': {'cost': 200, 'time': 10, 'eco': 6},
        'fast_delivery': {'cost': 400, 'time': 1, 'eco': 9}
    }

    # Load types
    load_type_options = {
        'MCC': {'cost': 200, 'time': 8, 'eco': 3},
        'FCL': {'cost': 400, 'time': 1, 'eco': 6},
        'LCL': {'cost': 100, 'time': 6, 'eco': 3}
    }

    # Select the correct options based on the category
    options = {
        'rental_duration': rental_duration_options,
        'transport': transport_options,
        'load_type': load_type_options
    }[option_category]

    weights = preference_weights.get(preference)
    if not weights:
        return None

    best_option = max(options.keys(), key=lambda option: calculate_score(options[option], weights))
    return best_option
