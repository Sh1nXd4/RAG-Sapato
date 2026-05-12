# Camada Silver

## Objetivo

A camada Silver é responsável pelo tratamento, limpeza e padronização dos dados provenientes da camada Bronze.

Nesta etapa, os dados passam por transformações estruturais para preparação analítica, engenharia de features e utilização em modelos de Machine Learning e sistemas RAG.

---

# Estrutura da Camada

```text
silver/
│
├── silver.py
├── silver.ipynb
├── silver_data.parquet
├── correlation_matrix.png
├── stars_distribution.png
├── delivery_vs_rating.png
├── reviews_vs_stars.png
└── README.md
```

---

# Entrada de Dados

Arquivo consumido da camada Bronze:

```text
bronze/restaurants_with_embeddings.csv
```

---

# Saída de Dados

Arquivo gerado:

```text
silver/silver_data.parquet
```

Formato utilizado:

- Parquet
- Compressão colunar
- Melhor performance para leitura analítica

---

# Processamentos Realizados

## 1. Leitura do Dataset

O pipeline realiza a leitura do CSV bruto:

```python
df = pd.read_csv(caminho_bronze)
```

---

## 2. Filtragem de Restaurantes Abertos

Foram mantidos apenas estabelecimentos ativos:

```python
df = df[df['is_open'] == 1].copy()
```

Objetivo:
- Remover restaurantes fechados
- Melhorar consistência dos dados

---

# Conversão da Coluna Attributes

A coluna `attributes` originalmente encontra-se em formato String.

Exemplo original:

```text
"{'RestaurantsDelivery': 'True', 'OutdoorSeating': 'False'}"
```

Foi criada uma função para converter esse conteúdo em dicionário Python:

```python
ast.literal_eval()
```

Objetivo:
- Permitir acesso estruturado aos atributos
- Facilitar engenharia de features

---

# Engenharia de Features

Foram criadas variáveis derivadas importantes para análise e treinamento.

---

## 1. Feature: has_delivery

Indica se o restaurante possui delivery.

```python
df['has_delivery']
```

Valores:
- True
- False

---

## 2. Feature: has_outdoor

Indica se o restaurante possui área externa.

```python
df['has_outdoor']
```

Valores:
- True
- False

---

## 3. Feature: price_range

Representa faixa de preço do restaurante.

Extraída de:

```text
RestaurantsPriceRange2
```

Valores típicos:
- 1 → barato
- 2 → médio
- 3 → caro
- 4 → premium

---

## 4. Feature: categories_list

Transforma categorias textuais em lista Python.

Exemplo original:

```text
"Restaurants, Pizza, Italian"
```

Após transformação:

```python
['Restaurants', 'Pizza', 'Italian']
```

Objetivo:
- Preparação para encoding de categorias
- Machine Learning
- Sistemas RAG

---

## 5. Conversão dos Embeddings

A coluna `embedding` originalmente estava em formato String.

Exemplo:

```text
"[0.123, 0.532, 0.912]"
```

Após processamento:

```python
[0.123, 0.532, 0.912]
```

Nova coluna criada:

```python
embedding_list
```

Objetivo:
- Busca vetorial
- Similaridade semântica
- RAG

---

# Limpeza de Dados

Foram removidas colunas intermediárias e desnecessárias:

```text
attributes
attributes_dict
hours
is_open
```

Objetivos:
- Redução de redundância
- Organização do dataset
- Melhor performance

---

# Visualizações Geradas

A camada Silver também executa análise exploratória automática.

---

## 1. Mapa de Correlação

Arquivo:

```text
correlation_matrix.png
```

Analisa correlação entre:
- stars
- review_count
- price_range
- has_delivery
- has_outdoor

Objetivo:
- Identificar relações entre variáveis

---

## 2. Distribuição das Avaliações

Arquivo:

```text
stars_distribution.png
```

Mostra distribuição das notas dos restaurantes.

Objetivo:
- Entender comportamento das avaliações

---

## 3. Delivery vs Avaliação

Arquivo:

```text
delivery_vs_rating.png
```

Compara média de avaliações:
- restaurantes com delivery
- restaurantes sem delivery

---

## 4. Reviews vs Stars

Arquivo:

```text
reviews_vs_stars.png
```

Mostra relação entre:
- quantidade de reviews
- avaliação média

Objetivo:
- Identificar popularidade vs qualidade

---

# Tecnologias Utilizadas

- Python
- Pandas
- NumPy
- Matplotlib
- PyArrow
- AST

---

# Formato de Saída

Formato escolhido:

```text
Parquet
```

Motivos:
- Melhor performance
- Compressão eficiente
- Compatível com Data Lakes
- Melhor integração com analytics

---

# Objetivo da Camada Silver

A camada Silver fornece dados limpos, estruturados e enriquecidos para:

- Machine Learning
- Sistemas de Recomendação
- Retrieval-Augmented Generation (RAG)
- Analytics
- Busca Semântica
- Vetorização
- Engenharia de Features

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
| Limpeza de dados | Silver |
| Conversão de tipos | Silver |
| Engenharia de features | Silver |
| Estruturação analítica | Silver |
| Preparação para ML | Silver |
| Preparação para RAG | Silver |

---

# Resultado Final

O resultado da camada Silver é um dataset estruturado e pronto para:

- consumo analítico
- modelagem preditiva
- classificação
- recomendação
- busca vetorial
- pipelines de IA