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
 *
 * Contribuciones:
 *
 * Dario Correal - Version inicial
 """


from DISClib.DataStructures.arraylist import getElement
import config as cf
from DISClib.ADT import list as lt
from DISClib.ADT import map as mp
from DISClib.DataStructures import mapentry as me
from DISClib.Algorithms.Sorting import shellsort as sa
from DISClib.ADT.graph import gr
import math as m
assert cf

"""
Se define la estructura de un catálogo de videos. El catálogo tendrá dos listas, una para los videos, otra para las categorias de
los mismos.
"""

# Construccion de modelos
def NewMacrostructure():
 macrostructure={"connections":None, "countries":None,"lp":None, "cables":None}                         
         
 macrostructure['connections']=gr.newGraph(datastructure='ADJ_LIST',
                                              directed=True,
                                              size=3262,
                                              comparefunction=compareLPs)
 macrostructure['countries'] = mp.newMap(numelements=238,
                                     maptype='PROBING',
                                     comparefunction=None)
 macrostructure['lp']=mp.newMap(numelements=1279,
                                     maptype='PROBING',
                                     comparefunction=None)
 macrostructure['cables']=mp.newMap(numelements=1279,
                                     maptype='PROBING',
                                     comparefunction=compareLPs)
 

 return macrostructure
# Funciones para agregar informacion al catalogo

def addLandingPoint(macrostructure, lp):
    entry =  mp.get(macrostructure['lp'], int(lp['landing_point_id']))
    if entry is None:
        lpdata = lt.newList(cmpfunction=None)
        lt.addLast(lpdata, lp['id'])
        lt.addLast(lpdata, lp['name'])
        lt.addLast(lpdata, lp['latitude'])
        lt.addLast(lpdata, lp['longitude'])
        mp.put(macrostructure['lp'], int(lp['landing_point_id']), lpdata)


def addLandingConnection(macrostructure, connection):
    origin = int(connection['\ufefforigin'])
    destination = int(connection['destination'])
    olat = float(lt.getElement((mp.get(macrostructure['lp'], origin)['value']), 3))
    olong = float(lt.getElement((mp.get(macrostructure['lp'], origin)['value']), 4))
    dlat = float(lt.getElement((mp.get(macrostructure['lp'], destination)['value']), 3))
    dlong = float(lt.getElement((mp.get(macrostructure['lp'], destination)['value']), 4))
    distance = round(haversine(olat, olong, dlat, dlong), 3)
    distance = abs(distance)
    addLanding(macrostructure, origin)
    addLanding(macrostructure, destination)
    addConnection(macrostructure, origin, destination, distance)

def addCountry(macrostructure,country):
    entry = mp.get(macrostructure['countries'], country['CountryCode'])
    if entry is None:
        lstroutes = lt.newList(cmpfunction=None)
        lt.addLast(lstroutes, country['CountryName'])
        mp.put(macrostructure['countries'], country['CountryCode'], lstroutes)
    else:
        lstroutes = entry['value']
        info = country['CountryName']
        if not lt.isPresent(lstroutes, info):
            lt.addLast(lstroutes, info)
    return macrostructure
    
    
def addLanding(macrostructure, landing):
    """
    Adiciona una estación como un vertice del grafo
    """
    if not gr.containsVertex(macrostructure['connections'], landing):
        gr.insertVertex(macrostructure['connections'], landing)
    return macrostructure

def addConnection(macrostructure, origin, destination, distance):
    """
    Adiciona un arco entre dos estaciones
    """
    edge = gr.getEdge(macrostructure['connections'], origin, destination)
    if edge is None:
        gr.addEdge(macrostructure['connections'], origin, destination, distance)
    return macrostructure

def totalLPs(analyzer):
    return gr.numVertices(analyzer['connections'])


def totalConnections(analyzer):
    return gr.numEdges(analyzer['connections'])
    
def totalCountries(analyzer):
    return mp.size(analyzer['countries'])    

def getFirstLP(catalog):
    LPs = mp.valueSet(catalog['lp'])
    lp = lt.getElement(LPs, 1)
    ans = (lt.getElement(lp, 1), lt.getElement(lp, 2), lt.getElement(lp, 3), lt.getElement(lp, 4))
    return ans


#def AddConnection():

# Funciones para creacion de datos

# Funciones de consulta

# Funciones utilizadas para comparar elementos dentro de una lista
def compareLPs(stop, keyvaluestop):
    """
    Compara dos estaciones
    """
    stopcode = keyvaluestop['key']
    if (stop == stopcode):
        return 0
    elif (stop > stopcode):
        return 1
    else:
        return -1


def haversine(lat1, long1, lat2, long2):
    r = 6.371
    lat1, long1, lat2, long2 = map(m.radians, [lat1, long1, lat2, long2]) 
    distance = r *(m.acos(m.sin(lat1)*m.sin(lat2)+m.cos(lat1)*m.cos(lat2)*m.cos(long1-long2)))
    return distance

# Funciones de ordenamiento
