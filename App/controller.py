"""
 * Copyright 2020, Departamento de sistemas y Computación,
 * Universidad de Los Andes
 *
 *
 * Desarrolado para el curso ISIS1225 - Estructuras de Datos y Algoritmos
 *
 *
 * This program is free software: you can redistribute it and/or modify
 * it under the terms of the GNU General Public License as published by
 * the Free Software Foundation, either version 3 of the License, or
 * (at your option) any later version.
 *
 * This program is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU General Public License for more details.
 *
 * You should have received a copy of the GNU General Public License
 * along withthis program.  If not, see <http://www.gnu.org/licenses/>.
 """

import config as cf
import model
import csv


"""
El controlador se encarga de mediar entre la vista y el modelo.
"""

# Inicialización del Catálogo de libros
def startCatalog():
    """
    Llama la funcion de inicializacion del catalogo del modelo.
    """
    catalog = model.NewMacrostructure()
    return catalog

# Funciones para la carga de datos
def startData(catalog):
    """
    Carga los datos de los archivos y cargar los datos en la
    estructura de datos
    """

    #EJECUCIÓN DE CARGA
    loadLPs(catalog)
    loadConnections(catalog)
    loadCountries(catalog)
    #EJECUCIÓN DE CARGA
    
def loadLPs(catalog):
    filename = cf.data_dir + "landing_points.csv"
    input_file = csv.DictReader(open(filename, encoding="utf-8"),
                                delimiter=",")
    for lp in input_file:
        model.addLandingPoint(catalog, lp)                           


def loadConnections(catalog):
    filename = cf.data_dir + "connections.csv"
    input_file = csv.DictReader(open(filename, encoding="utf-8"),
                                delimiter=",")
    for connection in input_file:
        model.addLandingConnection(catalog, connection, 0, None, None)

    
def loadCountries(catalog):
    filename = cf.data_dir + "countries.csv"
    input_file = csv.DictReader(open(filename, encoding="utf-8"),
                                delimiter=",")
    for country in input_file:
        model.addCountry(catalog, country)

def totalLPs(analyzer):
    return model.totalLPs(analyzer)


def totalConnections(analyzer):
    return model.totalConnections(analyzer)    

def totalCountries(analyzer):
    return model.totalCountries(analyzer) 

def getFirstLP(catalog):
    return model.getFirstLP(catalog)      




# Funciones de ordenamiento

# Funciones de consulta sobre el catálogo

def ClusterCheck(catalog, v1, v2):
    return model.ClusterCheck(catalog, v1, v2)

def MostConnectionLPs(catalog):
    return model.MostConnectionLPs(catalog)

def minDistanceAB(catalog, pais1, pais2):
    return model.minDistanceAB(catalog, pais1, pais2)

def affectedLPs(catalog, lp):
    return model.affectedLPs(catalog, lp)

def expansionMin(catalog):
    return model.expansionMin(catalog)
