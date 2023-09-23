import sys
import time
import requests

key = "&appid=155505a47faf9082a7ee3d45f7b1ea0b&units=metric"
url = "https://api.openweathermap.org/data/2.5/weather?"
coordinates = {}

def validLine(raw_line):
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
    cache = {}
    tickets = {}
    for raw_line in data_list:
        line = validLine(raw_line)
        tickets[line[0]] = [line[1], line[2]]
        
        if not line[1] in cache:
            try:
                url1 = (f"{url}lat={line[3]}&lon={line[4]}{key}")
                res1 = requests.get(url1)
                data1 = res1.json()
                cache[line[1]] = data1["weather"][0]
                coordinates[f"{line[3]}, {line[4]}"] = data1["weather"][0]
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
    if(IATA in cache):
        return cache[IATA]
    else:
        return "O.o"
        
def searchWeatherWith_Coordinates(lat, lon):
    if((f"{lat}, {lon}") in coordinates):
        return coordinates[f"{lat}, {lon}"]
    else:
        url1 = (f"{url}lat={lat}&lon={lon}{key}")
        res1 = requests.get(url1)
        data1 = res1.json()
        coordinates[f"{lat}, {lon}"] = data1["weather"][0]
        return data1["weather"][0]
