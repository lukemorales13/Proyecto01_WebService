import json
import pickle
import re
import unidecode


def create_list(jsonfile):
    print()
    print("####### Transfering '", jsonfile, "' to list #######")
    print()

    with open(jsonfile, 'r', encoding='utf-8-sig') as file_contents:
        parsed_json = json.loads(file_contents.read())

    print("####### Transference to list completed #######")
    print()
    return parsed_json

def normalize_name(name):
    new_name = unidecode.unidecode(name)
    new_name = re.sub("[^A-Z]", "", name, 0,re.IGNORECASE)
    new_name = new_name.upper()
    if (len(new_name) > 0):
        return new_name
    else:
        return name

def create_dictionary(parsed_json):
    print('####### Creating dictionary #######')
    print()    

    cities_dictionary = {}
    for city in parsed_json:
        cities_dictionary[normalize_name(city['name'])[0]] = {}

    for city in parsed_json:
        cities_dictionary[normalize_name(city['name'])[0]][city['name']] = []
        
    for city in parsed_json:
        if city['country'] in cities_dictionary[normalize_name(city['name'])[0]][city['name']]:
            continue
        cities_dictionary[normalize_name(city['name'])[0]][city['name']].append(city['country'])
    
    print('####### Dictionary created #######')
    print()    
    return cities_dictionary

def create_file(pklfile, cities_dictionary):
    print("####### Creating file '", pklfile, "' #######")
    print()    

    with open(pklfile, 'wb') as file_out:
        pickle.dump(cities_dictionary, file_out)
        
    print('####### File "ciudades.pkl" created #######')
    print()    


parsed_json = create_list('json/city.list.json')
cities_dictionary = create_dictionary(parsed_json)
create_file('ciudades.pkl', cities_dictionary)
 
