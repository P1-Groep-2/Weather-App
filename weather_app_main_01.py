import urllib.request
import json
from urllib.error import HTTPError

# function for the input of the weather app
def request_location():
    while True:
        location = input('Voer een postcode of plaatsnaam in: ').strip().replace(" ","+")  # Remove leading/trailing whitespace
        if not location:
            print("Error: Voer alstublieft een geldige postcode of plaatsnaam in.")
            continue
        elif location.isdigit():
            PostalCode = location
            city = converter(PostalCode)
            if city:
                break
            else:
                print("Error: Kan de stad niet vinden op basis van de opgegeven postcode.")
        else:
            city = location
            break

    return city


# converter used for postalcode to make them a city
# also has error handeling aswell as a check for code 200 (ok)
def converter(postal_code):
    url = f"http://opzoeken-postcode.be/{postal_code}.json"
    try:
        response = urllib.request.urlopen(url)
        if response.status == 200:
            data = json.load(response)
            if data:
                city = data[0]["Postcode"]["naam_hoofdgemeente"]
                return city
            else:
                print("Error: geen data gevonden voor de postal code.")
                return None
        else:
            print(f"Error: {response.status} - {response.reason}")
            return None
    except Exception as e:
        print(f"een error gebeurd voor het opvangen van de data: {e}")
        return None


# function to calculate the wind directions and show them
def get_wind_direction(degrees):
    directions = ["N", "N/NE", "NE", "E/NE", "E", "E/SE", "SE", "S/SE", "S", "S/SW", "SW", "W/SW", "W", "W/NW", "NW", "N/NW"]
    index = round((degrees % 360) / (360. / len(directions)))
    return directions[index % len(directions)]

def request_weather(location):
    api_key = "a63d18c496d1634e8b62e88c148e8f90"
    lang = "nl"
    url = f"https://api.openweathermap.org/data/2.5/weather?q={location}&appid={api_key}&lang={lang}"
   
    response = urllib.request.urlopen(url)
     
    if response.status == 200:
        response_json = response.read()
        parsed_json = json.loads(response_json)   #json converter
       
        weather_dict = {}   #Directory to save all necesary information
           
        #add data to weather_dict with certain key , value from the parsed_json obj
        weather_dict["temp"]= parsed_json.get("main").get("temp")
        weather_dict["temp_min"]= parsed_json.get("main").get("temp_min")
        weather_dict["temp_max"]= parsed_json.get("main").get("temp_max")
        weather_dict["humidity"]= parsed_json.get("main").get("humidity")
        weather_dict["desc"]= parsed_json.get("weather")[0].get("description")
        weather_dict["wind"]= parsed_json.get("wind")
    else:
        print(f"Error: {response.status} - {response.reason}")
    return weather_dict

def main():
    print("Hallo welkom op onze weer-cli")
    #weather_json = request_weather(request_location())
    while True:
        location = request_location()
        try:
            weather_json = request_weather(location)
            if weather_json:
                break  # Exit the loop if weather data is successfully retrieved
            else:
                print("Error: Could not retrieve weather data. Please try again.")
        except HTTPError as e:
                print(f"HTTP Error: {e.code} - {e.reason}")
 
   
    temp_celsius = round(weather_json.get("temp") - 273.15) # all tempatures from Kelvin to Celsius
    temp_celsius_max = round(weather_json.get("temp_max") - 273.15)
    temp_celsius_min = round(weather_json.get("temp_min") - 273.15)
    wind_speed_mps = weather_json.get('wind').get('speed')
    wind_speed_kph = round(wind_speed_mps * 3.6, 2)  # Convert m/s to km/h
    wind_speed = f"{wind_speed_kph} km/h"
    wind_degree = weather_json.get('wind').get('deg')
    humidity = weather_json.get("humidity")
   
    #Wind degrees to  wind direction
    wind_direction = get_wind_direction(wind_degree)
     
    print(f"\nWeersomschrijving: {weather_json.get('desc')}\nTemperatuur: {temp_celsius} graden Celsius \nMax temperatuur: {temp_celsius_max} graden Celsius\nMin temperatuur: {temp_celsius_min} graden Celsius\nWind: {wind_speed} {wind_direction}\nLuchtvochtigheid: {humidity}%\n")

main()
