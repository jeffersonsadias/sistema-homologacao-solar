import unittest

from app import clientes


class TestBuscaClientesPorNome(unittest.TestCase):
    """
    Testes da função buscar_clientes_por_nome().
    """

    def setUp(self):
        """
        Prepara uma lista controlada antes de cada teste.
        """

        self.clientes_originais = clientes.clientes

        clientes.clientes = [
            {
                "codigo": 1,
                "nome": "Solar Bahia Engenharia",
                "cidade": "Salvador",
                "telefone": "71999999999"
            },
            {
                "codigo": 2,
                "nome": "Grupo Nordeste Solar",
                "cidade": "Recife",
                "telefone": "81999999999"
            },
            {
                "codigo": 3,
                "nome": "Comercial Santos",
                "cidade": "Caetité",
                "telefone": "77999999999"
            }
        ]

    def tearDown(self):
        """
        Restaura a lista original depois de cada teste.
        """

        clientes.clientes = self.clientes_originais

    def test_busca_por_nome_completo(self):
        resultado = clientes.buscar_clientes_por_nome(
            "Comercial Santos"
        )

        self.assertEqual(len(resultado), 1)
        self.assertEqual(
            resultado[0]["nome"],
            "Comercial Santos"
        )

    def test_busca_por_parte_do_nome(self):
        resultado = clientes.buscar_clientes_por_nome("solar")

        self.assertEqual(len(resultado), 2)

    def test_busca_deve_ignorar_maiusculas_e_minusculas(self):
        resultado = clientes.buscar_clientes_por_nome("SOLAR")

        self.assertEqual(len(resultado), 2)

    def test_busca_deve_ignorar_espacos_externos(self):
        resultado = clientes.buscar_clientes_por_nome(
            "   Comercial Santos   "
        )

        self.assertEqual(len(resultado), 1)

    def test_busca_sem_resultados_deve_retornar_lista_vazia(self):
        resultado = clientes.buscar_clientes_por_nome(
            "Cliente inexistente"
        )

        self.assertEqual(resultado, [])

    def test_quantidade_clientes(self):
        """
        Deve retornar a quantidade total de Clientes
        cadastrados na fachada.
        """

        resultado = clientes.quantidade_clientes()

        self.assertEqual(
            resultado,
            3,
        )

if __name__ == "__main__":
    unittest.main()