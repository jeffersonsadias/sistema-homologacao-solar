"""
Interface de terminal para Usuários.

Este módulo é responsável por:

- solicitar dados com input();
- exibir informações com print();
- apresentar menus;
- converter escolhas do usuário;
- chamar funções públicas das fachadas.

A interface não deve:

- acessar diretamente a coleção usuarios;
- acessar diretamente arquivos JSON;
- aplicar regras de negócio;
- criar dicionários de Usuário manualmente;
- importar funções internas do domínio.

Fluxo arquitetural:

Interface
    ↓
Fachada
    ↓
Domínio
    ↓
Infraestrutura
"""

from typing import Any

from app import empresas
from app import usuarios


# ============================================================
# FUNÇÕES AUXILIARES DE LEITURA
# ============================================================

def _ler_codigo(
    mensagem: str,
) -> int:
    """
    Solicita um código numérico inteiro e positivo.

    A função permanece solicitando o valor enquanto
    a entrada não for válida.
    """

    while True:
        entrada = input(
            mensagem
        ).strip()

        try:
            codigo = int(
                entrada
            )
        except ValueError:
            print(
                "\nDigite um número inteiro válido."
            )
            continue

        if codigo <= 0:
            print(
                "\nO código deve ser maior que zero."
            )
            continue

        return codigo


def _ler_texto_obrigatorio(
    mensagem: str,
) -> str:
    """
    Solicita um texto obrigatório.

    A interface impede somente uma entrada vazia.
    As demais validações pertencem ao domínio.
    """

    while True:
        texto = input(
            mensagem
        ).strip()

        if texto:
            return texto

        print(
            "\nEste campo é obrigatório."
        )


def _pausar() -> None:
    """
    Aguarda confirmação antes de retornar ao menu.
    """

    input(
        "\nPressione Enter para continuar..."
    )


# ============================================================
# EXIBIÇÃO DE USUÁRIO
# ============================================================

def _exibir_usuario(
    usuario: dict[str, Any],
) -> None:
    """
    Exibe os dados de um único Usuário.

    A função recebe o Usuário já localizado
    pela fachada.
    """

    print(
        "\n"
        "----------------------------------------"
    )

    print(
        f"Código: {usuario.get('codigo', '-')}"
    )

    print(
        f"Código da Empresa: "
        f"{usuario.get('codigo_empresa', '-')}"
    )

    print(
        f"Nome: {usuario.get('nome', '-')}"
    )

    print(
        f"E-mail: {usuario.get('email', '-')}"
    )

    print(
        f"Perfil: {usuario.get('perfil', '-')}"
    )

    print(
        f"Situação: {usuario.get('situacao', '-')}"
    )

    print(
        f"Data de cadastro: "
        f"{usuario.get('data_cadastro', '-')}"
    )

    print(
        f"Data de atualização: "
        f"{usuario.get('data_atualizacao', '-')}"
    )

    print(
        "----------------------------------------"
    )


def _exibir_lista_usuarios(
    lista_usuarios: list[dict[str, Any]],
) -> None:
    """
    Exibe uma coleção de Usuários.

    Quando a lista estiver vazia,
    apresenta uma mensagem apropriada.
    """

    if not lista_usuarios:
        print(
            "\nNenhum Usuário encontrado."
        )
        return

    print(
        f"\nQuantidade de Usuários: "
        f"{len(lista_usuarios)}"
    )

    for usuario in lista_usuarios:
        _exibir_usuario(
            usuario
        )


# ============================================================
# SELEÇÃO DA EMPRESA
# ============================================================

def _selecionar_empresa() -> dict[str, Any]:
    """
    Solicita o código de uma Empresa existente.

    A localização é delegada à fachada de Empresas.
    """

    codigo_empresa = _ler_codigo(
        "Código da Empresa: "
    )

    return empresas.obter_empresa(
        codigo_empresa
    )


def _exibir_empresa_selecionada(
    empresa: dict[str, Any],
) -> None:
    """
    Exibe uma identificação resumida da Empresa.
    """

    print(
        "\nEmpresa selecionada:"
    )

    print(
        f"Código: {empresa.get('codigo', '-')}"
    )

    print(
        f"Nome fantasia: "
        f"{empresa.get('nome_fantasia', '-')}"
    )

    print(
        f"Situação: {empresa.get('situacao', '-')}"
    )


# ============================================================
# SELEÇÃO DE PERFIL
# ============================================================

def _selecionar_perfil() -> str:
    """
    Exibe os perfis oficiais e retorna
    o perfil selecionado.

    A interface obtém os perfis pela fachada
    de Usuários, sem acessar diretamente o domínio.
    """

    perfis = usuarios.obter_perfis_usuario()

    while True:
        print(
            "\nPerfis disponíveis:"
        )

        for indice, perfil in enumerate(
            perfis,
            start=1,
        ):
            print(
                f"{indice} - {perfil}"
            )

        opcao = input(
            "\nEscolha o perfil: "
        ).strip()

        try:
            indice_escolhido = int(
                opcao
            )
        except ValueError:
            print(
                "\nDigite o número correspondente "
                "ao perfil."
            )
            continue

        if not 1 <= indice_escolhido <= len(perfis):
            print(
                "\nOpção de perfil inválida."
            )
            continue

        return perfis[
            indice_escolhido - 1
        ]


# ============================================================
# CADASTRO
# ============================================================

def cadastrar_usuario_interface() -> None:
    """
    Coordena o cadastro de um novo Usuário.

    A interface:

    1. solicita a Empresa;
    2. apresenta a Empresa selecionada;
    3. solicita os dados do Usuário;
    4. seleciona o perfil;
    5. chama a fachada;
    6. apresenta o resultado.
    """

    print(
        "\n"
        "========================================"
    )
    print(
        "CADASTRO DE USUÁRIO"
    )
    print(
        "========================================"
    )

    try:
        empresa = _selecionar_empresa()

        _exibir_empresa_selecionada(
            empresa
        )

        nome = _ler_texto_obrigatorio(
            "\nNome do Usuário: "
        )

        email = _ler_texto_obrigatorio(
            "E-mail do Usuário: "
        )

        perfil = _selecionar_perfil()

        novo_usuario = usuarios.cadastrar_usuario(
            codigo_empresa=empresa["codigo"],
            nome=nome,
            email=email,
            perfil=perfil,
        )

    except ValueError as erro:
        print(
            f"\nNão foi possível cadastrar "
            f"o Usuário: {erro}"
        )
        return

    print(
        "\nUsuário cadastrado com sucesso."
    )

    _exibir_usuario(
        novo_usuario
    )


# ============================================================
# BUSCA POR CÓDIGO
# ============================================================

def buscar_usuario_interface() -> None:
    """
    Busca um Usuário pelo código dentro
    do contexto de uma Empresa.
    """

    print(
        "\n"
        "========================================"
    )
    print(
        "BUSCAR USUÁRIO"
    )
    print(
        "========================================"
    )

    try:
        empresa = _selecionar_empresa()

        _exibir_empresa_selecionada(
            empresa
        )

        codigo_usuario = _ler_codigo(
            "\nCódigo do Usuário: "
        )

        usuario_encontrado = usuarios.obter_usuario(
            codigo_usuario=codigo_usuario,
            codigo_empresa=empresa["codigo"],
        )

    except ValueError as erro:
        print(
            f"\nNão foi possível realizar "
            f"a busca: {erro}"
        )
        return

    if usuario_encontrado is None:
        print(
            "\nUsuário não encontrado nesta Empresa."
        )
        return

    _exibir_usuario(
        usuario_encontrado
    )


# ============================================================
# BUSCA POR E-MAIL
# ============================================================

def buscar_usuario_por_email_interface() -> None:
    """
    Busca um Usuário pelo e-mail.

    Como o e-mail é único globalmente,
    a consulta não exige o código da Empresa.
    """

    print(
        "\n"
        "========================================"
    )
    print(
        "BUSCAR USUÁRIO POR E-MAIL"
    )
    print(
        "========================================"
    )

    email = _ler_texto_obrigatorio(
        "E-mail do Usuário: "
    )

    try:
        usuario_encontrado = (
            usuarios.buscar_usuario_por_email(
                email
            )
        )
    except ValueError as erro:
        print(
            f"\nNão foi possível realizar "
            f"a busca: {erro}"
        )
        return

    if usuario_encontrado is None:
        print(
            "\nNenhum Usuário foi encontrado "
            "com esse e-mail."
        )
        return

    _exibir_usuario(
        usuario_encontrado
    )


# ============================================================
# LISTAGENS
# ============================================================

def listar_usuarios_interface() -> None:
    """
    Lista todos os Usuários de uma Empresa.
    """

    print(
        "\n"
        "========================================"
    )
    print(
        "LISTAR USUÁRIOS"
    )
    print(
        "========================================"
    )

    try:
        empresa = _selecionar_empresa()

        _exibir_empresa_selecionada(
            empresa
        )

        lista_usuarios = usuarios.listar_usuarios(
            codigo_empresa=empresa["codigo"]
        )

    except ValueError as erro:
        print(
            f"\nNão foi possível listar "
            f"os Usuários: {erro}"
        )
        return

    _exibir_lista_usuarios(
        lista_usuarios
    )


def listar_usuarios_ativos_interface() -> None:
    """
    Lista somente os Usuários ativos
    de uma Empresa.
    """

    print(
        "\n"
        "========================================"
    )
    print(
        "USUÁRIOS ATIVOS"
    )
    print(
        "========================================"
    )

    try:
        empresa = _selecionar_empresa()

        _exibir_empresa_selecionada(
            empresa
        )

        lista_usuarios = (
            usuarios.listar_usuarios_ativos(
                codigo_empresa=empresa["codigo"]
            )
        )

    except ValueError as erro:
        print(
            f"\nNão foi possível listar "
            f"os Usuários ativos: {erro}"
        )
        return

    _exibir_lista_usuarios(
        lista_usuarios
    )


def listar_usuarios_por_perfil_interface() -> None:
    """
    Lista os Usuários de uma Empresa
    que possuem determinado perfil.
    """

    print(
        "\n"
        "========================================"
    )
    print(
        "USUÁRIOS POR PERFIL"
    )
    print(
        "========================================"
    )

    try:
        empresa = _selecionar_empresa()

        _exibir_empresa_selecionada(
            empresa
        )

        perfil = _selecionar_perfil()

        lista_usuarios = (
            usuarios.listar_usuarios_por_perfil(
                codigo_empresa=empresa["codigo"],
                perfil=perfil,
            )
        )

    except ValueError as erro:
        print(
            f"\nNão foi possível listar "
            f"os Usuários: {erro}"
        )
        return

    print(
        f"\nPerfil selecionado: {perfil}"
    )

    _exibir_lista_usuarios(
        lista_usuarios
    )


# ============================================================
# QUANTIDADE DE USUÁRIOS
# ============================================================

def mostrar_quantidade_usuarios_interface() -> None:
    """
    Exibe a quantidade de Usuários
    vinculados a uma Empresa.
    """

    print(
        "\n"
        "========================================"
    )
    print(
        "QUANTIDADE DE USUÁRIOS"
    )
    print(
        "========================================"
    )

    try:
        empresa = _selecionar_empresa()

        _exibir_empresa_selecionada(
            empresa
        )

        quantidade = usuarios.quantidade_usuarios(
            codigo_empresa=empresa["codigo"]
        )

    except ValueError as erro:
        print(
            f"\nNão foi possível consultar "
            f"a quantidade: {erro}"
        )
        return

    print(
        f"\nA Empresa possui "
        f"{quantidade} Usuário(s) cadastrado(s)."
    )

def _alterar_situacao_usuario_interface(
    operacao: str,
) -> None:
    """
    Coordena uma alteração de situação
    de Usuário pela interface.

    A operação recebida deve ser uma destas:

    - ATIVAR
    - INATIVAR
    - BLOQUEAR
    - CANCELAR
    """

    print(
        "\n"
        "========================================"
    )

    print(
        f"{operacao} USUÁRIO"
    )

    print(
        "========================================"
    )

    try:
        empresa = _selecionar_empresa()

        _exibir_empresa_selecionada(
            empresa
        )

        codigo_usuario = _ler_codigo(
            "\nCódigo do Usuário: "
        )

        if operacao == "ATIVAR":
            usuario_atualizado = (
                usuarios.ativar_usuario(
                    codigo_empresa=empresa["codigo"],
                    codigo_usuario=codigo_usuario,
                )
            )

        elif operacao == "INATIVAR":
            usuario_atualizado = (
                usuarios.inativar_usuario(
                    codigo_empresa=empresa["codigo"],
                    codigo_usuario=codigo_usuario,
                )
            )

        elif operacao == "BLOQUEAR":
            usuario_atualizado = (
                usuarios.bloquear_usuario(
                    codigo_empresa=empresa["codigo"],
                    codigo_usuario=codigo_usuario,
                )
            )

        elif operacao == "CANCELAR":
            usuario_atualizado = (
                usuarios.cancelar_usuario(
                    codigo_empresa=empresa["codigo"],
                    codigo_usuario=codigo_usuario,
                )
            )

        else:
            raise ValueError(
                "Operação de situação inválida."
            )

    except ValueError as erro:
        print(
            f"\nNão foi possível {operacao.lower()} "
            f"o Usuário: {erro}"
        )

        return

    print(
        f"\nUsuário alterado com sucesso."
    )

    _exibir_usuario(
        usuario_atualizado
    )

def ativar_usuario_interface() -> None:
    """
    Abre o fluxo de ativação de Usuário.
    """

    _alterar_situacao_usuario_interface(
        "ATIVAR"
    )


def inativar_usuario_interface() -> None:
    """
    Abre o fluxo de inativação de Usuário.
    """

    _alterar_situacao_usuario_interface(
        "INATIVAR"
    )


def bloquear_usuario_interface() -> None:
    """
    Abre o fluxo de bloqueio de Usuário.
    """

    _alterar_situacao_usuario_interface(
        "BLOQUEAR"
    )


def cancelar_usuario_interface() -> None:
    """
    Abre o fluxo de cancelamento de Usuário.
    """

    _alterar_situacao_usuario_interface(
        "CANCELAR"
    )

# ============================================================
# MENU DE USUÁRIOS
# ============================================================

def menu_usuarios() -> None:
    """
    Exibe o menu de gerenciamento de Usuários.

    O menu permanece em execução até que
    o usuário escolha retornar ao menu anterior.
    """

    while True:
        print(
            "\n"
            "========================================"
        )

        print(
            "GERENCIAMENTO DE USUÁRIOS"
        )

        print(
            "========================================"
        )

        print(
            "1 - Cadastrar Usuário"
        )

        print(
            "2 - Buscar Usuário por código"
        )

        print(
            "3 - Buscar Usuário por e-mail"
        )

        print(
            "4 - Listar todos os Usuários"
        )

        print(
            "5 - Listar Usuários ativos"
        )

        print(
            "6 - Listar Usuários por perfil"
        )

        print(
            "7 - Mostrar quantidade de Usuários"
        )

        print(
            "8 - Ativar Usuário"
        )

        print(
            "9 - Inativar Usuário"
        )

        print(
            "10 - Bloquear Usuário"
        )

        print(
            "11 - Cancelar Usuário"
        )

        print(
            "0 - Voltar"
        )

        opcao = input(
            "\nEscolha uma opção: "
        ).strip()

        if opcao == "1":
            cadastrar_usuario_interface()
            _pausar()

        elif opcao == "2":
            buscar_usuario_interface()
            _pausar()

        elif opcao == "3":
            buscar_usuario_por_email_interface()
            _pausar()

        elif opcao == "4":
            listar_usuarios_interface()
            _pausar()

        elif opcao == "5":
            listar_usuarios_ativos_interface()
            _pausar()

        elif opcao == "6":
            listar_usuarios_por_perfil_interface()
            _pausar()

        elif opcao == "7":
            mostrar_quantidade_usuarios_interface()
            _pausar()

        elif opcao == "8":
            ativar_usuario_interface()
            _pausar()

        elif opcao == "9":
            inativar_usuario_interface()
            _pausar()

        elif opcao == "10":
            bloquear_usuario_interface()
            _pausar()

        elif opcao == "11":
            cancelar_usuario_interface()
            _pausar()

        elif opcao == "0":
            return

        else:
            print(
                "\nOpção inválida."
            )