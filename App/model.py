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
import math
from DISClib.ADT.graph import gr
from DISClib.ADT import map as m
from DISClib.ADT import list as lt
from DISClib.ADT import stack as stk
from DISClib.DataStructures import listiterator as it
from DISClib.Algorithms.Graphs import scc
from DISClib.Algorithms.Graphs import dijsktra as djk
from DISClib.Utils import error as error
assert config
from DISClib.ADT import minpq as mpq

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
                  'estaciones': crear_mapa(),
                  'lista_estaciones': None,
                  'mapa_rango_edades': crear_mapa()}
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

def insertar_estacion(analizador, id_estacion, datos_estacion):
    """Inserta una estación en el analizador."""
    m.put(analizador['estaciones'],id_estacion,datos_estacion)
    gr.insertVertex(analizador['grafo'],id_estacion)

def actualizar_estacion(mapa, estacion, nueva_salida=None, nueva_llegada=None):
    datos_estacion = m.get(mapa, estacion)['value']
    if nueva_salida is not None:
        lt.addLast(datos_estacion['salidas'],nueva_salida[0])
        datos_estacion['rangos_edad']['salidas'][nueva_salida[1]] += 1
    
    if nueva_llegada is not None:
        lt.addLast(datos_estacion['llegadas'],nueva_llegada[0])
        datos_estacion['rangos_edad']['llegadas'][nueva_llegada[1]] += 1


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

def configurar_arcos(analizador):
    """Función que promedia cada uno de los pesos de cada arco en el grafo."""
    iterador = it.newIterator(gr.edges(analizador['grafo']))
    while it.hasNext(iterador):
        arco = it.next(iterador)
        vertice_a = m.get(analizador['estaciones'],arco['vertexA'])
        vertice_b = m.get(analizador['estaciones'],arco['vertexB'])
        lt.addLast(vertice_a['value']['salidas'],vertice_a)
        lt.addLast(vertice_b['value']['llegadas'],vertice_b)
        arco['weight'] = round(arco['weight'][0]/arco['weight'][1],3)
    analizador['lista_estaciones'] = m.valueSet(analizador['estaciones'])

# ==============================
# Funciones de consulta
# ==============================

def existe_estacion(mapa,estacion):
    """Función que retorna si existe una estación."""
    return m.contains(mapa,estacion)

def lista_estaciones(grafo):
    """Retorna una lista con todas las ID de las estaciones del grafo."""
    return gr.vertices(grafo)

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

def datos_estacion(analizador, estacion):
    return m.get(analizador['estaciones'], estacion)

# ==============================  
def encontrar_tops_3(analizador):
    """Requerimiento 3.

    Crea tres colas de prioridad y organiza los datos salida, llegada y
    tristeza (suma de salidas y llegadas) de cada una de las estaciones.

    Posteriormente obtiene los 3 elementos con más prioridad y los retorna
    """
    iterador = it.newIterator(analizador['lista_estaciones'])
    max_salidas = mpq.newMinPQ(comparacion_ranking)
    max_llegadas = mpq.newMinPQ(comparacion_ranking)
    mas_tristes = mpq.newMinPQ(comparacion_ranking_invertido)
    while it.hasNext(iterador):
        estacion = it.next(iterador)
        cantidad_salidas = calcular_cantidad_viajes(estacion['rangos_edad']['salidas'])
        cantidad_llegadas = calcular_cantidad_viajes(estacion['rangos_edad']['llegadas'])
        cantidad_tristes = cantidad_salidas + cantidad_llegadas
        mpq.insert(max_salidas, (cantidad_salidas, estacion['nombre']))
        mpq.insert(max_llegadas, (cantidad_llegadas, estacion['nombre']))
        mpq.insert(mas_tristes, (cantidad_tristes, estacion['nombre']))
    
    max_salidas_lst = []
    max_llegadas_lst = []
    mas_tristes_lst = []

    for i in range(3):
        max_salidas_lst.append(mpq.delMin(max_salidas))
        max_llegadas_lst.append(mpq.delMin(max_llegadas))
        mas_tristes_lst.append(mpq.delMin(mas_tristes))
    
    return (max_salidas_lst, max_llegadas_lst, mas_tristes_lst)

def encontrar_max_estaciones_rango_edad(analizador, indice_rango_edad):
    """Requerimiento 5."""
    iterador = it.newIterator(analizador['lista_estaciones'])
    max_salidas = [0, 0, None]
    max_llegadas = [0, 0, None]
    while it.hasNext(iterador):
        estacion = it.next(iterador)
        if estacion['rangos_edad']['salidas'][indice_rango_edad] > max_salidas[0]:
            max_salidas[0] = estacion['rangos_edad']['salidas'][indice_rango_edad]
            max_salidas[1] = estacion['id']
            max_salidas[2] = estacion['nombre']

        if estacion['rangos_edad']['llegadas'][indice_rango_edad] > max_llegadas[0]:
            max_llegadas[0] = estacion['rangos_edad']['llegadas'][indice_rango_edad]
            max_llegadas[1] = estacion['id']
            max_llegadas[2] = estacion['nombre']

    return max_salidas, max_llegadas

def encontrar_estaciones_lat_lon(analizador, lat_inicial, lon_inicial, lat_final, lon_final):
    """Requerimiento 6.

    Retorna la estación más cercana a las cordenadas lat, lon.
    """
    iterador = it.newIterator(analizador['lista_estaciones'])
    estacion_inicial = (math.inf, None)
    estacion_final = (math.inf, None)
    while it.hasNext(iterador):
        datos_estacion = it.next(iterador)
        distancia_estacion_inicial = distancia_lat_lon(lon_inicial, lat_inicial, datos_estacion['longitud'],  datos_estacion['latitud'])
        distancia_estacion_final = distancia_lat_lon(lon_final, lat_final, datos_estacion['longitud'],  datos_estacion['latitud'])
        if distancia_estacion_inicial < estacion_inicial[0]:
            estacion_inicial = (distancia_estacion_inicial, datos_estacion)
        elif distancia_estacion_final < estacion_final[0]:
            estacion_final = (distancia_estacion_final, datos_estacion)
    distancia_total = distancia_lat_lon(estacion_inicial[1]['longitud'], estacion_inicial[1]['latitud'], estacion_final[1]['longitud'], estacion_final[1]['latitud'])
    return (estacion_inicial[1], estacion_final[1]), distancia_total

def datos_dijkstra(analizador, estacion_inicio, estacion_final):
    """Retorna el tiempo necesario para llegar de estacion_inicio a estacion_final."""
    estructura_dijkstra = djk.Dijkstra(analizador['grafo'], estacion_inicio)
    caminos = djk.pathTo(estructura_dijkstra, estacion_final)
    lista_caminos = crear_lista()
    if caminos is not None:
        for i in range(stk.size(caminos)):
            lt.addLast(lista_caminos, stk.pop(caminos))
    return djk.distTo(estructura_dijkstra, estacion_final), lista_caminos

# ==============================
# Funciones Helper
# ==============================

def estructura_Kosaraju(grafo):
    """Retorna una estructura con el resultado del algoritmo de Kosaraju."""
    return scc.KosarajuSCC(grafo)

def distancia_lat_lon(lon1,lat1,lon2,lat2):
    """Retorna la distancia entre 2 puntos."""
    delta_lon = lon2-lon1
    delta_lat = lat2-lat1

    alpha = math.sin(delta_lat/2)**2 + math.cos(lat1) * math.cos(lat2) * math.sin(delta_lon/2)**2

    distancia = 2*math.asin(math.sqrt(alpha)) * 6371

    return distancia

def calcular_cantidad_viajes(lista_rangos):
    total = 0
    for i in lista_rangos:
        total += i
    return total

# ==============================
# Funciones de Comparacion
# ==============================

def comparar_estaciones(el1, el2):
    """Compara las ID de 2 estaciones."""
    if el1 > el2['key']:
        return 1
    elif el1 == el2['key']:
        return 0
    return -1

def comparacion_ranking(el1, el2):
    """Función para comparar los datos en una MinPQ."""
    if el1[0] < el2[0]:
        return 1
    elif el1 == el2[0]:
        return 0
    return -1

def comparacion_ranking_invertido(el1, el2):
    """Función para comparar los datos en una MaxPQ."""
    if el1[0] > el2[0]:
        return 1
    elif el1 == el2[0]:
        return 0
    return -1
