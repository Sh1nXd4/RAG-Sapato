# Camada Gold

## Objetivo

A camada Gold é responsável pela consolidação analítica dos dados e preparação final para consumo por aplicações de Machine Learning, sistemas de recomendação e arquiteturas RAG.

Nesta etapa, os dados recebem enriquecimento analítico, cálculo de métricas e construção de contexto textual estruturado.

---

# Estrutura da Camada

```text
gold/
│
├── gold.py
├── gold_data.parquet
├── gold.ipynb
└── README.md
```

---

# Entrada de Dados

Arquivo consumido da camada Silver:

```text
silver/silver_data.parquet
```

---

# Saída de Dados

Arquivo gerado:

```text
gold/gold_data.parquet
```

Formato utilizado:

- Parquet
- Estrutura colunar
- Alta performance analítica

---

# Processamentos Realizados

## 1. Leitura dos Dados

A camada Gold consome os dados previamente tratados na Silver:

```python
df = pd.read_parquet(caminho_silver)
```

---

# Construção do Score Analítico

Foi criado um indicador analítico denominado:

```python
gold_score
```

Objetivo:
- Criar uma métrica única de relevância dos restaurantes
- Combinar qualidade e popularidade

---

## 2. Transformação Logarítmica

A quantidade de reviews possui distribuição muito desigual.

Para reduzir distorções, foi aplicada transformação logarítmica:

```python
df['log_reviews'] = np.log1p(df['review_count'])
```

Objetivo:
- Reduzir impacto de valores extremos
- Melhorar estabilidade estatística

---

## 3. Normalização dos Dados

Foi utilizado:

```python
MinMaxScaler()
```

As colunas normalizadas foram:

- stars
- log_reviews

Resultado:
- valores convertidos para escala entre 0 e 1

---

## 4. Cálculo do Gold Score

Fórmula aplicada:

```python
gold_score = (stars_norm * 0.7) + (reviews_norm * 0.3)
```

Distribuição de pesos:

| Variável | Peso |
|---|---|
| Avaliação (stars) | 70% |
| Popularidade (reviews) | 30% |

Objetivo:
- Priorizar qualidade
- Considerar relevância/popularidade

---

# Construção do Contexto RAG

Foi criada a coluna:

```python
rag_context
```

Essa coluna consolida informações textuais relevantes dos restaurantes.

---

## Estrutura do Contexto

Exemplo:

```text
Nome: Pizza House.
Local: Las Vegas.
Estilo: Pizza, Italian.
Avaliação: 4.5 estrelas (320 reviews).
Delivery: Sim.
Score: 0.82.
```

---

# Objetivo do RAG Context

A coluna `rag_context` será utilizada em:

- Sistemas RAG
- Busca semântica
- Similaridade textual
- LLMs
- Recuperação contextual

---

# Seleção Final de Colunas

Foram mantidas apenas colunas relevantes para consumo analítico.

---

## Colunas Finais

| Coluna | Descrição |
|---|---|
| business_id | Identificador do restaurante |
| name | Nome do restaurante |
| city | Cidade |
| categories | Categorias textuais |
| categories_list | Categorias em lista |
| price_range | Faixa de preço |
| has_delivery | Possui delivery |
| has_outdoor | Possui área externa |
| stars | Avaliação média |
| review_count | Quantidade de reviews |
| gold_score | Score analítico |
| rag_context | Contexto textual para RAG |
| embedding_list | Vetor embedding |

---

# Tecnologias Utilizadas

- Python
- Pandas
- NumPy
- Scikit-learn
- MinMaxScaler
- PyArrow

---

# Formato de Saída

Formato escolhido:

```text
Parquet
```

Vantagens:
- Alta compressão
- Melhor leitura analítica
- Compatível com Data Lakes
- Melhor integração com pipelines de IA

---

# Objetivo da Camada Gold

A camada Gold fornece dados refinados para:

- Machine Learning
- Sistemas de recomendação
- Busca vetorial
- Retrieval-Augmented Generation (RAG)
- Dashboards
- Analytics avançado
- LLM Applications

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
| Consolidação analítica | Gold |
| Criação de score | Gold |
| Normalização | Gold |
| Preparação para RAG | Gold |
| Enriquecimento contextual | Gold |
| Dataset final para IA | Gold |

---

# Resultado Final

O resultado da camada Gold é um dataset analítico refinado e pronto para:

- treinamento de modelos
- classificação
- recomendação
- recuperação semântica
- aplicações com LLM
- pipelines de IA generativa
- sistemas inteligentes de busca