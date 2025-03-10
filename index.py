import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity

# Carregar os dados de vendas
sales_data = pd.read_csv('dados.csv')

# 1. Converter a coluna 'InvoiceDate' para datetime para facilitar manipulação
sales_data['InvoiceDate'] = pd.to_datetime(sales_data['InvoiceDate'])

# 2. Remover transações com quantidade negativa (indicando possíveis cancelamentos) e dados ausentes
sales_data = sales_data[sales_data['Quantity'] > 0]
sales_data = sales_data.dropna(subset=['CustomerID', 'StockCode'])

# 3. Criar a matriz de interação Cliente x Produto
# Cada linha representa um cliente e cada coluna, um produto. O valor é a quantidade comprada.
customer_product_matrix = sales_data.pivot_table(index='CustomerID', columns='StockCode', values='Quantity', aggfunc='sum', fill_value=0)

# 4. Calcular a similaridade entre produtos usando o método de cosseno
# Quanto mais alta a similaridade, mais semelhantes são os produtos.
product_similarity_matrix = cosine_similarity(customer_product_matrix.T)



# Transformar a matriz de similaridade em um DataFrame para facilitar a leitura
product_similarity_df = pd.DataFrame(product_similarity_matrix, index=customer_product_matrix.columns, columns=customer_product_matrix.columns)

# Função para recomendar produtos com base nas compras passadas de um cliente
def recommend_similar_products(customer_id, customer_product_matrix, product_similarity_df, top_n=5):
    # Obter os produtos comprados pelo cliente
    purchased_products = customer_product_matrix.loc[customer_id][customer_product_matrix.loc[customer_id] > 0].index.tolist()
    
    # Dicionário para armazenar as pontuações de recomendação
    recommendation_scores = {}
    
    # Para cada produto comprado, verificar os produtos mais semelhantes
    for product in purchased_products:
        similar_products = product_similarity_df[product]
        
        # Adicionar a pontuação de cada produto similar
        for similar_product, similarity_score in similar_products.items():
            # Não recomendar o mesmo produto que o cliente já comprou
            if similar_product not in purchased_products:
                if similar_product in recommendation_scores:
                    recommendation_scores[similar_product] += similarity_score
                else:
                    recommendation_scores[similar_product] = similarity_score
    
    # Ordenar os produtos recomendados por pontuação e retornar os top_n produtos
    recommended_products = sorted(recommendation_scores.items(), key=lambda x: x[1], reverse=True)[:top_n]
    
    # Retornar apenas os nomes dos produtos recomendados
    return [product for product, score in recommended_products]

# Exemplo: recomendação para um cliente específico
customer_id = 13047  # Exemplo de ID de cliente
recommended_products = recommend_similar_products(customer_id, customer_product_matrix, product_similarity_df, top_n=5)

# Exibir os produtos recomendados
print(f"Produtos recomendados para o cliente {customer_id}: {recommended_products}")
