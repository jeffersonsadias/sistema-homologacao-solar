"""
Interface de terminal para Projetos.

Este módulo pertence à camada de interface.

Responsabilidades:
- receber dados pelo terminal;
- exibir informações;
- coordenar chamadas ao domínio;
- solicitar persistência após alterações.

Este módulo não mantém uma lista global própria de Projetos.
A coleção de Projetos é recebida por parâmetro.
"""

from app import clientes
from app import concessionarias
from app import empresas
from app import status
from app import utils

from app.dominio.projetos import (
    buscar_projeto_por_codigo,
    criar_dados_projeto,
)

from app.infraestrutura.repositorio_projetos_json import (
    salvar_projetos,
)

def _selecionar_empresa_projeto():
    """
    Solicita a Empresa responsável
    pelo novo Projeto.

    Somente uma Empresa existente e ativa
    pode originar um Projeto manual.
    """

    codigo_empresa = utils.ler_int(
        "Código da Empresa responsável: "
    )

    try:
        empresa = empresas.obter_empresa(
            codigo_empresa
        )

    except ValueError as erro:
        print(
            f"\nNão foi possível selecionar "
            f"a Empresa: {erro}"
        )

        return None

    if not empresas.empresa_esta_ativa(
        codigo_empresa
    ):
        print(
            "\nNão é possível criar um Projeto "
            "para uma Empresa inativa."
        )

        return None

    return empresa

def _selecionar_concessionaria_projeto():
    """
    Solicita a Concessionária responsável
    pelo novo Projeto.

    Somente uma Concessionária cadastrada
    pode ser vinculada ao Projeto.
    """

    codigo_concessionaria = utils.ler_int(
        "Código da Concessionária: "
    )

    try:
        concessionaria = (
            concessionarias
            .obter_concessionaria(
                codigo_concessionaria
            )
        )

    except ValueError as erro:
        print(
            "\nNão foi possível selecionar "
            f"a Concessionária: {erro}"
        )

        return None

    return concessionaria

def cadastrar_projeto(lista_projetos):
    """
    Cadastra um novo Projeto.

    Parâmetros:
        lista_projetos:
            Lista atual de Projetos mantida pela fachada.
    """

    print("\n=== Cadastro de Projeto ===")

    empresa = _selecionar_empresa_projeto()

    if empresa is None:
        return None

    cliente = clientes.selecionar_cliente()

    if cliente is None:
        print("\nCadastre o cliente antes de criar o projeto.")
        return None

    concessionaria = (
        _selecionar_concessionaria_projeto()
    )

    if concessionaria is None:
        return None

    codigo = utils.gerar_proximo_codigo(lista_projetos)

    potencia = utils.ler_float(
        "Potência do sistema (kWp): "
    )

    projeto = criar_dados_projeto(
        codigo=codigo,
        codigo_empresa=empresa["codigo"],
        codigo_concessionaria=concessionaria.codigo,
        codigo_cliente=cliente["codigo"],
        distribuidora=concessionaria.nome,
        potencia=potencia,
        status_inicial=status.STATUS_INICIAL,
    )

    lista_projetos.append(projeto)

    salvar_projetos(lista_projetos)

    print("\nProjeto cadastrado com sucesso!")

    return projeto

def listar_projetos(lista_projetos):
    """
    Lista todos os Projetos cadastrados.
    """

    print("\n=== Projetos Cadastrados ===")

    if not lista_projetos:
        print("Nenhum projeto cadastrado.")
        return None

    for projeto in lista_projetos:
        mostrar_projeto(projeto)

    return None

def mostrar_projeto(projeto):
    """
    Exibe os dados de um Projeto específico.
    """

    cliente = clientes.buscar_cliente(
        projeto["cliente"]
    )

    print("----------------------------")
    print(f"Código: {projeto['codigo']}")

    if cliente:
        print(f"Cliente: {cliente['nome']}")
    else:
        print("Cliente: Não encontrado")

    print(
        f"Distribuidora: "
        f"{projeto['distribuidora']}"
    )

    print(
        f"Potência: "
        f"{projeto['potencia']} kWp"
    )

    print(
        f"Status: "
        f"{projeto['status']}"
    )

    return None

def alterar_status(lista_projetos):
    """
    Altera o status de um Projeto existente,
    respeitando as transições permitidas.
    """

    print("\n=== Alterar Status do Projeto ===")

    codigo = utils.ler_int(
        "Digite o código do projeto: "
    )

    projeto = buscar_projeto_por_codigo(
        lista_projetos,
        codigo,
    )

    if projeto is None:
        print("\nProjeto não encontrado.")
        return None

    print("\nProjeto selecionado:")

    mostrar_projeto(projeto)

    status.exibir_status()

    codigo_status = utils.ler_int(
        "\nDigite o código do novo status: "
    )

    novo_status = status.obter_status(
        codigo_status
    )

    if novo_status is None:
        print("\nStatus inválido.")
        return None

    status_atual = projeto["status"]

    if not status.transicao_permitida(
        status_atual,
        novo_status,
    ):
        print("\nTransição de status não permitida.")
        print(f"Status atual: {status_atual}")
        print(f"Status solicitado: {novo_status}")

        return None

    projeto["status"] = novo_status

    salvar_projetos(lista_projetos)

    print("\nStatus alterado com sucesso!")
    print(f"Novo status: {novo_status}")

    return projeto