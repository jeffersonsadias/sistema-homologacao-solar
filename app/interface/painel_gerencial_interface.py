"""
Interface textual do Painel Gerencial.

Responsabilidades:

- solicitar filtros;
- obter dados pela fachada;
- formatar indicadores;
- apresentar resultados ao usuário.

A interface não executa regras de negócio.
"""

from app import painel_gerencial
from app.utils import ler_int


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
    Aguarda confirmação do usuário.
    """

    input(
        "\nPressione ENTER para continuar..."
    )

def _formatar_percentual(
    valor: float,
) -> str:
    """
    Formata percentual usando
    vírgula como separador decimal.
    """

    return (
        f"{valor:.1f}%"
        .replace(".", ",")
    )

def _formatar_dias(
    valor: float,
) -> str:
    """
    Formata uma duração média em dias.
    """

    if valor == 1:
        return "1,0 dia"

    return (
        f"{valor:.1f} dias"
        .replace(".", ",")
    )

def _exibir_visao_geral(
    indicadores: dict,
) -> None:
    """
    Exibe os indicadores gerais.
    """

    visao_geral = indicadores[
        "visao_geral"
    ]

    print()
    print("VISÃO GERAL")
    print("-" * 60)

    print(
        "Projetos cadastrados............... "
        f"{visao_geral['total_projetos']:5}"
    )

    print(
        "Homologações cadastradas.......... "
        f"{visao_geral['total_homologacoes']:5}"
    )

    print(
        "Homologações em andamento.......... "
        f"{visao_geral['homologacoes_em_andamento']:5}"
    )

    print(
        "Homologações concluídas............ "
        f"{visao_geral['homologacoes_concluidas']:5}"
    )

    print(
        "Encerradas sem conclusão........... "
        f"{visao_geral['homologacoes_encerradas_sem_conclusao']:5}"
    )

def _exibir_desempenho(
    indicadores: dict,
) -> None:
    """
    Exibe os indicadores de desempenho
    da Homologação.
    """

    desempenho = indicadores[
        "desempenho"
    ]

    print()
    print("DESEMPENHO DA HOMOLOGAÇÃO")
    print("-" * 60)

    print(
        "Taxa de conclusão................. "
        f"{_formatar_percentual(
            desempenho['taxa_conclusao']
        )}"
    )

    print(
        "Tempo médio até conclusão......... "
        f"{_formatar_dias(
            desempenho[
                'tempo_medio_conclusao_dias'
            ]
        )}"
    )

    print(
        "Homologações com exigências....... "
        f"{desempenho[
            'homologacoes_com_exigencias_abertas'
        ]:5}"
    )

def _exibir_distribuicao(
    titulo: str,
    itens: list[dict],
) -> None:
    """
    Exibe uma distribuição gerencial.
    """

    print()
    print(titulo)
    print("-" * 60)

    if not itens:
        print(
            "Nenhum dado disponível."
        )
        return

    for item in itens:
        nome = item["nome"]
        quantidade = item["quantidade"]

        print(
            f"{nome:<45}"
            f"{quantidade:>5}"
        )

def _exibir_operacoes_campo(
    indicadores: dict,
) -> None:
    """
    Exibe indicadores das
    Operações de Campo.
    """

    operacoes = indicadores[
        "operacoes_campo"
    ]

    print()
    print("OPERAÇÕES DE CAMPO")
    print("-" * 60)

    print(
        "Instalações aguardando execução... "
        f"{operacoes[
            'instalacoes_aguardando_execucao'
        ]:5}"
    )

    print(
        "Vistorias aguardando resultado.... "
        f"{operacoes[
            'vistorias_aguardando_resultado'
        ]:5}"
    )

    print(
        "Ligações aguardando conclusão..... "
        f"{operacoes[
            'ligacoes_aguardando_conclusao'
        ]:5}"
    )

def exibir_painel_gerencial(
    codigo_empresa: int | None = None,
) -> None:
    """
    Obtém e exibe o Painel Gerencial.

    Quando codigo_empresa for informado,
    apresenta somente dados daquela Empresa.
    """

    indicadores = (
        painel_gerencial
        .obter_painel_gerencial(
            codigo_empresa=codigo_empresa
        )
    )

    _exibir_titulo(
        "PAINEL GERENCIAL"
    )

    _exibir_visao_geral(
        indicadores
    )

    _exibir_desempenho(
        indicadores
    )

    distribuicao = indicadores[
        "distribuicao"
    ]

    _exibir_distribuicao(
        titulo="PROJETOS POR EMPRESA",
        itens=(
            distribuicao[
                "projetos_por_empresa"
            ]
        ),
    )

    _exibir_distribuicao(
        titulo="PROJETOS POR CONCESSIONÁRIA",
        itens=(
            distribuicao[
                "projetos_por_concessionaria"
            ]
        ),
    )

    _exibir_operacoes_campo(
        indicadores
    )

def menu_painel_gerencial() -> None:
    """
    Exibe as opções de consulta
    do Painel Gerencial.
    """

    while True:
        _exibir_titulo(
            "PAINEL GERENCIAL"
        )

        print(
            "1 - Visão geral de todas as Empresas"
        )

        print(
            "2 - Filtrar por Empresa"
        )

        print(
            "0 - Voltar"
        )

        opcao = input(
            "\nEscolha uma opção: "
        ).strip()

        if opcao == "1":
            exibir_painel_gerencial()
            _pausar()

        elif opcao == "2":
            codigo_empresa = ler_int(
                "Código da Empresa: "
            )

            exibir_painel_gerencial(
                codigo_empresa=(
                    codigo_empresa
                )
            )

            _pausar()

        elif opcao == "0":
            return

        else:
            print(
                "\nOpção inválida."
            )

            _pausar()


