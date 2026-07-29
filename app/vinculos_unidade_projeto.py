"""
Fachada pública dos vínculos entre
Projetos e Unidades Consumidoras.

Este módulo coordena:

- domínio;
- persistência;
- lista de vínculos carregada;
- operações públicas do sistema.
"""
from app import projetos
from app import unidades_consumidoras

from app.dominio.status import (
    PapelUnidadeProjeto,
)

from app.dominio.vinculos_unidade_projeto import (
    buscar_vinculo_da_unidade_no_projeto
    as buscar_vinculo_unidade_dominio,
)

from app.dominio.vinculos_unidade_projeto import (
    buscar_vinculo_por_codigo
    as buscar_vinculo_por_codigo_dominio,
)

from app.dominio.vinculos_unidade_projeto import (
    criar_vinculo_unidade_projeto
    as criar_vinculo_dominio,
)

from app.dominio.vinculos_unidade_projeto import (
    listar_unidades_beneficiarias_do_projeto
    as listar_beneficiarias_dominio,
)

from app.dominio.vinculos_unidade_projeto import (
    listar_vinculos_do_projeto
    as listar_vinculos_projeto_dominio,
)

from app.dominio.vinculos_unidade_projeto import (
    obter_unidade_geradora_do_projeto
    as obter_geradora_dominio,
)

from app.infraestrutura.repositorio_vinculos_unidade_projeto_json import (
        carregar_vinculos_unidade_projeto,
        salvar_vinculos_unidade_projeto,
    )


vinculos_unidade_projeto = (
    carregar_vinculos_unidade_projeto()
)


def obter_vinculos_unidade_projeto():
    """
    Retorna a lista mantida
    pela fachada.

    Esta função deve ser usada por outros
    módulos em vez do acesso direto à
    variável global.
    """

    return vinculos_unidade_projeto


def gerar_proximo_codigo():
    """
    Gera o próximo código interno
    disponível para um vínculo.
    """

    if not vinculos_unidade_projeto:
        return 1

    maior_codigo = max(
        vinculo.codigo
        for vinculo
        in vinculos_unidade_projeto
    )

    return maior_codigo + 1

def _validar_existencia_projeto(
    codigo_projeto,
):
    """
    Verifica se o Projeto informado existe.

    Levanta ValueError quando o código
    não corresponde a um Projeto cadastrado.
    """

    projeto = projetos.buscar_projeto(
        codigo_projeto
    )

    if projeto is None:
        raise ValueError(
            "O Projeto informado não existe."
        )

    return projeto


def _validar_existencia_unidade_consumidora(
    codigo_unidade_consumidora,
):
    """
    Verifica se a Unidade Consumidora
    informada existe.

    Levanta ValueError quando o código
    não corresponde a uma Unidade cadastrada.
    """

    unidade = (
        unidades_consumidoras
        .obter_unidade_consumidora_por_codigo(
            codigo_unidade_consumidora
        )
    )

    if unidade is None:
        raise ValueError(
            "A Unidade Consumidora informada "
            "não existe."
        )

    return unidade

def criar_vinculo(
    codigo_projeto,
    codigo_unidade_consumidora,
    papel,
    observacoes="",
):
    """
    Cria e salva um novo vínculo entre
    Projeto e Unidade Consumidora.

    Antes da criação, verifica se:

    - o Projeto existe;
    - a Unidade Consumidora existe;
    - as regras do domínio são respeitadas.
    """

    _validar_existencia_projeto(
        codigo_projeto
    )

    _validar_existencia_unidade_consumidora(
        codigo_unidade_consumidora
    )

    codigo = gerar_proximo_codigo()

    novo_vinculo = criar_vinculo_dominio(
        codigo=codigo,
        codigo_projeto=codigo_projeto,
        codigo_unidade_consumidora=(
            codigo_unidade_consumidora
        ),
        papel=papel,
        vinculos_existentes=(
            vinculos_unidade_projeto
        ),
        observacoes=observacoes,
    )

    vinculos_unidade_projeto.append(
        novo_vinculo
    )

    salvar_vinculos_unidade_projeto(
        vinculos_unidade_projeto
    )

    return novo_vinculo


def vincular_unidade_geradora(
    codigo_projeto,
    codigo_unidade_consumidora,
    observacoes="",
):
    """
    Cria um vínculo com papel
    de Unidade Geradora.
    """

    return criar_vinculo(
        codigo_projeto=(
            codigo_projeto
        ),
        codigo_unidade_consumidora=(
            codigo_unidade_consumidora
        ),
        papel=(
            PapelUnidadeProjeto.GERADORA
        ),
        observacoes=observacoes,
    )


def vincular_unidade_beneficiaria(
    codigo_projeto,
    codigo_unidade_consumidora,
    observacoes="",
):
    """
    Cria um vínculo com papel
    de Unidade Beneficiária.
    """

    return criar_vinculo(
        codigo_projeto=(
            codigo_projeto
        ),
        codigo_unidade_consumidora=(
            codigo_unidade_consumidora
        ),
        papel=(
            PapelUnidadeProjeto.BENEFICIARIA
        ),
        observacoes=observacoes,
    )


def buscar_vinculo_por_codigo(
    codigo,
):
    """
    Busca um vínculo pelo código interno.
    """

    return buscar_vinculo_por_codigo_dominio(
        codigo,
        vinculos_unidade_projeto,
    )


def listar_vinculos_do_projeto(
    codigo_projeto,
    somente_ativos=True,
):
    """
    Lista os vínculos pertencentes
    a determinado Projeto.
    """

    return listar_vinculos_projeto_dominio(
        codigo_projeto,
        vinculos_unidade_projeto,
        somente_ativos,
    )


def buscar_vinculo_da_unidade_no_projeto(
    codigo_projeto,
    codigo_unidade_consumidora,
    somente_ativos=True,
):
    """
    Busca o vínculo de determinada
    Unidade dentro de um Projeto.
    """

    return buscar_vinculo_unidade_dominio(
        codigo_projeto,
        codigo_unidade_consumidora,
        vinculos_unidade_projeto,
        somente_ativos,
    )


def obter_unidade_geradora_do_projeto(
    codigo_projeto,
):
    """
    Retorna o vínculo ativo da Unidade
    Geradora de determinado Projeto.
    """

    return obter_geradora_dominio(
        codigo_projeto,
        vinculos_unidade_projeto,
    )


def listar_unidades_beneficiarias_do_projeto(
    codigo_projeto,
):
    """
    Retorna os vínculos ativos das Unidades
    Beneficiárias de determinado Projeto.
    """

    return listar_beneficiarias_dominio(
        codigo_projeto,
        vinculos_unidade_projeto,
    )


def inativar_vinculo(
    codigo,
):
    """
    Inativa um vínculo e salva
    a alteração no repositório.

    Retorna o vínculo alterado ou None
    quando ele não for encontrado.
    """

    vinculo = buscar_vinculo_por_codigo(
        codigo
    )

    if vinculo is None:
        return None

    vinculo.inativar()

    salvar_vinculos_unidade_projeto(
        vinculos_unidade_projeto
    )

    return vinculo

def ativar_vinculo(
    codigo,
):
    """
    Ativa um vínculo existente.

    Antes da ativação, verifica se ela
    causaria:

    - duplicidade da mesma Unidade
      no mesmo Projeto;
    - mais de uma Unidade Geradora
      ativa no mesmo Projeto.
    """

    vinculo = buscar_vinculo_por_codigo(
        codigo
    )

    if vinculo is None:
        return None

    if vinculo.esta_ativo():
        return vinculo

    vinculo_da_mesma_unidade = (
        buscar_vinculo_unidade_dominio(
            vinculo.codigo_projeto,
            vinculo.codigo_unidade_consumidora,
            vinculos_unidade_projeto,
            True,
        )
    )

    if (
        vinculo_da_mesma_unidade is not None
        and vinculo_da_mesma_unidade
        is not vinculo
    ):
        raise ValueError(
            "Já existe um vínculo ativo para "
            "essa Unidade no Projeto."
        )

    if (
        vinculo.papel
        == PapelUnidadeProjeto.GERADORA
    ):
        geradora_ativa = (
            obter_geradora_dominio(
                vinculo.codigo_projeto,
                vinculos_unidade_projeto,
            )
        )

        if (
            geradora_ativa is not None
            and geradora_ativa is not vinculo
        ):
            raise ValueError(
                "O Projeto já possui uma "
                "Unidade Geradora ativa."
            )

    vinculo.ativar()

    salvar_vinculos_unidade_projeto(
        vinculos_unidade_projeto
    )

    return vinculo

def alterar_observacoes(
    codigo,
    novas_observacoes,
):
    """
    Altera as observações de um vínculo
    e salva a atualização.

    Retorna o vínculo alterado ou None
    quando ele não for encontrado.
    """

    vinculo = buscar_vinculo_por_codigo(
        codigo
    )

    if vinculo is None:
        return None

    vinculo.alterar_observacoes(
        novas_observacoes
    )

    salvar_vinculos_unidade_projeto(
        vinculos_unidade_projeto
    )

    return vinculo