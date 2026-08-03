"""
Testes das regras locais das Exigências da concessionária.
"""

import unittest

from app.dominio.exigencias_concessionaria import (
    STATUS_INICIAL_ATENDIMENTO_EXIGENCIA,
    StatusAtendimentoExigencia,
    TipoExigencia,
    criar_dados_exigencia,
    exigencia_esta_atendida,
    exigencia_esta_pendente,
    obter_rotulo_status_atendimento_exigencia,
    obter_rotulo_tipo_exigencia,
    status_atendimento_exigencia_terminal,
    status_atendimento_exigencia_valido,
    tipo_exigencia_valido,
    transicao_status_exigencia_permitida,
    validar_compatibilidade_exigencia_submissao,
    validar_exigencia,
    validar_transicao_status_exigencia,
)


class TestCriacaoExigencia(unittest.TestCase):
    """
    Testes da criação da estrutura inicial.
    """

    def test_deve_criar_exigencia_valida(self):
        exigencia = criar_dados_exigencia(
            codigo=1,
            numero_sequencial=1,
            tipo=TipoExigencia.CORRECAO_DOCUMENTAL,
            descricao="Corrigir o diagrama unifilar.",
            codigos_documentos_afetados=[3],
        )

        self.assertEqual(exigencia["codigo"], 1)
        self.assertEqual(exigencia["numero_sequencial"], 1)
        self.assertEqual(
            exigencia["tipo"],
            "CORRECAO_DOCUMENTAL",
        )
        self.assertEqual(
            exigencia["descricao"],
            "Corrigir o diagrama unifilar.",
        )
        self.assertEqual(
            exigencia["codigos_documentos_afetados"],
            [3],
        )

    def test_status_inicial_deve_ser_pendente(self):
        exigencia = criar_dados_exigencia(
            codigo=1,
            numero_sequencial=1,
            tipo="ESCLARECIMENTO",
            descricao="Esclarecer a divisão dos créditos.",
        )

        self.assertEqual(
            exigencia["status_atendimento"],
            StatusAtendimentoExigencia.PENDENTE.value,
        )

    def test_constante_inicial_deve_ser_pendente(self):
        self.assertEqual(
            STATUS_INICIAL_ATENDIMENTO_EXIGENCIA,
            StatusAtendimentoExigencia.PENDENTE,
        )

    def test_campos_de_atendimento_devem_iniciar_vazios(self):
        exigencia = criar_dados_exigencia(
            codigo=2,
            numero_sequencial=1,
            tipo="COMPLEMENTACAO_DOCUMENTAL",
            descricao="Anexar documento do titular.",
        )

        self.assertIsNone(
            exigencia["codigo_submissao_atendimento"]
        )
        self.assertIsNone(exigencia["data_atendimento"])
        self.assertIsNone(
            exigencia["responsavel_atendimento"]
        )
        self.assertIsNone(
            exigencia["observacoes_atendimento"]
        )

    def test_lista_de_documentos_deve_iniciar_vazia(self):
        exigencia = criar_dados_exigencia(
            codigo=1,
            numero_sequencial=1,
            tipo="COMPLEMENTACAO_DOCUMENTAL",
            descricao="Apresentar novo formulário.",
        )

        self.assertEqual(
            exigencia["codigos_documentos_afetados"],
            [],
        )

    def test_deve_remover_espacos_externos_da_descricao(self):
        exigencia = criar_dados_exigencia(
            codigo=1,
            numero_sequencial=1,
            tipo="OUTRA",
            descricao="  Verificar dados informados.  ",
        )

        self.assertEqual(
            exigencia["descricao"],
            "Verificar dados informados.",
        )

    def test_codigo_zero_deve_ser_rejeitado(self):
        with self.assertRaises(ValueError):
            criar_dados_exigencia(
                codigo=0,
                numero_sequencial=1,
                tipo="OUTRA",
                descricao="Descrição válida.",
            )

    def test_codigo_negativo_deve_ser_rejeitado(self):
        with self.assertRaises(ValueError):
            criar_dados_exigencia(
                codigo=-1,
                numero_sequencial=1,
                tipo="OUTRA",
                descricao="Descrição válida.",
            )

    def test_bool_nao_deve_ser_aceito_como_codigo(self):
        with self.assertRaises(ValueError):
            criar_dados_exigencia(
                codigo=True,
                numero_sequencial=1,
                tipo="OUTRA",
                descricao="Descrição válida.",
            )

    def test_numero_sequencial_deve_ser_positivo(self):
        with self.assertRaises(ValueError):
            criar_dados_exigencia(
                codigo=1,
                numero_sequencial=0,
                tipo="OUTRA",
                descricao="Descrição válida.",
            )

    def test_tipo_invalido_deve_ser_rejeitado(self):
        with self.assertRaises(ValueError):
            criar_dados_exigencia(
                codigo=1,
                numero_sequencial=1,
                tipo="TIPO_INEXISTENTE",
                descricao="Descrição válida.",
            )

    def test_descricao_vazia_deve_ser_rejeitada(self):
        with self.assertRaises(ValueError):
            criar_dados_exigencia(
                codigo=1,
                numero_sequencial=1,
                tipo="OUTRA",
                descricao="   ",
            )

    def test_descricao_none_deve_ser_rejeitada(self):
        with self.assertRaises(ValueError):
            criar_dados_exigencia(
                codigo=1,
                numero_sequencial=1,
                tipo="OUTRA",
                descricao=None,
            )

    def test_codigos_documentos_devem_formar_lista(self):
        with self.assertRaises(ValueError):
            criar_dados_exigencia(
                codigo=1,
                numero_sequencial=1,
                tipo="CORRECAO_DOCUMENTAL",
                descricao="Corrigir documento.",
                codigos_documentos_afetados=3,
            )

    def test_codigo_documento_invalido_deve_ser_rejeitado(self):
        with self.assertRaises(ValueError):
            criar_dados_exigencia(
                codigo=1,
                numero_sequencial=1,
                tipo="CORRECAO_DOCUMENTAL",
                descricao="Corrigir documento.",
                codigos_documentos_afetados=[0],
            )

    def test_documento_duplicado_deve_ser_rejeitado(self):
        with self.assertRaises(ValueError):
            criar_dados_exigencia(
                codigo=1,
                numero_sequencial=1,
                tipo="CORRECAO_DOCUMENTAL",
                descricao="Corrigir documento.",
                codigos_documentos_afetados=[3, 3],
            )

    def test_funcao_deve_criar_nova_lista_de_documentos(self):
        documentos = [2, 5]

        exigencia = criar_dados_exigencia(
            codigo=1,
            numero_sequencial=1,
            tipo="CORRECAO_DOCUMENTAL",
            descricao="Corrigir documentos.",
            codigos_documentos_afetados=documentos,
        )

        self.assertIsNot(
            exigencia["codigos_documentos_afetados"],
            documentos,
        )


class TestEnumsExigencia(unittest.TestCase):
    """
    Testes dos enums e rótulos.
    """

    def test_tipo_exigencia_deve_possuir_seis_valores(self):
        self.assertEqual(len(TipoExigencia), 6)

    def test_status_atendimento_deve_possuir_dois_valores(self):
        self.assertEqual(len(StatusAtendimentoExigencia), 2)

    def test_tipo_exigencia_valido_deve_aceitar_enum(self):
        self.assertTrue(
            tipo_exigencia_valido(
                TipoExigencia.CORRECAO_TECNICA
            )
        )

    def test_tipo_exigencia_valido_deve_aceitar_texto(self):
        self.assertTrue(
            tipo_exigencia_valido("REENVIO_INTEGRAL")
        )

    def test_tipo_exigencia_invalido_deve_retornar_false(self):
        self.assertFalse(
            tipo_exigencia_valido("INEXISTENTE")
        )

    def test_status_atendimento_valido_deve_aceitar_texto(self):
        self.assertTrue(
            status_atendimento_exigencia_valido("PENDENTE")
        )

    def test_status_atendimento_invalido_deve_retornar_false(self):
        self.assertFalse(
            status_atendimento_exigencia_valido("EM_ANALISE")
        )

    def test_rotulo_correcao_tecnica(self):
        resultado = obter_rotulo_tipo_exigencia(
            TipoExigencia.CORRECAO_TECNICA
        )

        self.assertEqual(resultado, "Correção técnica")

    def test_rotulo_status_atendida(self):
        resultado = obter_rotulo_status_atendimento_exigencia(
            "ATENDIDA"
        )

        self.assertEqual(resultado, "Atendida")

    def test_rotulo_tipo_invalido_deve_retornar_none(self):
        self.assertIsNone(
            obter_rotulo_tipo_exigencia("INEXISTENTE")
        )


class TestStatusAtendimentoExigencia(unittest.TestCase):
    """
    Testes da máquina de estados do atendimento.
    """

    def setUp(self):
        self.exigencia = criar_dados_exigencia(
            codigo=1,
            numero_sequencial=1,
            tipo="ESCLARECIMENTO",
            descricao="Esclarecer informação.",
        )

    def test_exigencia_nova_deve_estar_pendente(self):
        self.assertTrue(
            exigencia_esta_pendente(self.exigencia)
        )

    def test_exigencia_nova_nao_deve_estar_atendida(self):
        self.assertFalse(
            exigencia_esta_atendida(self.exigencia)
        )

    def test_pendente_pode_ir_para_atendida(self):
        resultado = transicao_status_exigencia_permitida(
            "PENDENTE",
            "ATENDIDA",
        )

        self.assertTrue(resultado)

    def test_atendida_nao_pode_retornar_para_pendente(self):
        resultado = transicao_status_exigencia_permitida(
            "ATENDIDA",
            "PENDENTE",
        )

        self.assertFalse(resultado)

    def test_pendente_nao_pode_ir_para_pendente(self):
        resultado = transicao_status_exigencia_permitida(
            "PENDENTE",
            "PENDENTE",
        )

        self.assertFalse(resultado)

    def test_atendida_deve_ser_terminal(self):
        self.assertTrue(
            status_atendimento_exigencia_terminal("ATENDIDA")
        )

    def test_pendente_nao_deve_ser_terminal(self):
        self.assertFalse(
            status_atendimento_exigencia_terminal("PENDENTE")
        )

    def test_validar_transicao_valida_deve_retornar_true(self):
        self.assertTrue(
            validar_transicao_status_exigencia(
                "PENDENTE",
                "ATENDIDA",
            )
        )

    def test_validar_transicao_invalida_deve_lancar_erro(self):
        with self.assertRaises(ValueError):
            validar_transicao_status_exigencia(
                "ATENDIDA",
                "PENDENTE",
            )


class TestValidacaoEstruturalExigencia(unittest.TestCase):
    """
    Testes da validação da estrutura completa.
    """

    def test_exigencia_criada_deve_ser_valida(self):
        exigencia = criar_dados_exigencia(
            codigo=1,
            numero_sequencial=1,
            tipo="OUTRA",
            descricao="Verificar documentação.",
        )

        self.assertTrue(validar_exigencia(exigencia))

    def test_exigencia_deve_ser_dicionario(self):
        with self.assertRaises(ValueError):
            validar_exigencia([])

    def test_campo_obrigatorio_ausente_deve_ser_rejeitado(self):
        exigencia = criar_dados_exigencia(
            codigo=1,
            numero_sequencial=1,
            tipo="OUTRA",
            descricao="Verificar documentação.",
        )

        del exigencia["descricao"]

        with self.assertRaises(ValueError):
            validar_exigencia(exigencia)

    def test_pendente_nao_pode_possuir_submissao_atendimento(self):
        exigencia = criar_dados_exigencia(
            codigo=1,
            numero_sequencial=1,
            tipo="OUTRA",
            descricao="Verificar documentação.",
        )

        exigencia["codigo_submissao_atendimento"] = 4

        with self.assertRaises(ValueError):
            validar_exigencia(exigencia)

    def test_atendida_deve_possuir_dados_de_atendimento(self):
        exigencia = criar_dados_exigencia(
            codigo=1,
            numero_sequencial=1,
            tipo="OUTRA",
            descricao="Verificar documentação.",
        )

        exigencia["status_atendimento"] = "ATENDIDA"

        with self.assertRaises(ValueError):
            validar_exigencia(exigencia)

    def test_exigencia_atendida_completa_deve_ser_valida(self):
        exigencia = criar_dados_exigencia(
            codigo=1,
            numero_sequencial=1,
            tipo="OUTRA",
            descricao="Verificar documentação.",
        )

        exigencia["status_atendimento"] = "ATENDIDA"
        exigencia["codigo_submissao_atendimento"] = 4
        exigencia["data_atendimento"] = "2026-07-30"
        exigencia["responsavel_atendimento"] = "Ana Lima"
        exigencia["observacoes_atendimento"] = (
            "Atendida por meio do Reenvio 4."
        )

        self.assertTrue(validar_exigencia(exigencia))


class TestCompatibilidadeExigenciaSubmissao(unittest.TestCase):
    """
    Testes da compatibilidade entre Exigência e Submissão.
    """

    def test_complementacao_documental_aceita_complementacao(self):
        resultado = validar_compatibilidade_exigencia_submissao(
            "COMPLEMENTACAO_DOCUMENTAL",
            "COMPLEMENTACAO",
        )

        self.assertTrue(resultado)

    def test_complementacao_documental_aceita_reenvio(self):
        resultado = validar_compatibilidade_exigencia_submissao(
            "COMPLEMENTACAO_DOCUMENTAL",
            "REENVIO",
        )

        self.assertTrue(resultado)

    def test_correcao_documental_aceita_reenvio(self):
        resultado = validar_compatibilidade_exigencia_submissao(
            "CORRECAO_DOCUMENTAL",
            "REENVIO",
        )

        self.assertTrue(resultado)

    def test_correcao_documental_rejeita_complementacao(self):
        with self.assertRaises(ValueError):
            validar_compatibilidade_exigencia_submissao(
                "CORRECAO_DOCUMENTAL",
                "COMPLEMENTACAO",
            )

    def test_correcao_tecnica_aceita_reenvio(self):
        resultado = validar_compatibilidade_exigencia_submissao(
            "CORRECAO_TECNICA",
            "REENVIO",
        )

        self.assertTrue(resultado)

    def test_reenvio_integral_rejeita_complementacao(self):
        with self.assertRaises(ValueError):
            validar_compatibilidade_exigencia_submissao(
                "REENVIO_INTEGRAL",
                "COMPLEMENTACAO",
            )

    def test_reenvio_integral_aceita_reenvio(self):
        resultado = validar_compatibilidade_exigencia_submissao(
            "REENVIO_INTEGRAL",
            "REENVIO",
        )

        self.assertTrue(resultado)

    def test_esclarecimento_aceita_complementacao(self):
        resultado = validar_compatibilidade_exigencia_submissao(
            "ESCLARECIMENTO",
            "COMPLEMENTACAO",
        )

        self.assertTrue(resultado)

    def test_submissao_inicial_nao_pode_atender_exigencia(self):
        with self.assertRaises(ValueError):
            validar_compatibilidade_exigencia_submissao(
                "ESCLARECIMENTO",
                "INICIAL",
            )

    def test_tipo_submissao_invalido_deve_ser_rejeitado(self):
        with self.assertRaises(ValueError):
            validar_compatibilidade_exigencia_submissao(
                "OUTRA",
                "INEXISTENTE",
            )


if __name__ == "__main__":
    unittest.main()