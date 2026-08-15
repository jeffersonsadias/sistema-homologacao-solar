import unittest

from app.dominio.status_proposta_servico import (
    ESTADOS_TERMINAIS,
    STATUS_INICIAL,
    STATUS_PROPOSTA_SERVICO,
    obter_status,
    status_terminal,
    status_valido,
    transicao_permitida,
)


class TestStatusPropostaServico(
    unittest.TestCase
):
    """
    Testes da máquina de estados
    de Proposta de Serviço.
    """

    def test_status_inicial(
        self,
    ):
        self.assertEqual(
            STATUS_INICIAL,
            "EM_ELABORACAO",
        )

    def test_catalogo_possui_nove_status(
        self,
    ):
        self.assertEqual(
            len(
                STATUS_PROPOSTA_SERVICO
            ),
            9,
        )

    def test_obter_status_existente(
        self,
    ):
        self.assertEqual(
            obter_status(1),
            "EM_ELABORACAO",
        )

        self.assertEqual(
            obter_status(9),
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
            10,
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
            10,
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

    def test_elaboracao_pode_ser_enviada(
        self,
    ):
        self.assertTrue(
            transicao_permitida(
                "EM_ELABORACAO",
                "ENVIADA",
            )
        )

    def test_elaboracao_pode_ser_retirada(
        self,
    ):
        self.assertTrue(
            transicao_permitida(
                "EM_ELABORACAO",
                "RETIRADA",
            )
        )

    def test_enviada_pode_entrar_em_revisao(
        self,
    ):
        self.assertTrue(
            transicao_permitida(
                "ENVIADA",
                "EM_REVISAO",
            )
        )

    def test_revisao_pode_gerar_proposta_revisada(
        self,
    ):
        self.assertTrue(
            transicao_permitida(
                "EM_REVISAO",
                "REVISADA",
            )
        )

    def test_revisada_pode_ser_reenviada(
        self,
    ):
        self.assertTrue(
            transicao_permitida(
                "REVISADA",
                "ENVIADA",
            )
        )

    def test_enviada_pode_ser_aceita(
        self,
    ):
        self.assertTrue(
            transicao_permitida(
                "ENVIADA",
                "ACEITA",
            )
        )

    def test_enviada_pode_ser_recusada(
        self,
    ):
        self.assertTrue(
            transicao_permitida(
                "ENVIADA",
                "RECUSADA",
            )
        )

    def test_enviada_pode_ser_nao_selecionada(
        self,
    ):
        self.assertTrue(
            transicao_permitida(
                "ENVIADA",
                "NAO_SELECIONADA",
            )
        )

    def test_enviada_pode_ser_retirada(
        self,
    ):
        self.assertTrue(
            transicao_permitida(
                "ENVIADA",
                "RETIRADA",
            )
        )

    def test_enviada_pode_expirar(
        self,
    ):
        self.assertTrue(
            transicao_permitida(
                "ENVIADA",
                "EXPIRADA",
            )
        )

    def test_transicao_invalida(
        self,
    ):
        self.assertFalse(
            transicao_permitida(
                "EM_ELABORACAO",
                "ACEITA",
            )
        )

        self.assertFalse(
            transicao_permitida(
                "EM_REVISAO",
                "ACEITA",
            )
        )

    def test_estados_terminais(
        self,
    ):
        esperados = {
            "ACEITA",
            "RECUSADA",
            "NAO_SELECIONADA",
            "RETIRADA",
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
            "EM_ELABORACAO",
            "ENVIADA",
            "EM_REVISAO",
            "REVISADA",
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
                        "ENVIADA",
                    )
                )

                self.assertFalse(
                    transicao_permitida(
                        status,
                        "EM_REVISAO",
                    )
                )


if __name__ == "__main__":
    unittest.main()