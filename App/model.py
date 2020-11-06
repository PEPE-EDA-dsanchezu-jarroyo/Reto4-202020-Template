"""
 * Copyright 2020, Departamento de sistemas y Computación
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
 * along with this program.  If not, see <http://www.gnu.org/licenses/>.
 * Contribución de:
 *
 * Dario Correal
 *
 """
import config
from DISClib.ADT.graph import gr
from DISClib.ADT import map as m
from DISClib.ADT import list as lt
from DISClib.DataStructures import listiterator as it
from DISClib.Algorithms.Graphs import scc
from DISClib.Algorithms.Graphs import dijsktra as djk
from DISClib.Utils import error as error
assert config

"""
En este archivo definimos los TADs que vamos a usar y las operaciones
de creacion y consulta sobre las estructuras de datos.
"""

def crear_analizador():
    analizador = {'grafo': crear_grafo(True,15),
                  'estaciones': crear_mapa()}
    return analizador

def crear_grafo(directed,size):
    """
    Crea un grafo vacío
    """
    return gr.newGraph(datastructure='ADJ_LIST',directed=directed,size=size,comparefunction=comparar_estaciones)

def crear_mapa(numelements=157,loadfactor=2,maptype='CHAINING'):
    """
    Crea un mapa vacío
    """
    return m.newMap(numelements=numelements,maptype=maptype,loadfactor=loadfactor,comparefunction=comparar_estaciones)

def crear_lista(listtype='SINGLE_LINKED'):
    """
    Crea una lista vacía
    """
    return lt.newList(datastructure=listtype,cmpfunction=comparar_estaciones)

# -----------------------------------------------------
#                       API
# -----------------------------------------------------

# Funciones para agregar informacion al grafo

def insertar_estacion(grafo,mapa,id_estacion,datos_estacion):       #SI ESTÁ MUY DEMORADO LO REVISAMOS
    """
    Inserta una estación en el analizador
    """
    m.put(mapa,id_estacion,datos_estacion)
    gr.insertVertex(grafo,id_estacion)

def crear_camino(grafo,estacion1,estacion2,tiempo):
    """
    Crea un camino entre 2 estaciones con tiempo como peso.
    El peso es una lista de la forma: [Total de tiempo, cantidad de viajes realziados]
    """
    arco = gr.getEdge(grafo,estacion1,estacion2)
    if arco is None:
        gr.addEdge(grafo,estacion1,estacion2,[tiempo,1])
    else:
        arco['weight'][0]  += tiempo
        arco['weight'][1]  += 1

def promediar_pesos(grafo):
    """
    Se promedia cada uno de los pesos de cada arco en el grafo
    """
    iterador = it.newIterator(gr.edges(grafo))
    while it.hasNext(iterador):
        arco = it.next(iterador)
        arco['weight'] = round(arco['weight'][0]/arco['weight'][1],3)

# ==============================
# Funciones de consulta
# ==============================

def existe_estacion(mapa,estacion):
    return m.contains(mapa,estacion)

def lista_estaciones(grafo):
    return gr.vertices(grafo)


# ==============================
# Funciones Helper
# ==============================

# ==============================
# Funciones de Comparacion
# ==============================

def comparar_estaciones(el1,el2):
    """
    Compara los nombres de 2 estaciones
    """
    if el1 > el2['key']:
        return 1
    elif el1 == el2['key']:
        return 0
    return -1