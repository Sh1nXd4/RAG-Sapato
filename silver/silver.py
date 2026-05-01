# import pandas as pd
# import ast
# import os

# def process_silver():
#     print("Iniciando processamento Silver...")
    
#     # 1. Descobre o caminho absoluto dinamicamente
#     # Pega a pasta onde este script (silver.py) está: RAG-Sapato/silver
#     diretorio_atual = os.path.dirname(os.path.abspath(__file__))
#     # Sobe um nível para chegar na raiz do projeto: RAG-Sapato
#     diretorio_raiz = os.path.dirname(diretorio_atual)
    
#     # Monta o caminho exato do CSV na raiz
#     caminho_bronze = os.path.join(diretorio_raiz, 'bronze', 'restaurants_with_embeddings.csv')      
#     print(f"Lendo dados de: {caminho_bronze}")
#     df = pd.read_csv(caminho_bronze)
    
#     # Filtrar apenas restaurantes abertos
#     df = df[df['is_open'] == 1].copy()
    
#     # Função segura para converter string de dicionário
#     def parse_dict_string(x):
#         if pd.isna(x): return {}
#         try:
#             clean_str = str(x).replace('""', '"').replace("u'", "'")
#             return ast.literal_eval(clean_str)
#         except:
#             return {}

#     df['attributes_dict'] = df['attributes'].apply(parse_dict_string)
    
#     # Extrair features úteis
#     df['has_delivery'] = df['attributes_dict'].apply(lambda x: x.get('RestaurantsDelivery', 'False') == 'True')
#     df['has_outdoor'] = df['attributes_dict'].apply(lambda x: x.get('OutdoorSeating', 'False') == 'True')
    
#     def get_price(x):
#         val = x.get('RestaurantsPriceRange2', '1')
#         return int(val) if val and val.isdigit() else 1
        
#     df['price_range'] = df['attributes_dict'].apply(get_price)
    
#     # Converter embedding de String para Lista
#     df['embedding_list'] = df['embedding'].apply(lambda x: ast.literal_eval(x) if isinstance(x, str) else x)
    
#     # Dropar colunas desnecessárias
#     df_silver = df.drop(columns=['attributes', 'attributes_dict', 'hours', 'is_open'], errors='ignore')
    
#     # 2. Monta o caminho exato para salvar na pasta silver
#     caminho_saida = os.path.join(diretorio_atual, 'silver_data.parquet')
#     df_silver.to_parquet(caminho_saida, engine='pyarrow', index=False)
    
#     print(f"Camada Silver finalizada! Salvo em: {caminho_saida}")

# if __name__ == "__main__":
#     process_silver()


import pandas as pd
import ast
import os

def process_silver():
    print(" Iniciando processamento Silver...")
    
    diretorio_atual = os.path.dirname(os.path.abspath(__file__))
    diretorio_raiz = os.path.dirname(diretorio_atual)
    
    caminho_bronze = os.path.join(diretorio_raiz, 'bronze', 'restaurants_with_embeddings.csv')      
    print(f"Lendo dados de: {caminho_bronze}")
    
    df = pd.read_csv(caminho_bronze)

    # =====================================================
    # FILTRO
    # =====================================================
    df = df[df['is_open'] == 1].copy()

    # =====================================================
    # PARSE DE ATTRIBUTES
    # =====================================================
    def parse_dict_string(x):
        if pd.isna(x): return {}
        try:
            clean_str = str(x).replace('""', '"').replace("u'", "'")
            return ast.literal_eval(clean_str)
        except:
            return {}

    df['attributes_dict'] = df['attributes'].apply(parse_dict_string)

    # =====================================================
    # FEATURES IMPORTANTES
    # =====================================================
    df['has_delivery'] = df['attributes_dict'].apply(
        lambda x: x.get('RestaurantsDelivery', 'False') == 'True'
    )

    df['has_outdoor'] = df['attributes_dict'].apply(
        lambda x: x.get('OutdoorSeating', 'False') == 'True'
    )

    def get_price(x):
        val = x.get('RestaurantsPriceRange2', '1')
        return int(val) if val and val.isdigit() else 1
        
    df['price_range'] = df['attributes_dict'].apply(get_price)

    # =====================================================
    # NOVO: TRATAMENTO DE CATEGORIES
    # =====================================================
    df['categories_list'] = df['categories'].apply(
        lambda x: x.split(', ') if isinstance(x, str) else []
    )

    # =====================================================
    # EMBEDDING
    # =====================================================
    df['embedding_list'] = df['embedding'].apply(
        lambda x: ast.literal_eval(x) if isinstance(x, str) else x
    )

    # =====================================================
    # LIMPEZA FINAL
    # =====================================================
    df_silver = df.drop(
        columns=['attributes', 'attributes_dict', 'hours', 'is_open'],
        errors='ignore'
    )

    caminho_saida = os.path.join(diretorio_atual, 'silver_data.parquet')
    df_silver.to_parquet(caminho_saida, engine='pyarrow', index=False)


    import matplotlib.pyplot as plt

    # =====================================================
    # 1. MAPA DE CORRELAÇÃO
    # =====================================================
    print(" Gerando mapa de correlação...")

    df_corr = df[['stars', 'review_count', 'price_range', 'has_delivery', 'has_outdoor']].copy()
    df_corr['has_delivery'] = df_corr['has_delivery'].astype(int)
    df_corr['has_outdoor'] = df_corr['has_outdoor'].astype(int)

    corr = df_corr.corr()

    plt.figure()
    plt.imshow(corr)
    plt.colorbar()
    plt.xticks(range(len(corr.columns)), corr.columns, rotation=45)
    plt.yticks(range(len(corr.columns)), corr.columns)
    plt.title("Mapa de Correlação")
    plt.tight_layout()
    plt.savefig("correlation_matrix.png")
    plt.close()


    # =====================================================
    # 2. DISTRIBUIÇÃO DE NOTAS
    # =====================================================
    print(" Gerando distribuição de estrelas...")

    plt.figure()
    plt.hist(df['stars'], bins=10)
    plt.title("Distribuição de Avaliações (Stars)")
    plt.xlabel("Stars")
    plt.ylabel("Frequência")
    plt.savefig("stars_distribution.png")
    plt.close()


    # =====================================================
    # 3. DELIVERY vs AVALIAÇÃO
    # =====================================================
    print(" Comparando delivery vs avaliação...")

    df.groupby('has_delivery')['stars'].mean().plot(kind='bar')

    plt.title("Média de Avaliação por Delivery")
    plt.xlabel("Possui Delivery")
    plt.ylabel("Média de Stars")
    plt.savefig("delivery_vs_rating.png")
    plt.close()


    # =====================================================
    # 4. REVIEW COUNT vs STARS
    # =====================================================
    print(" Relação entre reviews e avaliação...")

    plt.figure()
    plt.scatter(df['review_count'], df['stars'])
    plt.title("Review Count vs Stars")
    plt.xlabel("Quantidade de Reviews")
    plt.ylabel("Stars")
    plt.savefig("reviews_vs_stars.png")
    plt.close()

    print(f" Silver finalizado! Salvo em: {caminho_saida}")


if __name__ == "__main__":
    process_silver()