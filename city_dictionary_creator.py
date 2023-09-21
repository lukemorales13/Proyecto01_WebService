import json
import pickle
import re

#with open('city.list.json', 'r', encoding='utf-8-sig') as file_contents:
with open('ejemplo.json', 'r', encoding='utf-8-sig') as file_contents:
    parsed_json = json.loads(file_contents.read())

print()
print("transference to diccionary completed")
print()

cities_dictionary = {}

for city in parsed_json:
    # Ver como aceptar letras raras
    name = re.sub("[^A-Z]", "", city['name'], 0,re.IGNORECASE)
#    print("String after conversion: ",name)
    cities_dictionary[name[0]] = {}

for city in parsed_json:
    name = re.sub("[^A-Z]", "", city['name'], 0,re.IGNORECASE)
    cities_dictionary[name[0]][city['name']] = []
    
for city in parsed_json:
    name = re.sub("[^A-Z]", "", city['name'], 0,re.IGNORECASE)
    cities_dictionary[name[0]][city['name']].append(city['country'])



print(cities_dictionary)
#print()

with open('ciudades.pkl', 'wb') as file_out:
#with open('ejemplo-ciudades.pkl', 'wb') as file_out:
    pickle.dump(cities_dictionary, file_out)
    
print('archivo creado')
print()    

 
