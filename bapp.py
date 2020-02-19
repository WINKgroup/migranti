import pandas as pd
import numpy as np
from bokeh.plotting import figure, output_file, show
from bokeh.io import curdoc, show
from bokeh.models import ColumnDataSource, Slider, HoverTool
from bokeh.models.glyphs import VBar
from bokeh.layouts import widgetbox, column

df1415 = pd.read_csv('mig14-15.csv', usecols=[1, 6, 7, 8, 10])
df1617 = pd.read_csv('mig16-17.csv', usecols=[1, 6, 7, 8, 10])
df1819 = pd.read_csv('mig18-19.csv', usecols=[1, 6, 7, 8, 10])
df = df1415.append(df1617).append(df1819)
df = df[df['Territorio'] == 'Italia']

dfByYear = {}
countries = set()
currYear = 2019

for year in range(2014, 2020):
    currDf = df[df['TIME'] == year]
    currDf = currDf.sort_values(by='Value', ascending=False)
    currDf = currDf.head(20)
    countries.update(list(map(str,currDf['ISO'])))
    dfByYear[year] = currDf

def callback(attr, old, new):
    source.data = {'x':dfByYear[new]['ISO'], 'top': dfByYear[new]['Value'], 'Country': dfByYear[new]['Paese di cittadinanza']}
    
years = list(dfByYear.keys())
slider = Slider(title='', start=years[0], end=years[-1], value=currYear)
slider.on_change('value', callback)

hover = HoverTool(tooltips=[('abitanti', '@top'), ('Paese', '@Country')])

plot = figure(
    title="Cittadini stranieri in Italia", 
    x_range=list(countries), 
    y_range=(0, 1.3e6), 
    plot_height=400, 
    x_axis_label="Sigla Paese",
    y_axis_label="Numero di abitanti",
    tools=[hover, 'pan', 'wheel_zoom', 'box_zoom','save','reset'])
source = ColumnDataSource(data={'x':dfByYear[currYear]['ISO'], 'top': dfByYear[currYear]['Value'], 'Country': dfByYear[currYear]['Paese di cittadinanza']})
plot.vbar(x='x', top='top', source=source, width=0.9)

layout = column(widgetbox(slider), plot)

curdoc().add_root(layout)
show(layout)