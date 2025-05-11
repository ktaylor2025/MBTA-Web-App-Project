"""
MBTA Finder - Flask Web Application
"""
import os
from flask import Flask, render_template, request, redirect, url_for, session, jsonify
from datetime import datetime
import requests
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Flask app setup
app = Flask(__name__)
app.secret_key = os.getenv("FLASK_SECRET_KEY", os.urandom(24))

# API keys from .env
MAPBOX_ACCESS_TOKEN = os.getenv("MAPBOX_ACCESS_TOKEN")
MBTA_API_KEY = os.getenv("MBTA_API_KEY")

# Constants
MAX_RECENT_SEARCHES = 5

# --- MBTA Station Finder Class ---
class MBTAStationFinder:
    """
    Manages interactions with Mapbox and MBTA APIs to find station information.
    
    This class encapsulates the logic for geocoding locations, finding nearby 
    stations, calculating distances, and retrieving route information.
    """
    
    def __init__(self, mapbox_token: str, mbta_key: str = None):
        """
        Initialize an MBTAStationFinder instance with API credentials.
        
        Args:
            mapbox_token: Authentication token for Mapbox API
            mbta_key: Optional authentication key for MBTA API
        """
        self.mapbox_token = mapbox_token
        self.mbta_key = mbta_key

    def geocode_location(self, location_query: str) -> dict:
        """
        Convert a location string to geographic coordinates using Mapbox.
        
        Args:
            location_query: A string containing an address, landmark, or place name
            
        Returns:
            dict: A dictionary containing longitude, latitude, and formatted address
                 or None if the location could not be geocoded
        """
        url = f"https://api.mapbox.com/geocoding/v5/mapbox.places/{location_query}.json"
        params = {"access_token": self.mapbox_token, "limit": 1, "country": "US"}
        try:
            response = requests.get(url, params=params)
            response.raise_for_status()
            data = response.json()
            if data["features"]:
                feature = data["features"][0]
                coords = feature["geometry"]["coordinates"]
                return {
                    "longitude": coords[0],
                    "latitude": coords[1],
                    "address": feature["place_name"]
                }
            return None
        except Exception as e:
            print(f"Geocoding error: {e}")
            return None

    def find_nearest_station(self, latitude: float, longitude: float) -> dict:
        """
        Find the nearest MBTA station to the given coordinates.
        
        Args:
            latitude: The latitude coordinate
            longitude: The longitude coordinate
            
        Returns:
            dict: Information about the nearest station including name, coordinates, and routes
                 None if no station could be found
        """
        url = "https://api-v3.mbta.com/stops"
        params = {
            "filter[route_type]": "0,1",
            "sort": "distance",
            "filter[latitude]": latitude,
            "filter[longitude]": longitude
        }
        if self.mbta_key:
            params["api_key"] = self.mbta_key
        try:
            response = requests.get(url, params=params)
            response.raise_for_status()
            data = response.json()
            if data["data"]:
                station = data["data"][0]
                return {
                    "name": station["attributes"]["name"],
                    "latitude": station["attributes"]["latitude"],
                    "longitude": station["attributes"]["longitude"],
                    "description": station["attributes"].get("description", ""),
                    "routes": self._get_station_routes(station["id"]),
                    "id": station["id"]
                }
            return None
        except Exception as e:
            print(f"MBTA API error: {e}")
            return None

    def _get_station_routes(self, station_id: str) -> list:
        """
        Get routes that serve a particular station.
        
        Args:
            station_id: The MBTA station ID
            
        Returns:
            list: Routes serving this station, with ID, name, and color
        """
        url = "https://api-v3.mbta.com/routes"
        params = {"filter[stop]": station_id}
        if self.mbta_key:
            params["api_key"] = self.mbta_key
        try:
            response = requests.get(url, params=params)
            response.raise_for_status()
            data = response.json()
            return [{
                "id": r["id"],
                "name": r["attributes"]["long_name"],
                "color": r["attributes"]["color"]
            } for r in data["data"]]
        except Exception as e:
            print(f"Error getting routes: {e}")
            return []
    
    def get_arrival_predictions(self, station_id: str, limit: int = 5) -> list:
        """
        Get real-time arrival predictions for a specific station.
        
        Args:
            station_id: The MBTA station ID
            limit: Maximum number of predictions to return
            
        Returns:
            list: Upcoming arrivals with time, destination, and status
        """
        url = "https://api-v3.mbta.com/predictions"
        params = {
            "filter[stop]": station_id,
            "sort": "arrival_time",
            "include": "route",
            "page[limit]": limit
        }
        
        if self.mbta_key:
            params["api_key"] = self.mbta_key
            
        try:
            response = requests.get(url, params=params)
            response.raise_for_status()
            data = response.json()
            
            predictions = []
            for prediction in data.get("data", []):
                # Extract prediction details
                arrival_time = prediction.get("attributes", {}).get("arrival_time")
                route_id = prediction.get("relationships", {}).get("route", {}).get("data", {}).get("id")
                
                # Find route info in included data
                route_name = "Unknown"
                route_color = "gray"
                for included in data.get("included", []):
                    if included.get("type") == "route" and included.get("id") == route_id:
                        route_name = included.get("attributes", {}).get("long_name", "Unknown")
                        route_color = included.get("attributes", {}).get("color", "gray")
                        break
                
                # Format arrival time
                arrival_display = "Scheduled"
                if arrival_time:
                    try:
                        arrival_dt = datetime.fromisoformat(arrival_time.replace("Z", "+00:00"))
                        # Convert to local timezone and format
                        arrival_local = arrival_dt.astimezone()
                        arrival_display = arrival_local.strftime("%I:%M %p")
                    except Exception as e:
                        print(f"Error parsing time: {e}")
                
                predictions.append({
                    "route_name": route_name,
                    "route_color": route_color,
                    "arrival_time": arrival_display
                })
            
            return predictions
        
        except Exception as e:
            print(f"Error getting predictions: {e}")
            return []
    
    def calculate_distance(self, lat1: float, lon1: float, lat2: float, lon2: float) -> float:
        """
        Calculate distance between two points in miles using Haversine formula.
        
        Args:
            lat1: Latitude of first point
            lon1: Longitude of first point
            lat2: Latitude of second point
            lon2: Longitude of second point
            
        Returns:
            float: Distance in miles, rounded to 2 decimal places
        """
        from math import radians, sin, cos, sqrt, atan2
        R = 3958.8  # miles
        lat1, lon1 = radians(lat1), radians(lon1)
        lat2, lon2 = radians(lat2), radians(lon2)
        dlon = lon2 - lon1
        dlat = lat2 - lat1
        a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
        c = 2 * atan2(sqrt(a), sqrt(1-a))
        return round(R * c, 2)

# --- Search History Manager Class ---
class SearchHistoryManager:
    """
    Manages user search history and favorites using Flask session storage.
    
    This class provides methods for adding, retrieving, and removing
    user data without requiring a database.
    """
    
    @staticmethod
    def add_to_recent_searches(session: dict, search_data: dict) -> None:
        """
        Add a search to recent searches in the session.
        
        Args:
            session: The Flask session object
            search_data: Data about the search to save
        """
        if 'recent_searches' not in session:
            session['recent_searches'] = []
        search_entry = {
            "query": search_data["query"],
            "address": search_data["address"],
            "station": search_data["station"]["name"],
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "user_lat": search_data["latitude"],
            "user_lng": search_data["longitude"],
            "station_lat": search_data["station"]["latitude"],
            "station_lng": search_data["station"]["longitude"],
            "distance": search_data["distance"]
        }
        existing = [s for s in session['recent_searches'] if s["address"] == search_entry["address"]]
        if existing:
            session['recent_searches'].remove(existing[0])
        session['recent_searches'].insert(0, search_entry)
        if len(session['recent_searches']) > MAX_RECENT_SEARCHES:
            session['recent_searches'] = session['recent_searches'][:MAX_RECENT_SEARCHES]
        session.modified = True

    @staticmethod
    def get_recent_searches(session: dict) -> list:
        """
        Get recent searches from the session.
        
        Args:
            session: The Flask session object
            
        Returns:
            list: Recent searches stored in the session
        """
        return session.get('recent_searches', [])

    @staticmethod
    def add_to_favorites(session: dict, search_data: dict) -> bool:
        """
        Add a location to favorites.
        
        Args:
            session: The Flask session object
            search_data: Data about the location to favorite
            
        Returns:
            bool: True if added successfully, False if already exists
        """
        if 'favorites' not in session:
            session['favorites'] = []
        favorite = {
            "address": search_data["address"],
            "latitude": search_data["latitude"],
            "longitude": search_data["longitude"],
            "station_name": search_data["station"]["name"],
            "added_on": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
        if not any(f["address"] == favorite["address"] for f in session['favorites']):
            session['favorites'].append(favorite)
            session.modified = True
            return True
        return False

    @staticmethod
    def remove_from_favorites(session: dict, address: str) -> bool:
        """
        Remove a location from favorites.
        
        Args:
            session: The Flask session object
            address: Address of the location to remove
            
        Returns:
            bool: True if removed successfully, False otherwise
        """
        if 'favorites' in session:
            session['favorites'] = [f for f in session['favorites'] if f["address"] != address]
            session.modified = True
            return True
        return False

    @staticmethod
    def get_favorites(session: dict) -> list:
        """
        Get favorites from the session.
        
        Args:
            session: The Flask session object
            
        Returns:
            list: Favorite locations stored in the session
        """
        return session.get('favorites', [])

# --- Route Definitions ---
station_finder = MBTAStationFinder(MAPBOX_ACCESS_TOKEN, MBTA_API_KEY)
history_manager = SearchHistoryManager()

@app.route('/')
def index():
    """
    Render the home page with the search form.
    """
    return render_template('index.html',
                           mapbox_token=MAPBOX_ACCESS_TOKEN,
                           recent_searches=history_manager.get_recent_searches(session),
                           favorites=history_manager.get_favorites(session))

@app.route('/find_station', methods=['POST'])
def find_station():
    """
    Handle the form submission to find the nearest station.
    """
    location_query = request.form.get('location', '')
    if not location_query:
        return render_template('index.html', error="Please enter a location")

    location_data = station_finder.geocode_location(location_query)
    if not location_data:
        return render_template('index.html', error="Could not find that location")

    nearest_station = station_finder.find_nearest_station(location_data["latitude"], location_data["longitude"])
    if not nearest_station:
        return render_template('index.html', error="No MBTA stations found near that location")

    distance = station_finder.calculate_distance(
        location_data["latitude"], location_data["longitude"],
        nearest_station["latitude"], nearest_station["longitude"]
    )
    
    # Get upcoming arrivals for this station
    upcoming_arrivals = station_finder.get_arrival_predictions(nearest_station["id"])
            
    search_data = {
        "query": location_query,
        "address": location_data["address"],
        "latitude": location_data["latitude"],
        "longitude": location_data["longitude"],
        "station": nearest_station,
        "distance": distance
    }

    history_manager.add_to_recent_searches(session, search_data)

    return render_template('result.html',
                           search_data=search_data,
                           mapbox_token=MAPBOX_ACCESS_TOKEN,
                           recent_searches=history_manager.get_recent_searches(session),
                           favorites=history_manager.get_favorites(session),
                           arrivals=upcoming_arrivals)  # Pass arrivals to template

@app.route('/add_favorite', methods=['POST'])
def add_favorite():
    """
    Add a location to favorites.
    """
    data = request.get_json()
    if history_manager.add_to_favorites(session, data):
        return jsonify({"status": "success"})
    return jsonify({"status": "already_exists"})

@app.route('/remove_favorite', methods=['POST'])
def remove_favorite():
    """
    Remove a location from favorites.
    """
    data = request.get_json()
    if history_manager.remove_from_favorites(session, data.get('address')):
        return jsonify({"status": "success"})
    return jsonify({"status": "error"})

@app.route('/clear_history', methods=['POST'])
def clear_history():
    """
    Clear search history.
    """
    session.pop('recent_searches', None)
    session.modified = True
    return redirect(url_for('index'))


@app.route('/api/station_info/<station_name>')
def station_info(station_name):
    """
    API endpoint to get information about a specific station.
    
    Args:
        station_name: Name of the station to look up
        
    Returns:
        JSON response with station information
    """
    # For demo purposes, return hardcoded data for some common stations
    stations = {
        "Symphony": {
            "name": "Symphony",
            "lines": ["Green Line - E Branch"],
            "accessible": True,
            "address": "Massachusetts Ave at Huntington Ave, Boston, MA"
        },
        "Fenway": {
            "name": "Fenway",
            "lines": ["Green Line - D Branch"],
            "accessible": True,
            "address": "Park Drive near Fenway Park, Boston, MA"
        },
        "Harvard": {
            "name": "Harvard",
            "lines": ["Red Line"],
            "accessible": True,
            "address": "Harvard Square, Cambridge, MA"
        }
    }
    
    # Case-insensitive lookup with fallback
    for key, data in stations.items():
        if key.lower() == station_name.lower():
            return jsonify(data)
    
    # Station not in our hardcoded list - fallback to a dummy response
    return jsonify({
        "name": station_name.title(),
        "lines": ["Unknown"],
        "accessible": False,
        "address": "Boston, MA"
    })


# --- Run the app ---
if __name__ == '__main__':
    app.run(debug=True)