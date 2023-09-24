from flask import Flask, request, jsonify, render_template
from levenshtein import iata_search, city_search, massive_search

import sys
import time
import requests

app = Flask(__name__)

key = "&appid=155505a47faf9082a7ee3d45f7b1ea0b&units=metric" #key of the API
url = "https://api.openweathermap.org/data/2.5/weather?"
coordinates = {} #Dictionary "lat, lon": weather
cache = {} #Dictionary "IATA" : weather
tickets = {} #Dictionary "ticket": [IATA1, IATA2]
cities = {} #Dictionary "country,city" : weather

def validLine(raw_line):
    """Method to check if a line in the dataset is valid. 

    Args:
        raw_line (string): the line as a string

    Returns:
        list: a list of the elements of the line
    """
    line = raw_line.rsplit(",")
    if len(line[0])!=16:
        print(f"\nTicket {line[0]} is not valid, must have exactly 16 characters.")
    try:
        line[3] = float(line[3])
        line[4] = float(line[4])
        line[5] = float(line[5])
        line[6] = float(line[6])
    except:
        print(f"\nFormat of latitude or longitude is not valid on line {line}, must have exactly 16 characters.")
    return line

def readData(data_list):
    """Method to read the data from the data_list

    Args:
        data_list (list): A list with the data of the dataset.

    Returns:
        dict,dict: Cache, with the weather of each IATA code. And tickets, with the IATA code of origin and destination.
    """
    cache = {}
    tickets = {}
    for raw_line in data_list:
        line = validLine(raw_line) #check if the line is valid
        tickets[line[0]] = [line[1], line[2]]
        
        if not line[1] in cache:
            try:
                url1 = (f"{url}lat={line[3]}&lon={line[4]}{key}") #create the url
                res1 = requests.get(url1) #makes the API call
                data1 = res1.json() #define the format
                cache[line[1]] = data1["weather"][0] #save the weather information that we want in the cache
                coordinates[f"{line[3]}, {line[4]}"] = data1["weather"][0] #save the weather information that we want associated with its coordinates
                time.sleep(1.5)
            except:
                print(f"\nCould't request the weather information. The input {line} is probably incorrect.")
                sys.exit()
                
        if not line[2] in cache:
            try:
                url2 = (f"{url}lat={line[5]}&lon={line[6]}{key}")
                res2 = requests.get(url2)
                data2 = res2.json()
                cache[line[2]] = data2["weather"][0]
                coordinates[f"{line[5]}, {line[6]}"] = data1["weather"][0]
                time.sleep(1.5)
            except:
                print(f"\nCould't request the weather information. The input {line} is probably incorrect.")
                sys.exit()

    return cache, tickets
    
def searchWeatherWith_ticket(ticket):
    """method to search the weather of the cities included in an airplane ticket

    Args:
        ticket (string): ticket we want to search

    Returns:
        string: weather of the cities included in the ticket
    """
    if(ticket in tickets):
        IATAS = tickets[ticket]
        weather1 = cache[IATAS[0]]
        weather2 = cache[IATAS[1]]
        IATA1 = tickets[ticket][0]
        IATA2 = tickets[ticket][1]
        return (f"{IATA1}:\n{weather1}\n\n{IATA2}:\n{weather2}")
    else:
        return ("Ticket not found.\nPlease check again the information.")

def searchWeatherWith_IATA(IATA):
    """method to search the weather of a city from a IATA code

    Args:
        IATA (string): IATA code

    Returns:
        string: The weather
    """
    if(IATA in cache):
        return cache[IATA]
    else:
        return "There are no results"
        
def searchWeatherWith_Coordinates(lat, lon):
    """method to search the weather of a city with its coordinates

    Args:
        lat (string): latitude of the city
        lon (string): longitude of the city

    Returns:
        string: the weather
    """
    if((f"{lat}, {lon}") in coordinates):
        return coordinates[f"{lat}, {lon}"]
    else:
        url1 = (f"{url}lat={lat}&lon={lon}{key}")
        res1 = requests.get(url1)
        data1 = res1.json()
        coordinates[f"{lat}, {lon}"] = data1["weather"][0]
        return data1["weather"][0]
    
def searchWeatherWith_NameOfCity(country, city):
    """method to search the weather of a city with the name of the city and country

    Args:
        country (string): name of the city's country
        city (string): name of the city

    Returns:
        string: the weather
    """
    location = f"{country.lower()},{city.lower()}"
    if(location in cities):
        return cities[location]
    else:
        url1 = (f"{url}q={location}{key}")
        res1 = requests.get(url1)
        data1 = res1.json()
        weather = data1["weather"][0]
        cities[location] = weather
        return weather

# Tu código de funciones y procesamiento de datos aquí (como validLine, readData, etc.)

# Ruta para el formulario HTML
@app.route('/')
def index():
    return render_template('src/app/static/templates/html/index.html')

# Ruta para obtener datos meteorológicos
@app.route('/get_weather', methods=['GET'])
def get_weather():
    search_term = request.args.get('search')

    # Intenta buscar por IATA code
    iata_results = iata_search(search_term)
    if iata_results:
        return jsonify({'weather1': iata_results[0]})

    # Si no se encontraron resultados por IATA code, buscar por nombre de ciudad
    city_results = city_search(search_term)
    if city_results:
        return jsonify({'weather1': city_results[0]})

    # Si no se encontraron resultados por nombre de ciudad, realizar una búsqueda masiva
    massive_results = massive_search(search_term)
    if massive_results:
        return jsonify({'weather1': massive_results[0]})

    # Si no se encontraron resultados, devolver un mensaje de error
    return jsonify({'error': 'No se encontraron datos para la búsqueda.'}), 404

if __name__ == '__main__':
    app.run(debug=True)
