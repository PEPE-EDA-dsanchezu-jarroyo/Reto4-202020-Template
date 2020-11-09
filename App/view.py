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
import timeit
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

analizador = {}

# ___________________________________________________
#  Menu principal
# ___________________________________________________


def imprimir_menu_principal():
    """Imprime todas las opciones del menú principal."""
    print("\n1- Inicializar el analizador")
    print("2- Cargar los datos")
    print("3- Req 1: Encontrar la cantidad de clusters")
    print("4- Req 2: Encontrar una ruta turística circular")
    print("5- Req 3: Encontrar estaciones críticas")
    print("6- Req 4: Encontrar una ruta turística por resistencia")
    print("7- Req 5: Recomendador de rutas")
    print("8- Req 6: Ruta de interés turístico")
    print("9- Req 7: Identificación de estaciones para publicidad")
    print("10- Req 8: Identiciación de bicicletas para mantenimiento")
    print("0- Salir\n")


"""
Menu principal
"""

while True:
    imprimir_menu_principal()
    seleccion = input("Seleccione una opción:\n")

    if seleccion[0] == '1':
        analizador = controller.inicializar_analizador()

    elif seleccion[0] == '2':
        analizador, total_estaciones, total_caminos = controller.cargar_viajes(analizador)
        # print("La cantidad de estaciones cargadas es:",total_estaciones)
        # print("La cantidad de caminos presentes es:",total_caminos)

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

    elif seleccion[0] == '9':
        pass

    elif seleccion[0] == '10':
        pass

    elif seleccion[0] == '0':
        sys.exit(0)
    
    else:
        sys.exit(0)