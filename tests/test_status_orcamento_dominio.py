import unittest

from app.dominio.status_orcamento import (
    STATUS_INICIAL,
    STATUS_ORCAMENTO,
    TRANSICOES_PERMITIDAS,
    obter_status,
    status_valido,
    transicao_permitida,
)


class TestStatusOrcamentoDominio(
    unittest.TestCase
):
    """
    Testes das regras de domínio
    dos status de Orçamento.
    """

    def test_status_inicial(self):
        """
        O status inicial deve ser
        Em elaboração.
        """

        self.assertEqual(
            STATUS_INICIAL,
            "Em elaboração",
        )

    def test_obter_status_existente(self):
        """
        Deve retornar a descrição
        do código informado.
        """

        resultado = obter_status(5)

        self.assertEqual(
            resultado,
            "Aprovado",
        )

    def test_obter_status_inexistente(self):
        """
        Deve retornar None para código
        inexistente.
        """

        resultado = obter_status(99)

        self.assertIsNone(resultado)

    def test_status_valido(self):
        """
        Deve identificar códigos válidos
        e inválidos.
        """

        self.assertTrue(
            status_valido(1)
        )

        self.assertFalse(
            status_valido(99)
        )

    def test_transicao_permitida(self):
        """
        Deve permitir uma transição
        cadastrada.
        """

        resultado = transicao_permitida(
            "Em elaboração",
            "Enviado ao cliente",
        )

        self.assertTrue(resultado)

    def test_transicao_nao_permitida(self):
        """
        Deve rejeitar uma transição
        não cadastrada.
        """

        resultado = transicao_permitida(
            "Em elaboração",
            "Aprovado",
        )

        self.assertFalse(resultado)

    def test_status_terminal_nao_possui_transicoes(self):
        """
        Status encerrados não devem possuir
        próximos status.
        """

        self.assertEqual(
            TRANSICOES_PERMITIDAS["Recusado"],
            [],
        )

        self.assertEqual(
            TRANSICOES_PERMITIDAS["Cancelado"],
            [],
        )

        self.assertEqual(
            TRANSICOES_PERMITIDAS[
                "Convertido em projeto"
            ],
            [],
        )

    def test_todos_status_possuem_regra_de_transicao(
        self,
    ):
        """
        Todo status oficial deve estar presente
        no mapa de transições.
        """

        for descricao in (
            STATUS_ORCAMENTO.values()
        ):
            self.assertIn(
                descricao,
                TRANSICOES_PERMITIDAS,
            )


if __name__ == "__main__":
    unittest.main()