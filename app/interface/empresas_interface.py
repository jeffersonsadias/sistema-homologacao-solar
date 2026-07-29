"""
Interface de terminal para Empresas.

Este módulo é responsável por:

- apresentar menus;
- receber dados do usuário;
- exibir resultados;
- chamar as funções públicas da fachada.

Este módulo não deve:

- validar CNPJ internamente;
- gerar códigos;
- manipular a lista interna de empresas;
- acessar diretamente o arquivo JSON;
- alterar diretamente os dicionários da fachada.
"""

from typing import Any

from app import empresas
from app.utils import ler_int


# ============================================================
# FUNÇÕES AUXILIARES DE EXIBIÇÃO
# ============================================================

def _formatar_cnpj(cnpj: str) -> str:
    """
    Formata um CNPJ armazenado somente com números.

    Exemplo:

        11222333000181

    torna-se:

        11.222.333/0001-81
    """

    if len(cnpj) != 14:
        return cnpj

    return (
        f"{cnpj[:2]}."
        f"{cnpj[2:5]}."
        f"{cnpj[5:8]}/"
        f"{cnpj[8:12]}-"
        f"{cnpj[12:]}"
    )


def _formatar_telefone(telefone: str) -> str:
    """
    Formata telefones brasileiros para exibição.

    A função não altera os dados persistidos.
    """

    if len(telefone) == 11:
        return (
            f"({telefone[:2]}) "
            f"{telefone[2:7]}-"
            f"{telefone[7:]}"
        )

    if len(telefone) == 10:
        return (
            f"({telefone[:2]}) "
            f"{telefone[2:6]}-"
            f"{telefone[6:]}"
        )

    return telefone


def _exibir_titulo(titulo: str) -> None:
    """
    Exibe um título padronizado.
    """

    print()
    print("=" * 60)
    print(titulo)
    print("=" * 60)


def _exibir_empresa(
    empresa: dict[str, Any],
) -> None:
    """
    Exibe todos os dados principais de uma empresa.
    """

    print()
    print(f"Código:         {empresa['codigo']}")
    print(f"Razão social:   {empresa['razao_social']}")
    print(f"Nome fantasia:  {empresa['nome_fantasia']}")
    print(
        "CNPJ:           "
        f"{_formatar_cnpj(empresa['cnpj'])}"
    )
    print(f"E-mail:         {empresa['email']}")
    print(
        "Telefone:       "
        f"{_formatar_telefone(empresa['telefone'])}"
    )
    print(f"Situação:       {empresa['situacao']}")
    print(
        "Data cadastro:  "
        f"{empresa.get('data_cadastro', '-')}"
    )
    print(
        "Última alteração: "
        f"{empresa.get('data_atualizacao', '-')}"
    )


def _exibir_empresa_resumida(
    empresa: dict[str, Any],
) -> None:
    """
    Exibe uma linha resumida da empresa.
    """

    print(
        f"Código: {empresa['codigo']} | "
        f"{empresa['nome_fantasia']} | "
        f"CNPJ: {_formatar_cnpj(empresa['cnpj'])} | "
        f"Situação: {empresa['situacao']}"
    )


def _pressionar_enter_para_continuar() -> None:
    """
    Aguarda o usuário antes de retornar ao menu.
    """

    input(
        "\nPressione Enter para continuar..."
    )


# ============================================================
# LEITURA E SELEÇÃO
# ============================================================

def _selecionar_empresa() -> dict[str, Any] | None:
    """
    Solicita um código e tenta localizar a empresa.

    Retorna:
    - o dicionário encontrado;
    - None quando a empresa não existe.
    """

    codigo_empresa = ler_int(
        "Informe o código da empresa: "
    )

    empresa_encontrada = empresas.buscar_empresa(
        codigo_empresa,
    )

    if empresa_encontrada is None:
        print(
            "\nEmpresa não encontrada."
        )

        return None

    return empresa_encontrada


def _ler_campo_opcional(
    mensagem: str,
    valor_atual: str,
) -> str | None:
    """
    Lê um campo durante a edição.

    Quando o usuário pressiona Enter sem digitar,
    o valor atual é preservado e None é retornado.
    """

    valor = input(
        f"{mensagem} [{valor_atual}]: "
    ).strip()

    if not valor:
        return None

    return valor


# ============================================================
# CADASTRO
# ============================================================

def cadastrar_empresa_interface() -> None:
    """
    Solicita os dados e cadastra uma nova empresa.
    """

    _exibir_titulo(
        "CADASTRO DE EMPRESA"
    )

    razao_social = input(
        "Razão social: "
    )

    nome_fantasia = input(
        "Nome fantasia: "
    )

    cnpj = input(
        "CNPJ: "
    )

    email = input(
        "E-mail: "
    )

    telefone = input(
        "Telefone: "
    )

    try:
        empresa_cadastrada = empresas.cadastrar_empresa(
            razao_social=razao_social,
            nome_fantasia=nome_fantasia,
            cnpj=cnpj,
            email=email,
            telefone=telefone,
        )

    except (TypeError, ValueError) as erro:
        print(
            f"\nNão foi possível cadastrar a empresa: {erro}"
        )

        _pressionar_enter_para_continuar()
        return

    print(
        "\nEmpresa cadastrada com sucesso."
    )

    _exibir_empresa(
        empresa_cadastrada,
    )

    _pressionar_enter_para_continuar()


# ============================================================
# LISTAGEM
# ============================================================

def listar_empresas_interface() -> None:
    """
    Exibe as empresas cadastradas.
    """

    _exibir_titulo(
        "LISTAGEM DE EMPRESAS"
    )

    lista_empresas = empresas.listar_empresas(
        ordenar_por_nome=True,
    )

    if not lista_empresas:
        print(
            "\nNenhuma empresa cadastrada."
        )

        _pressionar_enter_para_continuar()
        return

    print()

    for empresa in lista_empresas:
        _exibir_empresa_resumida(
            empresa,
        )

    print(
        f"\nTotal de empresas: {len(lista_empresas)}"
    )

    _pressionar_enter_para_continuar()


# ============================================================
# CONSULTA
# ============================================================

def consultar_empresa_interface() -> None:
    """
    Consulta uma empresa pelo código.
    """

    _exibir_titulo(
        "CONSULTA DE EMPRESA"
    )

    empresa_encontrada = _selecionar_empresa()

    if empresa_encontrada is not None:
        _exibir_empresa(
            empresa_encontrada,
        )

    _pressionar_enter_para_continuar()


# ============================================================
# EDIÇÃO
# ============================================================

def editar_empresa_interface() -> None:
    """
    Edita os dados cadastrais permitidos.
    """

    _exibir_titulo(
        "EDIÇÃO DE EMPRESA"
    )

    empresa_encontrada = _selecionar_empresa()

    if empresa_encontrada is None:
        _pressionar_enter_para_continuar()
        return

    _exibir_empresa(
        empresa_encontrada,
    )

    print()
    print(
        "Pressione Enter para preservar o valor atual."
    )

    razao_social = _ler_campo_opcional(
        "Nova razão social",
        empresa_encontrada["razao_social"],
    )

    nome_fantasia = _ler_campo_opcional(
        "Novo nome fantasia",
        empresa_encontrada["nome_fantasia"],
    )

    email = _ler_campo_opcional(
        "Novo e-mail",
        empresa_encontrada["email"],
    )

    telefone = _ler_campo_opcional(
        "Novo telefone",
        _formatar_telefone(
            empresa_encontrada["telefone"]
        ),
    )

    try:
        empresa_atualizada = empresas.editar_empresa(
            codigo_empresa=empresa_encontrada["codigo"],
            razao_social=razao_social,
            nome_fantasia=nome_fantasia,
            email=email,
            telefone=telefone,
        )

    except (TypeError, ValueError) as erro:
        print(
            f"\nNão foi possível editar a empresa: {erro}"
        )

        _pressionar_enter_para_continuar()
        return

    print(
        "\nEmpresa atualizada com sucesso."
    )

    _exibir_empresa(
        empresa_atualizada,
    )

    _pressionar_enter_para_continuar()


# ============================================================
# ALTERAÇÃO DE SITUAÇÃO
# ============================================================

def alterar_situacao_empresa_interface() -> None:
    """
    Exibe e executa as transições disponíveis.
    """

    _exibir_titulo(
        "ALTERAÇÃO DA SITUAÇÃO DA EMPRESA"
    )

    empresa_encontrada = _selecionar_empresa()

    if empresa_encontrada is None:
        _pressionar_enter_para_continuar()
        return

    print(
        f"\nEmpresa: {empresa_encontrada['nome_fantasia']}"
    )

    print(
        f"Situação atual: {empresa_encontrada['situacao']}"
    )

    try:
        transicoes = empresas.listar_transicoes_permitidas(
            empresa_encontrada["codigo"],
        )

    except (TypeError, ValueError) as erro:
        print(
            f"\nNão foi possível consultar as transições: {erro}"
        )

        _pressionar_enter_para_continuar()
        return

    if not transicoes:
        print(
            "\nEsta empresa não possui transições disponíveis."
        )

        _pressionar_enter_para_continuar()
        return

    print(
        "\nSituações disponíveis:"
    )

    for indice, situacao in enumerate(
        transicoes,
        start=1,
    ):
        print(
            f"{indice}. {situacao}"
        )

    print(
        "0. Cancelar operação"
    )

    opcao = ler_int(
        "\nEscolha a nova situação: "
    )

    if opcao == 0:
        print(
            "\nOperação cancelada."
        )

        _pressionar_enter_para_continuar()
        return

    if opcao < 1 or opcao > len(transicoes):
        print(
            "\nOpção inválida."
        )

        _pressionar_enter_para_continuar()
        return

    nova_situacao = transicoes[
        opcao - 1
    ]

    try:
        empresa_alterada = (
            _executar_alteracao_situacao(
                codigo_empresa=empresa_encontrada["codigo"],
                nova_situacao=nova_situacao,
            )
        )

    except (TypeError, ValueError) as erro:
        print(
            "\nNão foi possível alterar a situação: "
            f"{erro}"
        )

        _pressionar_enter_para_continuar()
        return

    print(
        "\nSituação alterada com sucesso."
    )

    _exibir_empresa(
        empresa_alterada,
    )

    _pressionar_enter_para_continuar()


def _executar_alteracao_situacao(
    codigo_empresa: int,
    nova_situacao: str,
) -> dict[str, Any]:
    """
    Encaminha a situação escolhida para a função correspondente
    da fachada.
    """

    operacoes = {
        "ATIVA": empresas.ativar_empresa,
        "INATIVA": empresas.inativar_empresa,
        "SUSPENSA": empresas.suspender_empresa,
        "CANCELADA": empresas.cancelar_empresa,
    }

    operacao = operacoes.get(
        nova_situacao,
    )

    if operacao is None:
        raise ValueError(
            "Não existe uma operação para a situação informada."
        )

    return operacao(
        codigo_empresa,
    )


# ============================================================
# MENU DE EMPRESAS
# ============================================================

def menu_empresas() -> None:
    """
    Exibe o menu de Empresas até o usuário escolher voltar.
    """

    while True:
        _exibir_titulo(
            "EMPRESAS"
        )

        print(
            "1. Cadastrar empresa"
        )
        print(
            "2. Listar empresas"
        )
        print(
            "3. Consultar empresa"
        )
        print(
            "4. Editar empresa"
        )
        print(
            "5. Alterar situação"
        )
        print(
            "0. Voltar"
        )

        opcao = ler_int(
            "\nEscolha uma opção: "
        )

        if opcao == 1:
            cadastrar_empresa_interface()

        elif opcao == 2:
            listar_empresas_interface()

        elif opcao == 3:
            consultar_empresa_interface()

        elif opcao == 4:
            editar_empresa_interface()

        elif opcao == 5:
            alterar_situacao_empresa_interface()

        elif opcao == 0:
            break

        else:
            print(
                "\nOpção inválida."
            )

            _pressionar_enter_para_continuar()