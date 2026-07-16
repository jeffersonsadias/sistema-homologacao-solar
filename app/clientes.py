from . import dados
from . import utils

# Lista que armazenará todos os clientes cadastrados
#clientes = [] - foi substituido por função que chama os "clientes" salvos.
clientes = dados.carregar_dados("clientes.json")

def cadastrar_cliente():
    """
    Cadastra um novo cliente na lista.
    """

    print("\n=== Cadastro de Cliente ===")

    # Código automático
    codigo = utils.gerar_proximo_codigo(clientes)

    nome = input("Nome do cliente: ")
    cidade = input("Cidade: ")
    telefone = input("Telefone: ")

    # Cria um dicionário contendo todas as informações
    cliente = {

        "codigo": codigo,
        "nome": nome,
        "cidade": cidade,
        "telefone": telefone

    }

    # Adiciona o dicionário dentro da lista e salva versão atual
    clientes.append(cliente)

    dados.salvar_dados("clientes.json", clientes)

    print("\nCliente cadastrado com sucesso!")


def listar_clientes():
    """
    Lista todos os clientes cadastrados em ordem alfabética.
    """

    print("\n=== Clientes Cadastrados ===")

    if not clientes:
        print("Nenhum cliente cadastrado.")
        return

    clientes_ordenados = sorted(
        clientes,
        key=lambda cliente: cliente["nome"].lower()
    )

    for cliente in clientes_ordenados:
        print("----------------------------")
        print(f"Código: {cliente['codigo']}")
        print(f"Nome: {cliente['nome']}")
        print(f"Cidade: {cliente['cidade']}")
        print(f"Telefone: {cliente['telefone']}")

def listar_clientes_resumido():
    """
    Lista os clientes de forma resumida e em ordem alfabética.
    """

    print("\n=== Clientes Cadastrados ===")

    if not clientes:
        print("Nenhum cliente cadastrado.")
        return

    clientes_ordenados = sorted(
        clientes,
        key=lambda cliente: cliente["nome"].lower()
    )

    for cliente in clientes_ordenados:
        print(f"{cliente['codigo']} - {cliente['nome']}")

def selecionar_cliente():
    """
    Exibe os clientes cadastrados, solicita um código
    e retorna o cliente encontrado.
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
    Busca um cliente pelo código.
    Retorna o cliente encontrado ou None.
    """

    for cliente in clientes:

        if cliente["codigo"] == codigo:
            return cliente

    return None

def buscar_clientes_por_nome(nome_busca):
    """
    Busca clientes pelo nome ou por parte do nome.
    Retorna uma lista com todos os clientes encontrados.
    """

    nome_busca = nome_busca.strip().lower()

    clientes_encontrados = []

    for cliente in clientes:

        nome_cliente = cliente["nome"].lower()

        if nome_busca in nome_cliente:
            clientes_encontrados.append(cliente)

    clientes_encontrados = sorted(
        clientes_encontrados,
        key=lambda cliente: cliente["nome"].lower()
    )

    return clientes_encontrados

def consultar_clientes_por_nome():
    """
    Solicita um nome ao usuário e exibe os clientes encontrados.
    """

    print("\n=== Buscar Cliente por Nome ===")

    nome_busca = input("Digite o nome ou parte do nome: ")

    clientes_encontrados = buscar_clientes_por_nome(nome_busca)

    if not clientes_encontrados:
        print("\nNenhum cliente encontrado.")
        return

    print(f"\nForam encontrados {len(clientes_encontrados)} cliente(s):")

    for cliente in clientes_encontrados:
        print("----------------------------")
        print(f"Código: {cliente['codigo']}")
        print(f"Nome: {cliente['nome']}")
        print(f"Cidade: {cliente['cidade']}")
        print(f"Telefone: {cliente['telefone']}")

