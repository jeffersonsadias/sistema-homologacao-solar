"""
Testes das funções de construção das Movimentações
do contexto de Homologação.
"""

import unittest

from app.dominio.documentos_homologacao import (
    StatusDocumentoHomologacao,
)

from app.dominio.movimentacoes_homologacao import (
    criar_movimentacao_de_abertura,
    criar_movimentacao_de_status,
    criar_movimentacao_documento_adicionado,
    criar_movimentacao_resposta_concessionaria,
    criar_movimentacao_resposta_exigencia,
    criar_movimentacao_status_documento,
    criar_movimentacao_status_operacional_submissao,
    criar_movimentacao_submissao_adicionada,
    criar_movimentacao_submissao_enviada,
    criar_movimentacao_submissao_protocolada,
    gerar_proximo_codigo_movimentacao,
)

from app.dominio.status_homologacao import (
    StatusHomologacao,
)

from app.dominio.status_submissao import (
    StatusAnaliseSubmissao,
    StatusOperacionalSubmissao,
)

from app.dominio.submissoes_homologacao import (
    CanalEnvioSubmissao,
)


class TestCodigoMovimentacao(unittest.TestCase):

    def test_lista_vazia_deve_gerar_codigo_um(self):
        self.assertEqual(
            gerar_proximo_codigo_movimentacao([]),
            1,
        )

    def test_deve_gerar_codigo_apos_o_maior_existente(self):
        movimentacoes = [
            {"codigo": 2},
            {"codigo": 5},
            {"codigo": 3},
        ]

        self.assertEqual(
            gerar_proximo_codigo_movimentacao(
                movimentacoes
            ),
            6,
        )


class TestMovimentacoesHomologacao(unittest.TestCase):

    def test_deve_criar_movimentacao_de_abertura(self):
        movimentacao = criar_movimentacao_de_abertura(
            data_abertura="2026-07-31",
            responsavel_abertura="Ana Lima",
        )

        self.assertEqual(
            movimentacao["codigo"],
            1,
        )

        self.assertEqual(
            movimentacao["tipo_evento"],
            "HOMOLOGACAO_ABERTA",
        )

        self.assertEqual(
            movimentacao["novo_status"],
            StatusHomologacao.EM_PREPARACAO.value,
        )

    def test_deve_criar_movimentacao_de_status(self):
        movimentacao = criar_movimentacao_de_status(
            movimentacoes=[{"codigo": 1}],
            status_anterior=(
                StatusHomologacao.EM_PREPARACAO
            ),
            novo_status=(
                StatusHomologacao.AGUARDANDO_DOCUMENTACAO
            ),
            data_movimentacao="2026-08-01",
            responsavel="Ana Lima",
            descricao="Aguardando documentos.",
            motivo=None,
        )

        self.assertEqual(
            movimentacao["codigo"],
            2,
        )

        self.assertEqual(
            movimentacao["tipo_evento"],
            "STATUS_HOMOLOGACAO_ALTERADO",
        )

        self.assertEqual(
            movimentacao["status_anterior"],
            "EM_PREPARACAO",
        )

        self.assertEqual(
            movimentacao["novo_status"],
            "AGUARDANDO_DOCUMENTACAO",
        )


class TestMovimentacoesDocumento(unittest.TestCase):

    def setUp(self):
        self.documento = {
            "codigo": 10,
            "nome": "Fatura de energia",
        }

    def test_deve_criar_movimentacao_documento_adicionado(
        self
    ):
        movimentacao = (
            criar_movimentacao_documento_adicionado(
                movimentacoes=[{"codigo": 1}],
                documento=self.documento,
                data_movimentacao="2026-08-01",
                responsavel="Ana Lima",
            )
        )

        self.assertEqual(
            movimentacao["tipo_evento"],
            "DOCUMENTO_ADICIONADO",
        )

        self.assertEqual(
            movimentacao["codigo_documento"],
            10,
        )

    def test_deve_criar_movimentacao_status_documento(
        self
    ):
        movimentacao = criar_movimentacao_status_documento(
            movimentacoes=[{"codigo": 1}],
            documento=self.documento,
            status_anterior=(
                StatusDocumentoHomologacao.RECEBIDO
            ),
            novo_status=(
                StatusDocumentoHomologacao.EM_VALIDACAO
            ),
            data_movimentacao="2026-08-01",
            responsavel="Ana Lima",
            motivo=None,
        )

        self.assertEqual(
            movimentacao["tipo_evento"],
            "STATUS_DOCUMENTO_ALTERADO",
        )

        self.assertEqual(
            movimentacao["status_anterior"],
            "RECEBIDO",
        )

        self.assertEqual(
            movimentacao["novo_status"],
            "EM_VALIDACAO",
        )


class TestMovimentacoesSubmissao(unittest.TestCase):

    def setUp(self):
        self.submissao = {
            "codigo": 20,
            "numero_sequencial": 2,
            "tipo": "COMPLEMENTACAO",
        }

    def test_deve_criar_movimentacao_submissao_adicionada(
        self
    ):
        movimentacao = (
            criar_movimentacao_submissao_adicionada(
                movimentacoes=[{"codigo": 1}],
                submissao=self.submissao,
                data_movimentacao="2026-08-01",
                responsavel="Ana Lima",
            )
        )

        self.assertEqual(
            movimentacao["tipo_evento"],
            "SUBMISSAO_ADICIONADA",
        )

        self.assertEqual(
            movimentacao["codigo_submissao"],
            20,
        )

        self.assertEqual(
            movimentacao["tipo_submissao"],
            "COMPLEMENTACAO",
        )

    def test_deve_criar_movimentacao_status_operacional(
        self
    ):
        movimentacao = (
            criar_movimentacao_status_operacional_submissao(
                movimentacoes=[{"codigo": 1}],
                submissao=self.submissao,
                status_anterior=(
                    StatusOperacionalSubmissao
                    .EM_PREPARACAO
                ),
                novo_status=(
                    StatusOperacionalSubmissao
                    .PRONTA_PARA_ENVIO
                ),
                data_movimentacao="2026-08-01",
                responsavel="Ana Lima",
                motivo=None,
            )
        )

        self.assertEqual(
            movimentacao["tipo_evento"],
            "STATUS_OPERACIONAL_SUBMISSAO_ALTERADO",
        )

        self.assertEqual(
            movimentacao["novo_status"],
            "PRONTA_PARA_ENVIO",
        )

    def test_deve_criar_movimentacao_submissao_enviada(
        self
    ):
        movimentacao = criar_movimentacao_submissao_enviada(
            movimentacoes=[{"codigo": 1}],
            submissao=self.submissao,
            canal_envio=CanalEnvioSubmissao.PORTAL,
            data_envio="2026-08-02",
            responsavel_envio="Ana Lima",
        )

        self.assertEqual(
            movimentacao["tipo_evento"],
            "SUBMISSAO_ENVIADA",
        )

        self.assertEqual(
            movimentacao["canal_envio"],
            "PORTAL",
        )

        self.assertEqual(
            movimentacao["novo_status"],
            "ENVIADA",
        )

    def test_deve_criar_movimentacao_protocolada(self):
        movimentacao = (
            criar_movimentacao_submissao_protocolada(
                movimentacoes=[{"codigo": 1}],
                submissao=self.submissao,
                protocolo="PROT-001",
                data_protocolo="2026-08-03",
                responsavel="Ana Lima",
            )
        )

        self.assertEqual(
            movimentacao["tipo_evento"],
            "SUBMISSAO_PROTOCOLADA",
        )

        self.assertEqual(
            movimentacao["protocolo"],
            "PROT-001",
        )

        self.assertEqual(
            movimentacao["novo_status"],
            "PROTOCOLADA",
        )


class TestMovimentacoesResposta(unittest.TestCase):

    def setUp(self):
        self.submissao = {
            "codigo": 20,
            "numero_sequencial": 2,
            "tipo": "COMPLEMENTACAO",
        }

        self.resposta = {
            "codigo": 30,
            "numero_sequencial": 1,
            "tipo": "RECEBIMENTO_CONFIRMADO",
            "data_registro": "2026-08-04",
            "responsavel_registro": "Ana Lima",
            "exigencias": [],
        }

    def test_deve_criar_movimentacao_resposta(
        self
    ):
        movimentacao = (
            criar_movimentacao_resposta_concessionaria(
                movimentacoes=[{"codigo": 1}],
                submissao=self.submissao,
                resposta=self.resposta,
                status_anterior=(
                    StatusAnaliseSubmissao.SEM_RESPOSTA
                ),
                novo_status=(
                    StatusAnaliseSubmissao.RECEBIDA
                ),
            )
        )

        self.assertEqual(
            movimentacao["tipo_evento"],
            "RESPOSTA_CONCESSIONARIA_REGISTRADA",
        )

        self.assertEqual(
            movimentacao["codigo_resposta"],
            30,
        )

        self.assertEqual(
            movimentacao["novo_status"],
            "RECEBIDA",
        )

    def test_deve_criar_movimentacao_resposta_exigencia(
        self
    ):
        resposta = {
            **self.resposta,
            "tipo": "EXIGENCIA",
            "exigencias": [
                {"codigo": 100},
                {"codigo": 101},
            ],
        }

        movimentacao = (
            criar_movimentacao_resposta_exigencia(
                movimentacoes=[{"codigo": 1}],
                submissao=self.submissao,
                resposta=resposta,
                status_anterior=(
                    StatusAnaliseSubmissao.EM_ANALISE
                ),
            )
        )

        self.assertEqual(
            movimentacao["tipo_evento"],
            "EXIGENCIAS_CONCESSIONARIA_REGISTRADAS",
        )

        self.assertEqual(
            movimentacao["novo_status"],
            "COM_EXIGENCIA",
        )

        self.assertEqual(
            movimentacao["codigos_exigencias"],
            [100, 101],
        )


if __name__ == "__main__":
    unittest.main()