import numpy
import pickle
import re
import unidecode

"""
Regresa la distancia entre dos palabras obtenida por el 
algoritmo de Levenshtein. 

Código obtenido de:
Gad, A. F. (2021). Implementing The Levenshtein Distance 
for Word Autocompletion and Autocorrection. Paperspace Blog. 
https://blog.paperspace.com/implementing-levenshtein-distance-word-autocomplete-autocorrect/
"""
def levenshtein_distance(token1, token2):
    
    token1 = __normalize_word(token1)
    token2 = __normalize_word(token2)
    distances = numpy.zeros((len(token1) + 1, len(token2) + 1))

    for t1 in range(len(token1) + 1):
        distances[t1][0] = t1
    for t2 in range(len(token2) + 1):
        distances[0][t2] = t2
        
    a = 0
    b = 0
    c = 0
    
    for t1 in range(1, len(token1) + 1):
        for t2 in range(1, len(token2) + 1):
            if (token1[t1-1] == token2[t2-1]):
                distances[t1][t2] = distances[t1 - 1][t2 - 1]
            else:
                a = distances[t1][t2 - 1]
                b = distances[t1 - 1][t2]
                c = distances[t1 - 1][t2 - 1]
                
                if (a <= b and a <= c):
                    distances[t1][t2] = a + 1
                elif (b <= a and b <= c):
                    distances[t1][t2] = b + 1
                else:
                    distances[t1][t2] = c + 1

    return distances[len(token1)][len(token2)]

def __normalize_word(name):
    new_name = unidecode.unidecode(name)
    new_name = re.sub("[^A-Z]", "", name, 0,re.IGNORECASE)
    new_name = new_name.upper()
    if (len(new_name) > 0):
        return new_name
    else:
        return name

def __import_pkl(pkl_file):
    try:
        with open(pkl_file, 'rb') as file_in:
            location_data = pickle.load(file_in)
        return location_data
    except FileNotFoundError:
        
        return

def __get_location(word, type, location_data):
    for location in location_data:
        location_distance = int(levenshtein_distance(word, location[type]))
        if (location_distance == 0):
            return [location]
    return []

"""
Calcula las distancias de Levenshtein entre la palabra 
escogida y cada palabra de la lista de las palabras a comparar.
Regresa un diccionario con subdiccionarios, donde cada uno 
tiene palabras con la misma distancias resspecto a la pedida.

Código basado en:
Gad, A. F. (2021). Implementing The Levenshtein Distance 
for Word Autocompletion and Autocorrection. Paperspace Blog. 
https://blog.paperspace.com/implementing-levenshtein-distance-word-autocomplete-autocorrect/
"""
def __calculate_distance(word, max_distance, type, location_data):
    dict_distance = {}
    for location in location_data:
        location_distance = int(levenshtein_distance(word, location[type]))
        if (location_distance <= max_distance):
            if not location_distance in dict_distance:
                dict_distance[location_distance] = []
            dict_distance[location_distance].append(location)
    return dict_distance
        
def __closest_words_short(num_words, level, max_distance, dict_distance, closest_locations):
    if(level <= max_distance):
        if level in dict_distance:
            dict_distance[level].sort()
            for location in dict_distance[level]:
                closest_locations.append(location)
                num_words = num_words - 1
                if (num_words == 0):
                    return closest_locations
        return __closest_words_short(num_words, level+1, max_distance, dict_distance, closest_locations)
    return closest_locations

def __short_search(word, num_words, max_distance, type):
    iata_list = __import_pkl('iata_list.pkl')
    exact_location = __get_location(word, type, iata_list)
    if(exact_location == []):
        dict_distance = __calculate_distance(word, max_distance, type, iata_list)
        return __closest_words_short(num_words, 1, max_distance, dict_distance, [])
    else:
        return exact_location

def iata_search(word):
    return __short_search(word, 5, 1, 0)

def city_search(word):
    return __short_search(word, 5, 3, 1)

"""
Calcula las distancias de Levenshtein entre la palabra 
escogida y cada palabra de la lista de las palabras a 
comparar, luego guarda las palabras con la distancia menor. 
Regresa una lista con las palabras más cercanas a la pedida.

Código basado en:
Gad, A. F. (2021). Implementing The Levenshtein Distance 
for Word Autocompletion and Autocorrection. Paperspace Blog. 
https://blog.paperspace.com/implementing-levenshtein-distance-word-autocomplete-autocorrect/
"""
def massive_search(word):
    num_words = 10
    max_distance = 3
    cities_dictionary = __import_pkl('ciudades.pkl')
    dict_distance = {}
    for location in cities_dictionary:
        location_distance = int(levenshtein_distance(word, location))
        if (location_distance <= max_distance):

            if (location_distance == 0):
                closest_locations = []
                for country in cities_dictionary[location]:
                    closest_locations.append([location, country])
                return closest_locations
            
            if not location_distance in dict_distance:
                dict_distance[location_distance] = {}
            dict_distance[location_distance][location] = cities_dictionary[location]
    return __closest_words_massive(num_words, 1, max_distance, dict_distance, [])

def __closest_words_massive(num_words, level, max_distance, dict_distance, closest_locations):
    if(level <= max_distance):
        if level in dict_distance:
            for location in dict_distance[level]:
                for country in dict_distance[level][location]:
                    closest_locations.append([location, country])
                    num_words = num_words - 1
                if (num_words == 0):
                    return closest_locations
        return __closest_words_massive(num_words, level+1, max_distance, dict_distance, closest_locations)
    return closest_locations


####### PRUEBAS #######

location = "Taglag"
print()
print('MASSIVE ##########')
print(massive_search(location))
print()
print('IATA ##########')
print("iata search: ", iata_search('mty'))
print()
print('CITY ##########')
print("city search: ", city_search(location))
print()