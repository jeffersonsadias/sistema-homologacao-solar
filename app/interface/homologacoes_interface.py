"""
Interface de terminal para Homologações.

Este módulo é responsável por:

- apresentar o menu de Homologações;
- solicitar dados ao operador;
- exibir resultados;
- chamar funções públicas da fachada.

A interface não deve:

- acessar diretamente a coleção de Homologações;
- acessar arquivos JSON;
- executar regras de negócio;
- criar dicionários de Homologação manualmente.
"""

from typing import Any

from app import homologacoes
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
    Aguarda confirmação antes de retornar ao menu.
    """

    input(
        "\nPressione Enter para continuar..."
    )

def _exibir_homologacao(
    homologacao: dict[str, Any],
) -> None:
    """
    Exibe os dados principais de uma Homologação.
    """

    print()
    print("-" * 60)

    print(
        f"Código:                    "
        f"{homologacao.get('codigo', '-')}"
    )

    print(
        f"Código da Empresa:         "
        f"{homologacao.get('codigo_empresa', '-')}"
    )

    print(
        f"Código do Projeto:         "
        f"{homologacao.get('codigo_projeto', '-')}"
    )

    print(
        f"Código da Concessionária:  "
        f"{homologacao.get('codigo_concessionaria', '-')}"
    )

    print(
        f"Status:                    "
        f"{homologacao.get('status', '-')}"
    )

    print(
        f"Data de abertura:          "
        f"{homologacao.get('data_abertura', '-')}"
    )

    print(
        f"Previsão de conclusão:     "
        f"{homologacao.get('data_prevista_conclusao', '-')}"
    )

    print(
        f"Responsável pela abertura: "
        f"{homologacao.get('responsavel_abertura', '-')}"
    )

    print(
        f"Responsável atual:         "
        f"{homologacao.get('responsavel_atual', '-')}"
    )

    print(
        f"Quantidade de documentos:  "
        f"{len(homologacao.get('documentos', []))}"
    )

    print(
        f"Quantidade de submissões:  "
        f"{len(homologacao.get('submissoes', []))}"
    )

    observacoes = (
        homologacao.get("observacoes")
        or "Nenhuma"
    )

    print(
        f"Observações:               "
        f"{observacoes}"
    )

    print("-" * 60)

# ============================================================
# CADASTRO
# ============================================================

def cadastrar_homologacao_interface() -> None:
    """
    Solicita os dados necessários e cria uma Homologação.

    Nesta primeira versão, o prazo estimado padrão da fachada,
    de 45 dias, será utilizado.
    """

    _exibir_titulo(
        "CADASTRO DE HOMOLOGAÇÃO"
    )

    codigo_empresa = ler_int(
        "Código da Empresa: "
    )

    codigo_projeto = ler_int(
        "Código do Projeto: "
    )

    codigo_concessionaria = ler_int(
        "Código da Concessionária: "
    )

    data_abertura = input(
        "Data de abertura (AAAA-MM-DD): "
    ).strip()

    responsavel_abertura = input(
        "Responsável pela abertura: "
    ).strip()

    observacoes = input(
        "Observações, se houver: "
    ).strip()

    try:
        nova_homologacao = (
            homologacoes.criar_homologacao(
                codigo_empresa=codigo_empresa,
                codigo_projeto=codigo_projeto,
                codigo_concessionaria=(
                    codigo_concessionaria
                ),
                data_abertura=data_abertura,
                responsavel_abertura=(
                    responsavel_abertura
                ),
                observacoes=observacoes,
            )
        )

    except (TypeError, ValueError) as erro:
        print(
            "\nNão foi possível criar a Homologação: "
            f"{erro}"
        )

        return

    print(
        "\nHomologação criada com sucesso."
    )

    _exibir_homologacao(
        nova_homologacao
    )

# ============================================================
# LISTAGEM
# ============================================================

def listar_homologacoes_interface() -> None:
    """
    Lista as Homologações de uma Empresa.

    A seleção da Empresa preserva o isolamento multiempresa.
    """

    _exibir_titulo(
        "LISTAGEM DE HOMOLOGAÇÕES"
    )

    codigo_empresa = ler_int(
        "Código da Empresa: "
    )

    lista_homologacoes = (
        homologacoes.listar_homologacoes(
            codigo_empresa=codigo_empresa,
        )
    )

    if not lista_homologacoes:
        print(
            "\nNenhuma Homologação encontrada "
            "para esta Empresa."
        )

        return

    for homologacao in lista_homologacoes:
        _exibir_homologacao(
            homologacao
        )

    print(
        "\nTotal de Homologações: "
        f"{len(lista_homologacoes)}"
    )

# ============================================================
# CONSULTA
# ============================================================

def buscar_homologacao_interface() -> None:
    """
    Busca uma Homologação por código dentro de uma Empresa.
    """

    _exibir_titulo(
        "CONSULTA DE HOMOLOGAÇÃO"
    )

    codigo_empresa = ler_int(
        "Código da Empresa: "
    )

    codigo_homologacao = ler_int(
        "Código da Homologação: "
    )

    homologacao_encontrada = (
        homologacoes.buscar_homologacao(
            codigo_homologacao=(
                codigo_homologacao
            ),
            codigo_empresa=codigo_empresa,
        )
    )

    if homologacao_encontrada is None:
        print(
            "\nHomologação não encontrada."
        )

        return

    _exibir_homologacao(
        homologacao_encontrada
    )

# ============================================================
# MENU DE HOMOLOGAÇÕES
# ============================================================

def menu_homologacoes() -> None:
    """
    Exibe o menu inicial de Homologações.

    O menu permanece aberto até o operador escolher voltar.
    """

    while True:
        _exibir_titulo(
            "HOMOLOGAÇÕES"
        )

        print(
            "1 - Cadastrar Homologação"
        )

        print(
            "2 - Listar Homologações"
        )

        print(
            "3 - Buscar Homologação"
        )

        print(
            "0 - Voltar"
        )

        opcao = input(
            "\nEscolha uma opção: "
        ).strip()

        if opcao == "1":
            cadastrar_homologacao_interface()
            _pausar()

        elif opcao == "2":
            listar_homologacoes_interface()
            _pausar()

        elif opcao == "3":
            buscar_homologacao_interface()
            _pausar()

        elif opcao == "0":
            return

        else:
            print(
                "\nOpção inválida."
            )

            _pausar()