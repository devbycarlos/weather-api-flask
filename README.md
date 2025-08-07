# 🌤️ Weather API Web App

A simple weather web application that retrieves real time weather data using the OpenWeatherMap API. 


## 🔧 Features

- Search by **city name**, **state abbreviation** or **ZIP code**
- Displays:
         - ✅ City and State Name
  - 🕒 Local Date and Time
  - 🌅 Sunrise and Sunset Times
  - 🌡️ Current Temperature and "Feels Like"
  - 🌤️ Weather Description (e.g., Cloudy, Clear, Rain)
  - 📆 8-Day Weather Forecast
  - 🌞 UV Index
  - 🌕 Moon Phase
  - 🌫️ Visibility (meters)
  - 💧 Humidity (%)
  - 🎯 Atmospheric Pressure (hPa)
  - Error handling for invalid or empty input
  - Custom HTML/CSS interface
 

## ⚙️ How It Works

1. **User Input:** The user enters a city or ZIP code in the form.
2. **Geocoding API:** The input is sent to the **OpenWeatherMap Geocoding API** to get latitude and longitude.
3. **Timezone Finder:** The coordinates are used with **timezonefinder** to determine the local time zone.
4. **Weather & Forecast Data:** The lat/lon values are sent to the **One Call API (3.0)** or **Current & Forecast Weather API**, which returns:
   - Current conditions
   - 8-day forecast
   - UV index
   - Sunrise/sunset
   - Moon phase and more

5. **Display:** 
The data is rendered on the frontend using HTML and styled with custom CSS.


## 🧰 Technologies & Resources

- **Frontend:**
  - HTML
  - CSS

- **Backend:**
  - Python 3
  - Flask
  - Requests

- **APIs & Libraries:**
  - [OpenWeatherMap API (One Call 3.0)](https://openweathermap.org/api/one-call-3)
  - [TimezoneFinder](https://pypi.org/project/timezonefinder/)
  - [Requests](https://docs.python-requests.org/)
  - [Datetime & pytz](https://pypi.org/project/pytz/



## 📸 Screenshot

![Weather App Screenshot](path/to/your/screenshot.png)

> Tip: You can upload your image to the repository and update this path. If hosted on GitHub, you can use a raw file link like:
> `https://raw.githubusercontent.com/yourusername/weather-api-app/main/static/images/screenshot.png`

## 🚀 Getting Started

1. **Clone the repository:**
   ```bash
   git clone https://github.com/yourusername/weather-api-app.git
   cd weather-api-app


2. Install the required packages:
	Pip install -r requirements.txt
	WEATHER_API_KEY=your_openweathermap_api_key_here

  Python3.13  app.py

**Open in your browser:**
   Visit `http://localhost:5000/weather/`
