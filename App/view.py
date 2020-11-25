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
    print("\nC- Cargar los datos")
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

    if str(seleccion[0]).upper() == 'C':
        analizador = controller.inicializar_analizador()
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
            print("Tiempo de ejecución: ", round(tf-ti,3), "segundos")
        else:
            print("Por favor cargue los datos primero")
            print("Escriba \'C\' para cargar")

    elif seleccion[0] == '2':
        origen = int(input("inserte estacion de origen: "))
        inicio = int(input("inserte el tiempo minimo en minutos: "))
        fin = int(input("inserte el tiempo maximo en minutos: "))
        controller.menor_recorrido_posible(analizador,origen,inicio,fin)
        pass

    elif seleccion[0] == '3':
        if analizador is not None:
            ti = time.perf_counter()
            resultado = controller.encontrar_tops_3(analizador)
            tf = time.perf_counter()
            print("\nTop 3 estaciones de salidas: ")
            for i in resultado[0]:
                print(f"{i[1]:<40}: {i[0]} salidas")
            print("\nTop 3 estaciones de llegada: ")
            for i in resultado[1]:
                print(f"{i[1]:<40}: {i[0]} llegadas")
            print("\nTop 3 estaciones más tristes: ")
            for i in resultado[2]:
                print(f"{i[1]:<40}: {i[0]} salidas y llegadas")
            print("Tiempo de ejecución:",round(tf-ti,3),"segundos")
        else:
            print("Por favor cargue los datos primero")
            print("Escriba \'C\' para cargar")

    elif seleccion[0] == '4':
        pass

    elif seleccion[0] == '5':
        if analizador is not None:
            print("Por favor ingrese su rango de edad según las siguientes opciones: ")
            print("1- 0-10")
            print("2- 11-20")
            print("3- 21-30")
            print("4- 31-40")
            print("5- 41-50")
            print("6- 51-60")
            print("7- 60+\n")
            indice_edad = int(input()[0])-1
            try:
                ti = time.perf_counter()
                est_inicio, est_final, camino, tiempo = controller.recomendador_de_rutas(analizador, indice_edad)
                tf = time.perf_counter()
                print(f"\nEstación inicial: {est_inicio[2]} - id: {est_inicio[1]} - Total de salidas: {est_inicio[0]}")
                print(f"Estación final:   {est_final[2]} - id: {est_final[1]} - Total de llegadas: {est_final[0]}")
                print(f"Ruta a tomar:\n{camino}")
                print(f"Tiempo estimado de viaje: {round(tiempo/60,3)}")
                print(f"Tiempo de ejecución: {round(tf-ti,3)} Segundos")
            except ValueError:
                print("No existen estaciones a las que salgan o lleguen personas en ese rango de fechas")
                time.sleep(1)
            except IndexError:
                print("Por favor seleccione un rango de edad válido")
                time.sleep(1)
        else:
            print("Por favor cargue los datos primero")
            print("Escriba \'C\' para cargar")

    elif seleccion[0] == '6':
        if analizador is not None:
            try:
                pos_inicial = input("Ingrese su posición de origen (ej: 40.69839895 -73.98068914): ").split()
                pos_final = input("Ingrese su posición de destino (ej: 40.69196566 -73.9813018): ").split()
                ti = time.perf_counter()
                resultado = controller.ruta_interes_turistico(analizador, float(pos_inicial[0]), float(pos_inicial[1]), float(pos_final[0]), float(pos_final[1]))
                tf = time.perf_counter()
                print(f"\nEstación inicial: {resultado[0][1]} (id: {resultado[0][0]})")
                print(f"Estación final: {resultado[1][1]} (id: {resultado[1][0]})")
                print(f"Ruta a tomar:\n{resultado[4]}")
                print(f"Tiempo estimado de viaje: {round(resultado[2]/60,3)}")
                print(f"Distancia total: {round(resultado[3],3)} Kilómetros")
                print(f"Tiempo de ejecución: {round(tf-ti,3)} Segundos")
            except ValueError:
                print("\nPor favor ingrese los datos en el formato correcto")
                time.sleep(1)
            except IndexError:
                print("\nPor favor ingrese los datos en el formato correcto")
                time.sleep(1)
        else:
            print("Por favor cargue los datos primero")
            print("Escriba \'C\' para cargar")

    elif seleccion[0] == '7':
        if analizador is not None:
            print("Por favor ingrese su rango de edad según las siguientes opciones: ")
            print("1- 0-10")
            print("2- 11-20")
            print("3- 21-30")
            print("4- 31-40")
            print("5- 41-50")
            print("6- 51-60")
            print("7- 60+\n")
            indice_edad = int(input()[0])-1
            cantidad_viajes, str_estaciones = controller.identificador_estaciones_publicidad(analizador, indice_edad)
            print(f"\nViajes:\n{str_estaciones}")
            print(f"La cantidad de viajes hechos fue: {cantidad_viajes}")
        else:
            print("Por favor cargue los datos primero")
            print("Escriba \'C\' para cargar")

    elif seleccion[0] == '8':
        if analizador is not None:
            id_bici = input("Ingrese la Id de bicicleta que desea buscar:\n")
            fecha = input("Ingrese el día que desea buscar en formato AAAA-MM-DD (ej: 2018-01-31):\n")
            try:
                ti = time.perf_counter()
                recorrido, tiempo_uso, tiempo_estacionado = controller.identificador_bicicletas_mantenimiento(analizador, id_bici, fecha)
                tf = time.perf_counter()
                print(f"Los recorridos que hizo ese día fueron:\n{recorrido}")
                print(f"El tiempo de uso total fue: {tiempo_uso} minutos")
                print(f"El tiempo de estacionado total fue: {tiempo_estacionado} minutos")
                print(f"Tiempo de ejecución: {round(tf-ti,3)} Segundos")
            except TypeError:
                print("No se ha encontrado la bicicleta o la fecha")
                print("Asegúrese de haber escrito bien los datos")
                time.sleep(1)
        else:
            print("Por favor cargue los datos primero")
            print("Escriba \'C\' para cargar")


    elif seleccion[0] == '0':
        sys.exit(0)
    
    else:
        sys.exit(0)

#180,2018-01-01,2018-01-01,1,estacion 1,1,1,4,estacion 4,4,4,03,1992