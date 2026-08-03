"""
Regras locais das Submissões de uma Homologação.

Uma Submissão representa um pacote formal preparado para envio à
concessionária.

Tipos existentes:

- INICIAL:
    primeiro pacote apresentado no processo;

- COMPLEMENTACAO:
    acrescenta informações ou Documentos sem substituir
    integralmente a apresentação anterior;

- REENVIO:
    corrige ou reapresenta informações anteriormente enviadas.

Este módulo é responsável por:

- definir os tipos de Submissão;
- definir os canais de envio;
- criar referências documentais;
- criar a estrutura inicial de uma Submissão;
- validar seu pacote documental;
- validar seus dados locais de envio e protocolo;
- validar as Respostas armazenadas;
- validar seus estados locais;
- garantir a coerência interna do versionamento e das origens
  informadas.

Este módulo não é responsável por:

- adicionar uma Submissão à Homologação;
- gerar códigos dentro do agregado;
- verificar a existência real dos Documentos referenciados;
- verificar a existência da Submissão ou da Resposta de origem;
- alterar Exigências;
- alterar o estado geral da Homologação;
- registrar Movimentações.

As regras relacionais e as operações coordenadas pertencem ao
Aggregate Root:

    app/dominio/homologacoes.py
"""

from datetime import date, datetime
from enum import Enum

from app.dominio.respostas_concessionaria import (
    obter_status_resultante_resposta,
    validar_resposta_concessionaria,
)
from app.dominio.status_submissao import (
    STATUS_ANALISE_INICIAL,
    STATUS_OPERACIONAL_INICIAL,
    StatusAnaliseSubmissao,
    StatusOperacionalSubmissao,
    status_analise_submissao_valido,
    status_operacional_submissao_valido,
)


class TipoSubmissao(str, Enum):
    """
    Tipos de Submissão existentes no processo.
    """

    INICIAL = "INICIAL"
    COMPLEMENTACAO = "COMPLEMENTACAO"
    REENVIO = "REENVIO"

class CanalEnvioSubmissao(str, Enum):
    """
    Canais pelos quais uma Submissão pode ser enviada.
    """

    PORTAL = "PORTAL"
    EMAIL = "EMAIL"
    PRESENCIAL = "PRESENCIAL"
    OUTRO = "OUTRO"

ROTULOS_TIPO_SUBMISSAO = {
    TipoSubmissao.INICIAL: "Inicial",
    TipoSubmissao.COMPLEMENTACAO: "Complementação",
    TipoSubmissao.REENVIO: "Reenvio",
}

ROTULOS_CANAL_ENVIO_SUBMISSAO = {
    CanalEnvioSubmissao.PORTAL: "Portal",
    CanalEnvioSubmissao.EMAIL: "E-mail",
    CanalEnvioSubmissao.PRESENCIAL: "Presencial",
    CanalEnvioSubmissao.OUTRO: "Outro",
}

def _converter_tipo_submissao(tipo):
    """
    Converte um enum ou texto válido em TipoSubmissao.
    """

    if isinstance(tipo, TipoSubmissao):
        return tipo

    try:
        return TipoSubmissao(tipo)
    except (ValueError, TypeError):
        return None

def _converter_canal_envio(canal):
    """
    Converte um enum ou texto válido em CanalEnvioSubmissao.
    """

    if isinstance(canal, CanalEnvioSubmissao):
        return canal

    try:
        return CanalEnvioSubmissao(canal)
    except (ValueError, TypeError):
        return None

def _validar_inteiro_positivo(valor, nome_campo):
    """
    Valida um número inteiro positivo.

    bool é rejeitado porque, em Python, bool é uma subclasse de int.
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

    None ou texto vazio resultam em None.
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
    Converte uma data válida para texto no formato ISO: YYYY-MM-DD.
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

def _normalizar_data_opcional(valor, nome_campo):
    """
    Normaliza uma data opcional.
    """

    if valor is None:
        return None

    return _converter_data_iso(valor, nome_campo)

def tipo_submissao_valido(tipo):
    """
    Informa se um tipo de Submissão é válido.
    """

    return _converter_tipo_submissao(tipo) is not None

def canal_envio_submissao_valido(canal):
    """
    Informa se um canal de envio é válido.
    """

    return _converter_canal_envio(canal) is not None

def criar_referencia_documento(
    codigo_documento,
    numero_versao,
):
    """
    Cria a referência de uma versão documental enviada no pacote.

    A Submissão não armazena uma cópia completa do Documento.

    Ela registra apenas:

    - o código do Documento;
    - o número exato da versão enviada.

    Isso permite preservar historicamente qual versão foi submetida.
    """

    _validar_inteiro_positivo(
        codigo_documento,
        "O código do Documento",
    )

    _validar_inteiro_positivo(
        numero_versao,
        "O número da versão documental",
    )

    return {
        "codigo_documento": codigo_documento,
        "numero_versao": numero_versao,
    }

def validar_referencia_documento(referencia):
    """
    Valida uma referência documental.
    """

    if not isinstance(referencia, dict):
        raise ValueError(
            "A referência documental deve ser um dicionário."
        )

    campos_obrigatorios = {
        "codigo_documento",
        "numero_versao",
    }

    campos_ausentes = campos_obrigatorios.difference(
        referencia.keys()
    )

    if campos_ausentes:
        raise ValueError(
            "A referência documental possui campos ausentes: "
            f"{sorted(campos_ausentes)}."
        )

    _validar_inteiro_positivo(
        referencia["codigo_documento"],
        "O código do Documento",
    )

    _validar_inteiro_positivo(
        referencia["numero_versao"],
        "O número da versão documental",
    )

    return True

def _normalizar_pacote_documental(pacote_documental):
    """
    Valida e copia o pacote documental.

    Um Documento não pode aparecer mais de uma vez no mesmo pacote,
    mesmo que as referências apontem para versões diferentes.

    Isso garante que cada pacote indique apenas uma versão enviada
    para cada Documento.
    """

    if pacote_documental is None:
        return []

    if not isinstance(pacote_documental, list):
        raise ValueError(
            "O pacote documental deve ser uma lista."
        )

    pacote_normalizado = []
    codigos_documentos = set()

    for referencia in pacote_documental:
        validar_referencia_documento(referencia)

        codigo_documento = referencia["codigo_documento"]

        if codigo_documento in codigos_documentos:
            raise ValueError(
                "Um mesmo Documento não pode aparecer mais de uma vez "
                "no pacote da Submissão."
            )

        codigos_documentos.add(codigo_documento)
        pacote_normalizado.append(referencia.copy())

    return pacote_normalizado

def _normalizar_codigos_exigencias(codigos_exigencias):
    """
    Valida os códigos das Exigências relacionadas à Submissão.
    """

    if codigos_exigencias is None:
        return []

    if not isinstance(codigos_exigencias, list):
        raise ValueError(
            "Os códigos das Exigências devem formar uma lista."
        )

    codigos_normalizados = []

    for codigo_exigencia in codigos_exigencias:
        _validar_inteiro_positivo(
            codigo_exigencia,
            "O código da Exigência",
        )

        if codigo_exigencia in codigos_normalizados:
            raise ValueError(
                "Uma mesma Exigência não pode ser relacionada "
                "mais de uma vez à Submissão."
            )

        codigos_normalizados.append(codigo_exigencia)

    return codigos_normalizados

def _normalizar_respostas(respostas):
    """
    Valida e copia a coleção de Respostas da Submissão.
    """

    if respostas is None:
        return []

    if not isinstance(respostas, list):
        raise ValueError(
            "As Respostas devem formar uma lista."
        )

    respostas_normalizadas = []
    codigos_encontrados = set()
    sequencias_encontradas = set()

    for resposta in respostas:
        validar_resposta_concessionaria(resposta)

        codigo_resposta = resposta["codigo"]
        numero_sequencial = resposta["numero_sequencial"]

        if codigo_resposta in codigos_encontrados:
            raise ValueError(
                "Existem códigos de Resposta duplicados "
                "na mesma Submissão."
            )

        if numero_sequencial in sequencias_encontradas:
            raise ValueError(
                "Existem números sequenciais de Resposta duplicados "
                "na mesma Submissão."
            )

        codigos_encontrados.add(codigo_resposta)
        sequencias_encontradas.add(numero_sequencial)
        respostas_normalizadas.append(resposta.copy())

    return respostas_normalizadas

def criar_dados_submissao(
    codigo,
    numero_sequencial,
    tipo,
    data_criacao,
    responsavel_criacao,
    pacote_documental=None,
    codigo_submissao_origem=None,
    codigo_resposta_origem=None,
    codigos_exigencias_relacionadas=None,
    observacoes=None,
):
    """
    Cria a estrutura inicial de uma Submissão.

    Regras:

    - a Submissão Inicial não possui origem;
    - Complementação e Reenvio devem possuir uma
      Submissão de origem;
    - Complementação e Reenvio devem informar
      qual Resposta originou a nova Submissão;
    - a Submissão nasce em EM_PREPARACAO;
    - a análise nasce em SEM_RESPOSTA;
    - nenhum dado de envio ou protocolo existe inicialmente.
    """

    _validar_inteiro_positivo(
        codigo,
        "O código da Submissão",
    )

    _validar_inteiro_positivo(
        numero_sequencial,
        "O número sequencial da Submissão",
    )

    tipo_convertido = _converter_tipo_submissao(tipo)

    if tipo_convertido is None:
        raise ValueError(
            f"Tipo de Submissão inválido: {tipo!r}."
        )

    data_criacao_normalizada = _converter_data_iso(
        data_criacao,
        "A data de criação",
    )

    responsavel_normalizado = _normalizar_texto_obrigatorio(
        responsavel_criacao,
        "O responsável pela criação",
    )

    pacote_normalizado = _normalizar_pacote_documental(
        pacote_documental
    )

    exigencias_normalizadas = _normalizar_codigos_exigencias(
        codigos_exigencias_relacionadas
    )

    observacoes_normalizadas = _normalizar_texto_opcional(
        observacoes,
        "As observações da Submissão",
    )

    if codigo_submissao_origem is not None:
        _validar_inteiro_positivo(
            codigo_submissao_origem,
            "O código da Submissão de origem",
        )

    if codigo_resposta_origem is not None:
        _validar_inteiro_positivo(
            codigo_resposta_origem,
            "O código da Resposta de origem",
        )

    if tipo_convertido == TipoSubmissao.INICIAL:

        if codigo_submissao_origem is not None:
            raise ValueError(
                "Uma Submissão Inicial não pode possuir "
                "Submissão de origem."
            )

        if codigo_resposta_origem is not None:
            raise ValueError(
                "Uma Submissão Inicial não pode possuir "
                "Resposta de origem."
            )

        if exigencias_normalizadas:
            raise ValueError(
                "Uma Submissão Inicial não pode atender Exigências."
            )

    else:

        if codigo_submissao_origem is None:
            raise ValueError(
                "Complementação e Reenvio devem possuir "
                "Submissão de origem."
            )

        if codigo_resposta_origem is None:
            raise ValueError(
                "Complementação e Reenvio devem possuir "
                "Resposta de origem."
            )

        if codigo_submissao_origem == codigo:
            raise ValueError(
                "Uma Submissão não pode apontar para si mesma "
                "como origem."
            )

        if (
            tipo_convertido == TipoSubmissao.COMPLEMENTACAO
            and not exigencias_normalizadas
        ):
            raise ValueError(
                "Uma Complementação deve informar as "
                "Exigências atendidas."
            )

    return {
        "codigo": codigo,
        "numero_sequencial": numero_sequencial,
        "tipo": tipo_convertido.value,
        "codigo_submissao_origem": codigo_submissao_origem,
        "codigo_resposta_origem": codigo_resposta_origem,
        "data_criacao": data_criacao_normalizada,
        "responsavel_criacao": responsavel_normalizado,
        "pacote_documental": pacote_normalizado,
        "codigos_exigencias_relacionadas": exigencias_normalizadas,
        "status_operacional": STATUS_OPERACIONAL_INICIAL.value,
        "status_analise": STATUS_ANALISE_INICIAL.value,
        "canal_envio": None,
        "data_envio": None,
        "responsavel_envio": None,
        "protocolo": None,
        "data_protocolo": None,
        "respostas": [],
        "observacoes": observacoes_normalizadas,
    }

def validar_submissao(submissao):
    """
    Valida a estrutura local completa de uma Submissão.

    Esta função não verifica relações externas, como:

    - existência da Submissão de origem;
    - existência da Resposta de origem;
    - existência dos Documentos;
    - existência das versões documentais;
    - existência das Exigências;
    - pertencimento à mesma Homologação.
    """

    if not isinstance(submissao, dict):
        raise ValueError(
            "A Submissão deve ser representada por um dicionário."
        )

    campos_obrigatorios = {
        "codigo",
        "numero_sequencial",
        "tipo",
        "codigo_submissao_origem",
        "codigo_resposta_origem",
        "data_criacao",
        "responsavel_criacao",
        "pacote_documental",
        "codigos_exigencias_relacionadas",
        "status_operacional",
        "status_analise",
        "canal_envio",
        "data_envio",
        "responsavel_envio",
        "protocolo",
        "data_protocolo",
        "respostas",
        "observacoes",
    }

    campos_ausentes = campos_obrigatorios.difference(
        submissao.keys()
    )

    if campos_ausentes:
        raise ValueError(
            "A Submissão possui campos obrigatórios ausentes: "
            f"{sorted(campos_ausentes)}."
        )

    _validar_inteiro_positivo(
        submissao["codigo"],
        "O código da Submissão",
    )

    _validar_inteiro_positivo(
        submissao["numero_sequencial"],
        "O número sequencial da Submissão",
    )

    tipo_convertido = _converter_tipo_submissao(
        submissao["tipo"]
    )

    if tipo_convertido is None:
        raise ValueError(
            f"Tipo de Submissão inválido: {submissao['tipo']!r}."
        )

    _converter_data_iso(
        submissao["data_criacao"],
        "A data de criação",
    )

    _normalizar_texto_obrigatorio(
        submissao["responsavel_criacao"],
        "O responsável pela criação",
    )

    _normalizar_pacote_documental(
        submissao["pacote_documental"]
    )

    codigos_exigencias = _normalizar_codigos_exigencias(
        submissao["codigos_exigencias_relacionadas"]
    )

    codigo_submissao_origem = submissao["codigo_submissao_origem"]
    codigo_resposta_origem = submissao["codigo_resposta_origem"]

    if codigo_submissao_origem is not None:
        _validar_inteiro_positivo(
            codigo_submissao_origem,
            "O código da Submissão de origem",
        )

    if codigo_resposta_origem is not None:
        _validar_inteiro_positivo(
            codigo_resposta_origem,
            "O código da Resposta de origem",
        )

    if tipo_convertido == TipoSubmissao.INICIAL:

        if codigo_submissao_origem is not None:
            raise ValueError(
                "Uma Submissão Inicial não pode possuir origem."
            )

        if codigo_resposta_origem is not None:
            raise ValueError(
                "Uma Submissão Inicial não pode possuir "
                "Resposta de origem."
            )

        if codigos_exigencias:
            raise ValueError(
                "Uma Submissão Inicial não pode atender Exigências."
            )

    else:

        if codigo_submissao_origem is None:
            raise ValueError(
                "Complementação e Reenvio devem possuir "
                "Submissão de origem."
            )

        if codigo_resposta_origem is None:
            raise ValueError(
                "Complementação e Reenvio devem possuir "
                "Resposta de origem."
            )

        if (
            codigo_submissao_origem
            == submissao["codigo"]
        ):
            raise ValueError(
                "Uma Submissão não pode apontar para si mesma "
                "como origem."
            )

        if (
            tipo_convertido == TipoSubmissao.COMPLEMENTACAO
            and not codigos_exigencias
        ):
            raise ValueError(
                "Uma Complementação deve informar "
                "as Exigências atendidas."
            )

    if not status_operacional_submissao_valido(
        submissao["status_operacional"]
    ):
        raise ValueError(
            "Status operacional da Submissão inválido: "
            f"{submissao['status_operacional']!r}."
        )

    if not status_analise_submissao_valido(
        submissao["status_analise"]
    ):
        raise ValueError(
            "Status da análise da Submissão inválido: "
            f"{submissao['status_analise']!r}."
        )

    status_operacional = StatusOperacionalSubmissao(
        submissao["status_operacional"]
    )

    status_analise = StatusAnaliseSubmissao(
        submissao["status_analise"]
    )

    canal = submissao["canal_envio"]
    data_envio = submissao["data_envio"]
    responsavel_envio = submissao["responsavel_envio"]
    protocolo = submissao["protocolo"]
    data_protocolo = submissao["data_protocolo"]

    estados_antes_do_envio = {
        StatusOperacionalSubmissao.EM_PREPARACAO,
        StatusOperacionalSubmissao.PRONTA_PARA_ENVIO,
        StatusOperacionalSubmissao.CANCELADA,
    }

    if status_operacional in estados_antes_do_envio:
        if canal is not None:
            raise ValueError(
                "Uma Submissão ainda não enviada não pode possuir "
                "canal de envio."
            )

        if data_envio is not None:
            raise ValueError(
                "Uma Submissão ainda não enviada não pode possuir "
                "data de envio."
            )

        if responsavel_envio is not None:
            raise ValueError(
                "Uma Submissão ainda não enviada não pode possuir "
                "responsável pelo envio."
            )

        if protocolo is not None or data_protocolo is not None:
            raise ValueError(
                "Uma Submissão ainda não enviada não pode possuir "
                "dados de protocolo."
            )

    if status_operacional in {
        StatusOperacionalSubmissao.ENVIADA,
        StatusOperacionalSubmissao.PROTOCOLADA,
    }:
        if not canal_envio_submissao_valido(canal):
            raise ValueError(
                "Uma Submissão enviada deve possuir "
                "um canal de envio válido."
            )

        _converter_data_iso(
            data_envio,
            "A data de envio",
        )

        _normalizar_texto_obrigatorio(
            responsavel_envio,
            "O responsável pelo envio",
        )

        if not submissao["pacote_documental"]:
            raise ValueError(
                "Uma Submissão enviada deve possuir "
                "pelo menos um Documento no pacote."
            )

    if status_operacional == StatusOperacionalSubmissao.ENVIADA:
        if protocolo is not None or data_protocolo is not None:
            raise ValueError(
                "Uma Submissão apenas enviada ainda não pode possuir "
                "dados de protocolo."
            )

    if status_operacional == StatusOperacionalSubmissao.PROTOCOLADA:
        _normalizar_texto_obrigatorio(
            protocolo,
            "O protocolo da Submissão",
        )

        data_protocolo_normalizada = _converter_data_iso(
            data_protocolo,
            "A data do protocolo",
        )

        data_envio_normalizada = _converter_data_iso(
            data_envio,
            "A data de envio",
        )

        if (
            date.fromisoformat(data_protocolo_normalizada)
            < date.fromisoformat(data_envio_normalizada)
        ):
            raise ValueError(
                "A data do protocolo não pode ser anterior "
                "à data de envio."
            )

    respostas = _normalizar_respostas(
        submissao["respostas"]
    )

    if respostas:
        if status_operacional not in {
            StatusOperacionalSubmissao.ENVIADA,
            StatusOperacionalSubmissao.PROTOCOLADA,
        }:
            raise ValueError(
                "Uma Submissão não enviada não pode possuir Respostas."
            )

        ultima_resposta = max(
            respostas,
            key=lambda resposta: resposta["numero_sequencial"],
        )

        status_resultante = obter_status_resultante_resposta(
            ultima_resposta["tipo"]
        )

        if status_resultante != status_analise:
            raise ValueError(
                "O status da análise deve corresponder ao tipo "
                "da última Resposta registrada."
            )

    else:
        if status_analise != StatusAnaliseSubmissao.SEM_RESPOSTA:
            raise ValueError(
                "Uma Submissão sem Respostas deve permanecer "
                "com status de análise SEM_RESPOSTA."
            )

    _normalizar_texto_opcional(
        submissao["observacoes"],
        "As observações da Submissão",
    )

    return True

def submissao_esta_em_preparacao(submissao):
    """
    Informa se a Submissão está em preparação.
    """

    if not isinstance(submissao, dict):
        return False

    return (
        submissao.get("status_operacional")
        == StatusOperacionalSubmissao.EM_PREPARACAO.value
    )

def submissao_foi_enviada(submissao):
    """
    Informa se a Submissão já foi enviada.

    Uma Submissão protocolada também foi previamente enviada.
    """

    if not isinstance(submissao, dict):
        return False

    return submissao.get("status_operacional") in {
        StatusOperacionalSubmissao.ENVIADA.value,
        StatusOperacionalSubmissao.PROTOCOLADA.value,
    }

def submissao_foi_protocolada(submissao):
    """
    Informa se a Submissão foi protocolada.
    """

    if not isinstance(submissao, dict):
        return False

    return (
        submissao.get("status_operacional")
        == StatusOperacionalSubmissao.PROTOCOLADA.value
    )

def obter_rotulo_tipo_submissao(tipo):
    """
    Retorna o rótulo amigável do tipo da Submissão.
    """

    tipo_convertido = _converter_tipo_submissao(tipo)

    if tipo_convertido is None:
        return None

    return ROTULOS_TIPO_SUBMISSAO[tipo_convertido]

def obter_rotulo_canal_envio_submissao(canal):
    """
    Retorna o rótulo amigável do canal de envio.
    """

    canal_convertido = _converter_canal_envio(canal)

    if canal_convertido is None:
        return None

    return ROTULOS_CANAL_ENVIO_SUBMISSAO[canal_convertido]