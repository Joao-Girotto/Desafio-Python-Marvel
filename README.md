
# Desafio Python - API da Marvel

Este projeto consiste em uma análise de dados utilizando a API pública da **Marvel Comics**. O objetivo é coletar informações sobre personagens, quadrinhos, criadores e outros elementos do universo Marvel, processar os dados e gerar visualizações informativas.

## Bibliotecas Utilizadas

- `requests`: para realizar requisições HTTP à API da Marvel.
- `hashlib`: para gerar o hash MD5 exigido pela autenticação da API.
- `os`, `time`, `json`: para manipulação geral e autenticação.
- `pandas`: para organização e manipulação tabular dos dados.
- `sqlite3`: para armazenamento local dos dados coletados.
- `matplotlib` e `plotly.express`: para visualizações gráficas.
- `regex`: para tratamento e limpeza de strings.
- `dotenv`: instalação sugerida (caso seja utilizado arquivo .env).
- `google.colab.userdata`: utilizado para acessar as chaves privadas/publicas de autenticação no ambiente do Google Colab.

## Autenticação

A API da Marvel exige três parâmetros de autenticação:
- `ts` (timestamp)
- `apikey` (chave pública)
- `hash` (MD5 gerado a partir de `ts + chave privada + chave pública`)

As chaves são carregadas via `google.colab.userdata.get()`.

## Endpoints Utilizados

O notebook acessa múltiplos endpoints da API da Marvel:
- `/characters`
- `/comics`
- `/series`
- `/creators`
- `/events`
- `/stories`

## Lógica do Código

1. **Requisições**:
   - É feita uma requisição inicial a cada endpoint para descobrir o número total de registros disponíveis.
   - Uma função `requisition` percorre todos os dados de forma paginada utilizando `offset` e `limit`.

2. **Armazenamento**:
   - Os dados são organizados em `DataFrames` com `pandas`.
   - Existe suporte para salvar os dados em um banco de dados SQLite.

3. **Visualizações**:
   - Geração de gráficos interativos com `plotly.express` e gráficos estáticos com `matplotlib`.
   - Análise da quantidade de aparições de personagens, frequência de criadores, e outros insights sobre o universo Marvel.

## Resultados Principais

- Coleta e consolidação de dados sobre personagens, quadrinhos, eventos e mais.
- Análises visuais sobre:
  - Os personagens com mais aparições.
  - A linha do tempo da publicação dos quadrinhos.
  - O volume de produção por criador.
- Utilização eficiente de paginação para grandes volumes de dados.

## Como Executar

1. Faça upload do notebook em uma instância do **Google Colab**.
2. Salve suas **chaves pública e privada da API da Marvel** em `google.colab.userdata`.
3. Execute as células sequencialmente.

## Observações

- A API da Marvel tem limites de requisição, então é necessário cautela ao coletar grandes volumes.
- Os dados podem ser salvos localmente em um banco SQLite para evitar novas chamadas.

## Contribuidores

João Vitor Girotto  
Henry Meneguini Farias
