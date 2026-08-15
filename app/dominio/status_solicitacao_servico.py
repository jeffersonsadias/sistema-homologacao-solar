"""
Regras de domínio dos status de Solicitação de Serviço.

Este módulo contém:

- catálogo oficial de status;
- status inicial;
- estados terminais;
- transições permitidas;
- consultas e validações.

O estado PUBLICADA significa que a Solicitação
foi disponibilizada ao destinatário adequado:

- Empresa específica, em Solicitação DIRETA;
- marketplace, em Solicitação ABERTA.

Este módulo não utiliza input(), print()
ou persistência.
"""


STATUS_SOLICITACAO_SERVICO = {
    1: "EM_ELABORACAO",
    2: "PUBLICADA",
    3: "RECEBENDO_PROPOSTAS",
    4: "EM_ANALISE_PELO_CLIENTE",
    5: "ENCERRADA_COM_CONTRATACAO",
    6: "ENCERRADA_SEM_CONTRATACAO",
    7: "CANCELADA",
    8: "EXPIRADA",
}

STATUS_INICIAL = (
    STATUS_SOLICITACAO_SERVICO[1]
)

ESTADOS_TERMINAIS = {
    "ENCERRADA_COM_CONTRATACAO",
    "ENCERRADA_SEM_CONTRATACAO",
    "CANCELADA",
    "EXPIRADA",
}

TRANSICOES_PERMITIDAS = {
    "EM_ELABORACAO": [
        "PUBLICADA",
        "CANCELADA",
    ],

    "PUBLICADA": [
        "RECEBENDO_PROPOSTAS",
        "CANCELADA",
        "EXPIRADA",
    ],

    "RECEBENDO_PROPOSTAS": [
        "EM_ANALISE_PELO_CLIENTE",
        "ENCERRADA_SEM_CONTRATACAO",
        "CANCELADA",
        "EXPIRADA",
    ],

    "EM_ANALISE_PELO_CLIENTE": [
        "RECEBENDO_PROPOSTAS",
        "ENCERRADA_COM_CONTRATACAO",
        "ENCERRADA_SEM_CONTRATACAO",
        "CANCELADA",
        "EXPIRADA",
    ],

    "ENCERRADA_COM_CONTRATACAO": [],
    "ENCERRADA_SEM_CONTRATACAO": [],
    "CANCELADA": [],
    "EXPIRADA": [],
}

def obter_status(
    codigo: int,
) -> str | None:
    """
    Retorna o status correspondente ao código.

    Retorna None quando o código não existe.
    """

    return STATUS_SOLICITACAO_SERVICO.get(
        codigo
    )

def status_valido(
    codigo: int,
) -> bool:
    """
    Verifica se o código informado representa
    um status válido de Solicitação de Serviço.
    """

    return (
        codigo
        in STATUS_SOLICITACAO_SERVICO
    )

def transicao_permitida(
    status_atual: str,
    novo_status: str,
) -> bool:
    """
    Verifica se uma transição entre dois status
    de Solicitação de Serviço é permitida.
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
    Informa se o status recebido é terminal.

    Solicitações em estado terminal não devem
    ser reabertas.
    """

    return status in ESTADOS_TERMINAIS