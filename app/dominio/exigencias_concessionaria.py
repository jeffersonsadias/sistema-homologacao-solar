"""
Regras locais das Exigências emitidas pela concessionária.

Uma Resposta da concessionária pode conter uma ou várias
Exigências.

Exemplo:

    Resposta de Exigência
    ├── corrigir o diagrama unifilar;
    ├── complementar o documento do titular;
    └── esclarecer a divisão dos créditos de energia.

Este módulo é responsável por:

- definir os tipos de Exigência;
- definir os estados de atendimento;
- criar a estrutura local de uma Exigência;
- validar seus dados;
- validar a transição do atendimento;
- verificar a compatibilidade entre uma Exigência e um tipo
  de Submissão;
- fornecer funções de consulta e rótulos amigáveis.

Este módulo não modifica diretamente:

- a Homologação;
- as Submissões;
- as Respostas;
- as coleções internas do agregado.

A localização das Exigências, o controle de atendimento ativo e a
alteração para ATENDIDA durante o envio de uma Submissão derivada
pertencem ao Aggregate Root:

    app/dominio/homologacoes.py
"""

from enum import Enum


class TipoExigencia(str, Enum):
    """
    Categorias padronizadas de Exigência da concessionária.
    """

    COMPLEMENTACAO_DOCUMENTAL = "COMPLEMENTACAO_DOCUMENTAL"
    CORRECAO_DOCUMENTAL = "CORRECAO_DOCUMENTAL"
    CORRECAO_TECNICA = "CORRECAO_TECNICA"
    ESCLARECIMENTO = "ESCLARECIMENTO"
    REENVIO_INTEGRAL = "REENVIO_INTEGRAL"
    OUTRA = "OUTRA"


class StatusAtendimentoExigencia(str, Enum):
    """
    Estados do atendimento de uma Exigência.

    Nesta primeira versão do domínio, a Exigência possui apenas:

    PENDENTE:
        Ainda não foi atendida por uma nova Submissão enviada.

    ATENDIDA:
        Foi relacionada a uma Complementação ou Reenvio que já foi
        efetivamente enviado à concessionária.
    """

    PENDENTE = "PENDENTE"
    ATENDIDA = "ATENDIDA"


STATUS_INICIAL_ATENDIMENTO_EXIGENCIA = (
    StatusAtendimentoExigencia.PENDENTE
)


TRANSICOES_STATUS_ATENDIMENTO_EXIGENCIA = {
    StatusAtendimentoExigencia.PENDENTE: {
        StatusAtendimentoExigencia.ATENDIDA,
    },
    StatusAtendimentoExigencia.ATENDIDA: set(),
}


STATUS_TERMINAIS_ATENDIMENTO_EXIGENCIA = {
    StatusAtendimentoExigencia.ATENDIDA,
}


ROTULOS_TIPO_EXIGENCIA = {
    TipoExigencia.COMPLEMENTACAO_DOCUMENTAL:
        "Complementação documental",
    TipoExigencia.CORRECAO_DOCUMENTAL:
        "Correção documental",
    TipoExigencia.CORRECAO_TECNICA:
        "Correção técnica",
    TipoExigencia.ESCLARECIMENTO:
        "Esclarecimento",
    TipoExigencia.REENVIO_INTEGRAL:
        "Reenvio integral",
    TipoExigencia.OUTRA:
        "Outra",
}


ROTULOS_STATUS_ATENDIMENTO_EXIGENCIA = {
    StatusAtendimentoExigencia.PENDENTE: "Pendente",
    StatusAtendimentoExigencia.ATENDIDA: "Atendida",
}


# A compatibilidade abaixo registra a orientação normal do domínio.
#
# Ela não determina que todas as combinações incompatíveis devam
# obrigatoriamente bloquear a operação.
#
# A regra bloqueante definitiva desta primeira versão será:
#
#     REENVIO_INTEGRAL
#     +
#     COMPLEMENTACAO
#     =
#     combinação proibida
#
# Os nomes dos tipos de Submissão são armazenados como texto para evitar
# dependência circular com submissoes_homologacao.py, que será criado em
# uma etapa posterior.
COMPATIBILIDADE_TIPO_EXIGENCIA_SUBMISSAO = {
    TipoExigencia.COMPLEMENTACAO_DOCUMENTAL: {
        "COMPLEMENTACAO",
        "REENVIO",
    },
    TipoExigencia.CORRECAO_DOCUMENTAL: {
        "REENVIO",
    },
    TipoExigencia.CORRECAO_TECNICA: {
        "REENVIO",
    },
    TipoExigencia.ESCLARECIMENTO: {
        "COMPLEMENTACAO",
        "REENVIO",
    },
    TipoExigencia.REENVIO_INTEGRAL: {
        "REENVIO",
    },
    TipoExigencia.OUTRA: {
        "COMPLEMENTACAO",
        "REENVIO",
    },
}


def _converter_tipo_exigencia(tipo):
    """
    Converte um enum ou texto válido para TipoExigencia.

    Retorna:
        TipoExigencia:
            Quando o valor é válido.

        None:
            Quando o valor não representa um tipo válido.
    """

    if isinstance(tipo, TipoExigencia):
        return tipo

    try:
        return TipoExigencia(tipo)
    except (ValueError, TypeError):
        return None

def _converter_status_atendimento(status):
    """
    Converte um enum ou texto válido para StatusAtendimentoExigencia.
    """

    if isinstance(status, StatusAtendimentoExigencia):
        return status

    try:
        return StatusAtendimentoExigencia(status)
    except (ValueError, TypeError):
        return None

def _validar_codigo_positivo(valor, nome_campo):
    """
    Valida códigos e números sequenciais positivos.

    Em Python, bool é uma subclasse de int:

        isinstance(True, int) == True

    Por isso, a validação rejeita bool explicitamente.
    """

    if isinstance(valor, bool):
        raise ValueError(
            f"{nome_campo} deve ser um número inteiro positivo."
        )

    if not isinstance(valor, int):
        raise ValueError(
            f"{nome_campo} deve ser um número inteiro positivo."
        )

    if valor <= 0:
        raise ValueError(
            f"{nome_campo} deve ser maior que zero."
        )

def _normalizar_descricao(descricao):
    """
    Remove espaços externos e valida a descrição da Exigência.
    """

    if not isinstance(descricao, str):
        raise ValueError(
            "A descrição da Exigência deve ser um texto."
        )

    descricao_normalizada = descricao.strip()

    if not descricao_normalizada:
        raise ValueError(
            "A descrição da Exigência é obrigatória."
        )

    return descricao_normalizada

def _normalizar_codigos_documentos_afetados(
    codigos_documentos_afetados,
):
    """
    Valida e devolve uma nova lista de códigos documentais.

    Uma lista vazia é permitida.

    Isso ocorre quando a concessionária solicita um documento que ainda
    não existe na Homologação, por exemplo:

        anexar procuração;
        apresentar novo formulário;
        incluir documento do titular.
    """

    if codigos_documentos_afetados is None:
        return []

    if not isinstance(codigos_documentos_afetados, list):
        raise ValueError(
            "Os códigos dos Documentos afetados devem formar uma lista."
        )

    codigos_normalizados = []

    for codigo_documento in codigos_documentos_afetados:
        _validar_codigo_positivo(
            codigo_documento,
            "O código do Documento afetado",
        )

        if codigo_documento in codigos_normalizados:
            raise ValueError(
                "Um mesmo Documento não pode aparecer mais de uma vez "
                "na mesma Exigência."
            )

        codigos_normalizados.append(codigo_documento)

    return codigos_normalizados

def tipo_exigencia_valido(tipo):
    """
    Informa se o valor representa um TipoExigencia válido.
    """

    return _converter_tipo_exigencia(tipo) is not None

def status_atendimento_exigencia_valido(status):
    """
    Informa se o valor representa um estado de atendimento válido.
    """

    return _converter_status_atendimento(status) is not None

def criar_dados_exigencia(
    codigo,
    numero_sequencial,
    tipo,
    descricao,
    codigos_documentos_afetados=None,
):
    """
    Cria a estrutura inicial de uma Exigência.

    Parâmetros:
        codigo:
            Identificador único da Exigência dentro da Homologação.

        numero_sequencial:
            Posição da Exigência dentro da Resposta que a contém.

        tipo:
            Categoria padronizada da Exigência.

        descricao:
            Conteúdo individual da solicitação da concessionária.

        codigos_documentos_afetados:
            Lista opcional de Documentos já existentes afetados pela
            Exigência.

    Retorna:
        dict:
            Estrutura inicial da Exigência.

    A Exigência sempre nasce com status PENDENTE.
    """

    _validar_codigo_positivo(
        codigo,
        "O código da Exigência",
    )

    _validar_codigo_positivo(
        numero_sequencial,
        "O número sequencial da Exigência",
    )

    tipo_convertido = _converter_tipo_exigencia(tipo)

    if tipo_convertido is None:
        raise ValueError(
            f"Tipo de Exigência inválido: {tipo!r}."
        )

    descricao_normalizada = _normalizar_descricao(descricao)

    documentos_normalizados = (
        _normalizar_codigos_documentos_afetados(
            codigos_documentos_afetados
        )
    )

    return {
        "codigo": codigo,
        "numero_sequencial": numero_sequencial,
        "tipo": tipo_convertido.value,
        "descricao": descricao_normalizada,
        "codigos_documentos_afetados": documentos_normalizados,
        "status_atendimento": (
            STATUS_INICIAL_ATENDIMENTO_EXIGENCIA.value
        ),
        "codigo_submissao_atendimento": None,
        "data_atendimento": None,
        "responsavel_atendimento": None,
        "observacoes_atendimento": None,
    }

def validar_exigencia(exigencia):
    """
    Valida a estrutura local completa de uma Exigência.

    Esta função não verifica relações externas, como:

    - existência dos Documentos afetados;
    - existência da Submissão de atendimento;
    - pertencimento à mesma Homologação;
    - existência da Resposta que contém a Exigência.
    """

    if not isinstance(exigencia, dict):
        raise ValueError(
            "A Exigência deve ser representada por um dicionário."
        )

    campos_obrigatorios = {
        "codigo",
        "numero_sequencial",
        "tipo",
        "descricao",
        "codigos_documentos_afetados",
        "status_atendimento",
        "codigo_submissao_atendimento",
        "data_atendimento",
        "responsavel_atendimento",
        "observacoes_atendimento",
    }

    campos_ausentes = campos_obrigatorios.difference(exigencia.keys())

    if campos_ausentes:
        raise ValueError(
            "A Exigência possui campos obrigatórios ausentes: "
            f"{sorted(campos_ausentes)}."
        )

    _validar_codigo_positivo(
        exigencia["codigo"],
        "O código da Exigência",
    )

    _validar_codigo_positivo(
        exigencia["numero_sequencial"],
        "O número sequencial da Exigência",
    )

    if not tipo_exigencia_valido(exigencia["tipo"]):
        raise ValueError(
            f"Tipo de Exigência inválido: {exigencia['tipo']!r}."
        )

    _normalizar_descricao(exigencia["descricao"])

    _normalizar_codigos_documentos_afetados(
        exigencia["codigos_documentos_afetados"]
    )

    status_convertido = _converter_status_atendimento(
        exigencia["status_atendimento"]
    )

    if status_convertido is None:
        raise ValueError(
            "Status de atendimento da Exigência inválido: "
            f"{exigencia['status_atendimento']!r}."
        )

    if status_convertido == StatusAtendimentoExigencia.PENDENTE:
        if exigencia["codigo_submissao_atendimento"] is not None:
            raise ValueError(
                "Uma Exigência pendente não pode possuir uma "
                "Submissão de atendimento."
            )

        if exigencia["data_atendimento"] is not None:
            raise ValueError(
                "Uma Exigência pendente não pode possuir data "
                "de atendimento."
            )

        if exigencia["responsavel_atendimento"] is not None:
            raise ValueError(
                "Uma Exigência pendente não pode possuir responsável "
                "pelo atendimento."
            )

    if status_convertido == StatusAtendimentoExigencia.ATENDIDA:
        _validar_codigo_positivo(
            exigencia["codigo_submissao_atendimento"],
            "O código da Submissão de atendimento",
        )

        if not isinstance(exigencia["data_atendimento"], str):
            raise ValueError(
                "A data de atendimento da Exigência é obrigatória."
            )

        if not exigencia["data_atendimento"].strip():
            raise ValueError(
                "A data de atendimento da Exigência é obrigatória."
            )

        if not isinstance(
            exigencia["responsavel_atendimento"],
            str,
        ):
            raise ValueError(
                "O responsável pelo atendimento da Exigência "
                "é obrigatório."
            )

        if not exigencia["responsavel_atendimento"].strip():
            raise ValueError(
                "O responsável pelo atendimento da Exigência "
                "é obrigatório."
            )

    return True

def transicao_status_exigencia_permitida(
    status_atual,
    novo_status,
):
    """
    Verifica se uma transição de atendimento é permitida.
    """

    status_atual_convertido = _converter_status_atendimento(
        status_atual
    )

    novo_status_convertido = _converter_status_atendimento(
        novo_status
    )

    if status_atual_convertido is None:
        return False

    if novo_status_convertido is None:
        return False

    destinos_permitidos = (
        TRANSICOES_STATUS_ATENDIMENTO_EXIGENCIA[
            status_atual_convertido
        ]
    )

    return novo_status_convertido in destinos_permitidos

def validar_transicao_status_exigencia(
    status_atual,
    novo_status,
):
    """
    Valida uma transição do atendimento da Exigência.

    Retorna True quando permitida e lança ValueError quando inválida.
    """

    status_atual_convertido = _converter_status_atendimento(
        status_atual
    )

    novo_status_convertido = _converter_status_atendimento(
        novo_status
    )

    if status_atual_convertido is None:
        raise ValueError(
            "Status atual da Exigência inválido: "
            f"{status_atual!r}."
        )

    if novo_status_convertido is None:
        raise ValueError(
            "Novo status da Exigência inválido: "
            f"{novo_status!r}."
        )

    if not transicao_status_exigencia_permitida(
        status_atual_convertido,
        novo_status_convertido,
    ):
        raise ValueError(
            "Transição do atendimento da Exigência não permitida: "
            f"{status_atual_convertido.value} -> "
            f"{novo_status_convertido.value}."
        )

    return True

def exigencia_esta_pendente(exigencia):
    """
    Informa se a Exigência está pendente.
    """

    if not isinstance(exigencia, dict):
        return False

    status = _converter_status_atendimento(
        exigencia.get("status_atendimento")
    )

    return status == StatusAtendimentoExigencia.PENDENTE

def exigencia_esta_atendida(exigencia):
    """
    Informa se a Exigência está atendida.
    """

    if not isinstance(exigencia, dict):
        return False

    status = _converter_status_atendimento(
        exigencia.get("status_atendimento")
    )

    return status == StatusAtendimentoExigencia.ATENDIDA

def status_atendimento_exigencia_terminal(status):
    """
    Informa se o estado de atendimento é terminal.
    """

    status_convertido = _converter_status_atendimento(status)

    if status_convertido is None:
        return False

    return (
        status_convertido
        in STATUS_TERMINAIS_ATENDIMENTO_EXIGENCIA
    )

def validar_compatibilidade_exigencia_submissao(
    tipo_exigencia,
    tipo_submissao,
):
    """
    Valida a compatibilidade entre uma Exigência e uma nova Submissão.

    Nesta etapa, tipo_submissao é recebido como texto:

        COMPLEMENTACAO
        REENVIO

    A Submissão INICIAL não pode atender Exigências.

    Regra bloqueante definitiva:

        REENVIO_INTEGRAL
        +
        COMPLEMENTACAO
        =
        inválido

    A função também aplica as compatibilidades formais registradas na
    matriz do domínio.
    """

    tipo_exigencia_convertido = _converter_tipo_exigencia(
        tipo_exigencia
    )

    if tipo_exigencia_convertido is None:
        raise ValueError(
            f"Tipo de Exigência inválido: {tipo_exigencia!r}."
        )

    if hasattr(tipo_submissao, "value"):
        tipo_submissao_normalizado = tipo_submissao.value
    else:
        tipo_submissao_normalizado = tipo_submissao

    if not isinstance(tipo_submissao_normalizado, str):
        raise ValueError(
            "O tipo da Submissão deve ser um texto válido."
        )

    tipo_submissao_normalizado = (
        tipo_submissao_normalizado.strip().upper()
    )

    tipos_submissao_validos = {
        "COMPLEMENTACAO",
        "REENVIO",
    }

    if tipo_submissao_normalizado not in tipos_submissao_validos:
        raise ValueError(
            "Apenas uma Complementação ou um Reenvio pode "
            "atender Exigências."
        )

    tipos_compativeis = (
        COMPATIBILIDADE_TIPO_EXIGENCIA_SUBMISSAO[
            tipo_exigencia_convertido
        ]
    )

    if tipo_submissao_normalizado not in tipos_compativeis:
        raise ValueError(
            "O tipo da Submissão é incompatível com a Exigência: "
            f"{tipo_exigencia_convertido.value} não pode ser atendida "
            f"por {tipo_submissao_normalizado}."
        )

    return True

def obter_rotulo_tipo_exigencia(tipo):
    """
    Retorna o rótulo amigável do tipo da Exigência.
    """

    tipo_convertido = _converter_tipo_exigencia(tipo)

    if tipo_convertido is None:
        return None

    return ROTULOS_TIPO_EXIGENCIA[tipo_convertido]

def obter_rotulo_status_atendimento_exigencia(status):
    """
    Retorna o rótulo amigável do estado de atendimento.
    """

    status_convertido = _converter_status_atendimento(status)

    if status_convertido is None:
        return None

    return ROTULOS_STATUS_ATENDIMENTO_EXIGENCIA[
        status_convertido
    ]