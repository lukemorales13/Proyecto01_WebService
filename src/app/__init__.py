
from flask import Flask, jsonify
from flask import request

from levenshtein import city_search, iata_search, massive_search #para metodos https
#-------------------------------------------------------------------------------------------------------
#-------------------------------------------------------------------------------------------------------
app = Flask(__name__)

###----------------------------------------------------------------------inicio de rutas------------------------------------------------------------------------------------###
# Ruta para obtener datos meteorológicos
@app.route('/get_weather', methods=['GET'])
def get_weather():
    search_term = request.args.get('search')

    # Intenta buscar por IATA code
    iata_results = iata_search(search_term)
    if iata_results:
        return jsonify({'weather1': iata_results[0]})

    # Si no se encontraron resultados por IATA code, buscar por nombre de ciudad
    city_results = city_search(search_term)
    if city_results:
        return jsonify({'weather1': city_results[0]})

    # Si no se encontraron resultados por nombre de ciudad, realizar una búsqueda masiva
    massive_results = massive_search(search_term)
    if massive_results:
        return jsonify({'weather1': massive_results[0]})

    # Si no se encontraron resultados, devolver un mensaje de error
    return jsonify({'error': 'No se encontraron datos para la búsqueda.'}), 404
###----------------------------------------------------------------------fin de rutas------------------------------------------------------------------------------------###


def main():
    app.run(host='0.0.0.0',port=5001,debug=False,)
        
if __name__ == '__main__':
    main()


