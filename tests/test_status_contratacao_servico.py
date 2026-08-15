import unittest

from app.dominio.status_contratacao_servico import (
    ESTADOS_TERMINAIS,
    STATUS_CONTRATACAO_SERVICO,
    STATUS_INICIAL,
    obter_status,
    status_terminal,
    status_valido,
    transicao_permitida,
)


class TestStatusContratacaoServico(
    unittest.TestCase
):
    """
    Testes da máquina de estados
    de Contratação de Serviço.
    """

    def test_status_inicial(
        self,
    ):
        self.assertEqual(
            STATUS_INICIAL,
            "EM_FORMALIZACAO",
        )

    def test_catalogo_possui_sete_status(
        self,
    ):
        self.assertEqual(
            len(
                STATUS_CONTRATACAO_SERVICO
            ),
            7,
        )

    def test_obter_status_existente(
        self,
    ):
        self.assertEqual(
            obter_status(1),
            "EM_FORMALIZACAO",
        )

        self.assertEqual(
            obter_status(7),
            "EXPIRADA",
        )

    def test_obter_status_inexistente(
        self,
    ):
        self.assertIsNone(
            obter_status(999)
        )

    def test_status_valido(
        self,
    ):
        for codigo in range(
            1,
            8,
        ):
            with self.subTest(
                codigo=codigo
            ):
                self.assertTrue(
                    status_valido(
                        codigo
                    )
                )

    def test_status_invalido(
        self,
    ):
        for codigo in (
            0,
            8,
            999,
            None,
        ):
            with self.subTest(
                codigo=codigo
            ):
                self.assertFalse(
                    status_valido(
                        codigo
                    )
                )

    def test_formalizacao_pode_ser_confirmada(
        self,
    ):
        self.assertTrue(
            transicao_permitida(
                "EM_FORMALIZACAO",
                "CONFIRMADA",
            )
        )

    def test_formalizacao_pode_ser_cancelada(
        self,
    ):
        self.assertTrue(
            transicao_permitida(
                "EM_FORMALIZACAO",
                "CANCELADA",
            )
        )

    def test_formalizacao_pode_expirar(
        self,
    ):
        self.assertTrue(
            transicao_permitida(
                "EM_FORMALIZACAO",
                "EXPIRADA",
            )
        )

    def test_confirmada_pode_gerar_processo(
        self,
    ):
        self.assertTrue(
            transicao_permitida(
                "CONFIRMADA",
                "PROCESSO_GERADO",
            )
        )

    def test_confirmada_pode_ser_cancelada(
        self,
    ):
        self.assertTrue(
            transicao_permitida(
                "CONFIRMADA",
                "CANCELADA",
            )
        )

    def test_processo_gerado_pode_entrar_em_andamento(
        self,
    ):
        self.assertTrue(
            transicao_permitida(
                "PROCESSO_GERADO",
                "EM_ANDAMENTO",
            )
        )

    def test_processo_gerado_pode_ser_cancelado(
        self,
    ):
        self.assertTrue(
            transicao_permitida(
                "PROCESSO_GERADO",
                "CANCELADA",
            )
        )

    def test_em_andamento_pode_ser_concluida(
        self,
    ):
        self.assertTrue(
            transicao_permitida(
                "EM_ANDAMENTO",
                "CONCLUIDA",
            )
        )

    def test_em_andamento_pode_ser_cancelada(
        self,
    ):
        self.assertTrue(
            transicao_permitida(
                "EM_ANDAMENTO",
                "CANCELADA",
            )
        )

    def test_confirmada_nao_pode_expirar(
        self,
    ):
        """
        Após confirmação, a Contratação
        não expira mais.
        """

        self.assertFalse(
            transicao_permitida(
                "CONFIRMADA",
                "EXPIRADA",
            )
        )

    def test_nao_pode_saltar_para_conclusao(
        self,
    ):
        """
        A Contratação deve passar pelo
        processo operacional.
        """

        self.assertFalse(
            transicao_permitida(
                "CONFIRMADA",
                "CONCLUIDA",
            )
        )

        self.assertFalse(
            transicao_permitida(
                "PROCESSO_GERADO",
                "CONCLUIDA",
            )
        )

    def test_estados_terminais(
        self,
    ):
        esperados = {
            "CONCLUIDA",
            "CANCELADA",
            "EXPIRADA",
        }

        self.assertEqual(
            ESTADOS_TERMINAIS,
            esperados,
        )

    def test_status_terminal(
        self,
    ):
        for status in ESTADOS_TERMINAIS:
            with self.subTest(
                status=status
            ):
                self.assertTrue(
                    status_terminal(
                        status
                    )
                )

    def test_status_nao_terminal(
        self,
    ):
        for status in (
            "EM_FORMALIZACAO",
            "CONFIRMADA",
            "PROCESSO_GERADO",
            "EM_ANDAMENTO",
        ):
            with self.subTest(
                status=status
            ):
                self.assertFalse(
                    status_terminal(
                        status
                    )
                )

    def test_estado_terminal_nao_possui_saida(
        self,
    ):
        for status in ESTADOS_TERMINAIS:
            with self.subTest(
                status=status
            ):
                self.assertFalse(
                    transicao_permitida(
                        status,
                        "EM_FORMALIZACAO",
                    )
                )

                self.assertFalse(
                    transicao_permitida(
                        status,
                        "EM_ANDAMENTO",
                    )
                )


if __name__ == "__main__":
    unittest.main()