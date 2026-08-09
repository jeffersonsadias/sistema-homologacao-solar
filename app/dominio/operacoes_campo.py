"""
Estrutura e validações das Operações de Campo.

As Operações de Campo representam as etapas executadas
após a emissão do parecer de acesso:

- instalação;
- vistoria;
- ligação e energização.

Este módulo não deve:

- alterar diretamente uma Homologação;
- modificar o status da Homologação;
- registrar Movimentações;
- persistir dados;
- utilizar input() ou print().

A coordenação dessas operações permanece pertencendo
ao Aggregate Root de Homologação.
"""
from datetime import date
from enum import Enum

class StatusInstalacao(str, Enum):
    """
    Estados internos da execução da Instalação.

    Esses estados detalham a atividade de campo e não
    substituem o status geral da Homologação.
    """

    PLANEJADA = "PLANEJADA"
    EM_EXECUCAO = "EM_EXECUCAO"
    CONCLUIDA = "CONCLUIDA"

class StatusVistoria(str, Enum):
    """
    Estados internos de uma Vistoria.

    Esses estados detalham a execução da Vistoria
    e não substituem o status geral da Homologação.
    """

    SOLICITADA = "SOLICITADA"
    AGENDADA = "AGENDADA"
    REALIZADA = "REALIZADA"
    APROVADA = "APROVADA"
    REPROVADA = "REPROVADA"

class StatusLigacao(str, Enum):
    """
    Estados internos da Ligação e Energização.

    Esses estados detalham a execução da Ligação
    e não substituem o status geral da Homologação.
    """

    SOLICITADA = "SOLICITADA"
    AGENDADA = "AGENDADA"
    CONCLUIDA = "CONCLUIDA"

def _validar_texto_obrigatorio(
    valor: str,
    nome_campo: str,
) -> str:
    """
    Valida e normaliza um texto obrigatório.
    """

    if not isinstance(
        valor,
        str,
    ):
        raise TypeError(
            f"{nome_campo} deve ser um texto."
        )

    valor_normalizado = valor.strip()

    if not valor_normalizado:
        raise ValueError(
            f"{nome_campo} é obrigatório."
        )

    return valor_normalizado

def _normalizar_texto_opcional(
    valor: str | None,
    nome_campo: str,
) -> str | None:
    """
    Normaliza um texto opcional.

    Textos vazios são convertidos para None.
    """

    if valor is None:
        return None

    if not isinstance(
        valor,
        str,
    ):
        raise TypeError(
            f"{nome_campo} deve ser um texto."
        )

    return valor.strip() or None

def _validar_data_iso(
    valor: str,
    nome_campo: str,
) -> str:
    """
    Valida uma data no formato AAAA-MM-DD
    e retorna sua representação normalizada.
    """

    if not isinstance(
        valor,
        str,
    ):
        raise TypeError(
            f"{nome_campo} deve ser um texto."
        )

    try:
        data_convertida = date.fromisoformat(
            valor
        )

    except ValueError as erro:
        raise ValueError(
            f"{nome_campo} deve utilizar "
            "o formato AAAA-MM-DD."
        ) from erro

    return data_convertida.isoformat()

def gerar_proximo_codigo_vistoria(
    vistorias: list[dict],
) -> int:
    """
    Gera o próximo código interno das Vistorias
    pertencentes à mesma Homologação.

    Quando a lista estiver vazia, retorna 1.
    """

    if not isinstance(
        vistorias,
        list,
    ):
        raise TypeError(
            "Vistorias devem formar uma lista."
        )

    if not vistorias:
        return 1

    maior_codigo = max(
        vistoria.get("codigo", 0)
        for vistoria in vistorias
    )

    return maior_codigo + 1

def gerar_proximo_numero_sequencial_vistoria(
    vistorias: list[dict],
) -> int:
    """
    Gera o número sequencial da próxima tentativa
    de Vistoria da Homologação.

    O primeiro registro recebe número sequencial 1.
    """

    if not isinstance(
        vistorias,
        list,
    ):
        raise TypeError(
            "Vistorias devem formar uma lista."
        )

    if not vistorias:
        return 1

    maior_numero = max(
        vistoria.get(
            "numero_sequencial",
            0,
        )
        for vistoria in vistorias
    )

    return maior_numero + 1

def criar_dados_operacoes_campo() -> dict:
    """
    Cria a estrutura inicial das Operações de Campo.

    A instalação e a ligação começam ausentes porque
    ainda não foram registradas.

    Vistorias formam uma lista porque uma Homologação
    pode passar por mais de uma vistoria.
    """

    return {
        "instalacao": None,
        "vistorias": [],
        "ligacao": None,
    }

def validar_operacoes_campo(
    operacoes_campo: dict,
) -> None:
    """
    Valida a estrutura mínima das Operações de Campo.

    A função não valida os dados internos de Instalação,
    Vistoria ou Ligação. Essas regras serão acrescentadas
    junto aos respectivos casos de uso.
    """

    if not isinstance(
        operacoes_campo,
        dict,
    ):
        raise TypeError(
            "Operações de Campo devem ser "
            "representadas por um dicionário."
        )

    campos_obrigatorios = (
        "instalacao",
        "vistorias",
        "ligacao",
    )

    for campo in campos_obrigatorios:
        if campo not in operacoes_campo:
            raise ValueError(
                "Estrutura de Operações de Campo inválida: "
                f"campo ausente: {campo}."
            )

    instalacao = operacoes_campo[
        "instalacao"
    ]

    if (
        instalacao is not None
        and not isinstance(
            instalacao,
            dict,
        )
    ):
        raise TypeError(
            "Instalação deve ser um dicionário "
            "ou None."
        )

    if not isinstance(
        operacoes_campo["vistorias"],
        list,
    ):
        raise TypeError(
            "Vistorias devem formar uma lista."
        )

    for vistoria in operacoes_campo[
        "vistorias"
    ]:
        validar_vistoria(
            vistoria
        )

    ligacao = operacoes_campo[
        "ligacao"
    ]

    if (
        ligacao is not None
        and not isinstance(
            ligacao,
            dict,
        )
    ):
        raise TypeError(
            "Ligação deve ser um dicionário "
            "ou None."
        )

    if ligacao is not None:
        validar_ligacao(
            ligacao
        )


def criar_dados_vistoria_solicitada(
    codigo: int,
    numero_sequencial: int,
    data_solicitacao: str,
    responsavel_solicitacao: str,
    protocolo: str,
    observacoes: str | None = None,
) -> dict:
    """
    Cria uma nova Vistoria com status SOLICITADA.

    Dados de agendamento, realização e resultado
    permanecem ausentes até os respectivos eventos.
    """

    if (
        isinstance(codigo, bool)
        or not isinstance(
            codigo,
            int,
        )
    ):
        raise TypeError(
            "Código da Vistoria deve ser "
            "um número inteiro."
        )

    if codigo <= 0:
        raise ValueError(
            "Código da Vistoria deve ser "
            "maior que zero."
        )

    if (
        isinstance(numero_sequencial, bool)
        or not isinstance(
            numero_sequencial,
            int,
        )
    ):
        raise TypeError(
            "Número sequencial da Vistoria deve "
            "ser um número inteiro."
        )

    if numero_sequencial <= 0:
        raise ValueError(
            "Número sequencial da Vistoria deve "
            "ser maior que zero."
        )

    data_normalizada = _validar_data_iso(
        data_solicitacao,
        "Data de solicitação da Vistoria",
    )

    responsavel_normalizado = (
        _validar_texto_obrigatorio(
            responsavel_solicitacao,
            "Responsável pela solicitação",
        )
    )

    protocolo_normalizado = (
        _validar_texto_obrigatorio(
            protocolo,
            "Protocolo da Vistoria",
        )
    )

    observacoes_normalizadas = (
        _normalizar_texto_opcional(
            observacoes,
            "Observações da Vistoria",
        )
    )

    return {
        "codigo": codigo,
        "numero_sequencial": numero_sequencial,
        "status": StatusVistoria.SOLICITADA.value,
        "data_solicitacao": data_normalizada,
        "responsavel_solicitacao": (
            responsavel_normalizado
        ),
        "protocolo": protocolo_normalizado,
        "data_agendamento": None,
        "responsavel_agendamento": None,
        "data_realizacao": None,
        "responsavel_realizacao": None,
        "data_resultado": None,
        "responsavel_resultado": None,
        "resultado": None,
        "motivo_reprovacao": None,
        "observacoes": observacoes_normalizadas,
    }

def validar_vistoria(
    vistoria: dict,
) -> None:
    """
    Valida a estrutura e a coerência interna
    de uma Vistoria.

    Estados considerados:

    - SOLICITADA;
    - AGENDADA;
    - REALIZADA;
    - APROVADA;
    - REPROVADA.
    """

    if not isinstance(
        vistoria,
        dict,
    ):
        raise TypeError(
            "Vistoria deve ser representada "
            "por um dicionário."
        )

    campos_obrigatorios = (
        "codigo",
        "numero_sequencial",
        "status",
        "data_solicitacao",
        "responsavel_solicitacao",
        "protocolo",
        "data_agendamento",
        "responsavel_agendamento",
        "data_realizacao",
        "responsavel_realizacao",
        "data_resultado",
        "responsavel_resultado",
        "resultado",
        "motivo_reprovacao",
        "observacoes",
    )

    for campo in campos_obrigatorios:
        if campo not in vistoria:
            raise ValueError(
                "Estrutura de Vistoria inválida: "
                f"campo ausente: {campo}."
            )

    codigo = vistoria["codigo"]

    if (
        isinstance(codigo, bool)
        or not isinstance(
            codigo,
            int,
        )
    ):
        raise TypeError(
            "Código da Vistoria deve ser "
            "um número inteiro."
        )

    if codigo <= 0:
        raise ValueError(
            "Código da Vistoria deve ser "
            "maior que zero."
        )

    numero_sequencial = vistoria[
        "numero_sequencial"
    ]

    if (
        isinstance(numero_sequencial, bool)
        or not isinstance(
            numero_sequencial,
            int,
        )
    ):
        raise TypeError(
            "Número sequencial da Vistoria deve "
            "ser um número inteiro."
        )

    if numero_sequencial <= 0:
        raise ValueError(
            "Número sequencial da Vistoria deve "
            "ser maior que zero."
        )

    try:
        status_vistoria = StatusVistoria(
            vistoria["status"]
        )

    except (
        ValueError,
        TypeError,
    ) as erro:
        raise ValueError(
            "Status de Vistoria inválido: "
            f"{vistoria.get('status')!r}."
        ) from erro

    _validar_data_iso(
        vistoria["data_solicitacao"],
        "Data de solicitação da Vistoria",
    )

    _validar_texto_obrigatorio(
        vistoria["responsavel_solicitacao"],
        "Responsável pela solicitação",
    )

    _validar_texto_obrigatorio(
        vistoria["protocolo"],
        "Protocolo da Vistoria",
    )

    _normalizar_texto_opcional(
        vistoria["observacoes"],
        "Observações da Vistoria",
    )

    if status_vistoria == StatusVistoria.SOLICITADA:
        if any(
            valor is not None
            for valor in (
                vistoria["data_agendamento"],
                vistoria[
                    "responsavel_agendamento"
                ],
                vistoria["data_realizacao"],
                vistoria[
                    "responsavel_realizacao"
                ],
                vistoria["data_resultado"],
                vistoria[
                    "responsavel_resultado"
                ],
                vistoria["resultado"],
                vistoria["motivo_reprovacao"],
            )
        ):
            raise ValueError(
                "Uma Vistoria solicitada não pode "
                "possuir dados de agendamento, "
                "realização ou resultado."
            )

    elif status_vistoria == StatusVistoria.AGENDADA:
        _validar_data_iso(
            vistoria["data_agendamento"],
            "Data de agendamento da Vistoria",
        )

        _validar_texto_obrigatorio(
            vistoria[
                "responsavel_agendamento"
            ],
            "Responsável pelo agendamento",
        )

        if any(
            valor is not None
            for valor in (
                vistoria["data_realizacao"],
                vistoria[
                    "responsavel_realizacao"
                ],
                vistoria["data_resultado"],
                vistoria[
                    "responsavel_resultado"
                ],
                vistoria["resultado"],
                vistoria["motivo_reprovacao"],
            )
        ):
            raise ValueError(
                "Uma Vistoria agendada não pode "
                "possuir dados de realização "
                "ou resultado."
            )

    elif status_vistoria == StatusVistoria.REALIZADA:
        _validar_data_iso(
            vistoria["data_agendamento"],
            "Data de agendamento da Vistoria",
        )

        _validar_texto_obrigatorio(
            vistoria[
                "responsavel_agendamento"
            ],
            "Responsável pelo agendamento",
        )

        _validar_data_iso(
            vistoria["data_realizacao"],
            "Data de realização da Vistoria",
        )

        _validar_texto_obrigatorio(
            vistoria[
                "responsavel_realizacao"
            ],
            "Responsável pela realização",
        )

        if any(
            valor is not None
            for valor in (
                vistoria["data_resultado"],
                vistoria[
                    "responsavel_resultado"
                ],
                vistoria["resultado"],
                vistoria["motivo_reprovacao"],
            )
        ):
            raise ValueError(
                "Uma Vistoria realizada e ainda sem "
                "resultado não pode possuir dados "
                "do resultado formal."
            )

    elif status_vistoria == StatusVistoria.APROVADA:
        _validar_data_iso(
            vistoria["data_agendamento"],
            "Data de agendamento da Vistoria",
        )

        _validar_texto_obrigatorio(
            vistoria[
                "responsavel_agendamento"
            ],
            "Responsável pelo agendamento",
        )

        _validar_data_iso(
            vistoria["data_realizacao"],
            "Data de realização da Vistoria",
        )

        _validar_texto_obrigatorio(
            vistoria[
                "responsavel_realizacao"
            ],
            "Responsável pela realização",
        )

        _validar_data_iso(
            vistoria["data_resultado"],
            "Data do resultado da Vistoria",
        )

        _validar_texto_obrigatorio(
            vistoria[
                "responsavel_resultado"
            ],
            "Responsável pelo resultado",
        )

        if vistoria["resultado"] != "APROVADA":
            raise ValueError(
                "Uma Vistoria aprovada deve possuir "
                "resultado APROVADA."
            )

        if vistoria["motivo_reprovacao"] is not None:
            raise ValueError(
                "Uma Vistoria aprovada não pode possuir "
                "motivo de reprovação."
            )

    elif status_vistoria == StatusVistoria.REPROVADA:
        _validar_data_iso(
            vistoria["data_agendamento"],
            "Data de agendamento da Vistoria",
        )

        _validar_texto_obrigatorio(
            vistoria[
                "responsavel_agendamento"
            ],
            "Responsável pelo agendamento",
        )

        _validar_data_iso(
            vistoria["data_realizacao"],
            "Data de realização da Vistoria",
        )

        _validar_texto_obrigatorio(
            vistoria[
                "responsavel_realizacao"
            ],
            "Responsável pela realização",
        )

        _validar_data_iso(
            vistoria["data_resultado"],
            "Data do resultado da Vistoria",
        )

        _validar_texto_obrigatorio(
            vistoria[
                "responsavel_resultado"
            ],
            "Responsável pelo resultado",
        )

        if vistoria["resultado"] != "REPROVADA":
            raise ValueError(
                "Uma Vistoria reprovada deve possuir "
                "resultado REPROVADA."
            )

        _validar_texto_obrigatorio(
            vistoria["motivo_reprovacao"],
            "Motivo da reprovação",
        )

def buscar_vistoria_por_codigo(
    vistorias: list[dict],
    codigo: int,
) -> dict | None:
    """
    Busca uma Vistoria por seu código interno.
    """

    for vistoria in vistorias:
        if vistoria.get("codigo") == codigo:
            return vistoria

    return None

def buscar_vistoria_por_numero_sequencial(
    vistorias: list[dict],
    numero_sequencial: int,
) -> dict | None:
    """
    Busca uma tentativa de Vistoria
    por seu número sequencial.
    """

    for vistoria in vistorias:
        if (
            vistoria.get("numero_sequencial")
            == numero_sequencial
        ):
            return vistoria

    return None

def buscar_ultima_vistoria(
    vistorias: list[dict],
) -> dict | None:
    """
    Retorna a Vistoria com o maior
    número sequencial.

    Retorna None quando a lista estiver vazia.
    """

    if not vistorias:
        return None

    return max(
        vistorias,
        key=lambda vistoria: vistoria.get(
            "numero_sequencial",
            0,
        ),
    )

def preparar_agendamento_vistoria(
    vistoria: dict,
    data_agendamento: str,
    responsavel_agendamento: str,
    observacoes: str | None = None,
) -> dict:
    """
    Prepara uma cópia da Vistoria com seu
    agendamento registrado.

    A função não modifica a Vistoria recebida.
    """

    validar_vistoria(
        vistoria
    )

    status_atual = StatusVistoria(
        vistoria["status"]
    )

    if status_atual != StatusVistoria.SOLICITADA:
        raise ValueError(
            "Somente uma Vistoria solicitada "
            "pode ser agendada."
        )

    data_agendamento_normalizada = (
        _validar_data_iso(
            data_agendamento,
            "Data de agendamento da Vistoria",
        )
    )

    responsavel_normalizado = (
        _validar_texto_obrigatorio(
            responsavel_agendamento,
            "Responsável pelo agendamento",
        )
    )

    observacoes_normalizadas = (
        _normalizar_texto_opcional(
            observacoes,
            "Observações da Vistoria",
        )
    )

    data_solicitacao_convertida = (
        date.fromisoformat(
            vistoria["data_solicitacao"]
        )
    )

    data_agendamento_convertida = (
        date.fromisoformat(
            data_agendamento_normalizada
        )
    )

    if (
        data_agendamento_convertida
        < data_solicitacao_convertida
    ):
        raise ValueError(
            "A data de agendamento da Vistoria "
            "não pode ser anterior à data de solicitação."
        )

    vistoria_candidata = vistoria.copy()

    vistoria_candidata["status"] = (
        StatusVistoria.AGENDADA.value
    )

    vistoria_candidata[
        "data_agendamento"
    ] = data_agendamento_normalizada

    vistoria_candidata[
        "responsavel_agendamento"
    ] = responsavel_normalizado

    if observacoes is not None:
        vistoria_candidata["observacoes"] = (
            observacoes_normalizadas
        )

    validar_vistoria(
        vistoria_candidata
    )

    return vistoria_candidata

def preparar_realizacao_vistoria(
    vistoria: dict,
    data_realizacao: str,
    responsavel_realizacao: str,
    observacoes: str | None = None,
) -> dict:
    """
    Prepara uma cópia da Vistoria com sua
    realização registrada.

    A função não modifica a Vistoria recebida.
    O resultado permanece ausente até seu
    registro formal.
    """

    validar_vistoria(
        vistoria
    )

    status_atual = StatusVistoria(
        vistoria["status"]
    )

    if status_atual != StatusVistoria.AGENDADA:
        raise ValueError(
            "Somente uma Vistoria agendada "
            "pode ser realizada."
        )

    data_realizacao_normalizada = (
        _validar_data_iso(
            data_realizacao,
            "Data de realização da Vistoria",
        )
    )

    responsavel_normalizado = (
        _validar_texto_obrigatorio(
            responsavel_realizacao,
            "Responsável pela realização",
        )
    )

    observacoes_normalizadas = (
        _normalizar_texto_opcional(
            observacoes,
            "Observações da Vistoria",
        )
    )

    data_agendamento_convertida = (
        date.fromisoformat(
            vistoria["data_agendamento"]
        )
    )

    data_realizacao_convertida = (
        date.fromisoformat(
            data_realizacao_normalizada
        )
    )

    if (
        data_realizacao_convertida
        < data_agendamento_convertida
    ):
        raise ValueError(
            "A data de realização da Vistoria "
            "não pode ser anterior à data agendada."
        )

    vistoria_candidata = vistoria.copy()

    vistoria_candidata["status"] = (
        StatusVistoria.REALIZADA.value
    )

    vistoria_candidata[
        "data_realizacao"
    ] = data_realizacao_normalizada

    vistoria_candidata[
        "responsavel_realizacao"
    ] = responsavel_normalizado

    if observacoes is not None:
        vistoria_candidata["observacoes"] = (
            observacoes_normalizadas
        )

    validar_vistoria(
        vistoria_candidata
    )

    return vistoria_candidata

def preparar_aprovacao_vistoria(
    vistoria: dict,
    data_resultado: str,
    responsavel_resultado: str,
    observacoes: str | None = None,
) -> dict:
    """
    Prepara uma cópia da Vistoria com
    o resultado de aprovação.

    A função não modifica a Vistoria recebida.
    """

    validar_vistoria(
        vistoria
    )

    status_atual = StatusVistoria(
        vistoria["status"]
    )

    if status_atual != StatusVistoria.REALIZADA:
        raise ValueError(
            "Somente uma Vistoria realizada "
            "pode ser aprovada."
        )

    data_resultado_normalizada = (
        _validar_data_iso(
            data_resultado,
            "Data do resultado da Vistoria",
        )
    )

    responsavel_normalizado = (
        _validar_texto_obrigatorio(
            responsavel_resultado,
            "Responsável pelo resultado",
        )
    )

    observacoes_normalizadas = (
        _normalizar_texto_opcional(
            observacoes,
            "Observações da Vistoria",
        )
    )

    data_realizacao_convertida = (
        date.fromisoformat(
            vistoria["data_realizacao"]
        )
    )

    data_resultado_convertida = (
        date.fromisoformat(
            data_resultado_normalizada
        )
    )

    if (
        data_resultado_convertida
        < data_realizacao_convertida
    ):
        raise ValueError(
            "A data do resultado da Vistoria "
            "não pode ser anterior à realização."
        )

    vistoria_candidata = vistoria.copy()

    vistoria_candidata["status"] = (
        StatusVistoria.APROVADA.value
    )

    vistoria_candidata["data_resultado"] = (
        data_resultado_normalizada
    )

    vistoria_candidata[
        "responsavel_resultado"
    ] = responsavel_normalizado

    vistoria_candidata["resultado"] = (
        StatusVistoria.APROVADA.value
    )

    vistoria_candidata[
        "motivo_reprovacao"
    ] = None

    if observacoes is not None:
        vistoria_candidata["observacoes"] = (
            observacoes_normalizadas
        )

    validar_vistoria(
        vistoria_candidata
    )

    return vistoria_candidata

def preparar_reprovacao_vistoria(
    vistoria: dict,
    data_resultado: str,
    responsavel_resultado: str,
    motivo_reprovacao: str,
    observacoes: str | None = None,
) -> dict:
    """
    Prepara uma cópia da Vistoria com
    o resultado de reprovação.

    A reprovação exige motivo obrigatório.
    A função não modifica a Vistoria recebida.
    """

    validar_vistoria(
        vistoria
    )

    status_atual = StatusVistoria(
        vistoria["status"]
    )

    if status_atual != StatusVistoria.REALIZADA:
        raise ValueError(
            "Somente uma Vistoria realizada "
            "pode ser reprovada."
        )

    data_resultado_normalizada = (
        _validar_data_iso(
            data_resultado,
            "Data do resultado da Vistoria",
        )
    )

    responsavel_normalizado = (
        _validar_texto_obrigatorio(
            responsavel_resultado,
            "Responsável pelo resultado",
        )
    )

    motivo_normalizado = (
        _validar_texto_obrigatorio(
            motivo_reprovacao,
            "Motivo da reprovação",
        )
    )

    observacoes_normalizadas = (
        _normalizar_texto_opcional(
            observacoes,
            "Observações da Vistoria",
        )
    )

    data_realizacao_convertida = (
        date.fromisoformat(
            vistoria["data_realizacao"]
        )
    )

    data_resultado_convertida = (
        date.fromisoformat(
            data_resultado_normalizada
        )
    )

    if (
        data_resultado_convertida
        < data_realizacao_convertida
    ):
        raise ValueError(
            "A data do resultado da Vistoria "
            "não pode ser anterior à realização."
        )

    vistoria_candidata = vistoria.copy()

    vistoria_candidata["status"] = (
        StatusVistoria.REPROVADA.value
    )

    vistoria_candidata["data_resultado"] = (
        data_resultado_normalizada
    )

    vistoria_candidata[
        "responsavel_resultado"
    ] = responsavel_normalizado

    vistoria_candidata["resultado"] = (
        StatusVistoria.REPROVADA.value
    )

    vistoria_candidata[
        "motivo_reprovacao"
    ] = motivo_normalizado

    if observacoes is not None:
        vistoria_candidata["observacoes"] = (
            observacoes_normalizadas
        )

    validar_vistoria(
        vistoria_candidata
    )

    return vistoria_candidata


def criar_dados_ligacao_solicitada(
    data_solicitacao: str,
    responsavel_solicitacao: str,
    protocolo: str,
    observacoes: str | None = None,
) -> dict:
    """
    Cria os dados iniciais da Ligação e Energização.

    A Ligação nasce com status SOLICITADA.

    Os dados de agendamento e conclusão permanecem
    ausentes até que os respectivos eventos ocorram.
    """

    data_normalizada = _validar_data_iso(
        data_solicitacao,
        "Data de solicitação da Ligação",
    )

    responsavel_normalizado = (
        _validar_texto_obrigatorio(
            responsavel_solicitacao,
            "Responsável pela solicitação",
        )
    )

    protocolo_normalizado = (
        _validar_texto_obrigatorio(
            protocolo,
            "Protocolo da Ligação",
        )
    )

    observacoes_normalizadas = (
        _normalizar_texto_opcional(
            observacoes,
            "Observações da Ligação",
        )
    )

    return {
        "status": StatusLigacao.SOLICITADA.value,
        "data_solicitacao": data_normalizada,
        "responsavel_solicitacao": (
            responsavel_normalizado
        ),
        "protocolo": protocolo_normalizado,
        "data_agendamento": None,
        "responsavel_agendamento": None,
        "data_ligacao": None,
        "responsavel_ligacao": None,
        "observacoes": observacoes_normalizadas,
    }

def validar_ligacao(
    ligacao: dict,
) -> None:
    """
    Valida a estrutura e a coerência interna
    da Ligação e Energização.

    Estados considerados:

    - SOLICITADA;
    - AGENDADA;
    - CONCLUIDA.
    """

    if not isinstance(
        ligacao,
        dict,
    ):
        raise TypeError(
            "Ligação deve ser representada "
            "por um dicionário."
        )

    campos_obrigatorios = (
        "status",
        "data_solicitacao",
        "responsavel_solicitacao",
        "protocolo",
        "data_agendamento",
        "responsavel_agendamento",
        "data_ligacao",
        "responsavel_ligacao",
        "observacoes",
    )

    for campo in campos_obrigatorios:
        if campo not in ligacao:
            raise ValueError(
                "Estrutura de Ligação inválida: "
                f"campo ausente: {campo}."
            )

    try:
        status_ligacao = StatusLigacao(
            ligacao["status"]
        )

    except (
        ValueError,
        TypeError,
    ) as erro:
        raise ValueError(
            "Status de Ligação inválido: "
            f"{ligacao.get('status')!r}."
        ) from erro

    _validar_data_iso(
        ligacao["data_solicitacao"],
        "Data de solicitação da Ligação",
    )

    _validar_texto_obrigatorio(
        ligacao["responsavel_solicitacao"],
        "Responsável pela solicitação",
    )

    _validar_texto_obrigatorio(
        ligacao["protocolo"],
        "Protocolo da Ligação",
    )

    _normalizar_texto_opcional(
        ligacao["observacoes"],
        "Observações da Ligação",
    )

    if (
        status_ligacao
        == StatusLigacao.SOLICITADA
    ):
        if any(
            valor is not None
            for valor in (
                ligacao["data_agendamento"],
                ligacao[
                    "responsavel_agendamento"
                ],
                ligacao["data_ligacao"],
                ligacao["responsavel_ligacao"],
            )
        ):
            raise ValueError(
                "Uma Ligação solicitada não pode "
                "possuir dados de agendamento "
                "ou conclusão."
            )

    elif (
        status_ligacao
        == StatusLigacao.AGENDADA
    ):
        _validar_data_iso(
            ligacao["data_agendamento"],
            "Data de agendamento da Ligação",
        )

        _validar_texto_obrigatorio(
            ligacao[
                "responsavel_agendamento"
            ],
            "Responsável pelo agendamento",
        )

        if any(
            valor is not None
            for valor in (
                ligacao["data_ligacao"],
                ligacao["responsavel_ligacao"],
            )
        ):
            raise ValueError(
                "Uma Ligação agendada não pode "
                "possuir dados de conclusão."
            )

    elif (
        status_ligacao
        == StatusLigacao.CONCLUIDA
    ):
        _validar_data_iso(
            ligacao["data_agendamento"],
            "Data de agendamento da Ligação",
        )

        _validar_texto_obrigatorio(
            ligacao[
                "responsavel_agendamento"
            ],
            "Responsável pelo agendamento",
        )

        _validar_data_iso(
            ligacao["data_ligacao"],
            "Data da Ligação",
        )

        _validar_texto_obrigatorio(
            ligacao["responsavel_ligacao"],
            "Responsável pela Ligação",
        )

def preparar_agendamento_ligacao(
    ligacao: dict,
    data_agendamento: str,
    responsavel_agendamento: str,
    observacoes: str | None = None,
) -> dict:
    """
    Prepara uma cópia da Ligação com
    o agendamento registrado.

    A função não modifica a Ligação recebida.
    """

    validar_ligacao(
        ligacao
    )

    status_atual = StatusLigacao(
        ligacao["status"]
    )

    if (
        status_atual
        != StatusLigacao.SOLICITADA
    ):
        raise ValueError(
            "Somente uma Ligação solicitada "
            "pode ser agendada."
        )

    data_agendamento_normalizada = (
        _validar_data_iso(
            data_agendamento,
            "Data de agendamento da Ligação",
        )
    )

    responsavel_normalizado = (
        _validar_texto_obrigatorio(
            responsavel_agendamento,
            "Responsável pelo agendamento",
        )
    )

    observacoes_normalizadas = (
        _normalizar_texto_opcional(
            observacoes,
            "Observações da Ligação",
        )
    )

    data_solicitacao_convertida = (
        date.fromisoformat(
            ligacao["data_solicitacao"]
        )
    )

    data_agendamento_convertida = (
        date.fromisoformat(
            data_agendamento_normalizada
        )
    )

    if (
        data_agendamento_convertida
        < data_solicitacao_convertida
    ):
        raise ValueError(
            "A data de agendamento da Ligação "
            "não pode ser anterior à data de solicitação."
        )

    ligacao_candidata = ligacao.copy()

    ligacao_candidata["status"] = (
        StatusLigacao.AGENDADA.value
    )

    ligacao_candidata[
        "data_agendamento"
    ] = data_agendamento_normalizada

    ligacao_candidata[
        "responsavel_agendamento"
    ] = responsavel_normalizado

    if observacoes is not None:
        ligacao_candidata["observacoes"] = (
            observacoes_normalizadas
        )

    validar_ligacao(
        ligacao_candidata
    )

    return ligacao_candidata

def preparar_conclusao_ligacao(
    ligacao: dict,
    data_ligacao: str,
    responsavel_ligacao: str,
    observacoes: str | None = None,
) -> dict:
    """
    Prepara uma cópia da Ligação com
    sua conclusão e energização registradas.

    A função não modifica a Ligação recebida.
    """

    validar_ligacao(
        ligacao
    )

    status_atual = StatusLigacao(
        ligacao["status"]
    )

    if (
        status_atual
        != StatusLigacao.AGENDADA
    ):
        raise ValueError(
            "Somente uma Ligação agendada "
            "pode ser concluída."
        )

    data_ligacao_normalizada = (
        _validar_data_iso(
            data_ligacao,
            "Data da Ligação",
        )
    )

    responsavel_normalizado = (
        _validar_texto_obrigatorio(
            responsavel_ligacao,
            "Responsável pela Ligação",
        )
    )

    observacoes_normalizadas = (
        _normalizar_texto_opcional(
            observacoes,
            "Observações da Ligação",
        )
    )

    data_agendamento_convertida = (
        date.fromisoformat(
            ligacao["data_agendamento"]
        )
    )

    data_ligacao_convertida = (
        date.fromisoformat(
            data_ligacao_normalizada
        )
    )

    if (
        data_ligacao_convertida
        < data_agendamento_convertida
    ):
        raise ValueError(
            "A data da Ligação não pode ser "
            "anterior à data agendada."
        )

    ligacao_candidata = ligacao.copy()

    ligacao_candidata["status"] = (
        StatusLigacao.CONCLUIDA.value
    )

    ligacao_candidata[
        "data_ligacao"
    ] = data_ligacao_normalizada

    ligacao_candidata[
        "responsavel_ligacao"
    ] = responsavel_normalizado

    if observacoes is not None:
        ligacao_candidata["observacoes"] = (
            observacoes_normalizadas
        )

    validar_ligacao(
        ligacao_candidata
    )

    return ligacao_candidata


def criar_dados_planejamento_instalacao(
    data_prevista: str,
    responsavel_planejamento: str,
    equipe_responsavel: str,
    observacoes: str | None = None,
) -> dict:
    """
    Cria o registro inicial de planejamento
    da Instalação.

    A Instalação nasce com status PLANEJADA.
    Os dados de início e conclusão permanecem
    ausentes até que esses eventos ocorram.
    """

    data_prevista_normalizada = (
        _validar_data_iso(
            data_prevista,
            "Data prevista da Instalação",
        )
    )

    responsavel_normalizado = (
        _validar_texto_obrigatorio(
            responsavel_planejamento,
            "Responsável pelo planejamento",
        )
    )

    equipe_normalizada = (
        _validar_texto_obrigatorio(
            equipe_responsavel,
            "Equipe responsável",
        )
    )

    observacoes_normalizadas = (
        _normalizar_texto_opcional(
            observacoes,
            "Observações da Instalação",
        )
    )

    return {
        "status": StatusInstalacao.PLANEJADA.value,
        "data_prevista": (
            data_prevista_normalizada
        ),
        "responsavel_planejamento": (
            responsavel_normalizado
        ),
        "equipe_responsavel": (
            equipe_normalizada
        ),
        "data_inicio": None,
        "responsavel_inicio": None,
        "data_conclusao": None,
        "responsavel_conclusao": None,
        "observacoes": observacoes_normalizadas,
    }

def validar_instalacao(
    instalacao: dict,
) -> None:
    """
    Valida a estrutura mínima de uma Instalação.

    A validação considera os três estados internos:

    - PLANEJADA;
    - EM_EXECUCAO;
    - CONCLUIDA.
    """

    if not isinstance(
        instalacao,
        dict,
    ):
        raise TypeError(
            "Instalação deve ser representada "
            "por um dicionário."
        )

    campos_obrigatorios = (
        "status",
        "data_prevista",
        "responsavel_planejamento",
        "equipe_responsavel",
        "data_inicio",
        "responsavel_inicio",
        "data_conclusao",
        "responsavel_conclusao",
        "observacoes",
    )

    for campo in campos_obrigatorios:
        if campo not in instalacao:
            raise ValueError(
                "Estrutura de Instalação inválida: "
                f"campo ausente: {campo}."
            )

    try:
        status_instalacao = StatusInstalacao(
            instalacao["status"]
        )

    except (
        ValueError,
        TypeError,
    ) as erro:
        raise ValueError(
            "Status de Instalação inválido: "
            f"{instalacao.get('status')!r}."
        ) from erro

    _validar_data_iso(
        instalacao["data_prevista"],
        "Data prevista da Instalação",
    )

    _validar_texto_obrigatorio(
        instalacao["responsavel_planejamento"],
        "Responsável pelo planejamento",
    )

    _validar_texto_obrigatorio(
        instalacao["equipe_responsavel"],
        "Equipe responsável",
    )

    _normalizar_texto_opcional(
        instalacao["observacoes"],
        "Observações da Instalação",
    )

    if status_instalacao == StatusInstalacao.PLANEJADA:
        if (
            instalacao["data_inicio"] is not None
            or instalacao["responsavel_inicio"] is not None
            or instalacao["data_conclusao"] is not None
            or instalacao["responsavel_conclusao"] is not None
        ):
            raise ValueError(
                "Uma Instalação planejada não pode possuir "
                "dados de início ou conclusão."
            )

    elif status_instalacao == StatusInstalacao.EM_EXECUCAO:
        _validar_data_iso(
            instalacao["data_inicio"],
            "Data de início da Instalação",
        )

        _validar_texto_obrigatorio(
            instalacao["responsavel_inicio"],
            "Responsável pelo início",
        )

        if (
            instalacao["data_conclusao"] is not None
            or instalacao["responsavel_conclusao"] is not None
        ):
            raise ValueError(
                "Uma Instalação em execução não pode possuir "
                "dados de conclusão."
            )

    elif status_instalacao == StatusInstalacao.CONCLUIDA:
        _validar_data_iso(
            instalacao["data_inicio"],
            "Data de início da Instalação",
        )

        _validar_texto_obrigatorio(
            instalacao["responsavel_inicio"],
            "Responsável pelo início",
        )

        _validar_data_iso(
            instalacao["data_conclusao"],
            "Data de conclusão da Instalação",
        )

        _validar_texto_obrigatorio(
            instalacao["responsavel_conclusao"],
            "Responsável pela conclusão",
        )

def preparar_inicio_instalacao(
    instalacao: dict,
    data_inicio: str,
    responsavel_inicio: str,
) -> dict:
    """
    Prepara uma cópia da Instalação com o início
    da execução registrado.

    A função não modifica a Instalação recebida.
    """

    validar_instalacao(
        instalacao
    )

    status_atual = StatusInstalacao(
        instalacao["status"]
    )

    if status_atual != StatusInstalacao.PLANEJADA:
        raise ValueError(
            "Somente uma Instalação planejada "
            "pode ser iniciada."
        )

    data_inicio_normalizada = (
        _validar_data_iso(
            data_inicio,
            "Data de início da Instalação",
        )
    )

    responsavel_normalizado = (
        _validar_texto_obrigatorio(
            responsavel_inicio,
            "Responsável pelo início",
        )
    )

    data_prevista = date.fromisoformat(
        instalacao["data_prevista"]
    )

    data_inicio_convertida = date.fromisoformat(
        data_inicio_normalizada
    )

    if data_inicio_convertida < data_prevista:
        raise ValueError(
            "A data de início da Instalação não pode "
            "ser anterior à data prevista."
        )

    instalacao_candidata = instalacao.copy()

    instalacao_candidata["status"] = (
        StatusInstalacao.EM_EXECUCAO.value
    )

    instalacao_candidata["data_inicio"] = (
        data_inicio_normalizada
    )

    instalacao_candidata["responsavel_inicio"] = (
        responsavel_normalizado
    )

    validar_instalacao(
        instalacao_candidata
    )

    return instalacao_candidata

def preparar_conclusao_instalacao(
    instalacao: dict,
    data_conclusao: str,
    responsavel_conclusao: str,
    observacoes: str | None = None,
) -> dict:
    """
    Prepara uma cópia da Instalação com sua
    conclusão registrada.

    A função não modifica a Instalação recebida.
    """

    validar_instalacao(
        instalacao
    )

    status_atual = StatusInstalacao(
        instalacao["status"]
    )

    if status_atual != StatusInstalacao.EM_EXECUCAO:
        raise ValueError(
            "Somente uma Instalação em execução "
            "pode ser concluída."
        )

    data_conclusao_normalizada = (
        _validar_data_iso(
            data_conclusao,
            "Data de conclusão da Instalação",
        )
    )

    responsavel_normalizado = (
        _validar_texto_obrigatorio(
            responsavel_conclusao,
            "Responsável pela conclusão",
        )
    )

    observacoes_normalizadas = (
        _normalizar_texto_opcional(
            observacoes,
            "Observações da Instalação",
        )
    )

    data_inicio_convertida = date.fromisoformat(
        instalacao["data_inicio"]
    )

    data_conclusao_convertida = date.fromisoformat(
        data_conclusao_normalizada
    )

    if (
        data_conclusao_convertida
        < data_inicio_convertida
    ):
        raise ValueError(
            "A data de conclusão da Instalação "
            "não pode ser anterior à data de início."
        )

    instalacao_candidata = instalacao.copy()

    instalacao_candidata["status"] = (
        StatusInstalacao.CONCLUIDA.value
    )

    instalacao_candidata["data_conclusao"] = (
        data_conclusao_normalizada
    )

    instalacao_candidata[
        "responsavel_conclusao"
    ] = responsavel_normalizado

    if observacoes is not None:
        instalacao_candidata["observacoes"] = (
            observacoes_normalizadas
        )

    validar_instalacao(
        instalacao_candidata
    )

    return instalacao_candidata
