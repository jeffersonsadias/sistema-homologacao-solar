"""
Regras de domínio das Movimentações dos Serviços.

Uma Movimentação representa um fato permanente ocorrido
durante o ciclo de vida de uma entidade dos Serviços
da Plataforma.

Movimentação e Notificação são responsabilidades distintas.

Este módulo não:

- altera Solicitações;
- altera Propostas;
- altera Contratações;
- altera Ordens de Serviço;
- altera Autorizações de Contato;
- executa a operação que originou o fato;
- envia notificações;
- executa persistência;
- realiza operações de interface.
"""

from dataclasses import dataclass
from datetime import datetime
from enum import Enum
from types import MappingProxyType
from typing import Mapping

from app.dominio.erros_dominio import (
    DadosObrigatoriosAusentes,
    ValorInvalido,
)

class TipoAtorMovimentacaoServico(
    str,
    Enum,
):
    """
    Identifica quem originou uma Movimentação.
    """

    CLIENTE = "CLIENTE"
    EMPRESA = "EMPRESA"
    PLATAFORMA = "PLATAFORMA"
    SISTEMA = "SISTEMA"

@dataclass(frozen=True)
class MovimentacaoServico:
    """
    Registro imutável de um fato ocorrido
    no ecossistema de Serviços da Plataforma.
    """

    codigo: int

    entidade_tipo: str
    entidade_codigo: int

    tipo_evento: str
    data_hora: datetime

    ator_tipo: TipoAtorMovimentacaoServico
    ator_codigo: int | None

    status_anterior: str | None
    status_novo: str | None

    descricao: str

    dados_anteriores: Mapping
    dados_novos: Mapping

def _validar_codigo(
    codigo,
    nome_campo: str,
) -> int:
    """
    Valida um identificador inteiro positivo.
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

def _normalizar_identificador_textual(
    valor,
    nome_campo: str,
) -> str:
    """
    Normaliza identificadores textuais utilizados
    para entidade, evento e status.
    """

    if not isinstance(
        valor,
        str,
    ):
        raise ValorInvalido(
            f"{nome_campo} deve ser texto."
        )

    valor_normalizado = (
        valor.strip().upper()
    )

    if not valor_normalizado:
        raise DadosObrigatoriosAusentes(
            f"{nome_campo} é obrigatório."
        )

    return valor_normalizado

def _normalizar_texto_obrigatorio(
    valor,
    nome_campo: str,
) -> str:
    """
    Normaliza um texto descritivo obrigatório.
    """

    if not isinstance(
        valor,
        str,
    ):
        raise ValorInvalido(
            f"{nome_campo} deve ser texto."
        )

    valor_normalizado = " ".join(
        valor.strip().split()
    )

    if not valor_normalizado:
        raise DadosObrigatoriosAusentes(
            f"{nome_campo} é obrigatório."
        )

    return valor_normalizado

def _normalizar_status_opcional(
    status,
    nome_campo: str,
) -> str | None:
    """
    Normaliza um status opcional.
    """

    if status is None:
        return None

    return _normalizar_identificador_textual(
        status,
        nome_campo,
    )

def _normalizar_ator_tipo(
    ator_tipo,
) -> TipoAtorMovimentacaoServico:
    """
    Normaliza o tipo do ator responsável
    pela Movimentação.
    """

    if isinstance(
        ator_tipo,
        TipoAtorMovimentacaoServico,
    ):
        return ator_tipo

    if not isinstance(
        ator_tipo,
        str,
    ):
        raise ValorInvalido(
            "Tipo do ator deve ser texto."
        )

    try:
        return TipoAtorMovimentacaoServico(
            ator_tipo.strip().upper()
        )
    except ValueError as erro:
        raise ValorInvalido(
            "Tipo do ator da Movimentação inválido."
        ) from erro

def _validar_ator_codigo(
    ator_tipo,
    ator_codigo,
) -> int | None:
    """
    Valida a relação entre o tipo do ator
    e seu identificador.
    """

    if ator_tipo in {
        TipoAtorMovimentacaoServico.CLIENTE,
        TipoAtorMovimentacaoServico.EMPRESA,
    }:
        if ator_codigo is None:
            raise DadosObrigatoriosAusentes(
                "Código do ator é obrigatório "
                "para CLIENTE ou EMPRESA."
            )

        return _validar_codigo(
            ator_codigo,
            "Código do ator",
        )

    if ator_codigo is not None:
        raise ValorInvalido(
            "PLATAFORMA e SISTEMA não devem "
            "possuir código de ator."
        )

    return None

def _validar_data_hora(
    data_hora,
) -> datetime:
    """
    Valida o instante em que o fato ocorreu.
    """

    if not isinstance(
        data_hora,
        datetime,
    ):
        raise ValorInvalido(
            "Data/hora da Movimentação "
            "deve ser válida."
        )

    return data_hora

def _copiar_mapeamento_imutavel(
    valores,
    nome_campo: str,
) -> Mapping:
    """
    Copia e protege os dados históricos
    contra alteração externa posterior.
    """

    if valores is None:
        valores = {}

    if not isinstance(
        valores,
        Mapping,
    ):
        raise ValorInvalido(
            f"{nome_campo} deve ser "
            "um mapeamento."
        )

    return MappingProxyType(
        dict(valores)
    )

def _validar_integridade_movimentacao(
    movimentacao,
) -> MovimentacaoServico:
    """
    Valida a integridade estrutural e semântica
    de uma Movimentação já existente.
    """

    if not isinstance(
        movimentacao,
        MovimentacaoServico,
    ):
        raise ValorInvalido(
            "Movimentação de Serviço inválida."
        )

    _validar_codigo(
        movimentacao.codigo,
        "Código da Movimentação",
    )

    entidade_tipo_normalizado = (
        _normalizar_identificador_textual(
            movimentacao.entidade_tipo,
            "Tipo da entidade",
        )
    )

    if (
        movimentacao.entidade_tipo
        != entidade_tipo_normalizado
    ):
        raise ValorInvalido(
            "Tipo da entidade da Movimentação "
            "está inconsistente."
        )

    _validar_codigo(
        movimentacao.entidade_codigo,
        "Código da entidade",
    )

    tipo_evento_normalizado = (
        _normalizar_identificador_textual(
            movimentacao.tipo_evento,
            "Tipo do evento",
        )
    )

    if (
        movimentacao.tipo_evento
        != tipo_evento_normalizado
    ):
        raise ValorInvalido(
            "Tipo do evento da Movimentação "
            "está inconsistente."
        )

    _validar_data_hora(
        movimentacao.data_hora
    )

    ator_tipo_normalizado = (
        _normalizar_ator_tipo(
            movimentacao.ator_tipo
        )
    )

    if (
        movimentacao.ator_tipo
        != ator_tipo_normalizado
    ):
        raise ValorInvalido(
            "Tipo do ator da Movimentação "
            "está inconsistente."
        )

    _validar_ator_codigo(
        ator_tipo_normalizado,
        movimentacao.ator_codigo,
    )

    descricao_normalizada = (
        _normalizar_texto_obrigatorio(
            movimentacao.descricao,
            "Descrição da Movimentação",
        )
    )

    if (
        movimentacao.descricao
        != descricao_normalizada
    ):
        raise ValorInvalido(
            "Descrição da Movimentação "
            "está inconsistente."
        )

    if not isinstance(
        movimentacao.dados_anteriores,
        Mapping,
    ):
        raise ValorInvalido(
            "Dados anteriores da Movimentação "
            "estão inválidos."
        )

    if not isinstance(
        movimentacao.dados_novos,
        Mapping,
    ):
        raise ValorInvalido(
            "Dados novos da Movimentação "
            "estão inválidos."
        )

    if tipo_evento_normalizado == "STATUS_ALTERADO":
        status_anterior = (
            _normalizar_identificador_textual(
                movimentacao.status_anterior,
                "Status anterior",
            )
        )

        status_novo = (
            _normalizar_identificador_textual(
                movimentacao.status_novo,
                "Status novo",
            )
        )

        if (
            movimentacao.status_anterior
            != status_anterior
            or movimentacao.status_novo
            != status_novo
        ):
            raise ValorInvalido(
                "Estados da Movimentação "
                "estão inconsistentes."
            )

        if status_anterior == status_novo:
            raise ValorInvalido(
                "Alteração de status exige estados "
                "anterior e novo diferentes."
            )

        if (
            movimentacao.dados_anteriores.get(
                "status"
            )
            != status_anterior
        ):
            raise ValorInvalido(
                "Snapshot anterior está inconsistente "
                "com o status anterior."
            )

        if (
            movimentacao.dados_novos.get(
                "status"
            )
            != status_novo
        ):
            raise ValorInvalido(
                "Snapshot novo está inconsistente "
                "com o status novo."
            )

    else:
        if (
            movimentacao.status_anterior is not None
            or movimentacao.status_novo is not None
        ):
            raise ValorInvalido(
                "Evento contextual não deve possuir "
                "status anterior ou novo."
            )

    return movimentacao

def _validar_colecao_movimentacoes(
    movimentacoes,
) -> tuple[MovimentacaoServico, ...]:
    """
    Valida e normaliza uma coleção de Movimentações.
    """

    if movimentacoes is None:
        raise ValorInvalido(
            "Coleção de Movimentações é obrigatória."
        )

    if isinstance(
        movimentacoes,
        (
            str,
            bytes,
            Mapping,
        ),
    ):
        raise ValorInvalido(
            "Coleção de Movimentações inválida."
        )

    try:
        movimentacoes_normalizadas = tuple(
            movimentacoes
        )
    except TypeError as erro:
        raise ValorInvalido(
            "Coleção de Movimentações inválida."
        ) from erro

    for movimentacao in movimentacoes_normalizadas:
        _validar_integridade_movimentacao(
            movimentacao
        )

    return movimentacoes_normalizadas

def criar_movimentacao_servico(
    codigo,
    entidade_tipo,
    entidade_codigo,
    tipo_evento,
    data_hora,
    ator_tipo,
    ator_codigo,
    descricao,
    status_anterior=None,
    status_novo=None,
    dados_anteriores=None,
    dados_novos=None,
) -> MovimentacaoServico:
    """
    Cria um registro imutável de Movimentação.

    A função registra o fato recebido.
    Ela não executa a operação que originou
    esse acontecimento.
    """

    tipo_evento_normalizado = (
        _normalizar_identificador_textual(
            tipo_evento,
            "Tipo do evento",
        )
    )

    status_anterior_normalizado = (
        _normalizar_status_opcional(
            status_anterior,
            "Status anterior",
        )
    )

    status_novo_normalizado = (
        _normalizar_status_opcional(
            status_novo,
            "Status novo",
        )
    )

    if tipo_evento_normalizado == "STATUS_ALTERADO":
        if (
            status_anterior_normalizado is None
            or status_novo_normalizado is None
        ):
            raise DadosObrigatoriosAusentes(
                "Alteração de status exige status "
                "anterior e status novo."
            )

        if (
            status_anterior_normalizado
            == status_novo_normalizado
        ):
            raise ValorInvalido(
                "Alteração de status exige estados "
                "anterior e novo diferentes."
            )

    elif (
        status_anterior_normalizado is not None
        or status_novo_normalizado is not None
    ):
        raise ValorInvalido(
            "Evento contextual não deve possuir "
            "status anterior ou novo."
        )

    ator_tipo_normalizado = (
        _normalizar_ator_tipo(
            ator_tipo
        )
    )

    ator_codigo_validado = (
        _validar_ator_codigo(
            ator_tipo_normalizado,
            ator_codigo,
        )
    )

    dados_anteriores_protegidos = (
        _copiar_mapeamento_imutavel(
            dados_anteriores,
            "Dados anteriores",
        )
    )

    dados_novos_protegidos = (
        _copiar_mapeamento_imutavel(
            dados_novos,
            "Dados novos",
        )
    )

    if tipo_evento_normalizado == "STATUS_ALTERADO":
        if (
            dados_anteriores_protegidos.get("status")
            != status_anterior_normalizado
        ):
            raise ValorInvalido(
                "Snapshot anterior deve refletir "
                "o status anterior."
            )

        if (
            dados_novos_protegidos.get("status")
            != status_novo_normalizado
        ):
            raise ValorInvalido(
                "Snapshot novo deve refletir "
                "o status novo."
            )

    return MovimentacaoServico(
        codigo=_validar_codigo(
            codigo,
            "Código da Movimentação",
        ),
        entidade_tipo=(
            _normalizar_identificador_textual(
                entidade_tipo,
                "Tipo da entidade",
            )
        ),
        entidade_codigo=_validar_codigo(
            entidade_codigo,
            "Código da entidade",
        ),
        tipo_evento=tipo_evento_normalizado,
        data_hora=_validar_data_hora(
            data_hora
        ),
        ator_tipo=ator_tipo_normalizado,
        ator_codigo=ator_codigo_validado,
        status_anterior=status_anterior_normalizado,
        status_novo=status_novo_normalizado,
        descricao=_normalizar_texto_obrigatorio(
            descricao,
            "Descrição da Movimentação",
        ),
        dados_anteriores=dados_anteriores_protegidos,
        dados_novos=dados_novos_protegidos,
    )

def criar_movimentacao_alteracao_status(
    codigo,
    entidade_tipo,
    entidade_codigo,
    data_hora,
    ator_tipo,
    ator_codigo,
    status_anterior,
    status_novo,
    descricao,
    dados_anteriores=None,
    dados_novos=None,
) -> MovimentacaoServico:
    """
    Registra uma alteração de status já ocorrida.

    Esta operação não altera o estado da entidade
    auditada. Ela apenas registra a transição.
    """

    status_anterior_normalizado = (
        _normalizar_identificador_textual(
            status_anterior,
            "Status anterior",
        )
    )

    status_novo_normalizado = (
        _normalizar_identificador_textual(
            status_novo,
            "Status novo",
        )
    )

    if (
        status_anterior_normalizado
        == status_novo_normalizado
    ):
        raise ValorInvalido(
            "Alteração de status exige estados "
            "anterior e novo diferentes."
        )

    anteriores = (
        {}
        if dados_anteriores is None
        else dict(
            _copiar_mapeamento_imutavel(
                dados_anteriores,
                "Dados anteriores",
            )
        )
    )

    novos = (
        {}
        if dados_novos is None
        else dict(
            _copiar_mapeamento_imutavel(
                dados_novos,
                "Dados novos",
            )
        )
    )

    anteriores["status"] = (
        status_anterior_normalizado
    )

    novos["status"] = (
        status_novo_normalizado
    )

    return criar_movimentacao_servico(
        codigo=codigo,
        entidade_tipo=entidade_tipo,
        entidade_codigo=entidade_codigo,
        tipo_evento="STATUS_ALTERADO",
        data_hora=data_hora,
        ator_tipo=ator_tipo,
        ator_codigo=ator_codigo,
        descricao=descricao,
        status_anterior=(
            status_anterior_normalizado
        ),
        status_novo=status_novo_normalizado,
        dados_anteriores=anteriores,
        dados_novos=novos,
    )

def criar_movimentacao_evento_contextual(
    codigo,
    entidade_tipo,
    entidade_codigo,
    tipo_evento,
    data_hora,
    ator_tipo,
    ator_codigo,
    descricao,
    dados_anteriores=None,
    dados_novos=None,
) -> MovimentacaoServico:
    """
    Registra um fato contextual que não representa,
    por si próprio, uma alteração de status.

    Eventos contextuais não carregam status anterior
    ou novo.
    """

    tipo_evento_normalizado = (
        _normalizar_identificador_textual(
            tipo_evento,
            "Tipo do evento",
        )
    )

    if tipo_evento_normalizado == "STATUS_ALTERADO":
        raise ValorInvalido(
            "STATUS_ALTERADO deve ser registrado "
            "pela operação específica de "
            "alteração de status."
        )

    return criar_movimentacao_servico(
        codigo=codigo,
        entidade_tipo=entidade_tipo,
        entidade_codigo=entidade_codigo,
        tipo_evento=tipo_evento_normalizado,
        data_hora=data_hora,
        ator_tipo=ator_tipo,
        ator_codigo=ator_codigo,
        descricao=descricao,
        status_anterior=None,
        status_novo=None,
        dados_anteriores=dados_anteriores,
        dados_novos=dados_novos,
    )

def buscar_movimentacao_por_codigo(
    movimentacoes,
    codigo,
) -> MovimentacaoServico | None:
    """
    Busca uma Movimentação pelo código.
    """

    movimentacoes_normalizadas = (
        _validar_colecao_movimentacoes(
            movimentacoes
        )
    )

    codigo_validado = _validar_codigo(
        codigo,
        "Código da Movimentação",
    )

    for movimentacao in movimentacoes_normalizadas:
        if movimentacao.codigo == codigo_validado:
            return movimentacao

    return None

def listar_movimentacoes_por_entidade(
    movimentacoes,
    entidade_tipo,
    entidade_codigo,
) -> tuple[MovimentacaoServico, ...]:
    """
    Lista as Movimentações de uma entidade específica.
    """

    movimentacoes_normalizadas = (
        _validar_colecao_movimentacoes(
            movimentacoes
        )
    )

    entidade_tipo_normalizado = (
        _normalizar_identificador_textual(
            entidade_tipo,
            "Tipo da entidade",
        )
    )

    entidade_codigo_validado = _validar_codigo(
        entidade_codigo,
        "Código da entidade",
    )

    return tuple(
        movimentacao
        for movimentacao
        in movimentacoes_normalizadas
        if (
            movimentacao.entidade_tipo
            == entidade_tipo_normalizado
            and movimentacao.entidade_codigo
            == entidade_codigo_validado
        )
    )

def listar_movimentacoes_por_tipo_evento(
    movimentacoes,
    tipo_evento,
) -> tuple[MovimentacaoServico, ...]:
    """
    Lista Movimentações pelo tipo de evento.
    """

    movimentacoes_normalizadas = (
        _validar_colecao_movimentacoes(
            movimentacoes
        )
    )

    tipo_evento_normalizado = (
        _normalizar_identificador_textual(
            tipo_evento,
            "Tipo do evento",
        )
    )

    return tuple(
        movimentacao
        for movimentacao
        in movimentacoes_normalizadas
        if (
            movimentacao.tipo_evento
            == tipo_evento_normalizado
        )
    )

def listar_movimentacoes_por_ator(
    movimentacoes,
    ator_tipo,
    ator_codigo=None,
) -> tuple[MovimentacaoServico, ...]:
    """
    Lista Movimentações originadas por determinado ator.
    """

    movimentacoes_normalizadas = (
        _validar_colecao_movimentacoes(
            movimentacoes
        )
    )

    ator_tipo_normalizado = (
        _normalizar_ator_tipo(
            ator_tipo
        )
    )

    ator_codigo_validado = (
        _validar_ator_codigo(
            ator_tipo_normalizado,
            ator_codigo,
        )
    )

    return tuple(
        movimentacao
        for movimentacao
        in movimentacoes_normalizadas
        if (
            movimentacao.ator_tipo
            == ator_tipo_normalizado
            and movimentacao.ator_codigo
            == ator_codigo_validado
        )
    )

def listar_movimentacoes_por_periodo(
    movimentacoes,
    data_hora_inicio,
    data_hora_fim,
) -> tuple[MovimentacaoServico, ...]:
    """
    Lista Movimentações ocorridas dentro de um período
    inclusivo.
    """

    movimentacoes_normalizadas = (
        _validar_colecao_movimentacoes(
            movimentacoes
        )
    )

    inicio = _validar_data_hora(
        data_hora_inicio
    )

    fim = _validar_data_hora(
        data_hora_fim
    )

    if fim < inicio:
        raise ValorInvalido(
            "Data/hora final não pode ser anterior "
            "à data/hora inicial."
        )

    return tuple(
        movimentacao
        for movimentacao
        in movimentacoes_normalizadas
        if inicio <= movimentacao.data_hora <= fim
    )


