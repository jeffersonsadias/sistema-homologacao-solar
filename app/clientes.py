"""
Fachada de compatibilidade do módulo de Clientes.

Este módulo preserva os imports e comportamentos utilizados
pelos módulos e testes criados durante a Sprint 1.

A interface real está localizada em:

    app.interface.clientes_interface

As regras puras estão localizadas em:

    app.dominio.clientes
"""

from app.dominio.clientes import (
    buscar_cliente_por_codigo,
    buscar_clientes_por_nome as buscar_clientes_no_dominio,
)

from app.interface import clientes_interface


# Mantém disponível a coleção pública usada pelo código legado
# e pelos testes da Sprint 1.
clientes = clientes_interface.clientes


def cadastrar_cliente():
    """
    Encaminha o cadastro para a interface de terminal.
    """

    return clientes_interface.cadastrar_cliente()


def listar_clientes():
    """
    Encaminha a listagem completa para a interface de terminal.
    """

    return clientes_interface.listar_clientes()


def listar_clientes_resumido():
    """
    Encaminha a listagem resumida para a interface de terminal.
    """

    return clientes_interface.listar_clientes_resumido()


def selecionar_cliente():
    """
    Encaminha a seleção para a interface de terminal.
    """

    return clientes_interface.selecionar_cliente()


def consultar_clientes_por_nome():
    """
    Encaminha a consulta interativa para a interface de terminal.
    """

    return clientes_interface.consultar_clientes_por_nome()


def buscar_cliente(codigo):
    """
    Busca um Cliente pelo código.

    Esta função utiliza a coleção pública desta fachada para
    preservar a compatibilidade com os testes e módulos antigos.
    """

    return buscar_cliente_por_codigo(
        clientes,
        codigo,
    )


def buscar_clientes_por_nome(nome_busca):
    """
    Busca Clientes por nome completo ou parcial.

    Esta função utiliza a coleção pública desta fachada para
    preservar a compatibilidade com os testes e módulos antigos.
    """

    return buscar_clientes_no_dominio(
        clientes,
        nome_busca,
    )

def quantidade_clientes():
    """
    Retorna a quantidade total de Clientes cadastrados.
    """

    return len(
        clientes
    )