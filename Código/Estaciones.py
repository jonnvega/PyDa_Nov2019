import requests
from bs4 import BeautifulSoup
import pandas as pd
import numpy as np
import time

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

estaciones = [enlace.attrs['href'] for enlace in enlaces if "Entrar" in enlace.text]

# len(estaciones)==len(cantones)==len(nombres)

# results_lib = requests.get(estaciones[1])

# src_lib = results_lib.content

# soup_lib = BeautifulSoup(src_lib,'lxml')

# iframe_lib = soup_lib.select("iframe")[0]

# tabla_lib = 'https://www.imn.ac.cr'+iframe_lib['src']

# resultado_tabla_lib = requests.get(tabla_lib)
# fuente_tabla_lib = resultado_tabla_lib.content
# soup_tabla_lib = BeautifulSoup(fuente_tabla_lib, 'lxml')
# tabla_html_lib = soup_tabla_lib.select('table')[0]
# tabla_lib = pd.read_html(str(tabla_html_lib))[0]

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

for enlace in estaciones:
    resultado = requests.get(enlace)
    fuente = resultado.content
    soup = BeautifulSoup(fuente, 'lxml')
    iframe = soup.select('iframe')[0]
    url_tabla = 'https://www.imn.ac.cr'+iframe['src']
    resultado_tabla = requests.get(url_tabla)
    fuente_tabla = resultado_tabla.content
    soup_tabla = BeautifulSoup(fuente_tabla, 'lxml')
    if not soup_tabla.select('table'):
        print(estaciones.index(enlace),"\n")

del estaciones[6], cantones[6], nombres[6]

for enlace in estaciones:
    resultado = requests.get(enlace)
    fuente = resultado.content
    soup = BeautifulSoup(fuente, 'lxml')
    if not soup.select('iframe'):
        print(estaciones.index(enlace),"\n")

del estaciones[29], cantones[29], nombres[29]

tablas = list(map(obtener_tabla, estaciones))

temp_actual = pd.DataFrame(columns=['Estacion', 'Canton','Fecha','Temp', 'Lluvia'],index=None)

for tabla in tablas:
    temp_actual = pd.concat([temp_actual,tabla.loc[[0],['Estacion','Canton','Fecha','Temp', 'Lluvia']]],ignore_index=True)

temp_actual.head()
temp_actual.shape

# temp_actual.isna().sum()
temp_actual.dropna(axis='index', how='any', inplace=True)
temp_actual = temp_actual.reset_index()
temp_actual.drop('index', axis=1, inplace=True)
# temp_actual.dtypes

temp_actual['Temp'] = temp_actual['Temp'].astype(float)

temp_actual['Temp'] = temp_actual['Temp'].apply(lambda x : x/100 if x>100 else x)    


from selenium import webdriver

print(temp_actual['Estacion'])

Cantones = pd.Series(temp_actual['Canton'].unique())


lat_list = []
lon_list = []

browser = webdriver.Chrome("C:\\Users\\jonva\\Downloads\\chromedriver")
browser.get('https://www.coordenadas-gps.com/mapa/pais/CR')

for canton in Cantones:
    try:
        direccion = browser.find_element_by_id('address')
        direccion.send_keys(canton)
        browser.find_element_by_class_name('btn').click()
        time.sleep(5)
        latitud = browser.find_element_by_id('latitude')
        lat_value = str(latitud.get_attribute('value'))
        longitud = browser.find_element_by_id('longitude')
        lon_value = str(longitud.get_attribute('value'))
        lat_list.append(lat_value)
        lon_list.append(lon_value)
    except:
        lat_value = np.nan
        lon_value = np.nan
        lat_list.append(lat_value)
        lon_list.append(lon_value)
    browser.find_element_by_id('address').clear()


len(lat_list)==len(lon_list)==len(Cantones)

cantones_coor = pd.DataFrame(columns=['Canton', 'Latitud', 'Longitud'],index=None)
cantones_coor['Canton'] = Cantones
cantones_coor['Latitud'] = lat_list
cantones_coor['Longitud'] = lon_list

cantones_coor.head()
cantones_coor[cantones_coor['Latitud'].isnull()].index.tolist()

cantones_coor.loc[17,'Latitud'] = 10.103415
cantones_coor.loc[17,'Longitud'] = -85.4153082


from bokeh.plotting import figure, show, output_notebook
from bokeh.tile_providers import CARTODBPOSITRON
p = figure(x_range=(-9780000, -9745000), y_range=(5130000, 5160000),
           x_axis_type="mercator", y_axis_type="mercator")
p.add_tile(CARTODBPOSITRON)
output_notebook()
show(p)