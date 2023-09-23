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

def create_dictionary(parsed_json):
    print('####### Creating dictionary #######')
    print()    

    cities_dictionary = {}
    for city in parsed_json:
        if not city['name'] in cities_dictionary:
            cities_dictionary[city['name']] = []
        if city['country'] in cities_dictionary[city['name']]:
            continue
        cities_dictionary[city['name']].append(city['country'])
    
    print('####### Dictionary created #######')
    print()
    return cities_dictionary

def create_file(pklfile, cities_dictionary):
    print("####### Creating file '", pklfile, "' #######")
    print()    

    with open(pklfile, 'wb') as file_out:
        pickle.dump(cities_dictionary, file_out)
        
    print("####### File '", pklfile, "' created #######")
    print()    


parsed_json = create_list('json/city.list.json')
cities_dictionary = create_dictionary(parsed_json)
create_file('ciudades.pkl', cities_dictionary)
 
