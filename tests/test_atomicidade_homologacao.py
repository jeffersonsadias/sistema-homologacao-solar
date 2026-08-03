"""
Testes arquiteturais de isolamento e atomicidade
do Aggregate Root Homologação.

Estes testes não validam fluxos funcionais completos.

Eles protegem o contrato interno segundo o qual:

- estruturas candidatas podem ser modificadas;
- entidades reais não sofrem alterações antecipadas;
- somente as coleções que precisam ser isoladas são copiadas;
- coleções apenas consultadas podem permanecer compartilhadas
  de forma intencional.
"""

import unittest
from unittest.mock import patch

import app.dominio.homologacoes as homologacoes

from app.dominio.exigencias_concessionaria import (
    criar_dados_exigencia,
)

from app.dominio.submissoes_homologacao import (
    criar_dados_submissao,
    criar_referencia_documento,
)

from app.dominio.documentos_homologacao import (
    OrigemDocumento,
    StatusDocumentoHomologacao,
    criar_dados_documento_homologacao,
)

from app.dominio.respostas_concessionaria import (
    criar_dados_resposta_exigencia,
    criar_dados_resposta_inicio_analise,
)

from app.dominio.status_homologacao import (
    EventoHomologacao,
    StatusHomologacao,
)

class TestCopiaExigencia(unittest.TestCase):
    """
    Testes da cópia defensiva de uma Exigência.
    """

    def setUp(self):
        self.exigencia = criar_dados_exigencia(
            codigo=1,
            numero_sequencial=1,
            tipo="CORRECAO_DOCUMENTAL",
            descricao="Corrigir o diagrama unifilar.",
            codigos_documentos_afetados=[3, 4],
        )

    def test_copia_deve_ser_novo_dicionario(self):
        exigencia_copiada = (
            homologacoes._copiar_exigencia(
                self.exigencia
            )
        )

        self.assertIsNot(
            exigencia_copiada,
            self.exigencia,
        )

        self.assertEqual(
            exigencia_copiada,
            self.exigencia,
        )

    def test_alterar_campo_escalar_nao_deve_alterar_original(
        self
    ):
        exigencia_copiada = (
            homologacoes._copiar_exigencia(
                self.exigencia
            )
        )

        exigencia_copiada["descricao"] = (
            "Descrição modificada apenas na cópia."
        )

        self.assertEqual(
            self.exigencia["descricao"],
            "Corrigir o diagrama unifilar.",
        )

    def test_lista_de_documentos_deve_ser_independente(
        self
    ):
        exigencia_copiada = (
            homologacoes._copiar_exigencia(
                self.exigencia
            )
        )

        exigencia_copiada[
            "codigos_documentos_afetados"
        ].append(99)

        self.assertEqual(
            self.exigencia[
                "codigos_documentos_afetados"
            ],
            [3, 4],
        )

        self.assertEqual(
            exigencia_copiada[
                "codigos_documentos_afetados"
            ],
            [3, 4, 99],
        )

        self.assertIsNot(
            exigencia_copiada[
                "codigos_documentos_afetados"
            ],
            self.exigencia[
                "codigos_documentos_afetados"
            ],
        )


class TestCopiaSubmissao(unittest.TestCase):
    """
    Testes da cópia defensiva de uma Submissão.
    """

    def setUp(self):
        referencia = criar_referencia_documento(
            codigo_documento=3,
            numero_versao=1,
        )

        self.submissao = criar_dados_submissao(
            codigo=1,
            numero_sequencial=1,
            tipo="INICIAL",
            data_criacao="2026-08-01",
            responsavel_criacao="Ana Lima",
            pacote_documental=[referencia],
        )

    def test_copia_deve_ser_novo_dicionario(self):
        submissao_copiada = (
            homologacoes._copiar_submissao(
                self.submissao
            )
        )

        self.assertIsNot(
            submissao_copiada,
            self.submissao,
        )

        self.assertEqual(
            submissao_copiada,
            self.submissao,
        )

    def test_pacote_documental_deve_ser_independente(
        self
    ):
        submissao_copiada = (
            homologacoes._copiar_submissao(
                self.submissao
            )
        )

        submissao_copiada[
            "pacote_documental"
        ][0]["numero_versao"] = 99

        submissao_copiada[
            "pacote_documental"
        ].append(
            {
                "codigo_documento": 10,
                "numero_versao": 1,
            }
        )

        self.assertEqual(
            self.submissao[
                "pacote_documental"
            ],
            [
                {
                    "codigo_documento": 3,
                    "numero_versao": 1,
                }
            ],
        )

        self.assertIsNot(
            submissao_copiada["pacote_documental"],
            self.submissao["pacote_documental"],
        )

        self.assertIsNot(
            submissao_copiada[
                "pacote_documental"
            ][0],
            self.submissao[
                "pacote_documental"
            ][0],
        )

    def test_codigos_exigencias_devem_formar_lista_independente(
        self
    ):
        submissao_copiada = (
            homologacoes._copiar_submissao(
                self.submissao
            )
        )

        submissao_copiada[
            "codigos_exigencias_relacionadas"
        ].append(50)

        self.assertEqual(
            self.submissao[
                "codigos_exigencias_relacionadas"
            ],
            [],
        )

        self.assertEqual(
            submissao_copiada[
                "codigos_exigencias_relacionadas"
            ],
            [50],
        )

        self.assertIsNot(
            submissao_copiada[
                "codigos_exigencias_relacionadas"
            ],
            self.submissao[
                "codigos_exigencias_relacionadas"
            ],
        )

    def test_lista_de_respostas_deve_ser_independente(
        self
    ):
        submissao_copiada = (
            homologacoes._copiar_submissao(
                self.submissao
            )
        )

        submissao_copiada["respostas"].append(
            {
                "codigo": 1,
                "tipo": "RESPOSTA_DE_TESTE",
            }
        )

        self.assertEqual(
            self.submissao["respostas"],
            [],
        )

        self.assertEqual(
            len(submissao_copiada["respostas"]),
            1,
        )

        self.assertIsNot(
            submissao_copiada["respostas"],
            self.submissao["respostas"],
        )

    def test_alterar_status_da_copia_nao_deve_alterar_original(
        self
    ):
        submissao_copiada = (
            homologacoes._copiar_submissao(
                self.submissao
            )
        )

        submissao_copiada["status_operacional"] = (
            "PRONTA_PARA_ENVIO"
        )

        self.assertEqual(
            self.submissao["status_operacional"],
            "EM_PREPARACAO",
        )


class TestCopiaHomologacao(unittest.TestCase):
    """
    Testes da cópia candidata usada na preparação de Eventos.
    """

    def setUp(self):
        self.homologacao = (
            homologacoes.criar_dados_homologacao(
                codigo=1,
                codigo_empresa=1,
                codigo_projeto=10,
                codigo_concessionaria=2,
                data_abertura="2026-08-01",
                responsavel_abertura="Ana Lima",
            )
        )

    def test_copia_deve_isolar_lista_de_movimentacoes(
        self
    ):
        movimentacao_adicional = {
            "codigo": 2,
            "tipo_evento": "EVENTO_DE_TESTE",
        }

        homologacao_copiada = (
            homologacoes._copiar_homologacao(
                homologacao=self.homologacao,
                movimentacoes_adicionais=[
                    movimentacao_adicional
                ],
            )
        )

        self.assertIsNot(
            homologacao_copiada,
            self.homologacao,
        )

        self.assertIsNot(
            homologacao_copiada["movimentacoes"],
            self.homologacao["movimentacoes"],
        )

        self.assertEqual(
            len(self.homologacao["movimentacoes"]),
            1,
        )

        self.assertEqual(
            len(homologacao_copiada["movimentacoes"]),
            2,
        )

        homologacao_copiada["movimentacoes"].append(
            {
                "codigo": 3,
                "tipo_evento": "OUTRO_EVENTO",
            }
        )

        self.assertEqual(
            len(self.homologacao["movimentacoes"]),
            1,
        )

    def test_campos_escalares_da_copia_devem_ser_independentes(
        self
    ):
        homologacao_copiada = (
            homologacoes._copiar_homologacao(
                homologacao=self.homologacao,
            )
        )

        homologacao_copiada["status"] = "EM_ANALISE"

        homologacao_copiada["responsavel_atual"] = (
            "Carlos Souza"
        )

        self.assertEqual(
            self.homologacao["status"],
            "EM_PREPARACAO",
        )

        self.assertEqual(
            self.homologacao["responsavel_atual"],
            "Ana Lima",
        )

    def test_documentos_e_submissoes_permanecem_compartilhados(
        self
    ):
        """
        Documenta uma decisão arquitetural intencional.

        A cópia da Homologação é utilizada somente para preparar
        Eventos de estado. Por isso, Documentos e Submissões não
        são duplicados profundamente.
        """

        homologacao_copiada = (
            homologacoes._copiar_homologacao(
                homologacao=self.homologacao,
            )
        )

        self.assertIs(
            homologacao_copiada["documentos"],
            self.homologacao["documentos"],
        )

        self.assertIs(
            homologacao_copiada["submissoes"],
            self.homologacao["submissoes"],
        )

class TestAtomicidadeDocumentos(unittest.TestCase):
    """
    Testes de atomicidade das operações documentais
    coordenadas pela Homologação.
    """

    def test_falha_no_versionamento_nao_deve_substituir_documento_anterior(
        self
    ):
        """
        Quando uma nova versão for inválida:

        - o Documento anterior deve preservar seu estado;
        - a nova versão não deve entrar no agregado;
        - nenhuma nova Movimentação deve ser registrada.
        """

        homologacao = homologacoes.criar_dados_homologacao(
            codigo=1,
            codigo_empresa=1,
            codigo_projeto=10,
            codigo_concessionaria=2,
            data_abertura="2026-08-01",
            responsavel_abertura="Ana Lima",
        )

        primeira_versao = (
            criar_dados_documento_homologacao(
                codigo=1,
                nome="Diagrama unifilar",
                categoria="Projeto técnico",
                data_registro="2026-08-01",
                responsavel_registro="Ana Lima",
                origem=OrigemDocumento.EMPRESA,
                status=(
                    StatusDocumentoHomologacao.VALIDADO
                ),
                referencia_arquivo=(
                    "arquivos/diagrama_v1.pdf"
                ),
                versao=1,
            )
        )

        homologacoes.adicionar_documento_homologacao(
            homologacao=homologacao,
            documento=primeira_versao,
            data_movimentacao="2026-08-01",
            responsavel="Ana Lima",
        )

        # A versão é sequencial e referencia corretamente a
        # anterior, mas altera indevidamente a categoria.
        segunda_versao_invalida = (
            criar_dados_documento_homologacao(
                codigo=2,
                nome="Diagrama unifilar",
                categoria="Categoria incompatível",
                data_registro="2026-08-02",
                responsavel_registro="Carlos Souza",
                origem=OrigemDocumento.EMPRESA,
                status=(
                    StatusDocumentoHomologacao.RECEBIDO
                ),
                referencia_arquivo=(
                    "arquivos/diagrama_v2.pdf"
                ),
                versao=2,
                codigo_documento_anterior=1,
            )
        )

        quantidade_documentos = len(
            homologacao["documentos"]
        )

        quantidade_movimentacoes = len(
            homologacao["movimentacoes"]
        )

        with self.assertRaisesRegex(
            ValueError,
            "deve manter a mesma categoria",
        ):
            homologacoes.adicionar_documento_homologacao(
                homologacao=homologacao,
                documento=segunda_versao_invalida,
                data_movimentacao="2026-08-02",
                responsavel="Carlos Souza",
            )

        self.assertEqual(
            primeira_versao["status"],
            StatusDocumentoHomologacao.VALIDADO.value,
        )

        self.assertEqual(
            len(homologacao["documentos"]),
            quantidade_documentos,
        )

        self.assertNotIn(
            segunda_versao_invalida,
            homologacao["documentos"],
        )

        self.assertEqual(
            len(homologacao["movimentacoes"]),
            quantidade_movimentacoes,
        )

        self.assertIs(
            homologacao["documentos"][0],
            primeira_versao,
        )

    def test_falha_na_alteracao_nao_deve_modificar_documento(
        self
    ):
        """
        Quando a alteração documental falhar:

        - o status original deve ser preservado;
        - a referência de arquivo deve permanecer intacta;
        - nenhuma nova Movimentação deve ser registrada;
        - o responsável atual da Homologação não deve mudar.
        """

        homologacao = homologacoes.criar_dados_homologacao(
            codigo=1,
            codigo_empresa=1,
            codigo_projeto=10,
            codigo_concessionaria=2,
            data_abertura="2026-08-01",
            responsavel_abertura="Ana Lima",
        )

        documento = criar_dados_documento_homologacao(
            codigo=1,
            nome="Diagrama unifilar",
            categoria="Projeto técnico",
            data_registro="2026-08-01",
            responsavel_registro="Ana Lima",
            origem=OrigemDocumento.EMPRESA,
            status=StatusDocumentoHomologacao.RECEBIDO,
            referencia_arquivo="arquivos/diagrama_v1.pdf",
        )

        homologacoes.adicionar_documento_homologacao(
            homologacao=homologacao,
            documento=documento,
            data_movimentacao="2026-08-01",
            responsavel="Ana Lima",
        )

        status_anterior = documento["status"]

        referencia_anterior = documento[
            "referencia_arquivo"
        ]

        responsavel_anterior = homologacao[
            "responsavel_atual"
        ]

        quantidade_movimentacoes = len(
            homologacao["movimentacoes"]
        )

        # RECEBIDO -> EM_VALIDACAO é uma transição válida.
        #
        # Porém, referencia_arquivo não pode ser informada nessa
        # transição. Ela somente é aceita em:
        #
        # SOLICITADO -> RECEBIDO
        with self.assertRaisesRegex(
            ValueError,
            "somente deve ser informada",
        ):
            homologacoes.alterar_status_documento_homologacao(
                homologacao=homologacao,
                codigo_documento=documento["codigo"],
                novo_status=(
                    StatusDocumentoHomologacao.EM_VALIDACAO
                ),
                data_movimentacao="2026-08-02",
                responsavel="Carlos Souza",
                referencia_arquivo=(
                    "arquivos/arquivo_indevido.pdf"
                ),
            )

        self.assertEqual(
            documento["status"],
            status_anterior,
        )

        self.assertEqual(
            documento["referencia_arquivo"],
            referencia_anterior,
        )

        self.assertEqual(
            homologacao["responsavel_atual"],
            responsavel_anterior,
        )

        self.assertEqual(
            len(homologacao["movimentacoes"]),
            quantidade_movimentacoes,
        )

        self.assertIs(
            homologacao["documentos"][0],
            documento,
        )

class TestAtomicidadeSubmissoes(unittest.TestCase):
    """
    Testes de atomicidade das operações sobre Submissões
    pertencentes à Homologação.
    """

    def test_cancelamento_sem_motivo_nao_deve_alterar_submissao(
        self
    ):
        """
        Quando o cancelamento falhar por ausência de motivo:

        - o status operacional deve ser preservado;
        - nenhuma Movimentação deve ser registrada;
        - o responsável atual da Homologação não deve mudar;
        - os demais campos da Submissão devem permanecer intactos.
        """

        homologacao = homologacoes.criar_dados_homologacao(
            codigo=1,
            codigo_empresa=1,
            codigo_projeto=10,
            codigo_concessionaria=2,
            data_abertura="2026-08-01",
            responsavel_abertura="Ana Lima",
        )

        documento = criar_dados_documento_homologacao(
            codigo=1,
            nome="Fatura de energia",
            categoria="Unidade Consumidora",
            data_registro="2026-08-01",
            responsavel_registro="Ana Lima",
            origem=OrigemDocumento.CLIENTE,
            status=StatusDocumentoHomologacao.RECEBIDO,
            referencia_arquivo="arquivos/fatura.pdf",
        )

        homologacoes.adicionar_documento_homologacao(
            homologacao=homologacao,
            documento=documento,
            data_movimentacao="2026-08-01",
            responsavel="Ana Lima",
        )

        referencia = criar_referencia_documento(
            codigo_documento=documento["codigo"],
            numero_versao=documento["versao"],
        )

        submissao = criar_dados_submissao(
            codigo=1,
            numero_sequencial=1,
            tipo="INICIAL",
            data_criacao="2026-08-01",
            responsavel_criacao="Ana Lima",
            pacote_documental=[referencia],
        )

        homologacoes.adicionar_submissao_homologacao(
            homologacao=homologacao,
            submissao=submissao,
            data_movimentacao="2026-08-01",
            responsavel="Ana Lima",
        )

        status_anterior = submissao[
            "status_operacional"
        ]

        responsavel_anterior = homologacao[
            "responsavel_atual"
        ]

        quantidade_movimentacoes = len(
            homologacao["movimentacoes"]
        )

        pacote_anterior = [
            referencia.copy()
            for referencia
            in submissao["pacote_documental"]
        ]

        with self.assertRaisesRegex(
            ValueError,
            "exige uma justificativa",
        ):
            homologacoes.alterar_status_operacional_submissao(
                homologacao=homologacao,
                codigo_submissao=submissao["codigo"],
                novo_status="CANCELADA",
                data_movimentacao="2026-08-02",
                responsavel="Carlos Souza",
                motivo=None,
            )

        self.assertEqual(
            submissao["status_operacional"],
            status_anterior,
        )

        self.assertEqual(
            submissao["status_operacional"],
            "EM_PREPARACAO",
        )

        self.assertEqual(
            submissao["pacote_documental"],
            pacote_anterior,
        )

        self.assertEqual(
            homologacao["responsavel_atual"],
            responsavel_anterior,
        )

        self.assertEqual(
            homologacao["responsavel_atual"],
            "Ana Lima",
        )

        self.assertEqual(
            len(homologacao["movimentacoes"]),
            quantidade_movimentacoes,
        )

        self.assertIs(
            homologacao["submissoes"][0],
            submissao,
        )

    def test_falha_no_evento_nao_deve_adicionar_submissao_derivada(
        self
    ):
        """
        Quando a preparação do Evento de criação de uma
        Submissão derivada falhar:

        - a nova Submissão não deve entrar no agregado;
        - nenhuma Movimentação deve ser registrada;
        - o status geral da Homologação deve ser preservado;
        - o responsável atual não deve mudar;
        - a Exigência deve continuar pendente;
        - a própria Submissão externa deve permanecer intacta.
        """

        homologacao = homologacoes.criar_dados_homologacao(
            codigo=1,
            codigo_empresa=1,
            codigo_projeto=10,
            codigo_concessionaria=2,
            data_abertura="2026-08-01",
            responsavel_abertura="Ana Lima",
        )

        documento = criar_dados_documento_homologacao(
            codigo=1,
            nome="Diagrama unifilar",
            categoria="Projeto técnico",
            data_registro="2026-08-01",
            responsavel_registro="Ana Lima",
            origem=OrigemDocumento.EMPRESA,
            status=StatusDocumentoHomologacao.RECEBIDO,
            referencia_arquivo="arquivos/diagrama.pdf",
        )

        homologacoes.adicionar_documento_homologacao(
            homologacao=homologacao,
            documento=documento,
            data_movimentacao="2026-08-01",
            responsavel="Ana Lima",
        )

        referencia = criar_referencia_documento(
            codigo_documento=documento["codigo"],
            numero_versao=documento["versao"],
        )

        submissao_inicial = criar_dados_submissao(
            codigo=1,
            numero_sequencial=1,
            tipo="INICIAL",
            data_criacao="2026-08-01",
            responsavel_criacao="Ana Lima",
            pacote_documental=[referencia],
        )

        homologacoes.adicionar_submissao_homologacao(
            homologacao=homologacao,
            submissao=submissao_inicial,
            data_movimentacao="2026-08-01",
            responsavel="Ana Lima",
        )

        homologacoes.alterar_status_operacional_submissao(
            homologacao=homologacao,
            codigo_submissao=submissao_inicial["codigo"],
            novo_status="PRONTA_PARA_ENVIO",
            data_movimentacao="2026-08-02",
            responsavel="Carlos Souza",
        )

        homologacoes.alterar_status_homologacao(
            homologacao=homologacao,
            novo_status=StatusHomologacao.PRONTA_PARA_ENVIO,
            data_movimentacao="2026-08-02",
            responsavel="Carlos Souza",
        )

        homologacoes.enviar_submissao_homologacao(
            homologacao=homologacao,
            codigo_submissao=submissao_inicial["codigo"],
            canal_envio="PORTAL",
            data_envio="2026-08-03",
            responsavel_envio="Carlos Souza",
        )

        homologacoes.aplicar_evento_homologacao(
            homologacao=homologacao,
            evento=(
                EventoHomologacao
                .SUBMISSAO_INICIAL_ENVIADA
            ),
            data_movimentacao="2026-08-03",
            responsavel="Carlos Souza",
        )

        homologacoes.protocolar_submissao_homologacao(
            homologacao=homologacao,
            codigo_submissao=submissao_inicial["codigo"],
            protocolo="PROT-2026-001",
            data_protocolo="2026-08-04",
            responsavel="Ana Lima",
        )

        exigencia_externa = criar_dados_exigencia(
            codigo=1,
            numero_sequencial=1,
            tipo="COMPLEMENTACAO_DOCUMENTAL",
            descricao="Apresentar documento complementar.",
            codigos_documentos_afetados=[1],
        )

        resposta_exigencia = criar_dados_resposta_exigencia(
            codigo=1,
            numero_sequencial=1,
            data_resposta="2026-08-05",
            data_registro="2026-08-05",
            responsavel_registro="Maria Santos",
            descricao="Complementação documental necessária.",
            exigencias=[exigencia_externa],
            prazo_atendimento="30 dias",
        )

        homologacoes.adicionar_resposta_exigencia_concessionaria(
            homologacao=homologacao,
            codigo_submissao=submissao_inicial["codigo"],
            resposta=resposta_exigencia,
        )

        exigencia_armazenada = (
            submissao_inicial["respostas"][0]["exigencias"][0]
        )

        complementacao = criar_dados_submissao(
            codigo=2,
            numero_sequencial=2,
            tipo="COMPLEMENTACAO",
            data_criacao="2026-08-06",
            responsavel_criacao="Ana Lima",
            pacote_documental=[referencia],
            codigo_submissao_origem=(
                submissao_inicial["codigo"]
            ),
            codigo_resposta_origem=(
                resposta_exigencia["codigo"]
            ),
            codigos_exigencias_relacionadas=[
                exigencia_armazenada["codigo"]
            ],
        )

        quantidade_submissoes = len(
            homologacao["submissoes"]
        )

        quantidade_movimentacoes = len(
            homologacao["movimentacoes"]
        )

        status_anterior = homologacao["status"]

        responsavel_anterior = homologacao[
            "responsavel_atual"
        ]

        dados_complementacao_antes = {
            **complementacao,
            "pacote_documental": [
                referencia.copy()
                for referencia
                in complementacao["pacote_documental"]
            ],
            "codigos_exigencias_relacionadas": list(
                complementacao[
                    "codigos_exigencias_relacionadas"
                ]
            ),
            "respostas": list(
                complementacao["respostas"]
            ),
        }

        with patch(
            (
                "app.dominio.homologacoes."
                "_preparar_evento_homologacao"
            ),
            side_effect=RuntimeError(
                "Falha simulada na preparação do Evento."
            ),
        ):
            with self.assertRaisesRegex(
                RuntimeError,
                "Falha simulada",
            ):
                homologacoes.adicionar_submissao_homologacao(
                    homologacao=homologacao,
                    submissao=complementacao,
                    data_movimentacao="2026-08-06",
                    responsavel="Carlos Souza",
                )

        self.assertEqual(
            len(homologacao["submissoes"]),
            quantidade_submissoes,
        )

        self.assertNotIn(
            complementacao,
            homologacao["submissoes"],
        )

        self.assertEqual(
            len(homologacao["movimentacoes"]),
            quantidade_movimentacoes,
        )

        self.assertEqual(
            homologacao["status"],
            status_anterior,
        )

        self.assertEqual(
            homologacao["status"],
            StatusHomologacao.COM_EXIGENCIA.value,
        )

        self.assertEqual(
            homologacao["responsavel_atual"],
            responsavel_anterior,
        )

        self.assertEqual(
            exigencia_armazenada["status_atendimento"],
            "PENDENTE",
        )

        self.assertEqual(
            complementacao,
            dados_complementacao_antes,
        )

        self.assertEqual(
            complementacao["status_operacional"],
            "EM_PREPARACAO",
        )

        self.assertIs(
            homologacao["submissoes"][0],
            submissao_inicial,
        )

    def test_falha_no_evento_nao_deve_enviar_submissao_derivada(
        self
    ):
        """
        Quando o envio de uma Submissão derivada falhar durante
        a preparação do Evento da Homologação:

        - a Submissão deve permanecer pronta para envio;
        - os dados de envio devem permanecer vazios;
        - a Exigência deve continuar pendente;
        - nenhuma Movimentação deve ser registrada;
        - o responsável atual não deve mudar;
        - o estado geral da Homologação deve ser preservado.
        """

        homologacao = homologacoes.criar_dados_homologacao(
            codigo=1,
            codigo_empresa=1,
            codigo_projeto=10,
            codigo_concessionaria=2,
            data_abertura="2026-08-01",
            responsavel_abertura="Ana Lima",
        )

        # -----------------------------------------------------
        # Documento utilizado pelas Submissões
        # -----------------------------------------------------

        documento = criar_dados_documento_homologacao(
            codigo=1,
            nome="Diagrama unifilar",
            categoria="Projeto técnico",
            data_registro="2026-08-01",
            responsavel_registro="Ana Lima",
            origem=OrigemDocumento.EMPRESA,
            status=StatusDocumentoHomologacao.RECEBIDO,
            referencia_arquivo="arquivos/diagrama.pdf",
        )

        homologacoes.adicionar_documento_homologacao(
            homologacao=homologacao,
            documento=documento,
            data_movimentacao="2026-08-01",
            responsavel="Ana Lima",
        )

        referencia = criar_referencia_documento(
            codigo_documento=documento["codigo"],
            numero_versao=documento["versao"],
        )

        # -----------------------------------------------------
        # Submissão Inicial
        # -----------------------------------------------------

        submissao_inicial = criar_dados_submissao(
            codigo=1,
            numero_sequencial=1,
            tipo="INICIAL",
            data_criacao="2026-08-01",
            responsavel_criacao="Ana Lima",
            pacote_documental=[referencia],
        )

        homologacoes.adicionar_submissao_homologacao(
            homologacao=homologacao,
            submissao=submissao_inicial,
            data_movimentacao="2026-08-01",
            responsavel="Ana Lima",
        )

        homologacoes.alterar_status_operacional_submissao(
            homologacao=homologacao,
            codigo_submissao=submissao_inicial["codigo"],
            novo_status="PRONTA_PARA_ENVIO",
            data_movimentacao="2026-08-02",
            responsavel="Carlos Souza",
        )

        homologacoes.alterar_status_homologacao(
            homologacao=homologacao,
            novo_status=StatusHomologacao.PRONTA_PARA_ENVIO,
            data_movimentacao="2026-08-02",
            responsavel="Carlos Souza",
        )

        homologacoes.enviar_submissao_homologacao(
            homologacao=homologacao,
            codigo_submissao=submissao_inicial["codigo"],
            canal_envio="PORTAL",
            data_envio="2026-08-03",
            responsavel_envio="Carlos Souza",
        )

        homologacoes.aplicar_evento_homologacao(
            homologacao=homologacao,
            evento=(
                EventoHomologacao
                .SUBMISSAO_INICIAL_ENVIADA
            ),
            data_movimentacao="2026-08-03",
            responsavel="Carlos Souza",
        )

        homologacoes.protocolar_submissao_homologacao(
            homologacao=homologacao,
            codigo_submissao=submissao_inicial["codigo"],
            protocolo="PROT-2026-001",
            data_protocolo="2026-08-04",
            responsavel="Ana Lima",
        )

        # -----------------------------------------------------
        # Resposta contendo uma Exigência
        # -----------------------------------------------------

        exigencia_externa = criar_dados_exigencia(
            codigo=1,
            numero_sequencial=1,
            tipo="COMPLEMENTACAO_DOCUMENTAL",
            descricao="Apresentar documento complementar.",
            codigos_documentos_afetados=[1],
        )

        resposta_exigencia = criar_dados_resposta_exigencia(
            codigo=1,
            numero_sequencial=1,
            data_resposta="2026-08-05",
            data_registro="2026-08-05",
            responsavel_registro="Ana Lima",
            descricao="Complementação documental necessária.",
            exigencias=[exigencia_externa],
            prazo_atendimento="30 dias",
        )

        homologacoes.adicionar_resposta_exigencia_concessionaria(
            homologacao=homologacao,
            codigo_submissao=submissao_inicial["codigo"],
            resposta=resposta_exigencia,
        )

        # A Homologação armazena uma cópia defensiva da Exigência.
        exigencia_armazenada = (
            submissao_inicial["respostas"][0]["exigencias"][0]
        )

        # -----------------------------------------------------
        # Complementação
        # -----------------------------------------------------

        complementacao = criar_dados_submissao(
            codigo=2,
            numero_sequencial=2,
            tipo="COMPLEMENTACAO",
            data_criacao="2026-08-06",
            responsavel_criacao="Ana Lima",
            pacote_documental=[referencia],
            codigo_submissao_origem=(
                submissao_inicial["codigo"]
            ),
            codigo_resposta_origem=(
                resposta_exigencia["codigo"]
            ),
            codigos_exigencias_relacionadas=[
                exigencia_armazenada["codigo"]
            ],
        )

        homologacoes.adicionar_submissao_homologacao(
            homologacao=homologacao,
            submissao=complementacao,
            data_movimentacao="2026-08-06",
            responsavel="Ana Lima",
        )

        homologacoes.alterar_status_operacional_submissao(
            homologacao=homologacao,
            codigo_submissao=complementacao["codigo"],
            novo_status="PRONTA_PARA_ENVIO",
            data_movimentacao="2026-08-07",
            responsavel="Carlos Souza",
        )

        self.assertEqual(
            homologacao["status"],
            StatusHomologacao.EM_CORRECAO.value,
        )

        # -----------------------------------------------------
        # Estado anterior à operação que deverá falhar
        # -----------------------------------------------------

        # Simula uma inconsistência externa.
        #
        # O Evento SUBMISSAO_DERIVADA_ENVIADA exige que a
        # Homologação esteja em EM_CORRECAO.
        homologacao["status"] = (
            StatusHomologacao.COM_EXIGENCIA.value
        )

        status_submissao_anterior = complementacao[
            "status_operacional"
        ]

        responsavel_anterior = homologacao[
            "responsavel_atual"
        ]

        quantidade_movimentacoes = len(
            homologacao["movimentacoes"]
        )

        # -----------------------------------------------------
        # Operação
        # -----------------------------------------------------

        with self.assertRaisesRegex(
            ValueError,
            "não pode ser aplicado ao estado atual",
        ):
            homologacoes.enviar_submissao_homologacao(
                homologacao=homologacao,
                codigo_submissao=complementacao["codigo"],
                canal_envio="PORTAL",
                data_envio="2026-08-08",
                responsavel_envio="Carlos Souza",
            )

        # -----------------------------------------------------
        # Verificação da atomicidade
        # -----------------------------------------------------

        self.assertEqual(
            complementacao["status_operacional"],
            status_submissao_anterior,
        )

        self.assertEqual(
            complementacao["status_operacional"],
            "PRONTA_PARA_ENVIO",
        )

        self.assertIsNone(
            complementacao["canal_envio"]
        )

        self.assertIsNone(
            complementacao["data_envio"]
        )

        self.assertIsNone(
            complementacao["responsavel_envio"]
        )

        self.assertEqual(
            exigencia_armazenada["status_atendimento"],
            "PENDENTE",
        )

        self.assertIsNone(
            exigencia_armazenada[
                "codigo_submissao_atendimento"
            ]
        )

        self.assertIsNone(
            exigencia_armazenada["data_atendimento"]
        )

        self.assertIsNone(
            exigencia_armazenada[
                "responsavel_atendimento"
            ]
        )

        self.assertEqual(
            len(homologacao["movimentacoes"]),
            quantidade_movimentacoes,
        )

        self.assertEqual(
            homologacao["responsavel_atual"],
            responsavel_anterior,
        )

        self.assertEqual(
            homologacao["status"],
            StatusHomologacao.COM_EXIGENCIA.value,
        )

        self.assertIs(
            homologacao["submissoes"][1],
            complementacao,
        )

    def test_falha_na_movimentacao_nao_deve_protocolar_submissao(
        self
    ):
        """
        Quando ocorrer uma falha na construção da Movimentação
        de protocolo:

        - a Submissão deve permanecer ENVIADA;
        - os dados de protocolo devem permanecer vazios;
        - nenhuma Movimentação deve ser acrescentada;
        - o responsável atual da Homologação não deve mudar;
        - a própria instância armazenada deve ser preservada.

        A falha é simulada depois que a Submissão candidata já
        tiver sido criada e validada.
        """

        homologacao = homologacoes.criar_dados_homologacao(
            codigo=1,
            codigo_empresa=1,
            codigo_projeto=10,
            codigo_concessionaria=2,
            data_abertura="2026-08-01",
            responsavel_abertura="Ana Lima",
        )

        documento = criar_dados_documento_homologacao(
            codigo=1,
            nome="Fatura de energia",
            categoria="Unidade Consumidora",
            data_registro="2026-08-01",
            responsavel_registro="Ana Lima",
            origem=OrigemDocumento.CLIENTE,
            status=StatusDocumentoHomologacao.RECEBIDO,
            referencia_arquivo="arquivos/fatura.pdf",
        )

        homologacoes.adicionar_documento_homologacao(
            homologacao=homologacao,
            documento=documento,
            data_movimentacao="2026-08-01",
            responsavel="Ana Lima",
        )

        referencia = criar_referencia_documento(
            codigo_documento=documento["codigo"],
            numero_versao=documento["versao"],
        )

        submissao = criar_dados_submissao(
            codigo=1,
            numero_sequencial=1,
            tipo="INICIAL",
            data_criacao="2026-08-01",
            responsavel_criacao="Ana Lima",
            pacote_documental=[referencia],
        )

        homologacoes.adicionar_submissao_homologacao(
            homologacao=homologacao,
            submissao=submissao,
            data_movimentacao="2026-08-01",
            responsavel="Ana Lima",
        )

        homologacoes.alterar_status_operacional_submissao(
            homologacao=homologacao,
            codigo_submissao=submissao["codigo"],
            novo_status="PRONTA_PARA_ENVIO",
            data_movimentacao="2026-08-02",
            responsavel="Carlos Souza",
        )

        homologacoes.enviar_submissao_homologacao(
            homologacao=homologacao,
            codigo_submissao=submissao["codigo"],
            canal_envio="PORTAL",
            data_envio="2026-08-03",
            responsavel_envio="Carlos Souza",
        )

        self.assertEqual(
            submissao["status_operacional"],
            "ENVIADA",
        )

        status_anterior = submissao[
            "status_operacional"
        ]

        protocolo_anterior = submissao[
            "protocolo"
        ]

        data_protocolo_anterior = submissao[
            "data_protocolo"
        ]

        responsavel_anterior = homologacao[
            "responsavel_atual"
        ]

        quantidade_movimentacoes = len(
            homologacao["movimentacoes"]
        )

        with patch(
            (
                "app.dominio.homologacoes."
                "criar_movimentacao_submissao_protocolada"
            ),
            side_effect=RuntimeError(
                "Falha simulada na criação da Movimentação."
            ),
        ):
            with self.assertRaisesRegex(
                RuntimeError,
                "Falha simulada",
            ):
                homologacoes.protocolar_submissao_homologacao(
                    homologacao=homologacao,
                    codigo_submissao=submissao["codigo"],
                    protocolo="PROT-2026-001",
                    data_protocolo="2026-08-04",
                    responsavel="Maria Santos",
                )

        self.assertEqual(
            submissao["status_operacional"],
            status_anterior,
        )

        self.assertEqual(
            submissao["status_operacional"],
            "ENVIADA",
        )

        self.assertEqual(
            submissao["protocolo"],
            protocolo_anterior,
        )

        self.assertIsNone(
            submissao["protocolo"]
        )

        self.assertEqual(
            submissao["data_protocolo"],
            data_protocolo_anterior,
        )

        self.assertIsNone(
            submissao["data_protocolo"]
        )

        self.assertEqual(
            homologacao["responsavel_atual"],
            responsavel_anterior,
        )

        self.assertEqual(
            homologacao["responsavel_atual"],
            "Carlos Souza",
        )

        self.assertEqual(
            len(homologacao["movimentacoes"]),
            quantidade_movimentacoes,
        )

        self.assertIs(
            homologacao["submissoes"][0],
            submissao,
        )

class TestAtomicidadeRespostas(unittest.TestCase):
    """
    Testes de atomicidade do registro de Respostas
    da concessionária.
    """

    def test_falha_no_evento_nao_deve_registrar_resposta(
        self
    ):
        """
        Quando a preparação do Evento da Homologação falhar:

        - a Resposta não deve entrar na Submissão;
        - o status da análise deve permanecer inalterado;
        - nenhuma Movimentação deve ser registrada;
        - o estado geral da Homologação deve permanecer intacto;
        - o responsável atual não deve mudar.
        """

        homologacao = homologacoes.criar_dados_homologacao(
            codigo=1,
            codigo_empresa=1,
            codigo_projeto=10,
            codigo_concessionaria=2,
            data_abertura="2026-08-01",
            responsavel_abertura="Ana Lima",
        )

        documento = criar_dados_documento_homologacao(
            codigo=1,
            nome="Diagrama unifilar",
            categoria="Projeto técnico",
            data_registro="2026-08-01",
            responsavel_registro="Ana Lima",
            origem=OrigemDocumento.EMPRESA,
            status=StatusDocumentoHomologacao.RECEBIDO,
            referencia_arquivo="arquivos/diagrama.pdf",
        )

        homologacoes.adicionar_documento_homologacao(
            homologacao=homologacao,
            documento=documento,
            data_movimentacao="2026-08-01",
            responsavel="Ana Lima",
        )

        referencia = criar_referencia_documento(
            codigo_documento=documento["codigo"],
            numero_versao=documento["versao"],
        )

        submissao = criar_dados_submissao(
            codigo=1,
            numero_sequencial=1,
            tipo="INICIAL",
            data_criacao="2026-08-01",
            responsavel_criacao="Ana Lima",
            pacote_documental=[referencia],
        )

        homologacoes.adicionar_submissao_homologacao(
            homologacao=homologacao,
            submissao=submissao,
            data_movimentacao="2026-08-01",
            responsavel="Ana Lima",
        )

        homologacoes.alterar_status_operacional_submissao(
            homologacao=homologacao,
            codigo_submissao=submissao["codigo"],
            novo_status="PRONTA_PARA_ENVIO",
            data_movimentacao="2026-08-02",
            responsavel="Carlos Souza",
        )

        homologacoes.alterar_status_homologacao(
            homologacao=homologacao,
            novo_status=StatusHomologacao.PRONTA_PARA_ENVIO,
            data_movimentacao="2026-08-02",
            responsavel="Carlos Souza",
        )

        homologacoes.enviar_submissao_homologacao(
            homologacao=homologacao,
            codigo_submissao=submissao["codigo"],
            canal_envio="PORTAL",
            data_envio="2026-08-03",
            responsavel_envio="Carlos Souza",
        )

        homologacoes.aplicar_evento_homologacao(
            homologacao=homologacao,
            evento=(
                EventoHomologacao
                .SUBMISSAO_INICIAL_ENVIADA
            ),
            data_movimentacao="2026-08-03",
            responsavel="Carlos Souza",
        )

        homologacoes.protocolar_submissao_homologacao(
            homologacao=homologacao,
            codigo_submissao=submissao["codigo"],
            protocolo="PROT-2026-001",
            data_protocolo="2026-08-04",
            responsavel="Ana Lima",
        )

        resposta = criar_dados_resposta_inicio_analise(
            codigo=1,
            numero_sequencial=1,
            data_resposta="2026-08-05",
            data_registro="2026-08-05",
            responsavel_registro="Maria Santos",
            descricao="Análise técnica iniciada.",
        )

        respostas_anteriores = list(
            submissao["respostas"]
        )

        status_analise_anterior = submissao[
            "status_analise"
        ]

        status_homologacao_anterior = homologacao[
            "status"
        ]

        responsavel_anterior = homologacao[
            "responsavel_atual"
        ]

        quantidade_movimentacoes = len(
            homologacao["movimentacoes"]
        )

        with patch(
            (
                "app.dominio.homologacoes."
                "_preparar_evento_homologacao"
            ),
            side_effect=RuntimeError(
                "Falha simulada na preparação do Evento."
            ),
        ):
            with self.assertRaisesRegex(
                RuntimeError,
                "Falha simulada",
            ):
                homologacoes.adicionar_resposta_concessionaria(
                    homologacao=homologacao,
                    codigo_submissao=submissao["codigo"],
                    resposta=resposta,
                )

        self.assertEqual(
            submissao["respostas"],
            respostas_anteriores,
        )

        self.assertEqual(
            submissao["respostas"],
            [],
        )

        self.assertEqual(
            submissao["status_analise"],
            status_analise_anterior,
        )

        self.assertEqual(
            submissao["status_analise"],
            "SEM_RESPOSTA",
        )

        self.assertEqual(
            homologacao["status"],
            status_homologacao_anterior,
        )

        self.assertEqual(
            homologacao["status"],
            (
                StatusHomologacao
                .ENVIADA_A_CONCESSIONARIA
                .value
            ),
        )

        self.assertEqual(
            homologacao["responsavel_atual"],
            responsavel_anterior,
        )

        self.assertEqual(
            homologacao["responsavel_atual"],
            "Ana Lima",
        )

        self.assertEqual(
            len(homologacao["movimentacoes"]),
            quantidade_movimentacoes,
        )

        self.assertIs(
            homologacao["submissoes"][0],
            submissao,
        )

    def test_falha_no_evento_nao_deve_registrar_resposta_exigencia(
        self
    ):
        """
        Quando a preparação do Evento EXIGENCIA_RECEBIDA falhar:

        - a Resposta de Exigência não deve entrar na Submissão;
        - nenhuma Exigência deve ser armazenada no agregado;
        - o status da análise deve permanecer SEM_RESPOSTA;
        - nenhuma Movimentação deve ser registrada;
        - o estado geral da Homologação deve permanecer intacto;
        - o responsável atual não deve mudar;
        - os objetos externos devem permanecer inalterados.
        """

        homologacao = homologacoes.criar_dados_homologacao(
            codigo=1,
            codigo_empresa=1,
            codigo_projeto=10,
            codigo_concessionaria=2,
            data_abertura="2026-08-01",
            responsavel_abertura="Ana Lima",
        )

        documento = criar_dados_documento_homologacao(
            codigo=1,
            nome="Diagrama unifilar",
            categoria="Projeto técnico",
            data_registro="2026-08-01",
            responsavel_registro="Ana Lima",
            origem=OrigemDocumento.EMPRESA,
            status=StatusDocumentoHomologacao.RECEBIDO,
            referencia_arquivo="arquivos/diagrama.pdf",
        )

        homologacoes.adicionar_documento_homologacao(
            homologacao=homologacao,
            documento=documento,
            data_movimentacao="2026-08-01",
            responsavel="Ana Lima",
        )

        referencia = criar_referencia_documento(
            codigo_documento=documento["codigo"],
            numero_versao=documento["versao"],
        )

        submissao = criar_dados_submissao(
            codigo=1,
            numero_sequencial=1,
            tipo="INICIAL",
            data_criacao="2026-08-01",
            responsavel_criacao="Ana Lima",
            pacote_documental=[referencia],
        )

        homologacoes.adicionar_submissao_homologacao(
            homologacao=homologacao,
            submissao=submissao,
            data_movimentacao="2026-08-01",
            responsavel="Ana Lima",
        )

        homologacoes.alterar_status_operacional_submissao(
            homologacao=homologacao,
            codigo_submissao=submissao["codigo"],
            novo_status="PRONTA_PARA_ENVIO",
            data_movimentacao="2026-08-02",
            responsavel="Carlos Souza",
        )

        homologacoes.alterar_status_homologacao(
            homologacao=homologacao,
            novo_status=StatusHomologacao.PRONTA_PARA_ENVIO,
            data_movimentacao="2026-08-02",
            responsavel="Carlos Souza",
        )

        homologacoes.enviar_submissao_homologacao(
            homologacao=homologacao,
            codigo_submissao=submissao["codigo"],
            canal_envio="PORTAL",
            data_envio="2026-08-03",
            responsavel_envio="Carlos Souza",
        )

        homologacoes.aplicar_evento_homologacao(
            homologacao=homologacao,
            evento=(
                EventoHomologacao
                .SUBMISSAO_INICIAL_ENVIADA
            ),
            data_movimentacao="2026-08-03",
            responsavel="Carlos Souza",
        )

        homologacoes.protocolar_submissao_homologacao(
            homologacao=homologacao,
            codigo_submissao=submissao["codigo"],
            protocolo="PROT-2026-001",
            data_protocolo="2026-08-04",
            responsavel="Ana Lima",
        )

        exigencia_externa = criar_dados_exigencia(
            codigo=1,
            numero_sequencial=1,
            tipo="COMPLEMENTACAO_DOCUMENTAL",
            descricao="Apresentar documento complementar.",
            codigos_documentos_afetados=[1],
        )

        resposta_exigencia = criar_dados_resposta_exigencia(
            codigo=1,
            numero_sequencial=1,
            data_resposta="2026-08-05",
            data_registro="2026-08-05",
            responsavel_registro="Maria Santos",
            descricao="Complementação documental necessária.",
            exigencias=[exigencia_externa],
            prazo_atendimento="30 dias",
        )

        respostas_anteriores = list(
            submissao["respostas"]
        )

        status_analise_anterior = submissao[
            "status_analise"
        ]

        status_homologacao_anterior = homologacao[
            "status"
        ]

        responsavel_anterior = homologacao[
            "responsavel_atual"
        ]

        quantidade_movimentacoes = len(
            homologacao["movimentacoes"]
        )

        exigencia_externa_antes = {
            **exigencia_externa,
            "codigos_documentos_afetados": list(
                exigencia_externa[
                    "codigos_documentos_afetados"
                ]
            ),
        }

        with patch(
            (
                "app.dominio.homologacoes."
                "_preparar_evento_homologacao"
            ),
            side_effect=RuntimeError(
                "Falha simulada na preparação do Evento."
            ),
        ):
            with self.assertRaisesRegex(
                RuntimeError,
                "Falha simulada",
            ):
                (
                    homologacoes
                    .adicionar_resposta_exigencia_concessionaria(
                        homologacao=homologacao,
                        codigo_submissao=submissao["codigo"],
                        resposta=resposta_exigencia,
                    )
                )

        self.assertEqual(
            submissao["respostas"],
            respostas_anteriores,
        )

        self.assertEqual(
            submissao["respostas"],
            [],
        )

        self.assertEqual(
            submissao["status_analise"],
            status_analise_anterior,
        )

        self.assertEqual(
            submissao["status_analise"],
            "SEM_RESPOSTA",
        )

        self.assertEqual(
            homologacao["status"],
            status_homologacao_anterior,
        )

        self.assertEqual(
            homologacao["status"],
            (
                StatusHomologacao
                .ENVIADA_A_CONCESSIONARIA
                .value
            ),
        )

        self.assertEqual(
            homologacao["responsavel_atual"],
            responsavel_anterior,
        )

        self.assertEqual(
            homologacao["responsavel_atual"],
            "Ana Lima",
        )

        self.assertEqual(
            len(homologacao["movimentacoes"]),
            quantidade_movimentacoes,
        )

        self.assertEqual(
            exigencia_externa,
            exigencia_externa_antes,
        )

        self.assertEqual(
            exigencia_externa["status_atendimento"],
            "PENDENTE",
        )

        self.assertEqual(
            exigencia_externa[
                "codigos_documentos_afetados"
            ],
            [1],
        )

        self.assertIs(
            homologacao["submissoes"][0],
            submissao,
        )

if __name__ == "__main__":
    unittest.main()