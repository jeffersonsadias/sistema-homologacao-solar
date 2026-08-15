"""
Domínio das Solicitações de Serviço da Plataforma.

Uma Solicitação de Serviço representa uma necessidade
apresentada para contratação de determinado Tipo de Serviço.

A Solicitação pode ser:

- DIRETA:
    destinada a uma oferta específica de uma Empresa;

- ABERTA:
    disponibilizada posteriormente ao marketplace.

Este módulo controla apenas as regras próprias
da Solicitação.

Não realiza:

- entrada de dados com input();
- exibição de dados com print();
- leitura ou gravação de arquivos;
- distribuição de oportunidades no marketplace;
- cálculo geográfico;
- criação de propostas;
- aceite de propostas;
- criação de contratações;
- liberação de dados de contato.
"""

from dataclasses import asdict, dataclass
from enum import Enum

from app.dominio.erros_dominio import (
    DadosObrigatoriosAusentes,
    TransicaoEstadoInvalida,
    ValorInvalido,
)

from app.dominio.servicos_empresa import (
    ServicoOfertadoEmpresa,
)

from app.dominio.status_solicitacao_servico import (
    STATUS_INICIAL,
    TRANSICOES_PERMITIDAS,
    transicao_permitida,
)

from app.dominio.tipos_servico import (
    TipoServico,
    tipo_servico_esta_ativo,
)

class ModalidadeSolicitacaoServico(
    str,
    Enum,
):
    """
    Define como a Solicitação será destinada.
    """

    DIRETA = "DIRETA"
    ABERTA = "ABERTA"


class OrigemSolicitacaoServico(
    str,
    Enum,
):
    """
    Define quem originou a Solicitação.

    CLIENTE:
        necessidade iniciada pelo próprio Cliente.

    EMPRESA:
        atendimento originado externamente e
        registrado posteriormente pela Empresa.
    """

    CLIENTE = "CLIENTE"
    EMPRESA = "EMPRESA"

@dataclass
class SolicitacaoServico:
    """
    Representa uma necessidade concreta
    de Serviço apresentada para a Plataforma.

    A entidade mantém somente os identificadores
    necessários dos outros agregados.

    Solicitações DIRETAS possuem Empresa
    destinatária e Serviço oferecido vinculados.

    Solicitações ABERTAS não pertencem previamente
    a nenhuma Empresa.
    """

    codigo: int
    codigo_cliente: int
    codigo_tipo_servico: int

    modalidade: ModalidadeSolicitacaoServico
    origem: OrigemSolicitacaoServico

    municipio: str
    uf: str
    dados_tecnicos: dict

    codigo_empresa_destinataria: int | None = None
    codigo_servico_ofertado_empresa: int | None = None

    status: str = STATUS_INICIAL

def _validar_codigo(
    codigo: int,
    nome_campo: str,
) -> int:
    """
    Valida um identificador inteiro positivo.
    """

    if (
        isinstance(
            codigo,
            bool,
        )
        or not isinstance(
            codigo,
            int,
        )
    ):
        raise ValorInvalido(
            f"{nome_campo} deve ser "
            "um número inteiro."
        )

    if codigo <= 0:
        raise ValorInvalido(
            f"{nome_campo} deve ser "
            "maior que zero."
        )

    return codigo

def _normalizar_modalidade(
    modalidade,
) -> ModalidadeSolicitacaoServico:
    """
    Converte o valor informado para
    ModalidadeSolicitacaoServico.
    """

    if isinstance(
        modalidade,
        ModalidadeSolicitacaoServico,
    ):
        return modalidade

    try:
        return ModalidadeSolicitacaoServico(
            modalidade
        )

    except (ValueError, TypeError):
        raise ValorInvalido(
            "Modalidade da Solicitação "
            "de Serviço inválida."
        )

def _normalizar_origem(
    origem,
) -> OrigemSolicitacaoServico:
    """
    Converte o valor informado para
    OrigemSolicitacaoServico.
    """

    if isinstance(
        origem,
        OrigemSolicitacaoServico,
    ):
        return origem

    try:
        return OrigemSolicitacaoServico(
            origem
        )

    except (ValueError, TypeError):
        raise ValorInvalido(
            "Origem da Solicitação "
            "de Serviço inválida."
        )

def _normalizar_municipio(
    municipio: str,
) -> str:
    """
    Valida e normaliza o Município
    onde o Serviço será executado.
    """

    if municipio is None:
        raise DadosObrigatoriosAusentes(
            "Município da Solicitação é obrigatório."
        )

    if not isinstance(
        municipio,
        str,
    ):
        raise ValorInvalido(
            "Município da Solicitação "
            "deve ser um texto."
        )

    municipio_normalizado = " ".join(
        municipio.strip().split()
    )

    if not municipio_normalizado:
        raise DadosObrigatoriosAusentes(
            "Município da Solicitação é obrigatório."
        )

    return municipio_normalizado

def _normalizar_uf(
    uf: str,
) -> str:
    """
    Valida e normaliza a UF
    onde o Serviço será executado.
    """

    if uf is None:
        raise DadosObrigatoriosAusentes(
            "UF da Solicitação é obrigatória."
        )

    if not isinstance(
        uf,
        str,
    ):
        raise ValorInvalido(
            "UF da Solicitação deve ser um texto."
        )

    uf_normalizada = (
        uf.strip().upper()
    )

    if len(
        uf_normalizada
    ) != 2:
        raise ValorInvalido(
            "UF da Solicitação deve possuir "
            "exatamente 2 caracteres."
        )

    if not uf_normalizada.isalpha():
        raise ValorInvalido(
            "UF da Solicitação deve conter "
            "apenas letras."
        )

    return uf_normalizada

def _validar_dados_tecnicos(
    dados_tecnicos,
) -> dict:
    """
    Valida a estrutura de dados técnicos.

    Nesta etapa, o conteúdo específico depende
    do Tipo de Serviço e ainda não possui schema
    próprio.

    Uma cópia é retornada para evitar alteração
    externa silenciosa da Solicitação.
    """

    if dados_tecnicos is None:
        raise DadosObrigatoriosAusentes(
            "Dados técnicos da Solicitação "
            "são obrigatórios."
        )

    if not isinstance(
        dados_tecnicos,
        dict,
    ):
        raise ValorInvalido(
            "Dados técnicos da Solicitação "
            "devem ser um dicionário."
        )

    return dict(
        dados_tecnicos
    )

def _validar_cliente(
    cliente: dict,
) -> int:
    """
    Valida o Cliente vinculado à Solicitação
    e retorna seu código.
    """

    if not isinstance(
        cliente,
        dict,
    ):
        raise TypeError(
            "Cliente deve ser representado "
            "por um dicionário."
        )

    if "codigo" not in cliente:
        raise DadosObrigatoriosAusentes(
            "Cliente precisa possuir código."
        )

    return _validar_codigo(
        cliente["codigo"],
        "Código do Cliente",
    )

def _validar_tipo_servico(
    tipo_servico: TipoServico,
) -> TipoServico:
    """
    Valida o Tipo de Serviço solicitado.

    Somente Tipos de Serviço ativos podem
    gerar novas Solicitações.
    """

    if not isinstance(
        tipo_servico,
        TipoServico,
    ):
        raise TypeError(
            "Tipo de Serviço deve ser uma "
            "instância de TipoServico."
        )

    if not tipo_servico_esta_ativo(
        tipo_servico
    ):
        raise ValorInvalido(
            "Não é possível solicitar um "
            "Tipo de Serviço inativo."
        )

    return tipo_servico

def _validar_oferta_direta(
    servico_ofertado,
    tipo_servico: TipoServico,
) -> ServicoOfertadoEmpresa:
    """
    Valida a oferta utilizada em uma
    Solicitação DIRETA.

    A oferta:

    - deve existir;
    - deve estar ativa;
    - deve aceitar Solicitações DIRETAS;
    - deve corresponder ao Tipo solicitado.
    """

    if not isinstance(
        servico_ofertado,
        ServicoOfertadoEmpresa,
    ):
        raise TypeError(
            "Solicitação DIRETA exige uma "
            "instância de ServicoOfertadoEmpresa."
        )

    if not servico_ofertado.ativo:
        raise ValorInvalido(
            "Não é possível criar Solicitação DIRETA "
            "para uma oferta inativa."
        )

    if not servico_ofertado.aceita_solicitacao_direta:
        raise ValorInvalido(
            "A oferta informada não aceita "
            "Solicitações DIRETAS."
        )

    if (
        servico_ofertado.codigo_tipo_servico
        != tipo_servico.codigo
    ):
        raise ValorInvalido(
            "A oferta informada não corresponde "
            "ao Tipo de Serviço solicitado."
        )

    return servico_ofertado

def _validar_novo_status(
    novo_status: str,
) -> str:
    """
    Valida um status textual de
    Solicitação de Serviço.
    """

    if novo_status is None:
        raise DadosObrigatoriosAusentes(
            "Novo status da Solicitação "
            "é obrigatório."
        )

    if not isinstance(
        novo_status,
        str,
    ):
        raise ValorInvalido(
            "Novo status da Solicitação "
            "deve ser um texto."
        )

    status_normalizado = (
        novo_status.strip().upper()
    )

    if not status_normalizado:
        raise DadosObrigatoriosAusentes(
            "Novo status da Solicitação "
            "é obrigatório."
        )

    if (
        status_normalizado
        not in TRANSICOES_PERMITIDAS
    ):
        raise ValorInvalido(
            "Status da Solicitação "
            "de Serviço inválido."
        )

    return status_normalizado

def alterar_status_solicitacao_servico(
    solicitacao: SolicitacaoServico,
    novo_status: str,
) -> SolicitacaoServico:
    """
    Altera o status de uma Solicitação
    respeitando sua máquina de estados.

    A regra de transição pertence ao módulo
    status_solicitacao_servico.
    """

    if not isinstance(
        solicitacao,
        SolicitacaoServico,
    ):
        raise TypeError(
            "Solicitação deve ser uma instância "
            "de SolicitacaoServico."
        )

    status_normalizado = (
        _validar_novo_status(
            novo_status
        )
    )

    if not transicao_permitida(
        solicitacao.status,
        status_normalizado,
    ):
        raise TransicaoEstadoInvalida(
            "Transição de status da Solicitação "
            f"de '{solicitacao.status}' para "
            f"'{status_normalizado}' não é permitida."
        )

    solicitacao.status = status_normalizado

    return solicitacao

def criar_solicitacao_servico(
    codigo: int,
    cliente: dict,
    tipo_servico: TipoServico,
    modalidade,
    origem,
    municipio: str,
    uf: str,
    dados_tecnicos: dict,
    servico_ofertado=None,
) -> SolicitacaoServico:
    """
    Cria uma nova Solicitação de Serviço.

    Regras estruturais iniciais:

    - código deve ser inteiro positivo;
    - Cliente precisa possuir código válido;
    - Tipo de Serviço precisa estar ativo;
    - modalidade precisa ser reconhecida;
    - origem precisa ser reconhecida;
    - município e UF são obrigatórios;
    - dados técnicos devem ser dicionário;
    - nova Solicitação inicia EM_ELABORACAO.

    Solicitação DIRETA:
        exige uma oferta válida.

    Solicitação ABERTA:
        não pode possuir oferta previamente
        vinculada.
    """

    codigo_validado = _validar_codigo(
        codigo,
        "Código da Solicitação",
    )

    codigo_cliente = _validar_cliente(
        cliente
    )

    tipo_validado = _validar_tipo_servico(
        tipo_servico
    )

    modalidade_normalizada = (
        _normalizar_modalidade(
            modalidade
        )
    )

    origem_normalizada = (
        _normalizar_origem(
            origem
        )
    )

    municipio_normalizado = (
        _normalizar_municipio(
            municipio
        )
    )

    uf_normalizada = (
        _normalizar_uf(
            uf
        )
    )

    dados_tecnicos_validados = (
        _validar_dados_tecnicos(
            dados_tecnicos
        )
    )

    codigo_empresa_destinataria = None
    codigo_oferta = None

    if (
        modalidade_normalizada
        == ModalidadeSolicitacaoServico.DIRETA
    ):
        oferta_validada = _validar_oferta_direta(
            servico_ofertado,
            tipo_validado,
        )

        codigo_empresa_destinataria = (
            oferta_validada.codigo_empresa
        )

        codigo_oferta = (
            oferta_validada.codigo
        )

    elif servico_ofertado is not None:
        raise ValorInvalido(
            "Solicitação ABERTA não pode possuir "
            "Serviço oferecido previamente vinculado."
        )

    return SolicitacaoServico(
        codigo=codigo_validado,
        codigo_cliente=codigo_cliente,
        codigo_tipo_servico=(
            tipo_validado.codigo
        ),
        modalidade=(
            modalidade_normalizada
        ),
        origem=origem_normalizada,
        municipio=municipio_normalizado,
        uf=uf_normalizada,
        dados_tecnicos=(
            dados_tecnicos_validados
        ),
        codigo_empresa_destinataria=(
            codigo_empresa_destinataria
        ),
        codigo_servico_ofertado_empresa=(
            codigo_oferta
        ),
        status=STATUS_INICIAL,
    )

def converter_solicitacao_servico_para_dicionario(
    solicitacao: SolicitacaoServico,
) -> dict:
    """
    Converte a Solicitação para dicionário
    preparado para persistência futura.
    """

    if not isinstance(
        solicitacao,
        SolicitacaoServico,
    ):
        raise TypeError(
            "Solicitação deve ser uma instância "
            "de SolicitacaoServico."
        )

    dados = asdict(
        solicitacao
    )

    dados["modalidade"] = (
        solicitacao.modalidade.value
    )

    dados["origem"] = (
        solicitacao.origem.value
    )

    return dados

def buscar_solicitacao_servico_por_codigo(
    solicitacoes: list[SolicitacaoServico],
    codigo: int,
) -> SolicitacaoServico | None:
    """
    Busca uma Solicitação de Serviço
    pelo seu código.

    Retorna a Solicitação encontrada
    ou None quando não existir.
    """

    codigo_validado = _validar_codigo(
        codigo,
        "Código da Solicitação",
    )

    for solicitacao in solicitacoes:
        if solicitacao.codigo == codigo_validado:
            return solicitacao

    return None

def listar_solicitacoes_por_cliente(
    solicitacoes: list[SolicitacaoServico],
    codigo_cliente: int,
) -> list[SolicitacaoServico]:
    """
    Retorna todas as Solicitações
    vinculadas ao Cliente informado.
    """

    codigo_validado = _validar_codigo(
        codigo_cliente,
        "Código do Cliente",
    )

    return [
        solicitacao
        for solicitacao in solicitacoes
        if solicitacao.codigo_cliente
        == codigo_validado
    ]

def listar_solicitacoes_por_tipo_servico(
    solicitacoes: list[SolicitacaoServico],
    codigo_tipo_servico: int,
) -> list[SolicitacaoServico]:
    """
    Retorna todas as Solicitações
    vinculadas ao Tipo de Serviço informado.
    """

    codigo_validado = _validar_codigo(
        codigo_tipo_servico,
        "Código do Tipo de Serviço",
    )

    return [
        solicitacao
        for solicitacao in solicitacoes
        if solicitacao.codigo_tipo_servico
        == codigo_validado
    ]

def listar_solicitacoes_diretas_por_empresa(
    solicitacoes: list[SolicitacaoServico],
    codigo_empresa: int,
) -> list[SolicitacaoServico]:
    """
    Retorna Solicitações DIRETAS destinadas
    à Empresa informada.
    """

    codigo_validado = _validar_codigo(
        codigo_empresa,
        "Código da Empresa",
    )

    return [
        solicitacao
        for solicitacao in solicitacoes
        if (
            solicitacao.modalidade
            == ModalidadeSolicitacaoServico.DIRETA
            and solicitacao.codigo_empresa_destinataria
            == codigo_validado
        )
    ]

def listar_solicitacoes_por_modalidade(
    solicitacoes: list[SolicitacaoServico],
    modalidade,
) -> list[SolicitacaoServico]:
    """
    Retorna todas as Solicitações
    da modalidade informada.
    """

    modalidade_normalizada = (
        _normalizar_modalidade(
            modalidade
        )
    )

    return [
        solicitacao
        for solicitacao in solicitacoes
        if solicitacao.modalidade
        == modalidade_normalizada
    ]

def listar_solicitacoes_por_status(
    solicitacoes: list[SolicitacaoServico],
    status: str,
) -> list[SolicitacaoServico]:
    """
    Retorna todas as Solicitações
    que possuem o status informado.
    """

    status_normalizado = (
        _validar_novo_status(
            status
        )
    )

    return [
        solicitacao
        for solicitacao in solicitacoes
        if solicitacao.status
        == status_normalizado
    ]


