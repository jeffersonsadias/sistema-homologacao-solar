"""
Fachada do Painel Gerencial.

Responsabilidades:

- carregar os dados necessários;
- aplicar isolamento por Empresa;
- delegar os cálculos ao domínio;
- enriquecer distribuições com nomes;
- devolver dados prontos para a interface.

A fachada não implementa regras gerenciais.
"""

from typing import Any

from app.dominio.painel_gerencial import (
    gerar_indicadores_painel_gerencial,
)

from app.infraestrutura.repositorio_concessionarias_json import (
    carregar_concessionarias,
)

from app.infraestrutura.repositorio_empresas_json import (
    carregar_empresas,
)

from app.infraestrutura.repositorio_homologacoes_json import (
    carregar_homologacoes,
)

from app.infraestrutura.repositorio_projetos_json import (
    carregar_projetos,
)

def _filtrar_por_empresa(
    registros: list[dict[str, Any]],
    codigo_empresa: int | None,
) -> list[dict[str, Any]]:
    """
    Filtra registros pelo código da Empresa.

    Quando codigo_empresa for None,
    devolve todos os registros.
    """

    if codigo_empresa is None:
        return list(
            registros
        )

    return [
        registro
        for registro in registros
        if registro.get("codigo_empresa")
        == codigo_empresa
    ]

def _buscar_nome_empresa(
    empresas: list[dict[str, Any]],
    codigo_empresa: int,
) -> str:
    """
    Retorna o nome amigável da Empresa.

    Caso não exista correspondência,
    utiliza uma identificação pelo código.
    """

    for empresa in empresas:
        if (
            empresa.get("codigo")
            == codigo_empresa
        ):
            return (
                empresa.get("nome")
                or empresa.get("razao_social")
                or f"Empresa {codigo_empresa}"
            )

    return f"Empresa {codigo_empresa}"

def _buscar_nome_concessionaria(
    concessionarias: list[dict[str, Any]],
    codigo_concessionaria: int,
) -> str:
    """
    Retorna o nome amigável da Concessionária.

    Caso não exista correspondência,
    utiliza uma identificação pelo código.
    """

    for concessionaria in concessionarias:
        if (
            concessionaria.get("codigo")
            == codigo_concessionaria
        ):
            return (
                concessionaria.get("nome")
                or f"Concessionária "
                f"{codigo_concessionaria}"
            )

    return (
        f"Concessionária "
        f"{codigo_concessionaria}"
    )

def _enriquecer_distribuicao(
    distribuicao: dict[int, int],
    resolver_nome,
) -> list[dict[str, Any]]:
    """
    Transforma uma distribuição por código
    em uma coleção amigável para apresentação.
    """

    resultado = []

    for codigo, quantidade in (
        distribuicao.items()
    ):
        resultado.append(
            {
                "codigo": codigo,
                "nome": resolver_nome(
                    codigo
                ),
                "quantidade": quantidade,
            }
        )

    resultado.sort(
        key=lambda item: (
            -item["quantidade"],
            item["nome"].casefold(),
        )
    )

    return resultado

def obter_painel_gerencial(
    codigo_empresa: int | None = None,
) -> dict[str, Any]:
    """
    Obtém os indicadores consolidados
    do Painel Gerencial.

    Quando codigo_empresa for informado,
    Projetos e Homologações são isolados
    para aquela Empresa.
    """

    projetos = carregar_projetos()
    homologacoes = carregar_homologacoes()
    empresas = carregar_empresas()
    concessionarias = (
        carregar_concessionarias()
    )

    projetos_filtrados = (
        _filtrar_por_empresa(
            registros=projetos,
            codigo_empresa=codigo_empresa,
        )
    )

    homologacoes_filtradas = (
        _filtrar_por_empresa(
            registros=homologacoes,
            codigo_empresa=codigo_empresa,
        )
    )

    indicadores = (
        gerar_indicadores_painel_gerencial(
            projetos=projetos_filtrados,
            homologacoes=(
                homologacoes_filtradas
            ),
        )
    )

    distribuicao = indicadores[
        "distribuicao"
    ]

    distribuicao[
        "projetos_por_empresa"
    ] = _enriquecer_distribuicao(
        distribuicao=(
            distribuicao[
                "projetos_por_empresa"
            ]
        ),
        resolver_nome=lambda codigo: (
            _buscar_nome_empresa(
                empresas,
                codigo,
            )
        ),
    )

    distribuicao[
        "projetos_por_concessionaria"
    ] = _enriquecer_distribuicao(
        distribuicao=(
            distribuicao[
                "projetos_por_concessionaria"
            ]
        ),
        resolver_nome=lambda codigo: (
            _buscar_nome_concessionaria(
                concessionarias,
                codigo,
            )
        ),
    )

    return indicadores




