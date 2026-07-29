"""
Domínio de Concessionárias.

Este módulo representa as distribuidoras de energia cadastradas
na plataforma e controla suas próprias regras de negócio.

Responsabilidades deste módulo:

- representar uma Concessionária;
- representar suas Áreas de Atuação;
- validar os dados da entidade;
- criar novas Concessionárias;
- reconstruir Concessionárias persistidas;
- buscar Concessionárias;
- controlar a situação cadastral;
- controlar as Áreas de Atuação;
- converter entidades para dicionários.

Este módulo não realiza:

- entrada de dados com input();
- exibição de dados com print();
- leitura ou gravação de arquivos JSON;
- interação direta com o usuário.
"""

from dataclasses import asdict, dataclass, field
from datetime import datetime
from typing import Optional

from app.dominio.erros_dominio import (
    DadosObrigatoriosAusentes,
    RegistroDuplicado,
    ValorInvalido,
)
from app.dominio.status import SituacaoConcessionaria


@dataclass(frozen=True)
class AreaAtuacao:
    """
    Representa uma área geográfica atendida por uma Concessionária.

    Nesta primeira versão, uma Área de Atuação é identificada pela
    combinação de estado e município.

    A entidade é imutável. Para alterar sua situação, a Concessionária
    substitui a Área de Atuação existente por uma nova instância.

    Exemplos:

        Bahia / Caetité
        Bahia / Guanambi
        Bahia / Vitória da Conquista
    """

    estado: str
    municipio: str
    ativa: bool = True


@dataclass
class Concessionaria:
    """
    Representa uma Concessionária de energia cadastrada na plataforma.

    A própria Concessionária controla suas Áreas de Atuação.

    Outros módulos não devem adicionar, remover ou alterar diretamente
    os elementos da lista areas_atuacao. Para isso, devem utilizar os
    métodos públicos disponibilizados pela própria entidade.
    """

    codigo: int
    nome: str
    nome_abreviado: str
    cnpj: Optional[str] = None
    situacao: SituacaoConcessionaria = (
        SituacaoConcessionaria.ATIVA
    )
    areas_atuacao: list[AreaAtuacao] = field(
        default_factory=list
    )
    data_cadastro: str = field(
        default_factory=lambda: obter_data_hora_atual()
    )
    data_atualizacao: str = field(
        default_factory=lambda: obter_data_hora_atual()
    )

    def adicionar_area_atuacao(
        self,
        estado,
        municipio,
    ):
        """
        Adiciona uma Área de Atuação à Concessionária.

        Não permite duplicidade da mesma combinação de estado
        e município, independentemente de letras maiúsculas,
        minúsculas ou espaços excedentes.

        Retorna a Área de Atuação criada.
        """

        estado_normalizado = validar_texto_obrigatorio(
            estado,
            "O estado da Área de Atuação é obrigatório.",
        )

        municipio_normalizado = validar_texto_obrigatorio(
            municipio,
            "O município da Área de Atuação é obrigatório.",
        )

        area_existente = self.buscar_area_atuacao(
            estado_normalizado,
            municipio_normalizado,
        )

        if area_existente is not None:
            raise RegistroDuplicado(
                "Esta Área de Atuação já está cadastrada "
                "para a Concessionária."
            )

        nova_area = AreaAtuacao(
            estado=estado_normalizado,
            municipio=municipio_normalizado,
        )

        self.areas_atuacao.append(nova_area)
        self.atualizar_data_modificacao()

        return nova_area

    def buscar_area_atuacao(
        self,
        estado,
        municipio,
    ):
        """
        Busca uma Área de Atuação pela combinação de estado
        e município.

        A busca não diferencia letras maiúsculas e minúsculas.

        Retorna a Área de Atuação quando encontrada.
        Retorna None quando não encontrada.
        """

        estado_normalizado = validar_texto_obrigatorio(
            estado,
            "O estado da Área de Atuação é obrigatório.",
        )

        municipio_normalizado = validar_texto_obrigatorio(
            municipio,
            "O município da Área de Atuação é obrigatório.",
        )

        for area in self.areas_atuacao:
            mesmo_estado = (
                area.estado.casefold()
                == estado_normalizado.casefold()
            )

            mesmo_municipio = (
                area.municipio.casefold()
                == municipio_normalizado.casefold()
            )

            if mesmo_estado and mesmo_municipio:
                return area

        return None

    def inativar_area_atuacao(
        self,
        estado,
        municipio,
    ):
        """
        Inativa uma Área de Atuação cadastrada.

        Como AreaAtuacao é imutável, a instância antiga é
        substituída por uma nova instância com ativa=False.

        Retorna a nova Área de Atuação inativa.
        """

        area = self.buscar_area_atuacao(
            estado,
            municipio,
        )

        if area is None:
            raise ValorInvalido(
                "A Área de Atuação informada não foi encontrada."
            )

        if not area.ativa:
            return area

        indice = self.areas_atuacao.index(area)

        area_inativa = AreaAtuacao(
            estado=area.estado,
            municipio=area.municipio,
            ativa=False,
        )

        self.areas_atuacao[indice] = area_inativa
        self.atualizar_data_modificacao()

        return area_inativa

    def ativar_area_atuacao(
        self,
        estado,
        municipio,
    ):
        """
        Ativa uma Área de Atuação cadastrada.

        Como AreaAtuacao é imutável, a instância antiga é
        substituída por uma nova instância com ativa=True.

        Retorna a nova Área de Atuação ativa.
        """

        area = self.buscar_area_atuacao(
            estado,
            municipio,
        )

        if area is None:
            raise ValorInvalido(
                "A Área de Atuação informada não foi encontrada."
            )

        if area.ativa:
            return area

        indice = self.areas_atuacao.index(area)

        area_ativa = AreaAtuacao(
            estado=area.estado,
            municipio=area.municipio,
            ativa=True,
        )

        self.areas_atuacao[indice] = area_ativa
        self.atualizar_data_modificacao()

        return area_ativa

    def inativar(self):
        """
        Altera a situação da Concessionária para INATIVA.

        Retorna a própria Concessionária atualizada.
        """

        self.situacao = SituacaoConcessionaria.INATIVA
        self.atualizar_data_modificacao()

        return self

    def ativar(self):
        """
        Altera a situação da Concessionária para ATIVA.

        Retorna a própria Concessionária atualizada.
        """

        self.situacao = SituacaoConcessionaria.ATIVA
        self.atualizar_data_modificacao()

        return self

    def suspender(self):
        """
        Altera a situação da Concessionária para SUSPENSA.

        Retorna a própria Concessionária atualizada.
        """

        self.situacao = SituacaoConcessionaria.SUSPENSA
        self.atualizar_data_modificacao()

        return self

    def atualizar_data_modificacao(self):
        """
        Atualiza a data da última modificação da entidade.

        Retorna a nova data de atualização.
        """

        self.data_atualizacao = obter_data_hora_atual()

        return self.data_atualizacao


def obter_data_hora_atual():
    """
    Retorna a data e a hora atuais no formato ISO.

    A precisão utilizada é de segundos.

    Exemplo:

        2026-07-27T10:35:42
    """

    return datetime.now().isoformat(
        timespec="seconds"
    )


def somente_digitos(valor):
    """
    Retorna apenas os caracteres numéricos de um valor.

    Exemplo:

        "12.345.678/0001-90"

    torna-se:

        "12345678000190"
    """

    return "".join(
        caractere
        for caractere in str(valor)
        if caractere.isdigit()
    )


def validar_texto_obrigatorio(
    valor,
    mensagem_erro,
):
    """
    Valida um campo textual obrigatório.

    A função:

    - rejeita None;
    - converte o valor para texto;
    - remove espaços no início e no final;
    - rejeita texto vazio.

    Retorna o texto normalizado.
    """

    if valor is None:
        raise DadosObrigatoriosAusentes(
            mensagem_erro
        )

    valor_normalizado = str(valor).strip()

    if not valor_normalizado:
        raise DadosObrigatoriosAusentes(
            mensagem_erro
        )

    return valor_normalizado


def validar_codigo(codigo):
    """
    Valida o código da Concessionária.

    O código deve ser:

    - do tipo int;
    - diferente de bool;
    - maior que zero.

    Retorna o código validado.
    """

    if (
        isinstance(codigo, bool)
        or not isinstance(codigo, int)
    ):
        raise ValorInvalido(
            "O código da Concessionária deve ser "
            "um número inteiro."
        )

    if codigo <= 0:
        raise ValorInvalido(
            "O código da Concessionária deve ser "
            "maior que zero."
        )

    return codigo


def normalizar_cnpj(cnpj):
    """
    Normaliza o CNPJ para conter apenas números.

    O CNPJ é opcional.

    Nesta primeira versão, a função valida somente
    a quantidade de 14 dígitos. A validação matemática
    dos dígitos verificadores poderá ser acrescentada
    posteriormente.

    Retorna:

    - None, quando o CNPJ não for informado;
    - uma string com 14 números, quando válido.
    """

    if cnpj is None:
        return None

    cnpj_normalizado = somente_digitos(cnpj)

    if not cnpj_normalizado:
        return None

    if len(cnpj_normalizado) != 14:
        raise ValorInvalido(
            "O CNPJ deve possuir exatamente 14 dígitos."
        )

    return cnpj_normalizado


def normalizar_situacao_concessionaria(situacao):
    """
    Converte uma situação para SituacaoConcessionaria.

    Aceita:

    - uma instância de SituacaoConcessionaria;
    - uma string correspondente a um valor do Enum.

    Retorna uma instância de SituacaoConcessionaria.
    """

    if isinstance(
        situacao,
        SituacaoConcessionaria,
    ):
        return situacao

    try:
        return SituacaoConcessionaria(situacao)

    except (ValueError, TypeError):
        raise ValorInvalido(
            "A situação da Concessionária é inválida."
        )


def criar_concessionaria(
    codigo,
    nome,
    nome_abreviado,
    cnpj=None,
):
    """
    Cria uma nova Concessionária após validar
    seus dados básicos.

    Novas Concessionárias são criadas com:

    - situação ATIVA;
    - lista vazia de Áreas de Atuação;
    - data de cadastro atual;
    - data de atualização atual.

    Retorna uma instância de Concessionaria.
    """

    codigo_validado = validar_codigo(codigo)

    nome_validado = validar_texto_obrigatorio(
        nome,
        "O nome da Concessionária é obrigatório.",
    )

    nome_abreviado_validado = (
        validar_texto_obrigatorio(
            nome_abreviado,
            "O nome abreviado da Concessionária "
            "é obrigatório.",
        )
    )

    cnpj_normalizado = normalizar_cnpj(cnpj)

    data_atual = obter_data_hora_atual()

    return Concessionaria(
        codigo=codigo_validado,
        nome=nome_validado,
        nome_abreviado=nome_abreviado_validado,
        cnpj=cnpj_normalizado,
        situacao=SituacaoConcessionaria.ATIVA,
        areas_atuacao=[],
        data_cadastro=data_atual,
        data_atualizacao=data_atual,
    )


def reconstruir_concessionaria(
    codigo,
    nome,
    nome_abreviado,
    cnpj=None,
    situacao=SituacaoConcessionaria.ATIVA,
    areas_atuacao=None,
    data_cadastro=None,
    data_atualizacao=None,
):
    """
    Reconstrói uma Concessionária a partir de dados persistidos.

    Esta função é destinada principalmente à camada de
    infraestrutura durante o carregamento do arquivo JSON.

    Diferentemente de criar_concessionaria(), ela permite
    restaurar:

    - situação cadastral;
    - Áreas de Atuação;
    - data de cadastro;
    - data de atualização.

    Retorna uma instância de Concessionaria.
    """

    codigo_validado = validar_codigo(codigo)

    nome_validado = validar_texto_obrigatorio(
        nome,
        "O nome da Concessionária é obrigatório.",
    )

    nome_abreviado_validado = (
        validar_texto_obrigatorio(
            nome_abreviado,
            "O nome abreviado da Concessionária "
            "é obrigatório.",
        )
    )

    cnpj_normalizado = normalizar_cnpj(cnpj)

    situacao_normalizada = (
        normalizar_situacao_concessionaria(
            situacao
        )
    )

    areas_reconstruidas = []

    for dados_area in areas_atuacao or []:
        if isinstance(dados_area, AreaAtuacao):
            area = dados_area

        elif isinstance(dados_area, dict):
            estado = validar_texto_obrigatorio(
                dados_area.get("estado"),
                "O estado da Área de Atuação é obrigatório.",
            )

            municipio = validar_texto_obrigatorio(
                dados_area.get("municipio"),
                "O município da Área de Atuação é obrigatório.",
            )

            ativa = dados_area.get(
                "ativa",
                True,
            )

            if not isinstance(ativa, bool):
                raise ValorInvalido(
                    "A situação da Área de Atuação "
                    "deve ser um valor booleano."
                )

            area = AreaAtuacao(
                estado=estado,
                municipio=municipio,
                ativa=ativa,
            )

        else:
            raise ValorInvalido(
                "Os dados da Área de Atuação são inválidos."
            )

        area_duplicada = any(
            area_existente.estado.casefold()
            == area.estado.casefold()
            and area_existente.municipio.casefold()
            == area.municipio.casefold()
            for area_existente in areas_reconstruidas
        )

        if area_duplicada:
            raise RegistroDuplicado(
                "Existe uma Área de Atuação duplicada "
                "nos dados da Concessionária."
            )

        areas_reconstruidas.append(area)

    data_atual = obter_data_hora_atual()

    return Concessionaria(
        codigo=codigo_validado,
        nome=nome_validado,
        nome_abreviado=nome_abreviado_validado,
        cnpj=cnpj_normalizado,
        situacao=situacao_normalizada,
        areas_atuacao=areas_reconstruidas,
        data_cadastro=data_cadastro or data_atual,
        data_atualizacao=(
            data_atualizacao
            or data_cadastro
            or data_atual
        ),
    )


def buscar_concessionaria_por_codigo(
    lista_concessionarias,
    codigo,
):
    """
    Busca uma Concessionária pelo código.

    Retorna a própria entidade quando encontrada.
    Retorna None quando não encontrada.
    """

    for concessionaria in lista_concessionarias:
        if concessionaria.codigo == codigo:
            return concessionaria

    return None


def codigo_concessionaria_existe(
    lista_concessionarias,
    codigo,
):
    """
    Verifica se existe uma Concessionária
    com o código informado.

    Retorna True ou False.
    """

    concessionaria = (
        buscar_concessionaria_por_codigo(
            lista_concessionarias,
            codigo,
        )
    )

    return concessionaria is not None


def buscar_concessionarias_por_nome(
    lista_concessionarias,
    nome,
):
    """
    Busca Concessionárias pelo nome completo
    ou pelo nome abreviado.

    A busca:

    - não diferencia letras maiúsculas e minúsculas;
    - permite informar somente parte do nome;
    - remove espaços excedentes da consulta.

    Retorna uma lista de resultados.
    """

    nome_normalizado = validar_texto_obrigatorio(
        nome,
        "O nome usado na busca é obrigatório.",
    ).casefold()

    resultados = []

    for concessionaria in lista_concessionarias:
        corresponde_nome = (
            nome_normalizado
            in concessionaria.nome.casefold()
        )

        corresponde_nome_abreviado = (
            nome_normalizado
            in concessionaria.nome_abreviado.casefold()
        )

        if (
            corresponde_nome
            or corresponde_nome_abreviado
        ):
            resultados.append(concessionaria)

    return resultados


def validar_duplicidade_concessionaria(
    lista_concessionarias,
    codigo,
    cnpj=None,
):
    """
    Verifica duplicidade de código e CNPJ.

    O código deve ser único.

    Quando informado, o CNPJ também deve ser único.

    Não retorna valor quando os dados estiverem disponíveis.
    Lança RegistroDuplicado quando houver conflito.
    """

    codigo_validado = validar_codigo(codigo)

    if codigo_concessionaria_existe(
        lista_concessionarias,
        codigo_validado,
    ):
        raise RegistroDuplicado(
            "Já existe uma Concessionária cadastrada "
            "com este código."
        )

    cnpj_normalizado = normalizar_cnpj(cnpj)

    if cnpj_normalizado is None:
        return

    for concessionaria in lista_concessionarias:
        if concessionaria.cnpj == cnpj_normalizado:
            raise RegistroDuplicado(
                "Já existe uma Concessionária cadastrada "
                "com este CNPJ."
            )


def converter_concessionaria_para_dicionario(
    concessionaria,
):
    """
    Converte uma Concessionária para um dicionário
    adequado à persistência em JSON.

    O Enum da situação é convertido para string.

    As Áreas de Atuação são convertidas automaticamente
    pelo asdict().
    """

    if not isinstance(
        concessionaria,
        Concessionaria,
    ):
        raise ValorInvalido(
            "O objeto informado não é uma Concessionária."
        )

    dados = asdict(concessionaria)

    dados["situacao"] = concessionaria.situacao.value

    return dados