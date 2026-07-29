"""
Repositório JSON de Projetos.

Este módulo pertence à camada de infraestrutura.

Sua responsabilidade é carregar e salvar Projetos,
sem conhecer regras de negócio, menu, input() ou print().
"""

from app import dados


ARQUIVO_PROJETOS = "projetos.json"


def carregar_projetos():
    """
    Carrega os Projetos armazenados no arquivo JSON.

    Retorna:
        Uma lista contendo os Projetos cadastrados.
    """

    return dados.carregar_dados(ARQUIVO_PROJETOS)


def salvar_projetos(projetos):
    """
    Salva a coleção atual de Projetos no arquivo JSON.

    Parâmetros:
        projetos:
            Lista contendo os Projetos que serão persistidos.
    """

    dados.salvar_dados(
        ARQUIVO_PROJETOS,
        projetos,
    )