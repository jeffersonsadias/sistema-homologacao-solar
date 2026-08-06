import unittest

from app.dominio.projetos import (
    buscar_projeto_por_codigo,
    buscar_projetos_por_cliente,
    buscar_projetos_por_status,
    codigo_projeto_existe,
    criar_dados_projeto,
    criar_dados_projeto_a_partir_do_orcamento,
    quantidade_projetos_por_status,
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

    def test_buscar_projetos_por_cliente(
        self,
    ):
        """
        Deve retornar somente os Projetos
        pertencentes ao Cliente informado.
        """

        resultado = buscar_projetos_por_cliente(
            self.projetos,
            10,
        )

        self.assertEqual(
            len(resultado),
            1,
        )

        self.assertEqual(
            resultado[0]["codigo"],
            1,
        )

    def test_buscar_projetos_por_cliente_sem_resultados(
        self,
    ):
        """
        Deve retornar uma lista vazia quando o Cliente
        não possuir Projetos.
        """

        resultado = buscar_projetos_por_cliente(
            self.projetos,
            999,
        )

        self.assertEqual(
            resultado,
            [],
        )

    def test_buscar_varios_projetos_do_mesmo_cliente(
        self,
    ):
        """
        Deve retornar todos os Projetos
        vinculados ao mesmo Cliente.
        """

        self.projetos.append(
            {
                "codigo": 3,
                "cliente": 10,
                "distribuidora": "Neoenergia Coelba",
                "potencia": 12.0,
                "status": "Aprovado",
            }
        )

        resultado = buscar_projetos_por_cliente(
            self.projetos,
            10,
        )

        self.assertEqual(
            len(resultado),
            2,
        )

        self.assertEqual(
            [
                projeto["codigo"]
                for projeto in resultado
            ],
            [
                1,
                3,
            ],
        )

    def test_busca_por_cliente_nao_deve_alterar_projetos(
        self,
    ):
        """
        A consulta não deve modificar
        a coleção recebida.
        """

        projetos_antes = [
            projeto.copy()
            for projeto in self.projetos
        ]

        buscar_projetos_por_cliente(
            self.projetos,
            10,
        )

        self.assertEqual(
            self.projetos,
            projetos_antes,
        )

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

    def test_quantidade_projetos_por_status(self):
        """
        Deve contar somente os Projetos
        com o status informado.
        """

        quantidade = quantidade_projetos_por_status(
            self.projetos,
            "Aguardando documentação",
        )

        self.assertEqual(
            quantidade,
            1,
        )

    def test_quantidade_projetos_por_status_inexistente(self):
        """
        Deve retornar zero quando nenhum Projeto
        possuir o status informado.
        """

        quantidade = quantidade_projetos_por_status(
            self.projetos,
            "Homologado",
        )

        self.assertEqual(
            quantidade,
            0,
        )

    def test_contagem_por_status_nao_deve_alterar_projetos(self):
        """
        A consulta não deve modificar a coleção recebida.
        """

        projetos_antes = [
            projeto.copy()
            for projeto in self.projetos
        ]

        quantidade_projetos_por_status(
            self.projetos,
            "Aguardando documentação",
        )

        self.assertEqual(
            self.projetos,
            projetos_antes,
        )

    def test_buscar_projetos_por_status(
        self,
    ):
        """
        Deve retornar somente os Projetos
        que possuem o status informado.
        """

        resultado = buscar_projetos_por_status(
            self.projetos,
            "Aguardando documentação",
        )

        self.assertEqual(
            len(resultado),
            1,
        )

        self.assertEqual(
            resultado[0]["codigo"],
            1,
        )

    def test_buscar_projetos_por_status_sem_resultados(
        self,
    ):
        """
        Deve retornar uma lista vazia quando não houver
        Projetos com o status informado.
        """

        resultado = buscar_projetos_por_status(
            self.projetos,
            "Homologado",
        )

        self.assertEqual(
            resultado,
            [],
        )

    def test_busca_de_projetos_por_status_nao_deve_alterar_colecao(
        self,
    ):
        """
        A consulta não deve modificar
        os Projetos recebidos.
        """

        projetos_antes = [
            projeto.copy()
            for projeto in self.projetos
        ]

        buscar_projetos_por_status(
            self.projetos,
            "Aguardando documentação",
        )

        self.assertEqual(
            self.projetos,
            projetos_antes,
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