# MBTA-Web-App-Project

This is the base repository for Web App project. Please read the [instructions](instructions.md) for details.


#added by me

MBTA Finder Web Application
Project Overview
MBTA Finder is an interactive web application that helps users find the nearest MBTA (Massachusetts Bay Transportation Authority) stations to any location in Boston. By simply entering a place name or address, users can discover nearby public transportation options, view their locations on an interactive map, and access real-time arrival information. The application combines data from the Mapbox Geocoding API and MBTA API to provide a seamless user experience.

Features
Location Search: Find MBTA stations near any place or address in Boston
Interactive Map: Visualize both your location and nearby stations on a Mapbox map
Transportation Filtering: Filter results by transportation type (subway, bus, commuter rail, ferry)
Real-time Arrivals: Get up-to-date arrival predictions for each station
Accessibility Information: See whether stations are wheelchair accessible
Distance Calculation: Know how far you need to walk to reach the station
Responsive Design: Works on both desktop and mobile devices
Technology Stack
Python: Core programming language
Flask: Web framework for building the application
Mapbox API: For geocoding and map visualization
MBTA API: For station data and real-time arrival information
Bootstrap: Front-end framework for responsive design
JavaScript: For interactive map and real-time data updates
HTML/CSS: For structure and styling
Getting Started
Prerequisites
Python 3.8 or higher
Mapbox API key
MBTA API key
Installation
Clone the repository
git clone https://github.com/yourusername/MBTA-Web-App-Project.git
cd MBTA-Web-App-Project
Create a virtual environment and activate it
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
Install required packages
pip install -r requirements.txt
Create a .env file in the project root with your API keys:
MAPBOX_TOKEN=your_mapbox_api_key
MBTA_API_KEY=your_mbta_api_key
FLASK_SECRET_KEY=any_random_string_for_session_security
Run the application
python app.py
Open your web browser and navigate to http://127.0.0.1:5000/
Project Structure
/MBTA-Web-App-Project
├── static/
│   └── css/
│       └── style.css
├── templates/
│   ├── base.html
│   ├── error.html
│   ├── index.html
│   └── mbta_station.html
├── .env
├── .gitignore
├── app.py
├── mbta_helper.py
└── README.md
Usage
Enter a location in Boston (e.g., "Fenway Park", "Boston Common")
Select which transportation types you're interested in
Click "Find Stations"
View the nearest station information and interactive map
Check real-time arrivals that automatically update every 30 seconds
Future Improvements
Add walking directions from your location to the station
Implement nearby attractions and points of interest
Include detailed station amenities information
Add user accounts to save favorite stations
Implement trip planning functionality
License
MIT

Acknowledgments
MBTA for providing the API
Mapbox for the geocoding and mapping services
Boston College for the project assignment
