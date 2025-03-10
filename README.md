# Recomendador de Produtos com Filtragem Colaborativa

Este projeto implementa um sistema de recomendação de produtos com base na similaridade entre clientes, utilizando a métrica de **similaridade do cosseno**.

## 📂 Estrutura dos Dados
O dataset utilizado contém registros de compras realizadas por clientes em uma loja. Os dados possuem as seguintes colunas:

- **InvoiceNo**: Número da fatura da transação.
- **StockCode**: Código do produto comprado.
- **Description**: Descrição do produto.
- **Quantity**: Quantidade comprada.
- **InvoiceDate**: Data e hora da compra.
- **UnitPrice**: Preço unitário do produto.
- **CustomerID**: Identificação única do cliente.
- **Country**: País de origem do cliente.

⚠️ **Pré-processamento realizado:**
1. Conversão da coluna `InvoiceDate` para formato datetime.
2. Remoção de transações com `Quantity <= 0`.
3. Remoção de registros com valores ausentes em `CustomerID` ou `StockCode`.

## 🛠️ Implementação
O sistema foi desenvolvido em **Python** utilizando as seguintes bibliotecas:

- `pandas` → Para manipulação de dados.
- `scikit-learn` → Para cálculo da similaridade do cosseno.

### 🔹 Passos da implementação
1. **Criação da matriz Cliente x Produto**
   - Cada linha representa um cliente e cada coluna, um produto.
   - O valor da célula é a quantidade comprada do produto pelo cliente.
2. **Cálculo da similaridade entre clientes**
   - Utilizando a métrica de **similaridade do cosseno** para comparar padrões de compra.
3. **Geração de recomendações**
   - Para um cliente específico, identificamos clientes similares e recomendamos produtos que ele ainda não comprou.

### 🔹 Função principal
```python
recommend_similar_products_collaborative(customer_id, customer_product_matrix, customer_similarity_df, top_n=5)
```
**Parâmetros:**
- `customer_id`: ID do cliente para quem queremos recomendar produtos.
- `customer_product_matrix`: Matriz Cliente x Produto.
- `customer_similarity_df`: DataFrame com similaridades entre clientes.
- `top_n`: Número de produtos a recomendar (padrão = 5).

## 🚀 Exemplo de Uso
```python
customer_id = 13047  # Exemplo de cliente
recommended_products = recommend_similar_products_collaborative(customer_id, customer_product_matrix, customer_similarity_df, top_n=5)
print(f"Produtos recomendados para o cliente {customer_id}: {recommended_products}")
```