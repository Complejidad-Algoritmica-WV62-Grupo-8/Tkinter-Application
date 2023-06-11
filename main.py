import openpyxl
import pandas as pd
import numpy as np
import random
import math

# ───────────────────────────────────────────────────────────
# :::::::::::::::::::::::::: Excel ::::::::::::::::::::::::::
# ───────────────────────────────────────────────────────────

# Leemos el archivo Excel Paises latinoamericanos en un DataFrame de pandas
df = pd.read_excel(io='C:\\Users\\rafae\\Desktop\\Upc\\Ciclo 6\\Complejidad Algoritmica\\Proyecto\\Codigos\\Tkinter-Application\\Tkinter-Application\\Paises de latinoamerica.xlsx',
                   sheet_name='Hoja1', header=0, names=None, index_col=None, usecols='A,B,D,E,F,J', engine='openpyxl')

# Imprime las primeras 3 filas del dataframe
print(df.head(3))


# ───────────────────────────────────────────────────────────
# :::::::::::::::::::::::: CIUDADES :::::::::::::::::::::::::
# ───────────────────────────────────────────────────────────

ciudades = []
for _, row in df.iterrows():
    obj = {
        'Id': row['id'],
        'Nombre': row['city'],
        'Latitud': row['lat'],
        'Longitud': row['lng'],
        'Pais': row['country'],
        'Tipo_de_capital': row['capital']
    }
    ciudades.append(obj)

# Imprimir los primeros 3 objetos del ciudades
print("\n ARREGLO DE CIUDADES \n")
for obj in ciudades[:3]:
    print(obj)


# ───────────────────────────────────────────────────────────
# :::::::::::::::::::::::: CAPITALES ::::::::::::::::::::::::
# ───────────────────────────────────────────────────────────

# Arreglo para almacenar los IDs de las ciudades capitales
capitales = []

# Recorrer el arreglo ciudades y obtener los IDs de las ciudades capitales
for obj in ciudades:
    if obj['Tipo_de_capital'] == 'primary':
        id = obj['Id']
        capitales.append(id)

# Imprimir el arreglo de ciudades capitales
# Las posiciones son 2 lugares por debajo de lo que dicta el excel,
# ya que el indice empieza en 0 y se opmite los titulos de las columnas.
print("\n ARREGLO IDs DE CAPITALES \n")
for obj in capitales[:3]:
    print(obj)


# ───────────────────────────────────────────────────────────
# :::::::::::::::::::::::::: PAISES :::::::::::::::::::::::::
# ───────────────────────────────────────────────────────────

print("\n LISTA DE PAISES \n")
# Recorremos las ciudades y solo guardamos los Países diferentes 
# en un conjunto que luego lo transformamos a una lista
paisesConjunto = set(ciudad['Pais'] for ciudad in ciudades)
paisesLista = list(paisesConjunto)
print(paisesLista)


