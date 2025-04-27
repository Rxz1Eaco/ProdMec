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

# Quadrante I
df_q1 = df_filtrado[df_filtrado['Quadrante'] == 'Quadrante I']
df_q1_cliente = df_q1['Cliente'].sum()
df_q1_interna = df_q1['Interna'].sum()
df_q1_mec_presente = len(df_q1)
df_q1_total = df_q1_cliente + df_q1_interna
df_q1_produtividade = df_q1_total / df_q1_mec_presente if df_q1_mec_presente else 0

# Quadrante II
df_q2 = df_filtrado[df_filtrado['Quadrante'] == 'Quadrante II']
df_q2_cliente = df_q2['Cliente'].sum()
df_q2_interna = df_q2['Interna'].sum()
df_q2_mec_presente = len(df_q2)
df_q2_total = df_q2_cliente + df_q2_interna
df_q2_produtividade = df_q2_total / df_q2_mec_presente if df_q2_mec_presente else 0

# Quadrante III
df_q3 = df_filtrado[df_filtrado['Quadrante'] == 'Quadrante III']
df_q3_cliente = df_q3['Cliente'].sum()
df_q3_interna = df_q3['Interna'].sum()
df_q3_mec_presente = len(df_q3)
df_q3_total = df_q3_cliente + df_q3_interna
df_q3_produtividade = df_q3_total / df_q3_mec_presente if df_q3_mec_presente else 0

# Quadrante IV
df_q4 = df_filtrado[df_filtrado['Quadrante'] == 'Quadrante IV']
df_q4_cliente = df_q4['Cliente'].sum()
df_q4_interna = df_q4['Interna'].sum()
df_q4_mec_presente = len(df_q4)
df_q4_total = df_q4_cliente + df_q4_interna
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
col13.metric("Quadrante I    - Produtividade", f"{df_q1_produtividade:.2f}")
col14.metric("Quadrante II   - Produtividade", f"{df_q2_produtividade:.2f}")
col15.metric("Quadrante III  - Produtividade", f"{df_q3_produtividade:.2f}")
col16.metric("Quadrante IV   - Produtividade", f"{df_q4_produtividade:.2f}")

# Soma total dos percentuais
if tm_cliente != 0:
    percentual_oficina = (df_q1_cliente + df_q2_cliente + df_q3_cliente + df_q4_cliente) / tm_cliente * 100
    st.write(f'Soma Percentual - Oficina: {percentual_oficina:.2f}%')

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

# Exibição dos resultados com o nome do líder
st.markdown("### 📊 Destaques dos Mecânicos")

st.write(f"👑 Mecânico que mais fez **Moto Cliente**: `{top_cliente}` ({qtd_cliente}) - Líder: `{mec_lider_dict.get(top_cliente, 'N/A')}`")
st.write(f"👶 Mecânico que menos fez **Cliente**: `{menos_cliente}` ({qtd_menos_cliente}) - Líder: `{mec_lider_dict.get(menos_cliente, 'N/A')}`")
st.write('\n')
st.write(f"🔧 Mecânico que mais fez **Interna**: `{top_interna}` ({qtd_interna}) - Líder: `{mec_lider_dict.get(top_interna, 'N/A')}`")
st.write(f"🔧 Mecânico que menos fez **Interna**: `{menos_interna}` ({qtd_menos_interna}) - Líder: `{mec_lider_dict.get(menos_interna, 'N/A')}`")
st.write('\n')
st.write(f"🏆 Mecânico que mais fez **Geral**: `{top_geral}` ({qtd_geral}) - Líder: `{mec_lider_dict.get(top_geral, 'N/A')}`")
st.write(f"🫥 Mecânico que menos fez **Geral**: `{menos_geral}` ({qtd_menos_geral}) - Líder: `{mec_lider_dict.get(menos_geral, 'N/A')}`")
st.write('\n')
st.write(f"❌ Mecânico que mais **perdeu motos**: `{top_Perdidas}` ({qtd_perdida}) - Líder: `{mec_lider_dict.get(top_Perdidas, 'N/A')}`")
st.write(f"✅ Mecânico que menos **perdeu motos** (incluindo zero): `{menos_perda_geral}` ({qtd_menos_perda_geral}) - Líder: `{mec_lider_dict.get(menos_perda_geral, 'N/A')}`")