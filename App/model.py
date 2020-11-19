"""Copyright 2020, Departamento de sistemas y Computación.

Universidad de Los Andes

Desarrolado para el curso ISIS1225 - Estructuras de Datos y Algoritmos

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.
Contribución de:

Dario Correal.
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
    """Función de crear un TAD analizador.

    Crea un analizador (diccionario) con las siguientes llaves:
    'grafo': Contiene el grafo de id de estaciones y conexiones entre ellas.
    'estaciones': Contiene una tabla de hash con las estaciones y todos sus datos.
    """
    analizador = {'grafo': crear_grafo(True,15),
                  'estaciones': crear_mapa()}
    return analizador

def crear_grafo(directed,size):
    """Crea un grafo vacío."""
    return gr.newGraph(datastructure='ADJ_LIST',directed=directed,size=size,comparefunction=comparar_estaciones)

def crear_mapa(numelements=157,loadfactor=2,maptype='CHAINING'):
    """Crea un mapa vacío."""
    return m.newMap(numelements=numelements,maptype=maptype,loadfactor=loadfactor,comparefunction=comparar_estaciones)

def crear_lista(listtype='SINGLE_LINKED'):
    """Crea una lista vacía."""
    return lt.newList(datastructure=listtype,cmpfunction=comparar_estaciones)

# -----------------------------------------------------
#                       API
# -----------------------------------------------------

# Funciones para agregar informacion al grafo

def insertar_estacion(grafo,mapa,id_estacion,datos_estacion):
    """Inserta una estación en el analizador."""
    m.put(mapa,id_estacion,datos_estacion)
    gr.insertVertex(grafo,id_estacion)

def crear_camino(grafo,estacion1,estacion2,tiempo):
    """Crea un camino entre 2 estaciones con tiempo como peso.

    El peso es una lista de la forma: [Total de tiempo, cantidad de viajes realziados]
    """
    arco = gr.getEdge(grafo,estacion1,estacion2)
    if arco is None:
        gr.addEdge(grafo,estacion1,estacion2,[tiempo,1])
        return 1
    else:
        arco['weight'][0]  += tiempo
        arco['weight'][1]  += 1
        return 0

def promediar_pesos(grafo):
    """Función que promedia cada uno de los pesos de cada arco en el grafo."""
    iterador = it.newIterator(gr.edges(grafo))
    while it.hasNext(iterador):
        arco = it.next(iterador)
        arco['weight'] = round(arco['weight'][0]/arco['weight'][1],3)

# ==============================
# Funciones de consulta
# ==============================

def existe_estacion(mapa,estacion):
    """Función que retorna si existe una estación."""
    return m.contains(mapa,estacion)

def lista_estaciones(grafo):
    """Retorna una lista con todas las ID de las estaciones del grafo."""
    return gr.vertices(grafo)

def estructura_Kosaraju(grafo):
    """Retorna una estructura con el resultado del algoritmo de Kosaraju."""
    return scc.KosarajuSCC(grafo)

def numero_componentes_conectados(kosaraju):
    """Retorna el número de componentes conectados en un grafo."""
    return scc.connectedComponents(kosaraju)

def encontrar_clusteres(kosaraju, estacion1, estacion2):
    """Retorna True si dos estaciones se encuentran en el mismo cluster."""
    return scc.stronglyConnected(kosaraju, estacion1, estacion2)

def estructura_Dijkstra(graph, source):
    """Retron un nuevo grafo vacío utilizado en el algoritmo de Dijkstra"""
    return djk.Dijkstra(graph, source)

def camino_vertice_a_vertice_dijstra(search, vertex):
    """Retorna una pila con el camino entre source y vertex"""
    return djk.pathTo(search, vertex)

def entradas_estaciones(analizador,estacion):
    return m.get(analizador['estaciones'],estacion)['values']['llegadas']

def peso_estacion_estacion(analizador,estacion1,estacion2):
    return gr.getEdge(analizador,estacion1,estacion2)
    
# ==============================  
# Funciones Helper
# ==============================

# ==============================
# Funciones de Comparacion
# ==============================

def comparar_estaciones(el1,el2):
    """Compara las ID de 2 estaciones."""
    if el1 > el2['key']:
        return 1
    elif el1 == el2['key']:
        return 0
    return -1