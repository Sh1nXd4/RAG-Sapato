import pandas as pd
import os

# 1. Criar a estrutura de pastas simulando os Buckets (Data Lake)
pastas = ['bronze', 'silver', 'gold']
for pasta in pastas:
    os.makedirs(pasta, exist_ok=True)
    print(f"Pasta '{pasta}' verificada/criada.")

print("\nIniciando Pipeline de Ingestão...")

# ==========================================
# CAMADA BRONZE (Raw Data - Dados Brutos)
# ==========================================
print("Processando Camada Bronze...")
# Lê o CSV original
df_raw = pd.read_csv('food_coded.csv')
# Salva exatamente como chegou, garantindo o histórico
df_raw.to_csv('bronze/food_coded_raw.csv', index=False)


# ==========================================
# CAMADA SILVER (Cleaned Data - Dados Limpos)
# ==========================================
print("Processando Camada Silver...")
df_silver = df_raw.copy()

# Regra 1: Remover colunas duplicadas (seu CSV tem 'comfort_food_reasons_coded' duas vezes)
df_silver = df_silver.loc[:, ~df_silver.columns.duplicated()]

# Regra 2: Tratar tipos de dados (Garantir que GPA e weight sejam números)
# O parâmetro errors='coerce' transforma textos inválidos (como "nan") em nulos reais do sistema
df_silver['GPA'] = pd.to_numeric(df_silver['GPA'], errors='coerce')
df_silver['weight'] = pd.to_numeric(df_silver['weight'], errors='coerce')

# Regra 3: Tratar valores nulos em colunas de texto
df_silver['comfort_food'] = df_silver['comfort_food'].fillna('Nao Informado')
df_silver['fav_cuisine'] = df_silver['fav_cuisine'].fillna('Nao Informado')

# Regra 4: Padronizar nomes das colunas para minúsculo (boa prática)
df_silver.columns = [col.lower() for col in df_silver.columns]

# Salva em formato Parquet (mais leve e rápido para analytics)
df_silver.to_parquet('silver/food_coded_cleaned.parquet', index=False)


# ==========================================
# CAMADA GOLD (Business/Analytics - Dados Agregados)
# ==========================================
print("Processando Camada Gold...")
# Pergunta de negócio 1: Qual a média de GPA e Peso por Gênero?
df_gold_genero = df_silver.groupby('gender').agg(
    media_gpa=('gpa', 'mean'),
    media_peso=('weight', 'mean'),
    total_estudantes=('gender', 'count')
).reset_index()

# Pergunta de negócio 2: Quais as comidas de conforto mais citadas por quem pratica esportes?
df_gold_esportes = df_silver[df_silver['sports'] == 1].groupby('comfort_food').size().reset_index(name='contagem')
df_gold_esportes = df_gold_esportes.sort_values(by='contagem', ascending=False).head(10)

# Salva as tabelas agregadas prontas para o BI/Dashboard
df_gold_genero.to_parquet('gold/metricas_por_genero.parquet', index=False)
df_gold_esportes.to_parquet('gold/top_comfort_food_esportistas.parquet', index=False)

print("\nPipeline concluído com sucesso! Verifique as pastas bronze, silver e gold.")
