#calcular total de internações - internacoes_filtradas(municipio), base_filtrada(total de internacoes)
import pandas as pd

def calcular_total_internacoes(internacoes_filtrada):
    """
    Calcula o total de internações considerando os filtros aplicados pelo usuário.
    """

    if internacoes_filtrada.empty:
        return 0

    return int(internacoes_filtrada["internacoes"].sum())

#calcular média de PM2,5
def calcular_media_poluente(poluentes_filtrada, poluente):
    """
    Calcula a média de um poluente selecionado.
    Exemplo de poluente: PM25, PM10, NO2, CO, O3.
    """

    if poluentes_filtrada.empty:
        return None

    if poluente not in poluentes_filtrada.columns:
        return None

    media = poluentes_filtrada[poluente].mean()

    if pd.isna(media):
        return None

    return round(media, 2)
    
#base mensal para análise
def montar_base_analise(internacoes_filtrada, poluentes_filtrada):
    """
     Base mensal que une internações e poluentes.

    A internação pode estar filtrada por município.
    Os poluentes são mensais e gerais, sem município.
    """

    internacoes_mensal = (
        internacoes_filtrada
        .groupby(["periodo", "ano", "mes"], as_index=False)["internacoes"]
        .sum()
        .rename(columns={"internacoes": "internacoes_total"})
    )

    base_analise = internacoes_mensal.merge(
        poluentes_filtrada,
        on=["periodo", "ano", "mes"],
        how="inner"
    )
    return base_analise

#calcular correlação
def calcular_correlacao(base_analise, poluente):
    """
    Calcula a correlação entre o poluente selecionado e as internações.
    """

    if base_analise.empty:
        return None

    if poluente not in base_analise.columns:
        return None

    if "internacoes_total" not in base_analise.columns:
        return None

    # Correlação precisa de pelo menos 2 registros
    if len(base_analise) < 2:
        return None

    # Se uma das colunas não varia, a correlação não é calculável
    if base_analise[poluente].nunique() <= 1:
        return None

    if base_analise["internacoes_total"].nunique() <= 1:
        return None

    correlacao = base_analise[poluente].corr(
        base_analise["internacoes_total"]
    )

    if pd.isna(correlacao):
        return None

    return round(correlacao, 2)

#gerar ranking de municípios
def gerar_ranking_municipios(internacoes_filtrada):
    """
    Gera ranking de municípios por total de internações.
    """

    if internacoes_filtrada.empty:
        return pd.DataFrame(columns=["municipio", "internacoes_total"])

    ranking = (
        internacoes_filtrada
        .groupby("municipio", as_index=False)["internacoes"]
        .sum()
        .rename(columns={"internacoes": "internacoes_total"})
        .sort_values("internacoes_total", ascending=False)
    )

    return ranking

#gerar internacoes por mês
def gerar_internacoes_por_mes(internacoes_filtrada):
    """
    Gera a série mensal de internações.
    Essa base será usada no gráfico de internações por mês.
    """

    if internacoes_filtrada.empty:
        return pd.DataFrame(columns=["periodo", "ano", "mes", "internacoes_total"])

    internacoes_por_mes = (
        internacoes_filtrada
        .groupby(["periodo", "ano", "mes"], as_index=False)["internacoes"]
        .sum()
        .rename(columns={"internacoes": "internacoes_total"})
        .sort_values("periodo")
    )

    return internacoes_por_mes
#gerar
def gerar_poluentes_por_mes(poluentes_filtrada):
    """
    Gera a série mensal de poluentes.
    Essa base será usada no gráfico de poluentes por mês.
    """

    if poluentes_filtrada.empty:
        return pd.DataFrame()

    colunas_poluentes = ["PM25", "PM10", "NO2", "SO2", "CO", "O3"]

    colunas_existentes = [
        coluna for coluna in colunas_poluentes
        if coluna in poluentes_filtrada.columns
    ]

    poluentes_por_mes = (
        poluentes_filtrada
        .groupby(["periodo", "ano", "mes"], as_index=False)[colunas_existentes]
        .mean()
        .sort_values("periodo")
    )

    return poluentes_por_mes

#variaveis a serem utilizadas:
#base_filtrada
#internacoes_filtrada
#poluentes_filtrada