import pandas as pd
import matplotlib.pyplot as plt
import streamlit as st

# Configurações iniciais do Streamlit
st.set_page_config(page_title="Pareto de Motos Perdidas", layout="wide")
st.title("📊 Pareto de Motos Perdidas - Geral e por Líder")



# Criando o DataFrame
pareto = pd.read_excel('ProdMecânico.xlsx',sheet_name='Pareto')

# Função para plotar Pareto
def plot_pareto(pareto_filtrado, titulo):
    st.subheader(titulo)

    # Agrupar
    pareto_grouped = pareto_filtrado.groupby("Motivo Perdidas")["Quantidade"].sum().sort_values(ascending=False)
    
    # Calcular % acumulada
    pareto_percentual = (pareto_grouped.cumsum() / pareto_grouped.sum()) * 100

    fig, ax1 = plt.subplots(figsize=(20, 8))  # Aumentando o tamanho do gráfico

    # Barras
    bars = ax1.bar(pareto_grouped.index, pareto_grouped.values, color="skyblue")
    ax1.set_ylabel("Quantidade", fontsize=12)  # Aumentando o tamanho da fonte
    ax1.set_xlabel("Motivo", fontsize=12)      # Aumentando o tamanho da fonte
    ax1.set_title(titulo, fontsize=14)         # Aumentando o tamanho da fonte

    # Rótulos nas barras
    for bar in bars:
        height = bar.get_height()
        ax1.annotate(f'{int(height)}',
                     xy=(bar.get_x() + bar.get_width() / 2, height),
                     xytext=(0, 3),  # Distância acima da barra
                     textcoords="offset points",
                     ha='center', va='bottom', fontsize=12, color="black")  # Fonte maior

    # Linha de % acumulada
    ax2 = ax1.twinx()
    ax2.plot(pareto_grouped.index, pareto_percentual.values, color="red", marker="o")
    ax2.set_ylabel("% Acumulado", fontsize=12)  # Aumentando o tamanho da fonte

    # Rótulos nos pontos de percentual
    for i, perc in enumerate(pareto_percentual):
        ax2.annotate(f'{perc:.1f}%',
                     xy=(i, perc),
                     xytext=(0, 5),
                     textcoords="offset points",
                     ha='center', va='bottom', fontsize=12, color="red")  # Fonte maior

    # Linha verde 80%
    ax2.axhline(80, color="green", linestyle="dashed")

    plt.xticks(rotation=45, ha="right", fontsize=12)  # Aumentando a fonte dos rótulos no eixo X
    plt.tight_layout()
    st.pyplot(fig)

# --- Pareto Geral ---
plot_pareto(pareto, "Pareto Geral")

# --- Pareto por Líder ---
lideres = pareto['Líder'].unique()

st.header("Pareto por Líder")

for lider in lideres:
    pareto_lider = pareto[pareto['Líder'] == lider]
    plot_pareto(pareto_lider, f"Pareto - {lider}")
