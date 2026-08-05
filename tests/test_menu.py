import unittest
from unittest.mock import patch

from app import menu


class TestMenuPrincipal(
    unittest.TestCase
):
    """
    Testes do menu principal
    do Sistema de Homologação Solar.

    Os módulos chamados pelo menu são simulados
    para que os testes não cadastrem, alterem
    ou salvem dados reais.
    """

    @patch(
        "app.menu."
        "concessionarias."
        "abrir_menu_concessionarias"
    )
    @patch(
        "builtins.input",
        side_effect=[
            "13",
            "0",
        ],
    )
    def test_abrir_menu_concessionarias(
        self,
        mock_input,
        mock_abrir_menu,
    ):
        """
        A opção 13 deve abrir
        o menu de Concessionárias.
        """

        menu.executar_menu()

        mock_abrir_menu.assert_called_once_with()

    @patch(
        "app.menu."
        "unidades_consumidoras."
        "abrir_menu_unidades_consumidoras"
    )
    @patch(
        "app.menu."
        "concessionarias."
        "obter_concessionarias"
    )
    @patch(
        "builtins.input",
        side_effect=[
            "14",
            "0",
        ],
    )
    def test_abrir_menu_unidades_consumidoras(
        self,
        mock_input,
        mock_obter_concessionarias,
        mock_abrir_menu_unidades,
    ):
        """
        A opção 14 deve obter as Concessionárias
        pela função pública da fachada e enviar
        a lista ao menu de Unidades Consumidoras.
        """

        lista_concessionarias = [
            object(),
        ]

        mock_obter_concessionarias.return_value = (
            lista_concessionarias
        )

        menu.executar_menu()

        (
            mock_obter_concessionarias
            .assert_called_once_with()
        )

        (
            mock_abrir_menu_unidades
            .assert_called_once_with(
                lista_concessionarias
            )
        )

    @patch(
        "app.menu."
        "vinculos_unidade_projeto_interface."
        "menu_vinculos_unidade_projeto"
    )
    @patch(
        "builtins.input",
        side_effect=[
            "15",
            "0",
        ],
    )
    def test_abrir_menu_vinculos_unidade_projeto(
        self,
        mock_input,
        mock_abrir_menu_vinculos,
    ):
        """
        A opção 15 deve abrir
        o menu de vínculos entre
        Projetos e Unidades Consumidoras.
        """

        menu.executar_menu()

        (
            mock_abrir_menu_vinculos
            .assert_called_once_with()
        )

    @patch(
        "app.menu."
        "empresas_interface."
        "menu_empresas"
    )
    @patch(
        "builtins.input",
        side_effect=[
            "16",
            "0",
        ],
    )
    def test_abrir_menu_empresas(
        self,
        mock_input,
        mock_menu_empresas,
    ):
        """
        A opção 16 deve abrir
        o menu de Empresas.
        """

        menu.executar_menu()

        (
            mock_menu_empresas
            .assert_called_once_with()
        )

    @patch(
        "app.menu."
        "homologacoes_interface."
        "menu_homologacoes"
    )
    @patch(
        "builtins.input",
        side_effect=[
            "18",
            "0",
        ],
    )
    def test_abrir_menu_homologacoes(
        self,
        mock_input,
        mock_menu_homologacoes,
    ):
        """
        A opção 18 deve abrir
        o menu de Homologações.
        """

        menu.executar_menu()

        (
            mock_menu_homologacoes
            .assert_called_once_with()
        )

    @patch(
        "app.menu."
        "painel_operacional_interface."
        "exibir_painel_operacional"
    )
    @patch(
        "builtins.input",
        side_effect=[
            "19",
            "0",
        ],
    )
    def test_abrir_painel_operacional(
        self,
        mock_input,
        mock_exibir_painel,
    ):
        """
        A opção 19 deve abrir
        o Painel Operacional.
        """

        menu.executar_menu()

        (
            mock_exibir_painel
            .assert_called_once_with()
        )

    @patch(
        "app.menu."
        "clientes."
        "cadastrar_cliente"
    )
    @patch(
        "builtins.input",
        side_effect=[
            "1",
            "0",
        ],
    )
    def test_cadastrar_cliente(
        self,
        mock_input,
        mock_cadastrar_cliente,
    ):
        """
        A opção 1 deve delegar o cadastro
        para a fachada de Clientes.
        """

        menu.executar_menu()

        (
            mock_cadastrar_cliente
            .assert_called_once_with()
        )

    @patch(
        "app.menu."
        "projetos."
        "alterar_status"
    )
    @patch(
        "builtins.input",
        side_effect=[
            "7",
            "0",
        ],
    )
    def test_alterar_status_projeto(
        self,
        mock_input,
        mock_alterar_status,
    ):
        """
        A opção 7 deve delegar a alteração
        de status para a fachada de Projetos.
        """

        menu.executar_menu()

        (
            mock_alterar_status
            .assert_called_once_with()
        )

    @patch(
        "app.menu."
        "orcamentos."
        "converter_para_projeto"
    )
    @patch(
        "builtins.input",
        side_effect=[
            "12",
            "0",
        ],
    )
    def test_converter_orcamento_para_projeto(
        self,
        mock_input,
        mock_converter,
    ):
        """
        A opção 12 deve delegar a conversão
        para a fachada de Orçamentos.
        """

        menu.executar_menu()

        mock_converter.assert_called_once_with()

    @patch(
        "builtins.print"
    )
    @patch(
        "builtins.input",
        return_value="0",
    )
    def test_encerrar_menu(
        self,
        mock_input,
        mock_print,
    ):
        """
        A opção 0 deve encerrar
        a execução do menu.
        """

        menu.executar_menu()

        mock_print.assert_any_call(
            "\nSaindo do sistema..."
        )

    @patch(
        "builtins.print"
    )
    @patch(
        "builtins.input",
        side_effect=[
            "99",
            "0",
        ],
    )
    def test_opcao_invalida(
        self,
        mock_input,
        mock_print,
    ):
        """
        Uma opção desconhecida deve exibir
        a mensagem de opção inválida.
        """

        menu.executar_menu()

        mock_print.assert_any_call(
            "\nOpção inválida."
        )


if __name__ == "__main__":
    unittest.main()