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
