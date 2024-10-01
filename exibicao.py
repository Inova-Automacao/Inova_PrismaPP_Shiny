from shinywidgets import render_plotly
from shiny import render, ui
import plotly.express as px

def exibe_tabela(data):
    return render.DataGrid(data, width='100%')

def exibe_grafico_barras(data, namex,namey):
    fig = px.bar(data, x=namex, y=namey)
    return fig

def exibe_texto(text):
    return text