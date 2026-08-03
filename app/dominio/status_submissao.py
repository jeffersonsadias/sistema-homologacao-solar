"""
Máquinas de estados das Submissões da Homologação.

Este módulo concentra dois ciclos de vida independentes de uma
Submissão à concessionária:

1. Ciclo operacional:
   representa a preparação, o envio, a protocolação e o eventual
   cancelamento do pacote.

2. Ciclo de análise:
   representa os retornos recebidos da concessionária depois do
   envio da Submissão.

Este módulo é responsável por:

- definir os estados operacionais;
- definir os estados da análise;
- definir os estados iniciais;
- definir as transições permitidas;
- identificar estados terminais;
- validar estados e transições;
- fornecer rótulos amigáveis.

Este módulo não modifica Submissões nem Homologações.

As operações que aplicam efetivamente essas transições pertencem ao
Aggregate Root:

    app/dominio/homologacoes.py
"""

from enum import Enum


class StatusOperacionalSubmissao(str, Enum):
    """
    Estados do ciclo operacional de uma Submissão.

    Herda de ``str`` para que os valores possam ser persistidos
    diretamente em JSON sem depender do nome interno do enum.
    """

    EM_PREPARACAO = "EM_PREPARACAO"
    PRONTA_PARA_ENVIO = "PRONTA_PARA_ENVIO"
    ENVIADA = "ENVIADA"
    PROTOCOLADA = "PROTOCOLADA"
    CANCELADA = "CANCELADA"


class StatusAnaliseSubmissao(str, Enum):
    """
    Estados do ciclo de análise de uma Submissão.

    Esse ciclo começa em SEM_RESPOSTA e só pode avançar depois
    que a Submissão tiver sido enviada.

    A verificação de que a Submissão foi realmente enviada não pertence
    a este módulo, pois exige acesso à estrutura completa da Submissão.
    Essa validação cruzada ficará em homologacoes.py.
    """

    SEM_RESPOSTA = "SEM_RESPOSTA"
    RECEBIDA = "RECEBIDA"
    EM_ANALISE = "EM_ANALISE"
    COM_EXIGENCIA = "COM_EXIGENCIA"
    APROVADA = "APROVADA"
    REJEITADA = "REJEITADA"


# Estado atribuído automaticamente quando uma nova Submissão é criada.
STATUS_OPERACIONAL_INICIAL = StatusOperacionalSubmissao.EM_PREPARACAO

# Estado da análise atribuído automaticamente na criação da Submissão.
STATUS_ANALISE_INICIAL = StatusAnaliseSubmissao.SEM_RESPOSTA


# Matriz das transições permitidas no ciclo operacional.
#
# Cada chave representa o estado atual.
# O conjunto associado contém os estados que podem ser alcançados
# diretamente a partir daquele estado.
TRANSICOES_STATUS_OPERACIONAL_SUBMISSAO = {
    StatusOperacionalSubmissao.EM_PREPARACAO: {
        StatusOperacionalSubmissao.PRONTA_PARA_ENVIO,
        StatusOperacionalSubmissao.CANCELADA,
    },
    StatusOperacionalSubmissao.PRONTA_PARA_ENVIO: {
        StatusOperacionalSubmissao.EM_PREPARACAO,
        StatusOperacionalSubmissao.ENVIADA,
        StatusOperacionalSubmissao.CANCELADA,
    },
    StatusOperacionalSubmissao.ENVIADA: {
        StatusOperacionalSubmissao.PROTOCOLADA,
    },
    StatusOperacionalSubmissao.PROTOCOLADA: set(),
    StatusOperacionalSubmissao.CANCELADA: set(),
}


# Matriz das transições permitidas no ciclo da análise.
#
# Os estados intermediários podem ser ignorados quando a concessionária
# não fornece todas as etapas formalmente.
#
# Exemplo:
# SEM_RESPOSTA -> APROVADA
#
# Isso é permitido porque algumas concessionárias podem comunicar
# diretamente a aprovação, sem registrar previamente recebimento
# confirmado ou início da análise.
TRANSICOES_STATUS_ANALISE_SUBMISSAO = {
    StatusAnaliseSubmissao.SEM_RESPOSTA: {
        StatusAnaliseSubmissao.RECEBIDA,
        StatusAnaliseSubmissao.EM_ANALISE,
        StatusAnaliseSubmissao.COM_EXIGENCIA,
        StatusAnaliseSubmissao.APROVADA,
        StatusAnaliseSubmissao.REJEITADA,
    },
    StatusAnaliseSubmissao.RECEBIDA: {
        StatusAnaliseSubmissao.EM_ANALISE,
        StatusAnaliseSubmissao.COM_EXIGENCIA,
        StatusAnaliseSubmissao.APROVADA,
        StatusAnaliseSubmissao.REJEITADA,
    },
    StatusAnaliseSubmissao.EM_ANALISE: {
        StatusAnaliseSubmissao.COM_EXIGENCIA,
        StatusAnaliseSubmissao.APROVADA,
        StatusAnaliseSubmissao.REJEITADA,
    },
    StatusAnaliseSubmissao.COM_EXIGENCIA: set(),
    StatusAnaliseSubmissao.APROVADA: set(),
    StatusAnaliseSubmissao.REJEITADA: set(),
}


# Estados que não permitem novas transições no ciclo operacional.
STATUS_TERMINAIS_OPERACIONAIS_SUBMISSAO = {
    StatusOperacionalSubmissao.PROTOCOLADA,
    StatusOperacionalSubmissao.CANCELADA,
}


# Estados que encerram a análise daquela Submissão específica.
#
# COM_EXIGENCIA é terminal porque o atendimento será feito por uma nova
# Complementação ou por um novo Reenvio. A Submissão original não volta
# para EM_ANALISE.
STATUS_TERMINAIS_ANALISE_SUBMISSAO = {
    StatusAnaliseSubmissao.COM_EXIGENCIA,
    StatusAnaliseSubmissao.APROVADA,
    StatusAnaliseSubmissao.REJEITADA,
}


# Rótulos amigáveis são separados dos valores persistidos.
#
# Dessa forma, podemos mudar futuramente a forma de exibição sem alterar
# os dados já gravados no JSON.
ROTULOS_STATUS_OPERACIONAL_SUBMISSAO = {
    StatusOperacionalSubmissao.EM_PREPARACAO: "Em preparação",
    StatusOperacionalSubmissao.PRONTA_PARA_ENVIO: "Pronta para envio",
    StatusOperacionalSubmissao.ENVIADA: "Enviada",
    StatusOperacionalSubmissao.PROTOCOLADA: "Protocolada",
    StatusOperacionalSubmissao.CANCELADA: "Cancelada",
}


ROTULOS_STATUS_ANALISE_SUBMISSAO = {
    StatusAnaliseSubmissao.SEM_RESPOSTA: "Sem resposta",
    StatusAnaliseSubmissao.RECEBIDA: "Recebimento confirmado",
    StatusAnaliseSubmissao.EM_ANALISE: "Em análise",
    StatusAnaliseSubmissao.COM_EXIGENCIA: "Com exigência",
    StatusAnaliseSubmissao.APROVADA: "Aprovada",
    StatusAnaliseSubmissao.REJEITADA: "Rejeitada",
}


def _converter_status_operacional(status):
    """
    Converte um enum ou texto válido para StatusOperacionalSubmissao.

    Esta é uma função auxiliar privada. O underline inicial indica
    que ela não faz parte da interface pública principal do módulo.

    Retorna:
        StatusOperacionalSubmissao:
            Quando o valor é válido.

        None:
            Quando o valor não representa um estado operacional válido.
    """

    if isinstance(status, StatusOperacionalSubmissao):
        return status

    try:
        return StatusOperacionalSubmissao(status)
    except (ValueError, TypeError):
        return None

def _converter_status_analise(status):
    """
    Converte um enum ou texto válido para StatusAnaliseSubmissao.

    Retorna:
        StatusAnaliseSubmissao:
            Quando o valor é válido.

        None:
            Quando o valor não representa um estado de análise válido.
    """

    if isinstance(status, StatusAnaliseSubmissao):
        return status

    try:
        return StatusAnaliseSubmissao(status)
    except (ValueError, TypeError):
        return None

def status_operacional_submissao_valido(status):
    """
    Informa se o valor representa um estado operacional válido.

    Aceita tanto:

        StatusOperacionalSubmissao.ENVIADA

    quanto:

        "ENVIADA"

    Retorna:
        bool: True quando válido; False quando inválido.
    """

    return _converter_status_operacional(status) is not None

def status_analise_submissao_valido(status):
    """
    Informa se o valor representa um estado de análise válido.

    Aceita tanto objetos do enum quanto seus valores textuais.
    """

    return _converter_status_analise(status) is not None

def transicao_operacional_submissao_permitida(
    status_atual,
    novo_status,
):
    """
    Verifica se uma transição operacional está prevista na matriz.

    Esta função não lança erro para transições inválidas. Ela funciona
    como uma consulta booleana.

    Retorna:
        bool:
            True quando a transição é permitida.
            False quando um estado é inválido ou a transição é proibida.
    """

    status_atual_convertido = _converter_status_operacional(status_atual)
    novo_status_convertido = _converter_status_operacional(novo_status)

    if status_atual_convertido is None:
        return False

    if novo_status_convertido is None:
        return False

    destinos_permitidos = TRANSICOES_STATUS_OPERACIONAL_SUBMISSAO[
        status_atual_convertido
    ]

    return novo_status_convertido in destinos_permitidos

def transicao_analise_submissao_permitida(
    status_atual,
    novo_status,
):
    """
    Verifica se uma transição do ciclo de análise está prevista.

    Esta função verifica somente a matriz abstrata.

    Ela não verifica se a Submissão está operacionalmente ENVIADA ou
    PROTOCOLADA. Essa é uma regra cruzada e será tratada pela raiz
    do agregado.
    """

    status_atual_convertido = _converter_status_analise(status_atual)
    novo_status_convertido = _converter_status_analise(novo_status)

    if status_atual_convertido is None:
        return False

    if novo_status_convertido is None:
        return False

    destinos_permitidos = TRANSICOES_STATUS_ANALISE_SUBMISSAO[
        status_atual_convertido
    ]

    return novo_status_convertido in destinos_permitidos

def validar_transicao_operacional_submissao(
    status_atual,
    novo_status,
):
    """
    Valida uma transição operacional.

    Diferentemente da função booleana, esta função lança ValueError
    quando a transição não é permitida.

    Nesta primeira implementação utilizamos ValueError para manter este
    módulo independente do conteúdo atual de erros_dominio.py.

    Quando a hierarquia definitiva das exceções do agregado for
    implementada, esta exceção poderá ser substituída por
    ErroTransicaoEstado sem alterar a regra da função.
    """

    status_atual_convertido = _converter_status_operacional(status_atual)
    novo_status_convertido = _converter_status_operacional(novo_status)

    if status_atual_convertido is None:
        raise ValueError(
            f"Status operacional atual inválido: {status_atual!r}."
        )

    if novo_status_convertido is None:
        raise ValueError(
            f"Novo status operacional inválido: {novo_status!r}."
        )

    if not transicao_operacional_submissao_permitida(
        status_atual_convertido,
        novo_status_convertido,
    ):
        raise ValueError(
            "Transição operacional da Submissão não permitida: "
            f"{status_atual_convertido.value} -> "
            f"{novo_status_convertido.value}."
        )

    return True

def validar_transicao_analise_submissao(
    status_atual,
    novo_status,
):
    """
    Valida uma transição no ciclo de análise.

    Retorna True quando a transição é permitida e lança ValueError
    quando os estados ou a transição forem inválidos.
    """

    status_atual_convertido = _converter_status_analise(status_atual)
    novo_status_convertido = _converter_status_analise(novo_status)

    if status_atual_convertido is None:
        raise ValueError(
            f"Status atual da análise inválido: {status_atual!r}."
        )

    if novo_status_convertido is None:
        raise ValueError(
            f"Novo status da análise inválido: {novo_status!r}."
        )

    if not transicao_analise_submissao_permitida(
        status_atual_convertido,
        novo_status_convertido,
    ):
        raise ValueError(
            "Transição da análise da Submissão não permitida: "
            f"{status_atual_convertido.value} -> "
            f"{novo_status_convertido.value}."
        )

    return True

def status_operacional_submissao_terminal(status):
    """
    Informa se um estado operacional é terminal.

    Estados terminais:

        PROTOCOLADA
        CANCELADA

    Um valor inválido retorna False.
    """

    status_convertido = _converter_status_operacional(status)

    if status_convertido is None:
        return False

    return status_convertido in STATUS_TERMINAIS_OPERACIONAIS_SUBMISSAO

def status_analise_submissao_terminal(status):
    """
    Informa se um estado da análise é terminal.

    Estados terminais:

        COM_EXIGENCIA
        APROVADA
        REJEITADA

    Um valor inválido retorna False.
    """

    status_convertido = _converter_status_analise(status)

    if status_convertido is None:
        return False

    return status_convertido in STATUS_TERMINAIS_ANALISE_SUBMISSAO

def obter_rotulo_status_operacional_submissao(status):
    """
    Retorna o rótulo amigável de um estado operacional.

    Retorna None quando o estado informado é inválido.
    """

    status_convertido = _converter_status_operacional(status)

    if status_convertido is None:
        return None

    return ROTULOS_STATUS_OPERACIONAL_SUBMISSAO[status_convertido]

def obter_rotulo_status_analise_submissao(status):
    """
    Retorna o rótulo amigável de um estado da análise.

    Retorna None quando o estado informado é inválido.
    """

    status_convertido = _converter_status_analise(status)

    if status_convertido is None:
        return None

    return ROTULOS_STATUS_ANALISE_SUBMISSAO[status_convertido]