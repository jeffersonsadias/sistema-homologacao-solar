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

def _exibir_instalacao(
    homologacao: dict[str, Any],
) -> None:
    """
    Exibe os dados da Instalação registrada
    nas Operações de Campo da Homologação.
    """

    operacoes_campo = homologacao.get(
        "operacoes_campo"
    ) or {}

    instalacao = operacoes_campo.get(
        "instalacao"
    )

    if instalacao is None:
        print(
            "\nNenhuma Instalação registrada."
        )

        return

    print()
    print("-" * 60)
    print("DADOS DA INSTALAÇÃO")
    print("-" * 60)

    print(
        f"Status:                     "
        f"{instalacao.get('status', '-')}"
    )

    print(
        f"Data prevista:              "
        f"{instalacao.get('data_prevista', '-')}"
    )

    print(
        f"Equipe responsável:         "
        f"{instalacao.get('equipe_responsavel', '-')}"
    )

    print(
        f"Responsável planejamento:   "
        f"{instalacao.get('responsavel_planejamento', '-')}"
    )

    print(
        f"Data de início:             "
        f"{instalacao.get('data_inicio') or '-'}"
    )

    print(
        f"Responsável pelo início:    "
        f"{instalacao.get('responsavel_inicio') or '-'}"
    )

    print(
        f"Data de conclusão:          "
        f"{instalacao.get('data_conclusao') or '-'}"
    )

    print(
        f"Responsável pela conclusão: "
        f"{instalacao.get('responsavel_conclusao') or '-'}"
    )

    print(
        f"Observações:                "
        f"{instalacao.get('observacoes') or 'Nenhuma'}"
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
# OPERAÇÕES DE CAMPO — INSTALAÇÃO
# ============================================================

def planejar_instalacao_interface() -> None:
    """
    Solicita os dados necessários para registrar
    o planejamento da Instalação.
    """

    _exibir_titulo(
        "PLANEJAMENTO DA INSTALAÇÃO"
    )

    codigo_empresa = ler_int(
        "Código da Empresa: "
    )

    codigo_homologacao = ler_int(
        "Código da Homologação: "
    )

    data_prevista = input(
        "Data prevista da Instalação "
        "(AAAA-MM-DD): "
    ).strip()

    responsavel_planejamento = input(
        "Responsável pelo planejamento: "
    ).strip()

    equipe_responsavel = input(
        "Equipe responsável: "
    ).strip()

    data_movimentacao = input(
        "Data do registro (AAAA-MM-DD): "
    ).strip()

    observacoes = input(
        "Observações, se houver: "
    ).strip()

    try:
        homologacao_atualizada = (
            homologacoes.planejar_instalacao(
                codigo_homologacao=(
                    codigo_homologacao
                ),
                codigo_empresa=codigo_empresa,
                data_prevista=data_prevista,
                responsavel_planejamento=(
                    responsavel_planejamento
                ),
                equipe_responsavel=(
                    equipe_responsavel
                ),
                data_movimentacao=(
                    data_movimentacao
                ),
                observacoes=observacoes,
            )
        )

    except (TypeError, ValueError) as erro:
        print(
            "\nNão foi possível planejar "
            f"a Instalação: {erro}"
        )

        return

    print(
        "\nInstalação planejada com sucesso."
    )

    _exibir_instalacao(
        homologacao_atualizada
    )

def iniciar_instalacao_interface() -> None:
    """
    Solicita os dados necessários para registrar
    o início da execução da Instalação.
    """

    _exibir_titulo(
        "INÍCIO DA INSTALAÇÃO"
    )

    codigo_empresa = ler_int(
        "Código da Empresa: "
    )

    codigo_homologacao = ler_int(
        "Código da Homologação: "
    )

    data_inicio = input(
        "Data de início (AAAA-MM-DD): "
    ).strip()

    responsavel_inicio = input(
        "Responsável pelo início: "
    ).strip()

    data_movimentacao = input(
        "Data do registro (AAAA-MM-DD): "
    ).strip()

    try:
        homologacao_atualizada = (
            homologacoes
            .iniciar_execucao_instalacao(
                codigo_homologacao=(
                    codigo_homologacao
                ),
                codigo_empresa=codigo_empresa,
                data_inicio=data_inicio,
                responsavel_inicio=(
                    responsavel_inicio
                ),
                data_movimentacao=(
                    data_movimentacao
                ),
            )
        )

    except (TypeError, ValueError) as erro:
        print(
            "\nNão foi possível iniciar "
            f"a Instalação: {erro}"
        )

        return

    print(
        "\nInstalação iniciada com sucesso."
    )

    _exibir_instalacao(
        homologacao_atualizada
    )

def concluir_instalacao_interface() -> None:
    """
    Solicita os dados necessários para registrar
    a conclusão da Instalação.
    """

    _exibir_titulo(
        "CONCLUSÃO DA INSTALAÇÃO"
    )

    codigo_empresa = ler_int(
        "Código da Empresa: "
    )

    codigo_homologacao = ler_int(
        "Código da Homologação: "
    )

    data_conclusao = input(
        "Data de conclusão (AAAA-MM-DD): "
    ).strip()

    responsavel_conclusao = input(
        "Responsável pela conclusão: "
    ).strip()

    data_movimentacao = input(
        "Data do registro (AAAA-MM-DD): "
    ).strip()

    observacoes = input(
        "Observações finais, se houver: "
    ).strip()

    try:
        homologacao_atualizada = (
            homologacoes
            .concluir_execucao_instalacao(
                codigo_homologacao=(
                    codigo_homologacao
                ),
                codigo_empresa=codigo_empresa,
                data_conclusao=data_conclusao,
                responsavel_conclusao=(
                    responsavel_conclusao
                ),
                data_movimentacao=(
                    data_movimentacao
                ),
                observacoes=observacoes,
            )
        )

    except (TypeError, ValueError) as erro:
        print(
            "\nNão foi possível concluir "
            f"a Instalação: {erro}"
        )

        return

    print(
        "\nInstalação concluída com sucesso."
    )

    _exibir_instalacao(
        homologacao_atualizada
    )

def menu_instalacao() -> None:
    """
    Exibe o submenu operacional da Instalação.
    """

    while True:
        _exibir_titulo(
            "GESTÃO DA INSTALAÇÃO"
        )

        print(
            "1 - Planejar Instalação"
        )

        print(
            "2 - Iniciar execução"
        )

        print(
            "3 - Concluir Instalação"
        )

        print(
            "0 - Voltar"
        )

        opcao = input(
            "\nEscolha uma opção: "
        ).strip()

        if opcao == "1":
            planejar_instalacao_interface()
            _pausar()

        elif opcao == "2":
            iniciar_instalacao_interface()
            _pausar()

        elif opcao == "3":
            concluir_instalacao_interface()
            _pausar()

        elif opcao == "0":
            return

        else:
            print(
                "\nOpção inválida."
            )

            _pausar()

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
            "4 - Gerenciar Instalação"
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

        elif opcao == "4":
            menu_instalacao()

        elif opcao == "0":
            return

        else:
            print(
                "\nOpção inválida."
            )

            _pausar()