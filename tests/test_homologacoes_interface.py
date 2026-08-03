"""
Testes da interface de terminal de Homologações.

As funções da fachada e as entradas do terminal são
simuladas para impedir alterações nos dados reais.
"""

import unittest
from unittest.mock import patch

from app.interface import homologacoes_interface


class TestHomologacoesInterface(
    unittest.TestCase
):
    """
    Testes dos fluxos iniciais da interface.
    """

    @patch(
        "app.interface.homologacoes_interface."
        "_exibir_homologacao"
    )
    @patch(
        "app.interface.homologacoes_interface."
        "homologacoes.criar_homologacao"
    )
    @patch(
        "app.interface.homologacoes_interface."
        "ler_int",
        side_effect=[
            1,
            10,
            2,
        ],
    )
    @patch(
        "builtins.input",
        side_effect=[
            "2026-08-03",
            "Ana Lima",
            "Processo inicial.",
        ],
    )
    def test_cadastrar_homologacao(
        self,
        mock_input,
        mock_ler_int,
        mock_criar,
        mock_exibir,
    ):
        homologacao_criada = {
            "codigo": 1,
        }

        mock_criar.return_value = (
            homologacao_criada
        )

        (
            homologacoes_interface
            .cadastrar_homologacao_interface()
        )

        mock_criar.assert_called_once_with(
            codigo_empresa=1,
            codigo_projeto=10,
            codigo_concessionaria=2,
            data_abertura="2026-08-03",
            responsavel_abertura="Ana Lima",
            observacoes="Processo inicial.",
        )

        mock_exibir.assert_called_once_with(
            homologacao_criada
        )

    @patch(
        "builtins.print"
    )
    @patch(
        "app.interface.homologacoes_interface."
        "homologacoes.criar_homologacao",
        side_effect=ValueError(
            "Projeto já possui Homologação."
        ),
    )
    @patch(
        "app.interface.homologacoes_interface."
        "ler_int",
        side_effect=[
            1,
            10,
            2,
        ],
    )
    @patch(
        "builtins.input",
        side_effect=[
            "2026-08-03",
            "Ana Lima",
            "",
        ],
    )
    def test_cadastro_invalido_exibe_erro(
        self,
        mock_input,
        mock_ler_int,
        mock_criar,
        mock_print,
    ):
        (
            homologacoes_interface
            .cadastrar_homologacao_interface()
        )

        mock_print.assert_any_call(
            "\nNão foi possível criar a Homologação: "
            "Projeto já possui Homologação."
        )

    @patch(
        "app.interface.homologacoes_interface."
        "_exibir_homologacao"
    )
    @patch(
        "app.interface.homologacoes_interface."
        "homologacoes.listar_homologacoes"
    )
    @patch(
        "app.interface.homologacoes_interface."
        "ler_int",
        return_value=1,
    )
    def test_listar_homologacoes(
        self,
        mock_ler_int,
        mock_listar,
        mock_exibir,
    ):
        primeira = {
            "codigo": 1,
        }

        segunda = {
            "codigo": 2,
        }

        mock_listar.return_value = [
            primeira,
            segunda,
        ]

        (
            homologacoes_interface
            .listar_homologacoes_interface()
        )

        mock_listar.assert_called_once_with(
            codigo_empresa=1,
        )

        self.assertEqual(
            mock_exibir.call_count,
            2,
        )

        mock_exibir.assert_any_call(
            primeira
        )

        mock_exibir.assert_any_call(
            segunda
        )

    @patch(
        "builtins.print"
    )
    @patch(
        "app.interface.homologacoes_interface."
        "homologacoes.listar_homologacoes",
        return_value=[],
    )
    @patch(
        "app.interface.homologacoes_interface."
        "ler_int",
        return_value=1,
    )
    def test_listar_sem_homologacoes(
        self,
        mock_ler_int,
        mock_listar,
        mock_print,
    ):
        (
            homologacoes_interface
            .listar_homologacoes_interface()
        )

        mock_print.assert_any_call(
            "\nNenhuma Homologação encontrada "
            "para esta Empresa."
        )

    @patch(
        "app.interface.homologacoes_interface."
        "_exibir_homologacao"
    )
    @patch(
        "app.interface.homologacoes_interface."
        "homologacoes.buscar_homologacao"
    )
    @patch(
        "app.interface.homologacoes_interface."
        "ler_int",
        side_effect=[
            1,
            5,
        ],
    )
    def test_buscar_homologacao(
        self,
        mock_ler_int,
        mock_buscar,
        mock_exibir,
    ):
        homologacao_encontrada = {
            "codigo": 5,
        }

        mock_buscar.return_value = (
            homologacao_encontrada
        )

        (
            homologacoes_interface
            .buscar_homologacao_interface()
        )

        mock_buscar.assert_called_once_with(
            codigo_homologacao=5,
            codigo_empresa=1,
        )

        mock_exibir.assert_called_once_with(
            homologacao_encontrada
        )

    @patch(
        "builtins.print"
    )
    @patch(
        "app.interface.homologacoes_interface."
        "homologacoes.buscar_homologacao",
        return_value=None,
    )
    @patch(
        "app.interface.homologacoes_interface."
        "ler_int",
        side_effect=[
            1,
            999,
        ],
    )
    def test_buscar_homologacao_inexistente(
        self,
        mock_ler_int,
        mock_buscar,
        mock_print,
    ):
        (
            homologacoes_interface
            .buscar_homologacao_interface()
        )

        mock_print.assert_any_call(
            "\nHomologação não encontrada."
        )

    @patch(
        "app.interface.homologacoes_interface."
        "cadastrar_homologacao_interface"
    )
    @patch(
        "app.interface.homologacoes_interface."
        "_pausar"
    )
    @patch(
        "builtins.input",
        side_effect=[
            "1",
            "0",
        ],
    )
    def test_menu_deve_abrir_cadastro(
        self,
        mock_input,
        mock_pausar,
        mock_cadastrar,
    ):
        homologacoes_interface.menu_homologacoes()

        mock_cadastrar.assert_called_once_with()
        mock_pausar.assert_called_once_with()

    @patch(
        "app.interface.homologacoes_interface."
        "listar_homologacoes_interface"
    )
    @patch(
        "app.interface.homologacoes_interface."
        "_pausar"
    )
    @patch(
        "builtins.input",
        side_effect=[
            "2",
            "0",
        ],
    )
    def test_menu_deve_abrir_listagem(
        self,
        mock_input,
        mock_pausar,
        mock_listar,
    ):
        homologacoes_interface.menu_homologacoes()

        mock_listar.assert_called_once_with()

    @patch(
        "app.interface.homologacoes_interface."
        "buscar_homologacao_interface"
    )
    @patch(
        "app.interface.homologacoes_interface."
        "_pausar"
    )
    @patch(
        "builtins.input",
        side_effect=[
            "3",
            "0",
        ],
    )
    def test_menu_deve_abrir_busca(
        self,
        mock_input,
        mock_pausar,
        mock_buscar,
    ):
        homologacoes_interface.menu_homologacoes()

        mock_buscar.assert_called_once_with()


if __name__ == "__main__":
    unittest.main()