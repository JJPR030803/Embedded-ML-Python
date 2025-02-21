import csv
from ML.data_imputation import suavizamiento_exponencial_simple,mediana
import statistics



file = "sensor_data.csv"

temperaturas = []

with open(file) as file:
    reader = csv.reader(file)
    next(reader)
    for linea in file:
       
        lineas = linea.split(",")
        try:
            temperaturas.append(float(lineas[1]))
        except TypeError:
           print("Error")


medianas = mediana(temperaturas,360)
datos_suavizados = suavizamiento_exponencial_simple(temperaturas,0.4)
medianas_suavizadas = suavizamiento_exponencial_simple(medianas,0.5)


print(len(datos_suavizados))