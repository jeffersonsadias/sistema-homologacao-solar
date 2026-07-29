"""
Regras de domínio relacionadas aos Clientes.

Este módulo não realiza entrada de dados com input(),
não exibe informações com print() e não acessa arquivos.

Ele recebe coleções de clientes, aplica regras puras
e devolve os resultados.
"""


def buscar_cliente_por_codigo(clientes, codigo):
    """
    Busca um cliente pelo código informado.

    Parâmetros:
        clientes:
            Lista contendo os clientes cadastrados.

        codigo:
            Código do cliente que será procurado.

    Retorno:
        O dicionário do cliente encontrado ou None.
    """

    for cliente in clientes:
        if cliente["codigo"] == codigo:
            return cliente

    return None


def codigo_cliente_existe(clientes, codigo):
    """
    Verifica se já existe um cliente com o código informado.

    Retorna True quando o código existe.
    Retorna False quando o código não existe.
    """

    return buscar_cliente_por_codigo(clientes, codigo) is not None


def ordenar_clientes_por_nome(clientes):
    """
    Retorna uma nova lista de clientes em ordem alfabética.

    A lista original não é modificada.
    """

    return sorted(
        clientes,
        key=lambda cliente: cliente["nome"].casefold(),
    )


def buscar_clientes_por_nome(clientes, nome_busca):
    """
    Busca clientes pelo nome completo ou por parte do nome.

    A busca não diferencia letras maiúsculas de minúsculas.

    Exemplos:
        "ana" encontra "Ana Souza"
        "SILVA" encontra "Carlos Silva"

    Retorna uma lista ordenada alfabeticamente.
    """

    nome_normalizado = nome_busca.strip().casefold()

    clientes_encontrados = []

    for cliente in clientes:
        nome_cliente = cliente["nome"].casefold()

        if nome_normalizado in nome_cliente:
            clientes_encontrados.append(cliente)

    return ordenar_clientes_por_nome(clientes_encontrados)