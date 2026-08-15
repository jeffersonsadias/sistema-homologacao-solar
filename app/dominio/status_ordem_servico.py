"""
Regras de domínio dos status de Ordem de Serviço.

Este módulo contém:

- catálogo oficial de status;
- status inicial;
- estados terminais;
- transições permitidas;
- consultas e validações.

A máquina admite fluxos diferentes conforme
a natureza do serviço.

Nem toda Ordem de Serviço precisa passar por:

- diagnóstico;
- aprovação comercial;
- espera por peça;
- retorno técnico.

A conclusão técnica não encerra diretamente
a Ordem de Serviço. Após a execução, o fluxo
passa por confirmação do Cliente.

Não utiliza input(), print() ou persistência.
"""


STATUS_ORDEM_SERVICO = {
    1: "ABERTA",
    2: "EM_TRIAGEM",
    3: "AGUARDANDO_DIAGNOSTICO",
    4: "AGUARDANDO_APROVACAO",
    5: "AGUARDANDO_AGENDAMENTO",
    6: "AGENDADA",
    7: "EM_EXECUCAO",
    8: "AGUARDANDO_PECA",
    9: "RETORNO_NECESSARIO",
    10: "AGUARDANDO_CONFIRMACAO_CLIENTE",
    11: "EM_ANALISE_DE_CONTESTACAO",
    12: "CONCLUIDA",
    13: "CANCELADA",
}


STATUS_INICIAL = (
    STATUS_ORDEM_SERVICO[1]
)


ESTADOS_TERMINAIS = {
    "CONCLUIDA",
    "CANCELADA",
}


TRANSICOES_PERMITIDAS = {
    "ABERTA": [
        "EM_TRIAGEM",
        "CANCELADA",
    ],

    "EM_TRIAGEM": [
        "AGUARDANDO_DIAGNOSTICO",
        "AGUARDANDO_APROVACAO",
        "AGUARDANDO_AGENDAMENTO",
        "CANCELADA",
    ],

    "AGUARDANDO_DIAGNOSTICO": [
        "AGUARDANDO_APROVACAO",
        "AGUARDANDO_AGENDAMENTO",
        "CANCELADA",
    ],

    "AGUARDANDO_APROVACAO": [
        "AGUARDANDO_AGENDAMENTO",
        "CANCELADA",
    ],

    "AGUARDANDO_AGENDAMENTO": [
        "AGENDADA",
        "CANCELADA",
    ],

    "AGENDADA": [
        "EM_EXECUCAO",
        "CANCELADA",
    ],

    "EM_EXECUCAO": [
        "AGUARDANDO_PECA",
        "RETORNO_NECESSARIO",
        "AGUARDANDO_CONFIRMACAO_CLIENTE",
        "CANCELADA",
    ],

    "AGUARDANDO_PECA": [
        "RETORNO_NECESSARIO",
        "AGUARDANDO_AGENDAMENTO",
        "CANCELADA",
    ],

    "RETORNO_NECESSARIO": [
        "AGUARDANDO_AGENDAMENTO",
        "CANCELADA",
    ],

    "AGUARDANDO_CONFIRMACAO_CLIENTE": [
        "CONCLUIDA",
        "EM_ANALISE_DE_CONTESTACAO",
    ],

    "EM_ANALISE_DE_CONTESTACAO": [
        "RETORNO_NECESSARIO",
        "CONCLUIDA",
    ],

    "CONCLUIDA": [],
    "CANCELADA": [],
}

def obter_status(
    codigo: int,
) -> str | None:
    """
    Retorna o status correspondente ao código.

    Retorna None quando o código não existe.
    """

    return STATUS_ORDEM_SERVICO.get(
        codigo
    )

def status_valido(
    codigo: int,
) -> bool:
    """
    Verifica se o código informado representa
    um status válido de Ordem de Serviço.
    """

    return codigo in STATUS_ORDEM_SERVICO

def transicao_permitida(
    status_atual: str,
    novo_status: str,
) -> bool:
    """
    Verifica se uma transição entre estados
    de Ordem de Serviço é permitida.
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
    Informa se o status da Ordem de Serviço
    é terminal.
    """

    return status in ESTADOS_TERMINAIS