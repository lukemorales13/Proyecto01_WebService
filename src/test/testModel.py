import unittest
import requests
import sys
import time

import src.app.methods as methods
from src.app.methods import cache
from src.app.methods import tickets
from src.app.methods import coordinates
from src.app.methods import validLine
from src.app.methods import readData
from src.app.methods import searchWeatherWith_IATA
from src.app.methods import searchWeatherWith_ticket


class TestModel(unittest.TestCase):

    """
    Prueba el procesamiento de las entradas (tickets).
    Revisa si el programa procesa correctamente las entradas con formato
    adecuado y si omite regresar las entradas no válidas.
    """
    
    def test_validLine(self):
        
        """
        Si la línea no es válida, debería saltar a la línea siguiente y no
        regresar nada.
        Aún debo decidir si evaluar que no pase nada o evaluar que arroje
        una excepción, por lo mismo. Por el momento, dejo las pruebas sucias
        de esta función comentadas.
        """

        """
        ticket = ""
        with self.assertRaises(Exception):
            validLine(ticket)
        ticket = "a"
        with self.assertRaises(Exception):
            validLine(ticket)
        ticket = "aaaaaaaaaaaaaaaa,bbb,ccc,d,e,f,g"
        with self.assertRaises(Exception):
            validLine(ticket)
        ticket = "aaaaaaaaaaaaaaaa,1,2,3,4,5,6"
        with self.assertRaises(Exception):
            validLine(ticket)
        """
        #Si una línea es válida, la separa.
        
        ticket = "C3NZsz5xBt82F4NJ,GDL,MEX,20.5218,-103.311,19.4363,-99.0721"
        list = ["C3NZsz5xBt82F4NJ","GDL","MEX",20.5218,-103.311,19.4363,-99.0721]
        self.assertEqual(list, validLine(ticket))


    """
    Prueba el procesamiento de tickets.
    Revisa si el programa genera correctamente los diccionarios del caché y
    los tickets.

    La función readData() debe guardar los números de ticket en tickets y
    los códigos IATA nuevos en el caché, no debe haber duplicados en caché.
    """

    def test_readData(self):

        """
        Preparamos tickets válidos, viendo si se agregan correctamente al leer
        los datos y si no aparecen duplicados
        """
        
        ticket1 = "ejcwGA8AcLcWQ72g,GDL,MEX,20.5218,-103.311,19.4363,-99.0721"
        ticket2 = "nB6WtNW8vKrWHzyC,GDL,MEX,20.5218,-103.311,19.4363,-99.0721"
        data_list_test = [ticket1, ticket2]
        tickets_test = {
            "ejcwGA8AcLcWQ72g" : ["GDL", "MEX"],
            "nB6WtNW8vKrWHzyC" : ["GDL", "MEX"]
            }
        
        """
        Es posible que de un request previo a llamar readData y los de readData
        haya cambios, así que omitimos la descripción del clima y nos fijamos
        en las llaves.
        """
        
        IATA_keys = ['GDL', 'MEX']
        returnedCache, returnedTickets = readData(data_list_test)
        self.assertFalse(returnedTickets == None)
        self.assertFalse(returnedCache == None)
        self.assertEqual(returnedTickets, tickets_test)
        returnedKeys = list(returnedCache.keys())
        self.assertEqual(returnedKeys, IATA_keys)

    """
    Corrobora que el resultado de buscar por IATA en el caché sea el adecuado
    tanto si está o no está el código guardado.
    """

    def test_searchWeatherWith_IATA(self):

        methods.cache = {}
        iata = "MEX"
        self.assertEqual(searchWeatherWith_IATA(iata), "O.o")
        ticket1 = "ejcwGA8AcLcWQ72g,GDL,MEX,20.5218,-103.311,19.4363,-99.0721"
        ticketList = [ticket1]
        methods.cache, ticketDict = readData(ticketList)
        self.assertEqual(searchWeatherWith_IATA(iata), methods.cache[iata])

    """
    Corrobora que el resultado de buscar por número de ticket en el diccionario
    sea el adecuado tanto si está o no está el código guardado.
    """

    def test_searchWeatherWith_ticket(self):
        
        ticket1 = "ejcwGA8AcLcWQ72g,GDL,MEX,20.5218,-103.311,19.4363,-99.0721"
        num1 = "ejcwGA8AcLcWQ72g"
        methods.cache = {}
        methods.tickets = {}
        err = "Ticket not found.\nPlease check again the information."
        self.assertEqual(searchWeatherWith_ticket(num1), err)        
        ticketList = [ticket1]
        methods.cache, methods.tickets = readData(ticketList)
        self.assertFalse(searchWeatherWith_ticket(num1) == err)

    def searchWeatherWith_Coordinates(self):

        methods.coordinates = {}
        ticket1 = "ejcwGA8AcLcWQ72g,GDL,MEX,20.5218,-103.311,19.4363,-99.0721"
        ticketList = [ticket1]
        testCache, testTickets = readData(ticketList)
        weather = testCache['GDL']
        assertEquals(searchWeatherWith_Coordinates(20.5218,-103.311), weather)


if __name__ == '__main__':
    unittest.main()
