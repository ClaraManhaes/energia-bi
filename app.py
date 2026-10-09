import pandas as pd
import streamlit as st

# Configuração inicial da página
st.set_page_config(
    page_title="Mercado Livre de Energia | Análise Econômica",
    page_icon="⚡",
    layout="wide",
)

# Título e Introdução
st.title("⚡ Análise Comparativa: Mercado Captivo vs. Mercado Livre de Energia")
st.markdown(
    "Painel de inteligência de custos e opções econômicas para migração e gestão de portfólio no ACL."
)

# ----------------------------------------------------------------------------
# Passo 1: Barra Lateral para Parâmetros de Simulação
# ------------------------------------------------------------
st.sidebar.header("📊 Parâmetros de Simulação")

consumo_medio_mwh = st.sidebar.slider(
    "Consumo Médio Mensal (MWh)", min_value=50, max_value=5000, value=500, step=50
)
perfil_carga = st.sidebar.selectbox(
    "Perfil de Carga", ["Horus (Industrial / Contínuo)", "Comercial / Ponta"]
)

# Indicadores de Viabilidade
st.subheader("Indicadores de Viabilidade")

col1, col2, col3 = st.columns(3)
col1.metric(
    "Custo Atual (Captivo)",
    f"R$ {consumo_medio_mwh * 450:,.2f}".replace(",", "."),
    delta="Tarifa Regulada",
    delta_color="inverse",
)
col2.metric(
    "Custo Estimado (ACL)",
    f"R$ {consumo_medio_mwh * 320:,.2f}".replace(",", "."),
    delta="-28.8% de economia",
)
col3.metric(
    "Economia Anual Projetada",
    f"R$ {(consumo_medio_mwh * 130) * 12:,.2f}".replace(",", "."),
    delta="Potencial Elevado",
)

st.divider()

# ----------------------------------------------------------------------------
# Passo 2: Adicionando Gráficos Comparativos
# ------------------------------------------------------------
st.subheader("📈 Projeção Anual de Custos: Captivo vs. Mercado Livre")

# Dados simulados para os próximos meses
meses = [
    "Jan",
    "Fev",
    "Mar",
    "Abr",
    "Mai",
    "Jun",
    "Jul",
    "Ago",
    "Set",
    "Out",
    "Nov",
    "Dez",
]
custo_captivo_mensal = [consumo_medio_mwh * 450] * 12
custo_acl_mensal = [consumo_medio_mwh * 320] * 12

df_grafico = pd.DataFrame(
    {
        "Mês": meses * 2,
        "Custo (R$)": custo_captivo_mensal + custo_acl_mensal,
        "Mercado": ["Mercado Captivo"] * 12 + ["Mercado Livre (ACL)"] * 12,
    }
)

st.line_chart(df_grafico, x="Mês", y="Custo (R$)", color="Mercado")
