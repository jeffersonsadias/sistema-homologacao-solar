import unittest

from app import orcamentos


class TestOrcamentos(unittest.TestCase):
    """
    Testes das operações básicas de orçamentos.
    """

    def setUp(self):
        """
        Substitui temporariamente a lista real
        por dados controlados de teste.
        """

        self.orcamentos_originais = orcamentos.orcamentos

        orcamentos.orcamentos = [
            {
                "codigo": 1,
                "cliente": 1,
                "status": "Em elaboração"
            },
            {
                "codigo": 2,
                "cliente": 2,
                "status": "Enviado ao cliente"
            }
        ]

    def tearDown(self):
        """
        Restaura a lista original após cada teste.
        """

        orcamentos.orcamentos = self.orcamentos_originais

    def test_buscar_orcamento_existente(self):
        resultado = orcamentos.buscar_orcamento(2)

        self.assertIsNotNone(resultado)
        self.assertEqual(resultado["codigo"], 2)
        self.assertEqual(
            resultado["status"],
            "Enviado ao cliente"
        )

    def test_buscar_orcamento_inexistente_deve_retornar_none(self):
        resultado = orcamentos.buscar_orcamento(999)

        self.assertIsNone(resultado)

    def test_quantidade_orcamentos(self):
        """
        Deve retornar a quantidade de Orçamentos cadastrados.
        """

        resultado = orcamentos.quantidade_orcamentos()

        self.assertEqual(
            resultado,
            2,
        )


if __name__ == "__main__":
    unittest.main()