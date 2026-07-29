import unittest

from app.dominio.orcamentos import (
    buscar_orcamento_por_codigo,
    codigo_orcamento_existe,
    criar_dados_orcamento,
    orcamento_pode_ser_convertido,
)


class TestOrcamentosDominio(unittest.TestCase):
    """
    Testes das regras puras do domínio
    de Orçamentos.
    """

    def setUp(self):
        """
        Cria dados reutilizados pelos testes.
        """

        self.orcamentos = [
            {
                "codigo": 1,
                "cliente": 10,
                "status": "Em negociação",
            },
            {
                "codigo": 2,
                "cliente": 20,
                "status": "Aprovado",
            },
        ]

    def test_buscar_orcamento_existente(self):
        """
        Deve retornar o Orçamento correspondente
        ao código informado.
        """

        resultado = buscar_orcamento_por_codigo(
            self.orcamentos,
            2,
        )

        self.assertEqual(
            resultado,
            self.orcamentos[1],
        )

    def test_buscar_orcamento_inexistente(self):
        """
        Deve retornar None quando o código
        não for encontrado.
        """

        resultado = buscar_orcamento_por_codigo(
            self.orcamentos,
            99,
        )

        self.assertIsNone(resultado)

    def test_codigo_orcamento_existe(self):
        """
        Deve informar corretamente se o código existe.
        """

        self.assertTrue(
            codigo_orcamento_existe(
                self.orcamentos,
                1,
            )
        )

        self.assertFalse(
            codigo_orcamento_existe(
                self.orcamentos,
                99,
            )
        )

    def test_criar_dados_orcamento(self):
        """
        Deve criar os dados completos
        de um novo Orçamento.
        """

        dimensionamento = {
            "consumo_medio_kwh": 650.0,
            "potencia_prevista_kwp": 5.5,
        }

        modulos = {
            "quantidade": 10,
            "fabricante": "Canadian Solar",
        }

        inversores = {
            "quantidade": 1,
            "fabricante": "Growatt",
            "tensao": "220 V",
        }

        local_instalacao = {
            "codigo_uc": "123456789",
            "distribuidora": "Neoenergia Coelba",
            "tipo_telhado": "Cerâmico",
        }

        comercial = {
            "valor_total": 23000.00,
            "validade_dias": 10,
            "prazo_instalacao_dias": 45,
        }

        resultado = criar_dados_orcamento(
            codigo=1,
            codigo_cliente=3,
            dimensionamento=dimensionamento,
            modulos=modulos,
            inversores=inversores,
            local_instalacao=local_instalacao,
            comercial=comercial,
            status_inicial="Em negociação",
        )

        self.assertEqual(
            resultado["codigo"],
            1,
        )

        self.assertEqual(
            resultado["cliente"],
            3,
        )

        self.assertEqual(
            resultado["status"],
            "Em negociação",
        )

        self.assertEqual(
            resultado["dimensionamento"],
            dimensionamento,
        )

        self.assertEqual(
            resultado["modulos"],
            modulos,
        )

        self.assertEqual(
            resultado["inversores"],
            inversores,
        )

        self.assertEqual(
            resultado["local_instalacao"],
            local_instalacao,
        )

        self.assertEqual(
            resultado["comercial"],
            comercial,
        )

    def test_orcamento_recebe_copia_dos_dados(self):
        """
        Os dicionários internos do Orçamento não devem
        compartilhar as referências recebidas.
        """

        dimensionamento = {
            "consumo_medio_kwh": 650.0,
            "potencia_prevista_kwp": 5.5,
        }

        modulos = {
            "quantidade": 10,
            "fabricante": "Canadian Solar",
        }

        inversores = {
            "quantidade": 1,
            "fabricante": "Growatt",
            "tensao": "220 V",
        }

        local_instalacao = {
            "codigo_uc": "123456789",
            "distribuidora": "Neoenergia Coelba",
            "tipo_telhado": "Cerâmico",
        }

        comercial = {
            "valor_total": 23000.00,
            "validade_dias": 10,
            "prazo_instalacao_dias": 45,
        }

        resultado = criar_dados_orcamento(
            codigo=1,
            codigo_cliente=3,
            dimensionamento=dimensionamento,
            modulos=modulos,
            inversores=inversores,
            local_instalacao=local_instalacao,
            comercial=comercial,
            status_inicial="Em negociação",
        )

        self.assertIsNot(
            resultado["dimensionamento"],
            dimensionamento,
        )

        self.assertIsNot(
            resultado["modulos"],
            modulos,
        )

        self.assertIsNot(
            resultado["inversores"],
            inversores,
        )

        self.assertIsNot(
            resultado["local_instalacao"],
            local_instalacao,
        )

        self.assertIsNot(
            resultado["comercial"],
            comercial,
        )

    def test_orcamento_aprovado_pode_ser_convertido(self):
        """
        Um Orçamento aprovado pode ser convertido
        em Projeto.
        """

        orcamento = {
            "status": "Aprovado",
        }

        self.assertTrue(
            orcamento_pode_ser_convertido(
                orcamento
            )
        )

    def test_orcamento_nao_aprovado_nao_pode_ser_convertido(
        self,
    ):
        """
        Um Orçamento não aprovado não pode
        ser convertido em Projeto.
        """

        orcamento = {
            "status": "Em negociação",
        }

        self.assertFalse(
            orcamento_pode_ser_convertido(
                orcamento
            )
        )


if __name__ == "__main__":
    unittest.main()