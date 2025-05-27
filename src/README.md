
# Projeto de Análise de Dados Marvel

##  Estrutura dos Arquivos

| Arquivo        | Função Principal                            |
|----------------|----------------------------------------------|
| auxiliary.py   | Funções auxiliares (DB, API, utils)         |
| characters.py  | Manipulação de dados dos personagens        |
| comics.py      | Dados e gráficos sobre quadrinhos           |
| creators.py    | (Vazio ou em desenvolvimento)               |
| desafio.py     | Arquivo principal de execução               |
| events.py      | Dados sobre eventos                         |
| series.py      | Dados sobre séries                          |
| stories.py     | Dados sobre histórias                       |

##  Bibliotecas Usadas

- **Manipulação de Dados:**  
  - pandas  
  - numpy

- **Visualização:**  
  - matplotlib  
  - plotly

- **Banco de Dados:**  
  - sqlite3

- **Requisições Web:**  
  - requests

- **Outras Utilidades:**  
  - regex  
  - os, json, hashlib, time

> Observação: `google.colab` aparece em alguns arquivos, indicando que pode ser executado tanto localmente quanto em notebooks no Colab.

##  Como Executar o Projeto

### Pré-requisitos

Instale as dependências:

```bash
pip install pandas numpy matplotlib plotly requests regex
```

### Execução

1. Garanta que todos os arquivos estão na mesma pasta `src/`.
2. No terminal, acesse a pasta:

```bash
cd src
```

3. Execute o arquivo principal:

```bash
python desafio.py
```

### Banco de Dados

- O projeto utiliza `sqlite3` para persistência local dos dados. O próprio código cria e atualiza o banco automaticamente conforme necessário.

## Observações Finais

Este projeto faz consumo da API da Marvel para análise e visualização de dados relacionados a personagens, quadrinhos, histórias, eventos e séries.

