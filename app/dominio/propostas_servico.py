"""
Regras de domínio das Propostas de Serviço.

Este módulo representa:

- a Proposta comercial apresentada por uma Empresa;
- as versões comerciais da Proposta;
- o versionamento das condições negociadas;
- as regras próprias do ciclo de vida da Proposta.

Não é responsabilidade deste módulo:

- alterar Solicitações de Serviço;
- criar Contratações;
- selecionar Empresas no marketplace;
- liberar dados de contato;
- executar persistência;
- realizar operações de interface.
"""

from dataclasses import dataclass
from datetime import date
from types import MappingProxyType
from typing import Mapping

from app.dominio.erros_dominio import (
    DadosObrigatoriosAusentes,
    OperacaoNaoPermitida,
    ValorInvalido,
)

from app.dominio.status_proposta_servico import (
    STATUS_INICIAL,
    STATUS_PROPOSTA_SERVICO,
    pode_alterar_condicoes_comerciais,
    transicao_permitida,
)

from app.dominio.servicos_empresa import (
    ServicoOfertadoEmpresa,
)

from app.dominio.areas_atendimento import (
    area_atende_localidade,
)

from app.dominio.solicitacoes_servico import (
    ModalidadeSolicitacaoServico,
    SolicitacaoServico,
)

from app.dominio.status_solicitacao_servico import (
    pode_receber_propostas,
)

STATUS_TRANSICAO_CONTEXTUAL = {
    "ACEITA",
    "RECUSADA",
    "NAO_SELECIONADA",
    "EXPIRADA",
}

@dataclass(frozen=True)
class VersaoPropostaServico:
    """
    Representa uma versão imutável
    das condições comerciais de uma Proposta.
    """

    numero: int
    valor: float
    prazo_execucao_dias: int
    validade: date
    descricao_tecnica: str
    itens_incluidos: tuple[str, ...]
    itens_nao_incluidos: tuple[str, ...]
    garantias: Mapping
    condicoes_comerciais: Mapping
    observacoes: str | None

@dataclass
class PropostaServico:
    """
    Representa a negociação comercial
    apresentada por uma Empresa
    em resposta a uma Solicitação de Serviço.
    """

    codigo: int
    codigo_solicitacao: int
    codigo_empresa: int
    codigo_servico_ofertado_empresa: int | None
    _versoes: list[VersaoPropostaServico]
    status: str

    @property
    def versoes(
        self,
    ) -> tuple[VersaoPropostaServico, ...]:
        """
        Retorna uma visão imutável
        do histórico de versões da Proposta.
        """

        return tuple(self._versoes)

def _validar_codigo(
    codigo,
    nome_campo: str,
) -> int:
    """
    Valida identificadores inteiros positivos
    utilizados pela Proposta de Serviço.
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

def _validar_codigo_opcional(
    codigo,
    nome_campo: str,
) -> int | None:
    """
    Valida um identificador opcional.
    """

    if codigo is None:
        return None

    return _validar_codigo(
        codigo,
        nome_campo,
    )

def _validar_numero_versao(
    numero,
) -> int:
    """
    Valida o número sequencial
    de uma versão de Proposta.
    """

    if (
        not isinstance(numero, int)
        or isinstance(numero, bool)
        or numero <= 0
    ):
        raise ValorInvalido(
            "Número da versão deve ser "
            "um inteiro maior que zero."
        )

    return numero

def _validar_valor_proposta(
    valor,
) -> float:
    """
    Valida o valor comercial
    da versão da Proposta.
    """

    if (
        isinstance(valor, bool)
        or not isinstance(
            valor,
            (int, float),
        )
        or valor <= 0
    ):
        raise ValorInvalido(
            "Valor da Proposta deve ser "
            "numérico e maior que zero."
        )

    return float(valor)

def _validar_prazo_execucao(
    prazo_execucao_dias,
) -> int:
    """
    Valida o prazo estimado
    de execução do Serviço.
    """

    if (
        not isinstance(
            prazo_execucao_dias,
            int,
        )
        or isinstance(
            prazo_execucao_dias,
            bool,
        )
        or prazo_execucao_dias <= 0
    ):
        raise ValorInvalido(
            "Prazo de execução deve ser "
            "um inteiro maior que zero."
        )

    return prazo_execucao_dias

def _validar_validade(
    validade,
) -> date:
    """
    Valida a data limite
    de validade da versão.
    """

    if not isinstance(
        validade,
        date,
    ):
        raise ValorInvalido(
            "Validade deve ser uma data."
        )

    return validade

def _validar_descricao_tecnica(
    descricao_tecnica,
) -> str:
    """
    Valida a descrição técnica
    da versão da Proposta.
    """

    if not isinstance(
        descricao_tecnica,
        str,
    ):
        raise ValorInvalido(
            "Descrição técnica deve ser texto."
        )

    descricao_normalizada = (
        descricao_tecnica.strip()
    )

    if not descricao_normalizada:
        raise DadosObrigatoriosAusentes(
            "Descrição técnica é obrigatória."
        )

    return descricao_normalizada

def _normalizar_lista_textos(
    valores,
    nome_campo: str,
) -> tuple[str, ...]:
    """
    Valida e converte uma coleção
    textual para estrutura imutável.
    """

    if valores is None:
        return ()

    if not isinstance(
        valores,
        (list, tuple),
    ):
        raise ValorInvalido(
            f"{nome_campo} deve ser "
            "uma lista ou tupla."
        )

    resultado = []
    valores_identificados = set()

    for valor in valores:
        if not isinstance(valor, str):
            raise ValorInvalido(
                f"{nome_campo} deve conter "
                "apenas textos."
            )

        valor_normalizado = valor.strip()

        if not valor_normalizado:
            raise ValorInvalido(
                f"{nome_campo} não pode conter "
                "texto vazio."
            )

        chave_comparacao = (
            valor_normalizado.casefold()
        )

        if chave_comparacao in valores_identificados:
            raise ValorInvalido(
                f"{nome_campo} não pode conter "
                "itens duplicados."
            )

        valores_identificados.add(
            chave_comparacao
        )

        resultado.append(
            valor_normalizado
        )

    return tuple(resultado)

def _validar_coerencia_itens_comerciais(
    itens_incluidos,
    itens_nao_incluidos,
) -> None:
    """
    Impede que o mesmo item comercial
    seja simultaneamente incluído
    e não incluído na versão.
    """

    incluidos_normalizados = {
        item.casefold()
        for item in itens_incluidos
    }

    nao_incluidos_normalizados = {
        item.casefold()
        for item in itens_nao_incluidos
    }

    if (
        incluidos_normalizados
        & nao_incluidos_normalizados
    ):
        raise ValorInvalido(
            "Um mesmo item não pode estar "
            "simultaneamente em itens incluídos "
            "e itens não incluídos."
        )

def _normalizar_mapeamento(
    valores,
    nome_campo: str,
) -> Mapping:
    """
    Copia e protege um mapeamento
    contra alteração externa.
    """

    if valores is None:
        valores = {}

    if not isinstance(valores, dict):
        raise ValorInvalido(
            f"{nome_campo} deve ser "
            "um dicionário."
        )

    return MappingProxyType(
        valores.copy()
    )

def _normalizar_observacoes(
    observacoes,
) -> str | None:
    """
    Normaliza observações opcionais.
    """

    if observacoes is None:
        return None

    if not isinstance(
        observacoes,
        str,
    ):
        raise ValorInvalido(
            "Observações devem ser texto."
        )

    observacoes_normalizadas = (
        observacoes.strip()
    )

    if not observacoes_normalizadas:
        return None

    return observacoes_normalizadas

def criar_versao_proposta_servico(
    numero,
    valor,
    prazo_execucao_dias,
    validade,
    descricao_tecnica,
    itens_incluidos=None,
    itens_nao_incluidos=None,
    garantias=None,
    condicoes_comerciais=None,
    observacoes=None,
) -> VersaoPropostaServico:
    """
    Cria uma versão validada
    de uma Proposta de Serviço.
    """

    itens_incluidos_normalizados = (
        _normalizar_lista_textos(
            itens_incluidos,
            "Itens incluídos",
        )
    )

    itens_nao_incluidos_normalizados = (
        _normalizar_lista_textos(
            itens_nao_incluidos,
            "Itens não incluídos",
        )
    )

    _validar_coerencia_itens_comerciais(
        itens_incluidos_normalizados,
        itens_nao_incluidos_normalizados,
    )

    return VersaoPropostaServico(
        numero=_validar_numero_versao(
            numero
        ),
        valor=_validar_valor_proposta(
            valor
        ),
        prazo_execucao_dias=(
            _validar_prazo_execucao(
                prazo_execucao_dias
            )
        ),
        validade=_validar_validade(
            validade
        ),
        descricao_tecnica=(
            _validar_descricao_tecnica(
                descricao_tecnica
            )
        ),
        itens_incluidos=(
            itens_incluidos_normalizados
        ),
        itens_nao_incluidos=(
            itens_nao_incluidos_normalizados
        ),
        garantias=_normalizar_mapeamento(
            garantias,
            "Garantias",
        ),
        condicoes_comerciais=(
            _normalizar_mapeamento(
                condicoes_comerciais,
                "Condições comerciais",
            )
        ),
        observacoes=_normalizar_observacoes(
            observacoes
        ),
    )

def criar_proposta_servico(
    codigo,
    codigo_solicitacao,
    codigo_empresa,
    primeira_versao,
    codigo_servico_ofertado_empresa=None,
) -> PropostaServico:
    """
    Cria uma Proposta de Serviço
    com sua primeira versão comercial.
    """

    if not isinstance(
        primeira_versao,
        VersaoPropostaServico,
    ):
        raise ValorInvalido(
            "Primeira versão deve ser uma "
            "VersaoPropostaServico válida."
        )

    if primeira_versao.numero != 1:
        raise ValorInvalido(
            "A primeira versão da Proposta "
            "deve possuir número 1."
        )

    return PropostaServico(
        codigo=_validar_codigo(
            codigo,
            "Código da Proposta",
        ),
        codigo_solicitacao=_validar_codigo(
            codigo_solicitacao,
            "Código da Solicitação",
        ),
        codigo_empresa=_validar_codigo(
            codigo_empresa,
            "Código da Empresa",
        ),
        codigo_servico_ofertado_empresa=(
            _validar_codigo_opcional(
                codigo_servico_ofertado_empresa,
                "Código do Serviço ofertado",
            )
        ),
        _versoes=[
            primeira_versao,
        ],
        status=STATUS_INICIAL,
    )

def validar_contexto_proposta_servico(
    proposta,
    solicitacao,
    servico_ofertado,
    distancia_km=None,
) -> None:
    """
    Valida o contexto relacional da Proposta
    em relação à Solicitação e à oferta.

    Aplica as invariantes comuns e as regras
    específicas das modalidades DIRETA
    e ABERTA.

    Para Área de Atendimento por RAIO,
    a distância deve ser previamente
    calculada e informada.
    """

    if not isinstance(
        proposta,
        PropostaServico,
    ):
        raise TypeError(
            "Proposta deve ser uma instância "
            "de PropostaServico."
        )

    if not isinstance(
        solicitacao,
        SolicitacaoServico,
    ):
        raise TypeError(
            "Solicitação deve ser uma instância "
            "de SolicitacaoServico."
        )

    if not isinstance(
        servico_ofertado,
        ServicoOfertadoEmpresa,
    ):
        raise TypeError(
            "Serviço oferecido deve ser uma instância "
            "de ServicoOfertadoEmpresa."
        )

    if not pode_receber_propostas(
        solicitacao.status
    ):
        raise OperacaoNaoPermitida(
            "A Solicitação deve estar em "
            "RECEBENDO_PROPOSTAS para aceitar "
            "uma nova Proposta."
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
        proposta.codigo_empresa
        != servico_ofertado.codigo_empresa
    ):
        raise ValorInvalido(
            "A Empresa da Proposta não corresponde "
            "à Empresa da oferta informada."
        )

    if (
        solicitacao.codigo_tipo_servico
        != servico_ofertado.codigo_tipo_servico
    ):
        raise ValorInvalido(
            "A oferta informada não corresponde "
            "ao Tipo de Serviço da Solicitação."
        )

    if (
        proposta.codigo_servico_ofertado_empresa
        is not None
        and proposta.codigo_servico_ofertado_empresa
        != servico_ofertado.codigo
    ):
        raise ValorInvalido(
            "A oferta informada não corresponde "
            "à oferta vinculada à Proposta."
        )

    if (
        solicitacao.modalidade
        == ModalidadeSolicitacaoServico.DIRETA
    ):
        if (
            solicitacao.codigo_empresa_destinataria
            is None
        ):
            raise ValorInvalido(
                "Solicitação DIRETA deve possuir "
                "Empresa destinatária."
            )

        if (
            solicitacao.codigo_servico_ofertado_empresa
            is None
        ):
            raise ValorInvalido(
                "Solicitação DIRETA deve possuir "
                "Serviço ofertado vinculado."
            )

        if (
            proposta.codigo_empresa
            != solicitacao.codigo_empresa_destinataria
        ):
            raise ValorInvalido(
                "A Empresa da Proposta deve ser "
                "a Empresa destinatária da "
                "Solicitação DIRETA."
            )

        if (
            proposta.codigo_servico_ofertado_empresa
            is None
        ):
            raise ValorInvalido(
                "Proposta para Solicitação DIRETA "
                "deve possuir Serviço ofertado "
                "vinculado."
            )

        if (
            proposta.codigo_servico_ofertado_empresa
            != solicitacao.codigo_servico_ofertado_empresa
        ):
            raise ValorInvalido(
                "A oferta da Proposta deve ser "
                "a oferta vinculada à "
                "Solicitação DIRETA."
            )

        if (
            servico_ofertado.codigo
            != solicitacao.codigo_servico_ofertado_empresa
        ):
            raise ValorInvalido(
                "A oferta informada deve ser "
                "a oferta vinculada à "
                "Solicitação DIRETA."
            )

    if (
        solicitacao.modalidade
        == ModalidadeSolicitacaoServico.ABERTA
    ):
        if (
            solicitacao.codigo_empresa_destinataria
            is not None
        ):
            raise ValorInvalido(
                "Solicitação ABERTA não deve possuir "
                "Empresa destinatária."
            )

        if (
            solicitacao.codigo_servico_ofertado_empresa
            is not None
        ):
            raise ValorInvalido(
                "Solicitação ABERTA não deve possuir "
                "Serviço ofertado previamente "
                "vinculado."
            )

        if (
            proposta.codigo_servico_ofertado_empresa
            is None
        ):
            raise ValorInvalido(
                "Proposta para Solicitação ABERTA "
                "deve possuir Serviço ofertado "
                "vinculado."
            )

        if not servico_ofertado.ativo:
            raise ValorInvalido(
                "Serviço ofertado deve estar ativo "
                "para participar de Solicitação "
                "ABERTA."
            )

        if not servico_ofertado.participa_marketplace:
            raise ValorInvalido(
                "Serviço ofertado deve participar "
                "do marketplace para receber "
                "Solicitação ABERTA."
            )

        if servico_ofertado.area_atendimento is None:
            raise ValorInvalido(
                "Serviço ofertado deve possuir "
                "Área de Atendimento configurada "
                "para receber Solicitação ABERTA."
            )

        if not area_atende_localidade(
            servico_ofertado.area_atendimento,
            municipio=solicitacao.municipio,
            uf=solicitacao.uf,
            distancia_km=distancia_km,
        ):
            raise ValorInvalido(
                "A localização da Solicitação "
                "não é atendida pela oferta."
            )

def obter_versao_atual_proposta(
    proposta,
) -> VersaoPropostaServico:
    """
    Retorna a versão comercial atual da Proposta.

    A versão atual é sempre a última versão
    registrada no histórico da Proposta.
    """

    if not isinstance(
        proposta,
        PropostaServico,
    ):
        raise ValorInvalido(
            "Proposta deve ser uma "
            "PropostaServico válida."
        )

    if not proposta._versoes:
        raise ValorInvalido(
            "Proposta deve possuir "
            "ao menos uma versão."
        )

    return proposta._versoes[-1]

def versao_proposta_esta_valida(
    versao,
    data_referencia=None,
) -> bool:
    """
    Informa se uma versão de Proposta
    ainda está dentro de sua validade comercial.

    Na ausência de data de referência,
    utiliza a data atual.

    A versão permanece válida durante
    todo o dia definido em sua validade.
    """

    if not isinstance(
        versao,
        VersaoPropostaServico,
    ):
        raise ValorInvalido(
            "Versão deve ser uma "
            "VersaoPropostaServico válida."
        )

    if data_referencia is None:
        data_referencia = date.today()

    if not isinstance(
        data_referencia,
        date,
    ):
        raise ValorInvalido(
            "Data de referência deve ser uma data."
        )

    return versao.validade >= data_referencia

def obter_proximo_numero_versao(
    proposta,
) -> int:
    """
    Retorna o número esperado
    para a próxima versão da Proposta.
    """

    versao_atual = (
        obter_versao_atual_proposta(
            proposta
        )
    )

    return versao_atual.numero + 1

def validar_permissao_alteracao_comercial(
    proposta,
) -> None:
    """
    Valida se a Proposta está em estado
    que permite trabalhar suas condições
    comerciais.

    Não altera status, histórico
    ou versões da Proposta.
    """

    if not isinstance(
        proposta,
        PropostaServico,
    ):
        raise ValorInvalido(
            "Proposta deve ser uma "
            "PropostaServico válida."
        )

    if not pode_alterar_condicoes_comerciais(
        proposta.status
    ):
        raise OperacaoNaoPermitida(
            "O estado atual da Proposta "
            "não permite alteração "
            "das condições comerciais."
        )

def registrar_nova_versao_proposta_servico(
    proposta,
    valor,
    prazo_execucao_dias,
    validade,
    descricao_tecnica,
    itens_incluidos=None,
    itens_nao_incluidos=None,
    garantias=None,
    condicoes_comerciais=None,
    observacoes=None,
) -> VersaoPropostaServico:
    """
    Cria e registra uma nova versão comercial
    no histórico da Proposta.

    O número da versão é determinado
    internamente pela sequência do histórico.
    """

    validar_permissao_alteracao_comercial(
        proposta
    )

    nova_versao = criar_versao_proposta_servico(
        numero=obter_proximo_numero_versao(
            proposta
        ),
        valor=valor,
        prazo_execucao_dias=prazo_execucao_dias,
        validade=validade,
        descricao_tecnica=descricao_tecnica,
        itens_incluidos=itens_incluidos,
        itens_nao_incluidos=itens_nao_incluidos,
        garantias=garantias,
        condicoes_comerciais=condicoes_comerciais,
        observacoes=observacoes,
    )

    proposta._versoes.append(
        nova_versao
    )

    return nova_versao

def alterar_status_proposta_servico(
    proposta,
    novo_status,
) -> None:
    """
    Altera o estado da Proposta de Serviço
    respeitando sua máquina de estados.

    A operação não altera versões,
    condições comerciais ou outros agregados.
    """

    if not isinstance(
        proposta,
        PropostaServico,
    ):
        raise ValorInvalido(
            "Proposta deve ser uma "
            "PropostaServico válida."
        )

    if not isinstance(
        novo_status,
        str,
    ):
        raise ValorInvalido(
            "Novo status deve ser texto."
        )

    if novo_status in STATUS_TRANSICAO_CONTEXTUAL:
        raise OperacaoNaoPermitida(
            "Esta transição exige uma "
            "operação contextual de domínio."
        )

    if not transicao_permitida(
        proposta.status,
        novo_status,
    ):
        raise OperacaoNaoPermitida(
            "Transição de status não permitida "
            "para a Proposta."
        )

    proposta.status = novo_status

def expirar_proposta_servico(
    proposta,
    data_referencia=None,
) -> None:
    """
    Expira uma Proposta quando sua versão
    comercial atual ultrapassou a validade.

    A expiração respeita a máquina de estados
    e não altera o histórico de versões.
    """

    if not isinstance(
        proposta,
        PropostaServico,
    ):
        raise ValorInvalido(
            "Proposta deve ser uma "
            "PropostaServico válida."
        )

    if data_referencia is None:
        data_referencia = date.today()

    if not isinstance(
        data_referencia,
        date,
    ):
        raise ValorInvalido(
            "Data de referência deve ser uma data."
        )

    versao_atual = obter_versao_atual_proposta(
        proposta
    )

    if versao_proposta_esta_valida(
        versao_atual,
        data_referencia=data_referencia,
    ):
        raise OperacaoNaoPermitida(
            "A Proposta ainda está dentro "
            "da validade comercial."
        )

    if not transicao_permitida(
        proposta.status,
        "EXPIRADA",
    ):
        raise OperacaoNaoPermitida(
            "O estado atual da Proposta "
            "não permite expiração."
        )

    proposta.status = "EXPIRADA"

def converter_versao_proposta_para_dicionario(
    versao,
) -> dict:
    """
    Converte uma versão de Proposta
    para uma estrutura serializável.

    A estrutura retornada não compartilha
    coleções mutáveis com a entidade original.
    """

    if not isinstance(
        versao,
        VersaoPropostaServico,
    ):
        raise ValorInvalido(
            "Versão deve ser uma "
            "VersaoPropostaServico válida."
        )

    return {
        "numero": versao.numero,
        "valor": versao.valor,
        "prazo_execucao_dias": (
            versao.prazo_execucao_dias
        ),
        "validade": versao.validade.isoformat(),
        "descricao_tecnica": (
            versao.descricao_tecnica
        ),
        "itens_incluidos": list(
            versao.itens_incluidos
        ),
        "itens_nao_incluidos": list(
            versao.itens_nao_incluidos
        ),
        "garantias": dict(
            versao.garantias
        ),
        "condicoes_comerciais": dict(
            versao.condicoes_comerciais
        ),
        "observacoes": versao.observacoes,
    }

def converter_proposta_servico_para_dicionario(
    proposta,
) -> dict:
    """
    Converte uma Proposta de Serviço
    e todo o seu histórico de versões
    para uma estrutura serializável.
    """

    if not isinstance(
        proposta,
        PropostaServico,
    ):
        raise ValorInvalido(
            "Proposta deve ser uma "
            "PropostaServico válida."
        )

    if not proposta._versoes:
        raise ValorInvalido(
            "Proposta deve possuir "
            "ao menos uma versão."
        )

    return {
        "codigo": proposta.codigo,
        "codigo_solicitacao": (
            proposta.codigo_solicitacao
        ),
        "codigo_empresa": (
            proposta.codigo_empresa
        ),
        "codigo_servico_ofertado_empresa": (
            proposta.codigo_servico_ofertado_empresa
        ),
        "versoes": [
            converter_versao_proposta_para_dicionario(
                versao
            )
            for versao in proposta._versoes
        ],
        "status": proposta.status,
    }

def buscar_proposta_servico_por_codigo(
    propostas: list[PropostaServico],
    codigo: int,
) -> PropostaServico | None:
    """
    Busca uma Proposta de Serviço
    pelo seu código.

    Retorna a Proposta encontrada
    ou None quando não houver correspondência.
    """

    codigo_validado = _validar_codigo(
        codigo,
        "Código da Proposta",
    )

    for proposta in propostas:
        if proposta.codigo == codigo_validado:
            return proposta

    return None

def listar_propostas_por_solicitacao(
    propostas: list[PropostaServico],
    codigo_solicitacao: int,
) -> list[PropostaServico]:
    """
    Retorna todas as Propostas
    vinculadas à Solicitação informada.
    """

    codigo_validado = _validar_codigo(
        codigo_solicitacao,
        "Código da Solicitação",
    )

    return [
        proposta
        for proposta in propostas
        if (
            proposta.codigo_solicitacao
            == codigo_validado
        )
    ]

def listar_propostas_por_empresa(
    propostas: list[PropostaServico],
    codigo_empresa: int,
) -> list[PropostaServico]:
    """
    Retorna todas as Propostas
    apresentadas pela Empresa informada.
    """

    codigo_validado = _validar_codigo(
        codigo_empresa,
        "Código da Empresa",
    )

    return [
        proposta
        for proposta in propostas
        if proposta.codigo_empresa == codigo_validado
    ]

def listar_propostas_por_servico_ofertado(
    propostas: list[PropostaServico],
    codigo_servico_ofertado_empresa: int,
) -> list[PropostaServico]:
    """
    Retorna todas as Propostas vinculadas
    ao Serviço Ofertado informado.
    """

    codigo_validado = _validar_codigo(
        codigo_servico_ofertado_empresa,
        "Código do Serviço ofertado",
    )

    return [
        proposta
        for proposta in propostas
        if (
            proposta.codigo_servico_ofertado_empresa
            == codigo_validado
        )
    ]

def _normalizar_status_consulta(
    status,
) -> str:
    """
    Valida e normaliza um status utilizado
    em consultas de Propostas de Serviço.
    """

    if not isinstance(
        status,
        str,
    ):
        raise ValorInvalido(
            "Status da Proposta deve ser texto."
        )

    status_normalizado = (
        status.strip().upper()
    )

    if not status_normalizado:
        raise ValorInvalido(
            "Status da Proposta é obrigatório."
        )

    if (
        status_normalizado
        not in STATUS_PROPOSTA_SERVICO.values()
    ):
        raise ValorInvalido(
            "Status da Proposta de Serviço inválido."
        )

    return status_normalizado

def listar_propostas_por_status(
    propostas: list[PropostaServico],
    status: str,
) -> list[PropostaServico]:
    """
    Retorna todas as Propostas
    que possuem o status informado.
    """

    status_normalizado = (
        _normalizar_status_consulta(
            status
        )
    )

    return [
        proposta
        for proposta in propostas
        if proposta.status == status_normalizado
    ]


