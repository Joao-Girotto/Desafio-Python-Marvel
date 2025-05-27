import pandas as pd

#Funções Events

## Função que retorna os maiores eventos


def get_top_events_by_comics(df, top_n=10):
    # Garante que as colunas necessárias estão presentes
    required_cols = {'title', 'comics_available'}
    if not required_cols.issubset(df.columns):
        raise ValueError(f"O DataFrame deve conter as colunas: {required_cols}")

    top_events = (
        df[['title', 'comics_available']]
        .sort_values(by='comics_available', ascending=False)
        .head(top_n)
        .reset_index(drop=True)
    )

    return top_events

## Função para analisar o tempo de druação de eventos

def get_past_events_with_duration(df, reference_date='2025-05-16'):
    # Garante que as colunas necessárias estão presentes
    required_cols = {'title', 'start', 'end', 'comics_available'}
    if not required_cols.issubset(df.columns):
        raise ValueError(f"O DataFrame deve conter as colunas: {required_cols}")

    # Converte colunas de data para datetime
    df['start'] = pd.to_datetime(df['start'], errors='coerce')
    df['end'] = pd.to_datetime(df['end'], errors='coerce')

    # Filtra eventos que começaram e terminaram até a data de referência
    ref_date = pd.to_datetime(reference_date)
    filtered_df = df[(df['start'] <= ref_date) & (df['end'] <= ref_date)].copy()

    # Calcula duração em anos (usando 365.25 dias/ano)
    filtered_df['duration_in_years'] = ((filtered_df['end'] - filtered_df['start']).dt.days / 365.25).astype(int)

    # Formata datas para o padrão dd/mm/yyyy
    filtered_df['start_formatted'] = filtered_df['start'].dt.strftime('%d/%m/%Y')
    filtered_df['end_formatted'] = filtered_df['end'].dt.strftime('%d/%m/%Y')

    # Ordena pela duração (em dias) decrescente
    filtered_df['duration_days'] = (filtered_df['end'] - filtered_df['start']).dt.days
    result = filtered_df.sort_values(by='duration_days', ascending=False)

    # Seleciona e reorganiza colunas de interesse
    result = result[['title', 'start_formatted', 'end_formatted', 'duration_in_years', 'comics_available']].reset_index(drop=True)

    return result

## Função para formatar o tempo de inicio e fim de um evento

def format_and_sort_events(df):
    # Converter as colunas para datetime (modified pode ter hora, cortamos isso)
    df['modified'] = pd.to_datetime(df['modified'].str[:10], errors='coerce')
    df['start'] = pd.to_datetime(df['start'], errors='coerce')
    df['end'] = pd.to_datetime(df['end'], errors='coerce')

    # Formatar as datas como 'dd/mm/yyyy'
    df['modified'] = df['modified'].dt.strftime('%d/%m/%Y')
    df['start'] = df['start'].dt.strftime('%d/%m/%Y')
    df['end'] = df['end'].dt.strftime('%d/%m/%Y')

    # Criar uma coluna auxiliar com o ano de 'modified' para ordenação
    df['_year'] = df['modified'].str[-4:].astype(int)

    # Ordenar pelo ano de forma decrescente
    df_sorted = df.sort_values(by='_year', ascending=False)

    # Selecionar colunas desejadas
    result = df_sorted[['title', 'modified', 'start', 'end']]

    return result.reset_index(drop=True)

## Função para retornar os 10 Eventos com mais personagens

def top_10_events_by_characters(df):
    # Ordenar pelo número de personagens disponíveis (decrescente)
    df_sorted = df.sort_values(by='characters_available', ascending=False)

    # Selecionar as colunas desejadas e pegar apenas os 10 primeiros
    top_10 = df_sorted[['title', 'characters_available', 'comics_available']].head(10)

    return top_10.reset_index(drop=True)
