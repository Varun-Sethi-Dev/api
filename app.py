from flask import Flask, request, jsonify
from scipy.optimize import least_squares


# Function to calculate distance based on path loss model (replace with your actual implementation)
def calculate_distance(rssi, tx_power, env_factor):
    path_loss = tx_power - rssi
    distance = 10.0 ** ((path_loss - 40.0) / (10.0 * env_factor))
    return distance


# Function to define the trilateration equations (same as before)
def trilateration_equations(coordinates, beacon_locs, distances):
    # ... (function definition remains the same)
    x, y, z = coordinates
    errors = []
    for i in range(len(beacon_locs)):
        beacon_x, beacon_y, beacon_z = beacon_locs[i]
        distance = distances[i]
        error = (x - beacon_x) ** 2 + (y - beacon_y) ** 2 + (z - beacon_z) ** 2 - distance ** 2
        errors.append(error)
    return errors


# Define the Flask app
app = Flask(__name__)

@app.route("/")
def start():
    return "Server is Running"


# API endpoint for trilateration
@app.route('/trilaterate/', methods=['POST'])
def trilaterate():
    # Get request data (beacon locations and estimated distances)

    data = request.get_json()
    beacon_locations = data.get('beacon_locations')
    estimated_distances = data.get('estimated_distances')

    # Check for required data
    # if not all([beacon_locations, estimated_distances]):
        # return jsonify({'error': 'Missing required data'}), 400

    # Perform trilateration calculations (same as before)
    initial_guess = [5.0, 5.0, 5.0]  # Replace with a better guess if available
    solution = least_squares(trilateration_equations, initial_guess, args=(beacon_locations, estimated_distances))
    optimized_x, optimized_y, optimized_z = solution.x

    # Return estimated location as JSON response
    return jsonify({'x': optimized_x, 'y': optimized_y, 'z': optimized_z})


