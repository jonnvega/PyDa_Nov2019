import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
 
pd.set_option('display.max_columns', None)
matplotlib.rcParams['font.family'] = "monospace"

#http://sistemas.inec.cr/pad4/index.php/catalog/166/datafile/F1
#diccionario: http://sistemas.inec.cr/pad4/index.php/catalog/166/datafile/F1
#python visualization gallery: https://python-graph-gallery.com/ 

defu_raw = pd.read_excel("C:\\Users\\jonva\\GitHub\\PyDa_Nov2019\\DEFU2016.xlsx")

defu = defu_raw
#defu.shape
# defu.head()
# defu.tail()
# defu.info()

defu = defu.drop(defu.index[0]).drop('Variable', axis=1)

# defu.columns
# defu.dtypes

# defu[(defu['instmurio']==3) & (defu['g62']==2)]

# df[(df['col1'] >= 3) & (df['col1'] <=1 )]

# defu['edads'].plot.hist(bins=30, title='Distribución de Defunciones por Edad')

# sns.boxplot(x=defu['edads'])

# defu.groupby('edads').count().iloc[:,0]

# defu.hist(column = 'edads', bins=30, grid=False)
# sns.distplot(defu['edads'], kde=False, bins=30)

defu = defu[defu['edads']<150]

# defu.loc[:,['diadef','mesdef','anodef']].head()

defu['fecha_def'] = (defu['anodef']*10000 + defu['mesdef']*100+defu['diadef'])

# defu['fecha_def'].head()

defu['fecha_def'] = pd.to_datetime(defu['fecha_def'], format ='%Y%m%d')

defu = defu[defu['anodef'].astype(int)==2016]


# defu.groupby([defu['fecha_def'].dt.year, defu['fecha_def'].dt.month]).count()['anotrab'].plot(kind='bar')
# defu.groupby(defu['fecha_def'].dt.month).count()['anotrab'].plot(kind='bar')


sexo_iu = defu.groupby(['sexo', 'iu'])
# sexo_iu['edads'].count()
# sexo_iu['edads'].count().reset_index()

# ax = sns.boxplot(x=defu['sexo'], y=defu['edads'],)
# ax.set(xlabel='Sexo', ylabel='Edad')

defu['provincia_tex'] = defu['provincia'].replace({1:'San Jose',2:'Alajuela', 3:'Cartago', 4:'Heredia', 5:'Guanacaste', 6:'Puntarenas', 7:'Limón'})

# defu['provincia_tex'].value_counts()
# defu['provincia_tex'].value_counts(normalize=True)


plt.figure(figsize=(10,5)) 
plt.xlabel('xlabel', fontsize=30)
plt.ylabel('ylabel', fontsize=30)
ax = sns.boxplot(data=defu, x='provincia_tex', y='edads', hue='sexo', )
plt.legend(title = 'Sexo', bbox_to_anchor=(1, 1), prop={'size':10})
plt.xlabel('Provincia', fontsize=18)
plt.ylabel('Edad', fontsize=16)
ax.set_title("Defunciones por Edad, Provincia y Sexo", fontsize='20')
ax.tick_params(axis = 'both', labelsize = 12)



fig, ax = plt.subplots(figsize=(15, 15))
ax = sns.violinplot(x="provincia_tex", y="edads",  data=defu, cut = 0)
ax.set_xlabel("Sexo",size = 20,alpha=0.8)
ax.set_ylabel("Edad",size = 20,alpha=0.8)
ax.set_title("Defunciones por Edad y Sexo",size=20)
ax.tick_params(axis = 'both', labelsize = 20)



##Categoría de defunción
# defu['g17'].value_counts().head(20).plot.bar()

g17 = pd.read_csv("C:\\Users\\jonva\\GitHub\\PyDa_Nov2019\\Datos\\g17.csv",encoding='latin-1')
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

g18_count = defu.groupby('g18').count().reset_index()

g18_count.sort_values(by='edads',ascending=False)[['g18','edads']]

ax = sns.barplot(x='edads', y='g18', palette="ch:.25", data=g18_count)
ax.set(xlabel='Edad', ylabel='Causa de Defunción', title='Defunciones por edad según causa de defunción')


defu.groupby(['g18', 'provincia_tex']).count().reset_index().pivot(index='provincia_tex', columns='g18', values='anotrab')

ax = sns.heatmap(defu.groupby(['g18', 'provincia_tex']).count().reset_index().pivot(index='provincia_tex', columns='g18', values='anotrab'))

##nombres son muy largos
defu.groupby('g18')['anotrab'].count()


g18_instmurio = defu[defu['provincia_tex']=='Limón'].groupby(['g18', 'instmurio'])['anotrab'].count().reset_index()

g18_instmurio = g18_instmurio[g18_instmurio['anotrab']>10]

g18_instmurio.pivot(columns='g18', index='instmurio').plot(kind='bar', stacked=True)
plt.legend(title = 'Sexo', bbox_to_anchor=(1, 1), prop={'size':10})

