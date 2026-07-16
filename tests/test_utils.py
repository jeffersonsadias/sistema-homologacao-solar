import unittest

from app import utils


class TestGerarProximoCodigo(unittest.TestCase):
    """
    Testes da função gerar_proximo_codigo().
    """

    def test_lista_vazia_deve_retornar_um(self):
        registros = []

        resultado = utils.gerar_proximo_codigo(registros)

        self.assertEqual(resultado, 1)

    def test_deve_retornar_proximo_codigo_sequencial(self):
        registros = [
            {"codigo": 1},
            {"codigo": 2},
            {"codigo": 3}
        ]

        resultado = utils.gerar_proximo_codigo(registros)

        self.assertEqual(resultado, 4)

    def test_deve_usar_maior_codigo_existente(self):
        registros = [
            {"codigo": 1},
            {"codigo": 5},
            {"codigo": 3}
        ]

        resultado = utils.gerar_proximo_codigo(registros)

        self.assertEqual(resultado, 6)


if __name__ == "__main__":
    unittest.main()