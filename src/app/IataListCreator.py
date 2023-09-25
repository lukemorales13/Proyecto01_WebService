import pickle

location_list = []
iata_list = []
iata_cities = {
    'ACA':'Acapulco',
    'AGU':'Aguascalientes',
    'AMS':'Ámsterdam',
    'ATL':'Atlanta',
    'BJX':'León',
    'BOG':'Bogotá',
    'BZE':'Belice',
    'CDG':'París',
    'CEN':'Ciudad Obregón',
    'CJS':'Ciudad Juárez',
    'CLT':'Charlotte',
    'CME':'Ciudad Del Carmen',
    'CTM':'Chetumal',
    'CUN':'Cancún',
    'CUU':'Chihuahua',
    'CZM':'Cozumel',
    'DFW':'Dallas',
    'GDL':'Guadalajara',
    'GUA':'Ciudad de Guatemala',
    'HAV':'La Habana',
    'HMO':'Hermosillo',
    'HUX':'Huatulco',
    'IAH':'Houston',
    'JFK':'Nueva York',
    'LAX':'Los Ángeles',
    'LIM':'Lima',
    'MAD':'Madrid',
    'MEX':'Ciudad de México',
    'MIA':'Miami',
    'MID':'Merida',
    'MTY':'Monterrey',
    'MZT':'Mazatlan',
    'OAX':'Oaxaca',
    'ORD':'Chicago',
    'PBC':'Puebla',
    'PHL':'Filadelfia',
    'PHX':'Phoenix',
    'PVR':'Puerto Vallarta',
    'PXM':'Puerto Escondido',
    'QRO':'Querétaro',
    'SCL':'Santiago de Chile',
    'SLP':'San Luis Potosí',
    'TAM':'Tampico',
    'TIJ':'Tijuana',
    'TLC':'Toluca',
    'TRC':'Coahuila',
    'VER':'Veracruz',
    'VSA':'Villahermosa',
    'YVR':'Vancouver',
    'YYZ':'Toronto',
    'ZCL':'Zacatecas',
    'ZIH':'Ixtapa/Zihuatenejo',
}

def read_csv(csv_file):
    try:
        data = open(csv_file)
        data_location = data.readlines()
        data_location.pop(0)
        data.close
        return data_location
    except FileNotFoundError:
        print("File ", csv_file, " not found!")
        exit()

def create_location_list(data_location):
    for line_string in data_location:  
        line = line_string.strip().split(',')
        if not line[1] in iata_list:
            location_list.append([line[1], iata_cities[line[1]], line[3], line[4]])
            iata_list.append(line[1])
        if not line[2] in iata_list:
            location_list.append([line[2], iata_cities[line[2]], line[5], line[6]])
            iata_list.append(line[2])
    location_list.sort()
    return location_list

def create_iata_file(pklfile):
    data_location = read_csv('src/app/dataset2.csv')
    location_list = create_location_list(data_location)

    print("####### Creating file '", pklfile, "' #######")
    print()

    with open(pklfile, 'wb') as file_out:
        pickle.dump(location_list, file_out)
        
    print("####### File '", pklfile, "' created #######")
    print()  






