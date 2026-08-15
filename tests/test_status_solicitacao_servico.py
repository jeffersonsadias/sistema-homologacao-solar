import unittest

from app.dominio.status_solicitacao_servico import (
    ESTADOS_TERMINAIS,
    STATUS_INICIAL,
    STATUS_SOLICITACAO_SERVICO,
    obter_status,
    status_terminal,
    status_valido,
    transicao_permitida,
)


class TestStatusSolicitacaoServico(
    unittest.TestCase
):
    """
    Testes da máquina de estados
    de Solicitação de Serviço.
    """

    def test_status_inicial(
        self,
    ):
        """
        Solicitação deve iniciar
        EM_ELABORACAO.
        """

        self.assertEqual(
            STATUS_INICIAL,
            "EM_ELABORACAO",
        )

    def test_catalogo_possui_oito_status(
        self,
    ):
        """
        Catálogo oficial deve conter
        os oito estados definidos.
        """

        self.assertEqual(
            len(
                STATUS_SOLICITACAO_SERVICO
            ),
            8,
        )

    def test_obter_status_existente(
        self,
    ):
        """
        Deve retornar o status correspondente
        ao código informado.
        """

        self.assertEqual(
            obter_status(1),
            "EM_ELABORACAO",
        )

        self.assertEqual(
            obter_status(8),
            "EXPIRADA",
        )

    def test_obter_status_inexistente(
        self,
    ):
        """
        Código inexistente deve retornar None.
        """

        self.assertIsNone(
            obter_status(999)
        )

    def test_status_valido(
        self,
    ):
        """
        Deve reconhecer códigos oficiais.
        """

        for codigo in range(
            1,
            9,
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
        """
        Deve rejeitar códigos que não
        pertençam ao catálogo.
        """

        for codigo in (
            0,
            9,
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

    def test_elaboracao_pode_ser_publicada(
        self,
    ):
        """
        Solicitação em elaboração pode
        ser disponibilizada ao destinatário.
        """

        self.assertTrue(
            transicao_permitida(
                "EM_ELABORACAO",
                "PUBLICADA",
            )
        )

    def test_elaboracao_pode_ser_cancelada(
        self,
    ):
        """
        Solicitação ainda em elaboração
        pode ser cancelada.
        """

        self.assertTrue(
            transicao_permitida(
                "EM_ELABORACAO",
                "CANCELADA",
            )
        )

    def test_publicada_pode_receber_propostas(
        self,
    ):
        """
        Solicitação publicada pode avançar
        para recebimento de propostas.
        """

        self.assertTrue(
            transicao_permitida(
                "PUBLICADA",
                "RECEBENDO_PROPOSTAS",
            )
        )

    def test_recebendo_propostas_pode_ir_para_analise(
        self,
    ):
        """
        Após receber propostas, o Cliente
        pode entrar em análise.
        """

        self.assertTrue(
            transicao_permitida(
                "RECEBENDO_PROPOSTAS",
                "EM_ANALISE_PELO_CLIENTE",
            )
        )

    def test_analise_pode_retornar_para_recebimento(
        self,
    ):
        """
        O fluxo pode retornar ao recebimento
        enquanto a Solicitação não estiver encerrada.
        """

        self.assertTrue(
            transicao_permitida(
                "EM_ANALISE_PELO_CLIENTE",
                "RECEBENDO_PROPOSTAS",
            )
        )

    def test_analise_pode_encerrar_com_contratacao(
        self,
    ):
        """
        Aceite de proposta pode encerrar
        a Solicitação com contratação.
        """

        self.assertTrue(
            transicao_permitida(
                "EM_ANALISE_PELO_CLIENTE",
                "ENCERRADA_COM_CONTRATACAO",
            )
        )

    def test_pode_encerrar_sem_contratacao(
        self,
    ):
        """
        Uma Solicitação pode ser encerrada
        sem escolha de proposta.
        """

        self.assertTrue(
            transicao_permitida(
                "RECEBENDO_PROPOSTAS",
                "ENCERRADA_SEM_CONTRATACAO",
            )
        )

    def test_publicada_pode_expirar(
        self,
    ):
        """
        Solicitação publicada pode expirar
        sem avanço comercial.
        """

        self.assertTrue(
            transicao_permitida(
                "PUBLICADA",
                "EXPIRADA",
            )
        )

    def test_transicao_nao_permitida(
        self,
    ):
        """
        Não deve permitir saltos incompatíveis
        com a máquina de estados.
        """

        self.assertFalse(
            transicao_permitida(
                "EM_ELABORACAO",
                "ENCERRADA_COM_CONTRATACAO",
            )
        )

        self.assertFalse(
            transicao_permitida(
                "PUBLICADA",
                "EM_ANALISE_PELO_CLIENTE",
            )
        )

    def test_estados_terminais(
        self,
    ):
        """
        Deve reconhecer exatamente os
        estados terminais oficiais.
        """

        esperados = {
            "ENCERRADA_COM_CONTRATACAO",
            "ENCERRADA_SEM_CONTRATACAO",
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
        """
        Consulta deve reconhecer
        estados terminais.
        """

        for status in (
            "ENCERRADA_COM_CONTRATACAO",
            "ENCERRADA_SEM_CONTRATACAO",
            "CANCELADA",
            "EXPIRADA",
        ):
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
        """
        Estados de fluxo ainda aberto
        não são terminais.
        """

        for status in (
            "EM_ELABORACAO",
            "PUBLICADA",
            "RECEBENDO_PROPOSTAS",
            "EM_ANALISE_PELO_CLIENTE",
        ):
            with self.subTest(
                status=status
            ):
                self.assertFalse(
                    status_terminal(
                        status
                    )
                )

    def test_terminal_nao_pode_ser_reaberto(
        self,
    ):
        """
        Nenhum estado terminal deve possuir
        transição de saída.
        """

        for status in ESTADOS_TERMINAIS:
            with self.subTest(
                status=status
            ):
                self.assertFalse(
                    transicao_permitida(
                        status,
                        "EM_ELABORACAO",
                    )
                )

                self.assertFalse(
                    transicao_permitida(
                        status,
                        "PUBLICADA",
                    )
                )


if __name__ == "__main__":
    unittest.main()