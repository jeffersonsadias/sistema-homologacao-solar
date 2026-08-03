"""
Regras locais das Respostas emitidas pela concessionária.

Uma Resposta representa um retorno formal recebido depois do envio
de uma Submissão.

Tipos existentes:

- recebimento confirmado;
- análise iniciada;
- exigência;
- aprovação;
- rejeição.

Este módulo é responsável por:

- definir os tipos de Resposta;
- definir o caráter das Rejeições;
- criar as estruturas locais das Respostas;
- validar seus campos e datas;
- validar as Exigências internas de uma Resposta;
- determinar o status de análise resultante de cada tipo.

Este módulo não modifica diretamente:

- a Submissão;
- a Homologação;
- as Movimentações;
- o estado geral do processo.

O registro das Respostas, a validação de suas relações com a
Submissão e os reflexos sobre a Homologação pertencem ao
Aggregate Root:

    app/dominio/homologacoes.py
"""

from datetime import date, datetime
from enum import Enum

from app.dominio.exigencias_concessionaria import validar_exigencia
from app.dominio.status_submissao import StatusAnaliseSubmissao


class TipoRespostaConcessionaria(str, Enum):
    """
    Tipos de retorno que podem ser registrados para uma Submissão.
    """

    RECEBIMENTO_CONFIRMADO = "RECEBIMENTO_CONFIRMADO"
    ANALISE_INICIADA = "ANALISE_INICIADA"
    EXIGENCIA = "EXIGENCIA"
    APROVACAO = "APROVACAO"
    REJEICAO = "REJEICAO"


class CaraterRejeicao(str, Enum):
    """
    Classificação do efeito de uma Rejeição.

    CORRIGIVEL:
        A causa pode ser corrigida e gerar um novo Reenvio.

    DEFINITIVA:
        A decisão impede a continuidade normal daquela tentativa.

    NAO_INFORMADO:
        A concessionária não informou claramente o caráter da Rejeição.
    """

    CORRIGIVEL = "CORRIGIVEL"
    DEFINITIVA = "DEFINITIVA"
    NAO_INFORMADO = "NAO_INFORMADO"


STATUS_ANALISE_POR_TIPO_RESPOSTA = {
    TipoRespostaConcessionaria.RECEBIMENTO_CONFIRMADO:
        StatusAnaliseSubmissao.RECEBIDA,

    TipoRespostaConcessionaria.ANALISE_INICIADA:
        StatusAnaliseSubmissao.EM_ANALISE,

    TipoRespostaConcessionaria.EXIGENCIA:
        StatusAnaliseSubmissao.COM_EXIGENCIA,

    TipoRespostaConcessionaria.APROVACAO:
        StatusAnaliseSubmissao.APROVADA,

    TipoRespostaConcessionaria.REJEICAO:
        StatusAnaliseSubmissao.REJEITADA,
}


ROTULOS_TIPO_RESPOSTA = {
    TipoRespostaConcessionaria.RECEBIMENTO_CONFIRMADO:
        "Recebimento confirmado",

    TipoRespostaConcessionaria.ANALISE_INICIADA:
        "Análise iniciada",

    TipoRespostaConcessionaria.EXIGENCIA:
        "Exigência",

    TipoRespostaConcessionaria.APROVACAO:
        "Aprovação",

    TipoRespostaConcessionaria.REJEICAO:
        "Rejeição",
}


ROTULOS_CARATER_REJEICAO = {
    CaraterRejeicao.CORRIGIVEL: "Corrigível",
    CaraterRejeicao.DEFINITIVA: "Definitiva",
    CaraterRejeicao.NAO_INFORMADO: "Não informado",
}


def _converter_tipo_resposta(tipo):
    """
    Converte um enum ou texto válido em TipoRespostaConcessionaria.
    """

    if isinstance(tipo, TipoRespostaConcessionaria):
        return tipo

    try:
        return TipoRespostaConcessionaria(tipo)
    except (ValueError, TypeError):
        return None

def _converter_carater_rejeicao(carater):
    """
    Converte um enum ou texto válido em CaraterRejeicao.
    """

    if isinstance(carater, CaraterRejeicao):
        return carater

    try:
        return CaraterRejeicao(carater)
    except (ValueError, TypeError):
        return None

def _validar_inteiro_positivo(valor, nome_campo):
    """
    Valida códigos e números sequenciais positivos.
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

def _normalizar_texto_obrigatorio(valor, nome_campo):
    """
    Valida e normaliza um texto obrigatório.
    """

    if not isinstance(valor, str):
        raise ValueError(
            f"{nome_campo} deve ser um texto."
        )

    valor_normalizado = valor.strip()

    if not valor_normalizado:
        raise ValueError(
            f"{nome_campo} é obrigatório."
        )

    return valor_normalizado

def _normalizar_texto_opcional(valor, nome_campo):
    """
    Valida e normaliza um texto opcional.

    None permanece None.

    Um texto vazio também é normalizado para None.
    """

    if valor is None:
        return None

    if not isinstance(valor, str):
        raise ValueError(
            f"{nome_campo} deve ser um texto ou None."
        )

    valor_normalizado = valor.strip()

    if not valor_normalizado:
        return None

    return valor_normalizado

def _converter_data_iso(valor, nome_campo):
    """
    Valida uma data e devolve seu valor no formato ISO.

    Formatos aceitos:

    - texto YYYY-MM-DD;
    - objeto datetime.date;
    - objeto datetime.datetime.
    """

    if isinstance(valor, datetime):
        return valor.date().isoformat()

    if isinstance(valor, date):
        return valor.isoformat()

    if not isinstance(valor, str):
        raise ValueError(
            f"{nome_campo} deve ser uma data válida."
        )

    valor_normalizado = valor.strip()

    try:
        data_convertida = date.fromisoformat(valor_normalizado)
    except ValueError as erro:
        raise ValueError(
            f"{nome_campo} deve usar o formato YYYY-MM-DD."
        ) from erro

    return data_convertida.isoformat()

def validar_datas_resposta(
    data_resposta,
    data_registro,
):
    """
    Valida as datas de uma Resposta.

    A data de registro não pode ser anterior à data informada
    pela concessionária.

    Retorna:
        tuple[str, str]:
            Data da Resposta e data do registro normalizadas.
    """

    data_resposta_normalizada = _converter_data_iso(
        data_resposta,
        "A data da Resposta",
    )

    data_registro_normalizada = _converter_data_iso(
        data_registro,
        "A data de registro",
    )

    data_resposta_convertida = date.fromisoformat(
        data_resposta_normalizada
    )

    data_registro_convertida = date.fromisoformat(
        data_registro_normalizada
    )

    if data_registro_convertida < data_resposta_convertida:
        raise ValueError(
            "A data de registro não pode ser anterior "
            "à data da Resposta."
        )

    return (
        data_resposta_normalizada,
        data_registro_normalizada,
    )

def tipo_resposta_concessionaria_valido(tipo):
    """
    Informa se um tipo de Resposta é válido.
    """

    return _converter_tipo_resposta(tipo) is not None

def carater_rejeicao_valido(carater):
    """
    Informa se um caráter de Rejeição é válido.
    """

    return _converter_carater_rejeicao(carater) is not None

def obter_status_resultante_resposta(tipo_resposta):
    """
    Retorna o status da análise correspondente ao tipo de Resposta.

    O retorno é um objeto StatusAnaliseSubmissao.

    Retorna None quando o tipo é inválido.
    """

    tipo_convertido = _converter_tipo_resposta(tipo_resposta)

    if tipo_convertido is None:
        return None

    return STATUS_ANALISE_POR_TIPO_RESPOSTA[tipo_convertido]

def _criar_dados_base_resposta(
    codigo,
    numero_sequencial,
    tipo,
    data_resposta,
    data_registro,
    responsavel_registro,
    descricao=None,
    referencia_arquivo=None,
):
    """
    Cria os campos comuns de qualquer Resposta.

    Esta função é privada porque uma Resposta deve ser criada por uma
    função específica, como:

        criar_dados_resposta_aprovacao()
        criar_dados_resposta_rejeicao()
    """

    _validar_inteiro_positivo(
        codigo,
        "O código da Resposta",
    )

    _validar_inteiro_positivo(
        numero_sequencial,
        "O número sequencial da Resposta",
    )

    tipo_convertido = _converter_tipo_resposta(tipo)

    if tipo_convertido is None:
        raise ValueError(
            f"Tipo de Resposta inválido: {tipo!r}."
        )

    (
        data_resposta_normalizada,
        data_registro_normalizada,
    ) = validar_datas_resposta(
        data_resposta,
        data_registro,
    )

    responsavel_normalizado = _normalizar_texto_obrigatorio(
        responsavel_registro,
        "O responsável pelo registro",
    )

    descricao_normalizada = _normalizar_texto_opcional(
        descricao,
        "A descrição da Resposta",
    )

    referencia_normalizada = _normalizar_texto_opcional(
        referencia_arquivo,
        "A referência do arquivo",
    )

    return {
        "codigo": codigo,
        "numero_sequencial": numero_sequencial,
        "tipo": tipo_convertido.value,
        "data_resposta": data_resposta_normalizada,
        "data_registro": data_registro_normalizada,
        "responsavel_registro": responsavel_normalizado,
        "descricao": descricao_normalizada,
        "referencia_arquivo": referencia_normalizada,
        "prazo_atendimento": None,
        "identificador_aprovacao": None,
        "carater_rejeicao": None,
        "exigencias": [],
    }

def criar_dados_resposta_recebimento(
    codigo,
    numero_sequencial,
    data_resposta,
    data_registro,
    responsavel_registro,
    descricao=None,
    referencia_arquivo=None,
):
    """
    Cria uma confirmação de recebimento da Submissão.
    """

    return _criar_dados_base_resposta(
        codigo=codigo,
        numero_sequencial=numero_sequencial,
        tipo=TipoRespostaConcessionaria.RECEBIMENTO_CONFIRMADO,
        data_resposta=data_resposta,
        data_registro=data_registro,
        responsavel_registro=responsavel_registro,
        descricao=descricao,
        referencia_arquivo=referencia_arquivo,
    )

def criar_dados_resposta_inicio_analise(
    codigo,
    numero_sequencial,
    data_resposta,
    data_registro,
    responsavel_registro,
    descricao=None,
    referencia_arquivo=None,
):
    """
    Cria uma Resposta que registra o início da análise.
    """

    return _criar_dados_base_resposta(
        codigo=codigo,
        numero_sequencial=numero_sequencial,
        tipo=TipoRespostaConcessionaria.ANALISE_INICIADA,
        data_resposta=data_resposta,
        data_registro=data_registro,
        responsavel_registro=responsavel_registro,
        descricao=descricao,
        referencia_arquivo=referencia_arquivo,
    )

def criar_dados_resposta_exigencia(
    codigo,
    numero_sequencial,
    data_resposta,
    data_registro,
    responsavel_registro,
    descricao,
    exigencias,
    prazo_atendimento=None,
    referencia_arquivo=None,
):
    """
    Cria uma Resposta contendo uma ou várias Exigências.
    """

    descricao_normalizada = _normalizar_texto_obrigatorio(
        descricao,
        "A descrição da Resposta de Exigência",
    )

    if not isinstance(exigencias, list):
        raise ValueError(
            "As Exigências devem formar uma lista."
        )

    if not exigencias:
        raise ValueError(
            "Uma Resposta de Exigência deve possuir "
            "pelo menos uma Exigência."
        )

    exigencias_copiadas = []
    codigos_encontrados = set()
    numeros_encontrados = set()

    for exigencia in exigencias:
        validar_exigencia(exigencia)

        codigo_exigencia = exigencia["codigo"]
        numero_exigencia = exigencia["numero_sequencial"]

        if codigo_exigencia in codigos_encontrados:
            raise ValueError(
                "Existem códigos de Exigência duplicados "
                "na mesma Resposta."
            )

        if numero_exigencia in numeros_encontrados:
            raise ValueError(
                "Existem números sequenciais de Exigência "
                "duplicados na mesma Resposta."
            )

        codigos_encontrados.add(codigo_exigencia)
        numeros_encontrados.add(numero_exigencia)

        exigencias_copiadas.append(exigencia.copy())

    resposta = _criar_dados_base_resposta(
        codigo=codigo,
        numero_sequencial=numero_sequencial,
        tipo=TipoRespostaConcessionaria.EXIGENCIA,
        data_resposta=data_resposta,
        data_registro=data_registro,
        responsavel_registro=responsavel_registro,
        descricao=descricao_normalizada,
        referencia_arquivo=referencia_arquivo,
    )

    resposta["exigencias"] = exigencias_copiadas
    resposta["prazo_atendimento"] = _normalizar_texto_opcional(
        prazo_atendimento,
        "O prazo de atendimento",
    )

    return resposta

def criar_dados_resposta_aprovacao(
    codigo,
    numero_sequencial,
    data_resposta,
    data_registro,
    responsavel_registro,
    descricao=None,
    identificador_aprovacao=None,
    referencia_arquivo=None,
):
    """
    Cria uma Resposta de aprovação.

    O identificador de aprovação é opcional, pois nem todas as
    concessionárias utilizam o mesmo tipo de código ou documento.
    """

    resposta = _criar_dados_base_resposta(
        codigo=codigo,
        numero_sequencial=numero_sequencial,
        tipo=TipoRespostaConcessionaria.APROVACAO,
        data_resposta=data_resposta,
        data_registro=data_registro,
        responsavel_registro=responsavel_registro,
        descricao=descricao,
        referencia_arquivo=referencia_arquivo,
    )

    resposta["identificador_aprovacao"] = (
        _normalizar_texto_opcional(
            identificador_aprovacao,
            "O identificador da aprovação",
        )
    )

    return resposta

def criar_dados_resposta_rejeicao(
    codigo,
    numero_sequencial,
    data_resposta,
    data_registro,
    responsavel_registro,
    descricao,
    carater_rejeicao,
    referencia_arquivo=None,
):
    """
    Cria uma Resposta de Rejeição.
    """

    descricao_normalizada = _normalizar_texto_obrigatorio(
        descricao,
        "A descrição da Rejeição",
    )

    carater_convertido = _converter_carater_rejeicao(
        carater_rejeicao
    )

    if carater_convertido is None:
        raise ValueError(
            "Caráter da Rejeição inválido: "
            f"{carater_rejeicao!r}."
        )

    resposta = _criar_dados_base_resposta(
        codigo=codigo,
        numero_sequencial=numero_sequencial,
        tipo=TipoRespostaConcessionaria.REJEICAO,
        data_resposta=data_resposta,
        data_registro=data_registro,
        responsavel_registro=responsavel_registro,
        descricao=descricao_normalizada,
        referencia_arquivo=referencia_arquivo,
    )

    resposta["carater_rejeicao"] = carater_convertido.value

    return resposta

def validar_resposta_concessionaria(resposta):
    """
    Valida a estrutura local completa de uma Resposta.

    A função não verifica:

    - existência da Submissão;
    - pertencimento à Homologação;
    - compatibilidade com o status operacional;
    - sequência histórica das Respostas.
    """

    if not isinstance(resposta, dict):
        raise ValueError(
            "A Resposta deve ser representada por um dicionário."
        )

    campos_obrigatorios = {
        "codigo",
        "numero_sequencial",
        "tipo",
        "data_resposta",
        "data_registro",
        "responsavel_registro",
        "descricao",
        "referencia_arquivo",
        "prazo_atendimento",
        "identificador_aprovacao",
        "carater_rejeicao",
        "exigencias",
    }

    campos_ausentes = campos_obrigatorios.difference(
        resposta.keys()
    )

    if campos_ausentes:
        raise ValueError(
            "A Resposta possui campos obrigatórios ausentes: "
            f"{sorted(campos_ausentes)}."
        )

    _validar_inteiro_positivo(
        resposta["codigo"],
        "O código da Resposta",
    )

    _validar_inteiro_positivo(
        resposta["numero_sequencial"],
        "O número sequencial da Resposta",
    )

    tipo_convertido = _converter_tipo_resposta(
        resposta["tipo"]
    )

    if tipo_convertido is None:
        raise ValueError(
            f"Tipo de Resposta inválido: {resposta['tipo']!r}."
        )

    validar_datas_resposta(
        resposta["data_resposta"],
        resposta["data_registro"],
    )

    _normalizar_texto_obrigatorio(
        resposta["responsavel_registro"],
        "O responsável pelo registro",
    )

    _normalizar_texto_opcional(
        resposta["referencia_arquivo"],
        "A referência do arquivo",
    )

    if not isinstance(resposta["exigencias"], list):
        raise ValueError(
            "As Exigências da Resposta devem formar uma lista."
        )

    if tipo_convertido == TipoRespostaConcessionaria.EXIGENCIA:
        _normalizar_texto_obrigatorio(
            resposta["descricao"],
            "A descrição da Resposta de Exigência",
        )

        if not resposta["exigencias"]:
            raise ValueError(
                "Uma Resposta de Exigência deve possuir "
                "pelo menos uma Exigência."
            )

        for exigencia in resposta["exigencias"]:
            validar_exigencia(exigencia)

        if resposta["carater_rejeicao"] is not None:
            raise ValueError(
                "Uma Resposta de Exigência não pode possuir "
                "caráter de Rejeição."
            )

        if resposta["identificador_aprovacao"] is not None:
            raise ValueError(
                "Uma Resposta de Exigência não pode possuir "
                "identificador de aprovação."
            )

    elif tipo_convertido == TipoRespostaConcessionaria.APROVACAO:
        if resposta["exigencias"]:
            raise ValueError(
                "Uma aprovação não pode conter Exigências."
            )

        if resposta["carater_rejeicao"] is not None:
            raise ValueError(
                "Uma aprovação não pode possuir "
                "caráter de Rejeição."
            )

        if resposta["prazo_atendimento"] is not None:
            raise ValueError(
                "Uma aprovação não pode possuir "
                "prazo de atendimento."
            )

    elif tipo_convertido == TipoRespostaConcessionaria.REJEICAO:
        _normalizar_texto_obrigatorio(
            resposta["descricao"],
            "A descrição da Rejeição",
        )

        if not carater_rejeicao_valido(
            resposta["carater_rejeicao"]
        ):
            raise ValueError(
                "Uma Rejeição deve possuir um caráter válido."
            )

        if resposta["exigencias"]:
            raise ValueError(
                "Uma Rejeição não pode conter Exigências."
            )

        if resposta["identificador_aprovacao"] is not None:
            raise ValueError(
                "Uma Rejeição não pode possuir "
                "identificador de aprovação."
            )

        if resposta["prazo_atendimento"] is not None:
            raise ValueError(
                "Uma Rejeição não pode possuir "
                "prazo de atendimento."
            )

    else:
        if resposta["exigencias"]:
            raise ValueError(
                "Este tipo de Resposta não pode conter Exigências."
            )

        if resposta["carater_rejeicao"] is not None:
            raise ValueError(
                "Este tipo de Resposta não pode possuir "
                "caráter de Rejeição."
            )

        if resposta["identificador_aprovacao"] is not None:
            raise ValueError(
                "Este tipo de Resposta não pode possuir "
                "identificador de aprovação."
            )

        if resposta["prazo_atendimento"] is not None:
            raise ValueError(
                "Este tipo de Resposta não pode possuir "
                "prazo de atendimento."
            )

    return True

def obter_rotulo_tipo_resposta(tipo):
    """
    Retorna o rótulo amigável de um tipo de Resposta.
    """

    tipo_convertido = _converter_tipo_resposta(tipo)

    if tipo_convertido is None:
        return None

    return ROTULOS_TIPO_RESPOSTA[tipo_convertido]

def obter_rotulo_carater_rejeicao(carater):
    """
    Retorna o rótulo amigável do caráter da Rejeição.
    """

    carater_convertido = _converter_carater_rejeicao(carater)

    if carater_convertido is None:
        return None

    return ROTULOS_CARATER_REJEICAO[carater_convertido]