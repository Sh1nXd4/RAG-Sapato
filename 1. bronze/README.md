# Camada Bronze

## Objetivo

A camada Bronze é responsável pelo armazenamento dos dados brutos do projeto.

Nesta etapa, os dados são preservados exatamente como foram recebidos originalmente, sem alterações estruturais ou transformações analíticas.

O principal objetivo é garantir:
- rastreabilidade
- integridade dos dados
- histórico bruto do dataset
- reprodutibilidade do pipeline

---

# Estrutura da Camada

```text
bronze/
│
├── restaurants_with_embeddings.csv
├── bronze.ipynb
└── README.md
```

---

# Dataset Utilizado

Arquivo bruto:

```text
restaurants_with_embeddings.csv
```

Formato:
- CSV

---

# Fonte dos Dados

O dataset contém informações de restaurantes, incluindo:

- nome
- localização
- categorias
- avaliações
- quantidade de reviews
- atributos do restaurante
- embeddings vetoriais

---

# Objetivo da Camada Bronze

A camada Bronze funciona como:

- armazenamento bruto
- backup dos dados originais
- ponto inicial do pipeline
- referência para auditoria e reprocessamento

Nenhuma limpeza ou transformação definitiva é aplicada nesta camada.

---

# Processamentos Realizados

A camada Bronze possui apenas:
- leitura
- inspeção
- análise exploratória inicial

Sem modificações estruturais permanentes.

---

# Leitura do Dataset

O dataset é carregado utilizando:

```python
pd.read_csv()
```

Exemplo:

```python
df_bronze = pd.read_csv(caminho_bronze)
```

---

# Análises Realizadas

## 1. Visualização Inicial

Foram exibidas as primeiras linhas do dataset:

```python
df_bronze.head()
```

Objetivo:
- validação visual
- entendimento inicial dos dados

---

## 2. Análise de Schema

Foi utilizada:

```python
df_bronze.info()
```

Objetivo:
- identificar tipos de dados
- verificar colunas
- analisar valores não nulos

---

## 3. Verificação de Valores Nulos

Foi executado:

```python
df_bronze.isnull().sum()
```

Objetivo:
- identificar colunas incompletas
- preparar futuras limpezas na Silver

---

# Coluna Attributes

A coluna:

```text
attributes
```

armazena informações estruturadas em formato String.

Exemplo:

```text
"{'RestaurantsDelivery': 'True', 'OutdoorSeating': 'False'}"
```

Observação:
- Ainda não é um dicionário Python
- A conversão ocorre na camada Silver

---

# Coluna Embedding

A coluna:

```text
embedding
```

contém embeddings vetoriais armazenados como String.

Exemplo:

```text
"[0.123, 0.532, 0.912]"
```

Observação:
- Ainda não é uma lista numérica
- A conversão ocorre na camada Silver

---

# Características da Camada Bronze

| Característica | Descrição |
|---|---|
| Dados brutos | Sim |
| Limpeza aplicada | Não |
| Conversões aplicadas | Não |
| Engenharia de features | Não |
| Dados históricos | Sim |
| Persistência original | Sim |

---

# Tecnologias Utilizadas

- Python
- Pandas
- NumPy

---

# Formato de Armazenamento

Formato escolhido:

```text
CSV
```

Objetivo:
- simplicidade
- compatibilidade
- preservação original

---

# Fluxo do Pipeline

```text
Bronze
   ↓
Silver
   ↓
Gold
   ↓
Machine Learning / RAG
```

---

# Responsabilidades da Camada

| Processo | Responsável |
|---|---|
| Armazenamento bruto | Bronze |
| Preservação original | Bronze |
| Auditoria de dados | Bronze |
| Inspeção inicial | Bronze |
| Fonte oficial do pipeline | Bronze |

---

# Resultado Final

O resultado da camada Bronze é um dataset bruto preservado, servindo como:

- fonte oficial do pipeline
- base para reprocessamento
- camada histórica
- ponto inicial das transformações analíticas
- entrada para limpeza e engenharia de features na camada Silver