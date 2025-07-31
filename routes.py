
from flask import Blueprint, request, render_template
from datetime import datetime
import requests
import os
import pytz
from timezonefinder import TimezoneFinder


weather_bp = Blueprint('weather', __name__,url_prefix='/weather')

API_KEY = os.getenv("WEATHER_API_KEY")
print("Loaded API Key: ", API_KEY)



@weather_bp.route('/',methods=["GET", "POST"]) #Accepts city or Zip
def get_weather():
    
    weather = None
    icon = None
    error = None
    uv_index_label = None
    moon_phase = None
    wind_speed = None
    humidity = None
    temperature = None
    pressure = None
    city_input = None
    dew_point = None 
    feels_like = None
    formatted_time = None
    attribute_icons = None
    moon_icons = None
    visibility_miles = None
    moon_icons_filename = 'moon.png'
    sunrise_time = None
    sunset_time = None
    weekly_descriptions = None
    description = None
    state = None
    state_code = None
    city_name = None
    is_daytime = True

    icon_map = {

        #Can't use Weather App icons.
        #Using icons from flaticon.com + moon phases
        "clear": "sun.png",
        "mostly cloudy": "mostly-cloudy.png",
        "shower rain": "dizzle.png",
        "cloudy": "cloudy-day.svg", 
        "scattered clouds": "scattered-clouds.png",
        "rain": "rain.svg",
        "thunderstorm": "thunderstorm.svg",
        "thunderstorm with heavy rain": "thunderstorm-with-heavyrain.png",
        "heavy thunderstorm": "thunderstorm-with-heavyrain.png",
        "thunderstorm with light rain": "thunderstorm-with-light-rain.png",
        "thunderstorm light drizzle": "thunderstorm-light-drizzle.png",
        "thunderstorm "
        "hail": "hail.png",
        "hazy": "hazy.png",
        "windy": "wind.svg",
        "snow": "snow.png",
        "light snow": "snowflake.png",
        "sunrise": "sunrise.png",
        "sunset": "sunset.png",
        "overcast clouds": "overcast-clouds.png",
        "broken clouds": "broken-clouds.png",
        "clear sky": "clear-sky.png",
        "light rain": "light-rain.png",
        "few clouds": "few-clouds.png",
        "moderate rain": "moderate-rain.png",
        "very heavy rain": "very-heavy-rain.png",
        "heavy intensity rain": "very-heavy-rain.png",

    }

    attribute_icons = {
        "Temperature": "thermometer.png",
        "Wind Speed": "windy.png",
        "UV Index": "uv-index.png",
        "Pressure": "pressure.png",
        "Humidity": "humidity.png",
        "Dew Point": "dew-point.png",
        "Visibility": "visibility.png",

    }

    moon_icons = {
        "new moon": "new-moon.png",
        "waning gibbous": "waning-gibbous.png",
        "waning crescent": "waning-crescent.png",
        "first quarter": "first-quarter.png",
        "last quarter": "last-quarter.png",
        "waxing crescent": "waxing-crescent.png",
        "full moon": "full-moon.png",
        "waxing gibbous": "waxing-gibbous.png",

    }

    us_state_abbrev = {
        'alabama': 'AL', 'alaska': 'AK', 'arizona': 'AZ', 'arkansas': 'AR',
        'california': 'CA', 'colorado': 'CO', 'connecticut': 'CT', 'delaware': 'DE',
        'florida': 'FL', 'georgia': 'GA', 'hawaii': 'HI', 'idaho': 'ID', 'illinois':'IL',
        'indiana': 'IN', 'iowa': 'IA', 'kansas': 'KS', 'kentucky': 'KY', 'louisiana': 'LA',
        'maine': 'ME', 'maryland':'MD', 'massachusetts': 'MA', 'michigan': 'MI', 'minnesota': 'MN',
        'mississippi': 'MS', 'missouri': 'MO', 'montana': 'MT', 'nebraska': 'NE', 'nevada': 'NV',
        'new hampshire': 'NH', 'new jersey': 'NJ', 'new mexico': 'NM', 'new york': 'NY',
        'north carolina': 'NC', 'north dakota':'ND', 'ohio': 'OH','oklahoma': 'OK',
        'oregon': 'OR', 'pennsylvania': 'PA', 'rhode island': 'RI', 'south carolina': 'SC', 
        'south dakota': 'SD', 'tennessee': 'TN', 'texas': 'TX', 'utah': 'UT', 'vermont': 'VT',
        'virginia': 'VA', 'washington':'WA', 'west virginia': 'WV','wisconsin': 'WI', 'wyoming': 'WY', 
    }

   

    if request.method == "POST":
        city_input = request.form.get("city").strip()        


        if ',' in city_input:
            city_parts = city_input.split(',')
            city_name = city_parts[0].strip()
            state_raw = city_parts[1].strip().lower()
            state_code = us_state_abbrev.get(state_raw, state_raw.upper())
        else:
            city_name = city_input
            state_code = ''

            
        #Handles the zip code queries
        if city_input.isdigit() and len(city_input) == 5:
            geo_url = f"https://api.openweathermap.org/geo/1.0/zip?zip={city_input},US&appid={API_KEY}"

        else:
            geo_url = f"http://api.openweathermap.org/geo/1.0/direct?q={city_name},{state_code},US&limit=1&appid={API_KEY}"
           
        
        geo_response = requests.get(geo_url)
        print(f"Geo API URL: {geo_url}")  #Added dugging to see real API error
        print(f"Geo API response: {geo_response.text}")
        print(f"Geo Status Code: {geo_response.status_code}")

        if geo_response.status_code != 200:
            return render_template("index.html", error=f"Geo API error: {geo_response.status_code} - {geo_response.text}")
            
        try:
            geo_data = geo_response.json()

            #Handle zip codes and city names
            if isinstance(geo_data, list):
                if not geo_data:
                    return render_template("index.html", error="Location not found.")
                geo_data = geo_data[0]
            elif isinstance(geo_data, dict):
                if "lat" not in geo_data or "lon" not in geo_data:
                    return render_template("index.html",error="Invalid zip code or coordinates not found.")
                if "name" in geo_data:
                    city_input = geo_data["name"]
            else:
                return render_template("index.html",error="Unexpected API format.")           
            
            
            lat = geo_data.get("lat")
            lon = geo_data.get("lon")
            state = geo_data.get("state", "")
            city_input = geo_data.get("name", "").title()
            

            if not lat or not lon:
                return render_template("index.html", error="Coordinates not found.")
        except ValueError:
            return render_template("index.html", error="Error decoding location.")

        
        tf = TimezoneFinder()
        timezone_str = tf.timezone_at(lat=lat, lng=lon)
        if timezone_str:
            timezone_obj = pytz.timezone(timezone_str)
            local_time = datetime.now(timezone_obj)
            formatted_time = local_time.strftime("%A, %B %d, %Y   - %I:%M %p %Z")
        else:
            formatted_time = "Timezone not found"
                
        onecall_url = (
                    f"https://api.openweathermap.org/data/3.0/onecall"
                    f"?lat={lat}&lon={lon}&units=imperial&exclude=minutely,hourly,alerts&appid={API_KEY}"
        )
                     

        weather_response = requests.get(onecall_url)
        print("One Call API URL:", onecall_url)
        print("Weather API Response:",weather_response.text)

        if weather_response.status_code != 200:
            return render_template("index.html",error=f"Weather API error: {weather_response}")
        
        weather = weather_response.json()
        print(f"Weather Data: {weather}")
                    
        if weather and timezone_str:
            sunset_unix = weather['current'].get('sunset')
            sunrise_unix = weather['current'].get('sunrise')


        if sunrise_unix and sunset_unix:
            sunrise_dt= datetime.fromtimestamp(sunrise_unix, timezone_obj)
            sunset_dt = datetime.fromtimestamp(sunset_unix, timezone_obj)

            #Debugs for sunset/sunset, current time
            print("Timezone:",timezone_str)
            print("Current Local Time:",local_time)
            print("Sunrise Local Time:",sunrise_dt)
            print("Sunset Local Time:",sunset_dt)

            is_daytime = sunrise_dt < local_time < sunset_dt
            print("Is Daytime:",is_daytime)

            sunrise_time = sunrise_dt.strftime('%I:%M %p')
            sunset_time = sunset_dt.strftime('%I:%M %p')
        else:
            print("Missing sunrise/sunset data. Using a fallback daytime range.")
            is_daytime = 6 <= local_time.hour < 18
            print("Fallback Is Daytime: ", is_daytime)
            
        

        daily = weather.get('daily')
        if isinstance(daily, list) and len(daily) > 0:
            moon_phase = get_moon_phases(daily[0].get("moon_phase",0))
        else:
            moon_phase = "N/A"


        temperature = weather['current'].get('temp')
        feels_like = weather['current']['feels_like']
        humidity = weather['current']['humidity']
        raw_pressure = weather['current']['pressure']

        pressure = round(raw_pressure * 0.02953, 2) #Converts pressure to inches 
        wind_speed = weather['current']['wind_speed']
        dew_point = weather['current']['dew_point']
        visibility = weather['current'].get('visibility')

        if visibility is not None:
            visibility_miles = round(visibility / 1609) #Converts miles, rounds to the nearest whole number
        else: 
            visibility_miles = "N/A"

        if 'weather' in weather['current'] and weather['current']['weather']:
            description = weather['current']['weather'][0]['description'].lower().strip()
            print(f"API weather description: '{description}' ")
            print(f"Mapped icon: {icon}")
            icon = icon_map.get(description, "na.png")
        else: 
            icon = "na.png"

        uvi_value = weather['current'].get("uvi", "N/A")
        uv_index_label = get_uv_index(uvi_value) if uvi_value is not None else '<span style:"color; gray;">Unknown</span>'
        moon_icons_filename = moon_icons.get(moon_phase.lower(), 'moon.png')
    else:
        error = None
    
    
    #Weekly Weather Forecast
    weekly_descriptions = []
    weekly_icons = []
    weekly_days = []

    if weather: 
        daily_forecast = weather.get('daily',[])
        for day in daily_forecast[1:8]:
            weather_list = day.get('weather', [])
            if weather_list and isinstance(weather_list, list):
                description = weather_list[0].get('description', 'No description')
            else:
                description = 'No description'
            weekly_descriptions.append(description.title())

            #Get icon
            icon_filename = icon_map.get(description.lower(), "na.png")
            weekly_icons.append(icon_filename)

            #Get weekday
            timestamp = day.get('dt')
            if timestamp:
                day_name = datetime.fromtimestamp(timestamp).strftime('%a')

            else:
                 day_name = 'N/A'
            weekly_days.append(day_name)
                 

    return render_template("index.html", moon_phase=moon_phase, wind_speed=wind_speed,pressure=pressure, 
                           humidity=humidity, dew_point=dew_point, icon=icon,feels_like=feels_like, weekly_icons=weekly_icons,
                           temperature=temperature, moon_icons=moon_icons,weather=weather,formatted_time=formatted_time, attribute_icons=attribute_icons , 
                           city_input=city_input, error=error, visibility=visibility_miles,uv_index_label=uv_index_label, moon_icons_filename=moon_icons_filename,
                           sunrise=sunrise_time,weekly_descriptions=weekly_descriptions, description=description,weekly_days=weekly_days,city_name=city_name,state=state, is_daytime=is_daytime,state_code=state_code,sunset=sunset_time)


def get_moon_phases(value): #Add moon phases
     if value == 0 or value == 1:
        return "New Moon"
     elif 0 < value < 0.25:
        return "Waxing Crescent"
     elif value == 0.25:
        return "First Quarter"
     elif 0.25 < value < 0.5:
        return "Waxing Gibbous"
     elif value == 0.5:
        return "Full Moon"
     elif 0.5 < value < 0.75:
        return "Waning Gibbous"
     elif value == 0.75:
        return "Last Quarter"
     else:
        return "Waning Crescent"

def get_uv_index(value):  #Add colors to uv index
    try:
        value = float(value)
    except (TypeError, ValueError):
        return '<span style="color: gray;">Unknown</span>'
    if value <= 2:
        return f'<span style="color: green;">Low</span>'
    elif 3 <= value <= 5:
        return f'<span style="color: orange;">Moderate</span>'
    elif 6 <= value <= 7:
        return f'<span style="color: red;">High</span>'
    elif 8 <= value <= 10:
        return f'<span style="color: darkred;">Very High</span>'
    else:
        return f'<span style="color: purple;">Extreme</span>'
    



