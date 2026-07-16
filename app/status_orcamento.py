STATUS_ORCAMENTO = {
    1: "Em elaboração",
    2: "Enviado ao cliente",
    3: "Em negociação",
    4: "Em revisão",
    5: "Aprovado",
    6: "Recusado",
    7: "Expirado",
    8: "Cancelado",
    9: "Convertido em projeto"
}


STATUS_INICIAL = STATUS_ORCAMENTO[1]


TRANSICOES_PERMITIDAS = {
    "Em elaboração": [
        "Enviado ao cliente",
        "Cancelado"
    ],

    "Enviado ao cliente": [
        "Em negociação",
        "Aprovado",
        "Recusado",
        "Expirado",
        "Cancelado"
    ],

    "Em negociação": [
        "Em revisão",
        "Aprovado",
        "Recusado",
        "Cancelado"
    ],

    "Em revisão": [
        "Enviado ao cliente",
        "Cancelado"
    ],

    "Aprovado": [
        "Convertido em projeto",
        "Cancelado"
    ],

    "Recusado": [],

    "Expirado": [
        "Em revisão",
        "Cancelado"
    ],

    "Cancelado": [],

    "Convertido em projeto": []
}


def exibir_status():
    """
    Exibe todos os status disponíveis para orçamentos.
    """

    print("\n--- STATUS DE ORÇAMENTO ---")

    for codigo, descricao in STATUS_ORCAMENTO.items():
        print(f"{codigo} - {descricao}")


def obter_status(codigo):
    """
    Retorna a descrição do status correspondente ao código.
    """

    return STATUS_ORCAMENTO.get(codigo)


def status_valido(codigo):
    """
    Verifica se o código informado representa um status válido.
    """

    return codigo in STATUS_ORCAMENTO


def transicao_permitida(status_atual, novo_status):
    """
    Verifica se uma mudança de status é permitida.
    """

    proximos_status = TRANSICOES_PERMITIDAS.get(
        status_atual,
        []
    )

    return novo_status in proximos_status