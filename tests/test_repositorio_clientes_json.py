import unittest
from unittest.mock import patch

from app.infraestrutura.repositorio_clientes_json import (
    ARQUIVO_CLIENTES,
    carregar_clientes,
    salvar_clientes,
)


class TestRepositorioClientesJson(unittest.TestCase):
    """
    Testes do repositório JSON de Clientes.

    Utilizamos mocks para não alterar o arquivo real durante os testes.
    """

    @patch(
        "app.infraestrutura."
        "repositorio_clientes_json.dados.carregar_dados"
    )
    def test_carregar_clientes(self, mock_carregar_dados):
        """
        Deve carregar os Clientes pelo módulo genérico de dados.
        """

        clientes_esperados = [
            {
                "codigo": 1,
                "nome": "Ana Lima",
            }
        ]

        mock_carregar_dados.return_value = clientes_esperados

        clientes = carregar_clientes()

        mock_carregar_dados.assert_called_once_with(
            ARQUIVO_CLIENTES
        )

        self.assertEqual(
            clientes,
            clientes_esperados,
        )

    @patch(
        "app.infraestrutura."
        "repositorio_clientes_json.dados.salvar_dados"
    )
    def test_salvar_clientes(self, mock_salvar_dados):
        """
        Deve salvar os Clientes pelo módulo genérico de dados.
        """

        clientes = [
            {
                "codigo": 1,
                "nome": "Ana Lima",
            }
        ]

        salvar_clientes(clientes)

        mock_salvar_dados.assert_called_once_with(
            ARQUIVO_CLIENTES,
            clientes,
        )


if __name__ == "__main__":
    unittest.main()