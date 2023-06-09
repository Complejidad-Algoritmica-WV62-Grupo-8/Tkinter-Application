import tkinter as tk
from tkinter import font
import heapq
import openpyxl
import pandas as pd
import numpy as np
import random
import math
import graphviz as gv
from graphviz import Source
from PIL import Image
from PIL import ImageTk, Image
# from graphviz import Digraph
###################################################################################################
###################################################################################################

import heapq
import graphviz as gv
from graphviz import Graph
import openpyxl
import pandas as pd
import numpy as np
import random
import math

# ───────────────────────────────────────────────────────────
# :::::::::::::::::::::::::: Excel ::::::::::::::::::::::::::
# ───────────────────────────────────────────────────────────

# Leemos el archivo Excel Paises latinoamericanos en un DataFrame de pandas
df = pd.read_excel(io='paisesprueba.xlsx',
                   sheet_name='Hoja1', header=0, names=None, index_col=None, usecols='A,B,D,E,F,J', engine='openpyxl')



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
#print("\n ARREGLO DE CIUDADES \n")
#for obj in ciudades[:3]:
#    print(obj)


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
#print("\n ARREGLO IDs DE CAPITALES \n")
#for obj in capitales[:3]:
#    print(obj)


# ───────────────────────────────────────────────────────────
# :::::::::::::::::::::::::: PAISES :::::::::::::::::::::::::
# ───────────────────────────────────────────────────────────

#print("\n LISTA DE PAISES \n")
# Recorremos las ciudades y solo guardamos los Países diferentes
# en un conjunto que luego lo transformamos a una lista
paisesConjunto = set(ciudad['Pais'] for ciudad in ciudades)
paisesLista = list(paisesConjunto)
#print(paisesLista)


# ───────────────────────────────────────────────────────────
# ::::::::::::::::::: MATRIZ DE RELACIONES ::::::::::::::::::
# ───────────────────────────────────────────────────────────

#print("\n MATRIZ DE RELACIONES CAPITALES \n")
# Matriz de ceros de n x n
n = len(ciudades)
matriz_relaciones = np.zeros((n, n), dtype=int)

# Relacionamos todos las capitales entre ellas exceptuando ellas mismas
for capitalA in capitales:
    for capitalB in capitales:
        if capitalA != capitalB:
            matriz_relaciones[capitalA][capitalB] = 1

# np.set_printoptions(threshold=np.inf)
#print(matriz_relaciones)


#print("\n MATRIZ DE RELACIONES ENTRE CIUDADES DEL MISMO PAIS \n")
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
        matriz_relaciones[id_B][id_A] = 1

#print(matriz_relaciones)


# ───────────────────────────────────────────────────────────
# ::::::::::::::::::: MATRIZ DE DISTANCIAS ::::::::::::::::::
# ───────────────────────────────────────────────────────────

def calcular_distancia(lat1, lon1, lat2, lon2):
    # Radio de la Tierra en kilómetros
    radio_tierra = 6371.0

    # Convertir las latitudes y longitudes de grados a radianes
    lat1_rad = math.radians(lat1)
    lon1_rad = math.radians(lon1)
    lat2_rad = math.radians(lat2)
    lon2_rad = math.radians(lon2)

    # Diferencias entre las latitudes y longitudes
    dlat = lat2_rad - lat1_rad
    dlon = lon2_rad - lon1_rad

    # Calcular la fórmula de Haversine
    a = math.sin(dlat/2)**2 + math.cos(lat1_rad) * \
        math.cos(lat2_rad) * math.sin(dlon/2)**2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))
    distancia = radio_tierra * c

    return distancia


#print("\n MATRIZ DE DISTANCIAS \n")
matriz_distancias = np.copy(matriz_relaciones)

for ciudadA in ciudades:
    for ciudadB in ciudades:
        i = ciudadA['Id']
        j = ciudadB['Id']
        if matriz_distancias[i][j] == 1:

            lat_A = ciudadA['Latitud']
            lng_A = ciudadA['Longitud']

            lat_B = ciudadB['Latitud']
            lng_B = ciudadB['Longitud']

            matriz_distancias[i][j] = calcular_distancia(
                lat_A, lng_A, lat_B, lng_B)

#print(matriz_distancias)


# ───────────────────────────────────────────────────────────
# ::::::::::::::::::::: EXCEL PARA NODOS ::::::::::::::::::::
# ───────────────────────────────────────────────────────────

# Crear un nuevo libro de Excel
excel_nodos = openpyxl.Workbook()

# Seleccionar la hoja activa
hoja = excel_nodos.active

# Agregar encabezados
hoja["A1"] = "ID"
hoja["B1"] = "Label"

# Agregar datos de ciudades en filas
for i, ciudad in enumerate(ciudades, start=2):
    hoja["A{}".format(i)] = ciudad['Id']
    hoja["B{}".format(i)] = ciudad['Nombre']

# Guardar el archivo de Excel
excel_nodos.save("Nodos.xlsx")


# ───────────────────────────────────────────────────────────
# ::::::::::::::::::::: EXCEL PARA LINKS ::::::::::::::::::::
# ───────────────────────────────────────────────────────────

# Crear un nuevo libro de Excel
excel_links = openpyxl.Workbook()

# Seleccionar la hoja activa
hoja = excel_links.active

# Agregar encabezados
hoja["A1"] = "Source"
hoja["B1"] = "Target"
hoja["C1"] = "Weight"
hoja["D1"] = "Label"
hoja["E1"] = "Type"

# Agregar datos de relaciones en filas
cont = 2
for i, ciudadA in enumerate(ciudades, start=2):
    for j, ciudadB in enumerate(ciudades, start=2):

        id_A = ciudadA['Id']
        id_B = ciudadB['Id']

        if matriz_distancias[id_A][id_B] != 0:
            hoja["A{}".format(cont)] = ciudadA['Id']
            hoja["B{}".format(cont)] = ciudadB['Id']
            hoja["C{}".format(cont)] = matriz_distancias[id_A][id_B]
            hoja["D{}".format(cont)] = "camino"
            hoja["E{}".format(cont)] = "Undirected"
            cont += 1

# Guardar el archivo de Excel
excel_links.save("Links.xlsx")

# ───────────────────────────────────────────────────────────
# ::::::::::::::::::::: ALGORITMOS ::::::::::::::::::::
# ───────────────────────────────────────────────────────────

def dijkstra(graph, start):
    distances = {node: float('inf') for node in graph}
    distances[start] = 0
    parents = {node: None for node in graph}
    queue = [(0, start)]

    while queue:
        current_distance, current_node = heapq.heappop(queue)

        if current_distance > distances[current_node]:
            continue

        for neighbor, weight in graph[current_node].items():
            distance = current_distance + weight
            if distance < distances[neighbor]:
                distances[neighbor] = distance
                parents[neighbor] = current_node
                heapq.heappush(queue, (distance, neighbor))

    return distances, parents

"""def drawG_am(G, directed=False, weighted=False, path=[], layout="sfdp"):
  graph = gv.Digraph("digrafo") if directed else gv.Graph("grafo")
  n = len(G)
  added = set()
  for v, u in enumerate(path):
    if u != -1:
      if weighted:
        graph.edge(str(u), str(v), str(G[u, v]), dir="forward", penwidth="2", color="orange")
      else:
        graph.edge(str(u), str(v), dir="forward", penwidth="2", color="orange")
      added.add(f"{u},{v}")
      added.add(f"{v},{u}")
  for u in range(n):
    for v in range(n):
      draw = False
      if G[u, v] > 0 and not directed and not f"{u},{v}" in added:
        added.add(f"{u},{v}")
        added.add(f"{v},{u}")
        draw = True
      elif directed:
        draw = True
      if draw:
        if weighted:
          graph.edge(str(u), str(v), str(G[u, v]))
        else:
          graph.edge(str(u), str(v))
  return graph"""

def draw_graph(graph, origin_cities, destination):
    dot = Graph(comment='Grafo de Rutas', strict=False)

    for city in graph:
        dot.node(str(city), label=str(city))

    added_edges = set()

    for city in graph:
        for neighbor, weight in graph[city].items():
            if (neighbor, city) not in added_edges:
                dot.edge(str(city), str(neighbor), label=str(weight))
                added_edges.add((city, neighbor))

    for origin_city in origin_cities:
        shortest_distances, parents = dijkstra(graph, origin_city)

        current_city = destination
        while current_city is not None:
            parent_city = parents[current_city]
            if parent_city is not None:
                dot.edge(str(parent_city), str(current_city), color='red', penwidth='2', dir="forward")
            current_city = parent_city

    # dot.render('grafo', format='png')
    # dot.view()
    return dot

def parse_city(city):
    city_id, supplies = city.split('-')
    return int(city_id), int(supplies)

def parse_cities(cities):
    parsed_cities = {}
    for city in cities:
        city_id, supplies = parse_city(city)
        parsed_cities[city_id] = supplies
    return parsed_cities

def create_graph(adjacency_matrix):
    graph = {}
    n = len(adjacency_matrix)

    for i in range(n):
        graph[i] = {}
        for j in range(n):
            if adjacency_matrix[i][j] > 0:
                graph[i][j] = adjacency_matrix[i][j]

    return graph

def shortest_route(adjacency_matrix, origin_cities, destination, demand):
    graph = create_graph(adjacency_matrix)
    cities = parse_cities(origin_cities)

    shortest_distances, parents = dijkstra(graph, destination)

    sorted_cities = sorted(cities, key=lambda city: shortest_distances[city])

    total_supplies = 0
    max_supplies = 0
    sending_cities = []
    distances_to_destination = {}
    supplies_sent = {}

    for city_id in sorted_cities:
        if total_supplies >= demand:
            break

        if cities[city_id] > 0:
            if shortest_distances[city_id] != math.inf:
                sending_cities.append(city_id)
                supplies_to_send = min(demand - total_supplies, cities[city_id])
                total_supplies += supplies_to_send
                cities[city_id] -= supplies_to_send
                supplies_sent[city_id] = supplies_to_send
                distances_to_destination[city_id] = shortest_distances[city_id]

    for city_id in sending_cities:
        max_supplies += supplies_sent[city_id]

    return sending_cities, distances_to_destination, supplies_sent, max_supplies


# ───────────────────────────────────────────────────────────
# ::::::::::::::::::::: TKINTER ::::::::::::::::::::
# ───────────────────────────────────────────────────────────


# DISEÑO - ventana principa
ventana = tk.Tk()
ventana.title("Complejidad Algoritmica")
ventana.geometry("1728x1117")
bold_font = font.Font(weight="bold")#este hace negrita el texto


# DISEÑO - header-----------------------------------------------------------------------------------------------------
parte_superior = tk.Frame(ventana, width=1728,height=75,background='light blue')
parte_superior.grid(row=0,column=0)

titulo = tk.Label(ventana, text="Cadena de suministros",background='light blue',font=('arial',20),fg='black')
titulo.grid(row=0, column=0, columnspan=2, sticky='w')


#funcion que lee archivo de excel que contengan las ciudades
def lecturaArch():
    #archivo = 'worldcities.xlsx'
    #df2 = pd.read_excel(archivo, sheet_name='Hoja1')
    df2 = pd.read_excel(io='paisesprueba.xlsx',
                   sheet_name='Hoja1', header=0, names=None, index_col=None, usecols='B', engine='openpyxl')
    return df2

def Scrollbar():
    scrollbar = tk.Scrollbar(ventana)
    scrollbar.place(x=466,y=202,height=401)
    return scrollbar

def frame1():

    lLista= tk.Label(ventana,text='Lista de ciudades', font=bold_font)
    lLista.place(x=325,y=170)

    listbox = tk.Listbox(ventana,width=30,height=25)

    filas = lecturaArch().to_records(index=False)#convierte el dateframe en filas para poder mostrar en el listbox

    i = 0# para poder ver los ID's
    #este for agrega los datos al listbox
    for fila in filas:
        fila_str = ' '.join(map(str, fila))
        listbox.insert(tk.END, f'{i}   - {fila_str}')
        i += 1

    scrollbar = Scrollbar()
    scrollbar.config(command=listbox.yview)
    listbox.config(yscrollcommand=scrollbar.set)
    listbox.place(x=300,y=200)#para que aparezca el listbox

frame1()

#  DISEÑO - FRAME DONDE INGRESAMOS DATOS
frameInput = tk.Frame(ventana, borderwidth=2, relief=tk.SOLID,width=500,height=400)
frameInput.place(x=680,y=200)
lLista2= tk.Label(ventana,text='Datos de entrada', font=bold_font)
lLista2.place(x=870,y=170)

def Input1():
    label1 = tk.Label(frameInput, text="Ciudades donde cuenta con suministro\ny sus respectivos stocks")
    label1.place(x=130,y=50)
    input1=tk.Text(frameInput,width=30, height=5)
    input1.place(x=130,y=90)
    return input1

def Input2():
    label2 = tk.Label(frameInput, text="Ciudades de destino(id)")
    label2.place(x=130,y=200)
    input2=tk.Text(frameInput,width=25, height=2)
    input2.place(x=130,y=220)
    return input2

def Input3():
    label3 = tk.Label(frameInput, text="Cantidad de suministro que necesita la ciudad")
    label3.place(x=130,y=275)
    input3=tk.Text(frameInput,width=30, height=2)
    input3.place(x=130,y=300)
    return input3

input1 = Input1()
input2 = Input2()
input3 = Input3()

#OBTENIENDO DATOS DEL TEXT
def almacenesYsuministros():
    contenido1 = input1.get("1.0", tk.END)

    return contenido1

def obtener_ID():
    
    contenido2 = input2.get("1.0", tk.END)
    
    #return f'datos2 {contenido2}'
    return contenido2

def obtener_suministro():
    
    contenido3 = input3.get("1.0", tk.END)
    # return f'datos3 {contenido3}'
    return contenido3

#texto de los ciudad(ID) y sus suministro
palabras = almacenesYsuministros()
lineas = palabras.splitlines()

arregloLineas = []

for linea in lineas:
    arregloLineas.append(linea)


Idies = obtener_ID()

suministro = obtener_suministro()


def salir_ventana(root):
    root.destroy()


def ventana_Restricciones():
    ventana_secundaria = tk.Toplevel(ventana)
    ventana_secundaria.title(" Restricciones ")
    ventana_secundaria.geometry("1728x1117")

    #header
    parte_superior2 = tk.Frame(ventana_secundaria, width=1728,height=75,background='light blue')
    parte_superior2.grid(row=0,column=0)


    def ScrollbarR():
        scrollbar = tk.Scrollbar(ventana_secundaria)
        scrollbar.place(x=466,y=202,height=401)
        return scrollbar

    #LISTA DE CIUDADES
    lLista= tk.Label(ventana_secundaria,text='Lista de ciudades', font=bold_font)
    lLista.place(x=325,y=170)

    lListaR= tk.Label(ventana_secundaria,text='Restricciones', font=bold_font)
    lListaR.place(x=700,y=170)

    listbox = tk.Listbox(ventana_secundaria,width=30,height=25)

    filas = lecturaArch().to_records(index=False)#convierte el dateframe en filas para poder mostrar en el listbox

    i = 0# para poder ver los ID's
    #este for agrega los datos al listbox
    for fila in filas:
        fila_str = ' '.join(map(str, fila))
        listbox.insert(tk.END, f'{i}   - {fila_str}')
        i += 1

    scrollbar = ScrollbarR()
    scrollbar.config(command=listbox.yview)
    listbox.config(yscrollcommand=scrollbar.set)
    listbox.place(x=300,y=200)#para que aparezca el listbox
    #=====================


    #titulo del header
    titulo2 = tk.Label(ventana_secundaria, text="Cadena de suministros",background='light blue',font=('arial',20),fg='black')
    titulo2.grid(row=0, column=0, columnspan=2, sticky='w')

    frameInputR = tk.Frame(ventana_secundaria, borderwidth=2, relief=tk.SOLID,width=500,height=400)
    frameInputR.place(x=500,y=200)
    labelR = tk.Label(frameInputR, text="Ciudades que se encuentran\nrestringuidos por diversos motivos")
    labelR.place(x=145,y=50)
    inputR=tk.Text(frameInputR,width=30, height=5)
    inputR.place(x=130,y=90)

    ##########################################################
    ##########################################################
    ##########################################################
    def obtList():
        # resctri = inputR.get("0.0", tk.END)
        # # listId = resctri

        numeros_texto = inputR.get("0.0", tk.END)
        numeros_lineas = numeros_texto.split("\n")
        restricciones1= [ int(n) for n in numeros_lineas if n ]


        # listenteros = []]

        # for i in resctri:
        #     listenteros.append( int(i) )

            # print(listId)

        restrictions = restricciones1#[1,3,4]
        for n in restrictions:
            for i in range(len(matriz_distancias)):
                matriz_distancias[n][i] = 0
                matriz_distancias[i][n] = 0

        # print(matriz_distancias)
    # return matriz_distancias
    
    # NuevaMatrizDistancias = obtList()
    print(matriz_distancias)
    matrizlol = matriz_distancias

    def salir():
        salir_ventana(ventana_secundaria)

    botonGrafos = tk.Button(frameInputR,text='Evaluar',bg='light blue',fg='black',width=12,height=1,command=ventana_respuesta_en_texto)
    # botonGrafos.config(borderwidth=10, relief=tk.RAISED)
    botonGrafos.place(x=280,y=180)
    

#para mostrar la otra ventana
def ventana_respuesta_en_texto():
    
    #ventana secundaria
    ventana_secundaria = tk.Toplevel(ventana)
    ventana_secundaria.title("Ventana Secundaria")
    ventana_secundaria.geometry("1728x1117")

    #header
    parte_superior2 = tk.Frame(ventana_secundaria, width=1728,height=75,background='light blue')
    parte_superior2.grid(row=0,column=0)

    #titulo del header
    titulo2 = tk.Label(ventana_secundaria, text="Cadena de suministros",background='light blue',font=('arial',20),fg='black')
    titulo2.grid(row=0, column=0, columnspan=2, sticky='w')

    frameInput2 = tk.Frame(ventana_secundaria, borderwidth=2, relief=tk.SOLID,width=500,height=400)
    frameInput2.place(x=450,y=200)

    subtitulo= tk.Label(frameInput2,text='Para abastecer a la ciudad que necesita suministros, debes enviar los suministros\ndesde las siguientes ciudades, ya que son las más cercanas y las mínimas\nnecesarias para completar los suministros solicitados:')
    subtitulo.place(x=55,y=45)

    subtitulo2 = tk.Label(frameInput2, text="id - nombre - distancia - suministros enviados")
    subtitulo2.place(x=130,y=170)

    ###############################################3
   
    datosRelevantes = almacenesYsuministros()
    datosRelevantes2 = datosRelevantes.splitlines()
 
    origin_cities = datosRelevantes2
    destination = int ( obtener_ID() )
    demand = int ( obtener_suministro() )

    #########################################################
    text = tk.Text(frameInput2,width=50, height=5)
    text.place(x=60,y=200)


    sending_cities, distances_to_destination, supplies_sent, max_supplies = shortest_route(matriz_distancias, origin_cities, destination, demand)

    #########################################################  
    
    if demand > max_supplies:
        print("No es posible satisfacer la demanda.")
    else:
        print("Ciudades desde las cuales se deben enviar los suministros:")
        for city in sending_cities:
            text.insert(tk.END,f"Ciudad {city}: Distancia a recorrer {distances_to_destination[city]} km - {supplies_sent[city]} suministros a enviar.")

    ###########################################################################
    
    graph = create_graph(matriz_distancias)
    dot = draw_graph(graph, sending_cities, destination)
    # dot = drawG_am(matriz_distancias, weighted=True)
    dot.format = 'png'
    dot.render('grafo', view=False)
    
 
    imagen = Image.open('grafo.png')
    ancho_deseado = 350
    altura_deseada = 200
    imagen = imagen.resize((ancho_deseado, altura_deseada), Image.ANTIALIAS)
    imagen_tk = ImageTk.PhotoImage(imagen)

    #################################################################################
    
    def salir():
        salir_ventana(ventana_secundaria)
    
    def ventana_Grafos1():

        ventana_secundaria = tk.Toplevel(ventana)
        ventana_secundaria.title(" Grafos ")
        ventana_secundaria.geometry("1728x1117")

        #header
        parte_superior2 = tk.Frame(ventana_secundaria, width=1728,height=75,background='light blue')
        parte_superior2.grid(row=0,column=0)

        lListaR= tk.Label(ventana_secundaria,text='Grafo recorrido', font=bold_font)
        lListaR.place(x=650,y=170)

        #titulo del header
        titulo2 = tk.Label(ventana_secundaria, text="Cadena de suministros",background='light blue',font=('arial',20),fg='black')
        titulo2.grid(row=0, column=0, columnspan=2, sticky='w')

        frameInput2R = tk.Frame(ventana_secundaria, borderwidth=2, relief=tk.SOLID,width=500,height=400)
        frameInput2R.place(x=450,y=200)
        #MOSTRAR GRAFOS
        
        # Crear un gadget Label y mostrar la imagen
        label = tk.Label(frameInput2R, image=imagen_tk)
        label.place(x=75,y=125)
        
        ################################################3
        
        labelR = tk.Label(frameInput2R, text="A continuación, se muestra el grafo que representa las conexiones entre\nciudades y sus distancias. Se remarcarán los caminos que se utilizaron\npara realizar el envío desde las distintas ciudades con stock hasta la\nciudad de destino.")
        labelR.place(x=50,y=50)

        def salir():
            salir_ventana(ventana_secundaria)

        botonVolver = tk.Button(frameInput2R,text='Volver',bg='light blue',fg='black',width=12,height=1, command=salir)
        # botonVolver.config(borderwidth=10, relief=tk.RAISED)
        botonVolver.place(x=200,y=350)

    
    botonVolver = tk.Button(frameInput2,text='Volver',bg='light blue',fg='black',width=12,height=1,command=salir)
    # botonVolver.config(borderwidth=10, relief=tk.RAISED)
    botonVolver.place(x=120,y=300)
    botonGrafos = tk.Button(frameInput2,text='Grafos',bg='light blue',fg='black',width=12,height=1, command=ventana_Grafos1)
    # botonGrafos.config(borderwidth=10, relief=tk.RAISED)
    botonGrafos.place(x=220,y=300)
    botonRestricciones = tk.Button(frameInput2,text='Restricciones',bg='light blue',fg='black',width=12,height=1, command=ventana_Restricciones)
    # botonGrafos.config(borderwidth=10, relief=tk.RAISED)
    botonRestricciones.place(x=320,y=300)

    ventana_secundaria.mainloop()


#boton para ejecutar la logica
botonEvaluar = tk.Button(frameInput,text='Evaluar',bg='light blue',fg='black',width=12,height=1,command=ventana_respuesta_en_texto)
botonEvaluar.place(x=210,y=350)

ventana.mainloop()