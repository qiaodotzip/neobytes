import requests

def classify_with_ml(numbers):
    key = "e42d7510-6018-11ee-a374-61128d8524ceed27e0c8-9ecf-4bdf-ac27-6c3b506d01b1"
    url = "https://machinelearningforkids.co.uk/api/scratch/"+ key + "/classify"

    response = requests.post(url, json={ "data" : numbers })

    if response.ok:
        responseData = response.json()
        topMatch = responseData[0]
        return topMatch
    else:
        print(f"Error from ML API: {response.text}")  # Log the error
        return None
    
preference_weights = {
    'cost-effective': {'cost': -1, 'time': 1, 'eco': 0.5},
    'time-effective': {'cost': 0, 'time': -1, 'eco': 0.5},
    'balanced': {'cost': -0.5, 'time': -0.5, 'eco': 1},
    'eco-friendly': {'cost': 0, 'time': 0.5, 'eco': -1}
}

# Rental durations
rental_duration_options = {
    'short_rental': {'cost': 100, 'time': 1, 'eco': 0},
    'long_rental': {'cost': 200, 'time': 7, 'eco': 0},
    'special_rental': {'cost': 300, 'time': 5, 'eco': 0}
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

def calculate_score(option_data, preference_weights):
    score = 0
    for key, weight in preference_weights.items():
        score += option_data.get(key, 0) * weight
    return score

def get_best_option_based_on_weights(preference, option_category, preference_weights):
    # This function is a part of your previous calc_preference function
    print(f"Preference received: {preference}")
    print(f"Option category received: {option_category}")
    # These weights can be fine-tuned based on business requirements

    # Select the correct options based on the category
    options = {
        'rental_duration': rental_duration_options,
        'transport': transport_options,
        'load_type': load_type_options
    }[option_category]

    best_option = max(options.keys(), key=lambda option: calculate_score(options[option], preference_weights))
    return best_option

def adjust_weights(preference_weights, ai_recommendation):
    if ai_recommendation == 'cost-effective':
        preference_weights['cost'] -= 0.1  # Emphasize cost-effectiveness
        preference_weights['time'] += 0.1  # De-emphasize time-effectiveness
        preference_weights['eco'] += 0.1   # De-emphasize eco-friendliness

    elif ai_recommendation == 'time-effective':
        preference_weights['cost'] += 0.1  # De-emphasize cost-effectiveness
        preference_weights['time'] -= 0.1  # Emphasize time-effectiveness
        preference_weights['eco'] += 0.1   # De-emphasize eco-friendliness

    elif ai_recommendation == 'eco-friendly':
        preference_weights['cost'] += 0.1  # De-emphasize cost-effectiveness
        preference_weights['time'] += 0.1  # De-emphasize time-effectiveness
        preference_weights['eco'] -= 0.1   # Emphasize eco-friendliness
    
    return preference_weights

def calc_preference_with_feedback(preference, option_category):
    max_attempts = 3
    attempts = 0
    
    preference_weights = {
        'cost-effective': {'cost': -1, 'time': 1, 'eco': 0.5},
        'time-effective': {'cost': 0, 'time': -1, 'eco': 0.5},
        'balanced': {'cost': -0.5, 'time': -0.5, 'eco': 1},
        'eco-friendly': {'cost': 0, 'time': 0.5, 'eco': -1}
        }
    weights = preference_weights.get(preference)
    
    while attempts < max_attempts:
        best_option_key = get_best_option_based_on_weights(preference, option_category, weights)
        
        # Use the existing dictionaries to fetch the values for the best option
        if option_category == 'rental_duration':
            best_option_values = rental_duration_options[best_option_key]
        elif option_category == 'transport':
            best_option_values = transport_options[best_option_key]
        else:  # option_category == 'load_type'
            best_option_values = load_type_options[best_option_key]
        
        numbers_for_ml = [best_option_values['cost'], best_option_values['time'], best_option_values['eco']]
        recommendation_from_ml = classify_with_ml(numbers_for_ml)
        
        if recommendation_from_ml['class_name'] == preference:
            return best_option_key
        else:
            # Adjust the weights based on AI feedback
            weights = adjust_weights(weights, recommendation_from_ml['class_name'])
            attempts += 1

    # After max_attempts, if no alignment found, return the most recent best_option
    return best_option_key


