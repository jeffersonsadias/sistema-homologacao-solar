"""
Interface de terminal dos status de Projeto.
"""

from app.dominio.status import STATUS_PROJETO


def exibir_status():
    """
    Exibe os status disponíveis para Projetos.
    """

    print("\n--- STATUS DISPONÍVEIS ---")

    for codigo, descricao in STATUS_PROJETO.items():
        print(f"{codigo} - {descricao}")