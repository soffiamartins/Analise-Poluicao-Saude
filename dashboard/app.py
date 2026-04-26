import sys
from pathlib import Path

import streamlit as st
import plotly.express as px

ROOT_DIR = Path(__file__).resolve().parents[1]
sys.path.append(str(ROOT_DIR))

from src.carregar_dados import carregar_dados
from src.filtros import aplicar_filtros
from src.metricas import calcular_total_internacoes, calcular_media_poluente, montar_base_analise,calcular_correlacao,gerar_ranking_municipios,gerar_internacoes_por_mes, gerar_poluentes_por_mes

st.set_page_config(
    page_title=" Poluição do ar e Internações - ES",
    layout="wide"
)

base, internacoes, poluentes = carregar_dados()
anos_disponiveis = sorted(base["ano"].unique())
municipios_disponiveis = (
internacoes["municipio"].dropna().astype(str).str.strip().sort_values().unique())

#DICIONARIO
mapa_poluentes = {
    "PM2,5": "PM25",
    "PM10": "PM10",
    "NO2": "NO2",
    "SO2": "SO2",
    "CO": "CO",
    "O3": "O3"
}

#SIDEBAR
anos_selecionados = st.sidebar.multiselect(
    "Ano", 
    anos_disponiveis,
    default=anos_disponiveis
)

municipios_selecionados = st.sidebar.multiselect(
    "Município",
    municipios_disponiveis,
    placeholder="Todos os municípios"
)

poluente_label = st.sidebar.selectbox(
    "Poluente para análise",
    list(mapa_poluentes.keys())
)

poluente_selecionado = mapa_poluentes[poluente_label]
base_filtrada, internacoes_filtrada, poluicoes_filtrada = aplicar_filtros(
    base, internacoes, poluentes, anos_selecionados, municipios_selecionados)

base_filtrada, internacoes_filtrada, poluentes_filtrada = aplicar_filtros(
    base=base,
    internacoes=internacoes,
    poluentes=poluentes,
    anos_selecionados=anos_selecionados,
    municipios_selecionados=municipios_selecionados
)

total_internacoes = calcular_total_internacoes(internacoes_filtrada)

media_pm25 = calcular_media_poluente(
    poluentes_filtrada=poluentes_filtrada,
    poluente="PM25"
)

base_analise = montar_base_analise(
    internacoes_filtrada=internacoes_filtrada,
    poluentes_filtrada=poluentes_filtrada
)

correlacao = calcular_correlacao(
    base_analise=base_analise,
    poluente=poluente_selecionado
)

ranking_municipios = gerar_ranking_municipios(internacoes_filtrada)

internacoes_por_mes = gerar_internacoes_por_mes(internacoes_filtrada)

poluentes_por_mes = gerar_poluentes_por_mes(poluentes_filtrada)

st.header("Poluição do Ar e Internações Hospitalares - Espírito Santo")
st.caption("Dashboard acadêmico para análise de internações respiratórias e poluentes atmosféricos.")

st.subheader("Teste das métricas")

col1, col2, col3 = st.columns(3)

with col1:
    st.metric(
        "Total de internações",
        f"{total_internacoes:,}".replace(",", ".")
    )

with col2:
    st.metric(
        "Média de PM2,5",
        media_pm25
    )

with col3:
    valor_correlacao = correlacao if correlacao is not None else "Sem dados"
    st.metric(
        f"Correlação {poluente_selecionado} x internações",
        valor_correlacao
    )

st.subheader("Base de análise")
st.dataframe(base_analise, use_container_width=True)

st.subheader("Internações por mês")
st.dataframe(internacoes_por_mes, use_container_width=True)

st.subheader("Poluentes por mês")
st.dataframe(poluentes_por_mes, use_container_width=True)

st.subheader("Ranking de municípios")
st.dataframe(ranking_municipios, use_container_width=True)



