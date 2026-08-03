import unittest

from app.dominio.status_homologacao import (
    STATUS_INICIAL_HOMOLOGACAO,
    STATUS_RESULTANTE_POR_EVENTO_HOMOLOGACAO,
    STATUS_TERMINAIS_HOMOLOGACAO,
    TRANSICOES_HOMOLOGACAO,
    EventoHomologacao,
    StatusHomologacao,
    evento_homologacao_valido,
    listar_transicoes_possiveis,
    obter_rotulo_status_homologacao,
    obter_status_resultante_evento_homologacao,
    status_homologacao_e_terminal,
    transicao_status_homologacao_e_valida,
    validar_evento_no_estado_homologacao,
)


class TestStatusHomologacao(unittest.TestCase):
    """
    Testes da máquina de estados da Homologação.
    """

    def test_estado_inicial_deve_ser_em_preparacao(self):
        self.assertEqual(
            STATUS_INICIAL_HOMOLOGACAO,
            StatusHomologacao.EM_PREPARACAO,
        )

    def test_todos_os_status_devem_possuir_transicoes_mapeadas(self):
        for status in StatusHomologacao:
            self.assertIn(
                status,
                TRANSICOES_HOMOLOGACAO,
            )

    def test_todos_os_status_devem_possuir_rotulo(self):
        for status in StatusHomologacao:
            rotulo = obter_rotulo_status_homologacao(status)

            self.assertIsInstance(rotulo, str)
            self.assertTrue(rotulo.strip())

    def test_fluxo_principal_deve_possuir_transicoes_validas(self):
        fluxo_principal = (
            StatusHomologacao.EM_PREPARACAO,
            StatusHomologacao.AGUARDANDO_DOCUMENTACAO,
            StatusHomologacao.PRONTA_PARA_ENVIO,
            StatusHomologacao.ENVIADA_A_CONCESSIONARIA,
            StatusHomologacao.EM_ANALISE,
            StatusHomologacao.PARECER_DE_ACESSO_EMITIDO,
            StatusHomologacao.AGUARDANDO_INSTALACAO,
            StatusHomologacao.INSTALACAO_CONCLUIDA,
            StatusHomologacao.VISTORIA_SOLICITADA,
            StatusHomologacao.AGUARDANDO_VISTORIA,
            StatusHomologacao.VISTORIA_APROVADA,
            StatusHomologacao.AGUARDANDO_LIGACAO,
            StatusHomologacao.SISTEMA_LIGADO,
            StatusHomologacao.CONCLUIDA,
        )

        for indice in range(len(fluxo_principal) - 1):
            status_atual = fluxo_principal[indice]
            novo_status = fluxo_principal[indice + 1]

            self.assertTrue(
                transicao_status_homologacao_e_valida(
                    status_atual,
                    novo_status,
                ),
                msg=(
                    "Transição esperada como válida: "
                    f"{status_atual.value} -> {novo_status.value}"
                ),
            )

    def test_ciclo_de_exigencia_deve_ser_valido(self):
        transicoes = (
            (
                StatusHomologacao.EM_ANALISE,
                StatusHomologacao.COM_EXIGENCIA,
            ),
            (
                StatusHomologacao.COM_EXIGENCIA,
                StatusHomologacao.EM_CORRECAO,
            ),
            (
                StatusHomologacao.EM_CORRECAO,
                StatusHomologacao.REAPRESENTADA,
            ),
            (
                StatusHomologacao.REAPRESENTADA,
                StatusHomologacao.EM_ANALISE,
            ),
        )

        for status_atual, novo_status in transicoes:
            self.assertTrue(
                transicao_status_homologacao_e_valida(
                    status_atual,
                    novo_status,
                )
            )

    def test_ciclo_de_reprovacao_da_vistoria_deve_ser_valido(self):
        transicoes = (
            (
                StatusHomologacao.AGUARDANDO_VISTORIA,
                StatusHomologacao.VISTORIA_REPROVADA,
            ),
            (
                StatusHomologacao.VISTORIA_REPROVADA,
                StatusHomologacao.CORRECAO_POS_VISTORIA,
            ),
            (
                StatusHomologacao.CORRECAO_POS_VISTORIA,
                StatusHomologacao.VISTORIA_SOLICITADA,
            ),
            (
                StatusHomologacao.VISTORIA_SOLICITADA,
                StatusHomologacao.AGUARDANDO_VISTORIA,
            ),
        )

        for status_atual, novo_status in transicoes:
            self.assertTrue(
                transicao_status_homologacao_e_valida(
                    status_atual,
                    novo_status,
                )
            )

    def test_nao_deve_permitir_conclusao_direta_a_partir_da_analise(self):
        resultado = transicao_status_homologacao_e_valida(
            StatusHomologacao.EM_ANALISE,
            StatusHomologacao.CONCLUIDA,
        )

        self.assertFalse(resultado)

    def test_nao_deve_permitir_ligacao_antes_da_vistoria(self):
        resultado = transicao_status_homologacao_e_valida(
            StatusHomologacao.INSTALACAO_CONCLUIDA,
            StatusHomologacao.SISTEMA_LIGADO,
        )

        self.assertFalse(resultado)

    def test_estados_terminais_devem_ser_identificados(self):
        self.assertTrue(
            status_homologacao_e_terminal(
                StatusHomologacao.CONCLUIDA
            )
        )

        self.assertTrue(
            status_homologacao_e_terminal(
                StatusHomologacao.REJEITADA
            )
        )

        self.assertTrue(
            status_homologacao_e_terminal(
                StatusHomologacao.CANCELADA
            )
        )

    def test_estado_em_analise_nao_deve_ser_terminal(self):
        self.assertFalse(
            status_homologacao_e_terminal(
                StatusHomologacao.EM_ANALISE
            )
        )

    def test_estados_terminais_nao_devem_possuir_transicoes(self):
        for status in STATUS_TERMINAIS_HOMOLOGACAO:
            self.assertEqual(
                listar_transicoes_possiveis(status),
                (),
            )

    def test_deve_listar_transicoes_possiveis(self):
        resultado = listar_transicoes_possiveis(
            StatusHomologacao.VISTORIA_REPROVADA
        )

        self.assertIn(
            StatusHomologacao.CORRECAO_POS_VISTORIA,
            resultado,
        )

        self.assertIn(
            StatusHomologacao.CANCELADA,
            resultado,
        )

        self.assertEqual(len(resultado), 2)

    def test_rotulo_de_em_analise_deve_ser_amigavel(self):
        resultado = obter_rotulo_status_homologacao(
            StatusHomologacao.EM_ANALISE
        )

        self.assertEqual(
            resultado,
            "Em análise",
        )

class TestEventosHomologacao(unittest.TestCase):
    """
    Testes dos reflexos dos Eventos de negócio sobre
    a máquina de estados da Homologação.
    """

    def test_todos_os_eventos_devem_possuir_status_resultante(
        self
    ):
        for evento in EventoHomologacao:
            self.assertIn(
                evento,
                STATUS_RESULTANTE_POR_EVENTO_HOMOLOGACAO,
            )

    def test_evento_valido_deve_aceitar_enum(self):
        self.assertTrue(
            evento_homologacao_valido(
                EventoHomologacao.EXIGENCIA_RECEBIDA
            )
        )

    def test_evento_valido_deve_aceitar_texto(self):
        self.assertTrue(
            evento_homologacao_valido(
                "SUBMISSAO_DERIVADA_ENVIADA"
            )
        )

    def test_evento_invalido_deve_retornar_false(self):
        self.assertFalse(
            evento_homologacao_valido(
                "EVENTO_INEXISTENTE"
            )
        )

    def test_exigencia_deve_resultar_em_com_exigencia(self):
        resultado = (
            obter_status_resultante_evento_homologacao(
                EventoHomologacao.EXIGENCIA_RECEBIDA
            )
        )

        self.assertEqual(
            resultado,
            StatusHomologacao.COM_EXIGENCIA,
        )

    def test_submissao_derivada_criada_deve_resultar_em_correcao(
        self
    ):
        resultado = (
            obter_status_resultante_evento_homologacao(
                "SUBMISSAO_DERIVADA_CRIADA"
            )
        )

        self.assertEqual(
            resultado,
            StatusHomologacao.EM_CORRECAO,
        )

    def test_submissao_derivada_enviada_deve_resultar_reapresentada(
        self
    ):
        resultado = (
            obter_status_resultante_evento_homologacao(
                "SUBMISSAO_DERIVADA_ENVIADA"
            )
        )

        self.assertEqual(
            resultado,
            StatusHomologacao.REAPRESENTADA,
        )

    def test_evento_compativel_deve_retornar_novo_status(
        self
    ):
        resultado = validar_evento_no_estado_homologacao(
            status_atual=StatusHomologacao.COM_EXIGENCIA,
            evento=(
                EventoHomologacao
                .SUBMISSAO_DERIVADA_CRIADA
            ),
        )

        self.assertEqual(
            resultado,
            StatusHomologacao.EM_CORRECAO,
        )

    def test_evento_incompativel_deve_ser_rejeitado(self):
        with self.assertRaisesRegex(
            ValueError,
            "não pode ser aplicado ao estado atual",
        ):
            validar_evento_no_estado_homologacao(
                status_atual=(
                    StatusHomologacao.EM_PREPARACAO
                ),
                evento=(
                    EventoHomologacao
                    .SUBMISSAO_DERIVADA_ENVIADA
                ),
            )

    def test_evento_invalido_deve_ser_rejeitado(self):
        with self.assertRaisesRegex(
            ValueError,
            "Evento da Homologação inválido",
        ):
            validar_evento_no_estado_homologacao(
                status_atual=(
                    StatusHomologacao.COM_EXIGENCIA
                ),
                evento="EVENTO_INEXISTENTE",
            )

    def test_ciclo_de_exigencia_deve_ser_representado_por_eventos(
        self
    ):
        status = StatusHomologacao.COM_EXIGENCIA

        status = validar_evento_no_estado_homologacao(
            status_atual=status,
            evento="SUBMISSAO_DERIVADA_CRIADA",
        )

        self.assertEqual(
            status,
            StatusHomologacao.EM_CORRECAO,
        )

        status = validar_evento_no_estado_homologacao(
            status_atual=status,
            evento="SUBMISSAO_DERIVADA_ENVIADA",
        )

        self.assertEqual(
            status,
            StatusHomologacao.REAPRESENTADA,
        )

        status = validar_evento_no_estado_homologacao(
            status_atual=status,
            evento="ANALISE_INICIADA",
        )

        self.assertEqual(
            status,
            StatusHomologacao.EM_ANALISE,
        )

if __name__ == "__main__":
    unittest.main()