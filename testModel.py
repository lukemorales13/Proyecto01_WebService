import unittest

import requests



class TestModel(unittest.TestCase):

    @unittest.skip("Se implementará después, menor prioridad en tanto se use exclusivamente el dataset dado")
    def test_validLine(self):
        
        """
        Prueba el procesamiento de las entradas (tickets).
        Revisa si el programa procesa correctamente las entradas con formato
        adecuado y si omite las entradas no válidas.

        La función [nombre] debe hacer un request si el ticket es
        válido, u omitir la línea presente para saltar a la siguiente línea, de
        lo contrario.
        """

        """
        self.assertTrue(procesa_ticket(None) == None)
        self.assertTrue(procesa_ticket("") == None)
        ticket = "C3NZsz5xBt82F4NJ	GDL	MEX	20.5218	-103.311
	19.4363	-99.0721"
        self.assertTrue(procesa_ticket(ticket) == None)
        """
        pass

        
    def test_readLine(self):

        """
        Prueba el procesamiento de tickets.
        Revisa si el programa genera correctamente los diccionarios del caché y
        los tickets.

        La función readData() debe guardar los números de ticket en tickets y
        los códigos IATA nuevos en el caché, no debe haber duplicados en caché.
        """

        #self.assertEquals(cache, tickets)
        ticket1 = "ejcwGA8AcLcWQ72g	GDL	MEX	20.5218	-103.311	19.4363	-99.0721"
        ticket2 = "nB6WtNW8vKrWHzyC	GDL	MEX	20.5218	-103.311	19.4363	-99.0721"
        data_list_test = [ticket1, ticket2]
        tickets_test = {
            "ejcwGA8AcLcWQ72g" : ["GDL", "MEX"],
            "nB6WtNW8vKrWHzyC" : ["GDL", "MEX"]
            }
        IATA_keys = ['GDL', 'MEX']
        returnedTickets, returnedCache = readLine(data_list_test)
        self.assertFalse(returnedTickets == None)
        self.assertFalse(returnedCache == None)
        self.assertEquals(returnedTickets, tickets_test)
        self.assertEquals(returnedCache.keys(), IATA_keys)

    


if __name__ == '__main__':
    unittest.main()
