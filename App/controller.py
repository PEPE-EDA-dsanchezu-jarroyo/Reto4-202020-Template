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
import csv
import os
import time

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
        ti = time.perf_counter()
        if archivo.endswith('.csv'):
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
    model.promediar_pesos(analizador['grafo'])
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
        if not model.existe_estacion(analizador['estaciones'], int(viaje['start station id'])):
            total_estaciones += 1
            datos_estacion_salida = {'id': int(viaje['start station id']),
                                     'nombre': viaje['start station name'],
                                     'latitud': float(viaje['start station latitude']),
                                     'longitud': float(viaje['start station longitude'])}
            model.insertar_estacion(analizador['grafo'],analizador['estaciones'],datos_estacion_salida['id'], datos_estacion_salida)

        if not model.existe_estacion(analizador['estaciones'], int(viaje['end station id'])):
            total_estaciones += 1
            datos_estacion_llegada = {'id': int(viaje['end station id']),
                                     'nombre': viaje['end station name'],
                                     'latitud': float(viaje['end station latitude']),
                                     'longitud': float(viaje['end station longitude'])}
            model.insertar_estacion(analizador['grafo'],analizador['estaciones'],datos_estacion_llegada['id'], datos_estacion_llegada)       

        total_viajes += 1
        total_caminos += model.crear_camino(analizador['grafo'], int(viaje['start station id']), int(viaje['end station id']),float(viaje['tripduration']))

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
    """Retorna el número de clústeres en el grafo y si dos estaciones se encuentran en un mismo clúster."""
    kosaraju = model.estructura_Kosaraju(analizador['grafo'])
    numero_scc = model.numero_componentes_conectados(kosaraju)
    scc_dos_estaciones = model.encontrar_clusteres(kosaraju, estacion1, estacion2)
    return numero_scc, scc_dos_estaciones

def funciones_djisktra(analizador, vertice,llegada):
    djisktra=model.estructura_Dijkstra(analizador['grafo'], vertice)
    print(djisktra)
    route=model.camino_vertice_a_vertice_dijstra(djisktra,llegada)
    print(route)
    return route

def menor_recorrido_posible(grafo, estacion_o):
    tiempo_menor=100000000000000000000000000
    ruta_menor=''
    lista_entradas=model.entradas_estaciones(grafo, estacion_o)
    for i in lista_entradas['elements']:
        lista_djistra=funciones_djisktra(grafo, estacion_o, i)
        tiempo1=0
        for j in lista_djistra['elements']:
            tiempo1+=(model.peso_estacion_estacion(grafo,estacion_o, j) + 20)
        tiempo1+=model.peso_estacion_estacion(grafo,estacion_o, i)
        if tiempo1 <= tiempo_menor:  
            tiempo_menor=tiempo1
            ruta_menor=j
    return (tiempo_menor, tiempo1)