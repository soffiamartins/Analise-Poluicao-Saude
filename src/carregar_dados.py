from pathlib import Path

import pandas as pd
import streamlit as st

ROOT_DIR = Path(__file__).resolve().parents[1]
DADOS_DIR = ROOT_DIR / "dados"

@st.cache_data
def carregar_dados():
    base = pd.read_csv( DADOS_DIR / "base_dashboard_mensal_limpa.csv", sep=";")
    internacoes = pd.read_csv( DADOS_DIR / "internacoes_municipio_mensal_limpa.csv", sep=";")
    poluentes = pd.read_csv( DADOS_DIR / "poluentes_mensal_limpa.csv", sep=";")

    base = preparar_datas(base)
    internacoes = preparar_datas(internacoes)
    poluentes = preparar_datas(poluentes)
    
    internacoes["internacoes"] = pd.to_numeric(
    internacoes["internacoes"],
    errors="coerce"
).fillna(0).astype(int)

    internacoes = converter_coluna_numerica(internacoes, "internacoes")

    colunas_poluentes = ["PM25", "PM10", "NO2", "SO2", "CO", "O3"]

    for coluna in colunas_poluentes:
        if coluna in poluentes.columns:
            poluentes = converter_coluna_numerica(poluentes, coluna)

    return base, internacoes, poluentes



    return base, internacoes, poluentes

def preparar_datas(df):
    df = df.copy() 

    df.columns = df.columns.str.strip()

    df["periodo"] = pd.to_datetime(df["periodo"])

    if "ano" not in df.columns:
        df["ano"] = df["periodo"].dt.year

    if "mes" not in df.columns:
        df["mes"] = df["periodo"].dt.month

    return df

def converter_coluna_numerica(df, coluna):
    df = df.copy()

    # Se já for número, não mexe
    if pd.api.types.is_numeric_dtype(df[coluna]):
        return df

    # Primeira tentativa: conversão direta
    conversao_direta = pd.to_numeric(df[coluna], errors="coerce")

    # Segunda tentativa: padrão brasileiro, exemplo "6,25"
    serie_tratada = (
        df[coluna]
        .astype(str)
        .str.strip()
        .str.replace(".", "", regex=False)
        .str.replace(",", ".", regex=False)
    )

    conversao_br = pd.to_numeric(serie_tratada, errors="coerce")

    # Usa a conversão que conseguiu converter mais valores
    if conversao_br.notna().sum() > conversao_direta.notna().sum():
        df[coluna] = conversao_br
    else:
        df[coluna] = conversao_direta

    return df


