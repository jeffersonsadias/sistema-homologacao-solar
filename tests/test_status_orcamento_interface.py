import unittest
from unittest.mock import patch

from app.interface.status_orcamento_interface import (
    exibir_status,
)

from app.dominio.status_orcamento import (
    STATUS_ORCAMENTO,
)


class TestStatusOrcamentoInterface(
    unittest.TestCase
):
    """
    Testes da exibição dos status
    no terminal.
    """

    @patch("builtins.print")
    def test_exibir_status(
        self,
        mock_print,
    ):
        """
        Deve exibir o título e todos
        os status disponíveis.
        """

        exibir_status()

        mock_print.assert_any_call(
            "\n--- STATUS DE ORÇAMENTO ---"
        )

        for codigo, descricao in (
            STATUS_ORCAMENTO.items()
        ):
            mock_print.assert_any_call(
                f"{codigo} - {descricao}"
            )


if __name__ == "__main__":
    unittest.main()