import pandas as pd
import streamlit as st

# Carrega o Excel
df = pd.read_excel('ProdMecânico.xlsx')

# Título
st.title('Produtividade Geral 🏍️')

# Conversão de data
df['Data'] = pd.to_datetime(df['Data'])

# Remove espaços extras nos nomes dos líderes
df['Líder'] = df['Líder'].str.strip()

# Cria a coluna de semana (ano-semana)
df['Semana'] = df['Data'].dt.strftime('%Y-%U')

# Criação dos quadrantes sem numpy
def definir_quadrante(lider):
    if lider == 'João Belo':
        return 'Quadrante I'
    elif lider == 'Maxsuel Conceição':
        return 'Quadrante II'
    elif lider == 'Leilson Alves':
        return 'Quadrante III'
    elif lider == 'Jamerson Igor':
        return 'Quadrante IV'
    else:
        return 'Outro'

df['Quadrante'] = df['Líder'].apply(definir_quadrante)

# Filtro de semana
semana_selecionada = st.sidebar.selectbox("📅 Selecione a Semana", df['Semana'].unique())

df_filtrado = df[df['Semana'] == semana_selecionada]

# Pega os dias únicos dessa semana e ordena
dias_semana = sorted(df_filtrado['Data'].dt.strftime('%d/%m/%Y').unique())

# Exibe intervalo de datas
dias_formatados = " - ".join([dias_semana[0], dias_semana[-1]]) if dias_semana else "Sem dados disponíveis"

st.write(f"## 📊 Semana: {semana_selecionada}")
st.write(f'#### Dias: {dias_formatados}')

# Exibe o DataFrame filtrado
st.write(df_filtrado)

tm_cliente = df_filtrado['Cliente'].sum()

# Seu código de cálculos (sem alterações)
df_q1 = df_filtrado[df_filtrado['Quadrante'] == 'Quadrante I']
df_q1_cliente = df_q1['Cliente'].sum()
df_q1_interna = df_q1['Interna'].sum()
df_q1_mec_presente = len(df_q1)
df_q1_total = df_q1_cliente + df_q1_interna
df_q1_perdidas = df_q1['Perdidas'].sum()
df_q1_produtividade = df_q1_total / df_q1_mec_presente if df_q1_mec_presente else 0

df_q2 = df_filtrado[df_filtrado['Quadrante'] == 'Quadrante II']
df_q2_cliente = df_q2['Cliente'].sum()
df_q2_interna = df_q2['Interna'].sum()
df_q2_mec_presente = len(df_q2)
df_q2_total = df_q2_cliente + df_q2_interna
df_q2_perdidas = df_q2['Perdidas'].sum()
df_q2_produtividade = df_q2_total / df_q2_mec_presente if df_q2_mec_presente else 0

df_q3 = df_filtrado[df_filtrado['Quadrante'] == 'Quadrante III']
df_q3_cliente = df_q3['Cliente'].sum()
df_q3_interna = df_q3['Interna'].sum()
df_q3_mec_presente = len(df_q3)
df_q3_total = df_q3_cliente + df_q3_interna
df_q3_perdidas = df_q3['Perdidas'].sum()
df_q3_produtividade = df_q3_total / df_q3_mec_presente if df_q3_mec_presente else 0

df_q4 = df_filtrado[df_filtrado['Quadrante'] == 'Quadrante IV']
df_q4_cliente = df_q4['Cliente'].sum()
df_q4_interna = df_q4['Interna'].sum()
df_q4_mec_presente = len(df_q4)
df_q4_total = df_q4_cliente + df_q4_interna
df_q4_perdidas = df_q4['Perdidas'].sum()
df_q4_produtividade = df_q4_total / df_q4_mec_presente if df_q4_mec_presente else 0

# Exibe totais
st.write(f'### Total de Manutenções Realizadas:')
st.write(f'###### {tm_cliente}')

col1, col2, col3, col4 = st.columns(4)
col1.metric("Quadrante I   - Cliente", f"{df_q1_cliente}")
col2.metric("Quadrante II  - Cliente", f"{df_q2_cliente}")
col3.metric("Quadrante III - Cliente", f"{df_q3_cliente}")
col4.metric("Quadrante IV  - Cliente", f"{df_q4_cliente}")

col5, col6, col7, col8 = st.columns(4)
col5.metric("Quadrante I   - Interna", f"{df_q1_interna}")
col6.metric("Quadrante II  - Interna", f"{df_q2_interna}")
col7.metric("Quadrante III - Interna", f"{df_q3_interna}")
col8.metric("Quadrante IV  - Interna", f"{df_q4_interna}")

col9, col10, col11, col12 = st.columns(4)
col9.metric("Quadrante I    - Mec Presentes", f"{df_q1_mec_presente}")
col10.metric("Quadrante II  - Mec Presentes", f"{df_q2_mec_presente}")
col11.metric("Quadrante III - Mec Presentes", f"{df_q3_mec_presente}")
col12.metric("Quadrante IV  - Mec Presentes", f"{df_q4_mec_presente}")

col13, col14, col15, col16 = st.columns(4)
col13.metric("Quadrante I    - Perdidas", f"{df_q1_perdidas}")
col14.metric("Quadrante II   - Perdidas", f"{df_q2_perdidas}")
col15.metric("Quadrante III  - Perdidas", f"{df_q3_perdidas}")
col16.metric("Quadrante IV   - Perdidas", f"{df_q4_perdidas}")

col17, col18, col19, col20 = st.columns(4)
col17.metric("Quadrante I    - Produtividade", f"{df_q1_produtividade:.2f}")
col18.metric("Quadrante II   - Produtividade", f"{df_q2_produtividade:.2f}")
col19.metric("Quadrante III  - Produtividade", f"{df_q3_produtividade:.2f}")
col20.metric("Quadrante IV   - Produtividade", f"{df_q4_produtividade:.2f}")

# Soma total dos percentuais
if tm_cliente != 0:
    percentual_oficina = (df_q1_cliente + df_q2_cliente + df_q3_cliente + df_q4_cliente) / tm_cliente * 100
    st.write(f'Soma Percentual - Oficina: {percentual_oficina:.2f}%')

# --- Parte Nova: Determinar os melhores quadrantes ---
st.markdown("## 🏆 Top Quadrantes")

# Organiza os dados em um dicionário
dados_quadrantes = {
    'Quadrante I': {
        'Cliente': df_q1_cliente,
        'Interna': df_q1_interna,
        'Mec_Presentes': df_q1_mec_presente,
        'Perdidas': df_q1_perdidas,
        'Produtividade': df_q1_produtividade,
    },
    'Quadrante II': {
        'Cliente': df_q2_cliente,
        'Interna': df_q2_interna,
        'Mec_Presentes': df_q2_mec_presente,
        'Perdidas': df_q2_perdidas,
        'Produtividade': df_q2_produtividade,
    },
    'Quadrante III': {
        'Cliente': df_q3_cliente,
        'Interna': df_q3_interna,
        'Mec_Presentes': df_q3_mec_presente,
        'Perdidas': df_q3_perdidas,
        'Produtividade': df_q3_produtividade,
    },
    'Quadrante IV': {
        'Cliente': df_q4_cliente,
        'Interna': df_q4_interna,
        'Mec_Presentes': df_q4_mec_presente,
        'Perdidas': df_q4_perdidas,
        'Produtividade': df_q4_produtividade,
    }
}

# Função para gerar Top 4
def gerar_top4(dados, chave, ordem_decrescente=True):
    return sorted(dados.items(), key=lambda x: x[1][chave], reverse=ordem_decrescente)

# Gera Top 4 de cada categoria
top4_cliente = gerar_top4(dados_quadrantes, 'Cliente')
top4_interna = gerar_top4(dados_quadrantes, 'Interna')
top4_mec_presentes = gerar_top4(dados_quadrantes, 'Mec_Presentes')
top4_perdidas = gerar_top4(dados_quadrantes, 'Perdidas', ordem_decrescente=False)  # Menor é melhor
top4_produtividade = gerar_top4(dados_quadrantes, 'Produtividade')

# Exibe Top 4

def exibir_top4(nome_categoria, top4):
    st.write(f"**{nome_categoria}:**")
    for idx, (quadrante, dados) in enumerate(top4, start=1):
        st.write(f"{idx}º - {quadrante}: {dados[nome_categoria]}")

# Cliente
st.write('#### Cliente (Mais manutenções)')
for i, (quadrante, valores) in enumerate(top4_cliente, start=1):
    st.write(f"{i}º - {quadrante}: {valores['Cliente']} manutenções")

# Interna
st.write('#### Interna (Mais manutenções internas)')
for i, (quadrante, valores) in enumerate(top4_interna, start=1):
    st.write(f"{i}º - {quadrante}: {valores['Interna']} manutenções")

# Mecânicos Presentes
st.write('#### Mecânicos Presentes (Maior número)')
for i, (quadrante, valores) in enumerate(top4_mec_presentes, start=1):
    st.write(f"{i}º - {quadrante}: {valores['Mec_Presentes']} mecânicos")

# Perdidas
st.write('#### Perdidas (Menor quantidade de perdas)')
for i, (quadrante, valores) in enumerate(top4_perdidas, start=1):
    st.write(f"{i}º - {quadrante}: {valores['Perdidas']} perdas")

# Produtividade
st.write('#### Produtividade (Maior produtividade)')
for i, (quadrante, valores) in enumerate(top4_produtividade, start=1):
    st.write(f"{i}º - {quadrante}: {valores['Produtividade']:.2f} produtividade")


# 🔍 Análises detalhadas por mecânico
st.markdown("## 🔍 Análise por Mecânico")

# Agrupamento por mecânico
mecanicos_df = df_filtrado.groupby('Mecânico')[['Cliente', 'Interna', 'Perdidas']].sum()

# Cálculo dos totais
mecanicos_df['Total'] = mecanicos_df['Cliente'] + mecanicos_df['Interna']
mecanicos_df['Total_Com_Perdida'] = mecanicos_df['Total'] + mecanicos_df['Perdidas']

# Criando dicionário de mecânico → líder
mec_lider_dict = df_filtrado.drop_duplicates(subset='Mecânico').set_index('Mecânico')['Líder'].to_dict()

# Identificação dos mecânicos
top_cliente = mecanicos_df['Cliente'].idxmax()
qtd_cliente = mecanicos_df.loc[top_cliente, 'Cliente']

top_interna = mecanicos_df['Interna'].idxmax()
qtd_interna = mecanicos_df.loc[top_interna, 'Interna']

top_geral = mecanicos_df['Total'].idxmax()
qtd_geral = mecanicos_df.loc[top_geral, 'Total']

menos_geral = mecanicos_df['Total'].idxmin()
qtd_menos_geral = mecanicos_df.loc[menos_geral, 'Total']

# Filtrar perdas positivas
perda_positiva = mecanicos_df[mecanicos_df['Perdidas'] > 0]
top_Perdidas = perda_positiva['Perdidas'].idxmax()
qtd_perdida = perda_positiva.loc[top_Perdidas, 'Perdidas']

menos_Perdidas = perda_positiva['Perdidas'].idxmin()
qtd_menos_Perdidas = perda_positiva.loc[menos_Perdidas, 'Perdidas']

# Identificação dos mecânicos adicionais
menos_cliente = mecanicos_df['Cliente'].idxmin()
qtd_menos_cliente = mecanicos_df.loc[menos_cliente, 'Cliente']

menos_interna = mecanicos_df['Interna'].idxmin()
qtd_menos_interna = mecanicos_df.loc[menos_interna, 'Interna']

menos_perda_geral = mecanicos_df['Perdidas'].idxmin()
qtd_menos_perda_geral = mecanicos_df.loc[menos_perda_geral, 'Perdidas']

st.markdown("### 👑 Top 5 - Mais Moto Cliente")
top5_cliente = mecanicos_df['Cliente'].sort_values(ascending=False).head(5)
for mec, qtd in top5_cliente.items():
    st.write(f"- {mec}: {qtd} motos (Líder: `{mec_lider_dict.get(mec, 'N/A')}`)")

# 📉 Exibição dos Bottom 5 - Cliente
st.markdown("### 👶 Top 5 - Menos Moto Cliente")
bottom5_cliente = mecanicos_df['Cliente'].sort_values(ascending=True).head(5)
for mec, qtd in bottom5_cliente.items():
    st.write(f"- {mec}: {qtd} motos (Líder: `{mec_lider_dict.get(mec, 'N/A')}`)")

# 🔧 Exibição dos Top 5 - Interna
st.markdown("### 🔧 Top 5 - Mais Interna")
top5_interna = mecanicos_df['Interna'].sort_values(ascending=False).head(5)
for mec, qtd in top5_interna.items():
    st.write(f"- {mec}: {qtd} internas (Líder: `{mec_lider_dict.get(mec, 'N/A')}`)")

# 🔧 Exibição dos Bottom 5 - Interna
st.markdown("### 🔧 Top 5 - Menos Interna")
bottom5_interna = mecanicos_df['Interna'].sort_values(ascending=True).head(5)
for mec, qtd in bottom5_interna.items():
    st.write(f"- {mec}: {qtd} internas (Líder: `{mec_lider_dict.get(mec, 'N/A')}`)")

# 🏆 Exibição dos Top 5 - Geral
st.markdown("### 🏆 Top 5 - Mais Geral (Cliente + Interna)")
top5_geral = mecanicos_df['Total'].sort_values(ascending=False).head(5)
for mec, qtd in top5_geral.items():
    st.write(f"- {mec}: {qtd} total (Líder: `{mec_lider_dict.get(mec, 'N/A')}`)")

# 🫥 Exibição dos Bottom 5 - Geral
st.markdown("### 🫥 Top 5 - Menos Geral (Cliente + Interna)")
bottom5_geral = mecanicos_df['Total'].sort_values(ascending=True).head(5)
for mec, qtd in bottom5_geral.items():
    st.write(f"- {mec}: {qtd} total (Líder: `{mec_lider_dict.get(mec, 'N/A')}`)")

# ❌ Exibição dos Top 5 - Perdas
st.markdown("### ❌ Top 5 - Mais Perdas")
top5_perdas = mecanicos_df[mecanicos_df['Perdidas'] > 0]['Perdidas'].sort_values(ascending=False).head(5)
for mec, qtd in top5_perdas.items():
    st.write(f"- {mec}: {qtd} perdas (Líder: `{mec_lider_dict.get(mec, 'N/A')}`)")

# ✅ Exibição dos Bottom 5 - Menos Perdas (maiores que zero)
st.markdown("### ✅ Top 5 - Menos Perdas (acima de 0)")
bottom5_perdas = mecanicos_df[mecanicos_df['Perdidas'] > 0]['Perdidas'].sort_values(ascending=True).head(5)
for mec, qtd in bottom5_perdas.items():
    st.write(f"- {mec}: {qtd} perdas (Líder: `{mec_lider_dict.get(mec, 'N/A')}`)")