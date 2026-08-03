"""
Testes das regras locais das Submissões da Homologação.
"""

import unittest

from app.dominio.respostas_concessionaria import (
    criar_dados_resposta_aprovacao,
)
from app.dominio.status_submissao import (
    StatusAnaliseSubmissao,
    StatusOperacionalSubmissao,
)
from app.dominio.submissoes_homologacao import (
    CanalEnvioSubmissao,
    TipoSubmissao,
    canal_envio_submissao_valido,
    criar_dados_submissao,
    criar_referencia_documento,
    obter_rotulo_canal_envio_submissao,
    obter_rotulo_tipo_submissao,
    submissao_esta_em_preparacao,
    submissao_foi_enviada,
    submissao_foi_protocolada,
    tipo_submissao_valido,
    validar_referencia_documento,
    validar_submissao,
)


class TestTiposSubmissao(unittest.TestCase):

    def test_tipo_submissao_deve_possuir_tres_valores(self):
        self.assertEqual(len(TipoSubmissao), 3)

    def test_canal_envio_deve_possuir_quatro_valores(self):
        self.assertEqual(len(CanalEnvioSubmissao), 4)

    def test_tipo_valido_deve_aceitar_enum(self):
        self.assertTrue(
            tipo_submissao_valido(TipoSubmissao.REENVIO)
        )

    def test_tipo_valido_deve_aceitar_texto(self):
        self.assertTrue(
            tipo_submissao_valido("COMPLEMENTACAO")
        )

    def test_tipo_invalido_deve_retornar_false(self):
        self.assertFalse(
            tipo_submissao_valido("INEXISTENTE")
        )

    def test_canal_valido_deve_aceitar_texto(self):
        self.assertTrue(
            canal_envio_submissao_valido("PORTAL")
        )

    def test_canal_invalido_deve_retornar_false(self):
        self.assertFalse(
            canal_envio_submissao_valido("WHATSAPP")
        )

    def test_rotulo_tipo_complementacao(self):
        self.assertEqual(
            obter_rotulo_tipo_submissao("COMPLEMENTACAO"),
            "Complementação",
        )

    def test_rotulo_canal_email(self):
        self.assertEqual(
            obter_rotulo_canal_envio_submissao("EMAIL"),
            "E-mail",
        )


class TestReferenciaDocumento(unittest.TestCase):

    def test_deve_criar_referencia_documental(self):
        referencia = criar_referencia_documento(
            codigo_documento=3,
            numero_versao=2,
        )

        self.assertEqual(
            referencia,
            {
                "codigo_documento": 3,
                "numero_versao": 2,
            },
        )

    def test_referencia_criada_deve_ser_valida(self):
        referencia = criar_referencia_documento(3, 2)

        self.assertTrue(
            validar_referencia_documento(referencia)
        )

    def test_codigo_documento_zero_deve_ser_rejeitado(self):
        with self.assertRaises(ValueError):
            criar_referencia_documento(0, 1)

    def test_numero_versao_zero_deve_ser_rejeitado(self):
        with self.assertRaises(ValueError):
            criar_referencia_documento(3, 0)

    def test_bool_nao_deve_ser_aceito_como_codigo(self):
        with self.assertRaises(ValueError):
            criar_referencia_documento(True, 1)

    def test_referencia_deve_ser_dicionario(self):
        with self.assertRaises(ValueError):
            validar_referencia_documento([])

    def test_campo_ausente_deve_ser_rejeitado(self):
        referencia = {
            "codigo_documento": 3,
        }

        with self.assertRaises(ValueError):
            validar_referencia_documento(referencia)


class TestCriacaoSubmissaoInicial(unittest.TestCase):

    def setUp(self):
        self.referencia = criar_referencia_documento(3, 1)

    def test_deve_criar_submissao_inicial(self):
        submissao = criar_dados_submissao(
            codigo=1,
            numero_sequencial=1,
            tipo="INICIAL",
            data_criacao="2026-07-30",
            responsavel_criacao="Jefferson",
            pacote_documental=[self.referencia],
        )

        self.assertEqual(submissao["codigo"], 1)
        self.assertEqual(submissao["tipo"], "INICIAL")
        self.assertIsNone(
            submissao["codigo_submissao_origem"]
        )
        self.assertEqual(
            submissao["status_operacional"],
            "EM_PREPARACAO",
        )
        self.assertEqual(
            submissao["status_analise"],
            "SEM_RESPOSTA",
        )

    def test_campos_de_envio_devem_iniciar_vazios(self):
        submissao = criar_dados_submissao(
            codigo=1,
            numero_sequencial=1,
            tipo="INICIAL",
            data_criacao="2026-07-30",
            responsavel_criacao="Jefferson",
        )

        self.assertIsNone(submissao["canal_envio"])
        self.assertIsNone(submissao["data_envio"])
        self.assertIsNone(submissao["responsavel_envio"])
        self.assertIsNone(submissao["protocolo"])
        self.assertIsNone(submissao["data_protocolo"])
        self.assertEqual(submissao["respostas"], [])

    def test_inicial_nao_pode_possuir_origem(self):
        with self.assertRaises(ValueError):
            criar_dados_submissao(
                codigo=1,
                numero_sequencial=1,
                tipo="INICIAL",
                data_criacao="2026-07-30",
                responsavel_criacao="Jefferson",
                codigo_submissao_origem=5,
            )

    def test_inicial_nao_pode_atender_exigencias(self):
        with self.assertRaises(ValueError):
            criar_dados_submissao(
                codigo=1,
                numero_sequencial=1,
                tipo="INICIAL",
                data_criacao="2026-07-30",
                responsavel_criacao="Jefferson",
                codigos_exigencias_relacionadas=[4],
            )

    def test_codigo_zero_deve_ser_rejeitado(self):
        with self.assertRaises(ValueError):
            criar_dados_submissao(
                codigo=0,
                numero_sequencial=1,
                tipo="INICIAL",
                data_criacao="2026-07-30",
                responsavel_criacao="Jefferson",
            )

    def test_responsavel_vazio_deve_ser_rejeitado(self):
        with self.assertRaises(ValueError):
            criar_dados_submissao(
                codigo=1,
                numero_sequencial=1,
                tipo="INICIAL",
                data_criacao="2026-07-30",
                responsavel_criacao="   ",
            )


class TestCriacaoComplementacaoReenvio(unittest.TestCase):

    def test_complementacao_deve_possuir_origem(self):
        submissao = criar_dados_submissao(
            codigo=2,
            numero_sequencial=2,
            tipo="COMPLEMENTACAO",
            data_criacao="2026-07-30",
            responsavel_criacao="Jefferson",
            codigo_submissao_origem=1,
            codigo_resposta_origem=1,
            codigos_exigencias_relacionadas=[5],
        )

        self.assertEqual(
            submissao["codigo_submissao_origem"],
            1,
        )

        self.assertEqual(
            submissao["codigo_resposta_origem"],
            1,
        )

        self.assertEqual(
            submissao["codigos_exigencias_relacionadas"],
            [5],
        )

    def test_reenvio_deve_possuir_origem(self):
        submissao = criar_dados_submissao(
            codigo=3,
            numero_sequencial=3,
            tipo="REENVIO",
            data_criacao="2026-07-30",
            responsavel_criacao="Jefferson",
            codigo_submissao_origem=2,
            codigo_resposta_origem=1,
        )

        self.assertEqual(
            submissao["tipo"],
            "REENVIO",
        )

        self.assertEqual(
            submissao["codigo_submissao_origem"],
            2,
        )

        self.assertEqual(
            submissao["codigo_resposta_origem"],
            1,
        )

    def test_complementacao_sem_origem_deve_ser_rejeitada(self):
        with self.assertRaises(ValueError):
            criar_dados_submissao(
                codigo=2,
                numero_sequencial=2,
                tipo="COMPLEMENTACAO",
                data_criacao="2026-07-30",
                responsavel_criacao="Jefferson",
            )

    def test_reenvio_sem_origem_deve_ser_rejeitado(self):
        with self.assertRaises(ValueError):
            criar_dados_submissao(
                codigo=2,
                numero_sequencial=2,
                tipo="REENVIO",
                data_criacao="2026-07-30",
                responsavel_criacao="Jefferson",
            )

    def test_submissao_nao_pode_ser_origem_de_si_mesma(self):
        with self.assertRaisesRegex(
            ValueError,
            "não pode apontar para si mesma",
        ):
            criar_dados_submissao(
                codigo=2,
                numero_sequencial=2,
                tipo="REENVIO",
                data_criacao="2026-07-30",
                responsavel_criacao="Jefferson",
                codigo_submissao_origem=2,
                codigo_resposta_origem=1,
            )

    def test_exigencia_duplicada_deve_ser_rejeitada(self):
        with self.assertRaises(ValueError):
            criar_dados_submissao(
                codigo=2,
                numero_sequencial=2,
                tipo="COMPLEMENTACAO",
                data_criacao="2026-07-30",
                responsavel_criacao="Jefferson",
                codigo_submissao_origem=1,
                codigos_exigencias_relacionadas=[5, 5],
            )


class TestPacoteDocumental(unittest.TestCase):

    def test_deve_copiar_lista_do_pacote(self):
        pacote = [
            criar_referencia_documento(3, 1),
        ]

        submissao = criar_dados_submissao(
            codigo=1,
            numero_sequencial=1,
            tipo="INICIAL",
            data_criacao="2026-07-30",
            responsavel_criacao="Jefferson",
            pacote_documental=pacote,
        )

        self.assertIsNot(
            submissao["pacote_documental"],
            pacote,
        )

    def test_documento_duplicado_deve_ser_rejeitado(self):
        pacote = [
            criar_referencia_documento(3, 1),
            criar_referencia_documento(3, 2),
        ]

        with self.assertRaises(ValueError):
            criar_dados_submissao(
                codigo=1,
                numero_sequencial=1,
                tipo="INICIAL",
                data_criacao="2026-07-30",
                responsavel_criacao="Jefferson",
                pacote_documental=pacote,
            )

    def test_pacote_deve_ser_lista(self):
        with self.assertRaises(ValueError):
            criar_dados_submissao(
                codigo=1,
                numero_sequencial=1,
                tipo="INICIAL",
                data_criacao="2026-07-30",
                responsavel_criacao="Jefferson",
                pacote_documental={
                    "codigo_documento": 3,
                    "numero_versao": 1,
                },
            )


class TestValidacaoSubmissao(unittest.TestCase):

    def setUp(self):
        self.submissao = criar_dados_submissao(
            codigo=1,
            numero_sequencial=1,
            tipo="INICIAL",
            data_criacao="2026-07-30",
            responsavel_criacao="Jefferson",
            pacote_documental=[
                criar_referencia_documento(3, 1)
            ],
        )

    def test_submissao_criada_deve_ser_valida(self):
        self.assertTrue(
            validar_submissao(self.submissao)
        )

    def test_submissao_deve_ser_dicionario(self):
        with self.assertRaises(ValueError):
            validar_submissao([])

    def test_campo_ausente_deve_ser_rejeitado(self):
        del self.submissao["tipo"]

        with self.assertRaises(ValueError):
            validar_submissao(self.submissao)

    def test_submissao_em_preparacao_nao_pode_ter_envio(self):
        self.submissao["canal_envio"] = "PORTAL"

        with self.assertRaises(ValueError):
            validar_submissao(self.submissao)

    def test_submissao_enviada_completa_deve_ser_valida(self):
        self.submissao["status_operacional"] = (
            StatusOperacionalSubmissao.ENVIADA.value
        )
        self.submissao["canal_envio"] = "PORTAL"
        self.submissao["data_envio"] = "2026-07-30"
        self.submissao["responsavel_envio"] = "Jefferson"

        self.assertTrue(
            validar_submissao(self.submissao)
        )

    def test_submissao_enviada_sem_pacote_deve_ser_rejeitada(self):
        self.submissao["status_operacional"] = "ENVIADA"
        self.submissao["canal_envio"] = "PORTAL"
        self.submissao["data_envio"] = "2026-07-30"
        self.submissao["responsavel_envio"] = "Jefferson"
        self.submissao["pacote_documental"] = []

        with self.assertRaises(ValueError):
            validar_submissao(self.submissao)

    def test_protocolada_deve_possuir_protocolo(self):
        self.submissao["status_operacional"] = "PROTOCOLADA"
        self.submissao["canal_envio"] = "PORTAL"
        self.submissao["data_envio"] = "2026-07-29"
        self.submissao["responsavel_envio"] = "Jefferson"

        with self.assertRaises(ValueError):
            validar_submissao(self.submissao)

    def test_protocolada_completa_deve_ser_valida(self):
        self.submissao["status_operacional"] = "PROTOCOLADA"
        self.submissao["canal_envio"] = "PORTAL"
        self.submissao["data_envio"] = "2026-07-29"
        self.submissao["responsavel_envio"] = "Jefferson"
        self.submissao["protocolo"] = "PROT-2026-001"
        self.submissao["data_protocolo"] = "2026-07-30"

        self.assertTrue(
            validar_submissao(self.submissao)
        )

    def test_data_protocolo_anterior_ao_envio_deve_ser_rejeitada(self):
        self.submissao["status_operacional"] = "PROTOCOLADA"
        self.submissao["canal_envio"] = "PORTAL"
        self.submissao["data_envio"] = "2026-07-30"
        self.submissao["responsavel_envio"] = "Jefferson"
        self.submissao["protocolo"] = "PROT-001"
        self.submissao["data_protocolo"] = "2026-07-29"

        with self.assertRaises(ValueError):
            validar_submissao(self.submissao)

    def test_resposta_em_submissao_nao_enviada_deve_ser_rejeitada(self):
        resposta = criar_dados_resposta_aprovacao(
            codigo=1,
            numero_sequencial=1,
            data_resposta="2026-07-30",
            data_registro="2026-07-30",
            responsavel_registro="Jefferson",
        )

        self.submissao["respostas"] = [resposta]
        self.submissao["status_analise"] = "APROVADA"

        with self.assertRaises(ValueError):
            validar_submissao(self.submissao)

    def test_status_analise_deve_corresponder_ultima_resposta(self):
        resposta = criar_dados_resposta_aprovacao(
            codigo=1,
            numero_sequencial=1,
            data_resposta="2026-07-30",
            data_registro="2026-07-30",
            responsavel_registro="Jefferson",
        )

        self.submissao["status_operacional"] = "ENVIADA"
        self.submissao["canal_envio"] = "PORTAL"
        self.submissao["data_envio"] = "2026-07-30"
        self.submissao["responsavel_envio"] = "Jefferson"
        self.submissao["respostas"] = [resposta]
        self.submissao["status_analise"] = "REJEITADA"

        with self.assertRaises(ValueError):
            validar_submissao(self.submissao)

    def test_resposta_aprovacao_deve_resultar_em_aprovada(self):
        resposta = criar_dados_resposta_aprovacao(
            codigo=1,
            numero_sequencial=1,
            data_resposta="2026-07-30",
            data_registro="2026-07-30",
            responsavel_registro="Jefferson",
        )

        self.submissao["status_operacional"] = "ENVIADA"
        self.submissao["canal_envio"] = "PORTAL"
        self.submissao["data_envio"] = "2026-07-30"
        self.submissao["responsavel_envio"] = "Jefferson"
        self.submissao["respostas"] = [resposta]
        self.submissao["status_analise"] = (
            StatusAnaliseSubmissao.APROVADA.value
        )

        self.assertTrue(
            validar_submissao(self.submissao)
        )


class TestConsultasSubmissao(unittest.TestCase):

    def setUp(self):
        self.submissao = criar_dados_submissao(
            codigo=1,
            numero_sequencial=1,
            tipo="INICIAL",
            data_criacao="2026-07-30",
            responsavel_criacao="Jefferson",
        )

    def test_nova_submissao_deve_estar_em_preparacao(self):
        self.assertTrue(
            submissao_esta_em_preparacao(self.submissao)
        )

    def test_nova_submissao_nao_foi_enviada(self):
        self.assertFalse(
            submissao_foi_enviada(self.submissao)
        )

    def test_enviada_deve_ser_considerada_enviada(self):
        self.submissao["status_operacional"] = "ENVIADA"

        self.assertTrue(
            submissao_foi_enviada(self.submissao)
        )

    def test_protocolada_tambem_deve_ser_considerada_enviada(self):
        self.submissao["status_operacional"] = "PROTOCOLADA"

        self.assertTrue(
            submissao_foi_enviada(self.submissao)
        )

    def test_protocolada_deve_ser_identificada(self):
        self.submissao["status_operacional"] = "PROTOCOLADA"

        self.assertTrue(
            submissao_foi_protocolada(self.submissao)
        )


if __name__ == "__main__":
    unittest.main()