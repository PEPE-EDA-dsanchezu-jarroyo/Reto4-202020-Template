simulacion = "tripduration,starttime,stoptime,start station id,start station name,start station latitude,start station longitude,end station id,end station name,end station latitude,end station longitude,bikeid,birth year\n"
continuar = True
while continuar:
    print()
    vertice_a = input("Ingrese la id del vertice A: ")
    vertice_b = input("Ingrese la id del vertice B: ")
    peso = input("Ingrese el peso de la conexión: ")
    bikeid = input("Ingrese la Id de la bicicleta: ")
    simulacion += f"{peso},2018-01-01,2018-01-01,{vertice_a},estacion {vertice_a},{vertice_a},{vertice_a},{vertice_b},estacion {vertice_b},{vertice_b},{vertice_b},{bikeid},1992\n"
    continuar_str = input("¿Quiere continuar agregando datos? (s/n): ")
    if continuar_str.lower() == 'n':
        continuar = False
archivo = open("Data/simulacion.csv",'w')
archivo.write(simulacion)
archivo.close

