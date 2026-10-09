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
    "Painel de monitoramento diário, comparativo YoY (2025 vs 2026) e otimização"
    " de portfólio corporativo."
)
st.write("")

# ----------------------------------------------------------------------------
# Geração Automática de Base de Dados Diária (Histórico e Atual)
# ----------------------------------------------------------------------------


@st.cache_data
def gerar_dados_diarios():
  hoje_2026 = pd.to_datetime("2026-10-09")
  hoje_2025 = pd.to_datetime("2025-10-09")

  datas_2026 = pd.date_range(end=hoje_2026, periods=60, freq="D")
  datas_2025 = pd.date_range(end=hoje_2025, periods=60, freq="D")

  registros = []
  np.random.seed(42)

  for d26, d25 in zip(datas_2026, datas_2025):
    consumo_base_26 = np.random.uniform(15.0, 25.0)
    custo_captivo_26 = consumo_base_26 * 450
    custo_acl_26 = consumo_base_26 * 320

    consumo_base_25 = consumo_base_26 * np.random.uniform(0.92, 0.98)
    custo_captivo_25 = consumo_base_25 * 420
    custo_acl_25 = consumo_base_25 * 300

    registros.append({
        "Data_2026": d26,
        "Data_2025": d25,
        "Consumo_MWh_2026": round(consumo_base_26, 2),
        "Custo_Captivo_2026": round(custo_captivo_26, 2),
        "Custo_ACL_2026": round(custo_acl_26, 2),
        "Economia_Diaria_2026": round(custo_captivo_26 - custo_acl_26, 2),
        "Custo_Captivo_2025": round(custo_captivo_25, 2),
        "Custo_ACL_2025": round(custo_acl_25, 2),
    })

  return pd.DataFrame(registros)


df_diario = gerar_dados_diarios()

# ----------------------------------------------------------------------------
# Controles de Simulação (Barra Lateral)
# ----------------------------------------------------------------------------
st.sidebar.markdown("### Parâmetros de Entrada")
st.sidebar.markdown("---")

fator_escala = st.sidebar.slider(
    "Fator de Escala de Carga",
    min_value=0.5,
    max_value=3.0,
    value=1.0,
    step=0.1,
)
perfil_carga = st.sidebar.selectbox(
    "Perfil Operacional", ["Industrial Contínuo", "Comercial Horário"]
)

# ----------------------------------------------------------------------------
# Estrutura em Abas (Tabs)
# ----------------------------------------------------------------------------
aba1, aba2, aba3 = st.tabs(
    ["Monitoramento Diário e YoY", "Projeção Anual de Custos", "Base de Dados"]
)

# ----------------------------------------------------------------------------
# ABA 1: Monitoramento Diário (Hoje vs Anteontem vs Ano Passado)
# ----------------------------------------------------------------------------
with aba1:
  st.subheader("Indicadores de Desempenho Diário e Comparativo YoY")
  st.markdown(
      "Comparação direta entre o desempenho operacional de hoje (09/10/2026), o"
      " dia anterior (D-1) e o mesmo período do ano anterior (09/10/2025)."
  )

  hoje_dados = df_diario.iloc[-1]
  ontem_dados = df_diario.iloc[-2]
  ano_passado_dados = df_diario.iloc[-1]

  col1, col2, col3, col4 = st.columns(4)

  with col1:
    st.metric(
        label="Consumo Hoje (09/10/2026)",
        value=f"{hoje_dados['Consumo_MWh_2026'] * fator_escala:.1f} MWh",
        delta=f"{((hoje_dados['Consumo_MWh_2026'] - ontem_dados['Consumo_MWh_2026']) / ontem_dados['Consumo_MWh_2026']) * 100:.1f}% vs D-1",
    )

  with col2:
    st.metric(
        label="Custo ACL Hoje",
        value=f"R$ {hoje_dados['Custo_ACL_2026'] * fator_escala:,.2f}"
        .replace(",", "X")
        .replace(".", ",")
        .replace("X", "."),
        delta="Mercado Livre",
    )

  with col3:
    st.metric(
        label="Custo YoY (09/10/2025)",
        value=f"R$ {ano_passado_dados['Custo_ACL_2025'] * fator_escala:,.2f}"
        .replace(",", "X")
        .replace(".", ",")
        .replace("X", "."),
        delta="Mesmo dia em 2025",
        delta_color="off",
    )

  with col4:
    variacao_yoy = (
        (
            (hoje_dados["Custo_ACL_2026"] - ano_passado_dados["Custo_ACL_2025"])
            / ano_passado_dados["Custo_ACL_2025"]
        )
        * 100
    )
    st.metric(
        label="Variação Anual (YoY)",
        value=f"{variacao_yoy:+.1f}%",
        delta="Evolução de Custo",
        delta_color="inverse",
    )

  st.markdown("---")
  st.subheader("Evolução Diária do Custo: Captivo vs. Mercado Livre (2026)")

  fig_diario = px.line(
      df_diario,
      x="Data_2026",
      y=["Custo_Captivo_2026", "Custo_ACL_2026"],
      labels={
          "Data_2026": "Data",
          "value": "Custo Diário (R$)",
          "variable": "Modelo de Mercado",
      },
      color_discrete_map={
          "Custo_Captivo_2026": "#6B7280",
          "Custo_ACL_2026": "#2563EB",
      },
  )

  fig_diario.update_layout(
      plot_bgcolor="rgba(0,0,0,0)",
      paper_bgcolor="rgba(0,0,0,0)",
      margin=dict(t=20, b=20, l=20, r=20),
      xaxis=dict(title="", showgrid=False),
      yaxis=dict(title="Custo Diário (R$)", showgrid=True, gridcolor="#E5E7EB"),
      legend=dict(
          orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1
      ),
      height=400,
  )

  st.plotly_chart(fig_diario, use_container_width=True)

# ----------------------------------------------------------------------------
# ABA 2: Projeção Anual de Custos
# ----------------------------------------------------------------------------
with aba2:
  st.subheader("Projeção de Custos Agregados por Mês")

  meses = [
      "Janeiro",
      "Fevereiro",
      "Março",
      "Abril",
      "Maio",
      "Junho",
      "Julho",
      "Agosto",
      "Setembro",
      "Outubro",
      "Novembro",
      "Dezembro",
  ]
  consumo_base_mensal = 500 * fator_escala
  custo_captivo_mensal = [consumo_base_mensal * 450] * 12
  custo_acl_mensal = [consumo_base_mensal * 320] * 12

  df_anual = pd.DataFrame(
      {
          "Mês": meses * 2,
          "Custo (R$)": custo_captivo_mensal + custo_acl_mensal,
          "Mercado": ["Mercado Captivo"] * 12 + ["Mercado Livre (ACL)"] * 12,
      }
  )

  fig_anual = px.line(
      df_anual,
      x="Mês",
      y="Custo (R$)",
      color="Mercado",
      markers=True,
      color_discrete_map={
          "Mercado Captivo": "#6B7280",
          "Mercado Livre (ACL)": "#2563EB",
      },
  )

  fig_anual.update_layout(
      plot_bgcolor="rgba(0,0,0,0)",
      paper_bgcolor="rgba(0,0,0,0)",
      margin=dict(t=20, b=20, l=20, r=20),
      xaxis=dict(title="", showgrid=False),
      yaxis=dict(title="Custo Total (R$)", showgrid=True, gridcolor="#E5E7EB"),
      legend=dict(
          orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1
      ),
      height=400,
  )

  st.plotly_chart(fig_anual, use_container_width=True)

# ----------------------------------------------------------------------------
# ABA 3: Base de Dados Completa
# ----------------------------------------------------------------------------
with aba3:
  st.subheader("Série Temporal Diária Consolidada")
  st.markdown(
      "Registros diários gerados automaticamente para auditoria e cruzamento"
      " estatístico."
  )

  st.dataframe(
      df_diario[[
          "Data_2026",
          "Consumo_MWh_2026",
          "Custo_Captivo_2026",
          "Custo_ACL_2026",
          "Economia_Diaria_2026",
      ]],
      use_container_width=True,
      hide_index=True,
  )
