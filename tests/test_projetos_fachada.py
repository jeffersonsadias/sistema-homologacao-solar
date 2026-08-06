import unittest
from unittest.mock import patch

from app import projetos


class TestProjetosFachada(unittest.TestCase):
    """
    Testes da fachada de compatibilidade de Projetos.

    A fachada deve encaminhar as operações para
    as camadas corretas, sempre utilizando a coleção
    global mantida por app.projetos.
    """

    def setUp(self):
        """
        Guarda a coleção original e utiliza
        uma lista vazia exclusiva para cada teste.
        """

        self.projetos_originais = projetos.projetos

        projetos.projetos = []

    def tearDown(self):
        """
        Restaura a coleção original após cada teste.
        """

        projetos.projetos = self.projetos_originais

    @patch(
        "app.projetos."
        "projetos_interface.cadastrar_projeto"
    )
    def test_cadastrar_projeto_encaminha_para_interface(
        self,
        mock_cadastrar_projeto,
    ):
        """
        Deve encaminhar o cadastro para a interface,
        utilizando a coleção mantida pela fachada.
        """

        projeto_esperado = {
            "codigo": 1,
        }

        mock_cadastrar_projeto.return_value = (
            projeto_esperado
        )

        resultado = projetos.cadastrar_projeto()

        mock_cadastrar_projeto.assert_called_once_with(
            projetos.projetos
        )

        self.assertEqual(
            resultado,
            projeto_esperado,
        )

    @patch(
        "app.projetos."
        "projetos_interface.listar_projetos"
    )
    def test_listar_projetos_encaminha_para_interface(
        self,
        mock_listar_projetos,
    ):
        """
        Deve encaminhar a listagem para a interface.
        """

        projetos.listar_projetos()

        mock_listar_projetos.assert_called_once_with(
            projetos.projetos
        )

    @patch(
        "app.projetos."
        "buscar_projeto_por_codigo"
    )
    def test_buscar_projeto_encaminha_para_dominio(
        self,
        mock_buscar_projeto_por_codigo,
    ):
        """
        Deve encaminhar a busca para o domínio.
        """

        projeto_esperado = {
            "codigo": 8,
        }

        mock_buscar_projeto_por_codigo.return_value = (
            projeto_esperado
        )

        resultado = projetos.buscar_projeto(8)

        mock_buscar_projeto_por_codigo.assert_called_once_with(
            projetos.projetos,
            8,
        )

        self.assertEqual(
            resultado,
            projeto_esperado,
        )

    @patch(
        "app.projetos."
        "buscar_por_cliente_no_dominio"
    )
    def test_buscar_projetos_do_cliente_encaminha_para_dominio(
        self,
        mock_buscar,
    ):
        """
        Deve encaminhar ao domínio a busca
        dos Projetos vinculados ao Cliente.
        """

        projetos_encontrados = [
            {
                "codigo": 1,
                "cliente": 10,
            },
            {
                "codigo": 2,
                "cliente": 10,
            },
        ]

        mock_buscar.return_value = (
            projetos_encontrados
        )

        resultado = (
            projetos.buscar_projetos_do_cliente(
                10
            )
        )

        mock_buscar.assert_called_once_with(
            projetos.projetos,
            10,
        )

        self.assertEqual(
            resultado,
            projetos_encontrados,
        )

    @patch(
        "app.projetos."
        "buscar_por_status_no_dominio"
    )
    def test_buscar_projetos_com_status_encaminha_para_dominio(
        self,
        mock_buscar,
    ):
        """
        Deve encaminhar ao domínio
        a busca dos Projetos por status.
        """

        projetos_encontrados = [
            {
                "codigo": 1,
                "status": "Aprovado",
            },
            {
                "codigo": 2,
                "status": "Aprovado",
            },
        ]

        mock_buscar.return_value = (
            projetos_encontrados
        )

        resultado = projetos.buscar_projetos_com_status(
            "Aprovado"
        )

        mock_buscar.assert_called_once_with(
            projetos.projetos,
            "Aprovado",
        )

        self.assertEqual(
            resultado,
            projetos_encontrados,
        )

    @patch(
            "app.projetos."
            "projetos_interface.mostrar_projeto"
        )
    def test_mostrar_projeto_encaminha_para_interface(
        self,
        mock_mostrar_projeto,
    ):
        """
        Deve encaminhar a exibição para a interface.
        """

        projeto = {
            "codigo": 1,
        }

        projetos.mostrar_projeto(projeto)

        mock_mostrar_projeto.assert_called_once_with(
            projeto
        )

    @patch(
        "app.projetos."
        "projetos_interface.alterar_status"
    )
    def test_alterar_status_encaminha_para_interface(
        self,
        mock_alterar_status,
    ):
        """
        Deve encaminhar a alteração de status
        para a interface.
        """

        projeto_alterado = {
            "codigo": 1,
            "status": "Em análise",
        }

        mock_alterar_status.return_value = (
            projeto_alterado
        )

        resultado = projetos.alterar_status()

        mock_alterar_status.assert_called_once_with(
            projetos.projetos
        )

        self.assertEqual(
            resultado,
            projeto_alterado,
        )

    def test_quantidade_projetos(self):
        """
        Deve retornar a quantidade de Projetos cadastrados.
        """

        projetos.projetos = [
            {"codigo": 1},
            {"codigo": 2},
            {"codigo": 3},
        ]

        resultado = projetos.quantidade_projetos()

        self.assertEqual(
            resultado,
            3,
        )


if __name__ == "__main__":
    unittest.main()