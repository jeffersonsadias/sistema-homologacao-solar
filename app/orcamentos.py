"""
Fachada pública do módulo de Orçamentos.

Este módulo preserva a compatibilidade com o restante
do sistema e encaminha as operações para as camadas
especializadas.
"""

from app.dominio.orcamentos import (
    buscar_orcamento_por_codigo,
)

from app.infraestrutura.repositorio_orcamentos_json import (
    carregar_orcamentos,
)

from app.interface import orcamentos_interface


orcamentos = carregar_orcamentos()


def cadastrar_orcamento():
    """
    Encaminha o cadastro para a interface.
    """

    return orcamentos_interface.cadastrar_orcamento(
        orcamentos
    )


def buscar_orcamento(codigo):
    """
    Busca um Orçamento pelo código.
    """

    return buscar_orcamento_por_codigo(
        orcamentos,
        codigo,
    )


def mostrar_orcamento(orcamento):
    """
    Encaminha a exibição para a interface.
    """

    return orcamentos_interface.mostrar_orcamento(
        orcamento
    )


def listar_orcamentos():
    """
    Encaminha a listagem para a interface.
    """

    return orcamentos_interface.listar_orcamentos(
        orcamentos
    )


def selecionar_orcamento():
    """
    Encaminha a seleção para a interface.
    """

    return orcamentos_interface.selecionar_orcamento(
        orcamentos
    )


def alterar_status():
    """
    Encaminha a alteração de status para a interface.
    """

    return orcamentos_interface.alterar_status(
        orcamentos
    )


def converter_para_projeto():
    """
    Encaminha a conversão para a interface.
    """

    return orcamentos_interface.converter_para_projeto(
        orcamentos
    )