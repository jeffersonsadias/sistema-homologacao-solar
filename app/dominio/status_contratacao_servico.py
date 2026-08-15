"""
Regras de domínio dos status de Contratação de Serviço.

Este módulo contém:

- catálogo oficial de status;
- status inicial;
- estados terminais;
- transições permitidas;
- consultas e validações.

PROCESSO_GERADO significa que o processo operacional
correspondente à Contratação foi criado e vinculado.

Esse processo pode ser, por exemplo:

- um Projeto, no fluxo de instalação fotovoltaica;
- uma Ordem de Serviço, no fluxo de pós-venda.

Este módulo não conhece o tipo concreto do processo
operacional e não realiza coordenação entre agregados.

Não utiliza input(), print() ou persistência.
"""


STATUS_CONTRATACAO_SERVICO = {
    1: "EM_FORMALIZACAO",
    2: "CONFIRMADA",
    3: "PROCESSO_GERADO",
    4: "EM_ANDAMENTO",
    5: "CONCLUIDA",
    6: "CANCELADA",
    7: "EXPIRADA",
}


STATUS_INICIAL = (
    STATUS_CONTRATACAO_SERVICO[1]
)


ESTADOS_TERMINAIS = {
    "CONCLUIDA",
    "CANCELADA",
    "EXPIRADA",
}


TRANSICOES_PERMITIDAS = {
    "EM_FORMALIZACAO": [
        "CONFIRMADA",
        "CANCELADA",
        "EXPIRADA",
    ],

    "CONFIRMADA": [
        "PROCESSO_GERADO",
        "CANCELADA",
    ],

    "PROCESSO_GERADO": [
        "EM_ANDAMENTO",
        "CANCELADA",
    ],

    "EM_ANDAMENTO": [
        "CONCLUIDA",
        "CANCELADA",
    ],

    "CONCLUIDA": [],
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

    return STATUS_CONTRATACAO_SERVICO.get(
        codigo
    )

def status_valido(
    codigo: int,
) -> bool:
    """
    Verifica se o código informado representa
    um status válido de Contratação de Serviço.
    """

    return (
        codigo
        in STATUS_CONTRATACAO_SERVICO
    )

def transicao_permitida(
    status_atual: str,
    novo_status: str,
) -> bool:
    """
    Verifica se uma transição entre estados
    de Contratação de Serviço é permitida.
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
    Informa se o status da Contratação
    é terminal.
    """

    return status in ESTADOS_TERMINAIS