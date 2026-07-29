import unittest

from app.dominio import status


class TestTransicaoStatus(unittest.TestCase):
    """
    Testes das regras e operações de status.
    """

    def test_transicao_valida_deve_retornar_true(self):
        resultado = status.transicao_permitida(
            "Aguardando documentação",
            "Documentação recebida"
        )

        self.assertTrue(resultado)

    def test_transicao_invalida_deve_retornar_false(self):
        resultado = status.transicao_permitida(
            "Aguardando documentação",
            "Homologado"
        )

        self.assertFalse(resultado)

    def test_status_final_nao_deve_permitir_nova_transicao(self):
        resultado = status.transicao_permitida(
            "Homologado",
            "Aguardando documentação"
        )

        self.assertFalse(resultado)

    def test_obter_status_existente(self):
        resultado = status.obter_status(1)

        self.assertEqual(
            resultado,
            "Aguardando documentação"
        )

    def test_obter_status_inexistente_deve_retornar_none(self):
        resultado = status.obter_status(999)

        self.assertIsNone(resultado)

    def test_codigo_de_status_valido_deve_retornar_true(self):
        resultado = status.status_valido(5)

        self.assertTrue(resultado)

    def test_codigo_de_status_invalido_deve_retornar_false(self):
        resultado = status.status_valido(999)

        self.assertFalse(resultado)


if __name__ == "__main__":
    unittest.main()