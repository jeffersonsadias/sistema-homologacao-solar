import unittest

from app.dominio.documentos_homologacao import (
    OrigemDocumento,
    StatusDocumentoHomologacao,
    VisibilidadeDocumento,
    buscar_documento_por_codigo,
    codigo_documento_existe,
    criar_dados_documento_homologacao,
    listar_documentos_visiveis_ao_cliente,
    listar_transicoes_status_documento,
    obter_rotulo_origem_documento,
    obter_rotulo_status_documento,
    obter_rotulo_visibilidade_documento,
    status_documento_e_terminal,
    transicao_status_documento_e_valida,
)

class TestDocumentosHomologacao(unittest.TestCase):
    """
    Testes do domínio dos Documentos da Homologação.
    """

    def setUp(self):
        self.documento_solicitado = (
            criar_dados_documento_homologacao(
                codigo=1,
                nome="Fatura de energia atualizada",
                categoria="Unidade Consumidora",
                data_registro="2026-07-29",
                responsavel_registro="Maria Santos",
                origem=OrigemDocumento.CLIENTE,
                visibilidade=(
                    VisibilidadeDocumento.CLIENTE
                ),
                status=(
                    StatusDocumentoHomologacao
                    .SOLICITADO
                ),
                obrigatorio=True,
            )
        )

        self.documento_interno = (
            criar_dados_documento_homologacao(
                codigo=2,
                nome="Memória de cálculo",
                categoria="Projeto técnico",
                data_registro="2026-07-29",
                responsavel_registro="Carlos Souza",
                origem=OrigemDocumento.EMPRESA,
                visibilidade=(
                    VisibilidadeDocumento.INTERNA
                ),
                status=(
                    StatusDocumentoHomologacao
                    .VALIDADO
                ),
                referencia_arquivo=(
                    "arquivos/memoria_calculo_v1.pdf"
                ),
            )
        )

        self.documentos = [
            self.documento_solicitado,
            self.documento_interno,
        ]

    def test_deve_criar_documento_solicitado(self):
        self.assertEqual(
            self.documento_solicitado["status"],
            StatusDocumentoHomologacao.SOLICITADO.value,
        )

        self.assertIsNone(
            self.documento_solicitado[
                "referencia_arquivo"
            ]
        )

    def test_deve_criar_documento_validado_com_arquivo(self):
        self.assertEqual(
            self.documento_interno["status"],
            StatusDocumentoHomologacao.VALIDADO.value,
        )

        self.assertEqual(
            self.documento_interno[
                "referencia_arquivo"
            ],
            "arquivos/memoria_calculo_v1.pdf",
        )

    def test_deve_normalizar_textos(self):
        documento = criar_dados_documento_homologacao(
            codigo=3,
            nome="  Parecer de acesso  ",
            categoria="  Homologação  ",
            data_registro="2026-07-29",
            responsavel_registro="  Ana Lima  ",
            origem=OrigemDocumento.CONCESSIONARIA,
            status=StatusDocumentoHomologacao.RECEBIDO,
            referencia_arquivo="  parecer.pdf  ",
            descricao="  Documento recebido pelo portal.  ",
        )

        self.assertEqual(
            documento["nome"],
            "Parecer de acesso",
        )

        self.assertEqual(
            documento["categoria"],
            "Homologação",
        )

        self.assertEqual(
            documento["responsavel_registro"],
            "Ana Lima",
        )

        self.assertEqual(
            documento["referencia_arquivo"],
            "parecer.pdf",
        )

        self.assertEqual(
            documento["descricao"],
            "Documento recebido pelo portal.",
        )

    def test_codigo_zero_deve_gerar_erro(self):
        with self.assertRaises(ValueError):
            criar_dados_documento_homologacao(
                codigo=0,
                nome="Fatura",
                categoria="Unidade Consumidora",
                data_registro="2026-07-29",
                responsavel_registro="Maria Santos",
                origem=OrigemDocumento.CLIENTE,
            )

    def test_codigo_booleano_deve_gerar_erro(self):
        with self.assertRaises(TypeError):
            criar_dados_documento_homologacao(
                codigo=True,
                nome="Fatura",
                categoria="Unidade Consumidora",
                data_registro="2026-07-29",
                responsavel_registro="Maria Santos",
                origem=OrigemDocumento.CLIENTE,
            )

    def test_data_invalida_deve_gerar_erro(self):
        with self.assertRaises(ValueError):
            criar_dados_documento_homologacao(
                codigo=3,
                nome="Fatura",
                categoria="Unidade Consumidora",
                data_registro="29/07/2026",
                responsavel_registro="Maria Santos",
                origem=OrigemDocumento.CLIENTE,
            )

    def test_documento_recebido_deve_possuir_arquivo(self):
        with self.assertRaises(ValueError):
            criar_dados_documento_homologacao(
                codigo=3,
                nome="Parecer de acesso",
                categoria="Homologação",
                data_registro="2026-07-29",
                responsavel_registro="Maria Santos",
                origem=OrigemDocumento.CONCESSIONARIA,
                status=(
                    StatusDocumentoHomologacao.RECEBIDO
                ),
            )

    def test_documento_solicitado_nao_deve_possuir_arquivo(
        self
    ):
        with self.assertRaises(ValueError):
            criar_dados_documento_homologacao(
                codigo=3,
                nome="Fatura",
                categoria="Unidade Consumidora",
                data_registro="2026-07-29",
                responsavel_registro="Maria Santos",
                origem=OrigemDocumento.CLIENTE,
                status=(
                    StatusDocumentoHomologacao.SOLICITADO
                ),
                referencia_arquivo="fatura.pdf",
            )

    def test_versao_superior_deve_informar_documento_anterior(
        self
    ):
        with self.assertRaises(ValueError):
            criar_dados_documento_homologacao(
                codigo=3,
                nome="Projeto elétrico",
                categoria="Projeto técnico",
                data_registro="2026-07-29",
                responsavel_registro="Maria Santos",
                origem=OrigemDocumento.EMPRESA,
                status=(
                    StatusDocumentoHomologacao.RECEBIDO
                ),
                referencia_arquivo="projeto_v2.pdf",
                versao=2,
            )

    def test_primeira_versao_nao_deve_informar_anterior(self):
        with self.assertRaises(ValueError):
            criar_dados_documento_homologacao(
                codigo=3,
                nome="Projeto elétrico",
                categoria="Projeto técnico",
                data_registro="2026-07-29",
                responsavel_registro="Maria Santos",
                origem=OrigemDocumento.EMPRESA,
                status=(
                    StatusDocumentoHomologacao.RECEBIDO
                ),
                referencia_arquivo="projeto_v1.pdf",
                versao=1,
                codigo_documento_anterior=1,
            )

    def test_deve_criar_segunda_versao(self):
        documento = criar_dados_documento_homologacao(
            codigo=3,
            nome="Projeto elétrico",
            categoria="Projeto técnico",
            data_registro="2026-07-29",
            responsavel_registro="Maria Santos",
            origem=OrigemDocumento.EMPRESA,
            status=StatusDocumentoHomologacao.RECEBIDO,
            referencia_arquivo="projeto_v2.pdf",
            versao=2,
            codigo_documento_anterior=1,
        )

        self.assertEqual(
            documento["versao"],
            2,
        )

        self.assertEqual(
            documento["codigo_documento_anterior"],
            1,
        )

    def test_deve_aceitar_enums_como_texto(self):
        documento = criar_dados_documento_homologacao(
            codigo=3,
            nome="Parecer de acesso",
            categoria="Homologação",
            data_registro="2026-07-29",
            responsavel_registro="Maria Santos",
            origem="CONCESSIONARIA",
            visibilidade="CLIENTE",
            status="RECEBIDO",
            referencia_arquivo="parecer.pdf",
        )

        self.assertEqual(
            documento["origem"],
            "CONCESSIONARIA",
        )

        self.assertEqual(
            documento["visibilidade"],
            "CLIENTE",
        )

        self.assertEqual(
            documento["status"],
            "RECEBIDO",
        )

    def test_origem_invalida_deve_gerar_erro(self):
        with self.assertRaises(ValueError):
            criar_dados_documento_homologacao(
                codigo=3,
                nome="Documento",
                categoria="Outros",
                data_registro="2026-07-29",
                responsavel_registro="Maria Santos",
                origem="ORIGEM_INEXISTENTE",
            )

    def test_deve_buscar_documento_por_codigo(self):
        resultado = buscar_documento_por_codigo(
            documentos=self.documentos,
            codigo=2,
        )

        self.assertIs(
            resultado,
            self.documento_interno,
        )

    def test_busca_inexistente_deve_retornar_none(self):
        resultado = buscar_documento_por_codigo(
            documentos=self.documentos,
            codigo=999,
        )

        self.assertIsNone(resultado)

    def test_codigo_documento_deve_existir(self):
        self.assertTrue(
            codigo_documento_existe(
                documentos=self.documentos,
                codigo=1,
            )
        )

    def test_codigo_documento_nao_deve_existir(self):
        self.assertFalse(
            codigo_documento_existe(
                documentos=self.documentos,
                codigo=999,
            )
        )

    def test_deve_listar_somente_documentos_do_cliente(
        self
    ):
        resultado = listar_documentos_visiveis_ao_cliente(
            self.documentos
        )

        self.assertEqual(
            len(resultado),
            1,
        )

        self.assertIs(
            resultado[0],
            self.documento_solicitado,
        )

    def test_rotulo_da_origem_deve_ser_amigavel(self):
        resultado = obter_rotulo_origem_documento(
            OrigemDocumento.CONCESSIONARIA
        )

        self.assertEqual(
            resultado,
            "Concessionária",
        )

    def test_rotulo_da_visibilidade_deve_ser_amigavel(
        self
    ):
        resultado = obter_rotulo_visibilidade_documento(
            VisibilidadeDocumento.CLIENTE
        )

        self.assertEqual(
            resultado,
            "Disponível para o cliente",
        )

    def test_rotulo_do_status_deve_ser_amigavel(self):
        resultado = obter_rotulo_status_documento(
            StatusDocumentoHomologacao.EM_VALIDACAO
        )

        self.assertEqual(
            resultado,
            "Em validação",
        )

    def test_fluxo_principal_documental_deve_ser_valido(self):
        fluxo = (
            StatusDocumentoHomologacao.SOLICITADO,
            StatusDocumentoHomologacao.RECEBIDO,
            StatusDocumentoHomologacao.EM_VALIDACAO,
            StatusDocumentoHomologacao.VALIDADO,
            StatusDocumentoHomologacao.SUBSTITUIDO,
        )

        for indice in range(len(fluxo) - 1):
            self.assertTrue(
                transicao_status_documento_e_valida(
                    fluxo[indice],
                    fluxo[indice + 1],
                )
            )

    def test_documento_em_validacao_pode_ser_rejeitado(self):
        self.assertTrue(
            transicao_status_documento_e_valida(
                StatusDocumentoHomologacao.EM_VALIDACAO,
                StatusDocumentoHomologacao.REJEITADO,
            )
        )

    def test_documento_solicitado_nao_pode_ser_validado(
        self
    ):
        self.assertFalse(
            transicao_status_documento_e_valida(
                StatusDocumentoHomologacao.SOLICITADO,
                StatusDocumentoHomologacao.VALIDADO,
            )
        )

    def test_substituido_deve_ser_terminal(self):
        self.assertTrue(
            status_documento_e_terminal(
                StatusDocumentoHomologacao.SUBSTITUIDO
            )
        )

    def test_validado_nao_deve_ser_terminal(self):
        self.assertFalse(
            status_documento_e_terminal(
                StatusDocumentoHomologacao.VALIDADO
            )
        )

    def test_deve_listar_transicoes_documentais(self):
        resultado = listar_transicoes_status_documento(
            StatusDocumentoHomologacao.EM_VALIDACAO
        )

        self.assertIn(
            StatusDocumentoHomologacao.VALIDADO,
            resultado,
        )

        self.assertIn(
            StatusDocumentoHomologacao.REJEITADO,
            resultado,
        )

        self.assertEqual(len(resultado), 2)

if __name__ == "__main__":
    unittest.main()