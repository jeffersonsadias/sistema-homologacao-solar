import unittest

from app.dominio.projetos import (
    buscar_projeto_por_codigo,
    codigo_projeto_existe,
    criar_dados_projeto,
    criar_dados_projeto_a_partir_do_orcamento,
)


class TestProjetosDominio(unittest.TestCase):
    """
    Testes das regras puras do domínio de Projetos.
    """

    def setUp(self):
        """
        Cria dados novos antes de cada teste.
        """

        self.projetos = [
            {
                "codigo": 1,
                "cliente": 10,
                "distribuidora": "Neoenergia Coelba",
                "potencia": 5.5,
                "status": "Aguardando documentação",
            },
            {
                "codigo": 2,
                "cliente": 20,
                "distribuidora": "Neoenergia Coelba",
                "potencia": 8.0,
                "status": "Em análise",
            },
        ]

        self.orcamento = {
            "codigo": 15,
            "cliente": 10,
            "local_instalacao": {
                "distribuidora": "Neoenergia Coelba",
                "codigo_uc": "123456789",
                "tipo_telhado": "Cerâmico",
            },
            "dimensionamento": {
                "potencia_prevista_kwp": 6.6,
            },
            "modulos": [
                {
                    "fabricante": "Fabricante Solar",
                    "quantidade": 12,
                }
            ],
            "inversores": [
                {
                    "fabricante": "Fabricante Inversor",
                    "quantidade": 1,
                }
            ],
        }

    def test_buscar_projeto_por_codigo_existente(self):
        """
        Deve retornar o Projeto correspondente ao código.
        """

        projeto = buscar_projeto_por_codigo(
            self.projetos,
            2,
        )

        self.assertIsNotNone(projeto)
        self.assertEqual(projeto["cliente"], 20)

    def test_buscar_projeto_por_codigo_inexistente(self):
        """
        Deve retornar None quando o código não existir.
        """

        projeto = buscar_projeto_por_codigo(
            self.projetos,
            999,
        )

        self.assertIsNone(projeto)

    def test_codigo_projeto_existe(self):
        """
        Deve informar corretamente se o código existe.
        """

        self.assertTrue(
            codigo_projeto_existe(
                self.projetos,
                1,
            )
        )

        self.assertFalse(
            codigo_projeto_existe(
                self.projetos,
                999,
            )
        )

    def test_criar_dados_projeto(self):
        """
        Deve criar os dados básicos de um Projeto.
        """

        projeto = criar_dados_projeto(
            codigo=3,
            codigo_cliente=30,
            distribuidora="Neoenergia Coelba",
            potencia=10.5,
            status_inicial="Aguardando documentação",
        )

        self.assertEqual(projeto["codigo"], 3)
        self.assertEqual(projeto["cliente"], 30)
        self.assertEqual(
            projeto["distribuidora"],
            "Neoenergia Coelba",
        )
        self.assertEqual(projeto["potencia"], 10.5)
        self.assertEqual(
            projeto["status"],
            "Aguardando documentação",
        )

    def test_criar_projeto_a_partir_do_orcamento(self):
        """
        Deve criar os dados do Projeto usando o Orçamento.
        """

        projeto = criar_dados_projeto_a_partir_do_orcamento(
            codigo=3,
            orcamento=self.orcamento,
            status_inicial="Aguardando documentação",
        )

        self.assertEqual(projeto["codigo"], 3)
        self.assertEqual(projeto["cliente"], 10)
        self.assertEqual(projeto["orcamento_origem"], 15)

        self.assertEqual(
            projeto["distribuidora"],
            "Neoenergia Coelba",
        )

        self.assertEqual(projeto["potencia"], 6.6)
        self.assertEqual(projeto["codigo_uc"], "123456789")
        self.assertEqual(projeto["tipo_telhado"], "Cerâmico")

    def test_projeto_recebe_copia_dos_modulos(self):
        """
        A lista de módulos do Projeto não deve ser
        a mesma lista do Orçamento.
        """

        projeto = criar_dados_projeto_a_partir_do_orcamento(
            codigo=3,
            orcamento=self.orcamento,
            status_inicial="Aguardando documentação",
        )

        self.assertIsNot(
            projeto["modulos"],
            self.orcamento["modulos"],
        )

        self.assertEqual(
            projeto["modulos"],
            self.orcamento["modulos"],
        )

    def test_projeto_recebe_copia_dos_inversores(self):
        """
        A lista de inversores do Projeto não deve ser
        a mesma lista do Orçamento.
        """

        projeto = criar_dados_projeto_a_partir_do_orcamento(
            codigo=3,
            orcamento=self.orcamento,
            status_inicial="Aguardando documentação",
        )

        self.assertIsNot(
            projeto["inversores"],
            self.orcamento["inversores"],
        )

        self.assertEqual(
            projeto["inversores"],
            self.orcamento["inversores"],
        )


if __name__ == "__main__":
    unittest.main()