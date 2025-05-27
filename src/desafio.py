import requests
import hashlib
import os
import time
import pandas as pd
import sqlite3
import json
from google.colab import userdata
import matplotlib.pyplot as plt
import matplotlib.cm as cm
import numpy as np
import regex as re
import plotly.express as px
from desafio import *
from events import *
from auxiliary import *
from characters import *
from comics import *
from creators import *
from series import *
from stories import *
## Pegando as chaves

PRIVATE_KEY = userdata.get("Private_Key")
PUBLIC_KEY = userdata.get("Public_Key")

## Endpoints e Parâmetros

ts = str(time.time())
to_hash = ts + PRIVATE_KEY + PUBLIC_KEY
hash_md5 = hashlib.md5(to_hash.encode()).hexdigest()

endCharacters = "https://gateway.marvel.com/v1/public/characters"
endComics = "https://gateway.marvel.com/v1/public/comics"
endSeries = "https://gateway.marvel.com/v1/public/series"
endCreators = "https://gateway.marvel.com/v1/public/creators"
endEvents = "https://gateway.marvel.com/v1/public/events"
endStories = "https://gateway.marvel.com/v1/public/stories"

params = {
    "apikey": PUBLIC_KEY,
    "ts": ts,
    "hash": hash_md5,
    "limit": 10
}

## Pegando o total de requisições

totalCharacters = requests.get(endCharacters, params=params)
totalCharacters = totalCharacters.json()
total = totalCharacters['data']['total']

totalEvents = requests.get(endEvents, params=params)
totalEvents = totalEvents.json()
totalE = totalEvents['data']['total']

totalCreators = requests.get(endCreators, params=params)
totalCreators = totalCreators.json()
totalC = totalCreators['data']['total']

totalSeries = requests.get(endSeries, params=params)
totalSeries = totalSeries.json()
totalSe = totalSeries['data']['total']

totalComics = requests.get(endComics, params=params)
totalComics = totalComics.json()
totalCo = totalComics['data']['total']

totalStories = requests.get(endStories, params=params)
totalStories = totalStories.json()
totalSt = totalStories['data']['total']

## Chamando as requisições

# Characters
df_characters = requisition(endCharacters, total, step=100, limit=100, params_base=params)
create_csv(df_characters, 'Characters.csv')

# Events
df_events = requisition(endEvents, totalE, step=10, limit=10, params_base=params)
create_csv(df_events, 'Events.csv')

# Creators
df_creators = requisition(endCreators, totalC, step=100, limit=100,  params_base=params)
create_csv(df_creators, 'Creators.csv')

## Realizando Converções

df_characters = df_characters[['name', 'id', 'description', 'comics', 'thumbnail']]
df_events = df_events[['title', 'id', 'description', 'characters', 'creators', 'comics', 'start', 'end', 'modified']]
df_creators = df_creators[['id', 'firstName', 'middleName', 'lastName', 'fullName', 'suffix', 'thumbnail','comics', 'events', 'stories', 'series']]
df_characters['comics_available'] = df_characters['comics'].apply(lambda x: x.get('available'))
df_characters['comics_returned'] = df_characters['comics'].apply(lambda x: x.get('returned'))
df_characters['thumbnail_path'] = df_characters['thumbnail'].apply(lambda x: x.get('path'))
df_characters['comics'] = df_characters['comics'].apply(lambda x: json.dumps(x))
df_characters['thumbnail'] = df_characters['thumbnail'].apply(lambda x: json.dumps(x))
df_events['comics_available'] = df_events['comics'].apply(lambda x: x.get('available'))
df_events['comics_returned'] = df_events['comics'].apply(lambda x: x.get('returned'))
df_events['comics'] = df_events['comics'].apply(lambda x: json.dumps(x))
df_events['creators_available'] = df_events['creators'].apply(lambda x: x.get('available'))
df_events['creators'] = df_events['creators'].apply(lambda x: json.dumps(x))
df_events['characters_available'] = df_events['characters'].apply(lambda x: x.get('available'))
df_events['characters'] = df_events['characters'].apply(lambda x: json.dumps(x))
df_creators['comics_available'] = df_creators['comics'].apply(lambda x: x.get('available'))
df_creators['events_available'] = df_creators['events'].apply(lambda x: x.get('available'))
df_creators['stories_available'] = df_creators['stories'].apply(lambda x: x.get('available'))
df_creators['series_available'] = df_creators['series'].apply(lambda x: x.get('available'))
df_creators['thumbnail_path'] = df_creators['thumbnail'].apply(lambda x: x.get('path'))
df_creators['comics'] = df_creators['comics'].apply(lambda x: json.dumps(x))
df_creators['events'] = df_creators['events'].apply(lambda x: json.dumps(x))
df_creators['series'] = df_creators['series'].apply(lambda x: json.dumps(x))
df_creators['stories'] = df_creators['stories'].apply(lambda x: json.dumps(x))
df_creators['thumbnail'] = df_creators['thumbnail'].apply(lambda x: json.dumps(x))

## Salvando no Banco de Dados

con = sqlite3.connect('Marvel.db')
df_characters.to_sql("characters", con, if_exists="replace", index=False)
df_events.to_sql("events", con, if_exists="replace", index=False)
df_creators.to_sql("creators", con, if_exists="replace", index=False)
con.close()

## Salvando Com funções em Banco de Dados

## Adicionando mais Endpoints ao Banco

df_series = requisition(endSeries, totalSe, step=100, limit=100, params_base=params)
create_csv(df_series, nome_arquivo='Series.csv')
series_add_db(df_series)

df_comics = requisition(endComics, total, step=100, limit=100, params_base=params)
create_csv(df_comics, nome_arquivo='Comics.csv')
series_add_db(df_comics)

df_stories = requisition(endStories, total, step=100, limit=100, params_base=params)
create_csv(df_stories, nome_arquivo='Stories.csv')
series_add_db(df_stories)

# Selecionando do Banco de Dados

dataSeries = query_db('SELECT * FROM series')
dataComics = query_db('SELECT * FROM comics')
dataStories = query_db('SELECT * FROM stories')
dataCharacters = query_db('SELECT * FROM characters')
dataEvents = query_db('SELECT * FROM events')
dataCreators = query_db('SELECT * FROM creators')

# Characters

## INSIGHT 1 Characters - Criando função para selecionar entidades que tenham nome aliterativo


# Aplica a função à coluna 'name' e cria uma nova coluna booleana
dataframe = dataCharacters.copy()
dataframe['nome_sobrenome'] = dataCharacters['name'].apply(verify_first_letters)

# Para ver os personagens que atendem à condição
df_same_letter = dataframe[dataframe['nome_sobrenome']]
df_same_letter[['name', 'nome_sobrenome']]

## INSIGHT 2 Characters - Número de entidades por letra

count_letters = count_characters_by_initial_letter(dataCharacters)
count_letters

## INSIGHT 2 Characters - Gráfico

count_letters.plot.bar(x='letra_inicial', y='total_por_letra', legend=False)

## INSIGHT 3 Characters - Demonstração dos 10 personagens que tem mais quadrinhos

most = get_top_characters_by_comics(dataCharacters)
most.plot.bar(x='name', y='comics_available')

## INSIGHT 4 Characters - Personagens que tem descrição

description_characters = get_characters_with_description(dataCharacters)
description_characters

## INSIGHT 4 Characters - Gráfico de comparação da quantidade de personagens com descrição

count_description = count_characters_by_description_presence(dataCharacters)
plot_donut_charts(count_description)

## INSIGHT 5 Characters - Gráfico de personagens que tem imagens

characters_images = count_by_image(dataCharacters)
plot_donut_charts(characters_images)

plot_side_by_side_donuts(
    count_description.iloc[0],
    characters_images.iloc[0],
    titles=["Distribuição de Descrição", "Distribuição de Imagem"],
    colors=['#66c2a5', '#fc8d62'],
    donut_width=0.2
)

# Events

## INSIGHT 1 Events - Os 10 eventos com mais histórias em quadrinhos


# plot(most_events_comics, "Teste", x_label=most_events_comics['title'], y_label='comics_available', )
most_events_comics = get_top_events_by_comics(dataEvents)
most_events_comics.plot.bar(x='title', y='comics_available')

## INSIGHT 2 Events - Os eventos com maior duração

most_duration_events = get_past_events_with_duration(dataEvents)
most_duration_events

## INSIGHT 2 Events - Gráfico de demonstração de duração dos eventos

events_modified = format_and_sort_events(dataEvents)
df_timeline = events_modified.copy()

# Converter datas de string para datetime
df_timeline['start'] = pd.to_datetime(df_timeline['start'], format='%d/%m/%Y', errors='coerce')
df_timeline['end'] = pd.to_datetime(df_timeline['end'], format='%d/%m/%Y', errors='coerce')

# Remover eventos com datas inválidas
df_timeline = df_timeline.dropna(subset=['start', 'end'])

# Ordenar por data de início
df_timeline = df_timeline.sort_values(by='start')
plt.figure(figsize=(12, len(df_timeline) * 0.2))  # ajusta altura dinamicamente
plt.margins(y=0)

# Índice para os nomes dos eventos
y_positions = range(len(df_timeline))

# Plotar as barras horizontais
plt.barh(
    y=y_positions,
    width=(df_timeline['end'] - df_timeline['start']).dt.days,
    left=df_timeline['start'],
    color='skyblue'
)

# Nome dos eventos no eixo Y
plt.yticks(ticks=y_positions, labels=df_timeline['title'])

# Formatando o eixo X para mostrar ano
plt.gca().xaxis_date()
plt.xlabel('Ano')
plt.title('Linha do Tempo dos Eventos Marvel')
plt.grid(True, axis='x')
plt.tight_layout()
plt.show()

## INSIGHT 3 Events - Eventos modificados mais recentemente

events_modified

## INSIGHT 4 Events - Distribuição de Personagens por Duração do Evento dos 10 Eventos mais longos

events_most_characters = top_10_events_by_characters(dataEvents)
plt.figure(figsize=(10, 6))  # ajusta altura dinamicamente
scatter = plt.scatter(
    x=events_most_characters['characters_available'],
    y=events_most_characters['title'],
    s=events_most_characters['comics_available'] * 2,  # tamanho da bolha (ajuste o fator)
    c=events_most_characters['comics_available'],  # cor baseada em quadrinhos
    cmap='viridis',
    alpha=0.7,
    edgecolors='black'
)

plt.xlabel('Personagens Disponíveis')
plt.ylabel('Titulo do Evento')
plt.title('Escala dos Eventos Marvel: Relação entre Personagens e Quadrinhos')
plt.colorbar(scatter, label='Quadrinhos Disponíveis')
plt.grid(True)
plt.tight_layout()
plt.show()

# Creators

## INSIGHT 1 Creators - Distribuição entre quantos comics o autor escreveu e em quantos eventos estava

comics_per_events = top_15_creators_by_comics(dataCreators)

plt.figure(figsize=(10, 8))

scatter = plt.scatter(
    x=comics_per_events['events_available'],
    y=comics_per_events['fullName'],
    s=comics_per_events['comics_available'],  # tamanho da bolha
    c=comics_per_events['comics_available'],      # cor baseada nos quadrinhos
    cmap='plasma',
    alpha=0.7,
    edgecolors='black'
)

plt.xlabel('Eventos Disponíveis')
plt.ylabel('Nome do Criador')
plt.title('Criadores: Participação em Eventos vs Quadrinhos (Tamanho/Cor)')
plt.colorbar(scatter, label='Quadrinhos Disponíveis')
plt.grid(True)
plt.tight_layout()
plt.show()

## INSIGHT 2 Creators - Comparação de Creators com imagens associadas e sem imagens associadas

creators_images = count_by_image(dataCreators)
plot_donut_charts(creators_images)

# Comics

## INSIGHT 1 Comics: Média de preço sobre o tempo


comics_average_price_over_time(dataComics, show_plot=True)

## INSIGHT 2 Comics: Média de páginas sobre o tempo

comics_average_pages_over_time(dataComics, show_plot=True)

## INSIGHT 3 Comics: Os formatos mais comuns

comics_count_format(dataComics, show_plot=True)

# Series

## INSIGHT 1 Series: Quantidade de issues lançadas por ano

series_by_year(dataSeries, show_plot=True)

## INSIGHT 2 Series: Média da duração das series

series_average_duration(dataSeries, show_plot=True)

## INSIGHT 3 Series: Distribuição classificatória de faixa etária

series_distribution_rating(dataSeries, show_plot=True)

## INSIGHT 4 Series: Distribuição dos tipos de séries

series_distribuition_type(dataSeries, show_plot=True)

## INSIGHT 5 Series: Quantidade de personagens por ano

series_quantity_characters_year(dataSeries, show_plot=True)

## Dados errados da API em relação a duração

duration = dataSeries['duration'].value_counts().sort_index()
dataSeries[(dataSeries['duration'] < 0) | (dataSeries['duration'] > 999)]

# Stories
## INSIGHT 1 Stories: Quantidade de cada tipo

types = stories_quantity_type(dataStories, show_plot=True)