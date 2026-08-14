"""
Domínio dos Tipos de Serviço da Plataforma.

Um Tipo de Serviço representa uma categoria de serviço que pode
ser disponibilizada às Empresas e solicitada pelos Clientes.

Exemplos:

- Instalação de Sistema Fotovoltaico;
- Limpeza de Módulos;
- Manutenção Preventiva;
- Diagnóstico de Baixa Geração.

Este módulo controla apenas as regras próprias do Tipo de Serviço.

Não realiza:

- entrada de dados com input();
- exibição de dados com print();
- leitura ou gravação de arquivos;
- interação direta com usuários;
- vinculação do serviço ao catálogo de uma Empresa.
"""

from dataclasses import asdict, dataclass
from enum import Enum

from app.dominio.erros_dominio import (
    DadosObrigatoriosAusentes,
    RegistroDuplicado,
    ValorInvalido,
)


class OrigemTipoServico(str, Enum):
    """
    Define quem originou o Tipo de Serviço.

    PADRAO_PLATAFORMA:
        serviço pertencente ao catálogo mestre.

    PERSONALIZADO_EMPRESA:
        serviço criado especificamente por uma Empresa.
    """

    PADRAO_PLATAFORMA = "PADRAO_PLATAFORMA"
    PERSONALIZADO_EMPRESA = "PERSONALIZADO_EMPRESA"


class FluxoOperacionalServico(str, Enum):
    """
    Define o processo operacional gerado após
    a contratação do serviço.
    """

    ORCAMENTO_FOTOVOLTAICO = (
        "ORCAMENTO_FOTOVOLTAICO"
    )

    ORDEM_SERVICO_POS_VENDA = (
        "ORDEM_SERVICO_POS_VENDA"
    )


class CategoriaTipoServico(str, Enum):
    """
    Categorias estruturadas inicialmente
    reconhecidas pela plataforma.
    """

    INSTALACAO = "INSTALACAO"
    LIMPEZA_E_CONSERVACAO = "LIMPEZA_E_CONSERVACAO"
    INSPECAO_E_DIAGNOSTICO = "INSPECAO_E_DIAGNOSTICO"
    MANUTENCAO_PREVENTIVA = "MANUTENCAO_PREVENTIVA"
    MANUTENCAO_CORRETIVA = "MANUTENCAO_CORRETIVA"
    MODULOS = "MODULOS"
    INVERSORES = "INVERSORES"
    ESTRUTURA = "ESTRUTURA"
    ELETRICA_CC = "ELETRICA_CC"
    ELETRICA_CA = "ELETRICA_CA"
    MONITORAMENTO = "MONITORAMENTO"
    ADEQUACAO = "ADEQUACAO"
    LAUDO_E_VISTORIA_TECNICA = (
        "LAUDO_E_VISTORIA_TECNICA"
    )
    SUPORTE_CONCESSIONARIA = (
        "SUPORTE_CONCESSIONARIA"
    )
    OUTROS = "OUTROS"


@dataclass
class TipoServico:
    """
    Representa um Tipo de Serviço disponível
    no ecossistema da plataforma.

    Um Tipo de Serviço pode ter origem:

    - no catálogo mestre da Plataforma;
    - no catálogo personalizado de uma Empresa.
    """

    codigo: int
    nome: str
    categoria: CategoriaTipoServico
    origem: OrigemTipoServico
    fluxo_operacional: FluxoOperacionalServico
    descricao: str | None = None
    codigo_empresa_criadora: int | None = None
    ativo: bool = True

    def inativar(self):
        """
        Inativa o Tipo de Serviço.

        A entidade não é removida para preservar
        vínculos e históricos existentes.
        """

        self.ativo = False

        return self

    def ativar(self):
        """
        Reativa o Tipo de Serviço.
        """

        self.ativo = True

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

def _validar_texto_obrigatorio(
    valor: str,
    nome_campo: str,
) -> str:
    """
    Valida e normaliza um texto obrigatório.
    """

    if valor is None:
        raise DadosObrigatoriosAusentes(
            f"{nome_campo} é obrigatório."
        )

    if not isinstance(valor, str):
        raise ValorInvalido(
            f"{nome_campo} deve ser um texto."
        )

    valor_normalizado = " ".join(
        valor.strip().split()
    )

    if not valor_normalizado:
        raise DadosObrigatoriosAusentes(
            f"{nome_campo} é obrigatório."
        )

    return valor_normalizado

def _normalizar_texto_opcional(
    valor: str | None,
    nome_campo: str,
) -> str | None:
    """
    Normaliza um texto opcional.

    None ou texto vazio são armazenados como None.
    """

    if valor is None:
        return None

    if not isinstance(valor, str):
        raise ValorInvalido(
            f"{nome_campo} deve ser um texto."
        )

    valor_normalizado = " ".join(
        valor.strip().split()
    )

    return valor_normalizado or None

def _normalizar_categoria(
    categoria,
) -> CategoriaTipoServico:
    """
    Converte o valor informado para
    CategoriaTipoServico.
    """

    if isinstance(
        categoria,
        CategoriaTipoServico,
    ):
        return categoria

    try:
        return CategoriaTipoServico(
            categoria
        )

    except (ValueError, TypeError):
        raise ValorInvalido(
            "Categoria do Tipo de Serviço inválida."
        )

def _normalizar_origem(
    origem,
) -> OrigemTipoServico:
    """
    Converte o valor informado para
    OrigemTipoServico.
    """

    if isinstance(
        origem,
        OrigemTipoServico,
    ):
        return origem

    try:
        return OrigemTipoServico(
            origem
        )

    except (ValueError, TypeError):
        raise ValorInvalido(
            "Origem do Tipo de Serviço inválida."
        )

def _normalizar_fluxo_operacional(
    fluxo_operacional,
) -> FluxoOperacionalServico:
    """
    Converte o valor informado para
    FluxoOperacionalServico.
    """

    if isinstance(
        fluxo_operacional,
        FluxoOperacionalServico,
    ):
        return fluxo_operacional

    try:
        return FluxoOperacionalServico(
            fluxo_operacional
        )

    except (ValueError, TypeError):
        raise ValorInvalido(
            "Fluxo operacional do Serviço inválido."
        )

def criar_tipo_servico(
    codigo: int,
    nome: str,
    categoria,
    origem,
    fluxo_operacional,
    descricao: str | None = None,
    codigo_empresa_criadora: int | None = None,
) -> TipoServico:
    """
    Cria um novo Tipo de Serviço.

    Regras:

    - o código deve ser inteiro positivo;
    - nome é obrigatório;
    - categoria deve ser reconhecida;
    - origem deve ser reconhecida;
    - fluxo operacional deve ser reconhecido;
    - serviços padrão não pertencem a uma Empresa;
    - serviços personalizados exigem Empresa criadora.
    """

    codigo_validado = _validar_codigo(
        codigo,
        "Código do Tipo de Serviço",
    )

    nome_normalizado = (
        _validar_texto_obrigatorio(
            nome,
            "Nome do Tipo de Serviço",
        )
    )

    categoria_normalizada = (
        _normalizar_categoria(
            categoria
        )
    )

    origem_normalizada = _normalizar_origem(
        origem
    )

    fluxo_normalizado = (
        _normalizar_fluxo_operacional(
            fluxo_operacional
        )
    )

    descricao_normalizada = (
        _normalizar_texto_opcional(
            descricao,
            "Descrição do Tipo de Serviço",
        )
    )

    if (
        origem_normalizada
        == OrigemTipoServico.PADRAO_PLATAFORMA
    ):
        if codigo_empresa_criadora is not None:
            raise ValorInvalido(
                "Um Tipo de Serviço padrão da Plataforma "
                "não pode possuir Empresa criadora."
            )

        codigo_empresa_validado = None

    else:
        if codigo_empresa_criadora is None:
            raise DadosObrigatoriosAusentes(
                "A Empresa criadora é obrigatória para "
                "Tipos de Serviço personalizados."
            )

        codigo_empresa_validado = (
            _validar_codigo(
                codigo_empresa_criadora,
                "Código da Empresa criadora",
            )
        )

    return TipoServico(
        codigo=codigo_validado,
        nome=nome_normalizado,
        categoria=categoria_normalizada,
        origem=origem_normalizada,
        fluxo_operacional=fluxo_normalizado,
        descricao=descricao_normalizada,
        codigo_empresa_criadora=(
            codigo_empresa_validado
        ),
        ativo=True,
    )

def converter_tipo_servico_para_dicionario(
    tipo_servico: TipoServico,
) -> dict:
    """
    Converte um Tipo de Serviço para dicionário.

    Enums são convertidos para seus valores textuais
    para facilitar a persistência futura.
    """

    if not isinstance(
        tipo_servico,
        TipoServico,
    ):
        raise TypeError(
            "Tipo de Serviço deve ser uma instância "
            "de TipoServico."
        )

    dados = asdict(
        tipo_servico
    )

    dados["categoria"] = (
        tipo_servico.categoria.value
    )

    dados["origem"] = (
        tipo_servico.origem.value
    )

    dados["fluxo_operacional"] = (
        tipo_servico.fluxo_operacional.value
    )

    return dados

def criar_catalogo_padrao() -> list[TipoServico]:
    """
    Cria o Catálogo Mestre inicial de Tipos
    de Serviço da Plataforma.

    Todos os itens deste catálogo:

    - possuem origem PADRAO_PLATAFORMA;
    - não pertencem a uma Empresa específica;
    - iniciam ativos;
    - possuem código estável;
    - definem o fluxo operacional correspondente.

    A função retorna uma nova lista e novas
    entidades a cada chamada.
    """

    dados_catalogo = [
        {
            "codigo": 1,
            "nome": (
                "Instalação de Sistema Fotovoltaico"
            ),
            "categoria": "INSTALACAO",
            "fluxo_operacional": (
                "ORCAMENTO_FOTOVOLTAICO"
            ),
            "descricao": (
                "Dimensionamento, fornecimento e "
                "instalação de sistema fotovoltaico."
            ),
        },
        {
            "codigo": 2,
            "nome": "Limpeza de Módulos",
            "categoria": (
                "LIMPEZA_E_CONSERVACAO"
            ),
            "fluxo_operacional": (
                "ORDEM_SERVICO_POS_VENDA"
            ),
            "descricao": (
                "Limpeza técnica dos módulos "
                "fotovoltaicos."
            ),
        },
        {
            "codigo": 3,
            "nome": "Manutenção Preventiva",
            "categoria": (
                "MANUTENCAO_PREVENTIVA"
            ),
            "fluxo_operacional": (
                "ORDEM_SERVICO_POS_VENDA"
            ),
            "descricao": (
                "Inspeção preventiva do sistema "
                "fotovoltaico e de seus componentes."
            ),
        },
        {
            "codigo": 4,
            "nome": "Manutenção Corretiva",
            "categoria": (
                "MANUTENCAO_CORRETIVA"
            ),
            "fluxo_operacional": (
                "ORDEM_SERVICO_POS_VENDA"
            ),
            "descricao": (
                "Correção de falhas identificadas "
                "no sistema fotovoltaico."
            ),
        },
        {
            "codigo": 5,
            "nome": "Diagnóstico de Baixa Geração",
            "categoria": (
                "INSPECAO_E_DIAGNOSTICO"
            ),
            "fluxo_operacional": (
                "ORDEM_SERVICO_POS_VENDA"
            ),
            "descricao": (
                "Diagnóstico técnico de sistemas "
                "com geração abaixo do esperado."
            ),
        },
        {
            "codigo": 6,
            "nome": "Inspeção Técnica",
            "categoria": (
                "INSPECAO_E_DIAGNOSTICO"
            ),
            "fluxo_operacional": (
                "ORDEM_SERVICO_POS_VENDA"
            ),
            "descricao": (
                "Inspeção técnica das condições "
                "do sistema fotovoltaico."
            ),
        },
        {
            "codigo": 7,
            "nome": "Termografia",
            "categoria": (
                "INSPECAO_E_DIAGNOSTICO"
            ),
            "fluxo_operacional": (
                "ORDEM_SERVICO_POS_VENDA"
            ),
            "descricao": (
                "Inspeção termográfica de módulos "
                "e componentes elétricos."
            ),
        },
        {
            "codigo": 8,
            "nome": "Manutenção de Inversor",
            "categoria": "INVERSORES",
            "fluxo_operacional": (
                "ORDEM_SERVICO_POS_VENDA"
            ),
            "descricao": (
                "Diagnóstico e manutenção de "
                "inversores fotovoltaicos."
            ),
        },
        {
            "codigo": 9,
            "nome": "Substituição de Inversor",
            "categoria": "INVERSORES",
            "fluxo_operacional": (
                "ORDEM_SERVICO_POS_VENDA"
            ),
            "descricao": (
                "Substituição de inversor do "
                "sistema fotovoltaico."
            ),
        },
        {
            "codigo": 10,
            "nome": "Substituição de Módulo",
            "categoria": "MODULOS",
            "fluxo_operacional": (
                "ORDEM_SERVICO_POS_VENDA"
            ),
            "descricao": (
                "Substituição de módulo "
                "fotovoltaico."
            ),
        },
        {
            "codigo": 11,
            "nome": "Reparo Elétrico CC",
            "categoria": "ELETRICA_CC",
            "fluxo_operacional": (
                "ORDEM_SERVICO_POS_VENDA"
            ),
            "descricao": (
                "Manutenção ou reparo no circuito "
                "elétrico em corrente contínua."
            ),
        },
        {
            "codigo": 12,
            "nome": "Reparo Elétrico CA",
            "categoria": "ELETRICA_CA",
            "fluxo_operacional": (
                "ORDEM_SERVICO_POS_VENDA"
            ),
            "descricao": (
                "Manutenção ou reparo no circuito "
                "elétrico em corrente alternada."
            ),
        },
        {
            "codigo": 13,
            "nome": "Monitoramento",
            "categoria": "MONITORAMENTO",
            "fluxo_operacional": (
                "ORDEM_SERVICO_POS_VENDA"
            ),
            "descricao": (
                "Configuração, acompanhamento ou "
                "suporte ao monitoramento do sistema."
            ),
        },
        {
            "codigo": 14,
            "nome": "Adequação do Sistema",
            "categoria": "ADEQUACAO",
            "fluxo_operacional": (
                "ORDEM_SERVICO_POS_VENDA"
            ),
            "descricao": (
                "Adequação técnica de sistema "
                "fotovoltaico existente."
            ),
        },
        {
            "codigo": 15,
            "nome": "Laudo e Vistoria Técnica",
            "categoria": (
                "LAUDO_E_VISTORIA_TECNICA"
            ),
            "fluxo_operacional": (
                "ORDEM_SERVICO_POS_VENDA"
            ),
            "descricao": (
                "Vistoria técnica e elaboração "
                "de documentação ou laudo técnico."
            ),
        },
        {
            "codigo": 16,
            "nome": "Suporte à Concessionária",
            "categoria": (
                "SUPORTE_CONCESSIONARIA"
            ),
            "fluxo_operacional": (
                "ORDEM_SERVICO_POS_VENDA"
            ),
            "descricao": (
                "Suporte técnico ou administrativo "
                "em demandas junto à concessionária."
            ),
        },
    ]

    return [
        criar_tipo_servico(
            codigo=dados["codigo"],
            nome=dados["nome"],
            categoria=dados["categoria"],
            origem="PADRAO_PLATAFORMA",
            fluxo_operacional=(
                dados["fluxo_operacional"]
            ),
            descricao=dados["descricao"],
        )
        for dados in dados_catalogo
    ]

def buscar_tipo_servico_por_codigo(
    tipos_servico: list[TipoServico],
    codigo: int,
) -> TipoServico | None:
    """
    Busca um Tipo de Serviço pelo código.

    Retorna:

    - o Tipo de Serviço encontrado;
    - None quando o código não existir.
    """

    codigo_validado = _validar_codigo(
        codigo,
        "Código do Tipo de Serviço",
    )

    for tipo_servico in tipos_servico:
        if tipo_servico.codigo == codigo_validado:
            return tipo_servico

    return None

def codigo_tipo_servico_existe(
    tipos_servico: list[TipoServico],
    codigo: int,
) -> bool:
    """
    Informa se determinado código já existe.
    """

    return (
        buscar_tipo_servico_por_codigo(
            tipos_servico,
            codigo,
        )
        is not None
    )

def buscar_tipos_servico_por_nome(
    tipos_servico: list[TipoServico],
    nome: str,
) -> list[TipoServico]:
    """
    Busca Tipos de Serviço por nome.

    A busca:

    - ignora letras maiúsculas e minúsculas;
    - ignora espaços externos;
    - aceita parte do nome;
    - preserva a ordem original da coleção.
    """

    nome_normalizado = (
        _validar_texto_obrigatorio(
            nome,
            "Nome para busca",
        )
    ).casefold()

    return [
        tipo_servico
        for tipo_servico in tipos_servico
        if nome_normalizado
        in tipo_servico.nome.casefold()
    ]

def tipo_servico_esta_ativo(
    tipo_servico: TipoServico,
) -> bool:
    """
    Informa se o Tipo de Serviço está ativo.
    """

    if not isinstance(
        tipo_servico,
        TipoServico,
    ):
        raise TypeError(
            "Tipo de Serviço deve ser uma instância "
            "de TipoServico."
        )

    return tipo_servico.ativo

def validar_duplicidade_tipo_servico(
    tipos_servico: list[TipoServico],
    nome: str,
    origem,
    codigo_empresa_criadora: int | None = None,
) -> None:
    """
    Impede cadastro duplicado de Tipo de Serviço.

    Regras:

    PADRAO_PLATAFORMA:
        não pode existir outro serviço padrão
        com o mesmo nome.

    PERSONALIZADO_EMPRESA:
        a mesma Empresa não pode possuir dois
        serviços personalizados com o mesmo nome.

        Empresas diferentes podem utilizar
        o mesmo nome.

    A comparação ignora diferenças entre
    maiúsculas/minúsculas e espaços excedentes.
    """

    nome_normalizado = (
        _validar_texto_obrigatorio(
            nome,
            "Nome do Tipo de Serviço",
        )
    ).casefold()

    origem_normalizada = _normalizar_origem(
        origem
    )

    if (
        origem_normalizada
        == OrigemTipoServico.PERSONALIZADO_EMPRESA
    ):
        if codigo_empresa_criadora is None:
            raise DadosObrigatoriosAusentes(
                "A Empresa criadora é obrigatória para "
                "validar um Tipo de Serviço personalizado."
            )

        codigo_empresa_validado = (
            _validar_codigo(
                codigo_empresa_criadora,
                "Código da Empresa criadora",
            )
        )

    else:
        codigo_empresa_validado = None

    for tipo_servico in tipos_servico:
        mesmo_nome = (
            tipo_servico.nome.casefold()
            == nome_normalizado
        )

        if not mesmo_nome:
            continue

        if (
            origem_normalizada
            == OrigemTipoServico.PADRAO_PLATAFORMA
            and tipo_servico.origem
            == OrigemTipoServico.PADRAO_PLATAFORMA
        ):
            raise RegistroDuplicado(
                "Já existe um Tipo de Serviço padrão "
                "com este nome."
            )

        if (
            origem_normalizada
            == OrigemTipoServico.PERSONALIZADO_EMPRESA
            and tipo_servico.origem
            == OrigemTipoServico.PERSONALIZADO_EMPRESA
            and tipo_servico.codigo_empresa_criadora
            == codigo_empresa_validado
        ):
            raise RegistroDuplicado(
                "Esta Empresa já possui um Tipo de "
                "Serviço personalizado com este nome."
            )

