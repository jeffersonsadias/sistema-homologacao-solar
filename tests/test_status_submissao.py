"""
Testes das máquinas de estados da Submissão.

Os testes deste módulo verificam somente os contratos abstratos
dos estados e das transições.

Eles ainda não testam:

- estrutura completa da Submissão;
- envio;
- protocolo;
- Respostas;
- Homologação;
- persistência.
"""

import unittest

from app.dominio.status_submissao import (
    STATUS_ANALISE_INICIAL,
    STATUS_OPERACIONAL_INICIAL,
    StatusAnaliseSubmissao,
    StatusOperacionalSubmissao,
    obter_rotulo_status_analise_submissao,
    obter_rotulo_status_operacional_submissao,
    status_analise_submissao_terminal,
    status_analise_submissao_valido,
    status_operacional_submissao_terminal,
    status_operacional_submissao_valido,
    transicao_analise_submissao_permitida,
    transicao_operacional_submissao_permitida,
    validar_transicao_analise_submissao,
    validar_transicao_operacional_submissao,
)


class TestStatusOperacionalSubmissao(unittest.TestCase):
    """
    Testes do ciclo operacional da Submissão.
    """

    def test_enum_operacional_deve_possuir_cinco_estados(self):
        self.assertEqual(len(StatusOperacionalSubmissao), 5)

    def test_valores_do_enum_operacional_devem_ser_textos(self):
        for status in StatusOperacionalSubmissao:
            self.assertIsInstance(status.value, str)

    def test_status_operacional_inicial_deve_ser_em_preparacao(self):
        self.assertEqual(
            STATUS_OPERACIONAL_INICIAL,
            StatusOperacionalSubmissao.EM_PREPARACAO,
        )

    def test_status_operacional_valido_deve_aceitar_enum(self):
        resultado = status_operacional_submissao_valido(
            StatusOperacionalSubmissao.ENVIADA
        )

        self.assertTrue(resultado)

    def test_status_operacional_valido_deve_aceitar_texto(self):
        resultado = status_operacional_submissao_valido("PROTOCOLADA")

        self.assertTrue(resultado)

    def test_status_operacional_invalido_deve_retornar_false(self):
        resultado = status_operacional_submissao_valido(
            "PROTOCOLIZADA"
        )

        self.assertFalse(resultado)

    def test_em_preparacao_pode_ir_para_pronta(self):
        resultado = transicao_operacional_submissao_permitida(
            StatusOperacionalSubmissao.EM_PREPARACAO,
            StatusOperacionalSubmissao.PRONTA_PARA_ENVIO,
        )

        self.assertTrue(resultado)

    def test_em_preparacao_pode_ser_cancelada(self):
        resultado = transicao_operacional_submissao_permitida(
            "EM_PREPARACAO",
            "CANCELADA",
        )

        self.assertTrue(resultado)

    def test_em_preparacao_nao_pode_ir_diretamente_para_enviada(self):
        resultado = transicao_operacional_submissao_permitida(
            "EM_PREPARACAO",
            "ENVIADA",
        )

        self.assertFalse(resultado)

    def test_pronta_pode_retornar_para_preparacao(self):
        resultado = transicao_operacional_submissao_permitida(
            "PRONTA_PARA_ENVIO",
            "EM_PREPARACAO",
        )

        self.assertTrue(resultado)

    def test_pronta_pode_ser_enviada(self):
        resultado = transicao_operacional_submissao_permitida(
            "PRONTA_PARA_ENVIO",
            "ENVIADA",
        )

        self.assertTrue(resultado)

    def test_enviada_pode_ser_protocolada(self):
        resultado = transicao_operacional_submissao_permitida(
            "ENVIADA",
            "PROTOCOLADA",
        )

        self.assertTrue(resultado)

    def test_enviada_nao_pode_ser_cancelada(self):
        resultado = transicao_operacional_submissao_permitida(
            "ENVIADA",
            "CANCELADA",
        )

        self.assertFalse(resultado)

    def test_protocolada_deve_ser_terminal(self):
        resultado = status_operacional_submissao_terminal(
            StatusOperacionalSubmissao.PROTOCOLADA
        )

        self.assertTrue(resultado)

    def test_cancelada_deve_ser_terminal(self):
        resultado = status_operacional_submissao_terminal("CANCELADA")

        self.assertTrue(resultado)

    def test_enviada_nao_deve_ser_terminal(self):
        resultado = status_operacional_submissao_terminal("ENVIADA")

        self.assertFalse(resultado)

    def test_estado_operacional_invalido_nao_deve_ser_terminal(self):
        resultado = status_operacional_submissao_terminal(
            "ESTADO_INEXISTENTE"
        )

        self.assertFalse(resultado)

    def test_validar_transicao_operacional_valida_deve_retornar_true(self):
        resultado = validar_transicao_operacional_submissao(
            "PRONTA_PARA_ENVIO",
            "ENVIADA",
        )

        self.assertTrue(resultado)

    def test_validar_transicao_operacional_invalida_deve_lancar_erro(self):
        with self.assertRaises(ValueError):
            validar_transicao_operacional_submissao(
                "EM_PREPARACAO",
                "PROTOCOLADA",
            )

    def test_validar_status_operacional_atual_inexistente_deve_lancar_erro(
        self,
    ):
        with self.assertRaises(ValueError):
            validar_transicao_operacional_submissao(
                "INEXISTENTE",
                "ENVIADA",
            )

    def test_rotulo_de_protocolada_deve_ser_protocolada(self):
        resultado = obter_rotulo_status_operacional_submissao(
            StatusOperacionalSubmissao.PROTOCOLADA
        )

        self.assertEqual(resultado, "Protocolada")

    def test_rotulo_operacional_invalido_deve_retornar_none(self):
        resultado = obter_rotulo_status_operacional_submissao(
            "INEXISTENTE"
        )

        self.assertIsNone(resultado)


class TestStatusAnaliseSubmissao(unittest.TestCase):
    """
    Testes do ciclo de análise da Submissão.
    """

    def test_enum_analise_deve_possuir_seis_estados(self):
        self.assertEqual(len(StatusAnaliseSubmissao), 6)

    def test_valores_do_enum_analise_devem_ser_textos(self):
        for status in StatusAnaliseSubmissao:
            self.assertIsInstance(status.value, str)

    def test_status_analise_inicial_deve_ser_sem_resposta(self):
        self.assertEqual(
            STATUS_ANALISE_INICIAL,
            StatusAnaliseSubmissao.SEM_RESPOSTA,
        )

    def test_status_analise_valido_deve_aceitar_enum(self):
        resultado = status_analise_submissao_valido(
            StatusAnaliseSubmissao.EM_ANALISE
        )

        self.assertTrue(resultado)

    def test_status_analise_valido_deve_aceitar_texto(self):
        resultado = status_analise_submissao_valido("APROVADA")

        self.assertTrue(resultado)

    def test_status_analise_invalido_deve_retornar_false(self):
        resultado = status_analise_submissao_valido("APROVADO")

        self.assertFalse(resultado)

    def test_sem_resposta_pode_ir_para_recebida(self):
        resultado = transicao_analise_submissao_permitida(
            "SEM_RESPOSTA",
            "RECEBIDA",
        )

        self.assertTrue(resultado)

    def test_sem_resposta_pode_ir_diretamente_para_em_analise(self):
        resultado = transicao_analise_submissao_permitida(
            "SEM_RESPOSTA",
            "EM_ANALISE",
        )

        self.assertTrue(resultado)

    def test_sem_resposta_pode_ir_diretamente_para_aprovada(self):
        resultado = transicao_analise_submissao_permitida(
            "SEM_RESPOSTA",
            "APROVADA",
        )

        self.assertTrue(resultado)

    def test_sem_resposta_pode_ir_diretamente_para_rejeitada(self):
        resultado = transicao_analise_submissao_permitida(
            "SEM_RESPOSTA",
            "REJEITADA",
        )

        self.assertTrue(resultado)

    def test_recebida_pode_ir_para_em_analise(self):
        resultado = transicao_analise_submissao_permitida(
            "RECEBIDA",
            "EM_ANALISE",
        )

        self.assertTrue(resultado)

    def test_em_analise_pode_ir_para_com_exigencia(self):
        resultado = transicao_analise_submissao_permitida(
            "EM_ANALISE",
            "COM_EXIGENCIA",
        )

        self.assertTrue(resultado)

    def test_em_analise_pode_ir_para_aprovada(self):
        resultado = transicao_analise_submissao_permitida(
            "EM_ANALISE",
            "APROVADA",
        )

        self.assertTrue(resultado)

    def test_em_analise_pode_ir_para_rejeitada(self):
        resultado = transicao_analise_submissao_permitida(
            "EM_ANALISE",
            "REJEITADA",
        )

        self.assertTrue(resultado)

    def test_com_exigencia_deve_ser_terminal(self):
        resultado = status_analise_submissao_terminal(
            "COM_EXIGENCIA"
        )

        self.assertTrue(resultado)

    def test_aprovada_deve_ser_terminal(self):
        resultado = status_analise_submissao_terminal("APROVADA")

        self.assertTrue(resultado)

    def test_rejeitada_deve_ser_terminal(self):
        resultado = status_analise_submissao_terminal("REJEITADA")

        self.assertTrue(resultado)

    def test_em_analise_nao_deve_ser_terminal(self):
        resultado = status_analise_submissao_terminal("EM_ANALISE")

        self.assertFalse(resultado)

    def test_com_exigencia_nao_pode_retornar_para_em_analise(self):
        resultado = transicao_analise_submissao_permitida(
            "COM_EXIGENCIA",
            "EM_ANALISE",
        )

        self.assertFalse(resultado)

    def test_aprovada_nao_pode_receber_nova_transicao(self):
        resultado = transicao_analise_submissao_permitida(
            "APROVADA",
            "REJEITADA",
        )

        self.assertFalse(resultado)

    def test_validar_transicao_analise_valida_deve_retornar_true(self):
        resultado = validar_transicao_analise_submissao(
            "RECEBIDA",
            "EM_ANALISE",
        )

        self.assertTrue(resultado)

    def test_validar_transicao_analise_invalida_deve_lancar_erro(self):
        with self.assertRaises(ValueError):
            validar_transicao_analise_submissao(
                "APROVADA",
                "EM_ANALISE",
            )

    def test_validar_novo_status_analise_inexistente_deve_lancar_erro(
        self,
    ):
        with self.assertRaises(ValueError):
            validar_transicao_analise_submissao(
                "SEM_RESPOSTA",
                "INEXISTENTE",
            )

    def test_rotulo_com_exigencia_deve_ser_amigavel(self):
        resultado = obter_rotulo_status_analise_submissao(
            StatusAnaliseSubmissao.COM_EXIGENCIA
        )

        self.assertEqual(resultado, "Com exigência")

    def test_rotulo_analise_invalido_deve_retornar_none(self):
        resultado = obter_rotulo_status_analise_submissao(
            "INEXISTENTE"
        )

        self.assertIsNone(resultado)


if __name__ == "__main__":
    unittest.main()