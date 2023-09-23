import unittest
import requests
import sys
import time

from methods import validLine
from methods import readData


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



if __name__ == '__main__':
    unittest.main()
