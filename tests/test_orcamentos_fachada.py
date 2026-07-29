import unittest
from unittest.mock import patch

from app import orcamentos


class TestOrcamentosFachada(unittest.TestCase):
    """
    Testes da fachada pública de Orçamentos.
    """

    def setUp(self):
        """
        Substitui temporariamente a coleção global
        utilizada pela fachada.
        """

        self.orcamentos_originais = (
            orcamentos.orcamentos
        )

        orcamentos.orcamentos = []

    def tearDown(self):
        """
        Restaura a coleção original.
        """

        orcamentos.orcamentos = (
            self.orcamentos_originais
        )

    @patch(
        "app.orcamentos."
        "orcamentos_interface.cadastrar_orcamento"
    )
    def test_cadastrar_orcamento(
        self,
        mock_cadastrar,
    ):
        """
        Deve encaminhar o cadastro para a interface.
        """

        orcamento_esperado = {
            "codigo": 1,
        }

        mock_cadastrar.return_value = (
            orcamento_esperado
        )

        resultado = (
            orcamentos.cadastrar_orcamento()
        )

        mock_cadastrar.assert_called_once_with(
            orcamentos.orcamentos
        )

        self.assertEqual(
            resultado,
            orcamento_esperado,
        )

    @patch(
        "app.orcamentos."
        "buscar_orcamento_por_codigo"
    )
    def test_buscar_orcamento(
        self,
        mock_buscar,
    ):
        """
        Deve encaminhar a busca para o domínio.
        """

        orcamento_esperado = {
            "codigo": 5,
        }

        mock_buscar.return_value = (
            orcamento_esperado
        )

        resultado = (
            orcamentos.buscar_orcamento(5)
        )

        mock_buscar.assert_called_once_with(
            orcamentos.orcamentos,
            5,
        )

        self.assertEqual(
            resultado,
            orcamento_esperado,
        )

    @patch(
        "app.orcamentos."
        "orcamentos_interface.mostrar_orcamento"
    )
    def test_mostrar_orcamento(
        self,
        mock_mostrar,
    ):
        """
        Deve encaminhar a exibição para a interface.
        """

        dados_orcamento = {
            "codigo": 1,
        }

        orcamentos.mostrar_orcamento(
            dados_orcamento
        )

        mock_mostrar.assert_called_once_with(
            dados_orcamento
        )

    @patch(
        "app.orcamentos."
        "orcamentos_interface.listar_orcamentos"
    )
    def test_listar_orcamentos(
        self,
        mock_listar,
    ):
        """
        Deve encaminhar a listagem para a interface.
        """

        orcamentos.listar_orcamentos()

        mock_listar.assert_called_once_with(
            orcamentos.orcamentos
        )

    @patch(
        "app.orcamentos."
        "orcamentos_interface.selecionar_orcamento"
    )
    def test_selecionar_orcamento(
        self,
        mock_selecionar,
    ):
        """
        Deve encaminhar a seleção para a interface.
        """

        orcamentos.selecionar_orcamento()

        mock_selecionar.assert_called_once_with(
            orcamentos.orcamentos
        )

    @patch(
        "app.orcamentos."
        "orcamentos_interface.alterar_status"
    )
    def test_alterar_status(
        self,
        mock_alterar,
    ):
        """
        Deve encaminhar a alteração para a interface.
        """

        orcamentos.alterar_status()

        mock_alterar.assert_called_once_with(
            orcamentos.orcamentos
        )

    @patch(
        "app.orcamentos."
        "orcamentos_interface.converter_para_projeto"
    )
    def test_converter_para_projeto(
        self,
        mock_converter,
    ):
        """
        Deve encaminhar a conversão para a interface.
        """

        projeto_esperado = {
            "codigo": 8,
        }

        mock_converter.return_value = (
            projeto_esperado
        )

        resultado = (
            orcamentos.converter_para_projeto()
        )

        mock_converter.assert_called_once_with(
            orcamentos.orcamentos
        )

        self.assertEqual(
            resultado,
            projeto_esperado,
        )


if __name__ == "__main__":
    unittest.main()