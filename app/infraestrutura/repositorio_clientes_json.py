"""
Repositório JSON de Clientes.

Este módulo pertence à camada de infraestrutura.

Sua responsabilidade é carregar e salvar os dados dos Clientes,
sem conhecer regras de negócio, menus, input() ou print().
"""

from app import dados


ARQUIVO_CLIENTES = "clientes.json"


def carregar_clientes():
    """
    Carrega os Clientes armazenados no arquivo JSON.

    Retorna:
        Uma lista contendo os Clientes cadastrados.
    """

    return dados.carregar_dados(ARQUIVO_CLIENTES)


def salvar_clientes(clientes):
    """
    Salva a coleção atual de Clientes no arquivo JSON.

    Parâmetros:
        clientes:
            Lista contendo os Clientes que serão persistidos.
    """

    dados.salvar_dados(
        ARQUIVO_CLIENTES,
        clientes,
    )