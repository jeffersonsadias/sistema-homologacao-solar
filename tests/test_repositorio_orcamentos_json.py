import unittest
from unittest.mock import patch

from app.infraestrutura.repositorio_orcamentos_json import (
    ARQUIVO_ORCAMENTOS,
    carregar_orcamentos,
    salvar_orcamentos,
)


class TestRepositorioOrcamentosJson(unittest.TestCase):
    """
    Testes do repositório JSON de Orçamentos.

    Os mocks impedem leitura ou alteração
    do arquivo real.
    """

    @patch(
        "app.infraestrutura."
        "repositorio_orcamentos_json."
        "dados.carregar_dados"
    )
    def test_carregar_orcamentos(
        self,
        mock_carregar_dados,
    ):
        """
        Deve carregar os Orçamentos pelo
        módulo genérico de dados.
        """

        orcamentos_esperados = [
            {
                "codigo": 1,
                "cliente": 3,
                "status": "Em negociação",
            }
        ]

        mock_carregar_dados.return_value = (
            orcamentos_esperados
        )

        resultado = carregar_orcamentos()

        mock_carregar_dados.assert_called_once_with(
            ARQUIVO_ORCAMENTOS
        )

        self.assertEqual(
            resultado,
            orcamentos_esperados,
        )

    @patch(
        "app.infraestrutura."
        "repositorio_orcamentos_json."
        "dados.salvar_dados"
    )
    def test_salvar_orcamentos(
        self,
        mock_salvar_dados,
    ):
        """
        Deve salvar os Orçamentos pelo
        módulo genérico de dados.
        """

        orcamentos = [
            {
                "codigo": 1,
                "cliente": 3,
                "status": "Em negociação",
            }
        ]

        salvar_orcamentos(
            orcamentos
        )

        mock_salvar_dados.assert_called_once_with(
            ARQUIVO_ORCAMENTOS,
            orcamentos,
        )


if __name__ == "__main__":
    unittest.main()