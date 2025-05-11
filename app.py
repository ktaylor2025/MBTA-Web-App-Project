"""
MBTA Finder - Flask Web Application
"""

import os
from flask import Flask, render_template, request, jsonify, session
from dotenv import load_dotenv

# Import our MBTA helper functions
import mbta_helper as mbta_helper

# Load environment variables from .env file
load_dotenv()

app = Flask(__name__)

# Configure a secret key for the session
app.secret_key = os.getenv("FLASK_SECRET_KEY", os.urandom(24))

# Get API tokens
MAPBOX_TOKEN = os.getenv("MAPBOX_TOKEN")


@app.route('/')
def index():
    """
    Render the home page with the search form
    """
    return render_template('index.html')


@app.route('/nearest_mbta', methods=['POST'])
def nearest_mbta():
    """
    Handle the form submission and find the nearest MBTA station
    """
    # Get the place name from the form
    place_name = request.form.get('place_name', '')
    
    if not place_name:
        return render_template('error.html', error_message="Please enter a place name or address")
    
    # Get the selected transportation types
    types = request.form.getlist('type[]')
    
    # Find the nearest MBTA station
    result = mbta_helper.find_stop_near(place_name, types)
    
    if not result:
        return render_template('error.html', 
                              error_message=f"Could not find a nearby MBTA station for '{place_name}'. "
                                            f"Please try a different location in the Boston area.")
    
    # Unpack the results
    station_name, wheelchair_accessible, station_id, station_lat, station_lng, station_lines, user_coords = result
    
    # Save to session for potential use in other routes
    session['station_info'] = {
        'id': station_id,
        'name': station_name,
        'lat': station_lat,
        'lng': station_lng
    }
    
    # Render the results template
    return render_template('mbta_station.html',
                          place_name=place_name,
                          station_name=station_name,
                          wheelchair_accessible=wheelchair_accessible,
                          station_id=station_id,
                          station_lat=station_lat,
                          station_lng=station_lng,
                          user_lat=user_coords[0],
                          user_lng=user_coords[1],
                          station_lines=station_lines,
                          mapbox_token=MAPBOX_TOKEN)


@app.route('/api/arrivals/<station_id>')
def get_arrivals(station_id):
    """
    API endpoint to get real-time arrivals for a station
    """
    # Get arrivals data
    arrivals_data = mbta_helper.get_station_arrivals(station_id)
    
    # Return as JSON
    return jsonify(arrivals_data)


@app.errorhandler(404)
def page_not_found(e):
    """
    Handle 404 errors
    """
    return render_template('error.html', error_message="Page not found"), 404


@app.errorhandler(500)
def server_error(e):
    """
    Handle 500 errors
    """
    return render_template('error.html', error_message="Internal server error"), 500


if __name__ == '__main__':
    # Run the app in debug mode
    app.run(debug=True)