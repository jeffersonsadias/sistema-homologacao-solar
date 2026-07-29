import unittest
from unittest.mock import patch

from app import status


class TestStatusFachada(unittest.TestCase):
    """
    Testes da fachada pública
    dos status de Projeto.
    """

    def test_disponibiliza_status_inicial(self):
        self.assertEqual(
            status.STATUS_INICIAL,
            "Aguardando documentação",
        )

    def test_disponibiliza_catalogo(self):
        self.assertEqual(
            status.STATUS_PROJETO[9],
            "Homologado",
        )

    def test_obter_status(self):
        resultado = status.obter_status(9)

        self.assertEqual(
            resultado,
            "Homologado",
        )

    def test_status_valido(self):
        self.assertTrue(
            status.status_valido(1)
        )

        self.assertFalse(
            status.status_valido(99)
        )

    def test_transicao_permitida(self):
        resultado = status.transicao_permitida(
            "Aprovado",
            "Instalação concluída",
        )

        self.assertTrue(resultado)

    @patch("app.status.exibir_status")
    def test_exibir_status_disponivel(
        self,
        mock_exibir_status,
    ):
        status.exibir_status()

        mock_exibir_status.assert_called_once_with()


if __name__ == "__main__":
    unittest.main()