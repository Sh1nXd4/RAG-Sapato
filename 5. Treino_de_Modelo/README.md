# Treinamento de Modelos de Classificação

## Objetivo

Este módulo é responsável pelo treinamento, avaliação e comparação de modelos de Machine Learning aplicados ao dataset processado na camada Gold.

Os dados são consumidos diretamente do MinIO/Data Lake utilizando o bucket Gold.

O objetivo principal é identificar quais restaurantes possuem maior probabilidade de recomendação com base em características estruturais e operacionais.

---

# Estrutura do Diretório

```text
Treino_de_Modelo/
│
├── train_classification.py
├── train_classification.ipynb
└── README.md
```

---

# Fonte dos Dados

Os dados são carregados diretamente do MinIO:

```text
s3://gold/gold_data.parquet
```

Bucket utilizado:
- gold

Formato:
- Parquet

---

# Tecnologias Utilizadas

- Python
- Pandas
- NumPy
- Scikit-Learn
- Matplotlib
- Seaborn
- MLflow
- MinIO
- S3FS

---

# Integração com MinIO

O carregamento do dataset ocorre diretamente do Data Lake utilizando credenciais S3 compatíveis com MinIO.

Configuração utilizada:

```python
credenciais_minio = {
    "key": "minio",
    "secret": "minio123",
    "client_kwargs": {
        "endpoint_url": "http://localhost:9000"
    }
}
```

Leitura do dataset:

```python
df = pd.read_parquet(
    's3://gold/gold_data.parquet',
    storage_options=credenciais_minio
)
```

---

# Objetivo do Modelo

O sistema busca classificar restaurantes como:

```text
Recomendado
ou
Não Recomendado
```

A classificação é baseada em:
- avaliação média
- quantidade de reviews
- faixa de preço
- delivery
- área externa
- categorias gastronômicas

---

# Construção da Variável Alvo

A coluna alvo criada foi:

```python
is_recommended
```

Regra utilizada:

```python
df['is_recommended'] = (df['stars'] >= 3.5).astype(int)
```

Critério:
- restaurantes com nota maior ou igual a 3.5 → recomendados
- restaurantes abaixo de 3.5 → não recomendados

---

# Features Utilizadas

As variáveis principais utilizadas foram:

```python
features_base = [
    'review_count',
    'price_range',
    'has_delivery',
    'has_outdoor'
]
```

---

# Engenharia de Features

## Conversão de Booleanos

As colunas booleanas foram convertidas para inteiro:

```python
df['has_delivery'] = df['has_delivery'].astype(int)
df['has_outdoor'] = df['has_outdoor'].astype(int)
```

Objetivo:
- compatibilidade com algoritmos de Machine Learning

---

# Processamento de Categorias

A coluna:

```text
categories_list
```

contém múltiplas categorias por restaurante.

Exemplo:

```text
['Pizza', 'Italian', 'Restaurants']
```

---

## Seleção das Categorias Mais Frequentes

Foi aplicado um filtro para selecionar apenas as 30 categorias mais relevantes:

```python
TOP_N = 30
```

Objetivo:
- reduzir dimensionalidade
- evitar explosão de features
- melhorar desempenho do modelo

---

# Codificação MultiLabel

As categorias foram transformadas em variáveis binárias utilizando:

```python
MultiLabelBinarizer()
```

Exemplo:

| Pizza | Italian | Mexican |
|---|---|---|
| 1 | 1 | 0 |

---

# Construção do Dataset Final

O dataset final foi composto por:

- features numéricas
- features booleanas
- categorias codificadas

Criação:

```python
X = pd.concat([df[features_base], df_categories], axis=1)
```

Target:

```python
y = df['is_recommended']
```

---

# Divisão Treino/Teste

Foi utilizada divisão padrão:

```python
train_test_split()
```

Configuração:

```python
test_size=0.2
random_state=42
```

Resultado:
- 80% treino
- 20% teste

---

# Modelos Treinados

Foram avaliados quatro algoritmos de classificação.

---

## 1. Naive Bayes

Modelo utilizado:

```python
GaussianNB()
```

Características:
- simples
- rápido
- baseado em probabilidade

---

## 2. Decision Tree

Modelo utilizado:

```python
DecisionTreeClassifier()
```

Configuração:

```python
max_depth=6
class_weight='balanced'
```

Características:
- interpretável
- baseado em regras
- fácil visualização

---

## 3. Rede Neural

Modelo utilizado:

```python
MLPClassifier()
```

Configuração:

```python
max_iter=400
```

Características:
- aprendizado não linear
- maior capacidade de generalização

---

## 4. Logistic Regression

Modelo utilizado:

```python
LogisticRegression()
```

Configuração:

```python
max_iter=1000
class_weight='balanced'
```

---

# Ajuste de Threshold

A Regressão Logística utilizou ajuste manual de threshold:

```python
pred = (prob > 0.35).astype(int)
```

Objetivo:
- aumentar recall
- reduzir falsos negativos

---

# Métricas Avaliadas

Foram utilizadas:

| Métrica | Objetivo |
|---|---|
| Accuracy | Taxa geral de acertos |
| Precision | Qualidade das previsões positivas |
| Recall | Capacidade de encontrar positivos |
| F1-Score | Equilíbrio entre precisão e recall |

---

# Função de Avaliação

A função principal de avaliação foi:

```python
avaliar()
```

Responsabilidades:
- cálculo das métricas
- geração da matriz de confusão
- exibição gráfica dos resultados

---

# Matrizes de Confusão

Para cada modelo foi gerada uma matriz de confusão utilizando:

```python
confusion_matrix()
```

Visualização:

```python
sns.heatmap()
```

Objetivo:
- identificar erros do modelo
- analisar falsos positivos
- analisar falsos negativos

---

# Comparação Entre Modelos

Os modelos foram comparados utilizando principalmente:

```text
F1-Score
```

Critério escolhido por equilibrar:
- precisão
- recall

---

# Seleção do Melhor Modelo

O melhor modelo foi definido automaticamente:

```python
melhor = max(resultados, key=resultados.get)
```

Critério:
- maior F1-score

---

# Integração com MLflow

O experimento registrado foi:

```python
mlflow.set_experiment("Foodhunter_Classification")
```

Objetivo:
- rastreamento de experimentos
- comparação entre execuções
- organização dos treinamentos

---

# Visualizações Geradas

Durante o treinamento são gerados:
- matrizes de confusão
- gráficos comparativos
- métricas de desempenho

Bibliotecas utilizadas:
- Matplotlib
- Seaborn

---

# Fluxo Completo do Pipeline

```text
Bronze
   ↓
Silver
   ↓
Gold
   ↓
Treinamento de Modelos
   ↓
Avaliação
   ↓
Comparação
```

---

# Responsabilidades do Módulo

| Processo | Responsável |
|---|---|
| Consumo do Gold | Treinamento |
| Engenharia de Features | Treinamento |
| Codificação de Categorias | Treinamento |
| Divisão treino/teste | Treinamento |
| Treinamento dos modelos | Treinamento |
| Avaliação de métricas | Treinamento |
| Matrizes de confusão | Treinamento |
| Seleção do melhor modelo | Treinamento |

---

# Resultado Final

Ao final do processo são obtidos:

- modelos treinados
- métricas comparativas
- matrizes de confusão
- avaliação de desempenho
- identificação do melhor algoritmo para recomendação de restaurantes

O módulo representa a etapa final analítica do pipeline de Machine Learning do projeto.

---

# Características do Pipeline

| Característica | Status |
|---|---|
| Integração com MinIO | Sim |
| Machine Learning | Sim |
| Classificação Binária | Sim |
| Engenharia de Features | Sim |
| Visualização de Métricas | Sim |
| Matrizes de Confusão | Sim |
| Comparação de Modelos | Sim |
| Integração com MLflow | Sim |

---

# Resultado Esperado

O pipeline deve ser capaz de:
- consumir dados analíticos da Gold
- processar features automaticamente
- treinar múltiplos algoritmos
- comparar desempenho
- identificar o melhor modelo
- apoiar sistemas de recomendação baseados em Machine Learning