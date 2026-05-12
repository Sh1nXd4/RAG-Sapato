# Documentação do Pré-processamento de Dados
## Projeto FoodHunter – Arquitetura Bronze, Silver e Gold

---

## 1. Visão Geral
O projeto **FoodHunter** utiliza uma arquitetura de Data Lake organizada em três camadas para garantir a confiabilidade dos dados para análises, Machine Learning e sistemas **RAG (Retrieval-Augmented Generation)**.

### Fluxo do Pipeline
O fluxo segue a estrutura:
`Dataset CSV → Bronze → Silver → Gold → Machine Learning`

Os dados são armazenados no **MinIO**, simulando um ambiente de armazenamento distribuído (S3).

---

## 2. Camada Bronze
**Objetivo:** Armazenamento bruto (Raw) e preservação da origem dos dados (*Single Source of Truth*).

*   **Dataset:** `restaurants_with_embeddings.csv`
*   **Conteúdo:** Informações de restaurantes, avaliações, categorias, localização e embeddings vetoriais.

### Processamentos Realizados
1.  **Leitura do CSV:** Utilização de `pd.read_csv()`.
2.  **Exploração Inicial:** Inspeção de tipos de dados e valores nulos (`head()`, `info()`, `isnull()`).
3.  **Análise de Colunas Complexas:** 
    *   `attributes`: Mantida como string (JSON-like).
    *   `embedding`: Mantida como texto (lista numérica vetoriais).

---

## 3. Camada Silver
**Objetivo:** Limpeza, padronização e engenharia de features.

### Processamentos Realizados
*   **Filtragem:** Mantidos apenas restaurantes ativos (`is_open == 1`).
*   **Conversão de Dados:**
    *   `attributes`: Convertido para dicionário via `ast.literal_eval()`.
    *   `embedding`: Convertido de string para listas numéricas reais.
    *   `categories`: Transformado de string para lista (ex: `["Pizza", "Italian"]`).
*   **Engenharia de Features:**
    *   `has_delivery`: Extraído de `RestaurantsDelivery`.
    *   `has_outdoor`: Extraído de `OutdoorSeating`.
    *   `price_range`: Extraído de `RestaurantsPriceRange2`.

| Valor | Interpretação |
| :--- | :--- |
| 1 | Barato |
| 2 | Médio |
| 3 | Alto |
| 4 | Premium |

---

## 4. Análises Exploratórias (EDA)
Na camada Silver, foram geradas visualizações para insights:
*   **Mapa de Correlação:** Relação entre estrelas, contagem de reviews e preço.
*   **Distribuição de Avaliações:** Histograma da variável `stars`.
*   **Impacto do Delivery:** Comparação de médias de avaliação.
*   **Popularidade vs Nota:** Dispersão entre `review_count` e `stars`.

---

## 5. Camada Gold
**Objetivo:** Dados refinados para consumo analítico e IA.

### 5.1 Criação do `gold_score`
O score de ranqueamento foi calculado seguindo os passos:
1.  **Log Transformation:** `np.log1p(review_count)` para suavizar extremos.
2.  **Normalização:** Uso do `MinMaxScaler` (intervalo 0 a 1).
3.  **Fórmula:**
$$gold\_score = (stars\_norm \times 0.7) + (reviews\_norm \times 0.3)$$

### 5.2 Construção do Contexto RAG
Criação da coluna `rag_context`, consolidando metadados (nome, cidade, categoria, score) para facilitar a recuperação semântica por modelos de linguagem.

---

## 6. Integração com MinIO
Os dados são persistidos em buckets específicos:
*   `bronze/`: Dados originais.
*   `silver/`: Dados limpos e tipados.
*   `gold/`: Tabelas prontas para consumo.

---

## 7. Machine Learning
O projeto aborda um problema de **Classificação Binária**.

### Variável Alvo (`is_recommended`)
O critério de recomendação foi definido como:
$$is\_recommended = \begin{cases} 1, & stars \geq 3.5 \\ 0, & stars < 3.5 \end{cases}$$

### Modelos Treinados
1.  **Gaussian Naive Bayes**
2.  **Decision Tree**
3.  **MLPClassifier (Rede Neural)**
4.  **Logistic Regression**

**Métricas de Avaliação:** Acurácia, Precisão, Recall e F1-Score, validados via Matriz de Confusão.

---

## 8. Conclusão
O pipeline FoodHunter demonstra uma arquitetura moderna de engenharia de dados, integrando desde o armazenamento bruto em Data Lake até a entrega de dados otimizados para sistemas de Recomendação e RAG.