import unittest
from unittest.mock import patch

from app import concessionarias


class TestConcessionariasFachada(
    unittest.TestCase
):
    """
    Testes da fachada pública
    do módulo de Concessionárias.

    As funções da interface são simuladas
    para verificar se a fachada delega
    corretamente as operações.
    """

    def setUp(self):
        """
        Substitui temporariamente a lista global
        de Concessionárias por uma lista vazia.
        """

        self.lista_original = (
            concessionarias.concessionarias
        )

        concessionarias.concessionarias = []

    def tearDown(self):
        """
        Restaura a lista global original
        depois de cada teste.
        """

        concessionarias.concessionarias = (
            self.lista_original
        )

    @patch(
    "app.concessionarias."
    "buscar_concessionaria_por_codigo"
    )
    def test_obter_concessionaria(
        self,
        mock_buscar,
    ):
        """
        Deve retornar obrigatoriamente a Concessionária
        encontrada pelo domínio.
        """

        concessionaria_esperada = object()

        mock_buscar.return_value = (
            concessionaria_esperada
        )

        resultado = concessionarias.obter_concessionaria(
            10
        )

        mock_buscar.assert_called_once_with(
            concessionarias.concessionarias,
            10,
        )

        self.assertIs(
            resultado,
            concessionaria_esperada,
        )

    @patch(
        "app.concessionarias."
        "buscar_concessionaria_por_codigo"
    )
    def test_obter_concessionaria_inexistente(
        self,
        mock_buscar,
    ):
        """
        Deve gerar ValueError quando a Concessionária
        não for encontrada.
        """

        mock_buscar.return_value = None

        with self.assertRaisesRegex(
            ValueError,
            "não encontrada",
        ):
            concessionarias.obter_concessionaria(
                999
            )

    @patch(
        "app.concessionarias."
        "concessionarias_interface."
        "cadastrar_concessionaria"
    )
    def test_cadastrar_concessionaria(
        self,
        mock_cadastrar,
    ):
        """
        Deve delegar o cadastro
        para a camada de interface.
        """

        objeto_esperado = object()

        mock_cadastrar.return_value = (
            objeto_esperado
        )

        resultado = (
            concessionarias
            .cadastrar_concessionaria()
        )

        mock_cadastrar.assert_called_once_with(
            concessionarias.concessionarias
        )

        self.assertIs(
            resultado,
            objeto_esperado,
        )

    @patch(
        "app.concessionarias."
        "concessionarias_interface."
        "listar_concessionarias"
    )
    def test_listar_concessionarias(
        self,
        mock_listar,
    ):
        """
        Deve delegar a listagem
        para a camada de interface.
        """

        concessionarias.listar_concessionarias()

        mock_listar.assert_called_once_with(
            concessionarias.concessionarias
        )

    @patch(
        "app.concessionarias."
        "concessionarias_interface."
        "buscar_concessionaria"
    )
    def test_buscar_concessionaria(
        self,
        mock_buscar,
    ):
        """
        Deve delegar a busca
        para a camada de interface.
        """

        objeto_esperado = object()

        mock_buscar.return_value = (
            objeto_esperado
        )

        resultado = (
            concessionarias
            .buscar_concessionaria()
        )

        mock_buscar.assert_called_once_with(
            concessionarias.concessionarias
        )

        self.assertIs(
            resultado,
            objeto_esperado,
        )

    @patch(
        "app.concessionarias."
        "concessionarias_interface."
        "selecionar_concessionaria_por_codigo"
    )
    def test_selecionar_concessionaria_por_codigo(
        self,
        mock_selecionar,
    ):
        """
        Deve delegar a seleção por código
        para a camada de interface.
        """

        objeto_esperado = object()

        mock_selecionar.return_value = (
            objeto_esperado
        )

        resultado = (
            concessionarias
            .selecionar_concessionaria_por_codigo()
        )

        mock_selecionar.assert_called_once_with(
            concessionarias.concessionarias
        )

        self.assertIs(
            resultado,
            objeto_esperado,
        )

    @patch(
        "app.concessionarias."
        "concessionarias_interface."
        "adicionar_area_atuacao"
    )
    def test_adicionar_area_atuacao(
        self,
        mock_adicionar_area,
    ):
        """
        Deve delegar a inclusão da Área de Atuação
        para a camada de interface.
        """

        area_esperada = object()

        mock_adicionar_area.return_value = (
            area_esperada
        )

        resultado = (
            concessionarias
            .adicionar_area_atuacao()
        )

        mock_adicionar_area.assert_called_once_with(
            concessionarias.concessionarias
        )

        self.assertIs(
            resultado,
            area_esperada,
        )

    @patch(
        "app.concessionarias."
        "concessionarias_interface."
        "alterar_situacao_concessionaria"
    )
    def test_alterar_situacao_concessionaria(
        self,
        mock_alterar_situacao,
    ):
        """
        Deve delegar a alteração de situação
        para a camada de interface.
        """

        objeto_esperado = object()

        mock_alterar_situacao.return_value = (
            objeto_esperado
        )

        resultado = (
            concessionarias
            .alterar_situacao_concessionaria()
        )

        mock_alterar_situacao.assert_called_once_with(
            concessionarias.concessionarias
        )

        self.assertIs(
            resultado,
            objeto_esperado,
        )

    @patch(
        "app.concessionarias."
        "concessionarias_interface."
        "alterar_situacao_area_atuacao"
    )
    def test_alterar_situacao_area_atuacao(
        self,
        mock_alterar_area,
    ):
        """
        Deve delegar a alteração da Área de Atuação
        para a camada de interface.
        """

        area_esperada = object()

        mock_alterar_area.return_value = (
            area_esperada
        )

        resultado = (
            concessionarias
            .alterar_situacao_area_atuacao()
        )

        mock_alterar_area.assert_called_once_with(
            concessionarias.concessionarias
        )

        self.assertIs(
            resultado,
            area_esperada,
        )

    @patch(
        "app.concessionarias."
        "concessionarias_interface."
        "menu_concessionarias"
    )
    def test_abrir_menu_concessionarias(
        self,
        mock_menu,
    ):
        """
        Deve delegar a abertura do menu
        para a camada de interface.
        """

        concessionarias.abrir_menu_concessionarias()

        mock_menu.assert_called_once_with(
            concessionarias.concessionarias
        )

    def test_obter_concessionarias(self):
        """
        Deve retornar exatamente a lista
        mantida pela fachada.

        O assertIs verifica se o resultado
        e a lista interna são o mesmo objeto.
        """

        resultado = (
            concessionarias
            .obter_concessionarias()
        )

        self.assertIs(
            resultado,
            concessionarias.concessionarias,
        )


if __name__ == "__main__":
    unittest.main()