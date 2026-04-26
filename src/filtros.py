def aplicar_filtros(
        base,
        internacoes,
        poluentes,
        anos_selecionados,
        municipios_selecionados=None
):
    """
    Aplica os filtros principais do dashboard.

    Regras:
    - Ano filtra base, internações e poluentes.
    - Município filtra apenas internações, pois a tabela de poluentes não possui coluna de município.
    """

    base_filtrada = base.copy()
    internacoes_filtrada = internacoes.copy()
    poluentes_fltrada = poluentes.copy()

    if anos_selecionados:
        base_filtrada = base_filtrada[base_filtrada["ano"].isin(anos_selecionados)]
        internacoes_filtrada = internacoes_filtrada[internacoes_filtrada["ano"].isin(anos_selecionados)]
        poluentes_fltrada = poluentes_fltrada[poluentes_fltrada["ano"].isin(anos_selecionados)]

    if municipios_selecionados:
        internacoes_filtrada = internacoes_filtrada[internacoes_filtrada["municipio"].isin(municipios_selecionados)]
    
    return base_filtrada, internacoes_filtrada, poluentes_fltrada

