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


# ───────────────────────────────────────────────────────────
# ::::::::::::::::::: MATRIZ DE RELACIONES ::::::::::::::::::
# ───────────────────────────────────────────────────────────

print("\n MATRIZ DE RELACIONES CAPITALES \n")
# Matriz de ceros de n x n
n = len(ciudades)
matriz_relaciones = np.zeros((n, n), dtype=int)

# Relacionamos todos las capitales entre ellas exceptuando ellas mismas
for capitalA in capitales:
    for capitalB in capitales:
        if capitalA != capitalB:
            matriz_relaciones[capitalA][capitalB] = 1

# np.set_printoptions(threshold=np.inf)
print(matriz_relaciones)


print("\n MATRIZ DE RELACIONES ENTRE CIUDADES DEL MISMO PAIS \n")
ciudades_mismo_pais = []

for ciudadA in ciudades:

    ciudades_mismo_pais = []

    for ciudadB in ciudades:
        if ciudadB['Pais'] == ciudadA['Pais'] and ciudadB['Id'] != ciudadA['Id']:
            ciudades_mismo_pais.append(ciudadB)

    cant_relaciones = random.randint(1, 3)
    cant_ciudades_mismo_pais = len(ciudades_mismo_pais)

    for _ in range(cant_relaciones):
        pos_ciudad_aleatoria = random.randint(0, cant_ciudades_mismo_pais - 1)
        objeto_ciudad = ciudades_mismo_pais[pos_ciudad_aleatoria]
        id_A = ciudadA['Id']
        id_B = objeto_ciudad['Id']
        matriz_relaciones[id_A][id_B] = 1

print(matriz_relaciones)


