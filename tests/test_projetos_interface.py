import unittest
from unittest.mock import Mock, patch

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
    @patch(
        "app.interface.projetos_interface."
        "clientes.selecionar_cliente"
    )
    @patch(
        "app.interface.projetos_interface."
        "_selecionar_concessionaria_projeto"
    )
    @patch(
        "app.interface.projetos_interface."
        "_selecionar_empresa_projeto"
    )
    def test_cadastrar_projeto(
        self,
        mock_selecionar_empresa,
        mock_selecionar_concessionaria,
        mock_selecionar_cliente,
        mock_ler_float,
        mock_criar_dados_projeto,
        mock_salvar_projetos,
    ):
        """
        Deve cadastrar um Projeto e solicitar
        o salvamento da lista atualizada.
        """

        empresa = {
            "codigo": 50,
            "nome": "Solar Alfa",
        }

        mock_selecionar_empresa.return_value = (
            empresa
        )

        concessionaria = Mock()
        concessionaria.codigo = 20
        concessionaria.nome = "Neoenergia Coelba"

        mock_selecionar_concessionaria.return_value = (
            concessionaria
        )

        mock_selecionar_cliente.return_value = (
            self.cliente
        )

        mock_ler_float.return_value = 5.5

        projeto_esperado = {
            "codigo": 1,
            "codigo_empresa": 50,
            "codigo_concessionaria": 20,
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
            codigo_empresa=50,
            codigo_concessionaria=20,
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
        "clientes.selecionar_cliente"
    )
    @patch(
        "app.interface.projetos_interface."
        "_selecionar_empresa_projeto",
        return_value=None,
    )
    def test_cadastrar_projeto_sem_empresa(
        self,
        mock_selecionar_empresa,
        mock_selecionar_cliente,
    ):
        """
        Não deve continuar o cadastro
        quando não houver Empresa válida.
        """

        resultado = (
            projetos_interface
            .cadastrar_projeto(
                self.lista_projetos
            )
        )

        self.assertIsNone(
            resultado
        )

        self.assertEqual(
            self.lista_projetos,
            [],
        )

        mock_selecionar_cliente.assert_not_called()

    @patch(
        "app.interface.projetos_interface."
        "salvar_projetos"
    )
    @patch(
        "app.interface.projetos_interface."
        "clientes.selecionar_cliente"
    )
    @patch(
        "app.interface.projetos_interface."
        "_selecionar_empresa_projeto",
        return_value={
            "codigo": 50,
            "nome": "Solar Alfa",
        },
    )
    def test_cadastrar_projeto_sem_cliente(
        self,
        mock_selecionar_empresa,
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

    @patch(
        "app.interface.projetos_interface."
        "utils.gerar_proximo_codigo"
    )
    @patch(
        "app.interface.projetos_interface."
        "_selecionar_concessionaria_projeto",
        return_value=None,
    )
    @patch(
        "app.interface.projetos_interface."
        "clientes.selecionar_cliente",
        return_value={
            "codigo": 3,
            "nome": "Cliente Teste",
        },
    )
    @patch(
        "app.interface.projetos_interface."
        "_selecionar_empresa_projeto",
        return_value={
            "codigo": 50,
            "nome": "Solar Alfa",
        },
    )
    def test_cadastrar_projeto_sem_concessionaria(
        self,
        mock_selecionar_empresa,
        mock_selecionar_cliente,
        mock_selecionar_concessionaria,
        mock_gerar_codigo,
    ):
        """
        Não deve cadastrar Projeto quando
        nenhuma Concessionária válida for selecionada.
        """

        resultado = (
            projetos_interface.cadastrar_projeto(
                self.lista_projetos
            )
        )

        self.assertIsNone(
            resultado
        )

        self.assertEqual(
            self.lista_projetos,
            [],
        )

        mock_gerar_codigo.assert_not_called()

    @patch(
        "app.interface.projetos_interface."
        "empresas.empresa_esta_ativa",
        return_value=True,
    )
    @patch(
        "app.interface.projetos_interface."
        "empresas.obter_empresa"
    )
    @patch(
        "app.interface.projetos_interface."
        "utils.ler_int",
        return_value=10,
    )
    def test_selecionar_empresa_projeto(
        self,
        mock_ler_int,
        mock_obter_empresa,
        mock_empresa_ativa,
    ):
        empresa = {
            "codigo": 10,
            "nome": "Solar Alfa",
        }

        mock_obter_empresa.return_value = (
            empresa
        )

        resultado = (
            projetos_interface
            ._selecionar_empresa_projeto()
        )

        self.assertIs(
            resultado,
            empresa,
        )

        mock_obter_empresa.assert_called_once_with(
            10
        )

        mock_empresa_ativa.assert_called_once_with(
            10
        )

    @patch(
        "app.interface.projetos_interface."
        "empresas.empresa_esta_ativa",
        return_value=False,
    )
    @patch(
        "app.interface.projetos_interface."
        "empresas.obter_empresa",
        return_value={
            "codigo": 10,
        },
    )
    @patch(
        "app.interface.projetos_interface."
        "utils.ler_int",
        return_value=10,
    )
    def test_nao_deve_selecionar_empresa_inativa(
        self,
        mock_ler_int,
        mock_obter_empresa,
        mock_empresa_ativa,
    ):
        resultado = (
            projetos_interface
            ._selecionar_empresa_projeto()
        )

        self.assertIsNone(
            resultado
        )

    @patch(
        "app.interface.projetos_interface."
        "concessionarias.obter_concessionaria"
    )
    @patch(
        "app.interface.projetos_interface."
        "utils.ler_int",
        return_value=20,
    )
    def test_selecionar_concessionaria_projeto(
        self,
        mock_ler_int,
        mock_obter_concessionaria,
    ):
        concessionaria = Mock()
        concessionaria.codigo = 20
        concessionaria.nome = "Neoenergia Coelba"

        mock_obter_concessionaria.return_value = (
            concessionaria
        )

        resultado = (
            projetos_interface
            ._selecionar_concessionaria_projeto()
        )

        self.assertIs(
            resultado,
            concessionaria,
        )

        mock_obter_concessionaria.assert_called_once_with(
            20
        )

    @patch("builtins.print")
    @patch(
        "app.interface.projetos_interface."
        "concessionarias.obter_concessionaria",
        side_effect=ValueError(
            "Concessionária não encontrada."
        ),
    )
    @patch(
        "app.interface.projetos_interface."
        "utils.ler_int",
        return_value=20,
    )
    def test_nao_deve_selecionar_concessionaria_inexistente(
        self,
        mock_ler_int,
        mock_obter_concessionaria,
        mock_print,
    ):
        resultado = (
            projetos_interface
            ._selecionar_concessionaria_projeto()
        )

        self.assertIsNone(
            resultado
        )

        mock_obter_concessionaria.assert_called_once_with(
            20
        )

        mock_print.assert_any_call(
            "\nNão foi possível selecionar "
            "a Concessionária: "
            "Concessionária não encontrada."
        )

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