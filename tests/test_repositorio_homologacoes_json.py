"""
Testes do repositório JSON de Homologações.

Os mocks impedem que os testes leiam ou alterem
o arquivo real homologacoes.json.
"""

import unittest
from unittest.mock import patch

from app.infraestrutura.repositorio_homologacoes_json import (
    ARQUIVO_HOMOLOGACOES,
    carregar_homologacoes,
    salvar_homologacoes,
)


class TestRepositorioHomologacoesJson(unittest.TestCase):
    """
    Testes do repositório JSON de Homologações.
    """

    @patch(
        "app.infraestrutura."
        "repositorio_homologacoes_json.dados.carregar_dados"
    )
    def test_carregar_homologacoes(
        self,
        mock_carregar_dados,
    ):
        """
        Deve carregar as Homologações pelo módulo genérico
        de dados.
        """

        homologacoes_esperadas = [
            {
                "codigo": 1,
                "codigo_empresa": 1,
                "codigo_projeto": 10,
                "status": "EM_PREPARACAO",
            }
        ]

        mock_carregar_dados.return_value = (
            homologacoes_esperadas
        )

        homologacoes = carregar_homologacoes()

        mock_carregar_dados.assert_called_once_with(
            ARQUIVO_HOMOLOGACOES
        )

        self.assertEqual(
            homologacoes,
            homologacoes_esperadas,
        )

    @patch(
        "app.infraestrutura."
        "repositorio_homologacoes_json.dados.salvar_dados"
    )
    def test_salvar_homologacoes(
        self,
        mock_salvar_dados,
    ):
        """
        Deve salvar as Homologações pelo módulo genérico
        de dados.
        """

        homologacoes = [
            {
                "codigo": 1,
                "codigo_empresa": 1,
                "codigo_projeto": 10,
                "status": "EM_PREPARACAO",
            }
        ]

        salvar_homologacoes(
            homologacoes
        )

        mock_salvar_dados.assert_called_once_with(
            ARQUIVO_HOMOLOGACOES,
            homologacoes,
        )


if __name__ == "__main__":
    unittest.main()