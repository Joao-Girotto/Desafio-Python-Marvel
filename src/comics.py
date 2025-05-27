import matplotlib.pyplot as plt
import requests
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.cm as cm
import numpy as np
import regex as re
import plotly.express as px
from auxiliary import plot
# Calcula a quantidade de cada formato de comics e retorna um dataframe
def comics_count_format(dataFrame, show_plot=False):
  format = dataFrame[dataFrame['format'] != '']['format'].value_counts()

  if show_plot:

    fig = px.bar(
        format,
        x=format.index,
        y=format.values,
        labels={'x': 'Formato', 'y': 'Quantidade de comics'},
        title='Quantidade de cada tipo',
        color_discrete_sequence=['purple']
    )

    fig.update_layout(
        xaxis_title='Formato',
        yaxis_title='Quantidade de comics',
        xaxis_tickangle=-45
    )

    fig.show()

  return format

# Calcula a média de preço das comics sobre o tempo e retorna um dataframe
def comics_average_price_over_time(dataframe, show_plot=False):
  def extract_number(text):
    match = re.findall(r'\d+', text)
    return int(match[0]) if match else None

  dataframe['year'] = dataframe['title'].apply(extract_number)
  price_over_time = dataframe[['year', 'price']]

  price_over_time = price_over_time[(price_over_time['year'] > 1900) &
                                    (price_over_time['year'] < 2050)]

  price_filter = price_over_time.query('price > 0 and price < 20').copy()
  price_filter = price_filter.dropna()
  price_filter_average = price_filter.groupby('year').mean()

  if show_plot:
    plt.figure(figsize=(20, 6))

    plt.plot(
        price_filter_average.index,
        price_filter_average['price'],
        color='purple',
        label='Preço Médio'
    )

    plt.scatter(
        price_filter['year'],
        price_filter['price'],
        color='grey',
        label='Preços individuais',
        alpha=0.4,
        s=10
    )

  return price_filter_average

# Calcula a média de páginas das comics sobre o tempo e retorna um dataframe
def comics_average_pages_over_time(dataframe, show_plot=False):
  def extract_number(text):
    match = re.findall(r'\d+', text)
    return int(match[0]) if match else None

  dataframe['year'] = dataframe['title'].apply(extract_number)
  pages_over_time = dataframe[['year', 'pageCount']]

  pages_over_time = pages_over_time[(pages_over_time['year'] > 1900) &
                                    (pages_over_time['year'] < 2050)]

  pages_filter = pages_over_time.query('pageCount > 0 and pageCount < 200')
  pages_filter = pages_filter.dropna()
  pags_filter_average = pages_filter.groupby('year').mean()

  if show_plot:

    plot(
      dataframe=pags_filter_average,
      title='Média de páginas',
      x_label='Ano',
      y_label='Média de páginas',
      kind='line'
    )

  return pags_filter_average
