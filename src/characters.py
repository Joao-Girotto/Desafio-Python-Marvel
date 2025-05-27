
import pandas as pd
# Funções Characters
## Função para pegar o Top 10 personagens com mais comics

def get_top_characters_by_comics(df, top_n=10):
    # Garante que a coluna 'comics_available' está presente
    if 'comics_available' not in df.columns:
        raise ValueError("O DataFrame deve conter a coluna 'comics_available'.")

    top_characters = (
        df[['id', 'name', 'comics_available']]
        .sort_values(by='comics_available', ascending=False)
        .head(top_n)
        .reset_index(drop=True)
    )

    return top_characters

## Função para contar o número de personagens por letra inicial

def count_characters_by_initial_letter(df):
    # Garante que a coluna 'name' está presente
    if 'name' not in df.columns:
        raise ValueError("O DataFrame deve conter a coluna 'name'.")

    # Remove valores nulos e pega a primeira letra (em maiúsculas)
    df_filtered = df[df['name'].notnull()].copy()
    df_filtered['letra_inicial'] = df_filtered['name'].str[0].str.upper()

    # Conta ocorrências por letra
    count_by_letter = (
        df_filtered['letra_inicial']
        .value_counts()
        .sort_index()
        .rename("total_por_letra")
        .reset_index()
        .rename(columns={'index': 'letra_inicial'})
    )

    return count_by_letter

## Função para pegar os personagens com descrição

def get_characters_with_description(df):
    # Garante que as colunas necessárias estão presentes
    required_cols = {'id', 'name', 'description', 'comics_available'}
    if not required_cols.issubset(df.columns):
        raise ValueError(f"O DataFrame deve conter as colunas: {required_cols}")

    filtered_df = df[
        df['description'].notnull() & (df['description'].str.strip() != '')
    ][['id', 'name', 'description', 'comics_available']].reset_index(drop=True)

    return filtered_df

## Função para contar quantos personagens tem descrição

def count_characters_by_description_presence(df):
    # Garante que a coluna 'description' está presente
    if 'description' not in df.columns:
        raise ValueError("O DataFrame deve conter a coluna 'description'.")

    has_description = df['description'].notnull() & (df['description'].str.strip() != '')
    com_descricao = has_description.sum()
    sem_descricao = (~has_description).sum()

    result = pd.DataFrame({
        'com_descricao': [com_descricao],
        'sem_descricao': [sem_descricao]
    })

    return result