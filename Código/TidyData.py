import pandas as pd
import numpy as np

ruta  = "Copia_de_SociedadesMorosasIPJ2017_2018_2019_al_26022019.xlsx" #ruta del archivo
morosos = pd.read_excel(ruta)

morosos.shape #tamaño del conjunto de datos 

morosos.head() #mostrar las primeras 10 filas

morosos.tail(10) ##últimas filas

morosos.isna().sum() ##mostrar los valores nulos

##borrar los últimos 5 valores
morosos.drop(morosos.tail(5).index, inplace=True)

##borrar columnas innecesarias
morosos = morosos.drop(morosos.columns[[7,8,9,10]], axis=1)  

##mostrar los valores con más observaciones 
for col in morosos.columns:
    print(col, "\n", morosos[col].value_counts().head(10), "\n") ##omiso renta 

##Omiso renta no es un número, hay que convertirlo a NA
columns = ['Monto Deuda 2017', 'Monto Deuda 2018', 'Monto Deuda 2019']

for col in columns:
    morosos[col] = morosos[col].replace('Omiso Renta', np.nan)

morosos.head()

##Para las columnas de monto, se deben derretir a una sola
##ya que están en formato de pivot
morosos_melt = pd.melt(morosos, id_vars=("Cedula", 
                                         "Nombre", 
                                         "Nombre del representante legal", 
                                         "Cédula representante legal"), 
                       var_name="Periodo", 
                       value_name='Deuda')

morosos_melt.head()

##remplazar los valores por año
morosos_melt['Periodo'] = morosos_melt["Periodo"].replace(["Monto Deuda 2017", 
                                                "Monto Deuda 2018", 
                                                "Monto Deuda 2019"], 
                                               [2017, 2018, 2019])

morosos_melt.head()

#tipos de datos
morosos_melt.dtypes

##agrupar los valores por año
grupo_morosos = morosos_melt['Deuda'].groupby(morosos_melt['Periodo'])
grupo_morosos.sum()


morosos_melt.loc[:,['Nombre', 'Deuda']][morosos_melt['Periodo']==2017].sort_values(by='Deuda',
                                                                                   ascending=False).head(10)

import matplotlib

morosos_melt.query('Periodo == 2017')

morosos_melt['Deuda'][morosos_melt['Periodo']==2017].hist(bins=100)

