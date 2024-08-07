import pandas as pd
import numpy as np
import streamlit as st
import plotly.express as px
from datetime import datetime, timedelta
import random

# Configurações iniciais
np.random.seed(42)
random.seed(42)

# Período de tempo para os dados
start_date = datetime(2023, 1, 1)
end_date = datetime(2024, 8, 1)
dates = pd.date_range(start_date, end_date)

# Categorias e produtos
categorias = ['Eletrônicos', 'Roupas', 'Alimentos', 'Brinquedos', 'Móveis']
produtos = {
    'Eletrônicos': ['Smartphone', 'Laptop', 'TV', 'Headphones'],
    'Roupas': ['Camisa', 'Calça', 'Jaqueta', 'Sapatos'],
    'Alimentos': ['Arroz', 'Feijão', 'Leite', 'Pão'],
    'Brinquedos': ['Boneca', 'Carrinho', 'Quebra-Cabeça', 'Lego'],
    'Móveis': ['Mesa', 'Cadeira', 'Sofá', 'Cama']
}

# Regiões
regioes = ['Norte', 'Sul', 'Leste', 'Oeste']

# Gerar dados de vendas
dados = []
for date in dates:
    for categoria in categorias:
        for produto in produtos[categoria]:
            for regiao in regioes:
                vendas = np.random.poisson(lam=20)
                preco = np.random.uniform(10, 100)
                custo = preco * np.random.uniform(0.5, 0.8)
                receita = vendas * preco
                lucro = receita - (vendas * custo)
                dados.append([date, categoria, produto, regiao, vendas, receita, custo, lucro])

# Criar DataFrame
df = pd.DataFrame(dados, columns=['Data', 'Categoria', 'Produto', 'Região', 'Vendas', 'Receita', 'Custo', 'Lucro'])

# Função para prever vendas futuras usando média móvel
def prever_vendas(df, periods=30):
    df['Previsão_Vendas'] = df['Vendas'].rolling(window=periods).mean().shift(-periods)
    return df

# Aplicar a previsão de vendas
df = df.groupby(['Categoria', 'Produto', 'Região']).apply(prever_vendas).reset_index(drop=True)

# Configurações do Streamlit
st.set_page_config(page_title="Dashboard de Vendas", layout="wide")

# Título
st.title("Dashboard de Análise de Vendas")

# Filtros
st.sidebar.header("Filtros")

# Seleção de categoria
categorias = df['Categoria'].unique()
categoria_selecionada = st.sidebar.selectbox("Categoria", categorias)

# Seleção de produto
produtos = df[df['Categoria'] == categoria_selecionada]['Produto'].unique()
produto_selecionado = st.sidebar.selectbox("Produto", produtos)

# Seleção de região
regioes = df['Região'].unique()
regiao_selecionada = st.sidebar.selectbox("Região", regioes)

# Filtrar dados com base nas seleções
df_filtrado = df[(df['Categoria'] == categoria_selecionada) & 
                 (df['Produto'] == produto_selecionado) & 
                 (df['Região'] == regiao_selecionada)]

# Visualizações
st.subheader(f"Vendas de {produto_selecionado} na região {regiao_selecionada}")

# Gráfico de Vendas ao longo do tempo
fig_vendas = px.bar(df_filtrado, x='Data', y='Vendas', title='Vendas ao Longo do Tempo')
st.plotly_chart(fig_vendas, use_container_width=True)

# Gráfico de Receita ao longo do tempo
fig_receita = px.bar(df_filtrado, x='Data', y='Receita', title='Receita ao Longo do Tempo')
st.plotly_chart(fig_receita, use_container_width=True)

# Gráfico de Previsão de Vendas
fig_previsao = px.bar(df_filtrado, x='Data', y='Previsão_Vendas', title='Previsão de Vendas')
st.plotly_chart(fig_previsao, use_container_width=True)

# Métricas
total_vendas = df_filtrado['Vendas'].sum()
total_receita = df_filtrado['Receita'].sum()
total_lucro = df_filtrado['Lucro'].sum()

st.subheader("Métricas Gerais")
st.metric("Total de Vendas", total_vendas)
st.metric("Total de Receita", f"R$ {total_receita:,.2f}")
st.metric("Total de Lucro", f"R$ {total_lucro:,.2f}")

# Download do DataFrame filtrado
csv = df_filtrado.to_csv(index=False)
st.download_button(
    label="Baixar dados filtrados",
    data=csv,
    file_name='dados_filtrados.csv',
    mime='text/csv',
)

# Exibir DataFrame filtrado
st.subheader("Dados Filtrados")
st.dataframe(df_filtrado)