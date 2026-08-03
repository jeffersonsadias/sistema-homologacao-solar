"""
Máquina de estados e eventos do Contexto de Homologação.

Este módulo define:

- os estados possíveis de uma Homologação;
- o estado inicial;
- as transições permitidas;
- os estados terminais;
- os eventos internos de negócio;
- o estado resultante de cada evento;
- funções de consulta e validação da máquina de estados.

Um Status representa a situação atual da Homologação.

Um EventoHomologacao representa um acontecimento relevante do
domínio capaz de produzir uma mudança no estado geral do processo.

Exemplos de eventos:

- envio da Submissão Inicial;
- início da análise pela concessionária;
- recebimento de Exigências;
- criação de Submissão derivada;
- reapresentação à concessionária;
- aprovação;
- rejeição.

Este módulo não modifica diretamente uma Homologação.

A aplicação efetiva dos estados e dos eventos pertence ao Aggregate
Root definido em:

    app/dominio/homologacoes.py
"""

from enum import Enum


class StatusHomologacao(str, Enum):
    """
    Estados possíveis do ciclo de vida de uma Homologação.

    A classe herda de:

    - str:
      permite que os valores sejam facilmente armazenados em JSON;

    - Enum:
      restringe os estados ao conjunto oficialmente definido.
    """

    EM_PREPARACAO = "EM_PREPARACAO"
    AGUARDANDO_DOCUMENTACAO = "AGUARDANDO_DOCUMENTACAO"
    PRONTA_PARA_ENVIO = "PRONTA_PARA_ENVIO"

    ENVIADA_A_CONCESSIONARIA = "ENVIADA_A_CONCESSIONARIA"
    EM_ANALISE = "EM_ANALISE"
    COM_EXIGENCIA = "COM_EXIGENCIA"
    EM_CORRECAO = "EM_CORRECAO"
    REAPRESENTADA = "REAPRESENTADA"
    PARECER_DE_ACESSO_EMITIDO = "PARECER_DE_ACESSO_EMITIDO"
    REJEITADA = "REJEITADA"

    AGUARDANDO_INSTALACAO = "AGUARDANDO_INSTALACAO"
    INSTALACAO_CONCLUIDA = "INSTALACAO_CONCLUIDA"

    VISTORIA_SOLICITADA = "VISTORIA_SOLICITADA"
    AGUARDANDO_VISTORIA = "AGUARDANDO_VISTORIA"
    VISTORIA_REPROVADA = "VISTORIA_REPROVADA"
    CORRECAO_POS_VISTORIA = "CORRECAO_POS_VISTORIA"
    VISTORIA_APROVADA = "VISTORIA_APROVADA"

    AGUARDANDO_LIGACAO = "AGUARDANDO_LIGACAO"
    SISTEMA_LIGADO = "SISTEMA_LIGADO"

    CONCLUIDA = "CONCLUIDA"
    CANCELADA = "CANCELADA"

class EventoHomologacao(str, Enum):
    """
    Eventos de negócio capazes de produzir reflexos no estado
    geral da Homologação.

    Um Evento representa algo que efetivamente aconteceu no
    processo. Ele não é um novo estado.

    Exemplos:

    - uma Submissão foi enviada;
    - a concessionária iniciou a análise;
    - uma Exigência foi recebida;
    - uma Complementação foi criada;
    - um Reenvio foi apresentado.
    """

    SUBMISSAO_INICIAL_ENVIADA = (
        "SUBMISSAO_INICIAL_ENVIADA"
    )

    ANALISE_INICIADA = "ANALISE_INICIADA"

    EXIGENCIA_RECEBIDA = "EXIGENCIA_RECEBIDA"

    SUBMISSAO_DERIVADA_CRIADA = (
        "SUBMISSAO_DERIVADA_CRIADA"
    )

    SUBMISSAO_DERIVADA_ENVIADA = (
        "SUBMISSAO_DERIVADA_ENVIADA"
    )

    APROVACAO_RECEBIDA = "APROVACAO_RECEBIDA"

    REJEICAO_RECEBIDA = "REJEICAO_RECEBIDA"

STATUS_INICIAL_HOMOLOGACAO = StatusHomologacao.EM_PREPARACAO


ROTULOS_STATUS_HOMOLOGACAO = {
    StatusHomologacao.EM_PREPARACAO:
        "Em preparação",

    StatusHomologacao.AGUARDANDO_DOCUMENTACAO:
        "Aguardando documentação",

    StatusHomologacao.PRONTA_PARA_ENVIO:
        "Pronta para envio",

    StatusHomologacao.ENVIADA_A_CONCESSIONARIA:
        "Enviada à concessionária",

    StatusHomologacao.EM_ANALISE:
        "Em análise",

    StatusHomologacao.COM_EXIGENCIA:
        "Com exigência",

    StatusHomologacao.EM_CORRECAO:
        "Em correção",

    StatusHomologacao.REAPRESENTADA:
        "Reapresentada",

    StatusHomologacao.PARECER_DE_ACESSO_EMITIDO:
        "Parecer de acesso emitido",

    StatusHomologacao.REJEITADA:
        "Rejeitada",

    StatusHomologacao.AGUARDANDO_INSTALACAO:
        "Aguardando instalação",

    StatusHomologacao.INSTALACAO_CONCLUIDA:
        "Instalação concluída",

    StatusHomologacao.VISTORIA_SOLICITADA:
        "Vistoria solicitada",

    StatusHomologacao.AGUARDANDO_VISTORIA:
        "Aguardando vistoria",

    StatusHomologacao.VISTORIA_REPROVADA:
        "Vistoria reprovada",

    StatusHomologacao.CORRECAO_POS_VISTORIA:
        "Correção pós-vistoria",

    StatusHomologacao.VISTORIA_APROVADA:
        "Vistoria aprovada",

    StatusHomologacao.AGUARDANDO_LIGACAO:
        "Aguardando ligação",

    StatusHomologacao.SISTEMA_LIGADO:
        "Sistema ligado",

    StatusHomologacao.CONCLUIDA:
        "Concluída",

    StatusHomologacao.CANCELADA:
        "Cancelada",
}


TRANSICOES_HOMOLOGACAO = {
    StatusHomologacao.EM_PREPARACAO: {
        StatusHomologacao.AGUARDANDO_DOCUMENTACAO,
        StatusHomologacao.PRONTA_PARA_ENVIO,
        StatusHomologacao.CANCELADA,
    },

    StatusHomologacao.AGUARDANDO_DOCUMENTACAO: {
        StatusHomologacao.EM_PREPARACAO,
        StatusHomologacao.PRONTA_PARA_ENVIO,
        StatusHomologacao.CANCELADA,
    },

    StatusHomologacao.PRONTA_PARA_ENVIO: {
        StatusHomologacao.AGUARDANDO_DOCUMENTACAO,
        StatusHomologacao.ENVIADA_A_CONCESSIONARIA,
        StatusHomologacao.CANCELADA,
    },

    StatusHomologacao.ENVIADA_A_CONCESSIONARIA: {
        StatusHomologacao.EM_ANALISE,
        StatusHomologacao.COM_EXIGENCIA,
        StatusHomologacao.PARECER_DE_ACESSO_EMITIDO,
        StatusHomologacao.REJEITADA,
        StatusHomologacao.CANCELADA,
    },

    StatusHomologacao.EM_ANALISE: {
        StatusHomologacao.COM_EXIGENCIA,
        StatusHomologacao.PARECER_DE_ACESSO_EMITIDO,
        StatusHomologacao.REJEITADA,
        StatusHomologacao.CANCELADA,
    },

    StatusHomologacao.COM_EXIGENCIA: {
        StatusHomologacao.EM_CORRECAO,
        StatusHomologacao.REJEITADA,
        StatusHomologacao.CANCELADA,
    },

    StatusHomologacao.EM_CORRECAO: {
        StatusHomologacao.REAPRESENTADA,
        StatusHomologacao.COM_EXIGENCIA,
        StatusHomologacao.CANCELADA,
    },

    StatusHomologacao.REAPRESENTADA: {
        StatusHomologacao.EM_ANALISE,
        StatusHomologacao.COM_EXIGENCIA,
        StatusHomologacao.PARECER_DE_ACESSO_EMITIDO,
        StatusHomologacao.REJEITADA,
        StatusHomologacao.CANCELADA,
    },

    StatusHomologacao.PARECER_DE_ACESSO_EMITIDO: {
        StatusHomologacao.AGUARDANDO_INSTALACAO,
        StatusHomologacao.INSTALACAO_CONCLUIDA,
        StatusHomologacao.CANCELADA,
    },

    StatusHomologacao.AGUARDANDO_INSTALACAO: {
        StatusHomologacao.INSTALACAO_CONCLUIDA,
        StatusHomologacao.CANCELADA,
    },

    StatusHomologacao.INSTALACAO_CONCLUIDA: {
        StatusHomologacao.VISTORIA_SOLICITADA,
        StatusHomologacao.CANCELADA,
    },

    StatusHomologacao.VISTORIA_SOLICITADA: {
        StatusHomologacao.AGUARDANDO_VISTORIA,
        StatusHomologacao.VISTORIA_APROVADA,
        StatusHomologacao.VISTORIA_REPROVADA,
        StatusHomologacao.CANCELADA,
    },

    StatusHomologacao.AGUARDANDO_VISTORIA: {
        StatusHomologacao.VISTORIA_APROVADA,
        StatusHomologacao.VISTORIA_REPROVADA,
        StatusHomologacao.CANCELADA,
    },

    StatusHomologacao.VISTORIA_REPROVADA: {
        StatusHomologacao.CORRECAO_POS_VISTORIA,
        StatusHomologacao.CANCELADA,
    },

    StatusHomologacao.CORRECAO_POS_VISTORIA: {
        StatusHomologacao.VISTORIA_SOLICITADA,
        StatusHomologacao.CANCELADA,
    },

    StatusHomologacao.VISTORIA_APROVADA: {
        StatusHomologacao.AGUARDANDO_LIGACAO,
        StatusHomologacao.SISTEMA_LIGADO,
        StatusHomologacao.CANCELADA,
    },

    StatusHomologacao.AGUARDANDO_LIGACAO: {
        StatusHomologacao.SISTEMA_LIGADO,
        StatusHomologacao.CANCELADA,
    },

    StatusHomologacao.SISTEMA_LIGADO: {
        StatusHomologacao.CONCLUIDA,
    },

    StatusHomologacao.CONCLUIDA: set(),
    StatusHomologacao.REJEITADA: set(),
    StatusHomologacao.CANCELADA: set(),
}

STATUS_RESULTANTE_POR_EVENTO_HOMOLOGACAO = {
    EventoHomologacao.SUBMISSAO_INICIAL_ENVIADA: (
        StatusHomologacao.ENVIADA_A_CONCESSIONARIA
    ),

    EventoHomologacao.ANALISE_INICIADA: (
        StatusHomologacao.EM_ANALISE
    ),

    EventoHomologacao.EXIGENCIA_RECEBIDA: (
        StatusHomologacao.COM_EXIGENCIA
    ),

    EventoHomologacao.SUBMISSAO_DERIVADA_CRIADA: (
        StatusHomologacao.EM_CORRECAO
    ),

    EventoHomologacao.SUBMISSAO_DERIVADA_ENVIADA: (
        StatusHomologacao.REAPRESENTADA
    ),

    EventoHomologacao.APROVACAO_RECEBIDA: (
        StatusHomologacao.PARECER_DE_ACESSO_EMITIDO
    ),

    EventoHomologacao.REJEICAO_RECEBIDA: (
        StatusHomologacao.REJEITADA
    ),
}

STATUS_TERMINAIS_HOMOLOGACAO = {
    StatusHomologacao.CONCLUIDA,
    StatusHomologacao.REJEITADA,
    StatusHomologacao.CANCELADA,
}


def transicao_status_homologacao_e_valida(
    status_atual: StatusHomologacao,
    novo_status: StatusHomologacao,
) -> bool:
    """
    Verifica se uma transição de status é permitida.

    Parâmetros:
        status_atual:
            Estado atual da Homologação.

        novo_status:
            Estado para o qual se deseja avançar.

    Retorno:
        True:
            quando a transição é permitida;

        False:
            quando a transição não é permitida.
    """

    proximos_status = TRANSICOES_HOMOLOGACAO.get(
        status_atual,
        set(),
    )

    return novo_status in proximos_status

def listar_transicoes_possiveis(
    status_atual: StatusHomologacao,
) -> tuple[StatusHomologacao, ...]:
    """
    Retorna os estados que podem ser alcançados a partir do estado atual.

    O retorno é uma tupla ordenada pelo valor interno dos estados.

    A tupla foi escolhida porque a função entrega uma consulta que não
    deve ser alterada diretamente pelo código chamador.
    """

    proximos_status = TRANSICOES_HOMOLOGACAO.get(
        status_atual,
        set(),
    )

    return tuple(
        sorted(
            proximos_status,
            key=lambda status: status.value,
        )
    )

def status_homologacao_e_terminal(
    status: StatusHomologacao,
) -> bool:
    """
    Verifica se um estado é terminal.

    Estados terminais não permitem novas transições.
    """

    return status in STATUS_TERMINAIS_HOMOLOGACAO

def obter_rotulo_status_homologacao(
    status: StatusHomologacao,
) -> str:
    """
    Retorna o texto amigável correspondente ao estado interno.

    Exemplo:

        Estado interno:
            StatusHomologacao.EM_ANALISE

        Texto apresentado:
            Em análise
    """

    return ROTULOS_STATUS_HOMOLOGACAO[status]

def _converter_evento_homologacao(
    evento,
) -> EventoHomologacao | None:
    """
    Converte um Enum ou texto válido em EventoHomologacao.

    Retorna None quando o valor não representa um Evento válido.
    """

    if isinstance(evento, EventoHomologacao):
        return evento

    try:
        return EventoHomologacao(evento)

    except (ValueError, TypeError):
        return None

def evento_homologacao_valido(
    evento,
) -> bool:
    """
    Informa se o valor representa um Evento válido
    da Homologação.
    """

    return _converter_evento_homologacao(
        evento
    ) is not None

def obter_status_resultante_evento_homologacao(
    evento,
) -> StatusHomologacao | None:
    """
    Retorna o estado pretendido por um Evento da Homologação.

    A função não verifica o estado atual e não altera nenhuma
    Homologação.

    Retorna None quando o Evento informado for inválido.
    """

    evento_convertido = _converter_evento_homologacao(
        evento
    )

    if evento_convertido is None:
        return None

    return STATUS_RESULTANTE_POR_EVENTO_HOMOLOGACAO[
        evento_convertido
    ]

def validar_evento_no_estado_homologacao(
    status_atual,
    evento,
) -> StatusHomologacao:
    """
    Valida se um Evento pode produzir uma mudança a partir
    do estado atual da Homologação.

    Retorna o novo Status quando:

    - o estado atual é válido;
    - o Evento é válido;
    - a transição resultante é permitida.

    Lança ValueError quando qualquer condição não for atendida.
    """

    try:
        status_atual_convertido = StatusHomologacao(
            status_atual
        )

    except (ValueError, TypeError) as erro:
        raise ValueError(
            "Status atual da Homologação inválido: "
            f"{status_atual!r}."
        ) from erro

    evento_convertido = _converter_evento_homologacao(
        evento
    )

    if evento_convertido is None:
        raise ValueError(
            "Evento da Homologação inválido: "
            f"{evento!r}."
        )

    novo_status = (
        STATUS_RESULTANTE_POR_EVENTO_HOMOLOGACAO[
            evento_convertido
        ]
    )

    if not transicao_status_homologacao_e_valida(
        status_atual=status_atual_convertido,
        novo_status=novo_status,
    ):
        raise ValueError(
            "O Evento não pode ser aplicado ao estado atual "
            "da Homologação: "
            f"{evento_convertido.value} em "
            f"{status_atual_convertido.value}."
        )

    return novo_status