# https://blog.paperspace.com/implementing-levenshtein-distance-word-autocomplete-autocorrect/

import numpy
import pickle
import re
import unidecode

def levenshtein_distance(token1, token2):
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

#    printDistances(distances, len(token1), len(token2))
    return distances[len(token1)][len(token2)]

def print_distances(distances, token1Length, token2Length):
    for t1 in range(token1Length + 1):
        for t2 in range(token2Length + 1):
            print(int(distances[t1][t2]), end=" ")
        print()


def normalize_name(name):
    new_name = unidecode.unidecode(name)
    new_name = re.sub("[^A-Z]", "", name, 0,re.IGNORECASE)
    new_name = new_name.upper()
    if (len(new_name) > 0):
        return new_name
    else:
        return name

def import_pkl(pkl_file):
    with open(pkl_file, 'rb') as file_in:
        location_data = pickle.load(file_in)
    return location_data

def calculate_distance(word, num_words, max_level, type, location_data):
    dict_distance = {}
    for location in location_data:
        location_distance = int(levenshtein_distance(word, location[type]))
        if (location_distance <= max_level):
            if not location_distance in dict_distance:
                dict_distance[location_distance] = []
            dict_distance[location_distance].append(location)

#    print(dict_distance.keys())
#    print(dict_distance)

    return closest_words(num_words, 1, max_level, dict_distance, [])
        
def closest_words(num_words, level, max_level, dict_distance, closest_locations):
    if(level <= max_level):
        if level in dict_distance:
            dict_distance[level].sort()
            for location in dict_distance[level]:
                closest_locations.append(location)
                num_words = num_words - 1
                if (num_words == 0):
                    return closest_locations
        return closest_words(num_words, level+1, max_level, dict_distance, closest_locations)
    return closest_locations

def short_search(word, num_words, max_distance, type):
    iata_list = import_pkl('iata_list.pkl')
    return calculate_distance(word, num_words, max_distance, type, iata_list)

def iata_search(word):
    print('IATA ##########')
    return short_search(word, 5, 1, 0)

def city_search(word):
    print('CITY ##########')
    return short_search(word, 5, 4, 1)

def massive_search(word, num_words):
    print('MASSIVE ##########')
    cities_dictionary = import_pkl('ciudades.pkl')

    location_data = cities_dictionary[normalize_name(word)[0]]

    list_distance = []
    wordIdx = 0
######## Ver excepcion si la primera letra no esta #########
    for city in location_data:
        word_distance = levenshtein_distance(word, city)
        if word_distance >= 10:
            word_distance = 9
        list_distance.append(str(int(word_distance)) + "-" + city)
        wordIdx = wordIdx + 1

    closestWords = {}
    wordDetails = []
    currWordDist = 0
    list_distance.sort()
    for i in range(num_words):
        currWordDist = list_distance[i]
        wordDetails = currWordDist.split("-")
        closestWords[wordDetails[1]] = location_data[wordDetails[1]]
    return closestWords 


####### PRUEBAS #######
location = "Jalapa"
print(massive_search(location, 10))
print()
print("iata search: ", iata_search('MY'))
print()
print("city search: ", city_search('Jalapa'))
print()