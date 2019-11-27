import requests
from bs4 import BeautifulSoup
import pandas as pd
import numpy as np

result = requests.get("https://www.imn.ac.cr/estaciones-automaticas")

# print(result.status_code)

# print(result.headers)

src = result.content

# print(src)

soup = BeautifulSoup(src, 'lxml')


td = soup.find_all("td")

# for nombre in nombres:
#     if 'width' not in nombre.attrs:
#         print(nombres.index(nombre), '\n')

del td[0:2]

cantones = [t.text for t in td if t.attrs['width']=='282']

nombres = [t.text for t in td if t.attrs['width']=='244']

enlaces = soup.find_all("a")

# print(enlaces)
# print("\n")

estaciones = [enlace.attrs['href'] for enlace in enlaces if "Entrar" in enlace.text]

# len(estaciones)==len(cantones)==len(nombres)

# results_lib = requests.get(estaciones[1])

# src_lib = results_lib.content

# soup_lib = BeautifulSoup(src_lib,'lxml')

# iframe_lib = soup_lib.select("iframe")[0]

# tabla_lib = 'https://www.imn.ac.cr'+iframe_lib['src']

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
    tabla['Estacion'] = nombres[estaciones.index(enlace)]

    return tabla


# obtener_tabla(estaciones[2]).iloc[0]

# tablas = list(map(obtener_tabla, estaciones))

# for enlace in estaciones:
#     resultado = requests.get(enlace)
#     fuente = resultado.content
#     soup = BeautifulSoup(fuente, 'lxml')
#     if not soup.select('iframe'):
#         print(estaciones.index(enlace))

del estaciones[31], cantones[31]

tablas = list(map(obtener_tabla, estaciones))

temp_actual = pd.DataFrame(columns=['Estacion', 'Canton','Fecha','Temp', 'Lluvia'],index=None)

for tabla in tablas:
    temp_actual = pd.concat([temp_actual,tabla.loc[[0],['Estacion','Canton','Fecha','Temp', 'Lluvia']]],ignore_index=True)

# temp_actual.isna().sum()
temp_actual.dropna(axis='index', how='any', inplace=True)

# temp_actual.dtypes

temp_actual['Temp'] = temp_actual['Temp'].astype(float)

temp_actual['Temp'] = temp_actual['Temp'].apply(lambda x : x/100 if x>100 else x)    

# temp_actual.head()


from selenium import webdriver

browser = webdriver.Chrome("C:\\Users\\jonva\\Downloads\\chromedriver")

browser.get('https://www.coordenadas-gps.com/mapa/pais/CR')
dirrecion = browser.find_element_by_id('address')
dirrecion.send_keys(temp_actual[1,'Estacion'])
browser.find_element_by_class_name('btn').click()
latitud = browser.find_element_by_id('latitude')
latitud.get_attribute('value')
longitud = browser.find_element_by_id('longitude')
longitud.get_attribute('value')