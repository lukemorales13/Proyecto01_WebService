import json
import pickle

def __create_list(jsonfile):
    try:
        print()
        print("####### Transfering '", jsonfile, "' to list #######")
        print()

        with open(jsonfile, 'r', encoding='utf-8-sig') as file_contents:
            parsed_json = json.loads(file_contents.read())

        print("####### Transference to list completed #######")
        print()
        return parsed_json
    except FileNotFoundError:
        print("File ", jsonfile, " not found!")
        exit()

def __create_dictionary(parsed_json):
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

def create_cities_file(pklfile):
    
    parsed_json = __create_list('src/app/static/json/city.list.json')
    cities_dictionary = __create_dictionary(parsed_json)

    print("####### Creating file '", pklfile, "' #######")
    print()    

    with open(pklfile, 'wb') as file_out:
        pickle.dump(cities_dictionary, file_out)
        
    print("####### File '", pklfile, "' created #######")
    print()    
 
