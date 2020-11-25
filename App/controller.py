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

Dario Correal
"""

import config as cf
from App import model
from DISClib.DataStructures import listiterator as it
from DISClib.ADT import list as lt
import csv
import os
import time
import math

"""
El controlador se encarga de mediar entre la vista y el modelo.
Existen algunas operaciones en las que se necesita invocar
el modelo varias veces o integrar varias de las respuestas
del modelo en una sola respuesta.  Esta responsabilidad
recae sobre el controlador.
"""

# ___________________________________________________
#  Inicializacion del catalogo
# ___________________________________________________


def inicializar_analizador():
    """Inicializa el analizador de rutas de bicicletas."""
    return model.crear_analizador()

# ___________________________________________________
#  Funciones para la carga de datos y almacenamiento
#  de datos en los modelos
# ___________________________________________________


def cargar_viajes(analizador):
    """Carga los viajes en el analizador.

    Se Carga en el analizador cada estación así como las distintas rutas entre ellas.
    Retorna la cantidad total de estaciones, de viajes y de caminos cargados.
    """
    total_estaciones = 0
    total_viajes = 0
    total_caminos = 0
    for archivo in os.listdir(cf.data_dir):
        if archivo.endswith('.csv'):
            ti = time.perf_counter()
            print('Cargando archivo: ' + archivo)
            estaciones_archivo, viajes_archivo, caminos_archivo = cargar_datos(analizador, archivo)
            total_estaciones += estaciones_archivo
            total_viajes += viajes_archivo
            total_caminos += caminos_archivo
            print("La cantidad de viajes presentes es:", total_viajes)
            print("La cantidad de estaciones presentes es:", total_estaciones)
            print("La cantidad de caminos presentes es:", total_caminos)
            print("La cantidad de componentes fuertemente conectados presentes es:", model.numero_componentes_conectados(model.estructura_Kosaraju(analizador['grafo'])))
            tf = time.perf_counter()
            print("Tiempo de ejecución:", round(tf-ti, 3), end='\n\n')
    model.configurar_arcos(analizador)
    return analizador, total_estaciones, total_viajes


def cargar_datos(analizador, archivo):
    """Carga los datos de un archivo.

    Abre el archivo y por cada línea revisa si la estación ya existe.
    Si no existe, agrega al grafo su ID y al mapa todos sus datos.
    """
    archivo_viajes = cf.data_dir + archivo
    datos = csv.DictReader(open(archivo_viajes, encoding='utf-8'),delimiter=',')
    total_estaciones = 0
    total_viajes = 0
    total_caminos = 0
    for viaje in datos:
        if not viaje['start station id'] == viaje['end station id']:

            if 2020-int(viaje['birth year']) in range(0,11):
                indice_rango = 0
            elif 2020-int(viaje['birth year']) in range(11,21):
                indice_rango = 1
            elif 2020-int(viaje['birth year']) in range(21,31):
                indice_rango = 2
            elif 2020-int(viaje['birth year']) in range(31,41):
                indice_rango = 3
            elif 2020-int(viaje['birth year']) in range(41,51):
                indice_rango = 4
            elif 2020-int(viaje['birth year']) in range(51,61):
                indice_rango = 5
            else:
                indice_rango = 6

            if not model.existe_estacion(analizador['estaciones'], int(viaje['start station id'])):
                total_estaciones += 1
                datos_estacion_salida = {'id': int(viaje['start station id']),
                                         'nombre': viaje['start station name'],
                                         'latitud': float(viaje['start station latitude']),
                                         'longitud': float(viaje['start station longitude']),
                                         'salidas': model.crear_lista(),
                                         'llegadas': model.crear_lista(),
                                         'rangos_edad': {'salidas': [0,0,0,0,0,0,0],
                                                        'llegadas': [0,0,0,0,0,0,0]}}
                model.insertar_estacion(analizador,datos_estacion_salida['id'], datos_estacion_salida)
                lt.addLast(datos_estacion_salida['salidas'], int(viaje['end station id']))
                datos_estacion_salida['rangos_edad']['salidas'][indice_rango] += 1
            else:
                model.actualizar_estacion(analizador['estaciones'], int(viaje['start station id']),nueva_salida=(int(viaje['end station id']), indice_rango))

            if not model.existe_estacion(analizador['estaciones'], int(viaje['end station id'])):
                total_estaciones += 1
                datos_estacion_llegada = {'id': int(viaje['end station id']),
                                         'nombre': viaje['end station name'],
                                         'latitud': float(viaje['end station latitude']),
                                         'longitud': float(viaje['end station longitude']),
                                         'salidas': model.crear_lista(),
                                         'llegadas': model.crear_lista(),
                                         'rangos_edad': {'salidas': [0,0,0,0,0,0,0],
                                                        'llegadas': [0,0,0,0,0,0,0]}}
                model.insertar_estacion(analizador,datos_estacion_llegada['id'], datos_estacion_llegada)       
                lt.addLast(datos_estacion_llegada['llegadas'], int(viaje['start station id']))
                datos_estacion_llegada['rangos_edad']['llegadas'][indice_rango] += 1

            else:
                model.actualizar_estacion(analizador['estaciones'], int(viaje['end station id']), nueva_llegada=(int(viaje['start station id']), indice_rango))

            total_caminos += model.crear_camino(analizador['grafo'], int(viaje['start station id']), int(viaje['end station id']),float(viaje['tripduration']))
            total_viajes += 1
        
            model.insertar_bici(analizador, viaje['bikeid'], {'inicio': viaje['start station id'],
                                                              'final': viaje['end station id'], 
                                                              'duracion': float(viaje['tripduration']),
                                                              'fecha': (viaje['starttime'][:10], viaje['stoptime'][:10])})

            if viaje['usertype'] == 'Customer':
                model.insertar_usuario(analizador, indice_rango, viaje['start station id'] + ' -> ' + viaje['end station id'])
    
    return total_estaciones, total_viajes, total_caminos

# ___________________________________________________
#  Funciones para consultas
# ___________________________________________________

def imprimir_lista_estaciones(grafo):
    """Imprime la lista de las estaciones del grafo."""
    iterador = it.newIterator(model.lista_estaciones(grafo))
    while it.hasNext(iterador):
        print(it.next(iterador))

def funciones_clusteres(analizador, estacion1, estacion2):
    """Requerimiento 1.
    
    Retorna el número de clústeres en el grafo y 
    si dos estaciones se encuentran en un mismo clúster.
    """
    kosaraju = model.estructura_Kosaraju(analizador['grafo'])
    numero_scc = model.numero_componentes_conectados(kosaraju)
    scc_dos_estaciones = model.encontrar_clusteres(kosaraju, estacion1, estacion2)
    return numero_scc, scc_dos_estaciones


def funciones_djisktra(analizador, vertice, llegada):
    djisktra=model.estructura_Dijkstra(analizador['grafo'], vertice)
    route=model.camino_vertice_a_vertice_dijstra(djisktra,llegada)
    return route

def menor_recorrido_posible(grafo, estacion_o, tiempo_pedido_min, tiempo_pedido_max):

    lista_entradas=model.entradas_estaciones(grafo, estacion_o)
    iterador_entradas = it.newIterator(lista_entradas)
    posibles_rutas=lt.newList()
    while it.hasNext(iterador_entradas):
        i = it.next(iterador_entradas)
        if type(i) == dict:
            i=i['key']
        if i!=estacion_o:
            lista_djistra=funciones_djisktra(grafo, estacion_o, i)
            if (lista_djistra is not None) :
                iterador_djistra = it.newIterator(lista_djistra)
                tiempo1=0
                camino_con_detalles=lt.newList()
                while it.hasNext(iterador_djistra):
                    j = it.next(iterador_djistra)
                    tiempo1+=(j['weight'] + 1200)
                    lt.addLast(camino_con_detalles,j)
                lt.addLast(camino_con_detalles,{'vertexA': i, 'vertexB': estacion_o, 'weight': model.peso_estacion_estacion(grafo, i, estacion_o)})
                tiempo1+=(model.peso_estacion_estacion(grafo, i, estacion_o))
                if (tiempo1//60 >= (tiempo_pedido_min)) and (tiempo1//60 <= (tiempo_pedido_max)): 
                    camino_con_detalles_str=organizar_rutas_str(camino_con_detalles,tiempo1,estacion_o) 
               
               
                    lt.addLast(posibles_rutas,camino_con_detalles_str)
    imprimir_rutas(posibles_rutas)
    
    return None

def esta_en_lista(lst,elemento):
    iterador_entradas = it.newIterator(lst)
    while it.hasNext(iterador_entradas):
        i = it.next(iterador_entradas)
        if i == elemento:
            return False
    return True

def organizar_rutas_str(lst, tiempo, estacion_o):
    iterador_entradas = it.newIterator(lst)
    ruta=''
    ruta+=('Estacion: '+str(estacion_o))
    while it.hasNext(iterador_entradas):
        i = it.next(iterador_entradas)
        llegada=str(i['vertexB'])
        duracion=str(round(i['weight']/60))
        ruta+=('__'+duracion+'min'+'--> Estacion: '+llegada)
    ruta+=('\n tiempo total del recorrido: '+str(round(tiempo/60)))
    return ruta

def imprimir_rutas(lst):
    if lt.size(lst)!=0:
        iterador_entradas = it.newIterator(lst)
        print('Acontinuacion las rutas circulares disponibles: \n')
        while it.hasNext(iterador_entradas):
            i = it.next(iterador_entradas)
            print(i)
            print()
        print('La cantidad de rutas encontradas fue: '+str(lt.size(lst)))
    else:
        print('No se encontraron rutas con las caracteristicas pedidas')


def encontrar_tops_3(analizador):
    """Requerimiento 3.
    
    Retorna los top 3 de las estaciones con más salidas
    más llegadas, y más tristes.
    """
    return model.encontrar_tops_3(analizador)

def recomendador_de_rutas(analizador, indice_edad):
    estacion_inicio, estacion_final = model.encontrar_max_estaciones_rango_edad(analizador, indice_edad)
    tiempo, caminos = model.datos_dijkstra(analizador, estacion_inicio[1], estacion_final[1])
    iterador_caminos = it.newIterator(caminos)
    camino = ""
    while it.hasNext(iterador_caminos):
        arco = it.next(iterador_caminos)
        camino += str(arco['vertexA']) + " -> " + str(arco['vertexB']) + "\n"
    return estacion_inicio, estacion_final, camino, tiempo

def ruta_interes_turistico(analizador, lat_inicial, lon_inicial, lat_final, lon_final):
    estaciones, distancia = model.encontrar_estaciones_lat_lon(analizador, lat_inicial, lon_inicial, lat_final, lon_final)
    tiempo, caminos = model.datos_dijkstra(analizador, estaciones[0]['id'], estaciones[1]['id'])
    iterador_caminos = it.newIterator(caminos)
    camino = ""
    while it.hasNext(iterador_caminos):
        arco = it.next(iterador_caminos)
        camino += str(arco['vertexA']) + " -> " + str(arco['vertexB']) + "\n"
    if tiempo != math.inf:
        return (estaciones[0]['id'], estaciones[0]['nombre']), (estaciones[1]['id'], estaciones[1]['nombre']), tiempo, distancia, camino
    elif tiempo == 0:
        return (estaciones[0]['id'], estaciones[0]['nombre']), (estaciones[1]['id'], estaciones[1]['nombre']), 0, 0, "Por favor quédese en esa estación"
    else:
        return (estaciones[0]['id'], estaciones[0]['nombre']), (estaciones[1]['id'], estaciones[1]['nombre']), 0, 0, "No existe ruta"

def identificador_estaciones_publicidad(analizador, indice_rango):
    """Requerimiento 7."""
    cantidad_viajes, lista_estaciones = model.encontrar_max_estaciones_adyacentes(analizador, indice_rango)
    str_estaciones = "Ninguna"
    if lista_estaciones is not None:
        str_estaciones = ""
        iterador = it.newIterator(lista_estaciones)
        while it.hasNext(iterador):
            str_estaciones += it.next(iterador) + '\n'
    return cantidad_viajes, str_estaciones


def identificador_bicicletas_mantenimiento(analizador, id_bici, fecha):
    lista_recorrido = model.encontrar_recorrido_estadisticas_bicis(analizador, id_bici, fecha)
    if lista_recorrido is not None:
        iterador = it.newIterator(lista_recorrido)
        recorrido = ""
        tiempo_recorrido = 0
        while it.hasNext(iterador):
            elemento = it.next(iterador)
            tiempo_recorrido += elemento['duracion']
            recorrido += elemento['inicio'] + ' -> ' + elemento['final'] + ' tiempo: ' + str(round(elemento['duracion']/60,3)) + '\n'
        return recorrido, round(tiempo_recorrido/60,3), round((86400-tiempo_recorrido)/60,3)
    return None
