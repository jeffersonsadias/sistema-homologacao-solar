"""
Fachada do módulo de Unidades Consumidoras.

Este módulo coordena o acesso às Unidades Consumidoras
cadastradas no sistema.

Responsabilidades da fachada:

- manter a coleção de Unidades Consumidoras carregada;
- encaminhar operações para a camada de interface;
- disponibilizar funções públicas para outros módulos;
- impedir que outros módulos manipulem diretamente
  a lista interna de Unidades Consumidoras.
"""

from app.dominio.unidades_consumidoras import (
    buscar_unidade_por_codigo
    as buscar_unidade_por_codigo_dominio,
)
from app.infraestrutura import (
    repositorio_unidades_consumidoras_json
    as repositorio,
)
from app.interface import (
    unidades_consumidoras_interface
    as interface,
)


# ============================================================
# CARREGAMENTO DOS DADOS
# ============================================================

unidades_consumidoras = (
    repositorio.carregar_unidades_consumidoras()
)


# ============================================================
# FUNÇÕES DE PERSISTÊNCIA
# ============================================================

def salvar_unidades_consumidoras():
    """
    Salva no arquivo JSON todas as Unidades Consumidoras
    mantidas atualmente pela fachada.
    """

    repositorio.salvar_unidades_consumidoras(
        unidades_consumidoras
    )


# ============================================================
# FUNÇÕES DE INTERFACE
# ============================================================

def cadastrar_unidade_consumidora(
    concessionarias,
):
    """
    Abre o fluxo de cadastro de uma Unidade Consumidora.

    A lista de Unidades Consumidoras e a lista de
    Concessionárias são encaminhadas para a interface.
    """

    return interface.cadastrar_unidade_consumidora(
        unidades_consumidoras,
        concessionarias,
    )


def listar_unidades_consumidoras(
    concessionarias,
):
    """
    Exibe todas as Unidades Consumidoras cadastradas.

    A lista de Concessionárias é fornecida para permitir
    que a interface apresente os dados da Concessionária
    relacionada a cada Unidade Consumidora.
    """

    return interface.listar_unidades_consumidoras(
        unidades_consumidoras,
        concessionarias,
    )


def buscar_unidade_consumidora(
    concessionarias,
):
    """
    Abre o fluxo interativo de busca de uma
    Unidade Consumidora.
    """

    return interface.buscar_unidade_consumidora(
        unidades_consumidoras,
        concessionarias,
    )


def selecionar_unidade_por_codigo():
    """
    Abre o fluxo de seleção de uma Unidade Consumidora
    pelo seu código interno.
    """

    return interface.selecionar_unidade_por_codigo(
        unidades_consumidoras
    )


def alterar_situacao_unidade():
    """
    Abre o fluxo responsável pela alteração da situação
    de uma Unidade Consumidora.
    """

    return interface.alterar_situacao_unidade(
        unidades_consumidoras
    )


def abrir_menu_unidades_consumidoras(
    concessionarias,
):
    """
    Abre o menu específico das Unidades Consumidoras.
    """

    return interface.menu_unidades_consumidoras(
        unidades_consumidoras,
        concessionarias,
    )


# ============================================================
# FUNÇÕES PÚBLICAS PARA OUTROS MÓDULOS
# ============================================================

def obter_unidade_consumidora_por_codigo(
    codigo,
):
    """
    Busca uma Unidade Consumidora pelo código interno.

    Esta função é pública e pode ser utilizada por outros
    módulos, como o módulo de vínculos entre Unidade
    Consumidora e Projeto.

    O primeiro argumento enviado ao domínio deve ser a
    coleção de Unidades Consumidoras.

    O segundo argumento deve ser o código pesquisado.
    """

    return buscar_unidade_por_codigo_dominio(
        unidades_consumidoras,
        codigo,
    )