# https://blog.paperspace.com/implementing-levenshtein-distance-word-autocomplete-autocorrect/

import numpy
import pickle
import re
import unidecode

def levenshteinDistanceDP(token1, token2):
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


def printDistances(distances, token1Length, token2Length):
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
    
    
def calcDictDistance(word, numWords):
    
    with open('ciudades.pkl', 'rb') as file_dictionary:
        cities_dictionary = pickle.load(file_dictionary)
    
    dictWordDist = []
    wordIdx = 0

######## Ver excepcion si la primera letra no esta #########
    for city in cities_dictionary[normalize_name(word)[0]]:
        wordDistance = levenshteinDistanceDP(word, city)
        if wordDistance >= 10:
            wordDistance = 9
        dictWordDist.append(str(int(wordDistance)) + "-" + city)
        wordIdx = wordIdx + 1

    closestWords = {}
    wordDetails = []
    currWordDist = 0
    dictWordDist.sort()

    for i in range(numWords):
        currWordDist = dictWordDist[i]
        wordDetails = currWordDist.split("-")
        closestWords[wordDetails[1]] = cities_dictionary[normalize_name(word)[0]][wordDetails[1]]

    return closestWords 

city = "Monterrey"
print(calcDictDistance(city, 10))
print()
