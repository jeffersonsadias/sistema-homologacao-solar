"""
Domínio dos Serviços oferecidos pelas Empresas.

ServicoOfertadoEmpresa representa o vínculo entre:

- uma Empresa cadastrada;
- um Tipo de Serviço existente.

Este módulo controla apenas as regras próprias
da oferta de serviço pela Empresa.

Não realiza:

- entrada de dados com input();
- exibição de dados com print();
- leitura ou gravação de arquivos;
- cálculo geográfico;
- criação de propostas;
- contratação de serviços.
"""

from dataclasses import asdict, dataclass
from enum import Enum

from app.dominio.empresas import (
    empresa_esta_ativa,
)

from app.dominio.erros_dominio import (
    DadosObrigatoriosAusentes,
    RegistroDuplicado,
    ValorInvalido,
)

from app.dominio.areas_atendimento import (
    AreaAtendimento,
    ModalidadeAreaAtendimento,
)

from app.dominio.tipos_servico import (
    OrigemTipoServico,
    TipoServico,
    tipo_servico_esta_ativo,
)

class ModeloPrecificacao(str, Enum):
    """
    Define como a Empresa apresenta
    comercialmente o Serviço.
    """

    ORCAMENTO = "ORCAMENTO"
    PRECO_FIXO = "PRECO_FIXO"
    A_PARTIR_DE = "A_PARTIR_DE"
    SOB_CONSULTA = "SOB_CONSULTA"

@dataclass
class ServicoOfertadoEmpresa:
    """
    Representa um Tipo de Serviço que determinada
    Empresa decidiu oferecer.

    A entidade mantém:

    - código do vínculo;
    - código da Empresa;
    - código do Tipo de Serviço;
    - modelo de precificação;
    - valor, quando aplicável;
    - permissão para solicitação direta;
    - participação no marketplace;
    - Área de Atendimento;
    - situação ativa/inativa.

    O vínculo Empresa + Tipo de Serviço deve ser
    único dentro do catálogo da Empresa.

    Uma oferta inativa permanece existente para
    preservação do histórico e deve ser reativada,
    não recriada.
    """

    codigo: int
    codigo_empresa: int
    codigo_tipo_servico: int
    modelo_precificacao: ModeloPrecificacao
    valor: float | None = None
    aceita_solicitacao_direta: bool = True
    participa_marketplace: bool = True
    area_atendimento: AreaAtendimento | None = None
    ativo: bool = True

    def inativar(self):
        """
        Inativa a oferta sem apagar seu histórico.
        """

        self.ativo = False

        return self

def _validar_codigo(
    codigo: int,
    nome_campo: str,
) -> int:
    """
    Valida um código inteiro positivo.
    """

    if (
        isinstance(codigo, bool)
        or not isinstance(codigo, int)
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

def _normalizar_modelo_precificacao(
    modelo_precificacao,
) -> ModeloPrecificacao:
    """
    Converte o valor informado para
    ModeloPrecificacao.
    """

    if isinstance(
        modelo_precificacao,
        ModeloPrecificacao,
    ):
        return modelo_precificacao

    try:
        return ModeloPrecificacao(
            modelo_precificacao
        )

    except (ValueError, TypeError):
        raise ValorInvalido(
            "Modelo de precificação inválido."
        )

def _validar_valor(
    modelo_precificacao: ModeloPrecificacao,
    valor,
) -> float | None:
    """
    Valida o valor conforme o modelo
    de precificação.

    Regras:

    PRECO_FIXO e A_PARTIR_DE:
        exigem valor numérico positivo.

    ORCAMENTO e SOB_CONSULTA:
        não utilizam valor nesta etapa.
    """

    modelos_com_valor = (
        ModeloPrecificacao.PRECO_FIXO,
        ModeloPrecificacao.A_PARTIR_DE,
    )

    modelos_sem_valor = (
        ModeloPrecificacao.ORCAMENTO,
        ModeloPrecificacao.SOB_CONSULTA,
    )

    if modelo_precificacao in modelos_com_valor:
        if valor is None:
            raise DadosObrigatoriosAusentes(
                "O valor é obrigatório para este "
                "modelo de precificação."
            )

        if (
            isinstance(valor, bool)
            or not isinstance(
                valor,
                (int, float),
            )
        ):
            raise ValorInvalido(
                "O valor do Serviço deve ser numérico."
            )

        valor_normalizado = float(
            valor
        )

        if valor_normalizado <= 0:
            raise ValorInvalido(
                "O valor do Serviço deve ser "
                "maior que zero."
            )

        return valor_normalizado

    if modelo_precificacao in modelos_sem_valor:
        if valor is not None:
            raise ValorInvalido(
                "Este modelo de precificação "
                "não deve possuir valor."
            )

        return None

    raise ValorInvalido(
        "Modelo de precificação inválido."
    )

def _validar_precificacao_para_tipo_servico(
    tipo_servico: TipoServico,
    modelo_precificacao: ModeloPrecificacao,
) -> None:
    """
    Valida regras de precificação específicas
    do Tipo de Serviço.

    Instalação de Sistema Fotovoltaico utiliza
    obrigatoriamente ORCAMENTO nesta fase.
    """

    if (
        tipo_servico.fluxo_operacional.value
        == "ORCAMENTO_FOTOVOLTAICO"
        and modelo_precificacao
        != ModeloPrecificacao.ORCAMENTO
    ):
        raise ValorInvalido(
            "Serviços com fluxo de Orçamento "
            "Fotovoltaico devem utilizar o modelo "
            "de precificação ORCAMENTO."
        )

def _validar_permissao_comercial(
    valor,
    nome_campo: str,
) -> bool:
    """
    Valida uma configuração booleana
    da oferta comercial da Empresa.
    """

    if not isinstance(
        valor,
        bool,
    ):
        raise ValorInvalido(
            f"{nome_campo} deve ser "
            "um valor booleano."
        )

    return valor

def _validar_area_atendimento(
    area_atendimento,
) -> AreaAtendimento | None:
    """
    Valida a Área de Atendimento vinculada
    à oferta de serviço.

    Nesta etapa, a área ainda é opcional
    para preservar compatibilidade com
    ofertas já existentes.
    """

    if area_atendimento is None:
        return None

    if not isinstance(
        area_atendimento,
        AreaAtendimento,
    ):
        raise TypeError(
            "Área de atendimento deve ser uma "
            "instância de AreaAtendimento."
        )

    return area_atendimento

def _validar_empresa(
    empresa: dict,
) -> dict:
    """
    Valida a Empresa utilizada na oferta.

    Somente Empresas ativas podem criar
    novas ofertas de serviço.
    """

    if not isinstance(
        empresa,
        dict,
    ):
        raise TypeError(
            "A Empresa deve ser representada "
            "por um dicionário."
        )

    if "codigo" not in empresa:
        raise DadosObrigatoriosAusentes(
            "A Empresa precisa possuir código."
        )

    codigo_empresa = _validar_codigo(
        empresa["codigo"],
        "Código da Empresa",
    )

    if not empresa_esta_ativa(
        empresa
    ):
        raise ValorInvalido(
            "Somente Empresas ativas podem "
            "oferecer novos serviços."
        )

    empresa["codigo"] = codigo_empresa

    return empresa

def _validar_tipo_servico(
    tipo_servico: TipoServico,
    codigo_empresa: int,
) -> TipoServico:
    """
    Valida o Tipo de Serviço utilizado
    pela Empresa.

    Regras:

    - deve ser TipoServico;
    - precisa estar ativo;
    - serviço personalizado só pode ser
      ofertado pela Empresa que o criou.
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
            "Não é possível oferecer um "
            "Tipo de Serviço inativo."
        )

    if (
        tipo_servico.origem
        == OrigemTipoServico.PERSONALIZADO_EMPRESA
        and tipo_servico.codigo_empresa_criadora
        != codigo_empresa
    ):
        raise ValorInvalido(
            "Um Tipo de Serviço personalizado "
            "só pode ser oferecido pela Empresa "
            "que o criou."
        )

    return tipo_servico

def criar_servico_ofertado_empresa(
    codigo: int,
    empresa: dict,
    tipo_servico: TipoServico,
    modelo_precificacao,
    valor=None,
    aceita_solicitacao_direta=True,
    participa_marketplace=True,
    area_atendimento=None,
) -> ServicoOfertadoEmpresa:
    """
    Cria o vínculo entre uma Empresa
    e um Tipo de Serviço.

    Regras:

    - código da oferta deve ser inteiro positivo;
    - Empresa precisa estar ativa;
    - Tipo de Serviço precisa estar ativo;
    - serviço personalizado pertence somente
      à Empresa que o criou;
    - nova oferta inicia ativa.
    """

    codigo_validado = _validar_codigo(
        codigo,
        "Código do Serviço oferecido",
    )

    empresa_validada = _validar_empresa(
        empresa
    )

    codigo_empresa = empresa_validada[
        "codigo"
    ]

    tipo_servico_validado = (
        _validar_tipo_servico(
            tipo_servico,
            codigo_empresa,
        )
    )

    modelo_precificacao_normalizado = (
        _normalizar_modelo_precificacao(
            modelo_precificacao
        )
    )

    _validar_precificacao_para_tipo_servico(
        tipo_servico_validado,
        modelo_precificacao_normalizado,
    )

    valor_validado = _validar_valor(
        modelo_precificacao_normalizado,
        valor,
    )

    aceita_solicitacao_direta_validado = (
        _validar_permissao_comercial(
            aceita_solicitacao_direta,
            "Aceita solicitação direta",
        )
    )

    participa_marketplace_validado = (
        _validar_permissao_comercial(
            participa_marketplace,
            "Participa do marketplace",
        )
    )

    area_atendimento_validada = (
        _validar_area_atendimento(
            area_atendimento
        )
    )

    return ServicoOfertadoEmpresa(
        codigo=codigo_validado,
        codigo_empresa=codigo_empresa,
        codigo_tipo_servico=(
            tipo_servico_validado.codigo
        ),
        modelo_precificacao=(
            modelo_precificacao_normalizado
        ),
        valor=valor_validado,
        aceita_solicitacao_direta=(
            aceita_solicitacao_direta_validado
        ),
        participa_marketplace=(
            participa_marketplace_validado
        ),
        area_atendimento=(
            area_atendimento_validada
        ),
        ativo=True,
    )

def reativar_servico_ofertado_empresa(
    servico_ofertado: ServicoOfertadoEmpresa,
    empresa: dict,
    tipo_servico: TipoServico,
) -> ServicoOfertadoEmpresa:
    """
    Reativa uma oferta de serviço após validar
    suas dependências atuais.

    Regras:

    - deve receber uma oferta válida;
    - a Empresa deve ser a mesma vinculada à oferta;
    - a Empresa precisa continuar ativa;
    - o Tipo de Serviço deve ser o mesmo vinculado;
    - o Tipo de Serviço precisa continuar ativo;
    - serviços personalizados devem continuar
      pertencendo à Empresa correta.
    """

    if not isinstance(
        servico_ofertado,
        ServicoOfertadoEmpresa,
    ):
        raise TypeError(
            "Serviço oferecido deve ser uma instância "
            "de ServicoOfertadoEmpresa."
        )

    empresa_validada = _validar_empresa(
        empresa
    )

    if (
        empresa_validada["codigo"]
        != servico_ofertado.codigo_empresa
    ):
        raise ValorInvalido(
            "A Empresa informada não corresponde "
            "à Empresa vinculada ao Serviço oferecido."
        )

    tipo_servico_validado = (
        _validar_tipo_servico(
            tipo_servico,
            servico_ofertado.codigo_empresa,
        )
    )

    if (
        tipo_servico_validado.codigo
        != servico_ofertado.codigo_tipo_servico
    ):
        raise ValorInvalido(
            "O Tipo de Serviço informado não corresponde "
            "ao Tipo de Serviço vinculado à oferta."
        )

    servico_ofertado.ativo = True

    return servico_ofertado

def converter_servico_ofertado_para_dicionario(
    servico_ofertado: ServicoOfertadoEmpresa,
) -> dict:
    """
    Converte a entidade para dicionário,
    preparando-a para persistência futura.
    """

    if not isinstance(
        servico_ofertado,
        ServicoOfertadoEmpresa,
    ):
        raise TypeError(
            "Serviço oferecido deve ser uma instância "
            "de ServicoOfertadoEmpresa."
        )

    dados = asdict(
        servico_ofertado
    )

    dados["modelo_precificacao"] = (
        servico_ofertado
        .modelo_precificacao
        .value
    )

    if servico_ofertado.area_atendimento is not None:
        dados["area_atendimento"]["modalidade"] = (
            servico_ofertado
            .area_atendimento
            .modalidade
            .value
        )

    return dados

def servico_elegivel_marketplace(
    servico_ofertado: ServicoOfertadoEmpresa,
) -> bool:
    """
    Informa se a oferta está habilitada para
    participar operacionalmente do marketplace.

    Para estar elegível, a oferta precisa:

    - estar ativa;
    - participar do marketplace;
    - possuir Área de Atendimento configurada.
    """

    if not isinstance(
        servico_ofertado,
        ServicoOfertadoEmpresa,
    ):
        raise TypeError(
            "Serviço oferecido deve ser uma instância "
            "de ServicoOfertadoEmpresa."
        )

    return (
        servico_ofertado.ativo
        and servico_ofertado.participa_marketplace
        and servico_ofertado.area_atendimento
        is not None
    )

def buscar_servico_ofertado_por_codigo(
    servicos_ofertados: list,
    codigo: int,
) -> ServicoOfertadoEmpresa | None:
    """
    Busca uma oferta pelo seu código.

    Retorna a entidade encontrada ou None
    quando não existir oferta com o código
    informado.
    """

    codigo_validado = _validar_codigo(
        codigo,
        "Código do Serviço oferecido",
    )

    for servico in servicos_ofertados:
        if not isinstance(
            servico,
            ServicoOfertadoEmpresa,
        ):
            raise TypeError(
                "A lista deve conter somente "
                "ServicosOfertadosEmpresa."
            )

        if servico.codigo == codigo_validado:
            return servico

    return None

def listar_servicos_ofertados_por_empresa(
    servicos_ofertados: list,
    codigo_empresa: int,
) -> list[ServicoOfertadoEmpresa]:
    """
    Retorna todas as ofertas vinculadas
    à Empresa informada.
    """

    codigo_empresa_validado = _validar_codigo(
        codigo_empresa,
        "Código da Empresa",
    )

    resultado = []

    for servico in servicos_ofertados:
        if not isinstance(
            servico,
            ServicoOfertadoEmpresa,
        ):
            raise TypeError(
                "A lista deve conter somente "
                "ServicosOfertadosEmpresa."
            )

        if (
            servico.codigo_empresa
            == codigo_empresa_validado
        ):
            resultado.append(
                servico
            )

    return resultado

def listar_servicos_ofertados_ativos(
    servicos_ofertados: list,
) -> list[ServicoOfertadoEmpresa]:
    """
    Retorna somente as ofertas atualmente ativas.
    """

    resultado = []

    for servico in servicos_ofertados:
        if not isinstance(
            servico,
            ServicoOfertadoEmpresa,
        ):
            raise TypeError(
                "A lista deve conter somente "
                "ServicosOfertadosEmpresa."
            )

        if servico.ativo:
            resultado.append(
                servico
            )

    return resultado

def listar_servicos_ofertados_por_tipo_servico(
    servicos_ofertados: list,
    codigo_tipo_servico: int,
) -> list[ServicoOfertadoEmpresa]:
    """
    Retorna todas as ofertas vinculadas
    ao Tipo de Serviço informado.
    """

    codigo_tipo_validado = _validar_codigo(
        codigo_tipo_servico,
        "Código do Tipo de Serviço",
    )

    resultado = []

    for servico in servicos_ofertados:
        if not isinstance(
            servico,
            ServicoOfertadoEmpresa,
        ):
            raise TypeError(
                "A lista deve conter somente "
                "ServicosOfertadosEmpresa."
            )

        if (
            servico.codigo_tipo_servico
            == codigo_tipo_validado
        ):
            resultado.append(
                servico
            )

    return resultado

def servico_ofertado_duplicado(
    servicos_ofertados: list,
    codigo_empresa: int,
    codigo_tipo_servico: int,
) -> bool:
    """
    Verifica se já existe uma oferta para a combinação
    Empresa + Tipo de Serviço.

    A situação ativa ou inativa da oferta não interfere
    nesta verificação.

    Uma oferta inativa continua representando o vínculo
    e deve ser reativada, não recriada.
    """

    codigo_empresa_validado = _validar_codigo(
        codigo_empresa,
        "Código da Empresa",
    )

    codigo_tipo_validado = _validar_codigo(
        codigo_tipo_servico,
        "Código do Tipo de Serviço",
    )

    for servico in servicos_ofertados:
        if not isinstance(
            servico,
            ServicoOfertadoEmpresa,
        ):
            raise TypeError(
                "A lista deve conter somente "
                "ServicosOfertadosEmpresa."
            )

        if (
            servico.codigo_empresa
            == codigo_empresa_validado
            and servico.codigo_tipo_servico
            == codigo_tipo_validado
        ):
            return True

    return False

def validar_nova_oferta_servico(
    servicos_ofertados: list,
    empresa: dict,
    tipo_servico: TipoServico,
) -> None:
    """
    Valida se uma nova oferta pode ser cadastrada.

    A combinação Empresa + Tipo de Serviço deve ser única.

    Se o vínculo já existir, mesmo inativo, uma nova oferta
    não deve ser criada. O fluxo correto será a reativação
    da oferta existente.
    """

    empresa_validada = _validar_empresa(
        empresa
    )

    codigo_empresa = empresa_validada[
        "codigo"
    ]

    tipo_servico_validado = (
        _validar_tipo_servico(
            tipo_servico,
            codigo_empresa,
        )
    )

    if servico_ofertado_duplicado(
        servicos_ofertados,
        codigo_empresa,
        tipo_servico_validado.codigo,
    ):
        raise RegistroDuplicado(
            "A Empresa já possui uma oferta cadastrada "
            "para este Tipo de Serviço."
        )


