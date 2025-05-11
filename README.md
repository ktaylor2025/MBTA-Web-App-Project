# MBTA Station Finder

## Project Overview
The MBTA Station Finder is a Flask web application that helps users find the nearest MBTA (Massachusetts Bay Transportation Authority) station from any location in the Boston area. The application uses the Mapbox API for geocoding and visualization, and the MBTA API to fetch real-time public transit data. This tool solves the common problem of travelers trying to locate the closest public transportation option in an unfamiliar city.

![MBTA Station Finder Screenshot](screenshot.png)

---

## Features

- 🔍 **Location-Based Search**  
  Enter any address, landmark, or place name in the Boston area to find nearby stations

- 📏 **Distance Calculation**  
  Shows the precise distance in miles between your location and the nearest MBTA station using the Haversine formula

- 🗺️ **Interactive Map Visualization**  
  Dynamic Mapbox integration with custom markers and route lines between your location and the station

- 🕓 **Search History Management**  
  Automatically saves your five most recent searches for quick access using session storage

- ⭐ **Favorites System**  
  Save frequently used locations to your favorites list for instant retrieval

- 💬 **AI-Assisted Helper**  
  Intelligent chatbot assistant that answers questions and helps you navigate the application

- 🚆 **Station Information**  
  Displays routes, line colors, and accessibility information for found stations

---

## Technologies Used

- **Python 3.x** – Core programming language with focus on modular object-oriented design
- **Flask** – Web framework for routing, templates, and session management
- **Mapbox API** – Geocoding services and interactive map visualization
- **MBTA API** – Real-time transit data including stations, routes, and service information
- **JavaScript** – Client-side interactivity, AJAX requests, and dynamic content updates
- **HTML/CSS** – Responsive frontend interface with custom styling
- **Flask Sessions** – User state management without requiring database infrastructure

---

## Project Structure
mbta-station-finder/
├── app.py                 # Main Flask application with route handlers and class definitions
├── static/
│   └── css/
│       └── styles.css     # Custom styling for the interface
│   └── js/                # (Optional) JavaScript modules if separated from templates
├── templates/
│   ├── base.html          # Base template with common layout elements
│   ├── index.html         # Home page with search form and assistant
│   └── result.html        # Results view showing station information
├── .env                   # Environment variables (not in version control)
├── .gitignore             # Git ignore file for sensitive data and cache
├── requirements.txt       # Project dependencies
└── README.md              # Project documentation

---

## Software Design Principles

### Modular Class-Based Architecture
The application follows object-oriented principles with a clean separation of concerns:

- `MBTAStationFinder`: Encapsulates all API interactions and data processing
  - Geocoding location queries to coordinates
  - Finding nearest stations based on coordinates
  - Retrieving route information
  - Calculating distances between points

- `SearchHistoryManager`: Manages user data persistence
  - Tracks recent searches 
  - Handles favorites management
  - Maintains session state

### Error Handling and Fault Tolerance
- Comprehensive try/except blocks ensure the application remains stable
- Graceful error messages when APIs fail or return unexpected data
- Fallback options when certain features are unavailable

### Clean Code Practices
- Consistent naming conventions following Python PEP8 guidelines
- Comprehensive docstrings and type hints for all methods
- Logical organization of code with related functionality grouped together

---

## Setup Instructions

### 1. Clone the Repository
git clone https://github.com/your-username/mbta-station-finder.git
cd mbta-station-finder
### 2. Install Dependencies
pip install -r requirements.txt
### 3. Set Up Environment Variables
Create a .env file in the root directory with:
MAPBOX_ACCESS_TOKEN=your_mapbox_key_here
MBTA_API_KEY=your_mbta_key_here
FLASK_SECRET_KEY=your_secret_key_here
* not added because I don't want to get in trouble or get robbed
### 4. Run the Application
python app.py
### 5. Access in Browser
Navigate to http://127.0.0.1:5000 to use the application

Implementation Details
Key Components

Geocoding: Converts user-entered locations to precise latitude/longitude coordinates
Station Finding: Queries the MBTA API with coordinates to locate the nearest stations
Distance Calculation: Uses the Haversine formula to calculate straight-line distances
Session Management: Employs Flask's session mechanism to store user data without a database
Dynamic UI: JavaScript-powered interface with real-time updates and interactive elements

Technical Workflow

User enters a location in the search box
The application geocodes this to coordinates using Mapbox
These coordinates are used to query the MBTA API for nearby stations
The application calculates the distance to each station
Results are displayed on an interactive map and in a detailed information panel
Search is saved to the user's history for future reference


Development Process
This project began as a simple proof-of-concept and evolved through several iterations:
Phase 1: Core Functionality

Basic Flask application setup
Integration with Mapbox for geocoding
MBTA API connection for station data

Phase 2: Enhanced User Experience

Added interactive mapping
Implemented distance calculations
Improved error handling and user feedback

Phase 3: Advanced Features

Developed session-based history tracking
Created favorites system
Built intelligent assistant chatbot
Added real-time data display and route visualization


Credits and Acknowledgments
Developed by Kaley Taylor for OIM3640: Problem Solving & Software Design at Babson College.
APIs Used:

MBTA API
Mapbox API

AI Assistance:
Some portions of code and content were developed with the assistance of AI tools (ChatGPT and Claude) to support design planning, debugging, and documentation refinement. All implementation decisions, testing, and final code architecture were completed by the developer.

License
This project is provided for educational purposes as part of Babson College's Spring 2025 curriculum.