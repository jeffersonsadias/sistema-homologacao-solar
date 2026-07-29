"""
Regras de domínio dos status de Orçamento.

Este módulo contém:
- catálogo oficial de status;
- status inicial;
- transições permitidas;
- consultas e validações.

Não utiliza input(), print() ou persistência.
"""


STATUS_ORCAMENTO = {
    1: "Em elaboração",
    2: "Enviado ao cliente",
    3: "Em negociação",
    4: "Em revisão",
    5: "Aprovado",
    6: "Recusado",
    7: "Expirado",
    8: "Cancelado",
    9: "Convertido em projeto",
}


STATUS_INICIAL = STATUS_ORCAMENTO[1]


TRANSICOES_PERMITIDAS = {
    "Em elaboração": [
        "Enviado ao cliente",
        "Cancelado",
    ],

    "Enviado ao cliente": [
        "Em negociação",
        "Aprovado",
        "Recusado",
        "Expirado",
        "Cancelado",
    ],

    "Em negociação": [
        "Em revisão",
        "Aprovado",
        "Recusado",
        "Cancelado",
    ],

    "Em revisão": [
        "Enviado ao cliente",
        "Cancelado",
    ],

    "Aprovado": [
        "Convertido em projeto",
        "Cancelado",
    ],

    "Recusado": [],

    "Expirado": [
        "Em revisão",
        "Cancelado",
    ],

    "Cancelado": [],

    "Convertido em projeto": [],
}


def obter_status(codigo):
    """
    Retorna a descrição correspondente ao código.

    Retorna None quando o código não existe.
    """

    return STATUS_ORCAMENTO.get(codigo)


def status_valido(codigo):
    """
    Verifica se o código representa
    um status válido.
    """

    return codigo in STATUS_ORCAMENTO


def transicao_permitida(
    status_atual,
    novo_status,
):
    """
    Verifica se a transição entre dois status
    é permitida pelas regras comerciais.
    """

    proximos_status = TRANSICOES_PERMITIDAS.get(
        status_atual,
        [],
    )

    return novo_status in proximos_status