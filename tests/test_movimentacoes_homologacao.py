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
    criar_movimentacao_instalacao_concluida,
    criar_movimentacao_instalacao_iniciada,
    criar_movimentacao_instalacao_planejada,
    criar_movimentacao_resposta_concessionaria,
    criar_movimentacao_resposta_exigencia,
    criar_movimentacao_status_documento,
    criar_movimentacao_status_operacional_submissao,
    criar_movimentacao_submissao_adicionada,
    criar_movimentacao_submissao_enviada,
    criar_movimentacao_submissao_protocolada,
    criar_movimentacao_vistoria_agendada,
    criar_movimentacao_vistoria_solicitada,
    criar_movimentacao_vistoria_realizada,
    criar_movimentacao_vistoria_aprovada,
    criar_movimentacao_vistoria_reprovada,
    criar_movimentacao_correcao_pos_vistoria,
    criar_movimentacao_ligacao_agendada,
    criar_movimentacao_ligacao_concluida,
    criar_movimentacao_ligacao_solicitada,
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


class TestMovimentacoesInstalacao(
    unittest.TestCase
):
    """
    Testes das Movimentações relacionadas
    à Instalação.
    """

    def test_deve_criar_movimentacao_de_planejamento(
        self,
    ):
        """
        Deve registrar os principais dados
        do planejamento da Instalação.
        """

        instalacao = {
            "data_prevista": "2026-08-20",
            "equipe_responsavel": (
                "Equipe Técnica A"
            ),
        }

        movimentacao = (
            criar_movimentacao_instalacao_planejada(
                movimentacoes=[
                    {
                        "codigo": 1,
                    }
                ],
                instalacao=instalacao,
                status_anterior=(
                    StatusHomologacao
                    .PARECER_DE_ACESSO_EMITIDO
                ),
                novo_status=(
                    StatusHomologacao
                    .AGUARDANDO_INSTALACAO
                ),
                data_movimentacao="2026-08-10",
                responsavel="Ana Lima",
            )
        )

        self.assertEqual(
            movimentacao["codigo"],
            2,
        )

        self.assertEqual(
            movimentacao["tipo_evento"],
            "INSTALACAO_PLANEJADA",
        )

        self.assertEqual(
            movimentacao["status_anterior"],
            "PARECER_DE_ACESSO_EMITIDO",
        )

        self.assertEqual(
            movimentacao["novo_status"],
            "AGUARDANDO_INSTALACAO",
        )

        self.assertEqual(
            movimentacao[
                "data_prevista_instalacao"
            ],
            "2026-08-20",
        )

        self.assertEqual(
            movimentacao[
                "equipe_responsavel"
            ],
            "Equipe Técnica A",
        )

    def test_deve_criar_movimentacao_de_inicio(
        self,
    ):
        """
        Deve registrar os principais dados
        do início da Instalação.
        """

        instalacao = {
            "status": "EM_EXECUCAO",
            "data_inicio": "2026-08-20",
            "equipe_responsavel": (
                "Equipe Técnica A"
            ),
        }

        movimentacao = (
            criar_movimentacao_instalacao_iniciada(
                movimentacoes=[
                    {
                        "codigo": 2,
                    }
                ],
                instalacao=instalacao,
                data_movimentacao="2026-08-20",
                responsavel="Carlos Souza",
            )
        )

        self.assertEqual(
            movimentacao["codigo"],
            3,
        )

        self.assertEqual(
            movimentacao["tipo_evento"],
            "INSTALACAO_INICIADA",
        )

        self.assertIsNone(
            movimentacao["status_anterior"]
        )

        self.assertIsNone(
            movimentacao["novo_status"]
        )

        self.assertEqual(
            movimentacao["status_instalacao"],
            "EM_EXECUCAO",
        )

        self.assertEqual(
            movimentacao[
                "data_inicio_instalacao"
            ],
            "2026-08-20",
        )

    def test_deve_criar_movimentacao_de_conclusao(
        self,
    ):
        """
        Deve registrar os principais dados
        da conclusão da Instalação.
        """

        instalacao = {
            "status": "CONCLUIDA",
            "data_inicio": "2026-08-20",
            "data_conclusao": "2026-08-22",
            "equipe_responsavel": (
                "Equipe Técnica A"
            ),
        }

        movimentacao = (
            criar_movimentacao_instalacao_concluida(
                movimentacoes=[
                    {
                        "codigo": 3,
                    }
                ],
                instalacao=instalacao,
                status_anterior=(
                    StatusHomologacao
                    .AGUARDANDO_INSTALACAO
                ),
                novo_status=(
                    StatusHomologacao
                    .INSTALACAO_CONCLUIDA
                ),
                data_movimentacao="2026-08-22",
                responsavel="Carlos Souza",
            )
        )

        self.assertEqual(
            movimentacao["codigo"],
            4,
        )

        self.assertEqual(
            movimentacao["tipo_evento"],
            "INSTALACAO_CONCLUIDA",
        )

        self.assertEqual(
            movimentacao["status_anterior"],
            "AGUARDANDO_INSTALACAO",
        )

        self.assertEqual(
            movimentacao["novo_status"],
            "INSTALACAO_CONCLUIDA",
        )

        self.assertEqual(
            movimentacao[
                "data_conclusao_instalacao"
            ],
            "2026-08-22",
        )

        self.assertEqual(
            movimentacao["status_instalacao"],
            "CONCLUIDA",
        )

class TestMovimentacoesVistoria(
    unittest.TestCase
):
    """
    Testes das Movimentações relacionadas
    às Vistorias.
    """

    def test_deve_criar_movimentacao_de_solicitacao(
        self,
    ):
        """
        Deve registrar os principais dados
        da solicitação da Vistoria.
        """

        vistoria = {
            "codigo": 1,
            "numero_sequencial": 1,
            "protocolo": "VST-2026-001",
            "data_solicitacao": "2026-08-25",
        }

        movimentacao = (
            criar_movimentacao_vistoria_solicitada(
                movimentacoes=[
                    {
                        "codigo": 4,
                    }
                ],
                vistoria=vistoria,
                status_anterior=(
                    StatusHomologacao
                    .INSTALACAO_CONCLUIDA
                ),
                novo_status=(
                    StatusHomologacao
                    .VISTORIA_SOLICITADA
                ),
                data_movimentacao="2026-08-25",
                responsavel="Ana Lima",
            )
        )

        self.assertEqual(
            movimentacao["codigo"],
            5,
        )

        self.assertEqual(
            movimentacao["tipo_evento"],
            "VISTORIA_SOLICITADA",
        )

        self.assertEqual(
            movimentacao["status_anterior"],
            "INSTALACAO_CONCLUIDA",
        )

        self.assertEqual(
            movimentacao["novo_status"],
            "VISTORIA_SOLICITADA",
        )

        self.assertEqual(
            movimentacao["codigo_vistoria"],
            1,
        )

        self.assertEqual(
            movimentacao[
                "numero_sequencial_vistoria"
            ],
            1,
        )

        self.assertEqual(
            movimentacao["protocolo_vistoria"],
            "VST-2026-001",
        )

    def test_deve_criar_movimentacao_de_agendamento(
        self,
    ):
        """
        Deve registrar os principais dados
        do agendamento da Vistoria.
        """

        vistoria = {
            "codigo": 1,
            "numero_sequencial": 1,
            "protocolo": "VST-2026-001",
            "data_agendamento": "2026-08-30",
        }

        movimentacao = (
            criar_movimentacao_vistoria_agendada(
                movimentacoes=[
                    {
                        "codigo": 5,
                    }
                ],
                vistoria=vistoria,
                status_anterior=(
                    StatusHomologacao
                    .VISTORIA_SOLICITADA
                ),
                novo_status=(
                    StatusHomologacao
                    .AGUARDANDO_VISTORIA
                ),
                data_movimentacao="2026-08-26",
                responsavel="Carlos Souza",
            )
        )

        self.assertEqual(
            movimentacao["codigo"],
            6,
        )

        self.assertEqual(
            movimentacao["tipo_evento"],
            "VISTORIA_AGENDADA",
        )

        self.assertEqual(
            movimentacao["status_anterior"],
            "VISTORIA_SOLICITADA",
        )

        self.assertEqual(
            movimentacao["novo_status"],
            "AGUARDANDO_VISTORIA",
        )

        self.assertEqual(
            movimentacao["codigo_vistoria"],
            1,
        )

        self.assertEqual(
            movimentacao[
                "data_agendamento_vistoria"
            ],
            "2026-08-30",
        )

    def test_deve_criar_movimentacao_de_realizacao(
        self,
    ):
        """
        Deve registrar os principais dados
        da realização da Vistoria.
        """

        vistoria = {
            "codigo": 1,
            "numero_sequencial": 1,
            "protocolo": "VST-2026-001",
            "status": "REALIZADA",
            "data_realizacao": "2026-08-30",
        }

        movimentacao = (
            criar_movimentacao_vistoria_realizada(
                movimentacoes=[
                    {
                        "codigo": 6,
                    }
                ],
                vistoria=vistoria,
                data_movimentacao="2026-08-30",
                responsavel="Marcos Oliveira",
            )
        )

        self.assertEqual(
            movimentacao["codigo"],
            7,
        )

        self.assertEqual(
            movimentacao["tipo_evento"],
            "VISTORIA_REALIZADA",
        )

        self.assertIsNone(
            movimentacao["status_anterior"]
        )

        self.assertIsNone(
            movimentacao["novo_status"]
        )

        self.assertEqual(
            movimentacao["codigo_vistoria"],
            1,
        )

        self.assertEqual(
            movimentacao[
                "data_realizacao_vistoria"
            ],
            "2026-08-30",
        )

        self.assertEqual(
            movimentacao["status_vistoria"],
            "REALIZADA",
        )

    def test_deve_criar_movimentacao_de_aprovacao(
        self,
    ):
        """
        Deve registrar os principais dados
        da aprovação da Vistoria.
        """

        vistoria = {
            "codigo": 1,
            "numero_sequencial": 1,
            "protocolo": "VST-2026-001",
            "data_resultado": "2026-09-01",
            "resultado": "APROVADA",
        }

        movimentacao = (
            criar_movimentacao_vistoria_aprovada(
                movimentacoes=[
                    {
                        "codigo": 7,
                    }
                ],
                vistoria=vistoria,
                status_anterior=(
                    StatusHomologacao
                    .AGUARDANDO_VISTORIA
                ),
                novo_status=(
                    StatusHomologacao
                    .VISTORIA_APROVADA
                ),
                data_movimentacao="2026-09-01",
                responsavel="Ana Lima",
            )
        )

        self.assertEqual(
            movimentacao["codigo"],
            8,
        )

        self.assertEqual(
            movimentacao["tipo_evento"],
            "VISTORIA_APROVADA",
        )

        self.assertEqual(
            movimentacao["status_anterior"],
            "AGUARDANDO_VISTORIA",
        )

        self.assertEqual(
            movimentacao["novo_status"],
            "VISTORIA_APROVADA",
        )

        self.assertEqual(
            movimentacao["resultado_vistoria"],
            "APROVADA",
        )

        self.assertIsNone(
            movimentacao["motivo"]
        )

    def test_deve_criar_movimentacao_de_reprovacao(
        self,
    ):
        """
        Deve registrar os principais dados
        da reprovação da Vistoria.
        """

        vistoria = {
            "codigo": 1,
            "numero_sequencial": 1,
            "protocolo": "VST-2026-001",
            "data_resultado": "2026-09-01",
            "resultado": "REPROVADA",
            "motivo_reprovacao": (
                "Inversor sem identificação."
            ),
        }

        movimentacao = (
            criar_movimentacao_vistoria_reprovada(
                movimentacoes=[
                    {
                        "codigo": 7,
                    }
                ],
                vistoria=vistoria,
                status_anterior=(
                    StatusHomologacao
                    .AGUARDANDO_VISTORIA
                ),
                novo_status=(
                    StatusHomologacao
                    .VISTORIA_REPROVADA
                ),
                data_movimentacao="2026-09-01",
                responsavel="Ana Lima",
            )
        )

        self.assertEqual(
            movimentacao["codigo"],
            8,
        )

        self.assertEqual(
            movimentacao["tipo_evento"],
            "VISTORIA_REPROVADA",
        )

        self.assertEqual(
            movimentacao["novo_status"],
            "VISTORIA_REPROVADA",
        )

        self.assertEqual(
            movimentacao["resultado_vistoria"],
            "REPROVADA",
        )

        self.assertEqual(
            movimentacao["motivo"],
            "Inversor sem identificação.",
        )

    def test_deve_criar_movimentacao_de_correcao(
        self,
    ):
        """
        Deve registrar a correção realizada
        após uma Vistoria reprovada.
        """

        vistoria = {
            "codigo": 1,
            "numero_sequencial": 1,
            "motivo_reprovacao": (
                "Inversor sem identificação."
            ),
        }

        movimentacao = (
            criar_movimentacao_correcao_pos_vistoria(
                movimentacoes=[
                    {
                        "codigo": 8,
                    }
                ],
                vistoria=vistoria,
                status_anterior=(
                    StatusHomologacao
                    .VISTORIA_REPROVADA
                ),
                novo_status=(
                    StatusHomologacao
                    .CORRECAO_POS_VISTORIA
                ),
                data_movimentacao="2026-09-03",
                responsavel="Carlos Souza",
                descricao_correcao=(
                    "Identificação do inversor instalada."
                ),
            )
        )

        self.assertEqual(
            movimentacao["codigo"],
            9,
        )

        self.assertEqual(
            movimentacao["tipo_evento"],
            "CORRECAO_POS_VISTORIA",
        )

        self.assertEqual(
            movimentacao["novo_status"],
            "CORRECAO_POS_VISTORIA",
        )

        self.assertEqual(
            movimentacao[
                "descricao_correcao"
            ],
            "Identificação do inversor instalada.",
        )

class TestMovimentacoesLigacao(
    unittest.TestCase
):
    """
    Testes das Movimentações relacionadas
    à Ligação e Energização.
    """

    def test_deve_criar_movimentacao_ligacao_solicitada(
        self,
    ):
        """
        Deve registrar os principais dados
        da solicitação da Ligação.
        """

        ligacao = {
            "status": "SOLICITADA",
            "data_solicitacao": "2026-09-05",
            "protocolo": "LIG-2026-001",
        }

        movimentacao = (
            criar_movimentacao_ligacao_solicitada(
                movimentacoes=[
                    {
                        "codigo": 9,
                    }
                ],
                ligacao=ligacao,
                status_anterior=(
                    StatusHomologacao
                    .VISTORIA_APROVADA
                ),
                novo_status=(
                    StatusHomologacao
                    .AGUARDANDO_LIGACAO
                ),
                data_movimentacao="2026-09-05",
                responsavel="Ana Lima",
            )
        )

        self.assertEqual(
            movimentacao["codigo"],
            10,
        )

        self.assertEqual(
            movimentacao["tipo_evento"],
            "LIGACAO_SOLICITADA",
        )

        self.assertEqual(
            movimentacao["status_anterior"],
            "VISTORIA_APROVADA",
        )

        self.assertEqual(
            movimentacao["novo_status"],
            "AGUARDANDO_LIGACAO",
        )

        self.assertEqual(
            movimentacao["protocolo_ligacao"],
            "LIG-2026-001",
        )

        self.assertEqual(
            movimentacao["status_ligacao"],
            "SOLICITADA",
        )

    def test_deve_criar_movimentacao_ligacao_agendada(
        self,
    ):
        """
        Deve registrar o agendamento sem
        alterar o estado geral da Homologação.
        """

        ligacao = {
            "status": "AGENDADA",
            "protocolo": "LIG-2026-001",
            "data_agendamento": "2026-09-10",
        }

        movimentacao = (
            criar_movimentacao_ligacao_agendada(
                movimentacoes=[
                    {
                        "codigo": 10,
                    }
                ],
                ligacao=ligacao,
                data_movimentacao="2026-09-06",
                responsavel="Carlos Souza",
            )
        )

        self.assertEqual(
            movimentacao["codigo"],
            11,
        )

        self.assertEqual(
            movimentacao["tipo_evento"],
            "LIGACAO_AGENDADA",
        )

        self.assertIsNone(
            movimentacao["status_anterior"]
        )

        self.assertIsNone(
            movimentacao["novo_status"]
        )

        self.assertEqual(
            movimentacao[
                "data_agendamento_ligacao"
            ],
            "2026-09-10",
        )

        self.assertEqual(
            movimentacao["status_ligacao"],
            "AGENDADA",
        )

    def test_deve_criar_movimentacao_ligacao_concluida(
        self,
    ):
        """
        Deve registrar a conclusão da Ligação
        e a mudança para SISTEMA_LIGADO.
        """

        ligacao = {
            "status": "CONCLUIDA",
            "protocolo": "LIG-2026-001",
            "data_ligacao": "2026-09-10",
        }

        movimentacao = (
            criar_movimentacao_ligacao_concluida(
                movimentacoes=[
                    {
                        "codigo": 11,
                    }
                ],
                ligacao=ligacao,
                status_anterior=(
                    StatusHomologacao
                    .AGUARDANDO_LIGACAO
                ),
                novo_status=(
                    StatusHomologacao
                    .SISTEMA_LIGADO
                ),
                data_movimentacao="2026-09-10",
                responsavel=(
                    "Equipe da Concessionária"
                ),
            )
        )

        self.assertEqual(
            movimentacao["codigo"],
            12,
        )

        self.assertEqual(
            movimentacao["tipo_evento"],
            "LIGACAO_CONCLUIDA",
        )

        self.assertEqual(
            movimentacao["status_anterior"],
            "AGUARDANDO_LIGACAO",
        )

        self.assertEqual(
            movimentacao["novo_status"],
            "SISTEMA_LIGADO",
        )

        self.assertEqual(
            movimentacao["data_ligacao"],
            "2026-09-10",
        )

        self.assertEqual(
            movimentacao["status_ligacao"],
            "CONCLUIDA",
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