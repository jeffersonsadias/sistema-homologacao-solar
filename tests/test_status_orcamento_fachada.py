import unittest
from unittest.mock import patch

from app import status_orcamento


class TestStatusOrcamentoFachada(
    unittest.TestCase
):
    """
    Testes da fachada pública dos status
    de Orçamento.
    """

    def test_reexporta_status_inicial(self):
        """
        A fachada deve disponibilizar
        o status inicial.
        """

        self.assertEqual(
            status_orcamento.STATUS_INICIAL,
            "Em elaboração",
        )

    def test_reexporta_catalogo_de_status(self):
        """
        A fachada deve disponibilizar
        o catálogo oficial de status.
        """

        self.assertEqual(
            status_orcamento.STATUS_ORCAMENTO[5],
            "Aprovado",
        )

    def test_obter_status(self):
        """
        A fachada deve disponibilizar
        a consulta de status por código.
        """

        resultado = (
            status_orcamento.obter_status(5)
        )

        self.assertEqual(
            resultado,
            "Aprovado",
        )

    def test_status_valido(self):
        """
        A fachada deve disponibilizar
        a validação de códigos.
        """

        self.assertTrue(
            status_orcamento.status_valido(1)
        )

        self.assertFalse(
            status_orcamento.status_valido(99)
        )

    def test_transicao_permitida(self):
        """
        A fachada deve disponibilizar
        a regra de transição.
        """

        resultado = (
            status_orcamento.transicao_permitida(
                "Em elaboração",
                "Enviado ao cliente",
            )
        )

        self.assertTrue(resultado)

    @patch(
        "app.status_orcamento.exibir_status"
    )
    def test_exibir_status_disponivel(
        self,
        mock_exibir_status,
    ):
        """
        A função de exibição deve permanecer
        disponível pela fachada.
        """

        status_orcamento.exibir_status()

        mock_exibir_status.assert_called_once_with()


if __name__ == "__main__":
    unittest.main()