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
from DISClib.Algorithms.Graphs import scc 
from DISClib.Algorithms.Graphs import bellmanford as bf
from DISClib.Algorithms.Graphs import prim as prm
from DISClib.Algorithms.Graphs import dijsktra as dj
from DISClib.ADT.graph import gr
from math import radians, cos, sin, asin, sqrt
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
 macrostructure['lp-names']=mp.newMap(numelements=1279,
                                     maptype='PROBING',
                                     comparefunction=None)
 macrostructure['cables']=mp.newMap(numelements=1279,
                                     maptype='PROBING',
                                     comparefunction=compareLPs)
 

 return macrostructure
# Funciones para agregar informacion al catalogo

def addLandingPoint(macrostructure, lp):
    entry =  mp.get(macrostructure['lp'], (lp['landing_point_id']))
    if entry is None:
        lpdata = lt.newList(datastructure="ARRAY_LIST", cmpfunction=None)
        lt.addLast(lpdata, lp['id'])
        lt.addLast(lpdata, lp['name'])
        lt.addLast(lpdata, lp['latitude'])
        lt.addLast(lpdata, lp['longitude'])
        mp.put(macrostructure['lp'], (lp['landing_point_id']), lpdata)
    name_country = lp['name'].split(", ")
    simple_name = (name_country)[0]
    country_name = (name_country)[-1]
    entry2 =  mp.get(macrostructure['lp'], simple_name)
    if entry2 is None:
        lpdata2 = lt.newList(datastructure="ARRAY_LIST", cmpfunction=None)
        lt.addLast(lpdata2, country_name)
        lt.addLast(lpdata2, lp['landing_point_id'])
        lt.addLast(lpdata2, lp['id'])
        lt.addLast(lpdata2, lp['latitude'])
        lt.addLast(lpdata2, lp['longitude'])
        mp.put(macrostructure['lp-names'], simple_name, lpdata2)

def addLandingConnection(macrostructure, connection, check, lonC, latC):
    if check == 0:
        origin = (connection['\ufefforigin'])
        destination = (connection['destination'])
        olat = float(lt.getElement((mp.get(macrostructure['lp'], origin)['value']), 3))
        olong = float(lt.getElement((mp.get(macrostructure['lp'], origin)['value']), 4))
        dlat = float(lt.getElement((mp.get(macrostructure['lp'], destination)['value']), 3))
        dlong = float(lt.getElement((mp.get(macrostructure['lp'], destination)['value']), 4))
        distance = round(haversine(olat, olong, dlat, dlong), 3)    
        distance = abs(distance)
        addLanding(macrostructure, origin)
        addLanding(macrostructure, destination)
        addConnection(macrostructure, origin, destination, distance, 0)
    if check == 1:
        origin = (connection['origin'])
        destination = (connection['destination'])
        olat = float(lonC)
        olong = float(latC)
        dlat = float(lt.getElement((mp.get(macrostructure['lp'], destination)['value']), 3))
        dlong = float(lt.getElement((mp.get(macrostructure['lp'], destination)['value']), 4))
        distance = round(haversine(olong, olat, dlong, dlat), 3)
        distance = abs(distance)
        addLanding(macrostructure, origin)
        addLanding(macrostructure, destination)
        addConnection(macrostructure, origin, destination, distance, 1)


def addCountry(macrostructure,country):
    entry = mp.get(macrostructure['countries'], country['CountryName'])
    if entry is None:
        lstroutes = lt.newList(datastructure="ARRAY_LIST", cmpfunction=None)
        lt.addLast(lstroutes, country['CapitalName'])
        lt.addLast(lstroutes, country['CapitalLatitude'])
        lt.addLast(lstroutes, country['CapitalLongitude'])
        lt.addLast(lstroutes, country['CountryCode'])
        lt.addLast(lstroutes, country['ContinentName'])
        lt.addLast(lstroutes, country['Population'])
        lt.addLast(lstroutes, country['Internet users'])
        mp.put(macrostructure['countries'], country['CountryName'], lstroutes)
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

def addConnection(macrostructure, origin, destination, distance, check):
    """
    Adiciona un arco entre dos estaciones
    """
    if check == 0:
        edge = gr.getEdge(macrostructure['connections'], origin, destination)
        if edge is None:
            gr.addEdge(macrostructure['connections'], origin, destination, distance)
    if check == 1:
        outedge = gr.getEdge(macrostructure['connections'], origin, destination)
        if outedge is None:
            gr.addEdge(macrostructure['connections'], origin, destination, distance)
        inedge = gr.getEdge(macrostructure['connections'], destination, origin)
        if inedge is None:
            gr.addEdge(macrostructure['connections'], destination, origin, distance)

    return macrostructure

def addCapital(macrostructure, capital, country):
    connection = {}
    if not gr.containsVertex(macrostructure['connections'], lt.getElement(capital, 1)):
        gr.insertVertex(macrostructure['connections'], lt.getElement(capital, 1))
        connection['origin'] = lt.getElement(capital, 1)
    LPs = mp.valueSet(macrostructure['lp-names'])   
    for index in range(0, lt.size(LPs)):
        info = lt.getElement(LPs, int(index))
        if lt.getElement(info, 1) == country:
            connection['destination'] = lt.getElement(info, 2)
            addLandingConnection(macrostructure, connection, 1, lt.getElement(capital, 2), lt.getElement(capital, 3))
    
    

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


# Funciones de consulta
def ClusterCheck(macrostructure, vertex1, vertex2):
    connected = scc.KosarajuSCC(macrostructure['connections'])
    lp1 = lt.getElement((mp.get(macrostructure['lp-names'], vertex1))['value'], 1)
    lp2 = lt.getElement((mp.get(macrostructure['lp-names'], vertex2))['value'], 1)
    pertains = scc.stronglyConnected(macrostructure['connections'], lp1, lp2)
    #pertains = None
    ans = (int(connected['components']), pertains)
    return ans

def MostConnectionLPs(macrostructure):
    final = []
    answers = []
    vertices = gr.vertices(macrostructure['connections'])
    most_connections = 0
    for index in range(0, lt.size(vertices)):
        vertex = lt.getElement(vertices, int(index))
        connections = gr.degree(macrostructure['connections'], vertex)
        if connections == most_connections:
            answers.append(vertex)
        if connections > most_connections:
            answers = []
            most_connections = connections
            answers.append(vertex)
    for ver in answers:
        info = lt.newList("ARRAY_LIST")
        datos = mp.get(macrostructure['lp'], ver)['value']
        nom_pais = (lt.getElement(datos, 2)).split(', ')
        nombre = nom_pais[0]
        pais = nom_pais[1]
        lt.addLast(info, nombre)
        lt.addLast(info, pais)
        lt.addLast(info, ver)
        final.append(info)
    return final, most_connections

def minDistanceAB(macrostructure, pais1, pais2):
    list_capital1 = lt.newList('ARRAY_LIST')
    list_capital2 = lt.newList('ARRAY_LIST')
    capital1 = lt.getElement(mp.get(macrostructure['countries'], pais1)['value'], 1)
    capital2 = lt.getElement(mp.get(macrostructure['countries'], pais2)['value'], 1)
    latC1 = lt.getElement(mp.get(macrostructure['countries'], pais1)['value'], 2)
    lonC1 = lt.getElement(mp.get(macrostructure['countries'], pais1)['value'], 3)
    latC2 = lt.getElement(mp.get(macrostructure['countries'], pais2)['value'], 2)
    lonC2 = lt.getElement(mp.get(macrostructure['countries'], pais2)['value'], 3)
    lt.addLast(list_capital1, capital1)
    lt.addLast(list_capital1, latC1)
    lt.addLast(list_capital1, lonC1)
    lt.addLast(list_capital2, capital2)
    lt.addLast(list_capital2, latC2)
    lt.addLast(list_capital2, lonC2)
    if mp.get(macrostructure['lp-names'], capital1) == None:
        addCapital(macrostructure, list_capital1, pais1)
    else:
        capital1=lt.getElement(mp.get(macrostructure['lp-names'], capital1)['value'], 2)
    if mp.get(macrostructure['lp-names'], capital2) == None:
        addCapital(macrostructure, list_capital2, pais2)
        destino = capital2
    else:
        destino = lt.getElement(mp.get(macrostructure['lp-names'], capital2)['value'], 2)
    search = bf.BellmanFord(macrostructure['connections'], capital1)
    distancia = bf.distTo(search, destino)
    search2 = dj.Dijkstra(macrostructure['connections'], capital1)
    camino2 = dj.pathTo(search2, destino)
    print("La ruta desde el pais A al pais B es: ")
    for index in range(1, int(lt.size(camino2))+1):
        data = lt.getElement(camino2, index)
        print(data)
    return distancia

def expansionMin(macrostructure):
    mst = prm.PrimMST(macrostructure['connections'])
    camino = prm.edgesMST(macrostructure['connections'], mst)
    numero = mp.size(camino['edgeTo'])
    peso_total = 0
    keys = mp.keySet(camino['distTo'])
    for index in range(1, int(lt.size(keys))+1):
        data = lt.getElement(keys, index)
        peso = mp.get(camino['distTo'], data)['value']
        peso_total += int(peso)

    return numero, peso_total

def affectedLPs(macrostructure, lp):
    answer = []
    affected = []
    vertex = lt.getElement((mp.get(macrostructure['lp-names'], lp))['value'], 2)
    x = gr.adjacents(macrostructure['connections'], vertex)
    y = gr.degree(macrostructure['connections'], vertex)
    answer.append(y)
    for index in range(1, int(lt.size(x))+1):
        data = lt.getElement(x, index)
        pais = lt.getElement(mp.get(macrostructure['lp'], data)['value'], 2)
        edge = gr.getEdge(macrostructure['connections'], vertex, data)
        print(edge)
        affected.append(pais)
    answer.append(affected)
    return answer




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



def haversine(lon1, lat1, lon2, lat2):

    lon1, lat1, lon2, lat2 = map(radians, [lon1, lat1, lon2, lat2])

    # haversine formula 
    dlon = lon2 - lon1 
    dlat = lat2 - lat1 
    a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
    c = 2 * asin(sqrt(a)) 
    r = 6371 # Radius of earth in kilometers. Use 3956 for miles
    return c * r

# Funciones de ordenamiento
