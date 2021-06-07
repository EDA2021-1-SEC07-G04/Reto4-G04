"""
 * Copyright 2020, Departamento de sistemas y Computación, Universidad
 * de Los Andes
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
import sys
import controller
from DISClib.ADT import list as lt
assert cf


"""
La vista se encarga de la interacción con el usuario
Presenta el menu de opciones y por cada seleccion
se hace la solicitud al controlador para ejecutar la
operación solicitada
"""

def printMenu():
    print("Bienvenido")
    print("1- Cargar información en el catálogo")
    print("2- Cantidad de clústeres y si dos landing points pertenecen al mismo. ")
    print("3- Landing points que sirven como punto de interconexión a más cables en la red. ")
    print("4- Ruta mínima para enviar información entre dos países. ")
    print("5- Red de expansión mínima en cuanto a distancia . ")
    print("6- Lista de países que podrían verse afectados al producirse una caída en el proceso de comunicación. ")

catalog = None

"""
Menu principal
"""
while True:
    printMenu()
    inputs = input('Seleccione una opción para continuar\n')
    if int(inputs[0]) == 1:
        print("Cargando información de los archivos ....")
        catalog = controller.startCatalog()
        controller.startData(catalog)
        numedges = controller.totalConnections(catalog)
        numvertex = controller.totalLPs(catalog)   
        numcount = controller.totalCountries(catalog) 
        firstlp = controller.getFirstLP(catalog)    
        print('Numero de landing points: ' + str(numvertex))
        print('Numero de conexiones: ' + str(numedges))
        print('El primer landing point y su info es: '+str(firstlp[0])+', '+str(firstlp[1])+', '+str(firstlp[2])+', '+str(firstlp[3]))
        print("\n")

    elif int(inputs[0]) == 2:
        v1 = input("Escriba el nombre del primer landing point: ")
        v2 = input("Escriba el nombre del segundo landing point: ")
        print("Cargando Requerimiento 1 .... ")
        answer = controller.ClusterCheck(catalog, v1, v2)
        print(" Numero de componentes conectados: "+str(answer[0]))
        print("Los vértices están conectados? "+str(answer[1]))
        print("\n")

    elif int(inputs[0]) == 3:
        print("Cargando Requerimiento 2 .... ")
        answer = controller.MostConnectionLPs(catalog)
        print("Los landing points con más conexiones a cables son: ")
        for ver in answer[0]:
            nombre = lt.getElement(ver, 1)
            pais = lt.getElement(ver, 2)
            lp_id = lt.getElement(ver, 3)
            print("--- "+nombre+", "+pais+", "+lp_id)
        print("Su número total de conexiones fue: "+str(answer[1]))
        print("\n")

    elif int(inputs[0]) == 4:
        pais1 = input("Seleccione el primer país: ")
        pais2 = input("Seleccione el segundo país: ")
        print("Cargando Requerimiento 3 .... ")
        answer = controller.minDistanceAB(catalog, pais1, pais2)
        print("La distancia total de la ruta es: "+str(answer))

        print("\n")

    elif int(inputs[0]) == 5:
        print("Cargando Requerimiento 4 .... ")
        answer = controller.expansionMin(catalog)
        print("El numero total de nodos conectados en al expansión mínima es: "+str(answer[0]))
        print("El costo total de la red de expansión mínima es: "+str(answer[1]))
        print("\n")

    elif int(inputs[0]) == 6:
        lp = input("Seleccione el nombre del landing point: ")
        print("Cargando Requerimiento 5 .... ")
        answer = controller.affectedLPs(catalog, lp)
        print("Numero de paises afectados: "+str(answer[0]))
        print("Lista de paises:")
        for x in answer[1]:
            print(x)
        print("\n")


    else:
        sys.exit(0)
sys.exit(0)
