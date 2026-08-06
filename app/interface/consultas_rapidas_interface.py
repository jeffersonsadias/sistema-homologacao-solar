"""
Interface de terminal das Consultas Rápidas.

Este módulo é responsável por:

- solicitar os critérios das consultas;
- chamar funções públicas das fachadas;
- exibir Projetos e Homologações encontrados;
- manter o submenu de Consultas Rápidas.

Este módulo não deve:

- acessar coleções internas das fachadas;
- acessar arquivos JSON;
- alterar dados;
- implementar regras de negócio;
- persistir informações.
"""

from typing import Any

from app import homologacoes
from app import projetos
from app import status

from app.dominio.status_homologacao import (
    ROTULOS_STATUS_HOMOLOGACAO,
    StatusHomologacao,
)

from app.utils import ler_int

# ============================================================
# FUNÇÕES AUXILIARES DE EXIBIÇÃO
# ============================================================

def _exibir_titulo(
    titulo: str,
) -> None:
    """
    Exibe um título padronizado.
    """

    print()
    print("=" * 60)
    print(titulo)
    print("=" * 60)

def _pausar() -> None:
    """
    Aguarda confirmação antes de retornar
    ao menu de Consultas Rápidas.
    """

    input(
        "\nPressione Enter para continuar..."
    )

def _exibir_projetos(
    lista_projetos: list[dict[str, Any]],
) -> None:
    """
    Exibe os Projetos encontrados.

    A apresentação individual é delegada à fachada
    pública de Projetos.
    """

    if not lista_projetos:
        print(
            "\nNenhum Projeto encontrado."
        )

        return

    for projeto in lista_projetos:
        projetos.mostrar_projeto(
            projeto
        )

    print(
        "\nTotal de Projetos encontrados: "
        f"{len(lista_projetos)}"
    )

def _exibir_homologacao_resumida(
    homologacao: dict[str, Any],
) -> None:
    """
    Exibe os principais dados de uma Homologação.
    """

    print()
    print("-" * 60)

    print(
        f"Código da Homologação: "
        f"{homologacao.get('codigo', '-')}"
    )

    print(
        f"Código da Empresa: "
        f"{homologacao.get('codigo_empresa', '-')}"
    )

    print(
        f"Código do Projeto: "
        f"{homologacao.get('codigo_projeto', '-')}"
    )

    print(
        f"Código da Concessionária: "
        f"{homologacao.get('codigo_concessionaria', '-')}"
    )

    print(
        f"Status: "
        f"{homologacao.get('status', '-')}"
    )

    print(
        f"Responsável atual: "
        f"{homologacao.get('responsavel_atual', '-')}"
    )

    print("-" * 60)

def _exibir_homologacoes(
    lista_homologacoes: list[dict[str, Any]],
) -> None:
    """
    Exibe as Homologações encontradas.
    """

    if not lista_homologacoes:
        print(
            "\nNenhuma Homologação encontrada."
        )

        return

    for homologacao in lista_homologacoes:
        _exibir_homologacao_resumida(
            homologacao
        )

    print(
        "\nTotal de Homologações encontradas: "
        f"{len(lista_homologacoes)}"
    )

# ============================================================
# SELEÇÃO DE STATUS
# ============================================================

def _selecionar_status_projeto() -> str | None:
    """
    Exibe os status oficiais de Projeto e retorna
    o status correspondente ao código informado.

    Retorna None quando o código for inválido.
    """

    status.exibir_status()

    codigo_status = ler_int(
        "\nDigite o código do status: "
    )

    status_selecionado = status.obter_status(
        codigo_status
    )

    if status_selecionado is None:
        print(
            "\nStatus de Projeto inválido."
        )

    return status_selecionado

def _selecionar_status_homologacao(
) -> StatusHomologacao | None:
    """
    Exibe os status oficiais da Homologação e retorna
    o estado correspondente à opção informada.

    Retorna None quando a opção for inválida.
    """

    status_disponiveis = list(
        StatusHomologacao
    )

    print(
        "\nStatus de Homologação:"
    )

    for indice, status_homologacao in enumerate(
        status_disponiveis,
        start=1,
    ):
        rotulo = ROTULOS_STATUS_HOMOLOGACAO[
            status_homologacao
        ]

        print(
            f"{indice} - {rotulo}"
        )

    opcao = ler_int(
        "\nDigite o código do status: "
    )

    if (
        opcao < 1
        or opcao > len(status_disponiveis)
    ):
        print(
            "\nStatus de Homologação inválido."
        )

        return None

    return status_disponiveis[
        opcao - 1
    ]

# ============================================================
# CONSULTAS DE PROJETOS
# ============================================================

def consultar_projetos_por_cliente() -> None:
    """
    Consulta os Projetos vinculados
    ao Cliente informado.
    """

    _exibir_titulo(
        "PROJETOS POR CLIENTE"
    )

    codigo_cliente = ler_int(
        "Código do Cliente: "
    )

    projetos_encontrados = (
        projetos.buscar_projetos_do_cliente(
            codigo_cliente
        )
    )

    _exibir_projetos(
        projetos_encontrados
    )

def consultar_projetos_por_status() -> None:
    """
    Consulta os Projetos que possuem
    o status selecionado.
    """

    _exibir_titulo(
        "PROJETOS POR STATUS"
    )

    status_selecionado = (
        _selecionar_status_projeto()
    )

    if status_selecionado is None:
        return

    projetos_encontrados = (
        projetos.buscar_projetos_com_status(
            status_selecionado
        )
    )

    _exibir_projetos(
        projetos_encontrados
    )

# ============================================================
# CONSULTAS DE HOMOLOGAÇÕES
# ============================================================

def consultar_homologacao_por_projeto() -> None:
    """
    Consulta a Homologação ativa de um Projeto
    dentro do contexto de uma Empresa.
    """

    _exibir_titulo(
        "HOMOLOGAÇÃO ATIVA POR PROJETO"
    )

    codigo_empresa = ler_int(
        "Código da Empresa: "
    )

    codigo_projeto = ler_int(
        "Código do Projeto: "
    )

    homologacao_encontrada = (
        homologacoes
        .buscar_homologacao_por_projeto(
            codigo_projeto=codigo_projeto,
            codigo_empresa=codigo_empresa,
        )
    )

    if homologacao_encontrada is None:
        print(
            "\nNenhuma Homologação ativa encontrada "
            "para o Projeto."
        )

        return

    _exibir_homologacao_resumida(
        homologacao_encontrada
    )

def consultar_homologacoes_por_empresa() -> None:
    """
    Consulta todas as Homologações
    pertencentes à Empresa informada.
    """

    _exibir_titulo(
        "HOMOLOGAÇÕES POR EMPRESA"
    )

    codigo_empresa = ler_int(
        "Código da Empresa: "
    )

    homologacoes_encontradas = (
        homologacoes.listar_homologacoes(
            codigo_empresa=codigo_empresa,
        )
    )

    _exibir_homologacoes(
        homologacoes_encontradas
    )

def consultar_homologacoes_por_concessionaria() -> None:
    """
    Consulta as Homologações vinculadas
    a uma Concessionária.

    O código da Empresa também é solicitado para preservar
    o isolamento multiempresa.
    """

    _exibir_titulo(
        "HOMOLOGAÇÕES POR CONCESSIONÁRIA"
    )

    codigo_empresa = ler_int(
        "Código da Empresa: "
    )

    codigo_concessionaria = ler_int(
        "Código da Concessionária: "
    )

    homologacoes_encontradas = (
        homologacoes
        .listar_homologacoes_por_concessionaria(
            codigo_concessionaria=(
                codigo_concessionaria
            ),
            codigo_empresa=codigo_empresa,
        )
    )

    _exibir_homologacoes(
        homologacoes_encontradas
    )

def consultar_homologacoes_por_status() -> None:
    """
    Consulta as Homologações de uma Empresa
    que possuem o status selecionado.
    """

    _exibir_titulo(
        "HOMOLOGAÇÕES POR STATUS"
    )

    codigo_empresa = ler_int(
        "Código da Empresa: "
    )

    status_selecionado = (
        _selecionar_status_homologacao()
    )

    if status_selecionado is None:
        return

    homologacoes_encontradas = (
        homologacoes
        .listar_homologacoes_por_status(
            status=status_selecionado,
            codigo_empresa=codigo_empresa,
        )
    )

    _exibir_homologacoes(
        homologacoes_encontradas
    )

# ============================================================
# MENU DE CONSULTAS RÁPIDAS
# ============================================================

def menu_consultas_rapidas() -> None:
    """
    Exibe o menu de Consultas Rápidas até
    que o operador escolha voltar.
    """

    while True:
        _exibir_titulo(
            "CONSULTAS RÁPIDAS"
        )

        print(
            "1 - Projetos por Cliente"
        )

        print(
            "2 - Homologação ativa por Projeto"
        )

        print(
            "3 - Homologações por Empresa"
        )

        print(
            "4 - Homologações por Concessionária"
        )

        print(
            "5 - Projetos por Status"
        )

        print(
            "6 - Homologações por Status"
        )

        print(
            "0 - Voltar"
        )

        opcao = input(
            "\nEscolha uma opção: "
        ).strip()

        if opcao == "1":
            consultar_projetos_por_cliente()
            _pausar()

        elif opcao == "2":
            consultar_homologacao_por_projeto()
            _pausar()

        elif opcao == "3":
            consultar_homologacoes_por_empresa()
            _pausar()

        elif opcao == "4":
            consultar_homologacoes_por_concessionaria()
            _pausar()

        elif opcao == "5":
            consultar_projetos_por_status()
            _pausar()

        elif opcao == "6":
            consultar_homologacoes_por_status()
            _pausar()

        elif opcao == "0":
            return

        else:
            print(
                "\nOpção inválida."
            )

            _pausar()