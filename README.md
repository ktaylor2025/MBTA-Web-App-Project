# MBTA-Web-App-Project

This is the base repository for Web App project. Please read the [instructions](instructions.md) for details.


#added by me (I worked alone)

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
Cloned the repository
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
Reflection:

Developing this project was both rewarding and challenging. From a development standpoint, learning how to work with multiple APIs (Mapbox and MBTA) was a big step forward in understanding how real-world data flows into applications. Implementing helper functions to abstract logic helped me organize my code better and made it easier to debug. The use of environment variables was also a new concept that improved my understanding of app security and configuration. One challenge I faced was parsing nested JSON responses from the APIs, especially when handling errors or missing fields — this pushed me to think more carefully about edge cases and exception handling.

Since I worked individually, I planned out tasks using a rough timeline and made sure to document everything along the way. Initially, I underestimated how much time would be needed for testing different location inputs and ensuring graceful failure when users entered invalid addresses. If I were to redo this project, I would start earlier on testing and perhaps implement a logging feature to track inputs and errors during development. I also would have explored how to deploy the app to a free platform like GitHub Pages or Vercel for broader access.

In terms of learning, this project greatly improved my confidence in working with Flask and APIs. I also gained hands-on experience with version control via GitHub, which I now see as essential for any collaborative or personal tech project. I used AI tools like ChatGPT to help break down tricky error messages and understand syntax or structural improvements for my functions. These tools were helpful for boosting efficiency, but I made sure to fully understand the code before using or modifying any suggestions. I now feel more prepared to take on web development and automation projects beyond this course.
Acknowledgments
MBTA for providing the API
Mapbox for the geocoding and mapping services
Boston College for the project assignment
