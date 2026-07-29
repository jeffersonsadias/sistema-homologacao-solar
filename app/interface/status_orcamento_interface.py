"""
Interface de terminal dos status de Orçamento.
"""

from app.dominio.status_orcamento import (
    STATUS_ORCAMENTO,
)


def exibir_status():
    """
    Exibe todos os status disponíveis
    para Orçamentos.
    """

    print("\n--- STATUS DE ORÇAMENTO ---")

    for codigo, descricao in (
        STATUS_ORCAMENTO.items()
    ):
        print(
            f"{codigo} - {descricao}"
        )
