"""
Domínio das Unidades Consumidoras.

Este módulo contém as entidades, enumerações,
validações e regras de negócio relacionadas
ao Cadastro Mestre de Unidades Consumidoras.

Uma Unidade Consumidora existe independentemente
de qualquer Projeto.

O papel de uma Unidade Consumidora como Geradora
ou Beneficiária será definido posteriormente
pelo vínculo entre a Unidade e o Projeto.
"""

from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum


class TipoTitular(Enum):
    """
    Tipos possíveis de titular da conta de energia.
    """

    PESSOA_FISICA = "PESSOA_FISICA"
    PESSOA_JURIDICA = "PESSOA_JURIDICA"


class TipoLigacao(Enum):
    """
    Tipos de ligação elétrica da Unidade Consumidora.
    """

    MONOFASICA = "MONOFASICA"
    BIFASICA = "BIFASICA"
    TRIFASICA = "TRIFASICA"


class SituacaoUnidadeConsumidora(Enum):
    """
    Situações possíveis da Unidade Consumidora
    dentro da plataforma.
    """

    ATIVA = "ATIVA"
    INATIVA = "INATIVA"


class TipoAlteracaoUnidade(Enum):
    """
    Tipos de alterações que podem ser registradas
    no histórico da Unidade Consumidora.
    """

    TITULARIDADE = "TITULARIDADE"
    CARGA_INSTALADA = "CARGA_INSTALADA"
    CODIGO_CLIENTE = "CODIGO_CLIENTE"
    ENDERECO = "ENDERECO"
    TIPO_LIGACAO = "TIPO_LIGACAO"
    SITUACAO = "SITUACAO"


def normalizar_documento(documento):
    """
    Remove todos os caracteres não numéricos
    de um CPF ou CNPJ.

    Exemplos:

        123.456.789-00
        torna-se
        12345678900

        12.345.678/0001-90
        torna-se
        12345678000190
    """

    return "".join(
        caractere
        for caractere in str(documento)
        if caractere.isdigit()
    )


def validar_texto_obrigatorio(valor, nome_campo):
    """
    Valida um campo textual obrigatório.

    Retorna o texto sem espaços nas extremidades.
    """

    texto = str(valor).strip()

    if not texto:
        raise ValueError(
            f"O campo '{nome_campo}' é obrigatório."
        )

    return texto


def validar_codigo_positivo(codigo, nome_campo):
    """
    Valida se um código é um número inteiro positivo.
    """

    if not isinstance(codigo, int):
        raise TypeError(
            f"O campo '{nome_campo}' deve ser inteiro."
        )

    if codigo <= 0:
        raise ValueError(
            f"O campo '{nome_campo}' deve ser positivo."
        )

    return codigo


def validar_valor_nao_negativo(valor, nome_campo):
    """
    Valida se um valor numérico é maior
    ou igual a zero.
    """

    try:
        valor_convertido = float(valor)

    except (TypeError, ValueError) as erro:
        raise TypeError(
            f"O campo '{nome_campo}' deve ser numérico."
        ) from erro

    if valor_convertido < 0:
        raise ValueError(
            f"O campo '{nome_campo}' não pode ser negativo."
        )

    return valor_convertido


@dataclass
class TitularConta:
    """
    Representa o titular atual da conta de energia.

    O titular pode ser uma pessoa física
    ou uma pessoa jurídica.
    """

    nome: str
    documento: str
    tipo: TipoTitular

    def __post_init__(self):
        """
        Executa as validações após a criação
        do objeto.
        """

        self.nome = validar_texto_obrigatorio(
            self.nome,
            "nome do titular",
        )

        self.documento = normalizar_documento(
            self.documento
        )

        if not isinstance(self.tipo, TipoTitular):
            raise TypeError(
                "O tipo do titular deve pertencer "
                "ao enum TipoTitular."
            )

        self._validar_documento()

    def _validar_documento(self):
        """
        Valida a quantidade de dígitos do documento
        conforme o tipo do titular.

        Nesta etapa, validamos apenas o formato básico.

        A validação matemática completa de CPF e CNPJ
        poderá ser acrescentada futuramente.
        """

        if self.tipo == TipoTitular.PESSOA_FISICA:
            if len(self.documento) != 11:
                raise ValueError(
                    "O CPF deve possuir 11 dígitos."
                )

        elif self.tipo == TipoTitular.PESSOA_JURIDICA:
            if len(self.documento) != 14:
                raise ValueError(
                    "O CNPJ deve possuir 14 dígitos."
                )


@dataclass
class EnderecoUnidade:
    """
    Representa o endereço da Unidade Consumidora.
    """

    logradouro: str
    numero: str
    bairro: str
    cidade: str
    estado: str
    cep: str
    complemento: str = ""

    def __post_init__(self):
        """
        Valida e normaliza os dados do endereço.
        """

        self.logradouro = validar_texto_obrigatorio(
            self.logradouro,
            "logradouro",
        )

        self.numero = validar_texto_obrigatorio(
            self.numero,
            "número",
        )

        self.bairro = validar_texto_obrigatorio(
            self.bairro,
            "bairro",
        )

        self.cidade = validar_texto_obrigatorio(
            self.cidade,
            "cidade",
        )

        self.estado = validar_texto_obrigatorio(
            self.estado,
            "estado",
        ).upper()

        self.cep = normalizar_documento(
            self.cep
        )

        self.complemento = str(
            self.complemento
        ).strip()

        if len(self.estado) != 2:
            raise ValueError(
                "O estado deve ser informado pela sigla "
                "com dois caracteres."
            )

        if len(self.cep) != 8:
            raise ValueError(
                "O CEP deve possuir 8 dígitos."
            )


@dataclass
class RegistroAlteracaoUnidade:
    """
    Representa uma alteração realizada
    em uma Unidade Consumidora.

    O histórico preserva os valores anteriores
    e novos para comparação e comprovação.
    """

    tipo: TipoAlteracaoUnidade
    valor_anterior: str
    valor_novo: str
    data_alteracao: datetime
    motivo: str = ""

    def __post_init__(self):
        """
        Valida os dados do registro histórico.
        """

        if not isinstance(
            self.tipo,
            TipoAlteracaoUnidade,
        ):
            raise TypeError(
                "O tipo da alteração deve pertencer "
                "ao enum TipoAlteracaoUnidade."
            )

        if not isinstance(
            self.data_alteracao,
            datetime,
        ):
            raise TypeError(
                "A data da alteração deve ser "
                "um objeto datetime."
            )

        self.valor_anterior = str(
            self.valor_anterior
        )

        self.valor_novo = str(
            self.valor_novo
        )

        self.motivo = str(
            self.motivo
        ).strip()


@dataclass
class UnidadeConsumidora:
    """
    Entidade principal do Cadastro Mestre
    de Unidades Consumidoras.

    A Unidade Consumidora pertence a uma Concessionária,
    possui um titular atual e pode ter seu histórico
    de alterações preservado.
    """

    codigo: int
    numero_uc: str
    codigo_cliente: str
    codigo_concessionaria: int
    titular: TitularConta
    endereco: EnderecoUnidade
    tipo_ligacao: TipoLigacao
    carga_instalada_kw: float = 0.0
    situacao: SituacaoUnidadeConsumidora = (
        SituacaoUnidadeConsumidora.ATIVA
    )
    data_cadastro: datetime = field(
        default_factory=datetime.now
    )
    data_atualizacao: datetime = field(
        default_factory=datetime.now
    )
    historico_alteracoes: list = field(
        default_factory=list
    )

    def __post_init__(self):
        """
        Valida e normaliza os dados da entidade.
        """

        self.codigo = validar_codigo_positivo(
            self.codigo,
            "código da Unidade Consumidora",
        )

        self.numero_uc = validar_texto_obrigatorio(
            self.numero_uc,
            "número da Unidade Consumidora",
        )

        self.codigo_cliente = (
            validar_texto_obrigatorio(
                self.codigo_cliente,
                "código do cliente",
            )
        )

        self.codigo_concessionaria = (
            validar_codigo_positivo(
                self.codigo_concessionaria,
                "código da Concessionária",
            )
        )

        if not isinstance(
            self.titular,
            TitularConta,
        ):
            raise TypeError(
                "O titular deve ser um objeto "
                "TitularConta."
            )

        if not isinstance(
            self.endereco,
            EnderecoUnidade,
        ):
            raise TypeError(
                "O endereço deve ser um objeto "
                "EnderecoUnidade."
            )

        if not isinstance(
            self.tipo_ligacao,
            TipoLigacao,
        ):
            raise TypeError(
                "O tipo de ligação deve pertencer "
                "ao enum TipoLigacao."
            )

        if not isinstance(
            self.situacao,
            SituacaoUnidadeConsumidora,
        ):
            raise TypeError(
                "A situação deve pertencer ao enum "
                "SituacaoUnidadeConsumidora."
            )

        self.carga_instalada_kw = (
            validar_valor_nao_negativo(
                self.carga_instalada_kw,
                "carga instalada",
            )
        )

        if not isinstance(
            self.data_cadastro,
            datetime,
        ):
            raise TypeError(
                "A data de cadastro deve ser "
                "um objeto datetime."
            )

        if not isinstance(
            self.data_atualizacao,
            datetime,
        ):
            raise TypeError(
                "A data de atualização deve ser "
                "um objeto datetime."
            )

        if not isinstance(
            self.historico_alteracoes,
            list,
        ):
            raise TypeError(
                "O histórico de alterações "
                "deve ser uma lista."
            )

        for registro in self.historico_alteracoes:
            if not isinstance(
                registro,
                RegistroAlteracaoUnidade,
            ):
                raise TypeError(
                    "Todos os itens do histórico devem "
                    "ser objetos RegistroAlteracaoUnidade."
                )

    def registrar_alteracao(
        self,
        tipo,
        valor_anterior,
        valor_novo,
        motivo="",
    ):
        """
        Adiciona uma alteração ao histórico
        da Unidade Consumidora.
        """

        registro = RegistroAlteracaoUnidade(
            tipo=tipo,
            valor_anterior=str(valor_anterior),
            valor_novo=str(valor_novo),
            data_alteracao=datetime.now(),
            motivo=motivo,
        )

        self.historico_alteracoes.append(
            registro
        )

        self.data_atualizacao = datetime.now()

        return registro

    def alterar_titular(
        self,
        novo_titular,
        motivo="",
    ):
        """
        Altera o titular da conta e registra
        a mudança no histórico.
        """

        if not isinstance(
            novo_titular,
            TitularConta,
        ):
            raise TypeError(
                "O novo titular deve ser um objeto "
                "TitularConta."
            )

        titular_anterior = (
            f"{self.titular.nome} - "
            f"{self.titular.documento}"
        )

        titular_novo = (
            f"{novo_titular.nome} - "
            f"{novo_titular.documento}"
        )

        if (
            self.titular.documento
            == novo_titular.documento
            and self.titular.nome
            == novo_titular.nome
            and self.titular.tipo
            == novo_titular.tipo
        ):
            return False

        self.titular = novo_titular

        self.registrar_alteracao(
            tipo=TipoAlteracaoUnidade.TITULARIDADE,
            valor_anterior=titular_anterior,
            valor_novo=titular_novo,
            motivo=motivo,
        )

        return True

    def alterar_carga_instalada(
        self,
        nova_carga_kw,
        motivo="",
    ):
        """
        Altera a carga instalada da Unidade Consumidora
        e registra a mudança no histórico.
        """

        nova_carga = validar_valor_nao_negativo(
            nova_carga_kw,
            "nova carga instalada",
        )

        if nova_carga == self.carga_instalada_kw:
            return False

        carga_anterior = self.carga_instalada_kw

        self.carga_instalada_kw = nova_carga

        self.registrar_alteracao(
            tipo=(
                TipoAlteracaoUnidade
                .CARGA_INSTALADA
            ),
            valor_anterior=carga_anterior,
            valor_novo=nova_carga,
            motivo=motivo,
        )

        return True

    def alterar_codigo_cliente(
        self,
        novo_codigo_cliente,
        motivo="",
    ):
        """
        Altera o código do cliente registrado
        pela Concessionária.
        """

        novo_codigo = validar_texto_obrigatorio(
            novo_codigo_cliente,
            "novo código do cliente",
        )

        if novo_codigo == self.codigo_cliente:
            return False

        codigo_anterior = self.codigo_cliente

        self.codigo_cliente = novo_codigo

        self.registrar_alteracao(
            tipo=(
                TipoAlteracaoUnidade
                .CODIGO_CLIENTE
            ),
            valor_anterior=codigo_anterior,
            valor_novo=novo_codigo,
            motivo=motivo,
        )

        return True

    def alterar_endereco(
        self,
        novo_endereco,
        motivo="",
    ):
        """
        Altera o endereço da Unidade Consumidora.
        """

        if not isinstance(
            novo_endereco,
            EnderecoUnidade,
        ):
            raise TypeError(
                "O novo endereço deve ser um objeto "
                "EnderecoUnidade."
            )

        endereco_anterior = (
            f"{self.endereco.logradouro}, "
            f"{self.endereco.numero}, "
            f"{self.endereco.cidade}/"
            f"{self.endereco.estado}"
        )

        endereco_novo = (
            f"{novo_endereco.logradouro}, "
            f"{novo_endereco.numero}, "
            f"{novo_endereco.cidade}/"
            f"{novo_endereco.estado}"
        )

        if self.endereco == novo_endereco:
            return False

        self.endereco = novo_endereco

        self.registrar_alteracao(
            tipo=TipoAlteracaoUnidade.ENDERECO,
            valor_anterior=endereco_anterior,
            valor_novo=endereco_novo,
            motivo=motivo,
        )

        return True

    def alterar_tipo_ligacao(
        self,
        novo_tipo,
        motivo="",
    ):
        """
        Altera o tipo de ligação elétrica
        da Unidade Consumidora.
        """

        if not isinstance(
            novo_tipo,
            TipoLigacao,
        ):
            raise TypeError(
                "O novo tipo de ligação deve pertencer "
                "ao enum TipoLigacao."
            )

        if novo_tipo == self.tipo_ligacao:
            return False

        tipo_anterior = self.tipo_ligacao

        self.tipo_ligacao = novo_tipo

        self.registrar_alteracao(
            tipo=(
                TipoAlteracaoUnidade
                .TIPO_LIGACAO
            ),
            valor_anterior=tipo_anterior.value,
            valor_novo=novo_tipo.value,
            motivo=motivo,
        )

        return True

    def ativar(self, motivo=""):
        """
        Ativa a Unidade Consumidora.
        """

        if (
            self.situacao
            == SituacaoUnidadeConsumidora.ATIVA
        ):
            return False

        situacao_anterior = self.situacao

        self.situacao = (
            SituacaoUnidadeConsumidora.ATIVA
        )

        self.registrar_alteracao(
            tipo=TipoAlteracaoUnidade.SITUACAO,
            valor_anterior=situacao_anterior.value,
            valor_novo=self.situacao.value,
            motivo=motivo,
        )

        return True

    def inativar(self, motivo=""):
        """
        Inativa a Unidade Consumidora.
        """

        if (
            self.situacao
            == SituacaoUnidadeConsumidora.INATIVA
        ):
            return False

        situacao_anterior = self.situacao

        self.situacao = (
            SituacaoUnidadeConsumidora.INATIVA
        )

        self.registrar_alteracao(
            tipo=TipoAlteracaoUnidade.SITUACAO,
            valor_anterior=situacao_anterior.value,
            valor_novo=self.situacao.value,
            motivo=motivo,
        )

        return True


def criar_unidade_consumidora(
    codigo,
    numero_uc,
    codigo_cliente,
    codigo_concessionaria,
    titular,
    endereco,
    tipo_ligacao,
    carga_instalada_kw=0.0,
):
    """
    Fábrica responsável por criar uma nova
    Unidade Consumidora.

    Toda Unidade nova começa ativa.
    """

    return UnidadeConsumidora(
        codigo=codigo,
        numero_uc=numero_uc,
        codigo_cliente=codigo_cliente,
        codigo_concessionaria=(
            codigo_concessionaria
        ),
        titular=titular,
        endereco=endereco,
        tipo_ligacao=tipo_ligacao,
        carga_instalada_kw=(
            carga_instalada_kw
        ),
        situacao=(
            SituacaoUnidadeConsumidora.ATIVA
        ),
    )


def buscar_unidade_por_codigo(
    unidades_consumidoras,
    codigo,
):
    """
    Busca uma Unidade Consumidora pelo código interno.

    Retorna a Unidade encontrada ou None.
    """

    for unidade in unidades_consumidoras:
        if unidade.codigo == codigo:
            return unidade

    return None


def buscar_unidade_por_numero_uc(
    unidades_consumidoras,
    numero_uc,
):
    """
    Busca uma Unidade Consumidora pelo número
    registrado na Concessionária.

    Retorna a Unidade encontrada ou None.
    """

    numero_procurado = str(
        numero_uc
    ).strip()

    for unidade in unidades_consumidoras:
        if unidade.numero_uc == numero_procurado:
            return unidade

    return None


def codigo_unidade_existe(
    unidades_consumidoras,
    codigo,
):
    """
    Verifica se já existe uma Unidade Consumidora
    com determinado código interno.
    """

    return (
        buscar_unidade_por_codigo(
            unidades_consumidoras,
            codigo,
        )
        is not None
    )


def numero_uc_existe(
    unidades_consumidoras,
    numero_uc,
    codigo_concessionaria=None,
):
    """
    Verifica se o número da Unidade Consumidora
    já está cadastrado.

    Quando o código da Concessionária é informado,
    a verificação considera a combinação:

        número da UC + Concessionária
    """

    numero_procurado = str(
        numero_uc
    ).strip()

    for unidade in unidades_consumidoras:
        numero_igual = (
            unidade.numero_uc
            == numero_procurado
        )

        if codigo_concessionaria is None:
            if numero_igual:
                return True

        else:
            concessionaria_igual = (
                unidade.codigo_concessionaria
                == codigo_concessionaria
            )

            if (
                numero_igual
                and concessionaria_igual
            ):
                return True

    return False