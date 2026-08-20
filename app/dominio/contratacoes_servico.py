"""
Regras de domínio das Contratações de Serviço.

Uma Contratação representa a formalização comercial
originada de uma versão aceita de uma Proposta de Serviço.

Este módulo controla apenas as regras próprias
da Contratação.

Não é responsabilidade deste módulo:

- alterar Solicitações de Serviço;
- alterar Propostas de Serviço;
- selecionar a Proposta vencedora;
- criar Projetos ou Ordens de Serviço;
- liberar dados de contato;
- executar persistência;
- realizar operações de interface.
"""

from dataclasses import dataclass
from datetime import date
from types import MappingProxyType
from typing import Mapping

from app.dominio.erros_dominio import (
    ValorInvalido,
)

from app.dominio.propostas_servico import (
    PropostaServico,
    VersaoPropostaServico,
)

from app.dominio.solicitacoes_servico import (
    SolicitacaoServico,
)

from app.dominio.status_contratacao_servico import (
    STATUS_INICIAL,
    transicao_permitida,
)


@dataclass(frozen=True)
class SnapshotContratacaoServico:
    """
    Representa as condições comerciais
    efetivamente congeladas na Contratação.
    """

    numero_versao_proposta: int
    valor_contratado: float
    prazo_execucao_dias: int
    descricao_tecnica: str
    itens_incluidos: tuple[str, ...]
    itens_nao_incluidos: tuple[str, ...]
    garantias: Mapping
    condicoes_comerciais: Mapping
    observacoes: str | None

@dataclass(frozen=True)
class ReferenciaProcessoOperacional:
    """
    Identifica genericamente o processo operacional
    originado pela Contratação.
    """

    tipo: str
    codigo: int

@dataclass
class ContratacaoServico:
    """
    Representa a formalização de uma contratação
    originada de uma Proposta de Serviço.
    """

    codigo: int
    codigo_solicitacao: int
    codigo_cliente: int
    codigo_tipo_servico: int
    codigo_empresa: int
    codigo_servico_ofertado_empresa: int | None
    codigo_proposta: int
    snapshot: SnapshotContratacaoServico
    data_limite_formalizacao: date
    processo_operacional: ReferenciaProcessoOperacional | None
    status: str

def _validar_codigo(
    codigo,
    nome_campo: str,
) -> int:
    """
    Valida identificadores inteiros positivos
    utilizados pela Contratação.
    """

    if (
        not isinstance(codigo, int)
        or isinstance(codigo, bool)
        or codigo <= 0
    ):
        raise ValorInvalido(
            f"{nome_campo} deve ser "
            "um inteiro maior que zero."
        )

    return codigo

def _validar_colecao_contratacoes(
    contratacoes,
) -> None:
    """
    Valida uma coleção utilizada pelas
    consultas de Contratações.
    """

    if (
        contratacoes is None
        or isinstance(
            contratacoes,
            (str, bytes),
        )
    ):
        raise ValorInvalido(
            "Coleção de Contratações inválida."
        )

    try:
        iter(contratacoes)
    except TypeError as erro:
        raise ValorInvalido(
            "Coleção de Contratações inválida."
        ) from erro

    for contratacao in contratacoes:
        if not isinstance(
            contratacao,
            ContratacaoServico,
        ):
            raise ValorInvalido(
                "Coleção contém item que não é "
                "uma ContratacaoServico."
            )

def _normalizar_status(
    status,
) -> str:
    """
    Normaliza um status recebido por uma
    operação da Contratação.
    """

    if not isinstance(
        status,
        str,
    ):
        raise ValorInvalido(
            "Status da Contratação deve ser texto."
        )

    status_normalizado = (
        status.strip().upper()
    )

    if not status_normalizado:
        raise ValorInvalido(
            "Status da Contratação é obrigatório."
        )

    return status_normalizado

def _normalizar_tipo_processo_operacional(
    tipo,
) -> str:
    """
    Valida e normaliza o identificador
    do tipo de processo operacional.
    """

    if not isinstance(
        tipo,
        str,
    ):
        raise ValorInvalido(
            "Tipo do processo operacional deve ser texto."
        )

    tipo_normalizado = (
        tipo.strip().upper()
    )

    if not tipo_normalizado:
        raise ValorInvalido(
            "Tipo do processo operacional é obrigatório."
        )

    return tipo_normalizado

def _validar_consistencia_contratacao(
    contratacao,
) -> None:
    """
    Valida invariantes estruturais essenciais
    de uma Contratação já existente.
    """

    if not isinstance(
        contratacao,
        ContratacaoServico,
    ):
        raise TypeError(
            "Contratação deve ser uma instância "
            "de ContratacaoServico."
        )

    _validar_codigo(
        contratacao.codigo,
        "Código da Contratação",
    )

    if not isinstance(
        contratacao.snapshot,
        SnapshotContratacaoServico,
    ):
        raise ValorInvalido(
            "Snapshot da Contratação inválido."
        )

    if (
        not isinstance(
            contratacao.data_limite_formalizacao,
            date,
        )
        or isinstance(
            contratacao.data_limite_formalizacao,
            bool,
        )
    ):
        raise ValorInvalido(
            "Data-limite de formalização inválida."
        )

    status_normalizado = _normalizar_status(
        contratacao.status
    )

    if (
        status_normalizado
        != contratacao.status
    ):
        raise ValorInvalido(
            "Status armazenado da Contratação "
            "não está normalizado."
        )

    if (
        contratacao.processo_operacional
        is not None
        and not isinstance(
            contratacao.processo_operacional,
            ReferenciaProcessoOperacional,
        )
    ):
        raise ValorInvalido(
            "Referência do processo operacional inválida."
        )

    if (
        contratacao.status
        in {
            "PROCESSO_GERADO",
            "EM_ANDAMENTO",
            "CONCLUIDA",
        }
        and contratacao.processo_operacional is None
    ):
        raise ValorInvalido(
            "Status operacional exige processo "
            "operacional vinculado."
        )

    if (
        contratacao.processo_operacional
        is not None
        and contratacao.status
        in {
            "EM_FORMALIZACAO",
            "CONFIRMADA",
            "EXPIRADA",
        }
    ):
        raise ValorInvalido(
            "Processo operacional incompatível "
            "com o status da Contratação."
        )

def _copiar_mapeamento_imutavel(
    valores: Mapping,
) -> Mapping:
    """
    Cria uma cópia protegida de um mapeamento
    pertencente ao snapshot contratado.
    """

    return MappingProxyType(
        dict(valores)
    )

def criar_snapshot_contratacao_servico(
    versao: VersaoPropostaServico,
) -> SnapshotContratacaoServico:
    """
    Cria um snapshot imutável das condições
    comerciais da versão contratada.
    """

    if not isinstance(
        versao,
        VersaoPropostaServico,
    ):
        raise ValorInvalido(
            "Versão contratada deve ser uma "
            "VersaoPropostaServico válida."
        )

    return SnapshotContratacaoServico(
        numero_versao_proposta=versao.numero,
        valor_contratado=versao.valor,
        prazo_execucao_dias=(
            versao.prazo_execucao_dias
        ),
        descricao_tecnica=(
            versao.descricao_tecnica
        ),
        itens_incluidos=tuple(
            versao.itens_incluidos
        ),
        itens_nao_incluidos=tuple(
            versao.itens_nao_incluidos
        ),
        garantias=_copiar_mapeamento_imutavel(
            versao.garantias
        ),
        condicoes_comerciais=(
            _copiar_mapeamento_imutavel(
                versao.condicoes_comerciais
            )
        ),
        observacoes=versao.observacoes,
    )

def criar_contratacao_servico(
    codigo,
    solicitacao,
    proposta,
    versao_contratada,
) -> ContratacaoServico:
    """
    Cria o núcleo de uma Contratação de Serviço
    a partir da Solicitação, da Proposta
    e da versão comercial contratada.

    Nesta etapa, a função valida somente
    invariantes estruturais locais.

    A coordenação completa do aceite
    será implementada posteriormente.
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
        proposta,
        PropostaServico,
    ):
        raise TypeError(
            "Proposta deve ser uma instância "
            "de PropostaServico."
        )

    if not isinstance(
        versao_contratada,
        VersaoPropostaServico,
    ):
        raise TypeError(
            "Versão contratada deve ser uma instância "
            "de VersaoPropostaServico."
        )

    if (
        proposta.codigo_solicitacao
        != solicitacao.codigo
    ):
        raise ValorInvalido(
            "A Proposta não pertence à "
            "Solicitação informada."
        )

    if (
        versao_contratada
        not in proposta.versoes
    ):
        raise ValorInvalido(
            "A versão contratada não pertence "
            "à Proposta informada."
        )

    snapshot = (
        criar_snapshot_contratacao_servico(
            versao_contratada
        )
    )

    return ContratacaoServico(
        codigo=_validar_codigo(
            codigo,
            "Código da Contratação",
        ),
        codigo_solicitacao=(
            solicitacao.codigo
        ),
        codigo_cliente=(
            solicitacao.codigo_cliente
        ),
        codigo_tipo_servico=(
            solicitacao.codigo_tipo_servico
        ),
        codigo_empresa=(
            proposta.codigo_empresa
        ),
        codigo_servico_ofertado_empresa=(
            proposta.codigo_servico_ofertado_empresa
        ),
        codigo_proposta=(
            proposta.codigo
        ),
        snapshot=snapshot,
        data_limite_formalizacao=(
            versao_contratada.validade
        ),
        processo_operacional=None,
        status=STATUS_INICIAL,
    )

def alterar_status_contratacao_servico(
    contratacao,
    novo_status,
) -> None:
    """
    Executa uma transição local de status
    da Contratação de Serviço.

    Transições que exigem contexto adicional
    possuem operações próprias e não podem
    ser executadas por esta API genérica.
    """

    _validar_consistencia_contratacao(
        contratacao
    )

    status_normalizado = (
        _normalizar_status(
            novo_status
        )
    )

    if status_normalizado in {
        "EXPIRADA",
        "PROCESSO_GERADO",
    }:
        raise ValorInvalido(
            "A transição solicitada exige "
            "uma operação contextual própria."
        )

    if not transicao_permitida(
        contratacao.status,
        status_normalizado,
    ):
        raise ValorInvalido(
            "Transição de status da Contratação "
            "não permitida."
        )

    contratacao.status = (
        status_normalizado
    )

def expirar_contratacao_servico(
    contratacao,
    data_referencia: date,
) -> None:
    """
    Expira uma Contratação cuja formalização
    ultrapassou a data-limite permitida.
    """

    _validar_consistencia_contratacao(
        contratacao
    )

    if (
        not isinstance(data_referencia, date)
        or isinstance(data_referencia, bool)
    ):
        raise ValorInvalido(
            "Data de referência deve ser uma data válida."
        )

    if not transicao_permitida(
        contratacao.status,
        "EXPIRADA",
    ):
        raise ValorInvalido(
            "Contratação não pode ser expirada "
            "no status atual."
        )

    if (
        data_referencia
        <= contratacao.data_limite_formalizacao
    ):
        raise ValorInvalido(
            "Contratação ainda está dentro "
            "do prazo de formalização."
        )

    contratacao.status = "EXPIRADA"

def registrar_processo_operacional(
    contratacao,
    tipo_processo,
    codigo_processo,
) -> None:
    """
    Registra o processo operacional previamente
    criado para uma Contratação confirmada.
    """

    _validar_consistencia_contratacao(
        contratacao
    )

    tipo_normalizado = (
        _normalizar_tipo_processo_operacional(
            tipo_processo
        )
    )

    codigo_validado = _validar_codigo(
        codigo_processo,
        "Código do processo operacional",
    )

    if (
        contratacao.processo_operacional
        is not None
    ):
        raise ValorInvalido(
            "Contratação já possui processo "
            "operacional vinculado."
        )

    if not transicao_permitida(
        contratacao.status,
        "PROCESSO_GERADO",
    ):
        raise ValorInvalido(
            "Contratação não permite gerar processo "
            "operacional no status atual."
        )

    referencia = ReferenciaProcessoOperacional(
        tipo=tipo_normalizado,
        codigo=codigo_validado,
    )

    contratacao.processo_operacional = referencia
    contratacao.status = "PROCESSO_GERADO"

def buscar_contratacao_servico_por_codigo(
    contratacoes,
    codigo,
) -> ContratacaoServico | None:
    """
    Busca uma Contratação pelo código.

    Retorna None quando não encontrada.
    """

    _validar_colecao_contratacoes(
        contratacoes
    )

    codigo_validado = _validar_codigo(
        codigo,
        "Código da Contratação",
    )

    for contratacao in contratacoes:
        if contratacao.codigo == codigo_validado:
            return contratacao

    return None

def listar_contratacoes_por_solicitacao(
    contratacoes,
    codigo_solicitacao,
) -> list[ContratacaoServico]:
    """
    Retorna as Contratações vinculadas
    a uma Solicitação.
    """

    _validar_colecao_contratacoes(
        contratacoes
    )

    codigo_validado = _validar_codigo(
        codigo_solicitacao,
        "Código da Solicitação",
    )

    return [
        contratacao
        for contratacao in contratacoes
        if (
            contratacao.codigo_solicitacao
            == codigo_validado
        )
    ]

def listar_contratacoes_por_cliente(
    contratacoes,
    codigo_cliente,
) -> list[ContratacaoServico]:
    """
    Retorna as Contratações vinculadas
    a um Cliente.
    """

    _validar_colecao_contratacoes(
        contratacoes
    )

    codigo_validado = _validar_codigo(
        codigo_cliente,
        "Código do Cliente",
    )

    return [
        contratacao
        for contratacao in contratacoes
        if contratacao.codigo_cliente == codigo_validado
    ]

def listar_contratacoes_por_empresa(
    contratacoes,
    codigo_empresa,
) -> list[ContratacaoServico]:
    """
    Retorna as Contratações vinculadas
    a uma Empresa.
    """

    _validar_colecao_contratacoes(
        contratacoes
    )

    codigo_validado = _validar_codigo(
        codigo_empresa,
        "Código da Empresa",
    )

    return [
        contratacao
        for contratacao in contratacoes
        if contratacao.codigo_empresa == codigo_validado
    ]

def listar_contratacoes_por_tipo_servico(
    contratacoes,
    codigo_tipo_servico,
) -> list[ContratacaoServico]:
    """
    Retorna as Contratações de determinado
    Tipo de Serviço.
    """

    _validar_colecao_contratacoes(
        contratacoes
    )

    codigo_validado = _validar_codigo(
        codigo_tipo_servico,
        "Código do Tipo de Serviço",
    )

    return [
        contratacao
        for contratacao in contratacoes
        if (
            contratacao.codigo_tipo_servico
            == codigo_validado
        )
    ]

def listar_contratacoes_por_proposta(
    contratacoes,
    codigo_proposta,
) -> list[ContratacaoServico]:
    """
    Retorna as Contratações originadas
    de determinada Proposta.
    """

    _validar_colecao_contratacoes(
        contratacoes
    )

    codigo_validado = _validar_codigo(
        codigo_proposta,
        "Código da Proposta",
    )

    return [
        contratacao
        for contratacao in contratacoes
        if contratacao.codigo_proposta == codigo_validado
    ]

def listar_contratacoes_por_status(
    contratacoes,
    status,
) -> list[ContratacaoServico]:
    """
    Retorna as Contratações que possuem
    determinado status.
    """

    _validar_colecao_contratacoes(
        contratacoes
    )

    status_normalizado = _normalizar_status(
        status
    )

    return [
        contratacao
        for contratacao in contratacoes
        if contratacao.status == status_normalizado
    ]

def listar_contratacoes_por_processo_operacional(
    contratacoes,
    tipo_processo,
    codigo_processo,
) -> list[ContratacaoServico]:
    """
    Retorna as Contratações vinculadas
    a determinado processo operacional.
    """

    _validar_colecao_contratacoes(
        contratacoes
    )

    tipo_normalizado = (
        _normalizar_tipo_processo_operacional(
            tipo_processo
        )
    )

    codigo_validado = _validar_codigo(
        codigo_processo,
        "Código do processo operacional",
    )

    return [
        contratacao
        for contratacao in contratacoes
        if (
            contratacao.processo_operacional
            is not None
            and (
                contratacao.processo_operacional.tipo
                == tipo_normalizado
            )
            and (
                contratacao.processo_operacional.codigo
                == codigo_validado
            )
        )
    ]

