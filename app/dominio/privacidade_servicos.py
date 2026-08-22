"""
Regras de domínio de privacidade e autorização
de contato dos Serviços da Plataforma.

Este módulo representa permissões explícitas
para que uma Empresa tenha acesso aos dados
de contato de um Cliente.

Não é responsabilidade deste módulo:

- alterar Solicitações de Serviço;
- alterar Propostas de Serviço;
- alterar Contratações de Serviço;
- selecionar a Proposta vencedora;
- coordenar o aceite;
- armazenar os dados pessoais do Cliente;
- executar persistência;
- realizar operações de interface.
"""

from dataclasses import dataclass
from datetime import datetime
from enum import Enum

from app.dominio.contratacoes_servico import (
    ContratacaoServico,
)

from app.dominio.erros_dominio import (
    OperacaoNaoPermitida,
    ValorInvalido,
)

from app.dominio.solicitacoes_servico import (
    ModalidadeSolicitacaoServico,
    SolicitacaoServico,
)

class MotivoAutorizacaoContato(
    str,
    Enum,
):
    """
    Motivo que originou a autorização
    de acesso ao contato do Cliente.
    """

    SOLICITACAO_DIRETA = "SOLICITACAO_DIRETA"
    PROPOSTA_ACEITA = "PROPOSTA_ACEITA"

@dataclass
class AutorizacaoContato:
    """
    Representa uma autorização rastreável
    de acesso aos dados de contato do Cliente.
    """

    codigo: int
    codigo_cliente: int
    codigo_empresa: int
    codigo_solicitacao: int
    codigo_contratacao: int | None
    motivo: MotivoAutorizacaoContato
    data_hora_liberacao: datetime
    ativo: bool
    data_hora_revogacao: datetime | None

def _validar_codigo(
    codigo,
    nome_campo: str,
) -> int:
    """
    Valida identificadores inteiros positivos.
    """

    if (
        not isinstance(
            codigo,
            int,
        )
        or isinstance(
            codigo,
            bool,
        )
        or codigo <= 0
    ):
        raise ValorInvalido(
            f"{nome_campo} deve ser "
            "um inteiro maior que zero."
        )

    return codigo

def _validar_data_hora(
    valor,
    nome_campo: str,
) -> datetime:
    """
    Valida um instante temporal utilizado
    pela autorização.
    """

    if not isinstance(
        valor,
        datetime,
    ):
        raise ValorInvalido(
            f"{nome_campo} deve ser "
            "uma data e hora válida."
        )

    return valor

def _validar_integridade_autorizacao(
    autorizacao,
) -> AutorizacaoContato:
    """
    Valida a coerência estrutural e temporal
    de uma Autorização de Contato existente.
    """

    if not isinstance(
        autorizacao,
        AutorizacaoContato,
    ):
        raise ValorInvalido(
            "Autorização de Contato inválida."
        )

    _validar_codigo(
        autorizacao.codigo,
        "Código da Autorização",
    )

    _validar_codigo(
        autorizacao.codigo_cliente,
        "Código do Cliente",
    )

    _validar_codigo(
        autorizacao.codigo_empresa,
        "Código da Empresa",
    )

    _validar_codigo(
        autorizacao.codigo_solicitacao,
        "Código da Solicitação",
    )

    if not isinstance(
        autorizacao.motivo,
        MotivoAutorizacaoContato,
    ):
        raise ValorInvalido(
            "Motivo da Autorização de Contato inválido."
        )

    _validar_data_hora(
        autorizacao.data_hora_liberacao,
        "Data/hora de liberação",
    )

    if not isinstance(
        autorizacao.ativo,
        bool,
    ):
        raise ValorInvalido(
            "Estado da Autorização de Contato "
            "deve ser booleano."
        )

    if (
        autorizacao.motivo
        == MotivoAutorizacaoContato.SOLICITACAO_DIRETA
    ):
        if autorizacao.codigo_contratacao is not None:
            raise ValorInvalido(
                "Autorização por Solicitação DIRETA "
                "não pode possuir Contratação."
            )

    elif (
        autorizacao.motivo
        == MotivoAutorizacaoContato.PROPOSTA_ACEITA
    ):
        _validar_codigo(
            autorizacao.codigo_contratacao,
            "Código da Contratação",
        )

    if autorizacao.ativo:
        if autorizacao.data_hora_revogacao is not None:
            raise ValorInvalido(
                "Autorização ativa não pode possuir "
                "data/hora de revogação."
            )

    else:
        data_revogacao = _validar_data_hora(
            autorizacao.data_hora_revogacao,
            "Data/hora de revogação",
        )

        if (
            data_revogacao
            < autorizacao.data_hora_liberacao
        ):
            raise ValorInvalido(
                "Data/hora de revogação não pode ser "
                "anterior à liberação."
            )

    return autorizacao

def _validar_colecao_autorizacoes(
    autorizacoes,
) -> tuple[AutorizacaoContato, ...]:
    """
    Valida uma coleção utilizada por consultas
    e decisões de acesso a dados de contato.
    """

    if (
        autorizacoes is None
        or isinstance(
            autorizacoes,
            (str, bytes),
        )
    ):
        raise ValorInvalido(
            "Autorizações devem ser uma coleção."
        )

    try:
        autorizacoes_normalizadas = tuple(
            autorizacoes
        )
    except TypeError as erro:
        raise ValorInvalido(
            "Autorizações devem ser uma coleção."
        ) from erro

    for autorizacao in autorizacoes_normalizadas:
        _validar_integridade_autorizacao(
            autorizacao
        )

    return autorizacoes_normalizadas

def criar_autorizacao_contato_solicitacao_direta(
    codigo,
    solicitacao,
    data_hora_liberacao,
) -> AutorizacaoContato:
    """
    Cria autorização de contato originada
    de uma Solicitação DIRETA.

    Somente a Empresa destinatária da
    Solicitação recebe a autorização.
    """

    if not isinstance(
        solicitacao,
        SolicitacaoServico,
    ):
        raise TypeError(
            "Solicitação deve ser uma instância "
            "de SolicitacaoServico."
        )

    if (
        solicitacao.modalidade
        != ModalidadeSolicitacaoServico.DIRETA
    ):
        raise ValorInvalido(
            "Autorização por Solicitação DIRETA "
            "exige uma Solicitação DIRETA."
        )

    if (
        solicitacao.codigo_empresa_destinataria
        is None
    ):
        raise ValorInvalido(
            "Solicitação DIRETA deve possuir "
            "Empresa destinatária."
        )

    return AutorizacaoContato(
        codigo=_validar_codigo(
            codigo,
            "Código da Autorização",
        ),
        codigo_cliente=_validar_codigo(
            solicitacao.codigo_cliente,
            "Código do Cliente",
        ),
        codigo_empresa=_validar_codigo(
            solicitacao.codigo_empresa_destinataria,
            "Código da Empresa",
        ),
        codigo_solicitacao=_validar_codigo(
            solicitacao.codigo,
            "Código da Solicitação",
        ),
        codigo_contratacao=None,
        motivo=(
            MotivoAutorizacaoContato
            .SOLICITACAO_DIRETA
        ),
        data_hora_liberacao=_validar_data_hora(
            data_hora_liberacao,
            "Data/hora de liberação",
        ),
        ativo=True,
        data_hora_revogacao=None,
    )

def criar_autorizacao_contato_proposta_aceita(
    codigo,
    solicitacao,
    contratacao,
    data_hora_liberacao,
) -> AutorizacaoContato:
    """
    Cria autorização de contato para a Empresa
    vencedora de uma Solicitação ABERTA.

    A Contratação é utilizada como registro
    estrutural da relação efetivamente escolhida.
    """

    if not isinstance(
        solicitacao,
        SolicitacaoServico,
    ):
        raise TypeError(
            "Solicitação deve ser uma instância "
            "de SolicitacaoServico."
        )

    if not isinstance(
        contratacao,
        ContratacaoServico,
    ):
        raise TypeError(
            "Contratação deve ser uma instância "
            "de ContratacaoServico."
        )

    if (
        solicitacao.modalidade
        != ModalidadeSolicitacaoServico.ABERTA
    ):
        raise ValorInvalido(
            "Autorização por Proposta aceita "
            "exige uma Solicitação ABERTA."
        )

    if (
        contratacao.codigo_solicitacao
        != solicitacao.codigo
    ):
        raise ValorInvalido(
            "Contratação não pertence à "
            "Solicitação informada."
        )

    if (
        contratacao.codigo_cliente
        != solicitacao.codigo_cliente
    ):
        raise ValorInvalido(
            "Cliente da Contratação não corresponde "
            "ao Cliente da Solicitação."
        )

    return AutorizacaoContato(
        codigo=_validar_codigo(
            codigo,
            "Código da Autorização",
        ),
        codigo_cliente=_validar_codigo(
            solicitacao.codigo_cliente,
            "Código do Cliente",
        ),
        codigo_empresa=_validar_codigo(
            contratacao.codigo_empresa,
            "Código da Empresa",
        ),
        codigo_solicitacao=_validar_codigo(
            solicitacao.codigo,
            "Código da Solicitação",
        ),
        codigo_contratacao=_validar_codigo(
            contratacao.codigo,
            "Código da Contratação",
        ),
        motivo=(
            MotivoAutorizacaoContato
            .PROPOSTA_ACEITA
        ),
        data_hora_liberacao=_validar_data_hora(
            data_hora_liberacao,
            "Data/hora de liberação",
        ),
        ativo=True,
        data_hora_revogacao=None,
    )

def autorizacao_contato_esta_ativa(
    autorizacao,
) -> bool:
    """
    Informa se uma Autorização de Contato
    estruturalmente válida está atualmente ativa.
    """

    _validar_integridade_autorizacao(
        autorizacao
    )

    return autorizacao.ativo

def pode_visualizar_contato_cliente(
    solicitacao,
    codigo_empresa,
    autorizacoes,
) -> bool:
    """
    Informa se determinada Empresa possui
    autorização atual para visualizar os dados
    de contato do Cliente de uma Solicitação.

    A decisão depende da modalidade da Solicitação
    e de uma Autorização de Contato ativa.
    """

    if not isinstance(
        solicitacao,
        SolicitacaoServico,
    ):
        raise TypeError(
            "Solicitação deve ser uma instância "
            "de SolicitacaoServico."
        )

    codigo_empresa_validado = _validar_codigo(
        codigo_empresa,
        "Código da Empresa",
    )

    autorizacoes_normalizadas = (
        _validar_colecao_autorizacoes(
            autorizacoes
        )
    )

    if (
        solicitacao.modalidade
        == ModalidadeSolicitacaoServico.DIRETA
    ):
        if (
            solicitacao.codigo_empresa_destinataria
            != codigo_empresa_validado
        ):
            return False

        return any(
            autorizacao.ativo
            and autorizacao.codigo_cliente
            == solicitacao.codigo_cliente
            and autorizacao.codigo_empresa
            == codigo_empresa_validado
            and autorizacao.codigo_solicitacao
            == solicitacao.codigo
            and autorizacao.motivo
            == (
                MotivoAutorizacaoContato
                .SOLICITACAO_DIRETA
            )
            and autorizacao.codigo_contratacao
            is None
            for autorizacao
            in autorizacoes_normalizadas
        )

    if (
        solicitacao.modalidade
        == ModalidadeSolicitacaoServico.ABERTA
    ):
        return any(
            autorizacao.ativo
            and autorizacao.codigo_cliente
            == solicitacao.codigo_cliente
            and autorizacao.codigo_empresa
            == codigo_empresa_validado
            and autorizacao.codigo_solicitacao
            == solicitacao.codigo
            and autorizacao.motivo
            == (
                MotivoAutorizacaoContato
                .PROPOSTA_ACEITA
            )
            and autorizacao.codigo_contratacao
            is not None
            for autorizacao
            in autorizacoes_normalizadas
        )

    raise ValorInvalido(
        "Modalidade da Solicitação inválida."
    )

def revogar_autorizacao_contato(
    autorizacao,
    data_hora_revogacao,
) -> None:
    """
    Revoga uma Autorização de Contato ativa.

    A revogação não apaga o registro original
    da liberação.
    """

    _validar_integridade_autorizacao(
        autorizacao
    )

    data_validada = _validar_data_hora(
        data_hora_revogacao,
        "Data/hora de revogação",
    )

    if not autorizacao.ativo:
        raise OperacaoNaoPermitida(
            "Autorização de Contato já está revogada."
        )

    if (
        data_validada
        < autorizacao.data_hora_liberacao
    ):
        raise ValorInvalido(
            "Data/hora de revogação não pode ser "
            "anterior à liberação."
        )

    autorizacao.ativo = False
    autorizacao.data_hora_revogacao = (
        data_validada
    )

def buscar_autorizacao_contato_por_codigo(
    autorizacoes,
    codigo,
) -> AutorizacaoContato | None:
    """
    Busca uma Autorização de Contato
    por seu código.
    """

    autorizacoes_normalizadas = (
        _validar_colecao_autorizacoes(
            autorizacoes
        )
    )

    codigo_validado = _validar_codigo(
        codigo,
        "Código da Autorização",
    )

    for autorizacao in autorizacoes_normalizadas:
        if autorizacao.codigo == codigo_validado:
            return autorizacao

    return None

def listar_autorizacoes_por_cliente(
    autorizacoes,
    codigo_cliente,
) -> list[AutorizacaoContato]:
    """
    Lista as Autorizações vinculadas
    a determinado Cliente.
    """

    autorizacoes_normalizadas = (
        _validar_colecao_autorizacoes(
            autorizacoes
        )
    )

    codigo_validado = _validar_codigo(
        codigo_cliente,
        "Código do Cliente",
    )

    return [
        autorizacao
        for autorizacao
        in autorizacoes_normalizadas
        if autorizacao.codigo_cliente
        == codigo_validado
    ]

def listar_autorizacoes_por_empresa(
    autorizacoes,
    codigo_empresa,
) -> list[AutorizacaoContato]:
    """
    Lista as Autorizações vinculadas
    a determinada Empresa.
    """

    autorizacoes_normalizadas = (
        _validar_colecao_autorizacoes(
            autorizacoes
        )
    )

    codigo_validado = _validar_codigo(
        codigo_empresa,
        "Código da Empresa",
    )

    return [
        autorizacao
        for autorizacao
        in autorizacoes_normalizadas
        if autorizacao.codigo_empresa
        == codigo_validado
    ]

def listar_autorizacoes_por_solicitacao(
    autorizacoes,
    codigo_solicitacao,
) -> list[AutorizacaoContato]:
    """
    Lista as Autorizações vinculadas
    a determinada Solicitação.
    """

    autorizacoes_normalizadas = (
        _validar_colecao_autorizacoes(
            autorizacoes
        )
    )

    codigo_validado = _validar_codigo(
        codigo_solicitacao,
        "Código da Solicitação",
    )

    return [
        autorizacao
        for autorizacao
        in autorizacoes_normalizadas
        if autorizacao.codigo_solicitacao
        == codigo_validado
    ]

def listar_autorizacoes_por_contratacao(
    autorizacoes,
    codigo_contratacao,
) -> list[AutorizacaoContato]:
    """
    Lista as Autorizações vinculadas
    a determinada Contratação.
    """

    autorizacoes_normalizadas = (
        _validar_colecao_autorizacoes(
            autorizacoes
        )
    )

    codigo_validado = _validar_codigo(
        codigo_contratacao,
        "Código da Contratação",
    )

    return [
        autorizacao
        for autorizacao
        in autorizacoes_normalizadas
        if autorizacao.codigo_contratacao
        == codigo_validado
    ]

def listar_autorizacoes_ativas(
    autorizacoes,
) -> list[AutorizacaoContato]:
    """
    Lista somente as Autorizações
    atualmente ativas.
    """

    autorizacoes_normalizadas = (
        _validar_colecao_autorizacoes(
            autorizacoes
        )
    )

    return [
        autorizacao
        for autorizacao
        in autorizacoes_normalizadas
        if autorizacao.ativo
    ]




