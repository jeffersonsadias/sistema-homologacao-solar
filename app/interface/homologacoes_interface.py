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

def _exibir_vistorias(
    homologacao: dict[str, Any],
) -> None:
    """
    Exibe as Vistorias registradas
    nas Operações de Campo da Homologação.
    """

    operacoes_campo = homologacao.get(
        "operacoes_campo"
    ) or {}

    vistorias = operacoes_campo.get(
        "vistorias"
    ) or []

    if not vistorias:
        print(
            "\nNenhuma Vistoria registrada."
        )

        return

    print()
    print("-" * 60)
    print("VISTORIAS")
    print("-" * 60)

    for vistoria in vistorias:
        print(
            f"Código:                    "
            f"{vistoria.get('codigo', '-')}"
        )

        print(
            f"Status:                    "
            f"{vistoria.get('status', '-')}"
        )

        print(
            f"Data da solicitação:       "
            f"{vistoria.get('data_solicitacao') or '-'}"
        )

        print(
            f"Protocolo:                 "
            f"{vistoria.get('protocolo') or '-'}"
        )

        print(
            f"Data do agendamento:       "
            f"{vistoria.get('data_agendamento') or '-'}"
        )

        print(
            f"Data da realização:        "
            f"{vistoria.get('data_realizacao') or '-'}"
        )

        print(
            f"Data do resultado:         "
            f"{vistoria.get('data_resultado') or '-'}"
        )

        print(
            f"Motivo da reprovação:      "
            f"{vistoria.get('motivo_reprovacao') or '-'}"
        )

        print(
            f"Observações:               "
            f"{vistoria.get('observacoes') or 'Nenhuma'}"
        )

        print("-" * 60)

def _exibir_ligacao(
    homologacao: dict[str, Any],
) -> None:
    """
    Exibe os dados da Ligação e Energização
    registrada nas Operações de Campo.
    """

    operacoes_campo = homologacao.get(
        "operacoes_campo"
    ) or {}

    ligacao = operacoes_campo.get(
        "ligacao"
    )

    if ligacao is None:
        print(
            "\nNenhuma Ligação registrada."
        )

        return

    print()
    print("-" * 60)
    print("LIGAÇÃO E ENERGIZAÇÃO")
    print("-" * 60)

    print(
        f"Status:                    "
        f"{ligacao.get('status', '-')}"
    )

    print(
        f"Data da solicitação:       "
        f"{ligacao.get('data_solicitacao') or '-'}"
    )

    print(
        f"Responsável solicitação:   "
        f"{ligacao.get('responsavel_solicitacao') or '-'}"
    )

    print(
        f"Protocolo:                 "
        f"{ligacao.get('protocolo') or '-'}"
    )

    print(
        f"Data do agendamento:       "
        f"{ligacao.get('data_agendamento') or '-'}"
    )

    print(
        f"Responsável agendamento:   "
        f"{ligacao.get('responsavel_agendamento') or '-'}"
    )

    print(
        f"Data da Ligação:           "
        f"{ligacao.get('data_ligacao') or '-'}"
    )

    print(
        f"Responsável pela Ligação:  "
        f"{ligacao.get('responsavel_ligacao') or '-'}"
    )

    print(
        f"Observações:               "
        f"{ligacao.get('observacoes') or 'Nenhuma'}"
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
# OPERAÇÕES DE CAMPO — VISTORIA
# ============================================================

def solicitar_vistoria_interface() -> None:
    """
    Solicita os dados necessários para registrar
    uma nova tentativa de Vistoria.
    """

    _exibir_titulo(
        "SOLICITAÇÃO DE VISTORIA"
    )

    codigo_empresa = ler_int(
        "Código da Empresa: "
    )

    codigo_homologacao = ler_int(
        "Código da Homologação: "
    )

    data_solicitacao = input(
        "Data da solicitação (AAAA-MM-DD): "
    ).strip()

    responsavel_solicitacao = input(
        "Responsável pela solicitação: "
    ).strip()

    protocolo = input(
        "Protocolo da solicitação: "
    ).strip()

    data_movimentacao = input(
        "Data do registro (AAAA-MM-DD): "
    ).strip()

    observacoes = input(
        "Observações, se houver: "
    ).strip()

    try:
        homologacao_atualizada = (
            homologacoes.solicitar_nova_vistoria(
                codigo_homologacao=(
                    codigo_homologacao
                ),
                codigo_empresa=codigo_empresa,
                data_solicitacao=(
                    data_solicitacao
                ),
                responsavel_solicitacao=(
                    responsavel_solicitacao
                ),
                protocolo=protocolo,
                data_movimentacao=(
                    data_movimentacao
                ),
                observacoes=observacoes,
            )
        )

    except (TypeError, ValueError) as erro:
        print(
            "\nNão foi possível solicitar "
            f"a Vistoria: {erro}"
        )

        return

    print(
        "\nVistoria solicitada com sucesso."
    )

    _exibir_vistorias(
        homologacao_atualizada
    )

def agendar_vistoria_interface() -> None:
    """
    Solicita os dados necessários para registrar
    o agendamento de uma Vistoria.
    """

    _exibir_titulo(
        "AGENDAMENTO DA VISTORIA"
    )

    codigo_empresa = ler_int(
        "Código da Empresa: "
    )

    codigo_homologacao = ler_int(
        "Código da Homologação: "
    )

    codigo_vistoria = ler_int(
        "Código da Vistoria: "
    )

    data_agendamento = input(
        "Data do agendamento (AAAA-MM-DD): "
    ).strip()

    responsavel_agendamento = input(
        "Responsável pelo agendamento: "
    ).strip()

    data_movimentacao = input(
        "Data do registro (AAAA-MM-DD): "
    ).strip()

    observacoes = input(
        "Observações, se houver: "
    ).strip()

    try:
        homologacao_atualizada = (
            homologacoes
            .agendar_vistoria_homologacao(
                codigo_homologacao=(
                    codigo_homologacao
                ),
                codigo_empresa=codigo_empresa,
                codigo_vistoria=codigo_vistoria,
                data_agendamento=(
                    data_agendamento
                ),
                responsavel_agendamento=(
                    responsavel_agendamento
                ),
                data_movimentacao=(
                    data_movimentacao
                ),
                observacoes=observacoes,
            )
        )

    except (TypeError, ValueError) as erro:
        print(
            "\nNão foi possível agendar "
            f"a Vistoria: {erro}"
        )

        return

    print(
        "\nVistoria agendada com sucesso."
    )

    _exibir_vistorias(
        homologacao_atualizada
    )

def registrar_realizacao_vistoria_interface() -> None:
    """
    Solicita os dados necessários para registrar
    a realização de uma Vistoria.
    """

    _exibir_titulo(
        "REALIZAÇÃO DA VISTORIA"
    )

    codigo_empresa = ler_int(
        "Código da Empresa: "
    )

    codigo_homologacao = ler_int(
        "Código da Homologação: "
    )

    codigo_vistoria = ler_int(
        "Código da Vistoria: "
    )

    data_realizacao = input(
        "Data da realização (AAAA-MM-DD): "
    ).strip()

    responsavel_realizacao = input(
        "Responsável pela realização: "
    ).strip()

    data_movimentacao = input(
        "Data do registro (AAAA-MM-DD): "
    ).strip()

    observacoes = input(
        "Observações, se houver: "
    ).strip()

    try:
        homologacao_atualizada = (
            homologacoes
            .registrar_realizacao_vistoria_homologacao(
                codigo_homologacao=(
                    codigo_homologacao
                ),
                codigo_empresa=codigo_empresa,
                codigo_vistoria=codigo_vistoria,
                data_realizacao=data_realizacao,
                responsavel_realizacao=(
                    responsavel_realizacao
                ),
                data_movimentacao=(
                    data_movimentacao
                ),
                observacoes=observacoes,
            )
        )

    except (TypeError, ValueError) as erro:
        print(
            "\nNão foi possível registrar "
            f"a realização da Vistoria: {erro}"
        )

        return

    print(
        "\nRealização da Vistoria registrada "
        "com sucesso."
    )

    _exibir_vistorias(
        homologacao_atualizada
    )

def aprovar_vistoria_interface() -> None:
    """
    Solicita os dados necessários para registrar
    a aprovação formal de uma Vistoria.
    """

    _exibir_titulo(
        "APROVAÇÃO DA VISTORIA"
    )

    codigo_empresa = ler_int(
        "Código da Empresa: "
    )

    codigo_homologacao = ler_int(
        "Código da Homologação: "
    )

    codigo_vistoria = ler_int(
        "Código da Vistoria: "
    )

    data_resultado = input(
        "Data do resultado (AAAA-MM-DD): "
    ).strip()

    responsavel_resultado = input(
        "Responsável pelo resultado: "
    ).strip()

    data_movimentacao = input(
        "Data do registro (AAAA-MM-DD): "
    ).strip()

    observacoes = input(
        "Observações, se houver: "
    ).strip()

    try:
        homologacao_atualizada = (
            homologacoes
            .aprovar_vistoria_homologacao(
                codigo_homologacao=(
                    codigo_homologacao
                ),
                codigo_empresa=codigo_empresa,
                codigo_vistoria=codigo_vistoria,
                data_resultado=data_resultado,
                responsavel_resultado=(
                    responsavel_resultado
                ),
                data_movimentacao=(
                    data_movimentacao
                ),
                observacoes=observacoes,
            )
        )

    except (TypeError, ValueError) as erro:
        print(
            "\nNão foi possível aprovar "
            f"a Vistoria: {erro}"
        )

        return

    print(
        "\nVistoria aprovada com sucesso."
    )

    _exibir_vistorias(
        homologacao_atualizada
    )

def reprovar_vistoria_interface() -> None:
    """
    Solicita os dados necessários para registrar
    a reprovação formal de uma Vistoria.
    """

    _exibir_titulo(
        "REPROVAÇÃO DA VISTORIA"
    )

    codigo_empresa = ler_int(
        "Código da Empresa: "
    )

    codigo_homologacao = ler_int(
        "Código da Homologação: "
    )

    codigo_vistoria = ler_int(
        "Código da Vistoria: "
    )

    data_resultado = input(
        "Data do resultado (AAAA-MM-DD): "
    ).strip()

    responsavel_resultado = input(
        "Responsável pelo resultado: "
    ).strip()

    motivo_reprovacao = input(
        "Motivo da reprovação: "
    ).strip()

    data_movimentacao = input(
        "Data do registro (AAAA-MM-DD): "
    ).strip()

    observacoes = input(
        "Observações, se houver: "
    ).strip()

    try:
        homologacao_atualizada = (
            homologacoes
            .reprovar_vistoria_homologacao(
                codigo_homologacao=(
                    codigo_homologacao
                ),
                codigo_empresa=codigo_empresa,
                codigo_vistoria=codigo_vistoria,
                data_resultado=data_resultado,
                responsavel_resultado=(
                    responsavel_resultado
                ),
                motivo_reprovacao=(
                    motivo_reprovacao
                ),
                data_movimentacao=(
                    data_movimentacao
                ),
                observacoes=observacoes,
            )
        )

    except (TypeError, ValueError) as erro:
        print(
            "\nNão foi possível reprovar "
            f"a Vistoria: {erro}"
        )

        return

    print(
        "\nVistoria reprovada registrada com sucesso."
    )

    _exibir_vistorias(
        homologacao_atualizada
    )

def registrar_correcao_pos_vistoria_interface() -> None:
    """
    Solicita os dados necessários para registrar
    uma correção após Vistoria reprovada.
    """

    _exibir_titulo(
        "CORREÇÃO PÓS-VISTORIA"
    )

    codigo_empresa = ler_int(
        "Código da Empresa: "
    )

    codigo_homologacao = ler_int(
        "Código da Homologação: "
    )

    codigo_vistoria = ler_int(
        "Código da Vistoria: "
    )

    descricao_correcao = input(
        "Descrição da correção: "
    ).strip()

    responsavel_correcao = input(
        "Responsável pela correção: "
    ).strip()

    data_movimentacao = input(
        "Data do registro (AAAA-MM-DD): "
    ).strip()

    try:
        homologacao_atualizada = (
            homologacoes
            .registrar_correcao_pos_vistoria_homologacao(
                codigo_homologacao=(
                    codigo_homologacao
                ),
                codigo_empresa=codigo_empresa,
                codigo_vistoria=codigo_vistoria,
                descricao_correcao=(
                    descricao_correcao
                ),
                responsavel_correcao=(
                    responsavel_correcao
                ),
                data_movimentacao=(
                    data_movimentacao
                ),
            )
        )

    except (TypeError, ValueError) as erro:
        print(
            "\nNão foi possível registrar "
            f"a correção pós-vistoria: {erro}"
        )

        return

    print(
        "\nCorreção pós-vistoria registrada "
        "com sucesso."
    )

    _exibir_vistorias(
        homologacao_atualizada
    )

def menu_vistoria() -> None:
    """
    Exibe o submenu operacional da Vistoria.
    """

    while True:
        _exibir_titulo(
            "GESTÃO DA VISTORIA"
        )

        print(
            "1 - Solicitar nova Vistoria"
        )

        print(
            "2 - Agendar Vistoria"
        )

        print(
            "3 - Registrar realização"
        )

        print(
            "4 - Registrar aprovação"
        )

        print(
            "5 - Registrar reprovação"
        )

        print(
            "6 - Registrar correção pós-vistoria"
        )

        print(
            "0 - Voltar"
        )

        opcao = input(
            "\nEscolha uma opção: "
        ).strip()

        if opcao == "1":
            solicitar_vistoria_interface()
            _pausar()

        elif opcao == "2":
            agendar_vistoria_interface()
            _pausar()

        elif opcao == "3":
            registrar_realizacao_vistoria_interface()
            _pausar()

        elif opcao == "4":
            aprovar_vistoria_interface()
            _pausar()

        elif opcao == "5":
            reprovar_vistoria_interface()
            _pausar()

        elif opcao == "6":
            registrar_correcao_pos_vistoria_interface()
            _pausar()

        elif opcao == "0":
            return

        else:
            print(
                "\nOpção inválida."
            )

            _pausar()

# ============================================================
# OPERAÇÕES DE CAMPO — LIGAÇÃO E ENERGIZAÇÃO
# ============================================================

def solicitar_ligacao_interface() -> None:
    """
    Solicita os dados necessários para registrar
    a solicitação da Ligação e Energização.
    """

    _exibir_titulo(
        "SOLICITAÇÃO DE LIGAÇÃO E ENERGIZAÇÃO"
    )

    codigo_empresa = ler_int(
        "Código da Empresa: "
    )

    codigo_homologacao = ler_int(
        "Código da Homologação: "
    )

    data_solicitacao = input(
        "Data da solicitação (AAAA-MM-DD): "
    ).strip()

    responsavel_solicitacao = input(
        "Responsável pela solicitação: "
    ).strip()

    protocolo = input(
        "Protocolo da solicitação: "
    ).strip()

    data_movimentacao = input(
        "Data do registro (AAAA-MM-DD): "
    ).strip()

    observacoes = input(
        "Observações, se houver: "
    ).strip()

    try:
        homologacao_atualizada = (
            homologacoes
            .solicitar_ligacao_homologacao(
                codigo_homologacao=(
                    codigo_homologacao
                ),
                codigo_empresa=codigo_empresa,
                data_solicitacao=(
                    data_solicitacao
                ),
                responsavel_solicitacao=(
                    responsavel_solicitacao
                ),
                protocolo=protocolo,
                data_movimentacao=(
                    data_movimentacao
                ),
                observacoes=observacoes,
            )
        )

    except (TypeError, ValueError) as erro:
        print(
            "\nNão foi possível solicitar "
            f"a Ligação: {erro}"
        )

        return

    print(
        "\nLigação solicitada com sucesso."
    )

    _exibir_ligacao(
        homologacao_atualizada
    )

def agendar_ligacao_interface() -> None:
    """
    Solicita os dados necessários para registrar
    o agendamento da Ligação.
    """

    _exibir_titulo(
        "AGENDAMENTO DA LIGAÇÃO"
    )

    codigo_empresa = ler_int(
        "Código da Empresa: "
    )

    codigo_homologacao = ler_int(
        "Código da Homologação: "
    )

    data_agendamento = input(
        "Data do agendamento (AAAA-MM-DD): "
    ).strip()

    responsavel_agendamento = input(
        "Responsável pelo agendamento: "
    ).strip()

    data_movimentacao = input(
        "Data do registro (AAAA-MM-DD): "
    ).strip()

    observacoes = input(
        "Observações, se houver: "
    ).strip()

    try:
        homologacao_atualizada = (
            homologacoes
            .agendar_ligacao_homologacao(
                codigo_homologacao=(
                    codigo_homologacao
                ),
                codigo_empresa=codigo_empresa,
                data_agendamento=(
                    data_agendamento
                ),
                responsavel_agendamento=(
                    responsavel_agendamento
                ),
                data_movimentacao=(
                    data_movimentacao
                ),
                observacoes=observacoes,
            )
        )

    except (TypeError, ValueError) as erro:
        print(
            "\nNão foi possível agendar "
            f"a Ligação: {erro}"
        )

        return

    print(
        "\nLigação agendada com sucesso."
    )

    _exibir_ligacao(
        homologacao_atualizada
    )

def concluir_ligacao_interface() -> None:
    """
    Solicita os dados necessários para registrar
    a Ligação e Energização do sistema.
    """

    _exibir_titulo(
        "LIGAÇÃO E ENERGIZAÇÃO DO SISTEMA"
    )

    codigo_empresa = ler_int(
        "Código da Empresa: "
    )

    codigo_homologacao = ler_int(
        "Código da Homologação: "
    )

    data_ligacao = input(
        "Data da Ligação (AAAA-MM-DD): "
    ).strip()

    responsavel_ligacao = input(
        "Responsável pela Ligação: "
    ).strip()

    data_movimentacao = input(
        "Data do registro (AAAA-MM-DD): "
    ).strip()

    observacoes = input(
        "Observações, se houver: "
    ).strip()

    try:
        homologacao_atualizada = (
            homologacoes
            .concluir_ligacao_homologacao(
                codigo_homologacao=(
                    codigo_homologacao
                ),
                codigo_empresa=codigo_empresa,
                data_ligacao=data_ligacao,
                responsavel_ligacao=(
                    responsavel_ligacao
                ),
                data_movimentacao=(
                    data_movimentacao
                ),
                observacoes=observacoes,
            )
        )

    except (TypeError, ValueError) as erro:
        print(
            "\nNão foi possível registrar "
            f"a Ligação: {erro}"
        )

        return

    print(
        "\nLigação e Energização registradas "
        "com sucesso."
    )

    _exibir_ligacao(
        homologacao_atualizada
    )

def menu_ligacao() -> None:
    """
    Exibe o submenu operacional
    da Ligação e Energização.
    """

    while True:
        _exibir_titulo(
            "GESTÃO DA LIGAÇÃO E ENERGIZAÇÃO"
        )

        print(
            "1 - Solicitar Ligação"
        )

        print(
            "2 - Agendar Ligação"
        )

        print(
            "3 - Registrar Ligação / Energização"
        )

        print(
            "0 - Voltar"
        )

        opcao = input(
            "\nEscolha uma opção: "
        ).strip()

        if opcao == "1":
            solicitar_ligacao_interface()
            _pausar()

        elif opcao == "2":
            agendar_ligacao_interface()
            _pausar()

        elif opcao == "3":
            concluir_ligacao_interface()
            _pausar()

        elif opcao == "0":
            return

        else:
            print(
                "\nOpção inválida."
            )

            _pausar()

# ============================================================
# ENCERRAMENTO DA HOMOLOGAÇÃO
# ============================================================

def concluir_homologacao_interface() -> None:
    """
    Solicita os dados necessários para
    encerrar formalmente uma Homologação.
    """

    _exibir_titulo(
        "ENCERRAMENTO DA HOMOLOGAÇÃO"
    )

    codigo_empresa = ler_int(
        "Código da Empresa: "
    )

    codigo_homologacao = ler_int(
        "Código da Homologação: "
    )

    data_conclusao = input(
        "Data da conclusão (AAAA-MM-DD): "
    ).strip()

    responsavel_conclusao = input(
        "Responsável pela conclusão: "
    ).strip()

    observacoes = input(
        "Observações, se houver: "
    ).strip()

    try:
        homologacao_atualizada = (
            homologacoes
            .concluir_homologacao_fachada(
                codigo_homologacao=(
                    codigo_homologacao
                ),
                codigo_empresa=codigo_empresa,
                data_conclusao=data_conclusao,
                responsavel_conclusao=(
                    responsavel_conclusao
                ),
                observacoes=observacoes,
            )
        )

    except (TypeError, ValueError) as erro:
        print(
            "\nNão foi possível concluir "
            f"a Homologação: {erro}"
        )

        return

    print(
        "\nHomologação concluída com sucesso."
    )

    _exibir_homologacao(
        homologacao_atualizada
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
            "4 - Gerenciar Instalação"
        )

        print(
            "5 - Gerenciar Vistoria"
        )

        print(
            "6 - Gerenciar Ligação e Energização"
        )

        print(
            "7 - Encerrar Homologação"
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

        elif opcao == "5":
            menu_vistoria()

        elif opcao == "6":
            menu_ligacao()

        elif opcao == "7":
            concluir_homologacao_interface()
            _pausar()

        elif opcao == "0":
            return

        else:
            print(
                "\nOpção inválida."
            )

            _pausar()