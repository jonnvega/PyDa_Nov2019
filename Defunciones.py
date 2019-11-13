import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
 
pd.set_option('display.max_columns', None)

defu_raw = pd.read_excel("C:\\Users\\jonva\\Downloads\\DEFU2016.xlsx")

defu = defu_raw
# defu.head()
# print(defu.info())
# defu_var = pd.read_excel("C:\\Users\\jonva\\Downloads\\DEFU2016.xlsx", sheet_name='ListVariables')
# defu_var = defu_var.drop('Variable', axis=1).drop(defu_var.index[0:4])
# defu_var.columns


defu = defu.drop(defu.index[0]).drop('Variable', axis=1)

# defu.columns

# plt.hist(defu['edads'], bins=30)
# sns.boxplot(x=defu['edads'])

defu['edads'].plot.hist(bins=30, title='Distribución de Defunciones por Edad')
defu.hist(column = 'edads', bins=30, grid=False)
sns.distplot(defu['edads'], kde=False, bins=30)

defu = defu[defu['edads']<150]

# defu.loc[:,['diadef','mesdef','anodef']].head()

defu['fecha_def'] = (defu['anodef']*10000 + defu['mesdef']*100+defu['diadef']).astype(int)

# defu['fecha_def'].head()

defu['fecha_def'] = pd.to_datetime(defu['fecha_def'], format ='%Y%m%d')

defu = defu[defu['anodef'].astype(int)>2013]

# defu['anodef'].value_counts()

# defu['fecha_def'].plot.bar()

sexo_iu = defu.groupby(['sexo', 'iu'])
sexo_iu['edads'].count()

ax = sns.boxplot(x=defu['sexo'], y=defu['edads'])
ax.set(xlabel='Sexo', ylabel='Edad')


defu['provincia_tex'] = defu['provincia'].replace({1:'San Jose',2:'Alajuela', 3:'Cartago', 4:'Heredia', 5:'Guanacaste', 6:'Puntarenas', 7:'Limón'})

plt.figure(figsize=(20,10)) 
plt.xlabel('xlabel', fontsize=30)
plt.ylabel('ylabel', fontsize=16)
ax = sns.boxplot(data=defu, x='provincia_tex', y='edads', hue='sexo', )
legend = plt.legend(title = 'Sexo', loc='upper left', bbox_to_anchor=(1, 1), prop={'size':20})
plt.setp(legend.get_title(),fontsize='20')
ax.set(xlabel='Provincia', ylabel='Edad')
ax.set_title("Defunciones por Edad, Provincia y Sexo", fontsize='40')
ax.tick_params(axis = 'both', which = 'major', labelsize = 20)

defu['causamuer'].value_counts().head(20).plot.bar()



##Categoría de defunción
sns.catplot(y='g18', kind='count', palette="ch:.25", data=defu)

g17 = pd.read_csv("C:\\Users\\jonva\\Desktop\\PyDa\\g17.csv",encoding='latin-1')
g17['g17'].str[7:]

def remove_char(oldstring, oldchar, newchar):
    newstring = oldstring.str.replace(oldchar, newchar)
    return newstring
g17['g17'] = remove_char(g17['g17'].str[7:40],"- ","") ##7:40 para cortar nombres muy largos

g17['numero'] = g17.index+1

defu['g18'] = defu['g17']
cat = 1.0
for i in list(g17['g17']):
    defu['g18'].replace(cat,i,inplace=True)
    cat = cat+1
defu['g18'].value_counts()

sns.catplot(y='g18', kind='count', palette="ch:.25", data=defu)

causa = defu.groupby(['g17','sexo'])
causa['anotrab'].sum()

##nombres son muy largos
defu.groupby('g18')['anotrab'].count()

##cortando los nombres
