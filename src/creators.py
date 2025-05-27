# Funções Creators
## Função para pegar os 15 criadores que mais escrevam quadrinhos

def top_15_creators_by_comics(df):
    # Ordenar pelo número de quadrinhos disponíveis em ordem decrescente
    df_sorted = df.sort_values(by='comics_available', ascending=False)

    # Selecionar as colunas desejadas e pegar os 15 primeiros
    top_15 = df_sorted[['firstName', 'middleName', 'lastName', 'fullName', 'comics_available', 'events_available']].head(15)

    return top_15.reset_index(drop=True)
