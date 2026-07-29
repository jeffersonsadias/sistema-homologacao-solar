import unittest

from app.dominio.status import (
    STATUS_INICIAL,
    STATUS_PROJETO,
    TRANSICOES_PERMITIDAS,
    obter_status,
    status_valido,
    transicao_permitida,
)


class TestStatusDominio(unittest.TestCase):
    """
    Testes das regras de domínio
    dos status de Projeto.
    """

    def test_status_inicial(self):
        self.assertEqual(
            STATUS_INICIAL,
            "Aguardando documentação",
        )

    def test_obter_status_existente(self):
        resultado = obter_status(5)

        self.assertEqual(
            resultado,
            "Aprovado",
        )

    def test_obter_status_inexistente(self):
        resultado = obter_status(99)

        self.assertIsNone(resultado)

    def test_status_valido(self):
        self.assertTrue(
            status_valido(1)
        )

        self.assertFalse(
            status_valido(99)
        )

    def test_transicao_permitida(self):
        resultado = transicao_permitida(
            "Aguardando documentação",
            "Documentação recebida",
        )

        self.assertTrue(resultado)

    def test_transicao_nao_permitida(self):
        resultado = transicao_permitida(
            "Aguardando documentação",
            "Homologado",
        )

        self.assertFalse(resultado)

    def test_status_finais_sem_transicoes(self):
        self.assertEqual(
            TRANSICOES_PERMITIDAS["Homologado"],
            [],
        )

        self.assertEqual(
            TRANSICOES_PERMITIDAS["Cancelado"],
            [],
        )

    def test_todos_status_possuem_regra(self):
        for descricao in STATUS_PROJETO.values():
            self.assertIn(
                descricao,
                TRANSICOES_PERMITIDAS,
            )


if __name__ == "__main__":
    unittest.main()