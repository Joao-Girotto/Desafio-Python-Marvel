from auxiliary import plot
import pandas as pd

# Analisa a quantidade de series por ano e retorna um dataframe
def series_by_year(dataframe, show_plot=False):
  series_year = (
      dataframe[(dataframe['startYear'] > 0) &
                (dataframe['startYear'] < 2029)]
                ['startYear']
                .value_counts()
                .sort_index()
      )

  if show_plot:
    plot(
      dataframe=series_year,
      title='Séries por Década',
      x_label='Década',
      y_label='Quantidade de Séries',
      figsize=(20, 6)
    )

  return series_year

# Analisa a média de duração das series e retorna um dataframe
def series_average_duration(dataframe, show_plot=False):
  anos_series = (
      dataframe[(dataframe['duration'] >= 0) &
                (dataframe['duration'] < 999)]
                ['duration']
                .value_counts()
                .sort_index()
                .head(10)
      )

  if show_plot:
    plot(
      dataframe=anos_series,
      title='Series: Média da duração das series',
      x_label='Duração (anos)',
      y_label='Quantidade de séries'
   )

  media = (
      dataframe[(dataframe['duration'] >= 0) &
                (dataframe['duration'] < 999)]
                ['duration']
                .mean()
      ) ## 999 definido para séries em produção
  return anos_series, media

# Analisa a distribuição das classificações etárias de series
# e retorna um dataframe
def series_distribution_rating(dataframe, show_plot=False):
  media = dataframe[dataframe['rating'] != '']['rating'].value_counts()

  if show_plot:
    plot(
      dataframe=media,
      x_label='Classificação etária',
      y_label='Quantidade de séries',
      title='Distribuição classificatória de faixa etária'
    )

  return media

# Analisa a distribuição dos tipos de series e retorna um dataframe
def series_distribuition_type(dataframe, show_plot=False):
  series_type = dataframe[dataframe['type'] != '']['type'].value_counts()

  if show_plot:
    plot(
      dataframe=series_type,
      x_label='Tipo',
      title='Distribuição dos tipos de séries',
      y_label='Quantidade de séries'
    )

  return series_type

# Analisa a quantidade de personagens por ano de series e retorna um dataframe
def series_quantity_characters_year(dataframe, show_plot=False):
  tempo = (
      dataframe[
          (dataframe['character_qty'] > 0) &
          (dataframe['startYear'] > 1900) &
          (dataframe['startYear'] < 2029)]
          .groupby('startYear')
          ['character_qty']
          .sum()
        )

  falta_anos = pd.Series(0, index=range(1939, 2025))
  arrumado =  falta_anos.add(tempo, fill_value=0)

  if show_plot:
    plot(
        dataframe=arrumado,
        title='Quantidade de personagens por ano',
        x_label='Ano',
        y_label='Quantidade de personagens',
        figsize=(20, 6)
    )

  return arrumado


