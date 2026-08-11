import unittest
from unittest.mock import patch

from app import projetos
from app.dominio import status


class TestConversaoOrcamentoProjeto(unittest.TestCase):
    """
    Testes da criação de Projetos a partir
    de um Orçamento aprovado.
    """

    def setUp(self):
        """
        Executado antes de cada teste.

        Guarda a lista original de Projetos
        e cria uma lista vazia exclusiva para o teste.
        """

        self.projetos_originais = projetos.projetos

        projetos.projetos = []

        self.orcamento_aprovado = {
            "codigo": 10,
            "codigo_empresa": 50,
            "codigo_concessionaria": 20,
            "cliente": 3,
            "dimensionamento": {
                "consumo_medio_kwh": 650.0,
                "potencia_prevista_kwp": 5.5,
            },

            "modulos": {
                "quantidade": 10,
                "fabricante": "Canadian Solar",
            },

            "inversores": {
                "quantidade": 1,
                "fabricante": "Growatt",
                "tensao": "220 V",
            },

            "local_instalacao": {
                "codigo_uc": "123456789",
                "distribuidora": "Neoenergia Coelba",
                "tipo_telhado": "Cerâmico",
            },

            "comercial": {
                "valor_total": 23000.00,
                "validade_dias": 10,
                "prazo_instalacao_dias": 45,
            },

            "status": "Aprovado",
        }

    def tearDown(self):
        """
        Executado após cada teste.

        Restaura a lista original para impedir
        interferência entre os testes.
        """

        projetos.projetos = self.projetos_originais

    @patch("app.projetos.salvar_projetos")
    def test_deve_criar_projeto_a_partir_do_orcamento(
        self,
        mock_salvar_projetos,
    ):
        """
        Deve criar um novo Projeto utilizando
        as informações do Orçamento aprovado.
        """

        projeto_criado = (
            projetos.criar_projeto_a_partir_do_orcamento(
                self.orcamento_aprovado
            )
        )

        self.assertIsNotNone(projeto_criado)

        self.assertEqual(
            projeto_criado["codigo"],
            1,
        )

        self.assertEqual(
            projeto_criado["codigo_empresa"],
            50,
        )

        self.assertEqual(
            projeto_criado["codigo_concessionaria"],
            20,
        )

        self.assertEqual(
            projeto_criado["cliente"],
            3,
        )

        self.assertEqual(
            projeto_criado["orcamento_origem"],
            10,
        )

        self.assertEqual(
            projeto_criado["potencia"],
            5.5,
        )

        self.assertEqual(
            projeto_criado["distribuidora"],
            "Neoenergia Coelba",
        )

        self.assertEqual(
            projeto_criado["codigo_uc"],
            "123456789",
        )

        self.assertEqual(
            projeto_criado["tipo_telhado"],
            "Cerâmico",
        )

        self.assertEqual(
            projeto_criado["status"],
            status.STATUS_INICIAL,
        )

        self.assertEqual(
            len(projetos.projetos),
            1,
        )

        mock_salvar_projetos.assert_called_once_with(
            projetos.projetos
        )

    @patch("app.projetos.salvar_projetos")
    def test_projeto_deve_receber_copia_dos_equipamentos(
        self,
        mock_salvar_projetos,
    ):
        """
        Verifica se módulos e inversores são copiados
        e não compartilham a mesma referência do Orçamento.
        """

        projeto_criado = (
            projetos.criar_projeto_a_partir_do_orcamento(
                self.orcamento_aprovado
            )
        )

        projeto_criado["modulos"]["fabricante"] = (
            "Outro Fabricante"
        )

        projeto_criado["inversores"]["tensao"] = (
            "380 V"
        )

        self.assertEqual(
            self.orcamento_aprovado["modulos"]["fabricante"],
            "Canadian Solar",
        )

        self.assertEqual(
            self.orcamento_aprovado["inversores"]["tensao"],
            "220 V",
        )

        self.assertIsNot(
            projeto_criado["modulos"],
            self.orcamento_aprovado["modulos"],
        )

        self.assertIsNot(
            projeto_criado["inversores"],
            self.orcamento_aprovado["inversores"],
        )

        mock_salvar_projetos.assert_called_once_with(
            projetos.projetos
        )


if __name__ == "__main__":
    unittest.main()