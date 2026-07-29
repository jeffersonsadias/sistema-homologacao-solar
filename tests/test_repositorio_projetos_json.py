import unittest
from unittest.mock import patch

from app.infraestrutura.repositorio_projetos_json import (
    ARQUIVO_PROJETOS,
    carregar_projetos,
    salvar_projetos,
)


class TestRepositorioProjetosJson(unittest.TestCase):
    """
    Testes do repositório JSON de Projetos.

    Os mocks impedem que os testes leiam ou alterem
    o arquivo real projetos.json.
    """

    @patch(
        "app.infraestrutura."
        "repositorio_projetos_json.dados.carregar_dados"
    )
    def test_carregar_projetos(self, mock_carregar_dados):
        """
        Deve carregar os Projetos pelo módulo genérico de dados.
        """

        projetos_esperados = [
            {
                "codigo": 1,
                "cliente": 10,
                "potencia": 5.5,
            }
        ]

        mock_carregar_dados.return_value = projetos_esperados

        projetos = carregar_projetos()

        mock_carregar_dados.assert_called_once_with(
            ARQUIVO_PROJETOS
        )

        self.assertEqual(
            projetos,
            projetos_esperados,
        )

    @patch(
        "app.infraestrutura."
        "repositorio_projetos_json.dados.salvar_dados"
    )
    def test_salvar_projetos(self, mock_salvar_dados):
        """
        Deve salvar os Projetos pelo módulo genérico de dados.
        """

        projetos = [
            {
                "codigo": 1,
                "cliente": 10,
                "potencia": 5.5,
            }
        ]

        salvar_projetos(projetos)

        mock_salvar_dados.assert_called_once_with(
            ARQUIVO_PROJETOS,
            projetos,
        )


if __name__ == "__main__":
    unittest.main()