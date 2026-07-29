import unittest

from app.dominio.clientes import (
    buscar_cliente_por_codigo,
    buscar_clientes_por_nome,
    codigo_cliente_existe,
    ordenar_clientes_por_nome,
)


class TestClientesDominio(unittest.TestCase):
    """
    Testes das regras puras do domínio de Clientes.
    """

    def setUp(self):
        """
        Cria uma lista nova antes de cada teste.
        """

        self.clientes = [
            {
                "codigo": 1,
                "nome": "Carlos Souza",
            },
            {
                "codigo": 2,
                "nome": "Ana Lima",
            },
            {
                "codigo": 3,
                "nome": "Bruno Santos",
            },
        ]

    def test_buscar_cliente_por_codigo_existente(self):
        """
        Deve retornar o cliente correspondente ao código.
        """

        cliente = buscar_cliente_por_codigo(
            self.clientes,
            2,
        )

        self.assertIsNotNone(cliente)
        self.assertEqual(cliente["nome"], "Ana Lima")

    def test_buscar_cliente_por_codigo_inexistente(self):
        """
        Deve retornar None quando o código não existir.
        """

        cliente = buscar_cliente_por_codigo(
            self.clientes,
            999,
        )

        self.assertIsNone(cliente)

    def test_codigo_cliente_existe(self):
        """
        Deve informar corretamente se o código existe.
        """

        self.assertTrue(
            codigo_cliente_existe(
                self.clientes,
                1,
            )
        )

        self.assertFalse(
            codigo_cliente_existe(
                self.clientes,
                999,
            )
        )

    def test_ordenar_clientes_por_nome(self):
        """
        Deve ordenar os clientes alfabeticamente.
        """

        clientes_ordenados = ordenar_clientes_por_nome(
            self.clientes
        )

        nomes = [
            cliente["nome"]
            for cliente in clientes_ordenados
        ]

        self.assertEqual(
            nomes,
            [
                "Ana Lima",
                "Bruno Santos",
                "Carlos Souza",
            ],
        )

    def test_ordenacao_nao_altera_lista_original(self):
        """
        A ordenação deve retornar uma nova lista.
        """

        ordem_original = [
            cliente["nome"]
            for cliente in self.clientes
        ]

        ordenar_clientes_por_nome(self.clientes)

        ordem_depois = [
            cliente["nome"]
            for cliente in self.clientes
        ]

        self.assertEqual(
            ordem_depois,
            ordem_original,
        )

    def test_buscar_clientes_por_nome_completo(self):
        """
        Deve localizar um cliente pelo nome completo.
        """

        encontrados = buscar_clientes_por_nome(
            self.clientes,
            "Ana Lima",
        )

        self.assertEqual(len(encontrados), 1)
        self.assertEqual(encontrados[0]["codigo"], 2)

    def test_buscar_clientes_por_parte_do_nome(self):
        """
        Deve localizar clientes por parte do nome.
        """

        encontrados = buscar_clientes_por_nome(
            self.clientes,
            "Santos",
        )

        self.assertEqual(len(encontrados), 1)
        self.assertEqual(
            encontrados[0]["nome"],
            "Bruno Santos",
        )

    def test_busca_por_nome_ignora_maiusculas_e_minusculas(self):
        """
        A busca não deve diferenciar letras maiúsculas
        de minúsculas.
        """

        encontrados = buscar_clientes_por_nome(
            self.clientes,
            "ANA",
        )

        self.assertEqual(len(encontrados), 1)
        self.assertEqual(
            encontrados[0]["nome"],
            "Ana Lima",
        )

    def test_busca_por_nome_remove_espacos_externos(self):
        """
        Deve remover espaços antes e depois do termo pesquisado.
        """

        encontrados = buscar_clientes_por_nome(
            self.clientes,
            "   ana   ",
        )

        self.assertEqual(len(encontrados), 1)
        self.assertEqual(
            encontrados[0]["nome"],
            "Ana Lima",
        )

    def test_busca_por_nome_retorna_lista_vazia(self):
        """
        Deve retornar uma lista vazia quando nenhum cliente
        for encontrado.
        """

        encontrados = buscar_clientes_por_nome(
            self.clientes,
            "Nome Inexistente",
        )

        self.assertEqual(encontrados, [])


if __name__ == "__main__":
    unittest.main()