"""
Interface de terminal para Clientes.

Este módulo é responsável por:

- receber dados com input();
- exibir informações com print();
- conduzir os fluxos de cadastro, consulta e seleção.

As regras de negócio pertencem ao domínio.
A persistência pertence à infraestrutura.
"""

from app import utils
from app.dominio.clientes import (
    buscar_cliente_por_codigo,
    buscar_clientes_por_nome,
    ordenar_clientes_por_nome,
)
from app.infraestrutura.repositorio_clientes_json import (
    carregar_clientes,
    salvar_clientes,
)


clientes = carregar_clientes()


def cadastrar_cliente():
    """
    Cadastra um novo Cliente e salva a coleção atualizada.
    """

    print("\n=== Cadastro de Cliente ===")

    codigo = utils.gerar_proximo_codigo(clientes)

    nome = input("Nome do cliente: ")
    cidade = input("Cidade: ")
    telefone = input("Telefone: ")

    cliente = {
        "codigo": codigo,
        "nome": nome,
        "cidade": cidade,
        "telefone": telefone,
    }

    clientes.append(cliente)

    salvar_clientes(clientes)

    print("\nCliente cadastrado com sucesso!")


def listar_clientes():
    """
    Lista todos os Clientes em ordem alfabética.
    """

    print("\n=== Clientes Cadastrados ===")

    if not clientes:
        print("Nenhum cliente cadastrado.")
        return

    clientes_ordenados = ordenar_clientes_por_nome(clientes)

    for cliente in clientes_ordenados:
        print("----------------------------")
        print(f"Código: {cliente['codigo']}")
        print(f"Nome: {cliente['nome']}")
        print(f"Cidade: {cliente['cidade']}")
        print(f"Telefone: {cliente['telefone']}")


def listar_clientes_resumido():
    """
    Lista os Clientes de forma resumida.
    """

    print("\n=== Clientes Cadastrados ===")

    if not clientes:
        print("Nenhum cliente cadastrado.")
        return

    clientes_ordenados = ordenar_clientes_por_nome(clientes)

    for cliente in clientes_ordenados:
        print(f"{cliente['codigo']} - {cliente['nome']}")


def selecionar_cliente():
    """
    Exibe os Clientes, solicita um código e retorna o encontrado.
    """

    listar_clientes_resumido()

    codigo_cliente = int(input("\nCódigo do cliente: "))

    cliente = buscar_cliente(codigo_cliente)

    if cliente is None:
        print("\nCliente não encontrado.")
        return None

    return cliente


def buscar_cliente(codigo):
    """
    Busca um Cliente pelo código na coleção carregada.
    """

    return buscar_cliente_por_codigo(
        clientes,
        codigo,
    )


def buscar_clientes_por_nome_interface(nome_busca):
    """
    Busca Clientes por nome na coleção carregada.

    O nome desta função evita conflito com a função importada
    do domínio.
    """

    return buscar_clientes_por_nome(
        clientes,
        nome_busca,
    )


def consultar_clientes_por_nome():
    """
    Solicita um nome e exibe os Clientes encontrados.
    """

    print("\n=== Buscar Cliente por Nome ===")

    nome_busca = input("Digite o nome ou parte do nome: ")

    clientes_encontrados = (
        buscar_clientes_por_nome_interface(nome_busca)
    )

    if not clientes_encontrados:
        print("\nNenhum cliente encontrado.")
        return

    print(
        f"\nForam encontrados "
        f"{len(clientes_encontrados)} cliente(s):"
    )

    for cliente in clientes_encontrados:
        print("----------------------------")
        print(f"Código: {cliente['codigo']}")
        print(f"Nome: {cliente['nome']}")
        print(f"Cidade: {cliente['cidade']}")
        print(f"Telefone: {cliente['telefone']}")