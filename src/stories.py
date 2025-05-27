import pandas as pd
from google.colab import userdata
import matplotlib.pyplot as plt
import matplotlib.cm as cm
import numpy as np
import regex as re
import plotly.express as px
# Calcula a quantidade de cada tipo de stories e retorna um dataframe
def stories_quantity_type(dataframe, show_plot=False):
  types = dataframe[dataframe['type'] != '']
  clean_types = types['type'].value_counts()
  if show_plot:

    fig = px.bar(
        clean_types,
        x=clean_types.index,
        y=clean_types.values,
        labels={'x': 'Tipo', 'y': 'Quantidade'},
        title='Quantidade de cada tipo',
        color_discrete_sequence=['purple']
    )

    fig.update_layout(
        xaxis_title='Tipos',
        yaxis_title='Quantidade',
        xaxis_tickangle=-45
    )

    fig.show()

  return types