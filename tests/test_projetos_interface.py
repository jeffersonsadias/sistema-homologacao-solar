import unittest
from unittest.mock import patch

from app import status
from app.interface import projetos_interface


class TestProjetosInterface(unittest.TestCase):
    """
    Testes da camada de interface de Projetos.

    As entradas, saídas e persistência são simuladas
    para impedir interação real com o terminal
    e com o arquivo projetos.json.
    """

    def setUp(self):
        """
        Cria os dados utilizados antes
        da execução de cada teste.
        """

        self.lista_projetos = []

        self.cliente = {
            "codigo": 3,
            "nome": "Cliente Teste",
        }

    @patch(
        "app.interface.projetos_interface."
        "salvar_projetos"
    )
    @patch(
        "app.interface.projetos_interface."
        "criar_dados_projeto"
    )
    @patch(
        "app.interface.projetos_interface."
        "utils.ler_float"
    )
    @patch("builtins.input")
    @patch(
        "app.interface.projetos_interface."
        "clientes.selecionar_cliente"
    )
    def test_cadastrar_projeto(
        self,
        mock_selecionar_cliente,
        mock_input,
        mock_ler_float,
        mock_criar_dados_projeto,
        mock_salvar_projetos,
    ):
        """
        Deve cadastrar um Projeto e solicitar
        o salvamento da lista atualizada.
        """

        mock_selecionar_cliente.return_value = (
            self.cliente
        )

        mock_input.return_value = (
            "Neoenergia Coelba"
        )

        mock_ler_float.return_value = 5.5

        projeto_esperado = {
            "codigo": 1,
            "cliente": 3,
            "distribuidora": "Neoenergia Coelba",
            "potencia": 5.5,
            "status": status.STATUS_INICIAL,
        }

        mock_criar_dados_projeto.return_value = (
            projeto_esperado
        )

        projeto_criado = (
            projetos_interface.cadastrar_projeto(
                self.lista_projetos
            )
        )

        self.assertEqual(
            projeto_criado,
            projeto_esperado,
        )

        self.assertEqual(
            self.lista_projetos,
            [projeto_esperado],
        )

        mock_criar_dados_projeto.assert_called_once_with(
            codigo=1,
            codigo_cliente=3,
            distribuidora="Neoenergia Coelba",
            potencia=5.5,
            status_inicial=status.STATUS_INICIAL,
        )

        mock_salvar_projetos.assert_called_once_with(
            self.lista_projetos
        )

    @patch(
        "app.interface.projetos_interface."
        "salvar_projetos"
    )
    @patch(
        "app.interface.projetos_interface."
        "clientes.selecionar_cliente"
    )
    def test_cadastrar_projeto_sem_cliente(
        self,
        mock_selecionar_cliente,
        mock_salvar_projetos,
    ):
        """
        Não deve cadastrar Projeto quando
        nenhum Cliente for selecionado.
        """

        mock_selecionar_cliente.return_value = None

        resultado = (
            projetos_interface.cadastrar_projeto(
                self.lista_projetos
            )
        )

        self.assertIsNone(resultado)

        self.assertEqual(
            self.lista_projetos,
            [],
        )

        mock_salvar_projetos.assert_not_called()

    @patch("builtins.print")
    def test_listar_projetos_lista_vazia(
        self,
        mock_print,
    ):
        """
        Deve informar quando não houver
        Projetos cadastrados.
        """

        resultado = (
            projetos_interface.listar_projetos(
                self.lista_projetos
            )
        )

        self.assertIsNone(resultado)

        mock_print.assert_any_call(
            "Nenhum projeto cadastrado."
        )

    @patch(
        "app.interface.projetos_interface."
        "mostrar_projeto"
    )
    def test_listar_projetos(
        self,
        mock_mostrar_projeto,
    ):
        """
        Deve solicitar a exibição de todos
        os Projetos cadastrados.
        """

        projeto_1 = {
            "codigo": 1,
        }

        projeto_2 = {
            "codigo": 2,
        }

        self.lista_projetos.extend(
            [
                projeto_1,
                projeto_2,
            ]
        )

        projetos_interface.listar_projetos(
            self.lista_projetos
        )

        self.assertEqual(
            mock_mostrar_projeto.call_count,
            2,
        )

        mock_mostrar_projeto.assert_any_call(
            projeto_1
        )

        mock_mostrar_projeto.assert_any_call(
            projeto_2
        )

    @patch(
        "app.interface.projetos_interface."
        "salvar_projetos"
    )
    @patch(
        "app.interface.projetos_interface."
        "status.transicao_permitida"
    )
    @patch(
        "app.interface.projetos_interface."
        "status.obter_status"
    )
    @patch(
        "app.interface.projetos_interface."
        "status.exibir_status"
    )
    @patch(
        "app.interface.projetos_interface."
        "mostrar_projeto"
    )
    @patch(
        "app.interface.projetos_interface."
        "utils.ler_int"
    )
    def test_alterar_status(
        self,
        mock_ler_int,
        mock_mostrar_projeto,
        mock_exibir_status,
        mock_obter_status,
        mock_transicao_permitida,
        mock_salvar_projetos,
    ):
        """
        Deve alterar o status quando
        a transição for permitida.
        """

        projeto = {
            "codigo": 1,
            "cliente": 3,
            "distribuidora": "Neoenergia Coelba",
            "potencia": 5.5,
            "status": status.STATUS_INICIAL,
        }

        self.lista_projetos.append(projeto)

        mock_ler_int.side_effect = [
            1,
            2,
        ]

        novo_status = "Documentação recebida"

        mock_obter_status.return_value = (
            novo_status
        )

        mock_transicao_permitida.return_value = (
            True
        )

        resultado = (
            projetos_interface.alterar_status(
                self.lista_projetos
            )
        )

        self.assertIs(
            resultado,
            projeto,
        )

        self.assertEqual(
            projeto["status"],
            novo_status,
        )

        mock_mostrar_projeto.assert_called_once_with(
            projeto
        )

        mock_exibir_status.assert_called_once_with()

        mock_obter_status.assert_called_once_with(
            2
        )

        mock_transicao_permitida.assert_called_once_with(
            status.STATUS_INICIAL,
            novo_status,
        )

        mock_salvar_projetos.assert_called_once_with(
            self.lista_projetos
        )


if __name__ == "__main__":
    unittest.main()