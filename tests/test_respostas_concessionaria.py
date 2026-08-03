"""
Testes das regras locais das Respostas da concessionária.
"""

import unittest
from datetime import date, datetime

from app.dominio.exigencias_concessionaria import (
    criar_dados_exigencia,
)
from app.dominio.respostas_concessionaria import (
    CaraterRejeicao,
    TipoRespostaConcessionaria,
    carater_rejeicao_valido,
    criar_dados_resposta_aprovacao,
    criar_dados_resposta_exigencia,
    criar_dados_resposta_inicio_analise,
    criar_dados_resposta_recebimento,
    criar_dados_resposta_rejeicao,
    obter_rotulo_carater_rejeicao,
    obter_rotulo_tipo_resposta,
    obter_status_resultante_resposta,
    tipo_resposta_concessionaria_valido,
    validar_datas_resposta,
    validar_resposta_concessionaria,
)
from app.dominio.status_submissao import (
    StatusAnaliseSubmissao,
)


class TestTiposRespostaConcessionaria(unittest.TestCase):

    def test_enum_deve_possuir_cinco_tipos(self):
        self.assertEqual(
            len(TipoRespostaConcessionaria),
            5,
        )

    def test_carater_rejeicao_deve_possuir_tres_valores(self):
        self.assertEqual(
            len(CaraterRejeicao),
            3,
        )

    def test_tipo_valido_deve_aceitar_enum(self):
        self.assertTrue(
            tipo_resposta_concessionaria_valido(
                TipoRespostaConcessionaria.APROVACAO
            )
        )

    def test_tipo_valido_deve_aceitar_texto(self):
        self.assertTrue(
            tipo_resposta_concessionaria_valido(
                "REJEICAO"
            )
        )

    def test_tipo_invalido_deve_retornar_false(self):
        self.assertFalse(
            tipo_resposta_concessionaria_valido(
                "INEXISTENTE"
            )
        )

    def test_carater_valido_deve_aceitar_texto(self):
        self.assertTrue(
            carater_rejeicao_valido("CORRIGIVEL")
        )

    def test_carater_invalido_deve_retornar_false(self):
        self.assertFalse(
            carater_rejeicao_valido("TEMPORARIA")
        )

    def test_rotulo_aprovacao(self):
        self.assertEqual(
            obter_rotulo_tipo_resposta("APROVACAO"),
            "Aprovação",
        )

    def test_rotulo_rejeicao_definitiva(self):
        self.assertEqual(
            obter_rotulo_carater_rejeicao("DEFINITIVA"),
            "Definitiva",
        )


class TestStatusResultanteResposta(unittest.TestCase):

    def test_recebimento_deve_resultar_em_recebida(self):
        resultado = obter_status_resultante_resposta(
            "RECEBIMENTO_CONFIRMADO"
        )

        self.assertEqual(
            resultado,
            StatusAnaliseSubmissao.RECEBIDA,
        )

    def test_inicio_analise_deve_resultar_em_em_analise(self):
        resultado = obter_status_resultante_resposta(
            "ANALISE_INICIADA"
        )

        self.assertEqual(
            resultado,
            StatusAnaliseSubmissao.EM_ANALISE,
        )

    def test_exigencia_deve_resultar_em_com_exigencia(self):
        resultado = obter_status_resultante_resposta(
            "EXIGENCIA"
        )

        self.assertEqual(
            resultado,
            StatusAnaliseSubmissao.COM_EXIGENCIA,
        )

    def test_aprovacao_deve_resultar_em_aprovada(self):
        resultado = obter_status_resultante_resposta(
            "APROVACAO"
        )

        self.assertEqual(
            resultado,
            StatusAnaliseSubmissao.APROVADA,
        )

    def test_rejeicao_deve_resultar_em_rejeitada(self):
        resultado = obter_status_resultante_resposta(
            "REJEICAO"
        )

        self.assertEqual(
            resultado,
            StatusAnaliseSubmissao.REJEITADA,
        )

    def test_tipo_invalido_deve_retornar_none(self):
        resultado = obter_status_resultante_resposta(
            "INEXISTENTE"
        )

        self.assertIsNone(resultado)


class TestDatasResposta(unittest.TestCase):

    def test_deve_aceitar_datas_em_texto(self):
        resultado = validar_datas_resposta(
            "2026-07-28",
            "2026-07-30",
        )

        self.assertEqual(
            resultado,
            ("2026-07-28", "2026-07-30"),
        )

    def test_deve_aceitar_objetos_date(self):
        resultado = validar_datas_resposta(
            date(2026, 7, 28),
            date(2026, 7, 30),
        )

        self.assertEqual(
            resultado,
            ("2026-07-28", "2026-07-30"),
        )

    def test_deve_aceitar_objetos_datetime(self):
        resultado = validar_datas_resposta(
            datetime(2026, 7, 28, 10, 30),
            datetime(2026, 7, 30, 14, 20),
        )

        self.assertEqual(
            resultado,
            ("2026-07-28", "2026-07-30"),
        )

    def test_data_registro_pode_ser_igual_a_resposta(self):
        resultado = validar_datas_resposta(
            "2026-07-30",
            "2026-07-30",
        )

        self.assertEqual(
            resultado,
            ("2026-07-30", "2026-07-30"),
        )

    def test_data_registro_anterior_deve_ser_rejeitada(self):
        with self.assertRaises(ValueError):
            validar_datas_resposta(
                "2026-07-30",
                "2026-07-29",
            )

    def test_data_em_formato_invalido_deve_ser_rejeitada(self):
        with self.assertRaises(ValueError):
            validar_datas_resposta(
                "30/07/2026",
                "2026-07-30",
            )


class TestCriacaoRespostasSimples(unittest.TestCase):

    def test_deve_criar_confirmacao_recebimento(self):
        resposta = criar_dados_resposta_recebimento(
            codigo=1,
            numero_sequencial=1,
            data_resposta="2026-07-29",
            data_registro="2026-07-30",
            responsavel_registro="Ana Lima",
        )

        self.assertEqual(
            resposta["tipo"],
            "RECEBIMENTO_CONFIRMADO",
        )
        self.assertEqual(
            resposta["responsavel_registro"],
            "Ana Lima",
        )
        self.assertEqual(resposta["exigencias"], [])

    def test_deve_criar_inicio_analise(self):
        resposta = criar_dados_resposta_inicio_analise(
            codigo=2,
            numero_sequencial=2,
            data_resposta="2026-07-30",
            data_registro="2026-07-30",
            responsavel_registro="Carlos Souza",
            descricao="Análise técnica iniciada.",
        )

        self.assertEqual(
            resposta["tipo"],
            "ANALISE_INICIADA",
        )
        self.assertEqual(
            resposta["descricao"],
            "Análise técnica iniciada.",
        )

    def test_responsavel_vazio_deve_ser_rejeitado(self):
        with self.assertRaises(ValueError):
            criar_dados_resposta_recebimento(
                codigo=1,
                numero_sequencial=1,
                data_resposta="2026-07-30",
                data_registro="2026-07-30",
                responsavel_registro="   ",
            )

    def test_codigo_bool_deve_ser_rejeitado(self):
        with self.assertRaises(ValueError):
            criar_dados_resposta_recebimento(
                codigo=True,
                numero_sequencial=1,
                data_resposta="2026-07-30",
                data_registro="2026-07-30",
                responsavel_registro="Ana",
            )


class TestCriacaoRespostaExigencia(unittest.TestCase):

    def setUp(self):
        self.exigencia = criar_dados_exigencia(
            codigo=1,
            numero_sequencial=1,
            tipo="CORRECAO_DOCUMENTAL",
            descricao="Corrigir diagrama.",
            codigos_documentos_afetados=[3],
        )

    def test_deve_criar_resposta_com_exigencia(self):
        resposta = criar_dados_resposta_exigencia(
            codigo=3,
            numero_sequencial=3,
            data_resposta="2026-07-30",
            data_registro="2026-07-30",
            responsavel_registro="Ana Lima",
            descricao="Foram identificadas pendências.",
            exigencias=[self.exigencia],
            prazo_atendimento="30 dias",
        )

        self.assertEqual(
            resposta["tipo"],
            "EXIGENCIA",
        )
        self.assertEqual(
            len(resposta["exigencias"]),
            1,
        )
        self.assertEqual(
            resposta["prazo_atendimento"],
            "30 dias",
        )

    def test_lista_vazia_deve_ser_rejeitada(self):
        with self.assertRaises(ValueError):
            criar_dados_resposta_exigencia(
                codigo=3,
                numero_sequencial=3,
                data_resposta="2026-07-30",
                data_registro="2026-07-30",
                responsavel_registro="Ana Lima",
                descricao="Foram identificadas pendências.",
                exigencias=[],
            )

    def test_exigencias_devem_formar_lista(self):
        with self.assertRaises(ValueError):
            criar_dados_resposta_exigencia(
                codigo=3,
                numero_sequencial=3,
                data_resposta="2026-07-30",
                data_registro="2026-07-30",
                responsavel_registro="Ana Lima",
                descricao="Foram identificadas pendências.",
                exigencias=self.exigencia,
            )

    def test_codigos_duplicados_devem_ser_rejeitados(self):
        segunda_exigencia = criar_dados_exigencia(
            codigo=1,
            numero_sequencial=2,
            tipo="ESCLARECIMENTO",
            descricao="Esclarecer informação.",
        )

        with self.assertRaises(ValueError):
            criar_dados_resposta_exigencia(
                codigo=3,
                numero_sequencial=3,
                data_resposta="2026-07-30",
                data_registro="2026-07-30",
                responsavel_registro="Ana Lima",
                descricao="Pendências identificadas.",
                exigencias=[
                    self.exigencia,
                    segunda_exigencia,
                ],
            )

    def test_numeros_sequenciais_duplicados_devem_ser_rejeitados(self):
        segunda_exigencia = criar_dados_exigencia(
            codigo=2,
            numero_sequencial=1,
            tipo="ESCLARECIMENTO",
            descricao="Esclarecer informação.",
        )

        with self.assertRaises(ValueError):
            criar_dados_resposta_exigencia(
                codigo=3,
                numero_sequencial=3,
                data_resposta="2026-07-30",
                data_registro="2026-07-30",
                responsavel_registro="Ana Lima",
                descricao="Pendências identificadas.",
                exigencias=[
                    self.exigencia,
                    segunda_exigencia,
                ],
            )

    def test_deve_criar_nova_lista_de_exigencias(self):
        exigencias = [self.exigencia]

        resposta = criar_dados_resposta_exigencia(
            codigo=3,
            numero_sequencial=3,
            data_resposta="2026-07-30",
            data_registro="2026-07-30",
            responsavel_registro="Ana Lima",
            descricao="Pendências identificadas.",
            exigencias=exigencias,
        )

        self.assertIsNot(
            resposta["exigencias"],
            exigencias,
        )


class TestCriacaoRespostaAprovacao(unittest.TestCase):

    def test_deve_criar_aprovacao(self):
        resposta = criar_dados_resposta_aprovacao(
            codigo=4,
            numero_sequencial=4,
            data_resposta="2026-07-30",
            data_registro="2026-07-30",
            responsavel_registro="Ana Lima",
            descricao="Projeto aprovado.",
            identificador_aprovacao="APR-2026-001",
        )

        self.assertEqual(
            resposta["tipo"],
            "APROVACAO",
        )
        self.assertEqual(
            resposta["identificador_aprovacao"],
            "APR-2026-001",
        )
        self.assertIsNone(
            resposta["carater_rejeicao"]
        )

    def test_identificador_aprovacao_deve_ser_opcional(self):
        resposta = criar_dados_resposta_aprovacao(
            codigo=4,
            numero_sequencial=4,
            data_resposta="2026-07-30",
            data_registro="2026-07-30",
            responsavel_registro="Ana Lima",
        )

        self.assertIsNone(
            resposta["identificador_aprovacao"]
        )


class TestCriacaoRespostaRejeicao(unittest.TestCase):

    def test_deve_criar_rejeicao_corrigivel(self):
        resposta = criar_dados_resposta_rejeicao(
            codigo=5,
            numero_sequencial=5,
            data_resposta="2026-07-30",
            data_registro="2026-07-30",
            responsavel_registro="Ana Lima",
            descricao="Dados técnicos inconsistentes.",
            carater_rejeicao=CaraterRejeicao.CORRIGIVEL,
        )

        self.assertEqual(
            resposta["tipo"],
            "REJEICAO",
        )
        self.assertEqual(
            resposta["carater_rejeicao"],
            "CORRIGIVEL",
        )

    def test_rejeicao_sem_descricao_deve_ser_rejeitada(self):
        with self.assertRaises(ValueError):
            criar_dados_resposta_rejeicao(
                codigo=5,
                numero_sequencial=5,
                data_resposta="2026-07-30",
                data_registro="2026-07-30",
                responsavel_registro="Ana Lima",
                descricao="  ",
                carater_rejeicao="CORRIGIVEL",
            )

    def test_carater_invalido_deve_ser_rejeitado(self):
        with self.assertRaises(ValueError):
            criar_dados_resposta_rejeicao(
                codigo=5,
                numero_sequencial=5,
                data_resposta="2026-07-30",
                data_registro="2026-07-30",
                responsavel_registro="Ana Lima",
                descricao="Dados inconsistentes.",
                carater_rejeicao="TEMPORARIA",
            )


class TestValidacaoRespostaConcessionaria(unittest.TestCase):

    def test_resposta_recebimento_criada_deve_ser_valida(self):
        resposta = criar_dados_resposta_recebimento(
            codigo=1,
            numero_sequencial=1,
            data_resposta="2026-07-30",
            data_registro="2026-07-30",
            responsavel_registro="Ana Lima",
        )

        self.assertTrue(
            validar_resposta_concessionaria(resposta)
        )

    def test_resposta_exigencia_criada_deve_ser_valida(self):
        exigencia = criar_dados_exigencia(
            codigo=1,
            numero_sequencial=1,
            tipo="ESCLARECIMENTO",
            descricao="Esclarecer informação.",
        )

        resposta = criar_dados_resposta_exigencia(
            codigo=2,
            numero_sequencial=2,
            data_resposta="2026-07-30",
            data_registro="2026-07-30",
            responsavel_registro="Ana Lima",
            descricao="Esclarecimento necessário.",
            exigencias=[exigencia],
        )

        self.assertTrue(
            validar_resposta_concessionaria(resposta)
        )

    def test_resposta_deve_ser_dicionario(self):
        with self.assertRaises(ValueError):
            validar_resposta_concessionaria([])

    def test_campo_ausente_deve_ser_rejeitado(self):
        resposta = criar_dados_resposta_recebimento(
            codigo=1,
            numero_sequencial=1,
            data_resposta="2026-07-30",
            data_registro="2026-07-30",
            responsavel_registro="Ana Lima",
        )

        del resposta["tipo"]

        with self.assertRaises(ValueError):
            validar_resposta_concessionaria(resposta)

    def test_aprovacao_com_carater_rejeicao_deve_ser_rejeitada(self):
        resposta = criar_dados_resposta_aprovacao(
            codigo=1,
            numero_sequencial=1,
            data_resposta="2026-07-30",
            data_registro="2026-07-30",
            responsavel_registro="Ana Lima",
        )

        resposta["carater_rejeicao"] = "DEFINITIVA"

        with self.assertRaises(ValueError):
            validar_resposta_concessionaria(resposta)

    def test_recebimento_com_exigencia_deve_ser_rejeitado(self):
        resposta = criar_dados_resposta_recebimento(
            codigo=1,
            numero_sequencial=1,
            data_resposta="2026-07-30",
            data_registro="2026-07-30",
            responsavel_registro="Ana Lima",
        )

        resposta["exigencias"] = [
            criar_dados_exigencia(
                codigo=1,
                numero_sequencial=1,
                tipo="OUTRA",
                descricao="Solicitação.",
            )
        ]

        with self.assertRaises(ValueError):
            validar_resposta_concessionaria(resposta)

    def test_prazo_so_deve_ser_permitido_em_exigencia(self):
        resposta = criar_dados_resposta_recebimento(
            codigo=1,
            numero_sequencial=1,
            data_resposta="2026-07-30",
            data_registro="2026-07-30",
            responsavel_registro="Ana Lima",
        )

        resposta["prazo_atendimento"] = "30 dias"

        with self.assertRaises(ValueError):
            validar_resposta_concessionaria(resposta)


if __name__ == "__main__":
    unittest.main()