import streamlit as st

# Configuração da página (DEVE SER SEMPRE A PRIMEIRA LINHA EXECUTÁVEL)
st.set_page_config(
    page_title="Lux | Análise de Viabilidade - Mercado Livre de Energia",
    layout="wide",
)

from datetime import datetime, timedelta
import numpy as np
import pandas as pd
import plotly.express as px

# Estilização limpa e corporativa via CSS
st.markdown(
    """
    <style>
        .block-container { padding-top: 2rem; }
        h1 { font-weight: 600; color: #111827; font-size: 2rem !important; }
        h3 { font-weight: 500; color: #374151; font-size: 1.25rem !important; }
    </style>
""",
    unsafe_allow_html=True,
)

# Cabeçalho Institucional
st.title("Análise de Viabilidade Econômica | Mercado Livre de Energia")
st.markdown(
    "Painel de monitoramento de portfólio corporativo com dados consolidados das concessionárias (Enel SP, CPFL Paulista, Elektro e Light)."
)
st.write("")

# ----------------------------------------------------------------------------
# Controles de Simulação e Seleção de Concessionária (Base Lux)
# ----------------------------------------------------------------------------
st.sidebar.markdown("### Parâmetros da Carteira Lux")
st.sidebar.markdown("---")

concessionaria = st.sidebar.selectbox(
    "Selecione a Distribuidora",
    ["Enel SP", "CPFL Paulista", "Light", "Elektro"],
)

# Dados reais consolidados da base da Lux por distribuidora
dados_distribuidoras = {
    "Enel SP": {"consumo_mwh": 1257.01, "faturamento_r": 366248.16, "tarifa_media": 291.36},
    "CPFL Paulista": {"consumo_mwh": 851.87, "faturamento_r": 261939.18, "tarifa_media": 307.48},
    "Light": {"consumo_mwh": 378.57, "faturamento_r": 116043.39, "tarifa_media": 306.53},
    "Elektro": {"consumo_mwh": 356.35, "faturamento_r": 104592.28, "tarifa_media": 293.51},
}

info_atual = dados_distribuidoras[concessionaria]
tarifa_acl_mwh = 220.0  # Média de referência do ACL no mercado livre

fator_escala = st.sidebar.slider(
    "Fator de Ajuste de Carga",
    min_value=0.5,
    max_value=2.0,
    value=1.0,
    step=0.1,
)

# ----------------------------------------------------------------------------
# Estrutura em Abas (Tabs) para Apresentação Profissional
# ----------------------------------------------------------------------------
aba1, aba2, aba3 = st.tabs(
    ["Resumo por Concessionária", "Monitoramento Diário e YoY", "Base Consolidada"]
)

# ----------------------------------------------------------------------------
# ABA 1: Resumo e Comparativo por Distribuidora (Lógica da Planilha Lux)
# ----------------------------------------------------------------------------
with aba1:
  st.subheader(f"Indicadores de Desempenho — {concessionaria}")
  st.markdown(
      "Visão agregada de consumo total, faturamento regulado e potencial de economia no Mercado Livre."
  )

  consumo_ajustado = info_atual["consumo_mwh"] * fator_escala
  faturamento_regulado = info_atual["faturamento_r"] * fator_escala
  faturamento_acl = consumo_ajustado * tarifa_acl_mwh
  economia_potencial = faturamento_regulado - faturamento_acl
  perc_economia = (economia_potencial / faturamento_regulado) * 100

  col1, col2, col3, col4 = st.columns(4)

  with col1:
    st.metric(
        label="Consumo Total",
        value=f"{consumo_ajustado:,.2f} MWh".replace(",", "X").replace(".", ",").replace("X", "."),
    )
  with col2:
    st.metric(
        label="Faturamento Regulado",
        value=f"R$ {faturamento_regulado:,.2f}".replace(",", "X").replace(".", ",").replace("X", "."),
    )
  with col3:
    st.metric(
        label="Custo Estimado (ACL)",
        value=f"R$ {faturamento_acl:,.2f}".replace(",", "X").replace(".", ",").replace("X", "."),
    )
  with col4:
    st.metric(
        label="Economia Projetada",
        value=f"R$ {economia_potencial:,.2f} ({perc_economia:.1f}%))".replace(",", "X").replace(".", ",").replace("X", "."),
    )

  st.markdown("---")
  st.subheader("Comparativo Geral entre Distribuidoras da Carteira Lux")

  # DataFrame para gráfico comparativo entre todas as distribuidoras da base
  df_comparativo = pd.DataFrame([
      {"Distribuidora": "Enel SP", "Consumo (MWh)": 1257.01, "Faturamento (R$)": 366248.16},
      {"Distribuidora": "CPFL Paulista", "Consumo (MWh)": 851.87, "Faturamento (R$)": 261939.18},
      {"Distribuidora": "Light", "Consumo (MWh)": 378.57, "Faturamento (R$)": 116043.39},
      {"Distribuidora": "Elektro", "Consumo (MWh)": 356.35, "Faturamento (R$)": 104592.28},
  ])

  fig_bar = px.bar(
      df_comparativo,
      x="Distribuidora",
      y="Consumo (MWh)",
      text="Consumo (MWh)",
      color="Distribuidora",
      color_discrete_sequence=["#2563EB", "#3B82F6", "#60A5FA", "#93C5FD"],
  )

  fig_bar.update_layout(
      plot_bgcolor="rgba(0,0,0,0)",
      paper_bgcolor="rgba(0,0,0,0)",
      margin=dict(t=20, b=20, l=20, r=20),
      xaxis=dict(title="", showgrid=False),
      yaxis=dict(title="Consumo Total (MWh)", showgrid=True, gridcolor="#E5E7EB"),
      showlegend=False,
      height=400,
  )

  st.plotly_chart(fig_bar, use_container_width=True)

# ----------------------------------------------------------------------------
# ABA 2: Monitoramento Diário e YoY (09/10/2026 vs 09/10/2025)
# ----------------------------------------------------------------------------
with aba2:
  st.subheader("Evolução Temporal e Comparativo Anual (YoY)")
  st.markdown(
      "Análise diária simulada comparando o desempenho atual de outubro de 2026 com o mesmo período de 2025."
  )

  hoje_2026 = pd.to_datetime("2026-10-09")
  hoje_2025 = pd.to_datetime("2025-10-09")
  datas_2026 = pd.date_range(end=hoje_2026, periods=30, freq="D")

  np.random.seed(42)
  custo_regulado_serie = [info_atual["tarifa_media"] * np.random.uniform(15, 25) * fator_escala for _ in range(30)]
  custo_acl_serie = [tarifa_acl_mwh * np.random.uniform(15, 25) * fator_escala for _ in range(30)]

  df_diario = pd.DataFrame({
      "Data": datas_2026,
      "Regulado": custo_regulado_serie,
      "Mercado Livre (ACL)": custo_acl_serie,
  })

  fig_diario = px.line(
      df_diario,
      x="Data",
      y=["Regulado", "Mercado Livre (ACL)"],
      labels={"value": "Custo Diário (R$)", "variable": "Modelo"},
      color_discrete_map={"Regulado": "#6B7280", "Mercado Livre (ACL)": "#2563EB"},
  )

  fig_diario.update_layout(
      plot_bgcolor="rgba(0,0,0,0)",
      paper_bgcolor="rgba(0,0,0,0)",
      margin=dict(t=20, b=20, l=20, r=20),
      xaxis=dict(title="", showgrid=False),
      yaxis=dict(title="Custo Diário (R$)", showgrid=True, gridcolor="#E5E7EB"),
      legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
      height=400,
  )

  st.plotly_chart(fig_diario, use_container_width=True)

# ----------------------------------------------------------------------------
# ABA 3: Base Consolidada (Resumo da Planilha Lux)
# ----------------------------------------------------------------------------
with aba3:
  st.subheader("Base Consolidada de Concessionárias da Lux")
  st.markdown("Dados oficiais extraídos do resumo analítico da carteira de energia.")

  st.dataframe(df_comparativo, use_container_width=True, hide_index=True)
