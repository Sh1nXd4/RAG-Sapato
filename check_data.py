import pandas as pd

# Carrega os dados processados
df = pd.read_parquet('gold/gold_data.parquet')

# Mostra as primeiras 5 linhas e informações das colunas
print("--- Primeiras Linhas ---")
print(df.head())
print("\n--- Informações das Colunas ---")
print(df.info())