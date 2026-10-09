import pandas as pd
import streamlit as st

# Configuração inicial da página (Layout limpo e profissional)
st.set_page_config(
    page_title="Mercado Livre de Energia | Análise Econômica",
    page_icon="⚡",
    layout="wide",
)

# Título e Introdução
st.title("⚡ Análise Comparativa: Mercado Captivo vs. Mercado Livre de Energia")
st.markdown(
    "Painel de inteligência de custos e viabilidade econômica para migração e gestão de portfólio no ACL."
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

# Simulando dados básicos de economia
st.subheader("Indicadores de Viabilidade")

# Métricas principais lado a lado
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

# Espaço reservado para os próximos gráficos comparativos
st.info(
    "💡 Dica: Este é o nosso ponto de partida. Na próxima etapa, vamos adicionar os gráficos de comparação de preços e simulação de PLD!"
)