from agents import function_tool
from dotenv import load_dotenv
import os

import requests
load_dotenv()

API_KEY = os.getenv('WEATHER_API_KEY')
BASE_URL = "http://api.weatherapi.com/v1/current.json"

@function_tool
def get_weather(city: str):
    """Fetch current weather for a given city from WeatherAPI."""
    print('get_weather tools hits <---')

    url = f"{BASE_URL}?key={API_KEY}&q={city}&aqi=no"
    try:
        response = requests.get(url, timeout=5)
        response.raise_for_status()  
        data = response.json()
        
        # Parsign useful info beacuse this is just the basic weathre tool other wise,
        # sending full res for more detailed anwser would be good
        lastUpdated =data['current']['last_updated']
        location =data['location']['name'] +', ' + data['location']['region']
        country = data["location"]["country"]
        temp_c = data["current"]["temp_c"]
        temp_f = data["current"]["temp_f"]
        windkph = data["current"]["wind_kph"]
        cloud = data["current"]["cloud"]
        humidity = data["current"]["humidity"]
        condition = data["current"]["condition"]["text"]
        
        return f"{location}, {country}, lastUpdated:{lastUpdated}, Centigrade:{temp_c}°C, Fahrenheit:{temp_f}°f, {condition} Cloud:{cloud}, humidity:{humidity}, wind_speed:{windkph}"
    
    except requests.exceptions.RequestException as e:
        return f"Error fetching weather data for city: {e}"
    except KeyError:
        return "Could not parse weather data lol."

@function_tool
def add(a: int, b: int) -> int:
    """add two integers and returns the result."""
    print('add tools hits <---')
    return a + b

# @function_tool
# def multiply(a: int, b: int) -> int:
#     """Multiplies two integers and returns the result."""
#     print('multiply tools hits <---')
#     return a * b