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
# from graphviz import Digraph


# ───────────────────────────────────────────────────────────
# :::::::::::::::::::::::::: Excel ::::::::::::::::::::::::::
# ───────────────────────────────────────────────────────────

# Leemos el archivo Excel Paises latinoamericanos en un DataFrame de pandas
df = pd.read_excel(io='paises prueba.xlsx',
                   sheet_name='Hoja1', header=0, names=None, index_col=None, usecols='A,B,D,E,F,J', engine='openpyxl')

# Imprime las primeras 3 filas del dataframe
#print(df.head(3))


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

def dijkstra(graph, start):
    distances = {node: float('inf') for node in graph}
    distances[start] = 0
    queue = [(0, start)]

    while queue:
        current_distance, current_node = heapq.heappop(queue)

        if current_distance > distances[current_node]:
            continue

        for neighbor, weight in graph[current_node].items():
            distance = current_distance + weight
            if distance < distances[neighbor]:
                distances[neighbor] = distance
                heapq.heappush(queue, (distance, neighbor))

    return distances


def drawG_am(G, directed=False, weighted=False, path=[], layout="sfdp"):
    graph = gv.Digraph("digrafo") if directed else gv.Graph("grafo")
    graph.graph_attr["layout"] = layout
    graph.edge_attr["color"] = "gray"
    graph.node_attr["color"] = "orangered"
    graph.node_attr["width"] = "0.1"
    graph.node_attr["height"] = "0.1"
    graph.node_attr["fontsize"] = "8"
    graph.node_attr["fontcolor"] = "mediumslateblue"
    graph.node_attr["fontname"] = "monospace"
    graph.edge_attr["fontsize"] = "8"
    graph.edge_attr["fontname"] = "monospace"
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
    return graph

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

    shortest_distances = {}
    for city_id in cities:
        distances = dijkstra(graph, city_id)
        shortest_distances[city_id] = distances[destination]

    sorted_cities = sorted(cities, key=lambda city: shortest_distances[city])

    total_supplies = 0
    sending_cities = []
    distances_to_destination = {}
    supplies_sent={}
    for city_id in sorted_cities:
        if total_supplies >= demand:
            break

        if cities[city_id] > 0:
            sending_cities.append(city_id)
            supplies_to_send = min(demand - total_supplies, cities[city_id])
            total_supplies += supplies_to_send
            cities[city_id] -= supplies_to_send
            supplies_sent[city_id]=supplies_to_send
            distances_to_destination[city_id] = shortest_distances[city_id] if shortest_distances[city_id] != math.inf else -1

    return sending_cities, distances_to_destination, supplies_sent




###################################################################################################
###################################################################################################


#ventana principal-----------------------
ventana = tk.Tk()
ventana.title("Complejidad Algoritmica")
ventana.geometry("1728x1117")

#Dato global
bold_font = font.Font(weight="bold")#este hace negrita el texto
#----------------------------------------

#header-----------------------------------------------------------------------------------------------------
parte_superior = tk.Frame(ventana, width=1728,height=75,background='cyan')
parte_superior.grid(row=0,column=0)

titulo = tk.Label(ventana, text="Cadena de suministros",background='cyan',font=('arial',20),fg='white')
titulo.grid(row=0, column=0, columnspan=2, sticky='w')
#-----------------------------------------------------------------------------------------------------------


#funcion que lee archivo de excel que contengan las ciudades
def lecturaArch():

    archivo = 'worldcities.xlsx'
    df = pd.read_excel(archivo, sheet_name='Hoja1')
    return df

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

#FRAME DONDE INGRESAMOS DATOS
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




#OBTENIENDO DATOS DEL TEXT#####################
def almacenesYsuministros():
    contenido1 = input1.get("1.0", tk.END)

    # return f'datos1 {contenido1}'
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

def ventana_Grafos():

   

    ventana_secundaria = tk.Toplevel(ventana)
    ventana_secundaria.title(" Grafos ")
    ventana_secundaria.geometry("1728x1117")

    #header
    parte_superior2 = tk.Frame(ventana_secundaria, width=1728,height=75,background='cyan')
    parte_superior2.grid(row=0,column=0)

    lListaR= tk.Label(ventana_secundaria,text='Grafo recorrido', font=bold_font)
    lListaR.place(x=650,y=170)


    #titulo del header
    titulo2 = tk.Label(ventana_secundaria, text="Cadena de suministros",background='cyan',font=('arial',20),fg='white')
    titulo2.grid(row=0, column=0, columnspan=2, sticky='w')

    frameInput2R = tk.Frame(ventana_secundaria, borderwidth=2, relief=tk.SOLID,width=500,height=400)
    frameInput2R.place(x=450,y=200)
    #GRAFOS
    # grafos = drawG_am(matriz_distancias, weighted=True)
    # grafos.format('jpg')
    # grafos.render('temp_grafo', view=False)
    # imagen_grafo = tk.PhotoImage(file='temp_grafo.jpg')

    # labelGrafo = tk.Label(frameInput2R)
    # #labelGrafo.pack()
    # labelGrafo.configure(image=imagen_grafo)
    # labelGrafo.image = imagen_grafo
    ################################################3
    
    labelR = tk.Label(frameInput2R, text="A continuación, se muestra el grafo que representa las conexiones entre\nciudades y sus distancias. Se remarcarán los caminos que se utilizaron\npara realizar el envío desde las distintas ciudades con stock hasta la\nciudad de destino.")
    labelR.place(x=57,y=25)
    # inputR=tk.Text(frameInput2R,width=30, height=5)
    # inputR.place(x=150,y=140)

    def salir():
        salir_ventana(ventana_secundaria)


    botonVolver = tk.Button(frameInput2R,text='Volver',bg='cyan',fg='white',width=12,height=1, command=salir)
    # botonVolver.config(borderwidth=10, relief=tk.RAISED)
    botonVolver.place(x=140,y=350)

    botonGrafos = tk.Button(frameInput2R,text='Restricciones',bg='cyan',fg='white',width=12,height=1)
    # botonGrafos.config(borderwidth=10, relief=tk.RAISED)
    botonGrafos.place(x=285,y=350)
    

def ventana_Restricciones():
    ventana_secundaria = tk.Toplevel(ventana)
    ventana_secundaria.title(" Restricciones ")
    ventana_secundaria.geometry("1728x1117")

    #header
    parte_superior2 = tk.Frame(ventana_secundaria, width=1728,height=75,background='cyan')
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
    titulo2 = tk.Label(ventana_secundaria, text="Cadena de suministros",background='cyan',font=('arial',20),fg='white')
    titulo2.grid(row=0, column=0, columnspan=2, sticky='w')

    frameInputR = tk.Frame(ventana_secundaria, borderwidth=2, relief=tk.SOLID,width=500,height=400)
    frameInputR.place(x=500,y=200)
    labelR = tk.Label(frameInputR, text="Ciudades que se encuentran\nrestringuidos por diversos motivos")
    labelR.place(x=145,y=50)
    inputR=tk.Text(frameInputR,width=30, height=5)
    inputR.place(x=130,y=90)

    def salir():
        salir_ventana(ventana_secundaria)

    botonVolver = tk.Button(frameInputR,text='Inicio',bg='cyan',fg='white',width=12,height=1, command=salir)
    # botonVolver.config(borderwidth=10, relief=tk.RAISED)
    botonVolver.place(x=130,y=180)

    botonGrafos = tk.Button(frameInputR,text='Evaluar',bg='cyan',fg='white',width=12,height=1)
    # botonGrafos.config(borderwidth=10, relief=tk.RAISED)
    botonGrafos.place(x=280,y=180)
    


#para mostrar la otra ventana
def mostrar_ventana():

    #ventana secundaria
    ventana_secundaria = tk.Toplevel(ventana)
    ventana_secundaria.title("Ventana Secundaria")
    ventana_secundaria.geometry("1728x1117")

    #header
    parte_superior2 = tk.Frame(ventana_secundaria, width=1728,height=75,background='cyan')
    parte_superior2.grid(row=0,column=0)

    #titulo del header
    titulo2 = tk.Label(ventana_secundaria, text="Cadena de suministros",background='cyan',font=('arial',20),fg='white')
    titulo2.grid(row=0, column=0, columnspan=2, sticky='w')

    frameInput2 = tk.Frame(ventana_secundaria, borderwidth=2, relief=tk.SOLID,width=500,height=400)
    frameInput2.place(x=450,y=200)

    subtitulo= tk.Label(frameInput2,text='Para abastecer a la ciudad “31 - La Paz”, debes enviar los suministros\ndesde las siguientes ciudades, ya que son las más cercanas y las mínimas\nnecesarias para completar los suministros solicitados:')
    subtitulo.place(x=55,y=45)

    subtitulo2 = tk.Label(frameInput2, text="id - nombre - distancia - suministros enviados")
    subtitulo2.place(x=130,y=170)

    ###############################################3
    #almacenesYsuministros()
    #obtener_ID()
    #obtener_ID()
    datosRelevantes = almacenesYsuministros()
    datosRelevantes2 = datosRelevantes.splitlines()
    # print(f'CONSOLA PE\n{datosRelevantes2}')
    # print(type(datosRelevantes2))
    origin_cities = datosRelevantes2
    destination = int ( obtener_ID() )
    demand = int ( obtener_suministro() )

    # print(f'id: {type(destination)}\nsuministro: {type(demand)}')

    #########################################################
    text = tk.Text(frameInput2,width=50, height=5)
    text.place(x=80,y=200)
   
    # text.insert(tk.END, almacenesYsuministros())#datos de ejemplo por optimizar
    # text.insert(tk.END, obtener_ID())
    # text.insert(tk.END, obtener_ID())
    # text.insert(tk.END, "Dato 2\n")#datos de ejemplo por optimizar
    #########################################################



    """OUTPUT RESULTADO"""
    #sending_cities, distances_to_destination = shortest_route(matriz_distancias, origin_cities, destination, demand)

    sending_cities, distances_to_destination, supplies_sent = shortest_route(matriz_distancias, origin_cities, destination, demand)

    # print("Ciudades desde las cuales se deben enviar los suministros:")
    # for city in sending_cities:
    #     # print(f"Ciudad {city}: Distancia a recorrer {distances_to_destination[city]} km")
    #     text.insert(tk.END, f"Ciudad {city}: Distancia a recorrer {distances_to_destination[city]} km")


    print("Ciudades desde las cuales se deben enviar los suministros:")
    for city in sending_cities:
        if distances_to_destination[city] == -1:
              text.insert(tk.END,f"Ciudad {city}: No hay ruta hacia el destino")
        else:
              text.insert(tk.END,f"Ciudad {city}: Distancia a recorrer {distances_to_destination[city]} km - {supplies_sent[city]} suministros a enviar ")


    ###############################################3
    #dot = drawG_am(matriz_distancias, weighted=True)
    # ggg.render('grafo', format='pdf')
    #dot.render('grafo', format='pdf')


    ################################################
    def salir():
        salir_ventana(ventana_secundaria)


    botonVolver = tk.Button(frameInput2,text='Volver',bg='cyan',fg='white',width=12,height=1,command=salir)
    # botonVolver.config(borderwidth=10, relief=tk.RAISED)
    botonVolver.place(x=120,y=260)

    botonGrafos = tk.Button(frameInput2,text='Grafos',bg='cyan',fg='white',width=12,height=1, command=ventana_Grafos)
    # botonGrafos.config(borderwidth=10, relief=tk.RAISED)
    botonGrafos.place(x=220,y=260)

    botonRestricciones = tk.Button(frameInput2,text='Restricciones',bg='cyan',fg='white',width=12,height=1, command=ventana_Restricciones)
    # botonGrafos.config(borderwidth=10, relief=tk.RAISED)
    botonRestricciones.place(x=320,y=260)


    #llamamos a la funcion para obtener datos
    print(obtener_suministro())
    print(obtener_ID())
    print(almacenesYsuministros())

    ventana_secundaria.mainloop()


#boton para ejecutar la logica
botonEvaluar = tk.Button(frameInput,text='Evaluar',bg='cyan',fg='white',width=12,height=1,command=mostrar_ventana)
botonEvaluar.place(x=210,y=350)

ventana.mainloop()