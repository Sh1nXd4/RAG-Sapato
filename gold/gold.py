# import pandas as pd
# import numpy as np
# import os
# from sklearn.preprocessing import MinMaxScaler

# def process_gold():
#     print("Iniciando processamento Gold...")
    
#     # Ler o dado limpo da Silver
#     caminho_silver = 'silver/silver_data.parquet'
#     df = pd.read_parquet(caminho_silver)
    
#     # 1. Regra de Negócio: Score de Confiança/Popularidade
#     # Suaviza a contagem de reviews para não desbalancear demais
#     df['log_reviews'] = np.log1p(df['review_count'])
    
#     scaler = MinMaxScaler()
#     df[['stars_norm', 'reviews_norm']] = scaler.fit_transform(df[['stars', 'log_reviews']])
    
#     # Peso: 70% pra nota, 30% pro volume de avaliações
#     df['gold_score'] = (df['stars_norm'] * 0.7) + (df['reviews_norm'] * 0.3)
    
#     # 2. Criação do Contexto para o RAG (O que o LLM vai ler)
#     df['rag_context'] = df.apply(
#         lambda row: f"Nome: {row['name']}. "
#                     f"Local: {row['city']}. "
#                     f"Estilo: {row['categories']}. "
#                     f"Avaliação: {row['stars']} estrelas ({row['review_count']} reviews). "
#                     f"Delivery: {'Sim' if row['has_delivery'] else 'Não'}. "
#                     f"Score de recomendação interno: {row['gold_score']:.2f}.", 
#         axis=1
#     )
    
#     # 3. Selecionar apenas o necessário para o Banco Vetorial
#     colunas_gold = [
#         'business_id', 'name', 'city', 'categories', 'price_range', 
#         'has_delivery', 'stars', 'gold_score', 'rag_context', 'embedding_list'
#     ]
#     df_gold = df[colunas_gold]
    
#     # Salvar o dado final
#     caminho_saida = 'gold/gold_data.parquet'
#     os.makedirs('gold', exist_ok=True)
#     df_gold.to_parquet(caminho_saida, engine='pyarrow', index=False)
    
#     print(f"Camada Gold finalizada! Salvo em: {caminho_saida}")

# if __name__ == "__main__":
#     process_gold()


import pandas as pd
import numpy as np
import os
from sklearn.preprocessing import MinMaxScaler

def process_gold():
    print(" Iniciando processamento Gold...")
    
    diretorio_atual = os.path.dirname(os.path.abspath(__file__))
    diretorio_raiz = os.path.dirname(diretorio_atual)

    caminho_silver = os.path.join(diretorio_raiz, 'silver', 'silver_data.parquet')

    print(f"Lendo dados de: {caminho_silver}")
    df = pd.read_parquet(caminho_silver)

    # =====================================================
    # SCORE
    # =====================================================
    df['log_reviews'] = np.log1p(df['review_count'])

    scaler = MinMaxScaler()
    df[['stars_norm', 'reviews_norm']] = scaler.fit_transform(
        df[['stars', 'log_reviews']]
    )

    df['gold_score'] = (df['stars_norm'] * 0.7) + (df['reviews_norm'] * 0.3)

    # =====================================================
    # RAG
    # =====================================================
    df['rag_context'] = df.apply(
        lambda row: f"Nome: {row['name']}. "
                    f"Local: {row['city']}. "
                    f"Estilo: {row['categories']}. "
                    f"Avaliação: {row['stars']} estrelas ({row['review_count']} reviews). "
                    f"Delivery: {'Sim' if row['has_delivery'] else 'Não'}. "
                    f"Score: {row['gold_score']:.2f}.",
        axis=1
    )

    # =====================================================
    # COLUNAS CORRIGIDAS
    # =====================================================
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

    df_gold = df[colunas_gold]

    caminho_saida = 'gold_data.parquet'
    os.makedirs('gold', exist_ok=True)
    df_gold.to_parquet(caminho_saida, engine='pyarrow', index=False)

    print(f" Gold finalizado! Salvo em: {caminho_saida}")


if __name__ == "__main__":
    process_gold()