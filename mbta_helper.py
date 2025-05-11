"""
MBTA Helper functions for interacting with the Mapbox and MBTA APIs
"""

import json
import os
import urllib.parse
import urllib.request
from datetime import datetime, timedelta

from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# API Keys from environment variables
MAPBOX_TOKEN = os.getenv("MAPBOX_TOKEN")
MBTA_API_KEY = os.getenv("MBTA_API_KEY")

# Base URLs for APIs
MAPBOX_BASE_URL = "https://api.mapbox.com/geocoding/v5/mapbox.places"
MBTA_BASE_URL = "https://api-v3.mbta.com"

# Line colors mapping
LINE_COLORS = {
    "Red": "red",
    "Orange": "orange",
    "Green-B": "green",
    "Green-C": "green",
    "Green-D": "green",
    "Green-E": "green",
    "Blue": "blue",
    "Mattapan": "red",  # Typically considered part of the Red Line
    "SL1": "silver",
    "SL2": "silver",
    "SL3": "silver",
    "SL4": "silver",
    "SL5": "silver",
}


def get_json(url):
    """
    Given a properly formatted URL for a JSON web API request, return
    a Python JSON object containing the response to that request.
    """
    try:
        with urllib.request.urlopen(url) as response:
            response_text = response.read().decode("utf-8")
            return json.loads(response_text)
    except Exception as e:
        print(f"Error fetching data from {url}: {e}")
        return None


def get_lat_lng(place_name):
    """
    Given a place name or address, return a (latitude, longitude) tuple
    with the coordinates of the given place.

    See https://docs.mapbox.com/api/search/geocoding/
    for Mapbox Geocoding API URL formatting requirements.
    """
    # URL encode the place name
    encoded_place = urllib.parse.quote(place_name)
    
    # Construct the URL
    url = f"{MAPBOX_BASE_URL}/{encoded_place}.json?access_token={MAPBOX_TOKEN}&types=poi,address&limit=1&proximity=-71.0589,42.3601"
    
    # Get the JSON response
    response_data = get_json(url)
    
    # Check if we got a valid response with features
    if response_data and 'features' in response_data and len(response_data['features']) > 0:
        # Extract coordinates [longitude, latitude]
        coordinates = response_data['features'][0]['geometry']['coordinates']
        # Return as (latitude, longitude) tuple - note the order swap
        print(f"Mapbox response for {place_name}: {response_data}")
        return (coordinates[1], coordinates[0])
    
    return None


def get_nearest_stations(latitude, longitude, types=None, limit=5):
    """
    Given latitude and longitude strings, return a list of the `limit` closest MBTA stations
    and relevant information.
    
    Parameters:
    - latitude: Latitude of the location
    - longitude: Longitude of the location
    - types: List of MBTA route types to filter by (0=subway, 1=subway, 2=commuter rail, 3=bus, 4=ferry)
    - limit: Maximum number of stations to return
    
    Returns a list of dictionaries containing information about each station
    """
    # Base URL parameters
    params = {
        'api_key': MBTA_API_KEY,
        'sort': 'distance',
        'filter[latitude]': str(latitude),
        'filter[longitude]': str(longitude),
        'include': 'route',
    }
    
    # Add type filter if provided
    if types:
        params['filter[route_type]'] = ','.join(types)
    
    # Build the URL with parameters
    url = f"{MBTA_BASE_URL}/stops?"
    url += urllib.parse.urlencode(params)
    
    # Make the request
    response_data = get_json(url)
    
    if not response_data or 'data' not in response_data:
        return []
    
    # Process each station
    stations = []
    for stop in response_data['data'][:limit]:  # Limit to specified number
        # Get related routes information from included data
        route_ids = []
        if 'relationships' in stop and 'route' in stop['relationships']:
            route_ids = [route_data['id'] for route_data in stop['relationships']['route'].get('data', [])]
        
        # Find route information in included data
        routes = []
        if 'included' in response_data:
            for included in response_data['included']:
                if included['type'] == 'route' and included['id'] in route_ids:
                    route_color = 'bus'  # Default
                    
                    # Determine line color based on route short name or ID
                    route_name = included.get('attributes', {}).get('short_name', '') or included['id']
                    if route_name in LINE_COLORS:
                        route_color = LINE_COLORS[route_name]
                    elif included.get('attributes', {}).get('type') == 2:
                        route_color = 'commuter-rail'
                    
                    routes.append({
                        'id': included['id'],
                        'name': included.get('attributes', {}).get('long_name', '') or route_name,
                        'short_name': route_name,
                        'color': route_color
                    })
        
        # Create station dictionary
        station = {
            'id': stop['id'],
            'name': stop['attributes']['name'],
            'latitude': stop['attributes']['latitude'],
            'longitude': stop['attributes']['longitude'],
            'wheelchair_accessible': stop['attributes']['wheelchair_boarding'] == 1,
            'distance': stop['attributes'].get('distance', None),
            'routes': routes
        }
        
        stations.append(station)
    
    return stations


def find_stop_near(place_name, types=None):
    """
    Given a place name and optional types, return the name of the closest MBTA stop and whether it is wheelchair accessible.
    
    Parameters:
    - place_name: A string place name or address
    - types: Optional list of MBTA route types
    
    Returns:
    - A tuple of (station_name, wheelchair_accessible) or None if no station is found
    """
    # Get coordinates for the place
    coords = get_lat_lng(place_name)
    
    if not coords:
        return None
    
    # Get nearest stations
    stations = get_nearest_stations(coords[0], coords[1], types)
    
    if not stations:
        return None
    
    # Return information about the first (closest) station
    nearest = stations[0]
    return (nearest['name'], nearest['wheelchair_accessible'], nearest['id'], 
            nearest['latitude'], nearest['longitude'], nearest['routes'], coords)


def get_station_arrivals(station_id):
    """
    Get upcoming arrivals for a specific station
    
    Parameters:
    - station_id: MBTA station ID
    
    Returns:
    - Dictionary with arrival predictions
    """
    # Get the current time
    now = datetime.now()
    
    # Set time window - get predictions for the next 1 hour
    min_time = now.isoformat()
    max_time = (now + timedelta(hours=1)).isoformat()
    
    # Build parameters
    params = {
        'api_key': MBTA_API_KEY,
        'filter[stop]': station_id,
        'include': 'trip,route,stop',
        'filter[min_time]': min_time,
        'filter[max_time]': max_time,
        'sort': 'time'
    }
    
    # Build URL
    url = f"{MBTA_BASE_URL}/predictions?"
    url += urllib.parse.urlencode(params)
    
    # Make the request
    response_data = get_json(url)
    
    if not response_data or 'data' not in response_data:
        return {'arrivals': []}
    
    # Process predictions
    arrivals = []
    for prediction in response_data['data']:
        if 'attributes' not in prediction or not prediction['attributes'].get('arrival_time'):
            continue
            
        # Get route information
        route_id = None
        if 'relationships' in prediction and 'route' in prediction['relationships']:
            route_data = prediction['relationships']['route'].get('data')
            if route_data:
                route_id = route_data.get('id')
        
        # Find route information in included data
        route_name = "Unknown"
        route_color = "bus"
        if 'included' in response_data:
            for included in response_data['included']:
                if included['type'] == 'route' and included['id'] == route_id:
                    route_name = included.get('attributes', {}).get('short_name', '') or included['id']
                    
                    # Determine line color
                    if route_name in LINE_COLORS:
                        route_color = LINE_COLORS[route_name]
                    elif included.get('attributes', {}).get('type') == 2:
                        route_color = 'commuter-rail'
        
        # Get destination information
        destination = "Unknown"
        if 'relationships' in prediction and 'trip' in prediction['relationships']:
            trip_id = prediction['relationships']['trip'].get('data', {}).get('id')
            if trip_id and 'included' in response_data:
                for included in response_data['included']:
                    if included['type'] == 'trip' and included['id'] == trip_id:
                        destination = included.get('attributes', {}).get('headsign', 'Unknown')
        
        # Create arrival dictionary
        arrival = {
            'arrival_time': prediction['attributes']['arrival_time'],
            'line': route_name,
            'line_color': route_color,
            'destination': destination,
            'status': prediction['attributes'].get('status', ''),
        }
        
        arrivals.append(arrival)
    
    return {'arrivals': arrivals}