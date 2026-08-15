"""
Regras de domínio dos status de Proposta de Serviço.

Este módulo contém:

- catálogo oficial de status;
- status inicial;
- estados terminais;
- transições permitidas;
- consultas e validações.

Algumas transições, como ACEITA e NAO_SELECIONADA,
podem exigir coordenação entre agregados.

Este módulo apenas informa se a transição
faz parte da máquina de estados.

Não utiliza input(), print() ou persistência.
"""


STATUS_PROPOSTA_SERVICO = {
    1: "EM_ELABORACAO",
    2: "ENVIADA",
    3: "EM_REVISAO",
    4: "REVISADA",
    5: "ACEITA",
    6: "RECUSADA",
    7: "NAO_SELECIONADA",
    8: "RETIRADA",
    9: "EXPIRADA",
}


STATUS_INICIAL = (
    STATUS_PROPOSTA_SERVICO[1]
)


ESTADOS_TERMINAIS = {
    "ACEITA",
    "RECUSADA",
    "NAO_SELECIONADA",
    "RETIRADA",
    "EXPIRADA",
}


TRANSICOES_PERMITIDAS = {
    "EM_ELABORACAO": [
        "ENVIADA",
        "RETIRADA",
    ],

    "ENVIADA": [
        "EM_REVISAO",
        "ACEITA",
        "RECUSADA",
        "NAO_SELECIONADA",
        "RETIRADA",
        "EXPIRADA",
    ],

    "EM_REVISAO": [
        "REVISADA",
        "RETIRADA",
    ],

    "REVISADA": [
        "ENVIADA",
        "ACEITA",
        "RECUSADA",
        "NAO_SELECIONADA",
        "RETIRADA",
        "EXPIRADA",
    ],

    "ACEITA": [],
    "RECUSADA": [],
    "NAO_SELECIONADA": [],
    "RETIRADA": [],
    "EXPIRADA": [],
}


def obter_status(
    codigo: int,
) -> str | None:
    """
    Retorna o status correspondente ao código.

    Retorna None quando o código não existe.
    """

    return STATUS_PROPOSTA_SERVICO.get(
        codigo
    )

def status_valido(
    codigo: int,
) -> bool:
    """
    Verifica se o código informado representa
    um status válido de Proposta de Serviço.
    """

    return (
        codigo
        in STATUS_PROPOSTA_SERVICO
    )

def transicao_permitida(
    status_atual: str,
    novo_status: str,
) -> bool:
    """
    Verifica se uma transição entre estados
    de Proposta de Serviço é permitida.
    """

    proximos_status = (
        TRANSICOES_PERMITIDAS.get(
            status_atual,
            [],
        )
    )

    return novo_status in proximos_status

def status_terminal(
    status: str,
) -> bool:
    """
    Informa se o status da Proposta é terminal.
    """

    return status in ESTADOS_TERMINAIS