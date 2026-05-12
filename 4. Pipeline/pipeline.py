import pandas as pd
import numpy as np
import ast
import os
from sklearn.preprocessing import MinMaxScaler

# =====================================================
# CONFIGURAÇÃO MINIO
# =====================================================

credenciais_minio = {
    "key": "minio",
    "secret": "minio123",
    "client_kwargs": {
        "endpoint_url": "http://localhost:9000"
    }
}

print("Iniciando Pipeline Data Lake...")

# =====================================================
# CAMADA BRONZE
# =====================================================

print("\n==============================")
print("CAMADA BRONZE")
print("==============================")

# Caminho do CSV bruto
caminho_csv = "bronze/restaurants_with_embeddings.csv"

print(f"Lendo dataset bruto: {caminho_csv}")

df_bronze = pd.read_csv(caminho_csv)

print(f"Registros Bronze: {len(df_bronze)}")

# Upload RAW para MinIO
df_bronze.to_csv(
    "s3://bronze/restaurants_with_embeddings.csv",
    index=False,
    storage_options=credenciais_minio
)

print("Bronze enviado para MinIO!")

# =====================================================
# CAMADA SILVER
# =====================================================

print("\n==============================")
print("CAMADA SILVER")
print("==============================")

df_silver = df_bronze.copy()

# -----------------------------------------
# Filtrar restaurantes abertos
# -----------------------------------------
df_silver = df_silver[df_silver['is_open'] == 1].copy()

# -----------------------------------------
# Parse attributes
# -----------------------------------------
def parse_dict_string(x):

    if pd.isna(x):
        return {}

    try:
        clean_str = str(x).replace('""', '"').replace("u'", "'")
        return ast.literal_eval(clean_str)

    except:
        return {}

df_silver['attributes_dict'] = df_silver['attributes'].apply(parse_dict_string)

# -----------------------------------------
# Features importantes
# -----------------------------------------
df_silver['has_delivery'] = df_silver['attributes_dict'].apply(
    lambda x: x.get('RestaurantsDelivery', 'False') == 'True'
)

df_silver['has_outdoor'] = df_silver['attributes_dict'].apply(
    lambda x: x.get('OutdoorSeating', 'False') == 'True'
)

# -----------------------------------------
# Faixa de preço
# -----------------------------------------
def get_price(x):

    val = x.get('RestaurantsPriceRange2', '1')

    return int(val) if val and val.isdigit() else 1

df_silver['price_range'] = df_silver['attributes_dict'].apply(get_price)

# -----------------------------------------
# Categories
# -----------------------------------------
df_silver['categories_list'] = df_silver['categories'].apply(
    lambda x: x.split(', ') if isinstance(x, str) else []
)

# -----------------------------------------
# Embeddings
# -----------------------------------------
df_silver['embedding_list'] = df_silver['embedding'].apply(
    lambda x: ast.literal_eval(x) if isinstance(x, str) else x
)

# -----------------------------------------
# Limpeza final
# -----------------------------------------
df_silver = df_silver.drop(
    columns=['attributes', 'attributes_dict', 'hours', 'is_open'],
    errors='ignore'
)

print(f"Registros Silver: {len(df_silver)}")

# Salvar local
os.makedirs("silver", exist_ok=True)

df_silver.to_parquet(
    "silver/silver_data.parquet",
    engine='pyarrow',
    index=False
)

# Upload MinIO
df_silver.to_parquet(
    "s3://silver/silver_data.parquet",
    engine='pyarrow',
    index=False,
    storage_options=credenciais_minio
)

print("Silver enviado para MinIO!")

# =====================================================
# CAMADA GOLD
# =====================================================

print("\n==============================")
print("CAMADA GOLD")
print("==============================")

df_gold = df_silver.copy()

# -----------------------------------------
# Score inteligente
# -----------------------------------------
df_gold['log_reviews'] = np.log1p(df_gold['review_count'])

scaler = MinMaxScaler()

df_gold[['stars_norm', 'reviews_norm']] = scaler.fit_transform(
    df_gold[['stars', 'log_reviews']]
)

# Score final
df_gold['gold_score'] = (
    df_gold['stars_norm'] * 0.7
    +
    df_gold['reviews_norm'] * 0.3
)

# -----------------------------------------
# Contexto para RAG
# -----------------------------------------
df_gold['rag_context'] = df_gold.apply(
    lambda row:
        f"Nome: {row['name']}. "
        f"Local: {row['city']}. "
        f"Estilo: {row['categories']}. "
        f"Avaliação: {row['stars']} estrelas ({row['review_count']} reviews). "
        f"Delivery: {'Sim' if row['has_delivery'] else 'Não'}. "
        f"Score: {row['gold_score']:.2f}.",
    axis=1
)

# -----------------------------------------
# Seleção final
# -----------------------------------------
colunas_gold = [
    'business_id',
    'name',
    'city',
    'categories',
    'categories_list',
    'price_range',
    'has_delivery',
    'has_outdoor',
    'stars',
    'review_count',
    'gold_score',
    'rag_context',
    'embedding_list'
]

df_gold = df_gold[colunas_gold]

print(f"Registros Gold: {len(df_gold)}")

# Salvar local
os.makedirs("gold", exist_ok=True)

df_gold.to_parquet(
    "gold/gold_data.parquet",
    engine='pyarrow',
    index=False
)

# Upload MinIO
df_gold.to_parquet(
    "s3://gold/gold_data.parquet",
    engine='pyarrow',
    index=False,
    storage_options=credenciais_minio
)

print("Gold enviado para MinIO!")

# =====================================================
# FINAL
# =====================================================

print("\n===================================")
print("PIPELINE FINALIZADO COM SUCESSO")
print("Bronze -> Silver -> Gold")
print("Dados enviados para o MinIO")
print("===================================")