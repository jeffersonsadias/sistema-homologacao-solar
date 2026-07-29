"""
Repositório JSON de Orçamentos.

Este módulo pertence à camada de infraestrutura.

Responsabilidades:
- carregar Orçamentos;
- salvar Orçamentos;
- conhecer o nome do arquivo físico.

Não contém regras de negócio nem interação
com o terminal.
"""

from app import dados


ARQUIVO_ORCAMENTOS = "orcamentos.json"


def carregar_orcamentos():
    """
    Carrega os Orçamentos armazenados no JSON.

    Retorna:
        Lista de Orçamentos cadastrados.
    """

    return dados.carregar_dados(
        ARQUIVO_ORCAMENTOS
    )


def salvar_orcamentos(orcamentos):
    """
    Salva a coleção atual de Orçamentos.

    Parâmetros:
        orcamentos:
            Lista de Orçamentos a ser persistida.
    """

    dados.salvar_dados(
        ARQUIVO_ORCAMENTOS,
        orcamentos,
    )