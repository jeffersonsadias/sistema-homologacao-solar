"""
Domínio dos vínculos entre Projetos
e Unidades Consumidoras.

Uma Unidade Consumidora não possui,
por natureza, o papel de Geradora
ou Beneficiária.

Esse papel existe somente dentro
do contexto de um Projeto.
"""

from dataclasses import dataclass
from datetime import datetime
from enum import Enum

from app.dominio.status import (
    PapelUnidadeProjeto,
)


class SituacaoVinculoUnidadeProjeto(Enum):
    """
    Situações possíveis de um vínculo
    entre Projeto e Unidade Consumidora.
    """

    ATIVO = "Ativo"
    INATIVO = "Inativo"


@dataclass
class VinculoUnidadeProjeto:
    """
    Representa a participação de uma
    Unidade Consumidora em um Projeto.

    O atributo papel determina se a Unidade
    atua como Geradora ou Beneficiária
    naquele Projeto específico.
    """

    codigo: int
    codigo_projeto: int
    codigo_unidade_consumidora: int
    papel: PapelUnidadeProjeto
    situacao: SituacaoVinculoUnidadeProjeto
    data_vinculo: datetime
    data_atualizacao: datetime
    observacoes: str = ""

    def esta_ativo(self):
        """
        Informa se o vínculo está ativo.
        """

        return (
            self.situacao
            == SituacaoVinculoUnidadeProjeto.ATIVO
        )

    def ativar(self):
        """
        Ativa o vínculo.
        """

        self.situacao = (
            SituacaoVinculoUnidadeProjeto.ATIVO
        )

        self.data_atualizacao = datetime.now()

    def inativar(self):
        """
        Inativa o vínculo.
        """

        self.situacao = (
            SituacaoVinculoUnidadeProjeto.INATIVO
        )

        self.data_atualizacao = datetime.now()

    def alterar_observacoes(
        self,
        novas_observacoes,
    ):
        """
        Atualiza as observações
        relacionadas ao vínculo.
        """

        self.observacoes = (
            novas_observacoes.strip()
        )

        self.data_atualizacao = datetime.now()


def criar_vinculo_unidade_projeto(
    codigo,
    codigo_projeto,
    codigo_unidade_consumidora,
    papel,
    vinculos_existentes,
    observacoes="",
):
    """
    Cria um vínculo entre uma Unidade
    Consumidora e um Projeto.

    Regras verificadas:

    - os códigos devem ser números inteiros
      positivos;
    - o papel deve ser válido;
    - uma mesma Unidade não pode ser vinculada
      duas vezes ao mesmo Projeto;
    - um Projeto não pode possuir mais de uma
      Unidade Geradora ativa.
    """

    _validar_codigo(
        codigo,
        "Código do vínculo",
    )

    _validar_codigo(
        codigo_projeto,
        "Código do projeto",
    )

    _validar_codigo(
        codigo_unidade_consumidora,
        "Código da Unidade Consumidora",
    )

    if codigo_vinculo_existe(
        codigo,
        vinculos_existentes,
    ):
        raise ValueError(
            "Já existe um vínculo com esse código."
        )

    if not isinstance(
        papel,
        PapelUnidadeProjeto,
    ):
        raise ValueError(
            "O papel informado para a Unidade "
            "Consumidora é inválido."
        )

    vinculo_existente = (
        buscar_vinculo_da_unidade_no_projeto(
            codigo_projeto,
            codigo_unidade_consumidora,
            vinculos_existentes,
            somente_ativos=True,
        )
    )

    if vinculo_existente is not None:
        raise ValueError(
            "A Unidade Consumidora já está "
            "vinculada a esse Projeto."
        )

    if (
        papel
        == PapelUnidadeProjeto.GERADORA
    ):
        geradora_existente = (
            obter_unidade_geradora_do_projeto(
                codigo_projeto,
                vinculos_existentes,
            )
        )

        if geradora_existente is not None:
            raise ValueError(
                "O Projeto já possui uma "
                "Unidade Geradora ativa."
            )

    agora = datetime.now()

    return VinculoUnidadeProjeto(
        codigo=codigo,
        codigo_projeto=codigo_projeto,
        codigo_unidade_consumidora=(
            codigo_unidade_consumidora
        ),
        papel=papel,
        situacao=(
            SituacaoVinculoUnidadeProjeto.ATIVO
        ),
        data_vinculo=agora,
        data_atualizacao=agora,
        observacoes=observacoes.strip(),
    )


def buscar_vinculo_por_codigo(
    codigo,
    vinculos,
):
    """
    Busca um vínculo pelo seu código interno.

    Retorna o vínculo encontrado ou None.
    """

    for vinculo in vinculos:
        if vinculo.codigo == codigo:
            return vinculo

    return None


def codigo_vinculo_existe(
    codigo,
    vinculos,
):
    """
    Informa se já existe um vínculo
    com o código recebido.
    """

    return (
        buscar_vinculo_por_codigo(
            codigo,
            vinculos,
        )
        is not None
    )


def listar_vinculos_do_projeto(
    codigo_projeto,
    vinculos,
    somente_ativos=True,
):
    """
    Retorna os vínculos pertencentes
    a determinado Projeto.
    """

    vinculos_encontrados = []

    for vinculo in vinculos:
        pertence_ao_projeto = (
            vinculo.codigo_projeto
            == codigo_projeto
        )

        if not pertence_ao_projeto:
            continue

        if (
            somente_ativos
            and not vinculo.esta_ativo()
        ):
            continue

        vinculos_encontrados.append(
            vinculo
        )

    return vinculos_encontrados


def buscar_vinculo_da_unidade_no_projeto(
    codigo_projeto,
    codigo_unidade_consumidora,
    vinculos,
    somente_ativos=True,
):
    """
    Busca o vínculo de uma Unidade
    Consumidora dentro de um Projeto.
    """

    for vinculo in vinculos:
        mesmo_projeto = (
            vinculo.codigo_projeto
            == codigo_projeto
        )

        mesma_unidade = (
            vinculo.codigo_unidade_consumidora
            == codigo_unidade_consumidora
        )

        if not (
            mesmo_projeto
            and mesma_unidade
        ):
            continue

        if (
            somente_ativos
            and not vinculo.esta_ativo()
        ):
            continue

        return vinculo

    return None


def obter_unidade_geradora_do_projeto(
    codigo_projeto,
    vinculos,
):
    """
    Retorna o vínculo ativo da Unidade Geradora
    de determinado Projeto.

    Retorna None quando o Projeto ainda não
    possui Unidade Geradora vinculada.
    """

    for vinculo in vinculos:
        pertence_ao_projeto = (
            vinculo.codigo_projeto
            == codigo_projeto
        )

        papel_geradora = (
            vinculo.papel
            == PapelUnidadeProjeto.GERADORA
        )

        if (
            pertence_ao_projeto
            and papel_geradora
            and vinculo.esta_ativo()
        ):
            return vinculo

    return None


def listar_unidades_beneficiarias_do_projeto(
    codigo_projeto,
    vinculos,
):
    """
    Retorna os vínculos ativos das Unidades
    Beneficiárias de determinado Projeto.
    """

    beneficiarias = []

    for vinculo in vinculos:
        pertence_ao_projeto = (
            vinculo.codigo_projeto
            == codigo_projeto
        )

        papel_beneficiaria = (
            vinculo.papel
            == PapelUnidadeProjeto.BENEFICIARIA
        )

        if (
            pertence_ao_projeto
            and papel_beneficiaria
            and vinculo.esta_ativo()
        ):
            beneficiarias.append(
                vinculo
            )

    return beneficiarias


def _validar_codigo(
    codigo,
    nome_campo,
):
    """
    Valida códigos numéricos internos.

    O underline inicial indica que esta função
    é de uso interno do módulo.
    """

    if not isinstance(
        codigo,
        int,
    ):
        raise ValueError(
            f"{nome_campo} deve ser um "
            "número inteiro."
        )

    if codigo <= 0:
        raise ValueError(
            f"{nome_campo} deve ser maior "
            "que zero."
        )