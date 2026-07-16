STATUS_PROJETO = {
    1: "Aguardando documentação",
    2: "Documentação recebida",
    3: "Em análise pela distribuidora",
    4: "Correção solicitada",
    5: "Aprovado",
    6: "Instalação concluída",
    7: "Vistoria solicitada",
    8: "Vistoria aprovada",
    9: "Homologado",
    10: "Cancelado"
}

STATUS_INICIAL = STATUS_PROJETO[1]

TRANSICOES_PERMITIDAS = {
    "Aguardando documentação": [
        "Documentação recebida",
        "Cancelado"
    ],

    "Documentação recebida": [
        "Em análise pela distribuidora",
        "Cancelado"
    ],

    "Em análise pela distribuidora": [
        "Correção solicitada",
        "Aprovado",
        "Cancelado"
    ],

    "Correção solicitada": [
        "Documentação recebida",
        "Cancelado"
    ],

    "Aprovado": [
        "Instalação concluída",
        "Cancelado"
    ],

    "Instalação concluída": [
        "Vistoria solicitada",
        "Cancelado"
    ],

    "Vistoria solicitada": [
        "Vistoria aprovada",
        "Correção solicitada",
        "Cancelado"
    ],

    "Vistoria aprovada": [
        "Homologado",
        "Cancelado"
    ],

    "Homologado": [],

    "Cancelado": []
}


def exibir_status():
    """
    Exibe todos os status disponíveis no sistema.
    """

    print("\n--- STATUS DISPONÍVEIS ---")

    for codigo, descricao in STATUS_PROJETO.items():
        print(f"{codigo} - {descricao}")


def obter_status(codigo):
    """
    Recebe o código digitado pelo usuário e retorna
    a descrição correspondente do status.
    """

    return STATUS_PROJETO.get(codigo)


def status_valido(codigo):
    """
    Verifica se o código informado existe dentro
    dos status permitidos.
    """

    return codigo in STATUS_PROJETO


def transicao_permitida(status_atual, novo_status):
    """
    Verifica se a mudança de um status para outro é permitida.
    """

    proximos_status = TRANSICOES_PERMITIDAS.get(status_atual, [])

    return novo_status in proximos_status