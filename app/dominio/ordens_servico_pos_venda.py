"""
Regras de domínio das Ordens de Serviço Pós-venda.

Uma Ordem de Serviço representa o processo operacional
de atendimento pós-venda originado de uma Contratação
de Serviço.

Este módulo controla apenas as regras próprias
da Ordem de Serviço.

Não é responsabilidade deste módulo:

- alterar Contratações de Serviço;
- alterar Solicitações ou Propostas;
- controlar pagamentos;
- controlar garantias;
- executar persistência;
- realizar operações de interface.
"""

from dataclasses import dataclass
from datetime import date, time

from app.dominio.contratacoes_servico import (
    ContratacaoServico,
)

from app.dominio.erros_dominio import (
    ValorInvalido,
)

from app.dominio.status_ordem_servico import (
    STATUS_INICIAL,
    STATUS_ORDEM_SERVICO,
    transicao_permitida,
)

RESULTADOS_EXECUCAO = (
    "RESOLVIDO",
    "PARCIALMENTE_RESOLVIDO",
    "NAO_RESOLVIDO",
    "RETORNO_NECESSARIO",
)

@dataclass(frozen=True)
class ExecucaoOrdemServico:
    """
    Registro imutável de uma execução ou visita
    realizada no contexto de uma Ordem de Serviço.
    """

    numero: int
    data_execucao: date
    responsaveis: tuple[str, ...]
    hora_inicio: time
    hora_fim: time
    descricao_executada: str
    diagnostico: str | None
    solucao_aplicada: str | None
    materiais_utilizados: tuple[str, ...]
    observacoes: str | None
    resultado: str

@dataclass
class OrdemServicoPosVenda:
    """
    Representa uma Ordem de Serviço Pós-venda
    vinculada a uma Contratação.
    """

    codigo: int
    codigo_contratacao: int
    codigo_cliente: int
    codigo_empresa: int
    codigo_tipo_servico: int
    descricao: str
    execucoes: tuple[ExecucaoOrdemServico, ...]
    status: str


def _validar_codigo(
    codigo,
    nome_campo: str,
) -> int:
    """
    Valida identificadores inteiros positivos
    utilizados pela Ordem de Serviço.
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

def _normalizar_descricao(
    descricao,
) -> str:
    """
    Valida e normaliza a descrição inicial
    da Ordem de Serviço.
    """

    if not isinstance(
        descricao,
        str,
    ):
        raise ValorInvalido(
            "Descrição da Ordem de Serviço "
            "deve ser texto."
        )

    descricao_normalizada = (
        descricao.strip()
    )

    if not descricao_normalizada:
        raise ValorInvalido(
            "Descrição da Ordem de Serviço "
            "é obrigatória."
        )

    return descricao_normalizada

def _normalizar_texto_obrigatorio(
    valor,
    nome_campo: str,
) -> str:
    """
    Valida e normaliza um texto obrigatório.
    """

    if not isinstance(
        valor,
        str,
    ):
        raise ValorInvalido(
            f"{nome_campo} deve ser texto."
        )

    valor_normalizado = valor.strip()

    if not valor_normalizado:
        raise ValorInvalido(
            f"{nome_campo} é obrigatório."
        )

    return valor_normalizado

def _normalizar_texto_opcional(
    valor,
    nome_campo: str,
) -> str | None:
    """
    Valida e normaliza um texto opcional.
    """

    if valor is None:
        return None

    if not isinstance(
        valor,
        str,
    ):
        raise ValorInvalido(
            f"{nome_campo} deve ser texto ou None."
        )

    valor_normalizado = valor.strip()

    if not valor_normalizado:
        return None

    return valor_normalizado

def _normalizar_lista_textual(
    valores,
    nome_campo: str,
    *,
    obrigatoria: bool,
) -> tuple[str, ...]:
    """
    Valida uma coleção textual e devolve
    uma tupla normalizada.
    """

    if (
        valores is None
        or isinstance(
            valores,
            (str, bytes),
        )
    ):
        raise ValorInvalido(
            f"{nome_campo} deve ser uma coleção."
        )

    try:
        itens = tuple(valores)
    except TypeError as erro:
        raise ValorInvalido(
            f"{nome_campo} deve ser uma coleção."
        ) from erro

    itens_normalizados = []

    for item in itens:
        itens_normalizados.append(
            _normalizar_texto_obrigatorio(
                item,
                nome_campo,
            )
        )

    if (
        obrigatoria
        and not itens_normalizados
    ):
        raise ValorInvalido(
            f"{nome_campo} deve possuir "
            "ao menos um item."
        )

    return tuple(
        itens_normalizados
    )

def _normalizar_resultado_execucao(
    resultado,
) -> str:
    """
    Valida e normaliza o resultado
    de uma execução.
    """

    resultado_normalizado = (
        _normalizar_texto_obrigatorio(
            resultado,
            "Resultado da execução",
        ).upper()
    )

    if (
        resultado_normalizado
        not in RESULTADOS_EXECUCAO
    ):
        raise ValorInvalido(
            "Resultado da execução inválido."
        )

    return resultado_normalizado

def _normalizar_status(
    status,
) -> str:
    """
    Valida e normaliza um status textual
    de Ordem de Serviço.
    """

    status_normalizado = (
        _normalizar_texto_obrigatorio(
            status,
            "Status da Ordem de Serviço",
        ).upper()
    )

    if (
        status_normalizado
        not in STATUS_ORDEM_SERVICO.values()
    ):
        raise ValorInvalido(
            "Status da Ordem de Serviço inválido."
        )

    return status_normalizado

def _normalizar_colecao_ordens(
    ordens,
) -> tuple[OrdemServicoPosVenda, ...]:
    """
    Valida uma coleção de Ordens de Serviço
    para operações de consulta.
    """

    if (
        ordens is None
        or isinstance(
            ordens,
            (str, bytes),
        )
    ):
        raise ValorInvalido(
            "Ordens devem ser uma coleção."
        )

    try:
        ordens_normalizadas = tuple(ordens)
    except TypeError as erro:
        raise ValorInvalido(
            "Ordens devem ser uma coleção."
        ) from erro

    for ordem in ordens_normalizadas:
        if not isinstance(
            ordem,
            OrdemServicoPosVenda,
        ):
            raise ValorInvalido(
                "Coleção contém Ordem de Serviço inválida."
            )

        _validar_integridade_ordem(
            ordem
        )

    return ordens_normalizadas

def _validar_integridade_ordem(
    ordem,
) -> None:
    """
    Valida a integridade estrutural e histórica
    de uma Ordem de Serviço existente.
    """

    if not isinstance(
        ordem,
        OrdemServicoPosVenda,
    ):
        raise TypeError(
            "Ordem deve ser uma instância "
            "de OrdemServicoPosVenda."
        )

    _validar_codigo(
        ordem.codigo,
        "Código da Ordem de Serviço",
    )

    _validar_codigo(
        ordem.codigo_contratacao,
        "Código da Contratação",
    )

    _validar_codigo(
        ordem.codigo_cliente,
        "Código do Cliente",
    )

    _validar_codigo(
        ordem.codigo_empresa,
        "Código da Empresa",
    )

    _validar_codigo(
        ordem.codigo_tipo_servico,
        "Código do Tipo de Serviço",
    )

    _normalizar_descricao(
        ordem.descricao
    )

    status_normalizado = _normalizar_status(
        ordem.status
    )

    if ordem.status != status_normalizado:
        raise ValorInvalido(
            "Status armazenado da Ordem de Serviço "
            "deve estar normalizado."
        )

    if not isinstance(
        ordem.execucoes,
        tuple,
    ):
        raise ValorInvalido(
            "Histórico de execuções deve ser uma tupla."
        )

    for indice, execucao in enumerate(
        ordem.execucoes,
        start=1,
    ):
        if not isinstance(
            execucao,
            ExecucaoOrdemServico,
        ):
            raise ValorInvalido(
                "Histórico contém execução inválida."
            )

        if execucao.numero != indice:
            raise ValorInvalido(
                "Histórico de execuções possui "
                "numeração inconsistente."
            )

    if status_normalizado in {
        "AGUARDANDO_CONFIRMACAO_CLIENTE",
        "EM_ANALISE_DE_CONTESTACAO",
        "CONCLUIDA",
    }:
        if (
            not ordem.execucoes
            or ordem.execucoes[-1].resultado
            != "RESOLVIDO"
        ):
            raise ValorInvalido(
                "Status da Ordem de Serviço é "
                "incompatível com seu histórico."
            )

    if status_normalizado == "RETORNO_NECESSARIO":
        if not ordem.execucoes:
            raise ValorInvalido(
                "Status da Ordem de Serviço é "
                "incompatível com seu histórico."
            )

def criar_ordem_servico_pos_venda(
    codigo,
    contratacao,
    descricao,
) -> OrdemServicoPosVenda:
    """
    Cria o núcleo de uma Ordem de Serviço
    Pós-venda a partir de uma Contratação.

    Nesta etapa são validadas apenas
    invariantes estruturais locais.
    """

    if not isinstance(
        contratacao,
        ContratacaoServico,
    ):
        raise TypeError(
            "Contratação deve ser uma instância "
            "de ContratacaoServico."
        )

    return OrdemServicoPosVenda(
        codigo=_validar_codigo(
            codigo,
            "Código da Ordem de Serviço",
        ),
        codigo_contratacao=(
            contratacao.codigo
        ),
        codigo_cliente=(
            contratacao.codigo_cliente
        ),
        codigo_empresa=(
            contratacao.codigo_empresa
        ),
        codigo_tipo_servico=(
            contratacao.codigo_tipo_servico
        ),
        descricao=_normalizar_descricao(
            descricao
        ),
        execucoes=(),
        status=STATUS_INICIAL,
    )

def criar_execucao_ordem_servico(
    numero,
    data_execucao,
    responsaveis,
    hora_inicio,
    hora_fim,
    descricao_executada,
    resultado,
    diagnostico=None,
    solucao_aplicada=None,
    materiais_utilizados=(),
    observacoes=None,
) -> ExecucaoOrdemServico:
    """
    Cria um registro imutável de execução
    de uma Ordem de Serviço.
    """

    numero_validado = _validar_codigo(
        numero,
        "Número da execução",
    )

    if (
        not isinstance(
            data_execucao,
            date,
        )
        or isinstance(
            data_execucao,
            bool,
        )
    ):
        raise ValorInvalido(
            "Data da execução deve ser uma data válida."
        )

    if (
        not isinstance(
            hora_inicio,
            time,
        )
        or not isinstance(
            hora_fim,
            time,
        )
    ):
        raise ValorInvalido(
            "Horários da execução devem ser válidos."
        )

    if hora_fim <= hora_inicio:
        raise ValorInvalido(
            "Horário final deve ser posterior "
            "ao horário inicial."
        )

    return ExecucaoOrdemServico(
        numero=numero_validado,
        data_execucao=data_execucao,
        responsaveis=_normalizar_lista_textual(
            responsaveis,
            "Responsáveis",
            obrigatoria=True,
        ),
        hora_inicio=hora_inicio,
        hora_fim=hora_fim,
        descricao_executada=(
            _normalizar_texto_obrigatorio(
                descricao_executada,
                "Descrição executada",
            )
        ),
        diagnostico=_normalizar_texto_opcional(
            diagnostico,
            "Diagnóstico",
        ),
        solucao_aplicada=(
            _normalizar_texto_opcional(
                solucao_aplicada,
                "Solução aplicada",
            )
        ),
        materiais_utilizados=(
            _normalizar_lista_textual(
                materiais_utilizados,
                "Materiais utilizados",
                obrigatoria=False,
            )
        ),
        observacoes=_normalizar_texto_opcional(
            observacoes,
            "Observações",
        ),
        resultado=_normalizar_resultado_execucao(
            resultado
        ),
    )

def registrar_execucao_ordem_servico(
    ordem,
    execucao,
) -> None:
    """
    Registra atomicamente uma execução
    realizada e aplica seu resultado ao fluxo
    da Ordem de Serviço.
    """

    _validar_integridade_ordem(
        ordem
    )

    if not isinstance(
        execucao,
        ExecucaoOrdemServico,
    ):
        raise TypeError(
            "Execução deve ser uma instância "
            "de ExecucaoOrdemServico."
        )

    if ordem.status != "EM_EXECUCAO":
        raise ValorInvalido(
            "Execução somente pode ser registrada "
            "quando a Ordem está EM_EXECUCAO."
        )

    numero_esperado = (
        len(ordem.execucoes) + 1
    )

    if execucao.numero != numero_esperado:
        raise ValorInvalido(
            "Número da execução deve respeitar "
            "a sequência da Ordem de Serviço."
        )

    if execucao.resultado == "RESOLVIDO":
        novo_status = (
            "AGUARDANDO_CONFIRMACAO_CLIENTE"
        )
    else:
        novo_status = (
            "RETORNO_NECESSARIO"
        )

    if not transicao_permitida(
        ordem.status,
        novo_status,
    ):
        raise ValorInvalido(
            "Resultado da execução incompatível "
            "com o status da Ordem de Serviço."
        )

    novo_historico = (
        ordem.execucoes
        + (execucao,)
    )

    ordem.execucoes = novo_historico
    ordem.status = novo_status

def alterar_status_ordem_servico(
    ordem,
    novo_status,
) -> None:
    """
    Executa uma transição local genérica
    da máquina de estados da Ordem de Serviço.

    Transições dependentes de eventos contextuais
    possuem operações próprias.
    """

    _validar_integridade_ordem(
        ordem
    )

    novo_status_normalizado = (
        _normalizar_status(
            novo_status
        )
    )

    status_contextuais = {
        "RETORNO_NECESSARIO",
        "AGUARDANDO_CONFIRMACAO_CLIENTE",
        "EM_ANALISE_DE_CONTESTACAO",
        "CONCLUIDA",
    }

    if (
        novo_status_normalizado
        in status_contextuais
    ):
        raise ValorInvalido(
            "Status exige operação contextual própria."
        )

    if not transicao_permitida(
        ordem.status,
        novo_status_normalizado,
    ):
        raise ValorInvalido(
            "Transição de status da Ordem de Serviço "
            "não permitida."
        )

    ordem.status = novo_status_normalizado

def confirmar_conclusao_ordem_servico(
    ordem,
) -> None:
    """
    Registra a confirmação do Cliente após
    uma execução tecnicamente resolvida.
    """

    _validar_integridade_ordem(
        ordem
    )

    if not transicao_permitida(
        ordem.status,
        "CONCLUIDA",
    ):
        raise ValorInvalido(
            "Ordem de Serviço não pode ser "
            "concluída neste estado."
        )

    ordem.status = "CONCLUIDA"

def contestar_conclusao_ordem_servico(
    ordem,
) -> None:
    """
    Registra contestação do Cliente sobre
    a conclusão técnica apresentada.
    """

    _validar_integridade_ordem(
        ordem
    )

    if not transicao_permitida(
        ordem.status,
        "EM_ANALISE_DE_CONTESTACAO",
    ):
        raise ValorInvalido(
            "Ordem de Serviço não pode entrar "
            "em contestação neste estado."
        )

    ordem.status = (
        "EM_ANALISE_DE_CONTESTACAO"
    )

def resolver_contestacao_ordem_servico(
    ordem,
    *,
    requer_retorno,
) -> None:
    """
    Resolve uma contestação do Cliente.

    Quando requer_retorno=True, a Ordem volta
    ao fluxo operacional.

    Quando False, a conclusão é confirmada.
    """

    _validar_integridade_ordem(
        ordem
    )

    if not isinstance(
        requer_retorno,
        bool,
    ):
        raise ValorInvalido(
            "Indicador de retorno deve ser booleano."
        )

    novo_status = (
        "RETORNO_NECESSARIO"
        if requer_retorno
        else "CONCLUIDA"
    )

    if not transicao_permitida(
        ordem.status,
        novo_status,
    ):
        raise ValorInvalido(
            "Contestação não pode ser resolvida "
            "neste estado."
        )

    ordem.status = novo_status

def buscar_ordem_servico_por_codigo(
    ordens,
    codigo,
) -> OrdemServicoPosVenda | None:
    """
    Busca uma Ordem de Serviço pelo código.
    """

    ordens_normalizadas = (
        _normalizar_colecao_ordens(
            ordens
        )
    )

    codigo_validado = _validar_codigo(
        codigo,
        "Código da Ordem de Serviço",
    )

    for ordem in ordens_normalizadas:
        if ordem.codigo == codigo_validado:
            return ordem

    return None

def listar_ordens_por_contratacao(
    ordens,
    codigo_contratacao,
) -> list[OrdemServicoPosVenda]:
    """
    Lista Ordens de Serviço vinculadas
    a uma Contratação.
    """

    ordens_normalizadas = (
        _normalizar_colecao_ordens(
            ordens
        )
    )

    codigo_validado = _validar_codigo(
        codigo_contratacao,
        "Código da Contratação",
    )

    return [
        ordem
        for ordem in ordens_normalizadas
        if ordem.codigo_contratacao
        == codigo_validado
    ]

def listar_ordens_por_cliente(
    ordens,
    codigo_cliente,
) -> list[OrdemServicoPosVenda]:
    """
    Lista Ordens de Serviço de um Cliente.
    """

    ordens_normalizadas = (
        _normalizar_colecao_ordens(
            ordens
        )
    )

    codigo_validado = _validar_codigo(
        codigo_cliente,
        "Código do Cliente",
    )

    return [
        ordem
        for ordem in ordens_normalizadas
        if ordem.codigo_cliente
        == codigo_validado
    ]

def listar_ordens_por_empresa(
    ordens,
    codigo_empresa,
) -> list[OrdemServicoPosVenda]:
    """
    Lista Ordens de Serviço de uma Empresa.
    """

    ordens_normalizadas = (
        _normalizar_colecao_ordens(
            ordens
        )
    )

    codigo_validado = _validar_codigo(
        codigo_empresa,
        "Código da Empresa",
    )

    return [
        ordem
        for ordem in ordens_normalizadas
        if ordem.codigo_empresa
        == codigo_validado
    ]

def listar_ordens_por_tipo_servico(
    ordens,
    codigo_tipo_servico,
) -> list[OrdemServicoPosVenda]:
    """
    Lista Ordens de Serviço de um
    determinado Tipo de Serviço.
    """

    ordens_normalizadas = (
        _normalizar_colecao_ordens(
            ordens
        )
    )

    codigo_validado = _validar_codigo(
        codigo_tipo_servico,
        "Código do Tipo de Serviço",
    )

    return [
        ordem
        for ordem in ordens_normalizadas
        if ordem.codigo_tipo_servico
        == codigo_validado
    ]

def listar_ordens_por_status(
    ordens,
    status,
) -> list[OrdemServicoPosVenda]:
    """
    Lista Ordens de Serviço que estão
    em determinado status.
    """

    ordens_normalizadas = (
        _normalizar_colecao_ordens(
            ordens
        )
    )

    status_normalizado = _normalizar_status(
        status
    )

    return [
        ordem
        for ordem in ordens_normalizadas
        if ordem.status
        == status_normalizado
    ]

