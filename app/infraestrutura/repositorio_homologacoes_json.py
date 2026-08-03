"""
Repositório JSON de Homologações.

Este módulo pertence à camada de infraestrutura.

Sua responsabilidade é carregar e salvar Homologações,
sem conhecer regras de negócio, menu, input() ou print().
"""

from app import dados


ARQUIVO_HOMOLOGACOES = "homologacoes.json"


def carregar_homologacoes():
    """
    Carrega as Homologações armazenadas no arquivo JSON.

    Retorna:
        Uma lista contendo as Homologações cadastradas.
    """

    return dados.carregar_dados(
        ARQUIVO_HOMOLOGACOES
    )

def salvar_homologacoes(
    homologacoes,
):
    """
    Salva a coleção atual de Homologações no arquivo JSON.

    Parâmetros:
        homologacoes:
            Lista contendo as Homologações que serão persistidas.
    """

    dados.salvar_dados(
        ARQUIVO_HOMOLOGACOES,
        homologacoes,
    )