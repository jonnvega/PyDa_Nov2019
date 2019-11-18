import requests
from bs4 import BeautifulSoup
import pandas as pd

result = requests.get("https://www.imn.ac.cr/estaciones-automaticas")

print(result.status_code)

print(result.headers)

src = result.content

print(src)

soup = BeautifulSoup(src, 'lxml')

enlaces = soup.find_all("a")

nombres = soup.find_all("td")

cantones = [nombre.text for nombre in nombres if nombre.attrs['width']=='282']

for nombre in nombres:
    if 'width' not in nombre.attrs:
        print(nombres.index(nombre), '\n')

del nombres[0:2]

cantones = [nombre.text for nombre in nombres if nombre.attrs['width']=='282']

cantones
len(cantones)

# print(enlaces)
# print("\n")

estaciones = [enlace.attrs['href'] for enlace in enlaces if "Entrar" in enlace.text]


results_lib = requests.get(estaciones[1])

src_lib = results_lib.content

soup_lib = BeautifulSoup(src_lib,'lxml')

iframe_lib = soup_lib.select("iframe")[0]

tabla_lib = 'https://www.imn.ac.cr'+iframe_lib['src']

def obtener_tabla(enlace):
    
    resultado = requests.get(enlace)
    fuente = resultado.content
    soup = BeautifulSoup(fuente, 'lxml')
    iframe = soup.select('iframe')[0]
    url_tabla = 'https://www.imn.ac.cr'+iframe['src']
    

    resultado_tabla = requests.get(url_tabla)
    fuente_tabla = resultado_tabla.content
    soup_tabla = BeautifulSoup(fuente_tabla, 'lxml')
    tabla_html = soup_tabla.select('table')[0]
    tabla = pd.read_html(str(tabla_html))[0]

    tabla['Canton'] = cantones[estaciones.index(enlace)]

    tabl

    return tabla


obtener_tabla(estaciones[2]).iloc[0]

tablas = list(map(obtener_tabla, estaciones))

for enlace in estaciones:
    resultado = requests.get(enlace)
    fuente = resultado.content
    soup = BeautifulSoup(fuente, 'lxml')
    if not soup.select('iframe'):
        print(estaciones.index(enlace))



del estaciones[31], cantones[31]

len(estaciones)==len(cantones)

tablas = list(map(obtener_tabla, estaciones))



type(tablas[3].iloc[0])

actuales = [tabla.iloc[2], ]


pares = list(zip(cantones, tablas))

pares[3]

