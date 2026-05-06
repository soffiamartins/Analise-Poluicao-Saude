

#gráfico de dispersão: usar a métrica poluente x internações;
#gráfico de barras horizontais: usar a métrica ranking de municípios.

import plotly.express as px

#gráfico de linha: usar a métrica internações por mês;
def grafico_internacoes_por_mes(internacoes_por_mes):
    """
    Cria gráfico de linha com o total de internações por mês.
    """

    fig = px.line(
        internacoes_por_mes,
        x="periodo",
        y="internacoes_total",
        markers=True,
        title="Internações por mês"
    )

    fig.update_layout(
        xaxis_title="Período",
        yaxis_title="Total de internações",
        title_x=0.0
    )

    return fig

#gráfico de linhas múltiplas: usar a métrica poluentes por mês;
def grafico_poluentes_por_mes(poluentes_por_mes):
    """
    Cria gráfico de linhas múltiplas com os poluentes por mês.
    """

    colunas_poluentes = ["PM25", "PM10", "NO2", "SO2", "CO", "O3"]

    colunas_existentes = [
        coluna for coluna in colunas_poluentes
        if coluna in poluentes_por_mes.columns
    ]

    dados_grafico = poluentes_por_mes.melt(
        id_vars=["periodo", "ano", "mes"],
        value_vars=colunas_existentes,
        var_name="poluente",
        value_name="media"
    )

    fig = px.line(
        dados_grafico,
        x="periodo",
        y="media",
        color="poluente",
        markers=True,
        title="Poluentes por mês"
    )

    fig.update_layout(
        xaxis_title="Período",
        yaxis_title="Média do poluente",
        legend_title="Poluente",
        title_x=0.0
    )

    return fig
