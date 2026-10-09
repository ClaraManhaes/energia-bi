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
st.title("Análise de Viabilidade Econômica | Mercado Livre de Energia (ACL)")
st.markdown(
    "Plataforma executiva de inteligência de custos, monitoramento de portfólio e simulação de risco de PLD (Base Lux Energia)."
)
st.write("")

# ----------------------------------------------------------------------------
# Base de Dados Simulada das 12 UCs (Extraída da Prova Técnica da Lux)
# ----------------------------------------------------------------------------
@st.cache_data
def carregar_base_ucs():
  dados_base = [
      {"UC": "UC-1001", "Cliente": "Cond. Res. Vila Nova", "Distribuidora": "Enel SP", "Modalidade": "Convencional", "Consumo_MWh": 56.0, "Preco_MWh": 285, "Status": "Ativa"},
      {"UC": "UC-1002", "Cliente": "Cond. Ed. Aurora", "Distribuidora": "Enel SP", "Modalidade": "Incentivada 50%", "Consumo_MWh": 42.28, "Preco_MWh": 315, "Status": "Ativa"},
      {"UC": "UC-1003", "Cliente": "Indústrias Reunidas SP", "Distribuidora": "Enel SP", "Modalidade": "Horofásica Verde", "Consumo_MWh": 145.5, "Preco_MWh": 270, "Status": "Ativa"},
      {"UC": "UC-1004", "Cliente": "Shopping Metropolitano", "Distribuidora": "CPFL Paulista", "Modalidade": "Horofásica Azul", "Consumo_MWh": 112.0, "Preco_MWh": 290, "Status": "Ativa"},
      {"UC": "UC-1005", "Cliente": "Metalúrgica Santa Rita", "Distribuidora": "CPFL Paulista", "Modalidade": "Incentivada 100%", "Consumo_MWh": 210.3, "Preco_MWh": 260, "Status": "Ativa"},
      {"UC": "UC-1006", "Cliente": "Centro Empresarial Sul", "Distribuidora": "CPFL Paulista", "Modalidade": "Convencional", "Consumo_MWh": 78.4, "Preco_MWh": 305, "Status": "Ativa"},
      {"UC": "UC-1007", "Cliente": "Cond. Res. Alphaville", "Distribuidora": "CPFL Paulista", "Modalidade": "Incentivada 50%", "Consumo_MWh": 350.1, "Preco_MWh": 312, "Status": "Ativa"},
      {"UC": "UC-1008", "Cliente": "Supermercados Paulistano", "Distribuidora": "Elektro", "Modalidade": "Convencional", "Consumo_MWh": 95.2, "Preco_MWh": 293, "Status": "Ativa"},
      {"UC": "UC-1009", "Cliente": "Têxtil Americana", "Distribuidora": "Elektro", "Modalidade": "Horofásica Verde", "Consumo_MWh": 180.6, "Preco_MWh": 275, "Status": "Ativa"},
      {"UC": "UC-1010", "Cliente": "Frigorífico Bandeirante", "Distribuidora": "Light", "Modalidade": "Horofásica Azul", "Consumo_MWh": 195.8, "Preco_MWh": 306, "Status": "Ativa"},
      {"UC": "UC-1011", "Cliente": "Parque Morumbi", "Distribuidora": "Light", "Modalidade": "Convencional", "Consumo_MWh": 88.0, "Preco_MWh": 320, "Status": "Em migração"},
      {"UC": "UC-1012", "Cliente": "Ipiranga Logística", "Distribuidora": "Light", "Modalidade": "Incentivada 50%", "Consumo_MWh": 110.5, "Preco_MWh": 298, "Status": "Em migração"},
  ]
  return pd.DataFrame(dados_base)

df_ucs = carregar_base_ucs()

# ----------------------------------------------------------------------------
# Controles na Barra Lateral
# ----------------------------------------------------------------------------
st.sidebar.markdown("### Parâmetros de Gestão")
st.sidebar.markdown("---")

filtro_distribuidora = st.sidebar.selectbox(
    "Filtrar por Concessionária",
    ["Todas"] + list(df_ucs["Distribuidora"].unique())
)

filtro_status = st.sidebar.selectbox(
    "Status da Unidade",
    ["Todas", "Ativa", "Em migração"]
)

# Aplicando filtros na base de UCs
df_filtrado = df_ucs.copy()
if filtro_distribuidora != "Todas":
  df_filtrado = df_filtrado[df_filtrado["Distribuidora"] == filtro_distribuidora]
if filtro_status != "Todas":
  df_filtrado = df_filtrado[df_filtrado["Status"] == filtro_status]

# ----------------------------------------------------------------------------
# Estrutura em Abas (Tabs) para Apresentação Profissional
# ----------------------------------------------------------------------------
aba1, aba2, aba3, aba4 = st.tabs([
    "Visão Geral & UCs", 
    "Simulação de PLD e Risco", 
    "Monitoramento Diário e YoY", 
    "Documentação (README)"
])

# ----------------------------------------------------------------------------
# ABA 1: Visão Geral e Gestão de Unidades Consumidoras (UCs)
# ----------------------------------------------------------------------------
with aba1:
  st.subheader("Gestão de Unidades Consumidoras da Carteira")
  st.markdown("Acompanhamento individualizado das UCs, status de migração e faturamento regulado vs. Mercado Livre.")

  consumo_total_f = df_filtrado["Consumo_MWh"].sum()
  faturamento_regulado_f = (df_filtrado["Consumo_MWh"] * df_filtrado["Preco_MWh"]).sum()
  tarifa_acl_media = 220.0 # R$/MWh referência ACL
  faturamento_acl_f = consumo_total_f * tarifa_acl_media
  economia_f = faturamento_regulado_f - faturamento_acl_f
  perc_eco_f = (economia_f / faturamento_regulado_f * 100) if faturamento_regulado_f > 0 else 0

  col1, col2, col3, col4 = st.columns(4)
  with col1:
    st.metric("Consumo Total Filtrado", f"{consumo_total_f:,.2f} MWh".replace(",", "X").replace(".", ",").replace("X", "."))
  with col2:
    st.metric("Custo Regulado Atual", f"R$ {faturamento_regulado_f:,.2f}".replace(",", "X").replace(".", ",").replace("X", "."))
  with col3:
    st.metric("Custo Estimado (ACL)", f"R$ {faturamento_acl_f:,.2f}".replace(",", "X").replace(".", ",").replace("X", "."))
  with col4:
    st.metric("Economia Potencial", f"R$ {economia_f:,.2f} ({perc_eco_f:.1f}%)".replace(",", "X").replace(".", ",").replace("X", "."))

  st.markdown("---")
  st.subheader("Detalhamento por Unidade Consumidora (UC)")
  st.dataframe(df_filtrado, use_container_width=True, hide_index=True)

  st.markdown("---")
  st.subheader("Consumo Consolidado por Concessionária")
  
  df_resumo_dist = df_ucs.groupby("Distribuidora")["Consumo_MWh"].sum().reset_index()
  fig_bar = px.bar(
      df_resumo_dist, x="Distribuidora", y="Consumo_MWh", text="Consumo_MWh",
      color="Distribuidora", color_discrete_sequence=["#2563EB", "#3B82F6", "#60A5FA", "#93C5FD"]
  )
  fig_bar.update_layout(
      plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)",
      margin=dict(t=20, b=20, l=20, r=20), xaxis=dict(title="", showgrid=False),
      yaxis=dict(title="Consumo Total (MWh)", showgrid=True, gridcolor="#E5E7EB"),
      showlegend=False, height=380
  )
  st.plotly_chart(fig_bar, use_container_width=True)

# ----------------------------------------------------------------------------
# ABA 2: Simulação de PLD e Risco de Mercado (Avançado)
# ----------------------------------------------------------------------------
with aba2:
  st.subheader("Análise de Sensibilidade e Volatilidade do PLD")
  st.markdown("Avaliação de risco de exposição ao Preço de Liquidação das Diferenças (PLD) para contratos no Mercado Livre.")

  col_pld1, col_pld2 = st.columns(2)
  with col_pld1:
    pld_medio = st.slider("PLD Médio Simulado (R$/MWh)", min_value=80.0, max_value=600.0, value=150.0, step=10.0)
  with col_pld2:
    exposicao_spot = st.slider("Percentual de Exposição ao Mercado Spot (%)", min_value=0, max_value=100, value=25, step=5)

  # Simulando impacto financeiro base
  consumo_carteira = df_ucs["Consumo_MWh"].sum()
  custo_fixo_contrato = consumo_carteira * (1 - exposicao_spot/100) * 210.0
  custo_spot = consumo_carteira * (exposicao_spot/100) * pld_medio
  custo_total_pld = custo_fixo_contrato + custo_spot

  st.info(f"💡 **Resultado da Simulação de Risco:** Para um PLD de R$ {pld_medio:.2f}/MWh com {exposicao_spot}% de exposição spot, o custo total estimado da carteira é de **R$ {custo_total_pld:,.2f}**.")

  # Gráfico de sensibilidade do PLD
  valores_pld = list(range(80, 550, 30))
  custos_simulados = [consumo_carteira * ((1 - exposicao_spot/100)*210 + (exposicao_spot/100)*p) for p in valores_pld]
  df_sens = pd.DataFrame({"PLD (R$/MWh)": valores_pld, "Custo Total da Carteira (R$)": custos_simulados})

  fig_sens = px.line(df_sens, x="PLD (R$/MWh)", y="Custo Total da Carteira (R$)", markers=True)
  fig_sens.update_layout(
      plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)",
      margin=dict(t=20, b=20, l=20, r=20),
      xaxis=dict(showgrid=True, gridcolor="#E5E7EB"),
      yaxis=dict(showgrid=True, gridcolor="#E5E7EB"),
      height=380
  )
  st.plotly_chart(fig_sens, use_container_width=True)

# ----------------------------------------------------------------------------
# ABA 3: Monitoramento Diário e YoY (09/10/2026 vs 09/10/2025)
# ----------------------------------------------------------------------------
with aba3:
  st.subheader("Monitoramento Diário e Comparativo Year-over-Year (YoY)")
  st.markdown("Comparativo do desempenho operacional atual (09/10/2026) frente ao mesmo dia de 2025 (09/10/2025).")

  hoje_2026 = pd.to_datetime("2026-10-09")
  hoje_2025 = pd.to_datetime("2025-10-09")
  datas = pd.date_range(end=hoje_2026, periods=30, freq="D")

  np.random.seed(42)
  custo_2026 = [45000 + np.random.uniform(-3000, 4000) for _ in range(30)]
  custo_2025 = [42000 + np.random.uniform(-2500, 3500) for _ in range(30)]

  df_yoy = pd.DataFrame({
      "Data": datas,
      "Custo Diário 2026 (R$)": custo_2026,
      "Custo Diário 2025 (R$)": custo_2025
  })

  fig_yoy = px.line(df_yoy, x="Data", y=["Custo Diário 2026 (R$)", "Custo Diário 2025 (R$)"],
                    color_discrete_map={"Custo Diário 2026 (R$)": "#2563EB", "Custo Diário 2025 (R$)": "#9CA3AF"})
  fig_yoy.update_layout(
      plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)",
      margin=dict(t=20, b=20, l=20, r=20),
      xaxis=dict(title="", showgrid=False), yaxis=dict(title="Custo (R$)", showgrid=True, gridcolor="#E5E7EB"),
      legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
      height=380
  )
  st.plotly_chart(fig_yoy, use_container_width=True)

# ----------------------------------------------------------------------------
# ABA 4: Documentação Técnica (README para o GitHub)
# ----------------------------------------------------------------------------
with aba4:
  st.subheader("Documentação Técnica do Projeto (README)")
  st.markdown("""
  Este painel foi desenvolvido para atender aos padrões técnicos de gestão de portfólio e análise de viabilidade no **Mercado Livre de Energia (ACL)**.

  ### 🚀 Funcionalidades Principais:
  1. **Gestão por Unidade Consumidora (UC):** Filtragem dinâmica por distribuidora (*Enel SP, CPFL Paulista, Elektro e Light*) e status operacional (*Ativa / Em migração*).
  2. **Simulação de Risco de PLD:** Módulo interativo para cálculo de exposição ao mercado spot e volatilidade de preços.
  3. **Monitoramento YoY (Year-over-Year):** Análise comparativa rigorosa entre o desempenho de 2026 e 2025 na mesma data base.
  4. **Arquitetura Executiva:** Desenvolvido em Python com Streamlit e Plotly, priorizando a limpeza visual e a tomada de decisão orientada a dados.

  ### 🛠️ Tecnologias Utilizadas:
  * **Python** (Manipulação e estruturação de dados com Pandas e NumPy)
  * **Streamlit** (Interface web interativa de alta performance)
  * **Plotly** (Gráficos corporativos responsivos e de alto padrão)
  """)
