import unittest

from app.dominio.status_ordem_servico import (
    ESTADOS_TERMINAIS,
    STATUS_INICIAL,
    STATUS_ORDEM_SERVICO,
    obter_status,
    status_terminal,
    status_valido,
    transicao_permitida,
)


class TestStatusOrdemServico(
    unittest.TestCase
):
    """
    Testes da máquina de estados
    de Ordem de Serviço.
    """

    def test_status_inicial(self):
        self.assertEqual(
            STATUS_INICIAL,
            "ABERTA",
        )

    def test_catalogo_possui_treze_status(self):
        self.assertEqual(
            len(STATUS_ORDEM_SERVICO),
            13,
        )

    def test_obter_status_existente(self):
        self.assertEqual(
            obter_status(1),
            "ABERTA",
        )

        self.assertEqual(
            obter_status(13),
            "CANCELADA",
        )

    def test_obter_status_inexistente(self):
        self.assertIsNone(
            obter_status(999)
        )

    def test_status_valido(self):
        for codigo in range(1, 14):
            with self.subTest(
                codigo=codigo
            ):
                self.assertTrue(
                    status_valido(codigo)
                )

    def test_status_invalido(self):
        for codigo in (
            0,
            14,
            999,
            None,
        ):
            with self.subTest(
                codigo=codigo
            ):
                self.assertFalse(
                    status_valido(codigo)
                )

    def test_aberta_pode_entrar_em_triagem(self):
        self.assertTrue(
            transicao_permitida(
                "ABERTA",
                "EM_TRIAGEM",
            )
        )

    def test_triagem_pode_ir_para_diagnostico(self):
        self.assertTrue(
            transicao_permitida(
                "EM_TRIAGEM",
                "AGUARDANDO_DIAGNOSTICO",
            )
        )

    def test_triagem_pode_pular_diagnostico(self):
        self.assertTrue(
            transicao_permitida(
                "EM_TRIAGEM",
                "AGUARDANDO_AGENDAMENTO",
            )
        )

    def test_triagem_pode_ir_direto_para_aprovacao(self):
        self.assertTrue(
            transicao_permitida(
                "EM_TRIAGEM",
                "AGUARDANDO_APROVACAO",
            )
        )

    def test_diagnostico_pode_exigir_aprovacao(self):
        self.assertTrue(
            transicao_permitida(
                "AGUARDANDO_DIAGNOSTICO",
                "AGUARDANDO_APROVACAO",
            )
        )

    def test_diagnostico_pode_ir_para_agendamento(self):
        self.assertTrue(
            transicao_permitida(
                "AGUARDANDO_DIAGNOSTICO",
                "AGUARDANDO_AGENDAMENTO",
            )
        )

    def test_aprovacao_pode_ir_para_agendamento(self):
        self.assertTrue(
            transicao_permitida(
                "AGUARDANDO_APROVACAO",
                "AGUARDANDO_AGENDAMENTO",
            )
        )

    def test_agendamento_pode_gerar_agendada(self):
        self.assertTrue(
            transicao_permitida(
                "AGUARDANDO_AGENDAMENTO",
                "AGENDADA",
            )
        )

    def test_agendada_pode_entrar_em_execucao(self):
        self.assertTrue(
            transicao_permitida(
                "AGENDADA",
                "EM_EXECUCAO",
            )
        )

    def test_execucao_pode_aguardar_peca(self):
        self.assertTrue(
            transicao_permitida(
                "EM_EXECUCAO",
                "AGUARDANDO_PECA",
            )
        )

    def test_execucao_pode_exigir_retorno(self):
        self.assertTrue(
            transicao_permitida(
                "EM_EXECUCAO",
                "RETORNO_NECESSARIO",
            )
        )

    def test_execucao_pode_aguardar_confirmacao_cliente(
        self,
    ):
        self.assertTrue(
            transicao_permitida(
                "EM_EXECUCAO",
                "AGUARDANDO_CONFIRMACAO_CLIENTE",
            )
        )

    def test_execucao_nao_pode_concluir_diretamente(
        self,
    ):
        self.assertFalse(
            transicao_permitida(
                "EM_EXECUCAO",
                "CONCLUIDA",
            )
        )

    def test_peca_pode_gerar_retorno(self):
        self.assertTrue(
            transicao_permitida(
                "AGUARDANDO_PECA",
                "RETORNO_NECESSARIO",
            )
        )

    def test_retorno_volta_para_agendamento(self):
        self.assertTrue(
            transicao_permitida(
                "RETORNO_NECESSARIO",
                "AGUARDANDO_AGENDAMENTO",
            )
        )

    def test_cliente_pode_confirmar_conclusao(self):
        self.assertTrue(
            transicao_permitida(
                "AGUARDANDO_CONFIRMACAO_CLIENTE",
                "CONCLUIDA",
            )
        )

    def test_cliente_pode_contestar(self):
        self.assertTrue(
            transicao_permitida(
                "AGUARDANDO_CONFIRMACAO_CLIENTE",
                "EM_ANALISE_DE_CONTESTACAO",
            )
        )

    def test_contestacao_pode_gerar_retorno(self):
        self.assertTrue(
            transicao_permitida(
                "EM_ANALISE_DE_CONTESTACAO",
                "RETORNO_NECESSARIO",
            )
        )

    def test_contestacao_pode_confirmar_conclusao(self):
        self.assertTrue(
            transicao_permitida(
                "EM_ANALISE_DE_CONTESTACAO",
                "CONCLUIDA",
            )
        )

    def test_estados_terminais(self):
        self.assertEqual(
            ESTADOS_TERMINAIS,
            {
                "CONCLUIDA",
                "CANCELADA",
            },
        )

    def test_status_terminal(self):
        for status in ESTADOS_TERMINAIS:
            with self.subTest(
                status=status
            ):
                self.assertTrue(
                    status_terminal(status)
                )

    def test_status_nao_terminal(self):
        for status in (
            "ABERTA",
            "EM_TRIAGEM",
            "AGUARDANDO_DIAGNOSTICO",
            "AGUARDANDO_APROVACAO",
            "AGUARDANDO_AGENDAMENTO",
            "AGENDADA",
            "EM_EXECUCAO",
            "AGUARDANDO_PECA",
            "RETORNO_NECESSARIO",
            "AGUARDANDO_CONFIRMACAO_CLIENTE",
            "EM_ANALISE_DE_CONTESTACAO",
        ):
            with self.subTest(
                status=status
            ):
                self.assertFalse(
                    status_terminal(status)
                )

    def test_estado_terminal_nao_possui_saida(self):
        for status in ESTADOS_TERMINAIS:
            with self.subTest(
                status=status
            ):
                self.assertFalse(
                    transicao_permitida(
                        status,
                        "EM_TRIAGEM",
                    )
                )

                self.assertFalse(
                    transicao_permitida(
                        status,
                        "EM_EXECUCAO",
                    )
                )

    def test_salto_invalido_triagem_para_execucao(self):
        self.assertFalse(
            transicao_permitida(
                "EM_TRIAGEM",
                "EM_EXECUCAO",
            )
        )


if __name__ == "__main__":
    unittest.main()