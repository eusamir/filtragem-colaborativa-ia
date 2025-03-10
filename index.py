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

# 4. Calcular a similaridade entre os clientes (não entre os produtos)
customer_similarity_matrix = cosine_similarity(customer_product_matrix)

# 5. Transformar a matriz de similaridade entre clientes em um DataFrame para facilitar a leitura
customer_similarity_df = pd.DataFrame(customer_similarity_matrix, index=customer_product_matrix.index, columns=customer_product_matrix.index)

# Função para recomendar produtos com base na filtragem colaborativa entre clientes
def recommend_similar_products_collaborative(customer_id, customer_product_matrix, customer_similarity_df, top_n=5):
    # Obter os clientes mais semelhantes ao cliente-alvo (excluindo o próprio cliente)
    similar_customers = customer_similarity_df[customer_id].sort_values(ascending=False)[1:].head(top_n).index.tolist()
    
    # Dicionário para armazenar as pontuações de recomendação
    recommendation_scores = {}

    # Para cada cliente semelhante, verificar os produtos que ele comprou
    for similar_customer in similar_customers:
        purchased_products = customer_product_matrix.loc[similar_customer][customer_product_matrix.loc[similar_customer] > 0].index.tolist()
        
        for product in purchased_products:
            # Verificar se o cliente já comprou o produto
            if customer_product_matrix.loc[customer_id, product] == 0:
                if product in recommendation_scores:
                    recommendation_scores[product] += 1
                else:
                    recommendation_scores[product] = 1

    # Ordenar os produtos recomendados por pontuação e retornar os top_n produtos
    recommended_products = sorted(recommendation_scores.items(), key=lambda x: x[1], reverse=True)[:top_n]

    return [product for product, score in recommended_products]

# Exemplo: recomendação para um cliente específico
customer_id = 13047  # Exemplo de ID de cliente
recommended_products = recommend_similar_products_collaborative(customer_id, customer_product_matrix, customer_similarity_df, top_n=5)

# Exibir os produtos recomendados
print(f"Produtos recomendados para o cliente {customer_id}: {recommended_products}")
