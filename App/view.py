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


import sys
import config
from App import controller
from DISClib.ADT import stack
import time
assert config

"""
La vista se encarga de la interacción con el usuario.
Presenta el menu de opciones  y  por cada seleccion
hace la solicitud al controlador para ejecutar la
operación seleccionada.
"""

print("Bienvenido!!")

# ___________________________________________________
#  Variables
# ___________________________________________________

analizador = None

# ___________________________________________________
#  Menu principal
# ___________________________________________________


def imprimir_menu_principal():
    """Imprime todas las opciones del menú principal."""
    print("\nI- Inicializar el analizador")
    print("C- Cargar los datos")
    print("1- Req 1: Encontrar la cantidad de clusters")
    print("2- Req 2: Encontrar una ruta turística circular")
    print("3- Req 3: Encontrar estaciones críticas")
    print("4- Req 4: Encontrar una ruta turística por resistencia")
    print("5- Req 5: Recomendador de rutas")
    print("6- Req 6: Ruta de interés turístico")
    print("7- Req 7: Identificación de estaciones para publicidad")
    print("8- Req 8: Identiciación de bicicletas para mantenimiento")
    print("0- Salir\n")


"""
Menu principal
"""

while True:
    imprimir_menu_principal()
    seleccion = input("Seleccione una opción:\n")

    if seleccion[0] == 'I':
        analizador = controller.inicializar_analizador()

    elif seleccion[0] == 'C':
        analizador, total_estaciones, total_caminos = controller.cargar_viajes(analizador)

    elif seleccion[0] == '1':
        if analizador is not None:
            es1 = int(input("Ingrese el ID de la primera estación:\n"))
            es2 = int(input("Ingrese el ID de la segunda estación:\n"))
            ti = time.perf_counter()
            numero_scc, scc_dos_estaciones = controller.funciones_clusteres(analizador, es1, es2)
            tf = time.perf_counter()
            print("El número de clústeres es:", numero_scc)
            print("La estación", es1, "y", es2, end=' ')
            if scc_dos_estaciones:
                print("pertenecen al mismo clúster")
            else:
                print("no pertenecen al mismo clúster")
            print("Tiempo de ejecución: ", tf-t1, "segundos")
        else:
            print("Por favor cargue los datos primero")
            print("Escriba \'I\' para inicializar y \'C\' para cargar")

    elif seleccion[0] == '2':
        pass

    elif seleccion[0] == '3':
        pass

    elif seleccion[0] == '4':
        pass

    elif seleccion[0] == '5':
        pass

    elif seleccion[0] == '6':
        pass

    elif seleccion[0] == '7':
        pass

    elif seleccion[0] == '8':
        pass

    elif seleccion[0] == '0':
        sys.exit(0)
    
    else:
        sys.exit(0)