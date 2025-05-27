import sqlite3
import matplotlib.pyplot as plt
import pandas as pd
import requests
# Funções Auxiliares

def plot_donut_charts(df, colors=None, figsize=(10, 6), center_text_prefix='Total'):
    # Transpor o DataFrame para que cada coluna vire um gráfico de donut
    df_transposed = df.transpose()

    # Criar gráficos de "donut"
    axes = df_transposed.plot.pie(
        subplots=True,
        autopct='%1.1f%%',
        figsize=figsize,
        legend=False,
        startangle=90,
        colors=colors
    )

    # Adicionar círculo no centro e texto com o total de cada gráfico
    for ax, col in zip(axes, df_transposed.columns):
        total = df_transposed[col].sum()
        centre_circle = plt.Circle((0, 0), 0.70, fc='white')
        ax.add_artist(centre_circle)

        # Texto central com total
        ax.text(0, 0, f'{center_text_prefix}:\n{total}', fontsize=10,
                fontweight='bold', ha='center', va='center')

        ax.set_ylabel('')  # Remove rótulo do eixo y
        ax.set_title(col, fontsize=12, fontweight='bold')

    plt.tight_layout()
    plt.show()

def verify_first_letters(nome_completo):
  partes_nome = nome_completo.split()
  if len(partes_nome) >= 2:
    nome = partes_nome[0]
    sobrenome = partes_nome[-1] # Pega a última parte como sobrenome
    if nome and sobrenome: # Verifica se nome e sobrenome não são vazios
      return nome[0].lower() == sobrenome[0].lower()
  return False # Retorna False se não for possível verificar (nome curto ou vazio)

def plot_side_by_side_donuts(series1, series2,
                            titles=None,
                            colors=None,
                            figsize=(12, 6),
                            donut_width=0.3,
                            center_text_prefix='Total'):
    fig, axes = plt.subplots(1, 2, figsize=figsize)

    # Donut 1
    series1.plot.pie(
        ax=axes[0],
        autopct='%1.1f%%',
        startangle=90,
        colors=colors,
        legend=False,
        wedgeprops={'width': donut_width, 'edgecolor': 'white'}
    )
    # Adiciona círculo no centro do primeiro donut
    centre_circle1 = plt.Circle((0, 0), 1 - donut_width, fc='white')
    axes[0].add_artist(centre_circle1)
    total1 = series1.sum()
    axes[0].text(0, 0, f'{center_text_prefix}:\n{total1}', fontsize=10,
                 fontweight='bold', ha='center', va='center')

    # Donut 2
    series2.plot.pie(
        ax=axes[1],
        autopct='%1.1f%%',
        startangle=90,
        colors=colors,
        legend=False,
        wedgeprops={'width': donut_width, 'edgecolor': 'white'}
    )
    # Adiciona círculo no centro do segundo donut
    centre_circle2 = plt.Circle((0, 0), 1 - donut_width, fc='white')
    axes[1].add_artist(centre_circle2)
    total2 = series2.sum()
    axes[1].text(0, 0, f'{center_text_prefix}:\n{total2}', fontsize=10,
                 fontweight='bold', ha='center', va='center')

    # Títulos
    if titles:
        axes[0].set_title(titles[0], fontsize=12, fontweight='bold')
        axes[1].set_title(titles[1], fontsize=12, fontweight='bold')

    # Remover rótulos dos eixos y
    axes[0].set_ylabel('')
    axes[1].set_ylabel('')

    plt.tight_layout()
    plt.show()

# Plota um gráfico, wrapper do plot do pandas, objetivo é a padronização dos gráficos
def plot(dataframe,
         title,
         x_label,
         y_label,
         grid='y',
         kind='bar',
         color='purple',
         rotation=90,
         show=True,
         **kwargs):
  ax = dataframe.plot(kind=kind, color=color, title=title, **kwargs)
  ax.set_xlabel(x_label)
  ax.set_ylabel(y_label)
  plt.xticks(rotation=rotation)
  plt.tight_layout()
  plt.grid(axis=grid)

  if show:
    plt.show()

  return ax


def count_by_image(df):
    # Conta os criadores com imagem associada
    com_imagem = (~df['thumbnail_path'].str.contains('image_not_available', na=False)).sum()

    # Conta os criadores sem imagem associada
    sem_imagem = (df['thumbnail_path'].str.contains('image_not_available', na=False)).sum()

    # Retorna em formato de DataFrame
    result = pd.DataFrame([{
        'Com_Imagem_Associada': com_imagem,
        'Sem_Imagem_Associada': sem_imagem
    }])

    return result

# Consulta o banco de dados
def query_db(query, params=None, db='Marvel.db'):
  try:
    with sqlite3.connect(db) as con:
      return pd.read_sql_query(query, con, params)

  except Exception as e:
    print(f'Erro com a database: {e}')
    return pd.DataFrame()

# Adiciona os dados à tabela de series
def series_add_db(df):  # Agora recebe um DataFrame

    def calculateDuration(row):
        end = 999 if row['endYear'] == 299 else row['endYear']
        return end - row['startYear']

    def function_dict(x):
        items = x['items'] if isinstance(x, dict) and 'items' in x else []
        creators = [item['name'] for item in items]
        return ', '.join(creators)

    def amount(x):
        return x.get('available', 0)

    with sqlite3.connect('Marvel.db') as con:
        df['duration'] = df.apply(calculateDuration, axis=1)
        df['creator_name'] = df['creators'].apply(function_dict)
        df['character_qty'] = df['characters'].apply(amount)
        df['creator_qty'] = df['creators'].apply(amount)
        df['story_qty'] = df['stories'].apply(amount)
        df['event_qty'] = df['events'].apply(amount)
        df['comic_qty'] = df['comics'].apply(amount)

        df = df[['id', 'title', 'description', 'startYear', 'endYear',
                 'rating', 'type', 'duration', 'creator_name', 'creator_qty',
                 'character_qty', 'story_qty', 'event_qty', 'comic_qty']]

        df.to_sql("series", con, if_exists="append", index=False)

# Adiciona os dados à tabela de comics
def comics_add_db(df):  # Agora recebe um DataFrame

    def funcao_series(x):
        return x.get('name', '') if isinstance(x, dict) else ''

    def funcao_price(x):
        if isinstance(x, list) and len(x) > 0 and isinstance(x[0], dict):
            return x[0].get('price', '')
        return ''

    with sqlite3.connect('Marvel.db') as con:
        df['price'] = df['prices'].apply(funcao_price)
        df['series_name'] = df['series'].apply(funcao_series)

        df = df[['id', 'digitalId', 'title', 'issueNumber', 'description',
                 'format', 'pageCount', 'series_name', 'price']]

        df.to_sql("comics", con, if_exists="append", index=False)


# Adiciona os dados à tabela de stories
def stories_add_db(df):  # Agora recebe um DataFrame
    with sqlite3.connect('Marvel.db') as con:
        df = df[['id', 'title', 'description', 'type']]
        df.to_sql("stories", con, if_exists="append", index=False)

## Conversão para CSV

def create_csv(df, nome_arquivo):
    try:
        df.to_csv(nome_arquivo, index=False, encoding='utf-8')
    except Exception as e:
        print(f'Error when creating the file {nome_arquivo}: {e}')

#Função para realizar requisições

def requisition(endpoint, total, step, limit, params_base=None):
    data_array = []
    offset = 0

    if params_base is None:
        params_base = {}

    while offset <= total:
        params = params_base.copy()
        params['offset'] = offset
        params['limit'] = limit

        response = requests.get(endpoint, params=params)

        if response.status_code != 200:
            print(f"Erro no offset {offset}: status code {response.status_code}")
            offset += step
            continue

        try:
            data = response.json()
        except ValueError:
            print(f"Erro ao converter JSON no offset {offset}")
            offset += step
            continue

        if not data or 'data' not in data or 'results' not in data['data']:
            print(f"Resposta inesperada ou vazia no offset {offset}")
            offset += step
            continue

        data_array.extend(data['data']['results'])
        print(f"Offset: {offset} | Status: {response.status_code}")
        offset += step

    df = pd.DataFrame(data_array)
    return df