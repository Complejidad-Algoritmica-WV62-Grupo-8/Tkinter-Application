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

