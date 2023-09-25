import sys
import time
import requests


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
    """Method to read the data from the data_list and to create the cache

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
                weather = get_weather(url1)
                cache[line[1]] = weather
                coordinates[f"{line[3]}, {line[4]}"] = weather 
                time.sleep(1.3)
            except:
                print(f"\nCould't request the weather information. The input {line} is probably incorrect.")
                sys.exit()
                
        if not line[2] in cache:
            try:
                url2 = (f"{url}lat={line[5]}&lon={line[6]}{key}")
                weather = get_weather(url2)
                cache[line[2]] = weather
                coordinates[f"{line[5]}, {line[6]}"] = weather
                time.sleep(1.3)
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
        IATA (string): IATA code.

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
        weather = get_weather(url1)
        coordinates[f"{lat}, {lon}"] = weather
        return weather
    
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
        weather = get_weather(url1)
        cities[location] = weather
        return weather

def get_weather(url1):
    res1 = requests.get(url1) 
    data1 = res1.json()
    return (f"\nCountry: {data1['sys']['country']}\nName: {data1['name']}"+
        f"\nWeather: {data1['weather'][0]['main']}, {data1['weather'][0]['description']}.\nTemperature: {data1['main']['temp']} degrees celcius.\nHumidity: {data1['main']['humidity']}%.")
