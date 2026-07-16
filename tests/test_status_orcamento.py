import unittest

from app import status_orcamento


class TestStatusOrcamento(unittest.TestCase):
    """
    Testes das regras de status dos orçamentos.
    """

    def test_status_inicial_deve_ser_em_elaboracao(self):
        self.assertEqual(
            status_orcamento.STATUS_INICIAL,
            "Em elaboração"
        )

    def test_obter_status_existente(self):
        resultado = status_orcamento.obter_status(1)

        self.assertEqual(
            resultado,
            "Em elaboração"
        )

    def test_obter_status_inexistente_deve_retornar_none(self):
        resultado = status_orcamento.obter_status(999)

        self.assertIsNone(resultado)

    def test_codigo_valido_deve_retornar_true(self):
        resultado = status_orcamento.status_valido(5)

        self.assertTrue(resultado)

    def test_codigo_invalido_deve_retornar_false(self):
        resultado = status_orcamento.status_valido(999)

        self.assertFalse(resultado)

    def test_transicao_valida_deve_retornar_true(self):
        resultado = status_orcamento.transicao_permitida(
            "Em elaboração",
            "Enviado ao cliente"
        )

        self.assertTrue(resultado)

    def test_transicao_invalida_deve_retornar_false(self):
        resultado = status_orcamento.transicao_permitida(
            "Em elaboração",
            "Convertido em projeto"
        )

        self.assertFalse(resultado)

    def test_orcamento_convertido_nao_deve_permitir_transicao(self):
        resultado = status_orcamento.transicao_permitida(
            "Convertido em projeto",
            "Em revisão"
        )

        self.assertFalse(resultado)

if __name__ == "__main__":
    unittest.main()