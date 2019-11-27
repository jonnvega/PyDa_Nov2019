import pandas as pd
import numpy as np
import pandas_profiling

from bokeh.plotting import figure
from bokeh.io import output_file, output_notebook, save, show
from bokeh.models import ColumnDataSource
from bokeh.models.tools import HoverTool

pd.set_option('display.max_columns', None)

constru_2017 = pd.read_excel('C:\\Users\\jonva\\GitHub\\PyDa_Nov2019\\Datos\\Construcciones_2017.xlsx',)

constru_2017.shape
constru_2017.head()
constru_2017.isna().sum()
constru_2017.info()

constru_2017[constru_2017['arecon']==0]

src=constru_2017

sns
p = figure( plot_width = 600, 
            plot_height=600, 
            title = "M2 construcción por valor de la obra", x_axis_label='M2 Construcción', 
            y_axis_label='Valor Obra')


p.add_tools(HoverTool(tooltips=[("Area", "@x"), ("Valor","@y")]))

p.circle(src['arecon'], src['valobr'], size=7, color='blue')
p.left[0].formatter.use_scientific = False
p.below[0].formatter.use_scientific = False
output_file('constru_bokeh.html')
show(p)

constru_2017.groupby('canton').count().reset_index().iloc[:,0:2]




per_canton = constru_2017[constru_2017['arecon']>0].groupby(['canton','claobr']).count().reset_index().iloc[:,0:3]
# per_canton.shape

output_file("per_canton.html")

p = figure( x_range = 'canton', 
            plot_width = 600, 
            plot_height=600, 
            title = "Cantones por tipo de permisos", x_axis_label='Canton', 
            y_axis_label='Permisos',
            toolbar_location = None, 
            tools="hover", tooltips="$name @canton: @$name")

p.vbar_stack(list[per_canton[]], x='fruits', width=0.9, color=colors, source=data,
             legend_label=years)





            




