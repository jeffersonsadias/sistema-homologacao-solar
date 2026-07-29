import unittest
from unittest.mock import patch

from app.dominio.status import STATUS_PROJETO
from app.interface.status_interface import (
    exibir_status,
)


class TestStatusInterface(unittest.TestCase):
    """
    Testes da interface dos status
    de Projeto.
    """

    @patch("builtins.print")
    def test_exibir_status(
        self,
        mock_print,
    ):
        exibir_status()

        mock_print.assert_any_call(
            "\n--- STATUS DISPONÍVEIS ---"
        )

        for codigo, descricao in STATUS_PROJETO.items():
            mock_print.assert_any_call(
                f"{codigo} - {descricao}"
            )


if __name__ == "__main__":
    unittest.main()