import unittest

from app.dominio.homologacoes import (
    adicionar_documento_homologacao,
    adicionar_resposta_concessionaria,
    adicionar_resposta_exigencia_concessionaria,
    adicionar_submissao_homologacao,
    agendar_vistoria,
    alterar_status_documento_homologacao,
    alterar_status_homologacao,
    alterar_status_operacional_submissao,
    aplicar_evento_homologacao,
    buscar_homologacao_ativa_por_projeto,
    buscar_homologacao_por_codigo,
    buscar_homologacoes_por_concessionaria,
    buscar_homologacoes_por_status,
    buscar_submissao_por_codigo,
    buscar_submissao_por_numero_sequencial,
    codigo_homologacao_existe,
    concluir_instalacao,
    criar_dados_homologacao,
    enviar_submissao_homologacao,
    homologacao_esta_sem_responsavel,
    homologacao_possui_exigencia_aberta,
    homologacao_possui_submissao_aguardando_envio,
    homologacao_possui_submissao_aguardando_resposta,
    iniciar_instalacao,
    projeto_possui_homologacao_ativa,
    protocolar_submissao_homologacao,
    quantidade_homologacoes_aguardando_envio,
    quantidade_homologacoes_aguardando_resposta,
    quantidade_homologacoes_com_exigencia_aberta,
    quantidade_homologacoes_por_status,
    quantidade_homologacoes_sem_responsavel,
    quantidade_total_pendencias_homologacao,
    registrar_planejamento_instalacao,
    registrar_realizacao_vistoria,
    registrar_correcao_pos_vistoria,
    solicitar_vistoria,
    aprovar_vistoria,
    reprovar_vistoria,
)

from app.dominio.documentos_homologacao import (
    OrigemDocumento,
    StatusDocumentoHomologacao,
    criar_dados_documento_homologacao,
)

from app.dominio.exigencias_concessionaria import (
    criar_dados_exigencia,
)

from app.dominio.submissoes_homologacao import (
    CanalEnvioSubmissao,
    criar_dados_submissao,
    criar_referencia_documento,
)

from app.dominio.respostas_concessionaria import (
    criar_dados_resposta_aprovacao,
    criar_dados_resposta_exigencia,
    criar_dados_resposta_inicio_analise,
    criar_dados_resposta_recebimento,
    criar_dados_resposta_rejeicao,
)

from app.dominio.status_homologacao import (
    EventoHomologacao,
    StatusHomologacao,
)

from app.dominio.status_submissao import (
    StatusAnaliseSubmissao,
    StatusOperacionalSubmissao,
)

from app.dominio.operacoes_campo import (
    StatusVistoria,
)

class TestHomologacoesDominio(unittest.TestCase):
    """
    Testes das regras iniciais do domínio de Homologação.
    """

    def setUp(self):
        """
        Prepara dados reutilizados pelos testes.
        """

        self.homologacao_ativa = criar_dados_homologacao(
            codigo=1,
            codigo_empresa=1,
            codigo_projeto=10,
            codigo_concessionaria=2,
            data_abertura="2026-07-29",
            responsavel_abertura="Maria Santos",
            prazo_estimado_dias=45,
        )

        self.homologacao_concluida = criar_dados_homologacao(
            codigo=2,
            codigo_empresa=1,
            codigo_projeto=20,
            codigo_concessionaria=2,
            data_abertura="2026-06-01",
            responsavel_abertura="Carlos Souza",
            prazo_estimado_dias=30,
        )

        self.homologacao_concluida["status"] = (
            StatusHomologacao.CONCLUIDA.value
        )

        self.homologacoes = [
            self.homologacao_ativa,
            self.homologacao_concluida,
        ]

    def _criar_documento(
        self,
        codigo=1,
        nome="Fatura de energia",
        categoria="Unidade Consumidora",
        versao=1,
        codigo_documento_anterior=None,
    ):
        """
        Cria documentos reutilizáveis nos testes de integração
        entre Homologação e Documento.
        """

        return criar_dados_documento_homologacao(
            codigo=codigo,
            nome=nome,
            categoria=categoria,
            data_registro="2026-07-30",
            responsavel_registro="Ana Lima",
            origem=OrigemDocumento.CLIENTE,
            status=StatusDocumentoHomologacao.RECEBIDO,
            referencia_arquivo=(
                f"arquivos/documento_{codigo}.pdf"
            ),
            versao=versao,
            codigo_documento_anterior=(
                codigo_documento_anterior
            ),
        )

    def _criar_submissao_inicial(
        self,
        codigo=1,
        numero_sequencial=1,
        codigo_documento=1,
        numero_versao=1,
    ):
        """
        Cria uma Submissão Inicial reutilizável nos testes
        de integração com a Homologação.
        """

        referencia = criar_referencia_documento(
            codigo_documento=codigo_documento,
            numero_versao=numero_versao,
        )

        return criar_dados_submissao(
            codigo=codigo,
            numero_sequencial=numero_sequencial,
            tipo="INICIAL",
            data_criacao="2026-07-30",
            responsavel_criacao="Ana Lima",
            pacote_documental=[referencia],
        )

    def _adicionar_submissao_inicial_valida(
        self,
    ):
        """
        Adiciona à Homologação um Documento e uma Submissão
        Inicial válidos.

        Retorna a Submissão adicionada para reutilização nos testes.
        """

        documento = self._criar_documento()

        adicionar_documento_homologacao(
            homologacao=self.homologacao_ativa,
            documento=documento,
            data_movimentacao="2026-07-30",
            responsavel="Ana Lima",
        )

        submissao = self._criar_submissao_inicial()

        adicionar_submissao_homologacao(
            homologacao=self.homologacao_ativa,
            submissao=submissao,
            data_movimentacao="2026-07-30",
            responsavel="Ana Lima",
        )

        return submissao

    def _preparar_submissao_para_envio(
        self,
    ):
        """
        Cria uma Submissão válida e altera seu estado para
        PRONTA_PARA_ENVIO.

        Retorna a própria Submissão preparada.
        """

        submissao = (
            self._adicionar_submissao_inicial_valida()
        )

        alterar_status_operacional_submissao(
            homologacao=self.homologacao_ativa,
            codigo_submissao=submissao["codigo"],
            novo_status="PRONTA_PARA_ENVIO",
            data_movimentacao="2026-07-31",
            responsavel="Carlos Souza",
        )

        return submissao

    def _enviar_submissao_valida(
        self,
    ):
        """
        Cria, prepara e envia uma Submissão válida.

        Retorna a própria Submissão enviada.
        """

        submissao = (
            self._preparar_submissao_para_envio()
        )

        enviar_submissao_homologacao(
            homologacao=self.homologacao_ativa,
            codigo_submissao=submissao["codigo"],
            canal_envio="PORTAL",
            data_envio="2026-08-01",
            responsavel_envio="Carlos Souza",
        )

        return submissao

    def _protocolar_submissao_valida(
        self,
    ):
        """
        Cria, envia e protocola uma Submissão válida.
        """

        submissao = (
            self._enviar_submissao_valida()
        )

        protocolar_submissao_homologacao(
            homologacao=self.homologacao_ativa,
            codigo_submissao=submissao["codigo"],
            protocolo="PROT-2026-001",
            data_protocolo="2026-08-02",
            responsavel="Ana Lima",
        )

        return submissao

    def _protocolar_submissao_com_homologacao_sincronizada(
        self,
    ):
        """
        Cria, prepara, envia e protocola uma Submissão Inicial,
        mantendo também o estado geral da Homologação sincronizado.

        Fluxo produzido:

            Homologação:
                EM_PREPARACAO
                -> PRONTA_PARA_ENVIO
                -> ENVIADA_A_CONCESSIONARIA

            Submissão:
                EM_PREPARACAO
                -> PRONTA_PARA_ENVIO
                -> ENVIADA
                -> PROTOCOLADA

        Retorna a própria Submissão protocolada.
        """

        submissao = (
            self._preparar_submissao_para_envio()
        )

        alterar_status_homologacao(
            homologacao=self.homologacao_ativa,
            novo_status=(
                StatusHomologacao.PRONTA_PARA_ENVIO
            ),
            data_movimentacao="2026-07-31",
            responsavel="Carlos Souza",
            descricao=(
                "Homologação pronta para o envio "
                "da Submissão Inicial."
            ),
        )

        enviar_submissao_homologacao(
            homologacao=self.homologacao_ativa,
            codigo_submissao=submissao["codigo"],
            canal_envio="PORTAL",
            data_envio="2026-08-01",
            responsavel_envio="Carlos Souza",
        )

        aplicar_evento_homologacao(
            homologacao=self.homologacao_ativa,
            evento=(
                EventoHomologacao
                .SUBMISSAO_INICIAL_ENVIADA
            ),
            data_movimentacao="2026-08-01",
            responsavel="Carlos Souza",
            descricao=(
                "Submissão Inicial enviada à concessionária."
            ),
        )

        protocolar_submissao_homologacao(
            homologacao=self.homologacao_ativa,
            codigo_submissao=submissao["codigo"],
            protocolo="PROT-2026-001",
            data_protocolo="2026-08-02",
            responsavel="Ana Lima",
        )

        return submissao

    def _criar_resposta_recebimento(
        self,
        codigo=1,
        numero_sequencial=1,
        data_resposta="2026-08-03",
        data_registro="2026-08-03",
    ):
        """
        Cria uma confirmação de recebimento reutilizável.
        """

        return criar_dados_resposta_recebimento(
            codigo=codigo,
            numero_sequencial=numero_sequencial,
            data_resposta=data_resposta,
            data_registro=data_registro,
            responsavel_registro="Ana Lima",
            descricao="Pacote recebido pela concessionária.",
        )

    def _criar_exigencia(
        self,
        codigo=1,
        numero_sequencial=1,
        tipo="CORRECAO_DOCUMENTAL",
        descricao="Corrigir o documento apresentado.",
        codigos_documentos_afetados=None,
    ):
        """
        Cria uma Exigência reutilizável nos testes de integração.

        Por padrão, a Exigência afeta o Documento de código 1,
        que já pertence à Submissão Inicial utilizada nos testes.
        """

        if codigos_documentos_afetados is None:
            codigos_documentos_afetados = [1]

        return criar_dados_exigencia(
            codigo=codigo,
            numero_sequencial=numero_sequencial,
            tipo=tipo,
            descricao=descricao,
            codigos_documentos_afetados=(
                codigos_documentos_afetados
            ),
        )

    def _criar_resposta_exigencia(
        self,
        codigo=1,
        numero_sequencial=1,
        exigencias=None,
        data_resposta="2026-08-05",
        data_registro="2026-08-05",
    ):
        """
        Cria uma Resposta de Exigência reutilizável.
        """

        if exigencias is None:
            exigencias = [
                self._criar_exigencia()
            ]

        return criar_dados_resposta_exigencia(
            codigo=codigo,
            numero_sequencial=numero_sequencial,
            data_resposta=data_resposta,
            data_registro=data_registro,
            responsavel_registro="Ana Lima",
            descricao=(
                "A concessionária solicitou correções."
            ),
            exigencias=exigencias,
            prazo_atendimento="30 dias",
        )

    def test_criar_homologacao_deve_definir_estado_inicial(self):
        self.assertEqual(
            self.homologacao_ativa["status"],
            StatusHomologacao.EM_PREPARACAO.value,
        )

    def test_criar_homologacao_deve_calcular_previsao(self):
        self.assertEqual(
            self.homologacao_ativa[
                "data_prevista_conclusao"
            ],
            "2026-09-12",
        )

    def test_criar_homologacao_deve_iniciar_listas_vazias(self):
        campos = (
            "documentos",
            "submissoes",
            "protocolos",
            "exigencias",
            "pendencias",
            "prazos",
        )

        for campo in campos:
            self.assertEqual(
                self.homologacao_ativa[campo],
                [],
            )

    def test_criar_homologacao_deve_iniciar_operacoes_campo(
        self,
    ):
        """
        Toda nova Homologação deve possuir
        a estrutura inicial das Operações de Campo.
        """

        self.assertEqual(
            self.homologacao_ativa[
                "operacoes_campo"
            ],
            {
                "instalacao": None,
                "vistorias": [],
                "ligacao": None,
            },
        )

    def test_criar_homologacao_deve_registrar_movimentacao_inicial(
        self
    ):
        movimentacoes = self.homologacao_ativa[
            "movimentacoes"
        ]

        self.assertEqual(len(movimentacoes), 1)

        self.assertEqual(
            movimentacoes[0]["tipo_evento"],
            "HOMOLOGACAO_ABERTA",
        )

        self.assertEqual(
            movimentacoes[0]["novo_status"],
            StatusHomologacao.EM_PREPARACAO.value,
        )

    def test_responsavel_deve_ser_normalizado(self):
        homologacao = criar_dados_homologacao(
            codigo=3,
            codigo_empresa=1,
            codigo_projeto=30,
            codigo_concessionaria=2,
            data_abertura="2026-07-29",
            responsavel_abertura="  Ana Lima  ",
        )

        self.assertEqual(
            homologacao["responsavel_abertura"],
            "Ana Lima",
        )

        self.assertEqual(
            homologacao["responsavel_atual"],
            "Ana Lima",
        )

    def test_codigo_invalido_deve_gerar_erro(self):
        with self.assertRaises(ValueError):
            criar_dados_homologacao(
                codigo=0,
                codigo_empresa=1,
                codigo_projeto=10,
                codigo_concessionaria=2,
                data_abertura="2026-07-29",
                responsavel_abertura="Maria Santos",
            )

    def test_data_invalida_deve_gerar_erro(self):
        with self.assertRaises(ValueError):
            criar_dados_homologacao(
                codigo=3,
                codigo_empresa=1,
                codigo_projeto=10,
                codigo_concessionaria=2,
                data_abertura="29/07/2026",
                responsavel_abertura="Maria Santos",
            )

    def test_prazo_invalido_deve_gerar_erro(self):
        with self.assertRaises(ValueError):
            criar_dados_homologacao(
                codigo=3,
                codigo_empresa=1,
                codigo_projeto=10,
                codigo_concessionaria=2,
                data_abertura="2026-07-29",
                responsavel_abertura="Maria Santos",
                prazo_estimado_dias=0,
            )

    def test_buscar_homologacao_por_codigo(self):
        resultado = buscar_homologacao_por_codigo(
            homologacoes=self.homologacoes,
            codigo=1,
        )

        self.assertIs(
            resultado,
            self.homologacao_ativa,
        )

    def test_busca_deve_respeitar_empresa(self):
        resultado = buscar_homologacao_por_codigo(
            homologacoes=self.homologacoes,
            codigo=1,
            codigo_empresa=999,
        )

        self.assertIsNone(resultado)

    def test_buscar_homologacoes_por_concessionaria(
        self,
    ):
        """
        Deve retornar somente as Homologações
        da Concessionária informada.
        """

        outra_homologacao = criar_dados_homologacao(
            codigo=3,
            codigo_empresa=1,
            codigo_projeto=30,
            codigo_concessionaria=99,
            data_abertura="2026-07-01",
            responsavel_abertura="Ana Lima",
            prazo_estimado_dias=45,
        )

        self.homologacoes.append(
            outra_homologacao
        )

        resultado = buscar_homologacoes_por_concessionaria(
            homologacoes=self.homologacoes,
            codigo_concessionaria=2,
        )

        self.assertEqual(
            len(resultado),
            2,
        )

        self.assertTrue(
            all(
                homologacao["codigo_concessionaria"] == 2
                for homologacao in resultado
            )
        )

    def test_busca_por_concessionaria_deve_respeitar_empresa(
        self,
    ):
        """
        Quando a Empresa for informada, a consulta
        deve aplicar também o isolamento multiempresa.
        """

        outra_empresa = criar_dados_homologacao(
            codigo=3,
            codigo_empresa=20,
            codigo_projeto=30,
            codigo_concessionaria=2,
            data_abertura="2026-07-01",
            responsavel_abertura="Ana Lima",
            prazo_estimado_dias=45,
        )

        self.homologacoes.append(
            outra_empresa
        )

        resultado = buscar_homologacoes_por_concessionaria(
            homologacoes=self.homologacoes,
            codigo_concessionaria=2,
            codigo_empresa=1,
        )

        self.assertEqual(
            len(resultado),
            2,
        )

        self.assertTrue(
            all(
                homologacao["codigo_empresa"] == 1
                for homologacao in resultado
            )
        )

    def test_busca_por_concessionaria_sem_resultados(
        self,
    ):
        """
        Deve retornar lista vazia quando não houver
        Homologações para a Concessionária.
        """

        resultado = buscar_homologacoes_por_concessionaria(
            homologacoes=self.homologacoes,
            codigo_concessionaria=999,
        )

        self.assertEqual(
            resultado,
            [],
        )

    def test_busca_por_concessionaria_nao_deve_alterar_colecao(
        self,
    ):
        """
        A consulta não deve modificar
        as Homologações recebidas.
        """

        homologacoes_antes = [
            homologacao.copy()
            for homologacao in self.homologacoes
        ]

        buscar_homologacoes_por_concessionaria(
            homologacoes=self.homologacoes,
            codigo_concessionaria=2,
        )

        self.assertEqual(
            self.homologacoes,
            homologacoes_antes,
        )

    def test_codigo_homologacao_deve_existir(self):
        resultado = codigo_homologacao_existe(
            homologacoes=self.homologacoes,
            codigo=1,
            codigo_empresa=1,
        )

        self.assertTrue(resultado)

    def test_codigo_homologacao_nao_deve_existir(self):
        resultado = codigo_homologacao_existe(
            homologacoes=self.homologacoes,
            codigo=999,
            codigo_empresa=1,
        )

        self.assertFalse(resultado)

    # ========================================================
    # CONSULTAS DE PENDÊNCIAS
    # ========================================================

    def test_quantidade_homologacoes_por_status(self):
        """
        Deve contar somente as Homologações
        que possuem o status informado.
        """

        self.homologacao_ativa["status"] = (
            StatusHomologacao
            .AGUARDANDO_DOCUMENTACAO
            .value
        )

        resultado = quantidade_homologacoes_por_status(
            homologacoes=self.homologacoes,
            status=(
                StatusHomologacao
                .AGUARDANDO_DOCUMENTACAO
            ),
        )

        self.assertEqual(
            resultado,
            1,
        )

    def test_quantidade_por_status_deve_aceitar_texto(self):
        """
        A consulta também deve aceitar o valor textual
        persistido no JSON.
        """

        self.homologacao_ativa["status"] = (
            StatusHomologacao
            .AGUARDANDO_DOCUMENTACAO
            .value
        )

        resultado = quantidade_homologacoes_por_status(
            homologacoes=self.homologacoes,
            status="AGUARDANDO_DOCUMENTACAO",
        )

        self.assertEqual(
            resultado,
            1,
        )

    def test_buscar_homologacoes_por_status(
        self,
    ):
        """
        Deve retornar somente as Homologações
        que possuem o status informado.
        """

        self.homologacao_ativa["status"] = (
            StatusHomologacao
            .AGUARDANDO_DOCUMENTACAO
            .value
        )

        resultado = buscar_homologacoes_por_status(
            homologacoes=self.homologacoes,
            status=(
                StatusHomologacao
                .AGUARDANDO_DOCUMENTACAO
            ),
        )

        self.assertEqual(
            len(resultado),
            1,
        )

        self.assertEqual(
            resultado[0]["codigo"],
            self.homologacao_ativa["codigo"],
        )

    def test_busca_de_homologacoes_por_status_deve_aceitar_texto(
        self,
    ):
        """
        A consulta deve aceitar o valor textual
        persistido no JSON.
        """

        resultado = buscar_homologacoes_por_status(
            homologacoes=self.homologacoes,
            status="CONCLUIDA",
        )

        self.assertEqual(
            len(resultado),
            1,
        )

        self.assertEqual(
            resultado[0]["codigo"],
            self.homologacao_concluida["codigo"],
        )

    def test_busca_por_status_deve_respeitar_empresa(
        self,
    ):
        """
        Quando a Empresa for informada, a consulta
        deve aplicar o isolamento multiempresa.
        """

        outra_empresa = criar_dados_homologacao(
            codigo=3,
            codigo_empresa=20,
            codigo_projeto=30,
            codigo_concessionaria=2,
            data_abertura="2026-07-01",
            responsavel_abertura="Ana Lima",
            prazo_estimado_dias=45,
        )

        outra_empresa["status"] = (
            StatusHomologacao.CONCLUIDA.value
        )

        self.homologacoes.append(
            outra_empresa
        )

        resultado = buscar_homologacoes_por_status(
            homologacoes=self.homologacoes,
            status=StatusHomologacao.CONCLUIDA,
            codigo_empresa=1,
        )

        self.assertEqual(
            len(resultado),
            1,
        )

        self.assertEqual(
            resultado[0]["codigo_empresa"],
            1,
        )

    def test_busca_de_homologacoes_por_status_sem_resultados(
        self,
    ):
        """
        Deve retornar lista vazia quando nenhuma Homologação
        possuir o status informado.
        """

        resultado = buscar_homologacoes_por_status(
            homologacoes=self.homologacoes,
            status=StatusHomologacao.EM_ANALISE,
        )

        self.assertEqual(
            resultado,
            [],
        )

    def test_busca_de_homologacoes_por_status_nao_altera_colecao(
        self,
    ):
        """
        A consulta não deve modificar
        as Homologações recebidas.
        """

        homologacoes_antes = [
            homologacao.copy()
            for homologacao in self.homologacoes
        ]

        buscar_homologacoes_por_status(
            homologacoes=self.homologacoes,
            status=StatusHomologacao.CONCLUIDA,
        )

        self.assertEqual(
            self.homologacoes,
            homologacoes_antes,
        )

    def test_homologacao_deve_identificar_exigencia_aberta(
        self,
    ):
        """
        Deve localizar uma Exigência pendente dentro
        das Respostas das Submissões.
        """

        self.homologacao_ativa["submissoes"] = [
            {
                "codigo": 1,
                "respostas": [
                    {
                        "codigo": 1,
                        "exigencias": [
                            {
                                "codigo": 1,
                                "status_atendimento": "PENDENTE",
                            }
                        ],
                    }
                ],
            }
        ]

        resultado = homologacao_possui_exigencia_aberta(
            self.homologacao_ativa
        )

        self.assertTrue(
            resultado
        )

    def test_exigencia_atendida_nao_deve_ser_considerada_aberta(
        self,
    ):
        """
        Uma Exigência atendida não representa
        pendência operacional.
        """

        self.homologacao_ativa["submissoes"] = [
            {
                "codigo": 1,
                "respostas": [
                    {
                        "codigo": 1,
                        "exigencias": [
                            {
                                "codigo": 1,
                                "status_atendimento": "ATENDIDA",
                            }
                        ],
                    }
                ],
            }
        ]

        resultado = homologacao_possui_exigencia_aberta(
            self.homologacao_ativa
        )

        self.assertFalse(
            resultado
        )

    def test_homologacao_com_varias_exigencias_deve_ser_contada_uma_vez(
        self,
    ):
        """
        A contagem representa Homologações com pendência,
        e não o número total de Exigências.
        """

        self.homologacao_ativa["submissoes"] = [
            {
                "codigo": 1,
                "respostas": [
                    {
                        "codigo": 1,
                        "exigencias": [
                            {
                                "codigo": 1,
                                "status_atendimento": "PENDENTE",
                            },
                            {
                                "codigo": 2,
                                "status_atendimento": "PENDENTE",
                            },
                        ],
                    }
                ],
            }
        ]

        resultado = (
            quantidade_homologacoes_com_exigencia_aberta(
                self.homologacoes
            )
        )

        self.assertEqual(
            resultado,
            1,
        )

    def test_homologacao_deve_identificar_submissao_aguardando_envio(
        self,
    ):
        """
        Uma Submissão pronta para envio deve representar
        uma pendência operacional.
        """

        self.homologacao_ativa["submissoes"] = [
            {
                "codigo": 1,
                "status_operacional": (
                    StatusOperacionalSubmissao
                    .PRONTA_PARA_ENVIO
                    .value
                ),
                "status_analise": (
                    StatusAnaliseSubmissao
                    .SEM_RESPOSTA
                    .value
                ),
            }
        ]

        resultado = (
            homologacao_possui_submissao_aguardando_envio(
                self.homologacao_ativa
            )
        )

        self.assertTrue(
            resultado
        )

    def test_deve_contar_homologacao_aguardando_envio(
        self,
    ):
        """
        Deve contar uma Homologação ativa com
        Submissão pronta para envio.
        """

        self.homologacao_ativa["submissoes"] = [
            {
                "codigo": 1,
                "status_operacional": (
                    StatusOperacionalSubmissao
                    .PRONTA_PARA_ENVIO
                    .value
                ),
                "status_analise": (
                    StatusAnaliseSubmissao
                    .SEM_RESPOSTA
                    .value
                ),
            }
        ]

        resultado = quantidade_homologacoes_aguardando_envio(
            self.homologacoes
        )

        self.assertEqual(
            resultado,
            1,
        )

    def test_homologacao_terminal_nao_deve_aguardar_envio(
        self,
    ):
        """
        Uma Homologação concluída não deve aparecer
        nas pendências, mesmo contendo dados inconsistentes.
        """

        self.homologacao_concluida["submissoes"] = [
            {
                "codigo": 1,
                "status_operacional": (
                    StatusOperacionalSubmissao
                    .PRONTA_PARA_ENVIO
                    .value
                ),
                "status_analise": (
                    StatusAnaliseSubmissao
                    .SEM_RESPOSTA
                    .value
                ),
            }
        ]

        resultado = quantidade_homologacoes_aguardando_envio(
            [
                self.homologacao_concluida
            ]
        )

        self.assertEqual(
            resultado,
            0,
        )

    def test_homologacao_deve_identificar_submissao_aguardando_resposta(
        self,
    ):
        """
        Uma Submissão enviada e ainda sem resposta
        deve representar uma pendência.
        """

        self.homologacao_ativa["submissoes"] = [
            {
                "codigo": 1,
                "status_operacional": (
                    StatusOperacionalSubmissao
                    .ENVIADA
                    .value
                ),
                "status_analise": (
                    StatusAnaliseSubmissao
                    .SEM_RESPOSTA
                    .value
                ),
            }
        ]

        resultado = (
            homologacao_possui_submissao_aguardando_resposta(
                self.homologacao_ativa
            )
        )

        self.assertTrue(
            resultado
        )

    def test_submissao_em_preparacao_nao_deve_aguardar_resposta(
        self,
    ):
        """
        Uma Submissão ainda não enviada não pode estar
        aguardando retorno da concessionária.
        """

        self.homologacao_ativa["submissoes"] = [
            {
                "codigo": 1,
                "status_operacional": (
                    StatusOperacionalSubmissao
                    .EM_PREPARACAO
                    .value
                ),
                "status_analise": (
                    StatusAnaliseSubmissao
                    .SEM_RESPOSTA
                    .value
                ),
            }
        ]

        resultado = (
            homologacao_possui_submissao_aguardando_resposta(
                self.homologacao_ativa
            )
        )

        self.assertFalse(
            resultado
        )

    def test_deve_contar_homologacao_aguardando_resposta(
        self,
    ):
        """
        Deve contar uma Homologação ativa com
        Submissão protocolada e sem resposta.
        """

        self.homologacao_ativa["submissoes"] = [
            {
                "codigo": 1,
                "status_operacional": (
                    StatusOperacionalSubmissao
                    .PROTOCOLADA
                    .value
                ),
                "status_analise": (
                    StatusAnaliseSubmissao
                    .SEM_RESPOSTA
                    .value
                ),
            }
        ]

        resultado = (
            quantidade_homologacoes_aguardando_resposta(
                self.homologacoes
            )
        )

        self.assertEqual(
            resultado,
            1,
        )

    def test_homologacao_com_responsavel_vazio_deve_ser_identificada(
        self,
    ):
        """
        Um texto vazio não representa
        um responsável operacional válido.
        """

        self.homologacao_ativa["responsavel_atual"] = "   "

        resultado = homologacao_esta_sem_responsavel(
            self.homologacao_ativa
        )

        self.assertTrue(
            resultado
        )

    def test_homologacao_com_responsavel_nao_deve_ser_pendente(
        self,
    ):
        """
        Uma Homologação com responsável atual definido
        não deve ser classificada como sem responsável.
        """

        resultado = homologacao_esta_sem_responsavel(
            self.homologacao_ativa
        )

        self.assertFalse(
            resultado
        )

    def test_deve_contar_homologacao_sem_responsavel(
        self,
    ):
        """
        Deve contar somente Homologações ativas
        sem responsável atual.
        """

        self.homologacao_ativa["responsavel_atual"] = None
        self.homologacao_concluida["responsavel_atual"] = None

        resultado = quantidade_homologacoes_sem_responsavel(
            self.homologacoes
        )

        self.assertEqual(
            resultado,
            1,
        )

    def test_total_de_pendencias_deve_somar_as_categorias(
        self,
    ):
        """
        Uma mesma Homologação pode contribuir
        para categorias de pendência diferentes.
        """

        self.homologacao_ativa["status"] = (
            StatusHomologacao
            .AGUARDANDO_DOCUMENTACAO
            .value
        )

        self.homologacao_ativa["responsavel_atual"] = None

        self.homologacao_ativa["submissoes"] = [
            {
                "codigo": 1,
                "status_operacional": (
                    StatusOperacionalSubmissao
                    .PRONTA_PARA_ENVIO
                    .value
                ),
                "status_analise": (
                    StatusAnaliseSubmissao
                    .SEM_RESPOSTA
                    .value
                ),
                "respostas": [
                    {
                        "codigo": 1,
                        "exigencias": [
                            {
                                "codigo": 1,
                                "status_atendimento": "PENDENTE",
                            }
                        ],
                    }
                ],
            },
            {
                "codigo": 2,
                "status_operacional": (
                    StatusOperacionalSubmissao
                    .ENVIADA
                    .value
                ),
                "status_analise": (
                    StatusAnaliseSubmissao
                    .SEM_RESPOSTA
                    .value
                ),
                "respostas": [],
            },
        ]

        resultado = (
            quantidade_total_pendencias_homologacao(
                [
                    self.homologacao_ativa
                ]
            )
        )

        self.assertEqual(
            resultado,
            5,
        )

    def test_deve_buscar_homologacao_ativa_do_projeto(self):
        resultado = buscar_homologacao_ativa_por_projeto(
            homologacoes=self.homologacoes,
            codigo_projeto=10,
            codigo_empresa=1,
        )

        self.assertIs(
            resultado,
            self.homologacao_ativa,
        )

    def test_homologacao_concluida_nao_deve_ser_considerada_ativa(
        self
    ):
        resultado = buscar_homologacao_ativa_por_projeto(
            homologacoes=self.homologacoes,
            codigo_projeto=20,
            codigo_empresa=1,
        )

        self.assertIsNone(resultado)

    def test_projeto_deve_possuir_homologacao_ativa(self):
        resultado = projeto_possui_homologacao_ativa(
            homologacoes=self.homologacoes,
            codigo_projeto=10,
            codigo_empresa=1,
        )

        self.assertTrue(resultado)

    def test_projeto_nao_deve_possuir_homologacao_ativa(self):
        resultado = projeto_possui_homologacao_ativa(
            homologacoes=self.homologacoes,
            codigo_projeto=20,
            codigo_empresa=1,
        )

        self.assertFalse(resultado)

    def test_deve_alterar_status_com_transicao_valida(self):
        resultado = alterar_status_homologacao(
            homologacao=self.homologacao_ativa,
            novo_status=(
                StatusHomologacao.AGUARDANDO_DOCUMENTACAO
            ),
            data_movimentacao="2026-07-30",
            responsavel="Ana Lima",
        )

        self.assertIs(
            resultado,
            self.homologacao_ativa,
        )

        self.assertEqual(
            resultado["status"],
            (
                StatusHomologacao
                .AGUARDANDO_DOCUMENTACAO
                .value
            ),
        )

        self.assertEqual(
            resultado["responsavel_atual"],
            "Ana Lima",
        )

    def test_transicao_deve_registrar_movimentacao(self):
        alterar_status_homologacao(
            homologacao=self.homologacao_ativa,
            novo_status=(
                StatusHomologacao.AGUARDANDO_DOCUMENTACAO
            ),
            data_movimentacao="2026-07-30",
            responsavel="Ana Lima",
        )

        movimentacoes = self.homologacao_ativa[
            "movimentacoes"
        ]

        self.assertEqual(len(movimentacoes), 2)

        nova_movimentacao = movimentacoes[-1]

        self.assertEqual(
            nova_movimentacao["codigo"],
            2,
        )

        self.assertEqual(
            nova_movimentacao["tipo_evento"],
            "STATUS_HOMOLOGACAO_ALTERADO",
        )

        self.assertEqual(
            nova_movimentacao["status_anterior"],
            StatusHomologacao.EM_PREPARACAO.value,
        )

        self.assertEqual(
            nova_movimentacao["novo_status"],
            (
                StatusHomologacao
                .AGUARDANDO_DOCUMENTACAO
                .value
            ),
        )

    def test_deve_aceitar_novo_status_como_texto(self):
        alterar_status_homologacao(
            homologacao=self.homologacao_ativa,
            novo_status="AGUARDANDO_DOCUMENTACAO",
            data_movimentacao="2026-07-30",
            responsavel="Ana Lima",
        )

        self.assertEqual(
            self.homologacao_ativa["status"],
            "AGUARDANDO_DOCUMENTACAO",
        )

    def test_nao_deve_permitir_transicao_invalida(self):
        with self.assertRaises(ValueError):
            alterar_status_homologacao(
                homologacao=self.homologacao_ativa,
                novo_status=StatusHomologacao.CONCLUIDA,
                data_movimentacao="2026-07-30",
                responsavel="Ana Lima",
            )

        self.assertEqual(
            self.homologacao_ativa["status"],
            StatusHomologacao.EM_PREPARACAO.value,
        )

        self.assertEqual(
            len(self.homologacao_ativa["movimentacoes"]),
            1,
        )

    def test_nao_deve_permitir_transicao_para_o_mesmo_status(
        self
    ):
        with self.assertRaises(ValueError):
            alterar_status_homologacao(
                homologacao=self.homologacao_ativa,
                novo_status=(
                    StatusHomologacao.EM_PREPARACAO
                ),
                data_movimentacao="2026-07-30",
                responsavel="Ana Lima",
            )

    def test_cancelamento_deve_exigir_motivo(self):
        with self.assertRaises(ValueError):
            alterar_status_homologacao(
                homologacao=self.homologacao_ativa,
                novo_status=StatusHomologacao.CANCELADA,
                data_movimentacao="2026-07-30",
                responsavel="Ana Lima",
            )

    def test_deve_cancelar_quando_existir_motivo(self):
        alterar_status_homologacao(
            homologacao=self.homologacao_ativa,
            novo_status=StatusHomologacao.CANCELADA,
            data_movimentacao="2026-07-30",
            responsavel="Ana Lima",
            motivo="Cliente desistiu do serviço.",
        )

        self.assertEqual(
            self.homologacao_ativa["status"],
            StatusHomologacao.CANCELADA.value,
        )

        movimentacao = self.homologacao_ativa[
            "movimentacoes"
        ][-1]

        self.assertEqual(
            movimentacao["motivo"],
            "Cliente desistiu do serviço.",
        )

    def test_nao_deve_alterar_homologacao_cancelada(self):
        alterar_status_homologacao(
            homologacao=self.homologacao_ativa,
            novo_status=StatusHomologacao.CANCELADA,
            data_movimentacao="2026-07-30",
            responsavel="Ana Lima",
            motivo="Cliente desistiu do serviço.",
        )

        with self.assertRaises(ValueError):
            alterar_status_homologacao(
                homologacao=self.homologacao_ativa,
                novo_status=(
                    StatusHomologacao
                    .AGUARDANDO_DOCUMENTACAO
                ),
                data_movimentacao="2026-07-31",
                responsavel="Ana Lima",
            )

        self.assertEqual(
            len(self.homologacao_ativa["movimentacoes"]),
            2,
        )

    def test_transicao_deve_normalizar_textos(self):
        alterar_status_homologacao(
            homologacao=self.homologacao_ativa,
            novo_status=StatusHomologacao.CANCELADA,
            data_movimentacao="2026-07-30",
            responsavel="  Ana Lima  ",
            motivo="  Cliente desistiu.  ",
        )

        movimentacao = self.homologacao_ativa[
            "movimentacoes"
        ][-1]

        self.assertEqual(
            movimentacao["responsavel"],
            "Ana Lima",
        )

        self.assertEqual(
            movimentacao["motivo"],
            "Cliente desistiu.",
        )

    def test_deve_aceitar_descricao_personalizada(self):
        alterar_status_homologacao(
            homologacao=self.homologacao_ativa,
            novo_status=(
                StatusHomologacao.AGUARDANDO_DOCUMENTACAO
            ),
            data_movimentacao="2026-07-30",
            responsavel="Ana Lima",
            descricao=(
                "Processo aguardando documentos do cliente."
            ),
        )

        movimentacao = self.homologacao_ativa[
            "movimentacoes"
        ][-1]

        self.assertEqual(
            movimentacao["descricao"],
            "Processo aguardando documentos do cliente.",
        )

    def test_conclusao_deve_registrar_data_real(self):
        homologacao = criar_dados_homologacao(
            codigo=50,
            codigo_empresa=1,
            codigo_projeto=50,
            codigo_concessionaria=2,
            data_abertura="2026-06-01",
            responsavel_abertura="Maria Santos",
        )

        homologacao["status"] = (
            StatusHomologacao.SISTEMA_LIGADO.value
        )

        alterar_status_homologacao(
            homologacao=homologacao,
            novo_status=StatusHomologacao.CONCLUIDA,
            data_movimentacao="2026-07-30",
            responsavel="Ana Lima",
        )

        self.assertEqual(
            homologacao["status"],
            StatusHomologacao.CONCLUIDA.value,
        )

        self.assertEqual(
            homologacao["data_conclusao_real"],
            "2026-07-30",
        )

    def test_deve_adicionar_documento_a_homologacao(self):
        documento = self._criar_documento()

        resultado = adicionar_documento_homologacao(
            homologacao=self.homologacao_ativa,
            documento=documento,
            data_movimentacao="2026-07-30",
            responsavel="Ana Lima",
        )

        self.assertIs(
            resultado,
            self.homologacao_ativa,
        )

        self.assertEqual(
            len(resultado["documentos"]),
            1,
        )

        self.assertIs(
            resultado["documentos"][0],
            documento,
        )

    def test_adicao_de_documento_deve_registrar_movimentacao(
        self
    ):
        documento = self._criar_documento()

        adicionar_documento_homologacao(
            homologacao=self.homologacao_ativa,
            documento=documento,
            data_movimentacao="2026-07-30",
            responsavel="Ana Lima",
        )

        movimentacoes = self.homologacao_ativa[
            "movimentacoes"
        ]

        self.assertEqual(
            len(movimentacoes),
            2,
        )

        movimentacao = movimentacoes[-1]

        self.assertEqual(
            movimentacao["codigo"],
            2,
        )

        self.assertEqual(
            movimentacao["tipo_evento"],
            "DOCUMENTO_ADICIONADO",
        )

        self.assertEqual(
            movimentacao["codigo_documento"],
            documento["codigo"],
        )

    def test_adicao_de_documento_deve_normalizar_responsavel(
        self
    ):
        documento = self._criar_documento()

        adicionar_documento_homologacao(
            homologacao=self.homologacao_ativa,
            documento=documento,
            data_movimentacao="2026-07-30",
            responsavel="  Ana Lima  ",
        )

        movimentacao = self.homologacao_ativa[
            "movimentacoes"
        ][-1]

        self.assertEqual(
            movimentacao["responsavel"],
            "Ana Lima",
        )

        self.assertEqual(
            movimentacao["data"],
            "2026-07-30",
        )

    def test_nao_deve_adicionar_documento_com_codigo_duplicado(
        self
    ):
        primeiro_documento = self._criar_documento(
            codigo=1
        )

        segundo_documento = self._criar_documento(
            codigo=1,
            nome="Outro documento",
            categoria="Outro",
        )

        adicionar_documento_homologacao(
            homologacao=self.homologacao_ativa,
            documento=primeiro_documento,
            data_movimentacao="2026-07-30",
            responsavel="Ana Lima",
        )

        with self.assertRaises(ValueError):
            adicionar_documento_homologacao(
                homologacao=self.homologacao_ativa,
                documento=segundo_documento,
                data_movimentacao="2026-07-31",
                responsavel="Ana Lima",
            )

        self.assertEqual(
            len(self.homologacao_ativa["documentos"]),
            1,
        )

        self.assertEqual(
            len(self.homologacao_ativa["movimentacoes"]),
            2,
        )

    def test_nova_versao_deve_encontrar_documento_anterior(
        self
    ):
        segunda_versao = self._criar_documento(
            codigo=2,
            versao=2,
            codigo_documento_anterior=999,
        )

        with self.assertRaises(ValueError):
            adicionar_documento_homologacao(
                homologacao=self.homologacao_ativa,
                documento=segunda_versao,
                data_movimentacao="2026-07-30",
                responsavel="Ana Lima",
            )

        self.assertEqual(
            self.homologacao_ativa["documentos"],
            [],
        )

    def test_deve_adicionar_nova_versao_de_documento(self):
        primeira_versao = self._criar_documento(
            codigo=1,
            versao=1,
        )

        segunda_versao = self._criar_documento(
            codigo=2,
            versao=2,
            codigo_documento_anterior=1,
        )

    # Primeiro, a versão 1 é adicionada à Homologação.
    #
    # A função auxiliar _criar_documento() cria esse documento
    # inicialmente com status RECEBIDO.
        adicionar_documento_homologacao(
            homologacao=self.homologacao_ativa,
            documento=primeira_versao,
            data_movimentacao="2026-07-30",
            responsavel="Ana Lima",
        )

    # O documento RECEBIDO entra na etapa de validação.
        alterar_status_documento_homologacao(
            homologacao=self.homologacao_ativa,
            codigo_documento=1,
            novo_status=(
                StatusDocumentoHomologacao.EM_VALIDACAO
            ),
            data_movimentacao="2026-07-30",
            responsavel="Ana Lima",
        )

    # Depois da análise, o documento é validado.
    #
    # Agora ele está autorizado a receber uma nova versão.
        alterar_status_documento_homologacao(
            homologacao=self.homologacao_ativa,
            codigo_documento=1,
            novo_status=(
                StatusDocumentoHomologacao.VALIDADO
            ),
            data_movimentacao="2026-07-30",
            responsavel="Ana Lima",
        )

    # Somente depois de a versão 1 estar VALIDADA,
    # a versão 2 é adicionada.
        adicionar_documento_homologacao(
            homologacao=self.homologacao_ativa,
            documento=segunda_versao,
            data_movimentacao="2026-07-31",
            responsavel="Ana Lima",
        )

    # As duas versões devem continuar preservadas.
        self.assertEqual(
            len(self.homologacao_ativa["documentos"]),
            2,
        )

    # A versão anterior é marcada automaticamente como substituída.
        self.assertEqual(
            primeira_versao["status"],
            StatusDocumentoHomologacao.SUBSTITUIDO.value,
        )

    # A nova versão mantém o status com o qual foi criada.
        self.assertEqual(
            segunda_versao["status"],
            StatusDocumentoHomologacao.RECEBIDO.value,
        )

    def test_versao_deve_ser_sequencial(self):
        primeira_versao = self._criar_documento(
            codigo=1,
            versao=1,
        )

        terceira_versao = self._criar_documento(
            codigo=3,
            versao=3,
            codigo_documento_anterior=1,
        )

        adicionar_documento_homologacao(
            homologacao=self.homologacao_ativa,
            documento=primeira_versao,
            data_movimentacao="2026-07-30",
            responsavel="Ana Lima",
        )

        # Preparamos corretamente o documento anterior.
        alterar_status_documento_homologacao(
            homologacao=self.homologacao_ativa,
            codigo_documento=1,
            novo_status=(
                StatusDocumentoHomologacao.EM_VALIDACAO
            ),
            data_movimentacao="2026-07-30",
            responsavel="Ana Lima",
        )

        alterar_status_documento_homologacao(
            homologacao=self.homologacao_ativa,
            codigo_documento=1,
            novo_status=(
                StatusDocumentoHomologacao.VALIDADO
            ),
            data_movimentacao="2026-07-30",
            responsavel="Ana Lima",
        )

        # Agora a substituição é permitida pelo status.
        #
        # Mesmo assim, a versão 3 deve ser rejeitada porque
        # a próxima versão depois da versão 1 deveria ser a versão 2.
        with self.assertRaises(ValueError):
            adicionar_documento_homologacao(
                homologacao=self.homologacao_ativa,
                documento=terceira_versao,
                data_movimentacao="2026-07-31",
                responsavel="Ana Lima",
            )

        # Como a operação falhou, o documento anterior deve continuar
        # com seu status original, sem ser marcado como SUBSTITUIDO.
        self.assertEqual(
            primeira_versao["status"],
            StatusDocumentoHomologacao.VALIDADO.value,
        )

        # A versão inválida não pode ter sido adicionada.
        self.assertEqual(
            len(self.homologacao_ativa["documentos"]),
            1,
        )

    def test_nova_versao_deve_manter_nome_do_documento(self):
        primeira_versao = self._criar_documento(
            codigo=1,
            nome="Projeto elétrico",
            categoria="Projeto técnico",
        )

        segunda_versao = self._criar_documento(
            codigo=2,
            nome="Memorial descritivo",
            categoria="Projeto técnico",
            versao=2,
            codigo_documento_anterior=1,
        )

        adicionar_documento_homologacao(
            homologacao=self.homologacao_ativa,
            documento=primeira_versao,
            data_movimentacao="2026-07-30",
            responsavel="Ana Lima",
        )

        # A versão anterior precisa estar apta à substituição.
        alterar_status_documento_homologacao(
            homologacao=self.homologacao_ativa,
            codigo_documento=1,
            novo_status=(
                StatusDocumentoHomologacao.EM_VALIDACAO
            ),
            data_movimentacao="2026-07-30",
            responsavel="Ana Lima",
        )

        alterar_status_documento_homologacao(
            homologacao=self.homologacao_ativa,
            codigo_documento=1,
            novo_status=(
                StatusDocumentoHomologacao.VALIDADO
            ),
            data_movimentacao="2026-07-30",
            responsavel="Ana Lima",
        )

        # A tentativa deve falhar especificamente porque o nome mudou.
        with self.assertRaises(ValueError):
            adicionar_documento_homologacao(
                homologacao=self.homologacao_ativa,
                documento=segunda_versao,
                data_movimentacao="2026-07-31",
                responsavel="Ana Lima",
            )

        self.assertEqual(
            primeira_versao["status"],
            StatusDocumentoHomologacao.VALIDADO.value,
        )

        self.assertEqual(
            len(self.homologacao_ativa["documentos"]),
            1,
        )

    def test_nova_versao_deve_manter_categoria(self):
        primeira_versao = self._criar_documento(
            codigo=1,
            nome="Projeto elétrico",
            categoria="Projeto técnico",
        )

        segunda_versao = self._criar_documento(
            codigo=2,
            nome="Projeto elétrico",
            categoria="Vistoria",
            versao=2,
            codigo_documento_anterior=1,
        )

        adicionar_documento_homologacao(
            homologacao=self.homologacao_ativa,
            documento=primeira_versao,
            data_movimentacao="2026-07-30",
            responsavel="Ana Lima",
        )

        alterar_status_documento_homologacao(
            homologacao=self.homologacao_ativa,
            codigo_documento=1,
            novo_status=(
                StatusDocumentoHomologacao.EM_VALIDACAO
            ),
            data_movimentacao="2026-07-30",
            responsavel="Ana Lima",
        )

        alterar_status_documento_homologacao(
            homologacao=self.homologacao_ativa,
            codigo_documento=1,
            novo_status=(
                StatusDocumentoHomologacao.VALIDADO
            ),
            data_movimentacao="2026-07-30",
            responsavel="Ana Lima",
        )

        with self.assertRaises(ValueError):
            adicionar_documento_homologacao(
                homologacao=self.homologacao_ativa,
                documento=segunda_versao,
                data_movimentacao="2026-07-31",
                responsavel="Ana Lima",
            )

        self.assertEqual(
            primeira_versao["status"],
            StatusDocumentoHomologacao.VALIDADO.value,
        )

        self.assertEqual(
            len(self.homologacao_ativa["documentos"]),
            1,
        )

    def test_documento_anterior_nao_deve_ser_substituido_duas_vezes(
        self
    ):
        primeira_versao = self._criar_documento(
            codigo=1,
        )

        segunda_versao = self._criar_documento(
            codigo=2,
            versao=2,
            codigo_documento_anterior=1,
        )

        outra_segunda_versao = self._criar_documento(
            codigo=3,
            versao=2,
            codigo_documento_anterior=1,
        )

        # Adicionamos a versão 1.
        adicionar_documento_homologacao(
            homologacao=self.homologacao_ativa,
            documento=primeira_versao,
            data_movimentacao="2026-07-30",
            responsavel="Ana Lima",
        )

        # Preparamos a versão 1 para poder ser substituída.
        alterar_status_documento_homologacao(
            homologacao=self.homologacao_ativa,
            codigo_documento=1,
            novo_status=(
                StatusDocumentoHomologacao.EM_VALIDACAO
            ),
            data_movimentacao="2026-07-30",
            responsavel="Ana Lima",
        )

        alterar_status_documento_homologacao(
            homologacao=self.homologacao_ativa,
            codigo_documento=1,
            novo_status=(
                StatusDocumentoHomologacao.VALIDADO
            ),
            data_movimentacao="2026-07-30",
            responsavel="Ana Lima",
        )

        # A primeira versão 2 é adicionada corretamente.
        adicionar_documento_homologacao(
            homologacao=self.homologacao_ativa,
            documento=segunda_versao,
            data_movimentacao="2026-07-31",
            responsavel="Ana Lima",
        )

        # Neste momento, a versão 1 já está SUBSTITUIDA.
        self.assertEqual(
            primeira_versao["status"],
            StatusDocumentoHomologacao.SUBSTITUIDO.value,
        )

        # Outra versão não poderá usar novamente a versão 1
        # como documento anterior.
        with self.assertRaises(ValueError):
            adicionar_documento_homologacao(
                homologacao=self.homologacao_ativa,
                documento=outra_segunda_versao,
                data_movimentacao="2026-08-01",
                responsavel="Ana Lima",
            )

        # Somente a versão 1 e a primeira versão 2 devem existir.
        self.assertEqual(
            len(self.homologacao_ativa["documentos"]),
            2,
        )

        self.assertIs(
            self.homologacao_ativa["documentos"][0],
            primeira_versao,
        )

        self.assertIs(
            self.homologacao_ativa["documentos"][1],
            segunda_versao,
        )

    def test_nao_deve_adicionar_documento_em_homologacao_terminal(
        self
    ):
        homologacao = criar_dados_homologacao(
            codigo=70,
            codigo_empresa=1,
            codigo_projeto=70,
            codigo_concessionaria=2,
            data_abertura="2026-07-29",
            responsavel_abertura="Maria Santos",
        )

        homologacao["status"] = (
            StatusHomologacao.CONCLUIDA.value
        )

        documento = self._criar_documento()

        with self.assertRaises(ValueError):
            adicionar_documento_homologacao(
                homologacao=homologacao,
                documento=documento,
                data_movimentacao="2026-07-30",
                responsavel="Ana Lima",
            )

        self.assertEqual(
            homologacao["documentos"],
            [],
        )

    def test_nao_deve_adicionar_documento_incompleto(self):
        documento_incompleto = {
            "codigo": 1,
            "nome": "Documento incompleto",
        }

        with self.assertRaises(ValueError):
            adicionar_documento_homologacao(
                homologacao=self.homologacao_ativa,
                documento=documento_incompleto,
                data_movimentacao="2026-07-30",
                responsavel="Ana Lima",
            )

        self.assertEqual(
            self.homologacao_ativa["documentos"],
            [],
        )

    def test_deve_receber_documento_solicitado(self):
        documento = criar_dados_documento_homologacao(
            codigo=10,
            nome="Fatura atualizada",
            categoria="Unidade Consumidora",
            data_registro="2026-07-30",
            responsavel_registro="Ana Lima",
            origem=OrigemDocumento.CLIENTE,
            status=StatusDocumentoHomologacao.SOLICITADO,
        )

        adicionar_documento_homologacao(
            homologacao=self.homologacao_ativa,
            documento=documento,
            data_movimentacao="2026-07-30",
            responsavel="Ana Lima",
        )

        alterar_status_documento_homologacao(
            homologacao=self.homologacao_ativa,
            codigo_documento=10,
            novo_status=StatusDocumentoHomologacao.RECEBIDO,
            data_movimentacao="2026-07-31",
            responsavel="João Souza",
            referencia_arquivo="arquivos/fatura.pdf",
        )

        self.assertEqual(
            documento["status"],
            StatusDocumentoHomologacao.RECEBIDO.value,
        )

        self.assertEqual(
            documento["referencia_arquivo"],
            "arquivos/fatura.pdf",
        )

    def test_recebimento_deve_exigir_referencia_arquivo(self):
        documento = criar_dados_documento_homologacao(
            codigo=10,
            nome="Fatura atualizada",
            categoria="Unidade Consumidora",
            data_registro="2026-07-30",
            responsavel_registro="Ana Lima",
            origem=OrigemDocumento.CLIENTE,
            status=StatusDocumentoHomologacao.SOLICITADO,
        )

        adicionar_documento_homologacao(
            homologacao=self.homologacao_ativa,
            documento=documento,
            data_movimentacao="2026-07-30",
            responsavel="Ana Lima",
        )

        with self.assertRaises(ValueError):
            alterar_status_documento_homologacao(
                homologacao=self.homologacao_ativa,
                codigo_documento=10,
                novo_status=(
                    StatusDocumentoHomologacao.RECEBIDO
                ),
                data_movimentacao="2026-07-31",
                responsavel="João Souza",
            )

        self.assertEqual(
            documento["status"],
            StatusDocumentoHomologacao.SOLICITADO.value,
        )

    def test_deve_avancar_documento_para_validacao(self):
        documento = self._criar_documento(
            codigo=10
        )

        adicionar_documento_homologacao(
            homologacao=self.homologacao_ativa,
            documento=documento,
            data_movimentacao="2026-07-30",
            responsavel="Ana Lima",
        )

        alterar_status_documento_homologacao(
            homologacao=self.homologacao_ativa,
            codigo_documento=10,
            novo_status=(
                StatusDocumentoHomologacao.EM_VALIDACAO
            ),
            data_movimentacao="2026-07-31",
            responsavel="Carlos Souza",
        )

        self.assertEqual(
            documento["status"],
            StatusDocumentoHomologacao.EM_VALIDACAO.value,
        )

    def test_rejeicao_documental_deve_exigir_motivo(self):
        documento = self._criar_documento(
            codigo=10
        )

        adicionar_documento_homologacao(
            homologacao=self.homologacao_ativa,
            documento=documento,
            data_movimentacao="2026-07-30",
            responsavel="Ana Lima",
        )

        alterar_status_documento_homologacao(
            homologacao=self.homologacao_ativa,
            codigo_documento=10,
            novo_status=(
                StatusDocumentoHomologacao.EM_VALIDACAO
            ),
            data_movimentacao="2026-07-31",
            responsavel="Carlos Souza",
        )

        with self.assertRaises(ValueError):
            alterar_status_documento_homologacao(
                homologacao=self.homologacao_ativa,
                codigo_documento=10,
                novo_status=(
                    StatusDocumentoHomologacao.REJEITADO
                ),
                data_movimentacao="2026-08-01",
                responsavel="Carlos Souza",
            )

        self.assertEqual(
            documento["status"],
            StatusDocumentoHomologacao.EM_VALIDACAO.value,
        )

    def test_deve_rejeitar_documento_com_motivo(self):
        documento = self._criar_documento(
            codigo=10
        )

        adicionar_documento_homologacao(
            homologacao=self.homologacao_ativa,
            documento=documento,
            data_movimentacao="2026-07-30",
            responsavel="Ana Lima",
        )

        alterar_status_documento_homologacao(
            homologacao=self.homologacao_ativa,
            codigo_documento=10,
            novo_status=(
                StatusDocumentoHomologacao.EM_VALIDACAO
            ),
            data_movimentacao="2026-07-31",
            responsavel="Carlos Souza",
        )

        alterar_status_documento_homologacao(
            homologacao=self.homologacao_ativa,
            codigo_documento=10,
            novo_status=(
                StatusDocumentoHomologacao.REJEITADO
            ),
            data_movimentacao="2026-08-01",
            responsavel="Carlos Souza",
            motivo="Documento ilegível.",
        )

        self.assertEqual(
            documento["status"],
            StatusDocumentoHomologacao.REJEITADO.value,
        )

        movimentacao = self.homologacao_ativa[
            "movimentacoes"
        ][-1]

        self.assertEqual(
            movimentacao["motivo"],
            "Documento ilegível.",
        )

    def test_deve_validar_documento(self):
        documento = self._criar_documento(
            codigo=10
        )

        adicionar_documento_homologacao(
            homologacao=self.homologacao_ativa,
            documento=documento,
            data_movimentacao="2026-07-30",
            responsavel="Ana Lima",
        )

        alterar_status_documento_homologacao(
            homologacao=self.homologacao_ativa,
            codigo_documento=10,
            novo_status=(
                StatusDocumentoHomologacao.EM_VALIDACAO
            ),
            data_movimentacao="2026-07-31",
            responsavel="Carlos Souza",
        )

        alterar_status_documento_homologacao(
            homologacao=self.homologacao_ativa,
            codigo_documento=10,
            novo_status=(
                StatusDocumentoHomologacao.VALIDADO
            ),
            data_movimentacao="2026-08-01",
            responsavel="Carlos Souza",
        )

        self.assertEqual(
            documento["status"],
            StatusDocumentoHomologacao.VALIDADO.value,
        )

    def test_transicao_documental_deve_registrar_movimentacao(
        self
    ):
        documento = self._criar_documento(
            codigo=10
        )

        adicionar_documento_homologacao(
            homologacao=self.homologacao_ativa,
            documento=documento,
            data_movimentacao="2026-07-30",
            responsavel="Ana Lima",
        )

        alterar_status_documento_homologacao(
            homologacao=self.homologacao_ativa,
            codigo_documento=10,
            novo_status=(
                StatusDocumentoHomologacao.EM_VALIDACAO
            ),
            data_movimentacao="2026-07-31",
            responsavel="Carlos Souza",
        )

        movimentacao = self.homologacao_ativa[
            "movimentacoes"
        ][-1]

        self.assertEqual(
            movimentacao["tipo_evento"],
            "STATUS_DOCUMENTO_ALTERADO",
        )

        self.assertEqual(
            movimentacao["codigo_documento"],
            10,
        )

        self.assertEqual(
            movimentacao["status_anterior"],
            StatusDocumentoHomologacao.RECEBIDO.value,
        )

        self.assertEqual(
            movimentacao["novo_status"],
            StatusDocumentoHomologacao.EM_VALIDACAO.value,
        )

    def test_nao_deve_alterar_documento_inexistente(self):
        with self.assertRaises(ValueError):
            alterar_status_documento_homologacao(
                homologacao=self.homologacao_ativa,
                codigo_documento=999,
                novo_status=(
                    StatusDocumentoHomologacao.RECEBIDO
                ),
                data_movimentacao="2026-07-31",
                responsavel="Carlos Souza",
                referencia_arquivo="arquivo.pdf",
            )

    def test_nao_deve_permitir_transicao_documental_invalida(
        self
    ):
        documento = criar_dados_documento_homologacao(
            codigo=10,
            nome="Fatura atualizada",
            categoria="Unidade Consumidora",
            data_registro="2026-07-30",
            responsavel_registro="Ana Lima",
            origem=OrigemDocumento.CLIENTE,
            status=StatusDocumentoHomologacao.SOLICITADO,
        )

        adicionar_documento_homologacao(
            homologacao=self.homologacao_ativa,
            documento=documento,
            data_movimentacao="2026-07-30",
            responsavel="Ana Lima",
        )

        with self.assertRaises(ValueError):
            alterar_status_documento_homologacao(
                homologacao=self.homologacao_ativa,
                codigo_documento=10,
                novo_status=(
                    StatusDocumentoHomologacao.VALIDADO
                ),
                data_movimentacao="2026-07-31",
                responsavel="Carlos Souza",
            )

        self.assertEqual(
            documento["status"],
            StatusDocumentoHomologacao.SOLICITADO.value,
        )

    def test_nao_deve_substituir_documento_ainda_recebido(self):
        primeira_versao = self._criar_documento(
            codigo=1,
        )

        segunda_versao = self._criar_documento(
            codigo=2,
            versao=2,
            codigo_documento_anterior=1,
        )

        adicionar_documento_homologacao(
            homologacao=self.homologacao_ativa,
            documento=primeira_versao,
            data_movimentacao="2026-07-30",
            responsavel="Ana Lima",
        )

        with self.assertRaises(ValueError):
            adicionar_documento_homologacao(
                homologacao=self.homologacao_ativa,
                documento=segunda_versao,
                data_movimentacao="2026-07-31",
                responsavel="Ana Lima",
            )

        self.assertEqual(
            primeira_versao["status"],
            StatusDocumentoHomologacao.RECEBIDO.value,
        )

        self.assertEqual(
            len(self.homologacao_ativa["documentos"]),
            1,
        )

    def test_deve_buscar_submissao_por_codigo(self):
        submissao = self._criar_submissao_inicial()

        resultado = buscar_submissao_por_codigo(
            submissoes=[submissao],
            codigo=1,
        )

        self.assertIs(resultado, submissao)

    def test_busca_submissao_codigo_inexistente_retorna_none(
        self
    ):
        resultado = buscar_submissao_por_codigo(
            submissoes=[],
            codigo=99,
        )

        self.assertIsNone(resultado)

    def test_deve_buscar_submissao_por_numero_sequencial(
        self
    ):
        submissao = self._criar_submissao_inicial()

        resultado = buscar_submissao_por_numero_sequencial(
            submissoes=[submissao],
            numero_sequencial=1,
        )

        self.assertIs(resultado, submissao)

    def test_deve_adicionar_submissao_inicial(self):
        documento = self._criar_documento()

        adicionar_documento_homologacao(
            homologacao=self.homologacao_ativa,
            documento=documento,
            data_movimentacao="2026-07-30",
            responsavel="Ana Lima",
        )

        submissao = self._criar_submissao_inicial()

        resultado = adicionar_submissao_homologacao(
            homologacao=self.homologacao_ativa,
            submissao=submissao,
            data_movimentacao="2026-07-30",
            responsavel="Ana Lima",
        )

        self.assertIs(
            resultado,
            self.homologacao_ativa,
        )

        self.assertEqual(
            len(resultado["submissoes"]),
            1,
        )

        self.assertIs(
            resultado["submissoes"][0],
            submissao,
        )

    def test_adicao_submissao_deve_registrar_movimentacao(
        self
    ):
        documento = self._criar_documento()

        adicionar_documento_homologacao(
            homologacao=self.homologacao_ativa,
            documento=documento,
            data_movimentacao="2026-07-30",
            responsavel="Ana Lima",
        )

        submissao = self._criar_submissao_inicial()

        adicionar_submissao_homologacao(
            homologacao=self.homologacao_ativa,
            submissao=submissao,
            data_movimentacao="2026-07-30",
            responsavel="Ana Lima",
        )

        movimentacao = self.homologacao_ativa[
            "movimentacoes"
        ][-1]

        self.assertEqual(
            movimentacao["tipo_evento"],
            "SUBMISSAO_ADICIONADA",
        )

        self.assertEqual(
            movimentacao["codigo_submissao"],
            1,
        )

        self.assertEqual(
            movimentacao["numero_sequencial_submissao"],
            1,
        )

        self.assertEqual(
            movimentacao["tipo_submissao"],
            "INICIAL",
        )

    def test_primeira_submissao_deve_ser_inicial(self):
        submissao = criar_dados_submissao(
            codigo=2,
            numero_sequencial=1,
            tipo="REENVIO",
            data_criacao="2026-07-30",
            responsavel_criacao="Ana Lima",
            codigo_submissao_origem=1,
            codigo_resposta_origem=1,
        )

        with self.assertRaisesRegex(
            ValueError,
            "A primeira Submissão da Homologação "
            "deve ser do tipo INICIAL",
        ):
            adicionar_submissao_homologacao(
                homologacao=self.homologacao_ativa,
                submissao=submissao,
                data_movimentacao="2026-07-30",
                responsavel="Ana Lima",
            )

        self.assertEqual(
            self.homologacao_ativa["submissoes"],
            [],
        )

    def test_primeira_submissao_deve_possuir_sequencia_um(
        self
    ):
        submissao = self._criar_submissao_inicial(
            numero_sequencial=2,
        )

        with self.assertRaises(ValueError):
            adicionar_submissao_homologacao(
                homologacao=self.homologacao_ativa,
                submissao=submissao,
                data_movimentacao="2026-07-30",
                responsavel="Ana Lima",
            )

        self.assertEqual(
            self.homologacao_ativa["submissoes"],
            [],
        )

    def test_documento_inexistente_deve_impedir_submissao(
        self
    ):
        submissao = self._criar_submissao_inicial(
            codigo_documento=99,
        )

        with self.assertRaises(ValueError):
            adicionar_submissao_homologacao(
                homologacao=self.homologacao_ativa,
                submissao=submissao,
                data_movimentacao="2026-07-30",
                responsavel="Ana Lima",
            )

        self.assertEqual(
            self.homologacao_ativa["submissoes"],
            [],
        )

    def test_versao_documental_incorreta_deve_ser_rejeitada(
        self
    ):
        documento = self._criar_documento(
            codigo=1,
            versao=1,
        )

        adicionar_documento_homologacao(
            homologacao=self.homologacao_ativa,
            documento=documento,
            data_movimentacao="2026-07-30",
            responsavel="Ana Lima",
        )

        submissao = self._criar_submissao_inicial(
            numero_versao=2,
        )

        with self.assertRaises(ValueError):
            adicionar_submissao_homologacao(
                homologacao=self.homologacao_ativa,
                submissao=submissao,
                data_movimentacao="2026-07-30",
                responsavel="Ana Lima",
            )

        self.assertEqual(
            self.homologacao_ativa["submissoes"],
            [],
        )

    def test_codigo_submissao_duplicado_deve_ser_rejeitado(
        self
    ):
        documento = self._criar_documento()

        adicionar_documento_homologacao(
            homologacao=self.homologacao_ativa,
            documento=documento,
            data_movimentacao="2026-07-30",
            responsavel="Ana Lima",
        )

        submissao = self._criar_submissao_inicial()

        adicionar_submissao_homologacao(
            homologacao=self.homologacao_ativa,
            submissao=submissao,
            data_movimentacao="2026-07-30",
            responsavel="Ana Lima",
        )

        outra_submissao = criar_dados_submissao(
            codigo=1,
            numero_sequencial=2,
            tipo="INICIAL",
            data_criacao="2026-07-31",
            responsavel_criacao="Ana Lima",
        )

        with self.assertRaises(ValueError):
            adicionar_submissao_homologacao(
                homologacao=self.homologacao_ativa,
                submissao=outra_submissao,
                data_movimentacao="2026-07-31",
                responsavel="Ana Lima",
            )

        self.assertEqual(
            len(self.homologacao_ativa["submissoes"]),
            1,
        )

    def test_segunda_submissao_inicial_deve_ser_rejeitada(
        self
    ):
        documento = self._criar_documento()

        adicionar_documento_homologacao(
            homologacao=self.homologacao_ativa,
            documento=documento,
            data_movimentacao="2026-07-30",
            responsavel="Ana Lima",
        )

        primeira = self._criar_submissao_inicial()

        adicionar_submissao_homologacao(
            homologacao=self.homologacao_ativa,
            submissao=primeira,
            data_movimentacao="2026-07-30",
            responsavel="Ana Lima",
        )

        segunda = self._criar_submissao_inicial(
            codigo=2,
            numero_sequencial=2,
        )

        with self.assertRaises(ValueError):
            adicionar_submissao_homologacao(
                homologacao=self.homologacao_ativa,
                submissao=segunda,
                data_movimentacao="2026-07-31",
                responsavel="Ana Lima",
            )

        self.assertEqual(
            len(self.homologacao_ativa["submissoes"]),
            1,
        )

    def test_submissao_origem_inexistente_deve_ser_rejeitada(
        self
    ):
        documento = self._criar_documento()

        adicionar_documento_homologacao(
            homologacao=self.homologacao_ativa,
            documento=documento,
            data_movimentacao="2026-07-30",
            responsavel="Ana Lima",
        )

        primeira = self._criar_submissao_inicial()

        adicionar_submissao_homologacao(
            homologacao=self.homologacao_ativa,
            submissao=primeira,
            data_movimentacao="2026-07-30",
            responsavel="Ana Lima",
        )

        reenvio = criar_dados_submissao(
            codigo=2,
            numero_sequencial=2,
            tipo="REENVIO",
            data_criacao="2026-07-31",
            responsavel_criacao="Ana Lima",
            codigo_submissao_origem=99,
            codigo_resposta_origem=1,
        )

        with self.assertRaisesRegex(
            ValueError,
            "Submissão de origem não encontrada",
        ):
            adicionar_submissao_homologacao(
                homologacao=self.homologacao_ativa,
                submissao=reenvio,
                data_movimentacao="2026-07-31",
                responsavel="Ana Lima",
            )

        self.assertEqual(
            len(self.homologacao_ativa["submissoes"]),
            1,
        )

    def test_homologacao_terminal_nao_recebe_submissao(self):
        documento = self._criar_documento()

        adicionar_documento_homologacao(
            homologacao=self.homologacao_ativa,
            documento=documento,
            data_movimentacao="2026-07-30",
            responsavel="Ana Lima",
        )

        self.homologacao_ativa["status"] = (
            StatusHomologacao.CANCELADA.value
        )

        submissao = self._criar_submissao_inicial()

        quantidade_movimentacoes = len(
            self.homologacao_ativa["movimentacoes"]
        )

        with self.assertRaises(ValueError):
            adicionar_submissao_homologacao(
                homologacao=self.homologacao_ativa,
                submissao=submissao,
                data_movimentacao="2026-07-30",
                responsavel="Ana Lima",
            )

        self.assertEqual(
            self.homologacao_ativa["submissoes"],
            [],
        )

        self.assertEqual(
            len(self.homologacao_ativa["movimentacoes"]),
            quantidade_movimentacoes,
        )

    def test_deve_marcar_submissao_como_pronta_para_envio(
        self
    ):
        submissao = (
            self._adicionar_submissao_inicial_valida()
        )

        resultado = alterar_status_operacional_submissao(
            homologacao=self.homologacao_ativa,
            codigo_submissao=submissao["codigo"],
            novo_status=(
                StatusOperacionalSubmissao
                .PRONTA_PARA_ENVIO
            ),
            data_movimentacao="2026-07-31",
            responsavel="Carlos Souza",
        )

        self.assertIs(
            resultado,
            self.homologacao_ativa,
        )

        self.assertEqual(
            submissao["status_operacional"],
            "PRONTA_PARA_ENVIO",
        )

        self.assertEqual(
            self.homologacao_ativa["responsavel_atual"],
            "Carlos Souza",
        )

    def test_status_operacional_deve_aceitar_texto(self):
        submissao = (
            self._adicionar_submissao_inicial_valida()
        )

        alterar_status_operacional_submissao(
            homologacao=self.homologacao_ativa,
            codigo_submissao=submissao["codigo"],
            novo_status="PRONTA_PARA_ENVIO",
            data_movimentacao="2026-07-31",
            responsavel="Carlos Souza",
        )

        self.assertEqual(
            submissao["status_operacional"],
            "PRONTA_PARA_ENVIO",
        )

    def test_alteracao_operacional_deve_registrar_movimentacao(
        self
    ):
        submissao = (
            self._adicionar_submissao_inicial_valida()
        )

        alterar_status_operacional_submissao(
            homologacao=self.homologacao_ativa,
            codigo_submissao=submissao["codigo"],
            novo_status="PRONTA_PARA_ENVIO",
            data_movimentacao="2026-07-31",
            responsavel="Carlos Souza",
        )

        movimentacao = self.homologacao_ativa[
            "movimentacoes"
        ][-1]

        self.assertEqual(
            movimentacao["tipo_evento"],
            "STATUS_OPERACIONAL_SUBMISSAO_ALTERADO",
        )

        self.assertEqual(
            movimentacao["codigo_submissao"],
            submissao["codigo"],
        )

        self.assertEqual(
            movimentacao["status_anterior"],
            "EM_PREPARACAO",
        )

        self.assertEqual(
            movimentacao["novo_status"],
            "PRONTA_PARA_ENVIO",
        )

    def test_deve_retornar_submissao_para_preparacao(self):
        submissao = (
            self._adicionar_submissao_inicial_valida()
        )

        alterar_status_operacional_submissao(
            homologacao=self.homologacao_ativa,
            codigo_submissao=submissao["codigo"],
            novo_status="PRONTA_PARA_ENVIO",
            data_movimentacao="2026-07-31",
            responsavel="Carlos Souza",
        )

        alterar_status_operacional_submissao(
            homologacao=self.homologacao_ativa,
            codigo_submissao=submissao["codigo"],
            novo_status="EM_PREPARACAO",
            data_movimentacao="2026-08-01",
            responsavel="Ana Lima",
            motivo="Pacote será revisado novamente.",
        )

        self.assertEqual(
            submissao["status_operacional"],
            "EM_PREPARACAO",
        )

    def test_deve_cancelar_submissao_em_preparacao(self):
        submissao = (
            self._adicionar_submissao_inicial_valida()
        )

        alterar_status_operacional_submissao(
            homologacao=self.homologacao_ativa,
            codigo_submissao=submissao["codigo"],
            novo_status="CANCELADA",
            data_movimentacao="2026-07-31",
            responsavel="Carlos Souza",
            motivo="Pacote criado em duplicidade.",
        )

        self.assertEqual(
            submissao["status_operacional"],
            "CANCELADA",
        )

        movimentacao = self.homologacao_ativa[
            "movimentacoes"
        ][-1]

        self.assertEqual(
            movimentacao["motivo"],
            "Pacote criado em duplicidade.",
        )

    def test_cancelamento_submissao_deve_exigir_motivo(
        self
    ):
        submissao = (
            self._adicionar_submissao_inicial_valida()
        )

        quantidade_movimentacoes = len(
            self.homologacao_ativa["movimentacoes"]
        )

        with self.assertRaises(ValueError):
            alterar_status_operacional_submissao(
                homologacao=self.homologacao_ativa,
                codigo_submissao=submissao["codigo"],
                novo_status="CANCELADA",
                data_movimentacao="2026-07-31",
                responsavel="Carlos Souza",
            )

        self.assertEqual(
            submissao["status_operacional"],
            "EM_PREPARACAO",
        )

        self.assertEqual(
            len(self.homologacao_ativa["movimentacoes"]),
            quantidade_movimentacoes,
        )

    def test_nao_deve_alterar_para_o_mesmo_status_operacional(
        self
    ):
        submissao = (
            self._adicionar_submissao_inicial_valida()
        )

        with self.assertRaises(ValueError):
            alterar_status_operacional_submissao(
                homologacao=self.homologacao_ativa,
                codigo_submissao=submissao["codigo"],
                novo_status="EM_PREPARACAO",
                data_movimentacao="2026-07-31",
                responsavel="Carlos Souza",
            )

        self.assertEqual(
            submissao["status_operacional"],
            "EM_PREPARACAO",
        )

    def test_transicao_operacional_invalida_deve_ser_rejeitada(
        self
    ):
        submissao = (
            self._adicionar_submissao_inicial_valida()
        )

        with self.assertRaises(ValueError):
            alterar_status_operacional_submissao(
                homologacao=self.homologacao_ativa,
                codigo_submissao=submissao["codigo"],
                novo_status="PROTOCOLADA",
                data_movimentacao="2026-07-31",
                responsavel="Carlos Souza",
            )

        self.assertEqual(
            submissao["status_operacional"],
            "EM_PREPARACAO",
        )

    def test_envio_deve_exigir_operacao_especifica(self):
        submissao = (
            self._adicionar_submissao_inicial_valida()
        )

        alterar_status_operacional_submissao(
            homologacao=self.homologacao_ativa,
            codigo_submissao=submissao["codigo"],
            novo_status="PRONTA_PARA_ENVIO",
            data_movimentacao="2026-07-31",
            responsavel="Carlos Souza",
        )

        quantidade_movimentacoes = len(
            self.homologacao_ativa["movimentacoes"]
        )

        with self.assertRaises(ValueError):
            alterar_status_operacional_submissao(
                homologacao=self.homologacao_ativa,
                codigo_submissao=submissao["codigo"],
                novo_status="ENVIADA",
                data_movimentacao="2026-08-01",
                responsavel="Carlos Souza",
            )

        self.assertEqual(
            submissao["status_operacional"],
            "PRONTA_PARA_ENVIO",
        )

        self.assertEqual(
            len(self.homologacao_ativa["movimentacoes"]),
            quantidade_movimentacoes,
        )

    def test_submissao_cancelada_nao_deve_ser_reaberta(self):
        submissao = (
            self._adicionar_submissao_inicial_valida()
        )

        alterar_status_operacional_submissao(
            homologacao=self.homologacao_ativa,
            codigo_submissao=submissao["codigo"],
            novo_status="CANCELADA",
            data_movimentacao="2026-07-31",
            responsavel="Carlos Souza",
            motivo="Pacote criado em duplicidade.",
        )

        with self.assertRaises(ValueError):
            alterar_status_operacional_submissao(
                homologacao=self.homologacao_ativa,
                codigo_submissao=submissao["codigo"],
                novo_status="EM_PREPARACAO",
                data_movimentacao="2026-08-01",
                responsavel="Ana Lima",
            )

        self.assertEqual(
            submissao["status_operacional"],
            "CANCELADA",
        )

    def test_submissao_inexistente_nao_deve_ser_alterada(
        self
    ):
        with self.assertRaises(ValueError):
            alterar_status_operacional_submissao(
                homologacao=self.homologacao_ativa,
                codigo_submissao=999,
                novo_status="PRONTA_PARA_ENVIO",
                data_movimentacao="2026-07-31",
                responsavel="Carlos Souza",
            )

    def test_homologacao_terminal_nao_altera_status_submissao(
        self
    ):
        submissao = (
            self._adicionar_submissao_inicial_valida()
        )

        self.homologacao_ativa["status"] = (
            StatusHomologacao.CANCELADA.value
        )

        quantidade_movimentacoes = len(
            self.homologacao_ativa["movimentacoes"]
        )

        with self.assertRaises(ValueError):
            alterar_status_operacional_submissao(
                homologacao=self.homologacao_ativa,
                codigo_submissao=submissao["codigo"],
                novo_status="PRONTA_PARA_ENVIO",
                data_movimentacao="2026-07-31",
                responsavel="Carlos Souza",
            )

        self.assertEqual(
            submissao["status_operacional"],
            "EM_PREPARACAO",
        )

        self.assertEqual(
            len(self.homologacao_ativa["movimentacoes"]),
            quantidade_movimentacoes,
        )

    def test_alteracao_operacional_deve_normalizar_textos(
        self
    ):
        submissao = (
            self._adicionar_submissao_inicial_valida()
        )

        alterar_status_operacional_submissao(
            homologacao=self.homologacao_ativa,
            codigo_submissao=submissao["codigo"],
            novo_status="CANCELADA",
            data_movimentacao="2026-07-31",
            responsavel="  Carlos Souza  ",
            motivo="  Pacote criado em duplicidade.  ",
        )

        movimentacao = self.homologacao_ativa[
            "movimentacoes"
        ][-1]

        self.assertEqual(
            movimentacao["responsavel"],
            "Carlos Souza",
        )

        self.assertEqual(
            movimentacao["motivo"],
            "Pacote criado em duplicidade.",
        )

    def test_deve_enviar_submissao_pronta(self):
        submissao = (
            self._preparar_submissao_para_envio()
        )

        resultado = enviar_submissao_homologacao(
            homologacao=self.homologacao_ativa,
            codigo_submissao=submissao["codigo"],
            canal_envio="PORTAL",
            data_envio="2026-08-01",
            responsavel_envio="Carlos Souza",
        )

        self.assertIs(
            resultado,
            self.homologacao_ativa,
        )

        self.assertEqual(
            submissao["status_operacional"],
            "ENVIADA",
        )

        self.assertEqual(
            submissao["canal_envio"],
            "PORTAL",
        )

        self.assertEqual(
            submissao["data_envio"],
            "2026-08-01",
        )

        self.assertEqual(
            submissao["responsavel_envio"],
            "Carlos Souza",
        )

    def test_envio_deve_aceitar_canal_como_enum(self):
        submissao = (
            self._preparar_submissao_para_envio()
        )

        enviar_submissao_homologacao(
            homologacao=self.homologacao_ativa,
            codigo_submissao=submissao["codigo"],
            canal_envio=CanalEnvioSubmissao.EMAIL,
            data_envio="2026-08-01",
            responsavel_envio="Carlos Souza",
        )

        self.assertEqual(
            submissao["canal_envio"],
            "EMAIL",
        )

    def test_envio_deve_normalizar_responsavel(self):
        submissao = (
            self._preparar_submissao_para_envio()
        )

        enviar_submissao_homologacao(
            homologacao=self.homologacao_ativa,
            codigo_submissao=submissao["codigo"],
            canal_envio="PORTAL",
            data_envio="2026-08-01",
            responsavel_envio="  Carlos Souza  ",
        )

        self.assertEqual(
            submissao["responsavel_envio"],
            "Carlos Souza",
        )

        self.assertEqual(
            self.homologacao_ativa["responsavel_atual"],
            "Carlos Souza",
        )

    def test_envio_deve_registrar_movimentacao(self):
        submissao = (
            self._preparar_submissao_para_envio()
        )

        enviar_submissao_homologacao(
            homologacao=self.homologacao_ativa,
            codigo_submissao=submissao["codigo"],
            canal_envio="PORTAL",
            data_envio="2026-08-01",
            responsavel_envio="Carlos Souza",
        )

        movimentacao = self.homologacao_ativa[
            "movimentacoes"
        ][-1]

        self.assertEqual(
            movimentacao["tipo_evento"],
            "SUBMISSAO_ENVIADA",
        )

        self.assertEqual(
            movimentacao["status_anterior"],
            "PRONTA_PARA_ENVIO",
        )

        self.assertEqual(
            movimentacao["novo_status"],
            "ENVIADA",
        )

        self.assertEqual(
            movimentacao["canal_envio"],
            "PORTAL",
        )

        self.assertEqual(
            movimentacao["codigo_submissao"],
            submissao["codigo"],
        )

    def test_submissao_em_preparacao_nao_pode_ser_enviada(
        self
    ):
        submissao = (
            self._adicionar_submissao_inicial_valida()
        )

        quantidade_movimentacoes = len(
            self.homologacao_ativa["movimentacoes"]
        )

        with self.assertRaises(ValueError):
            enviar_submissao_homologacao(
                homologacao=self.homologacao_ativa,
                codigo_submissao=submissao["codigo"],
                canal_envio="PORTAL",
                data_envio="2026-08-01",
                responsavel_envio="Carlos Souza",
            )

        self.assertEqual(
            submissao["status_operacional"],
            "EM_PREPARACAO",
        )

        self.assertIsNone(
            submissao["canal_envio"]
        )

        self.assertEqual(
            len(self.homologacao_ativa["movimentacoes"]),
            quantidade_movimentacoes,
        )

    def test_canal_de_envio_invalido_deve_ser_rejeitado(
        self
    ):
        submissao = (
            self._preparar_submissao_para_envio()
        )

        quantidade_movimentacoes = len(
            self.homologacao_ativa["movimentacoes"]
        )

        with self.assertRaises(ValueError):
            enviar_submissao_homologacao(
                homologacao=self.homologacao_ativa,
                codigo_submissao=submissao["codigo"],
                canal_envio="WHATSAPP",
                data_envio="2026-08-01",
                responsavel_envio="Carlos Souza",
            )

        self.assertEqual(
            submissao["status_operacional"],
            "PRONTA_PARA_ENVIO",
        )

        self.assertIsNone(
            submissao["canal_envio"]
        )

        self.assertEqual(
            len(self.homologacao_ativa["movimentacoes"]),
            quantidade_movimentacoes,
        )

    def test_data_de_envio_invalida_deve_ser_rejeitada(
        self
    ):
        submissao = (
            self._preparar_submissao_para_envio()
        )

        with self.assertRaises(ValueError):
            enviar_submissao_homologacao(
                homologacao=self.homologacao_ativa,
                codigo_submissao=submissao["codigo"],
                canal_envio="PORTAL",
                data_envio="01/08/2026",
                responsavel_envio="Carlos Souza",
            )

        self.assertEqual(
            submissao["status_operacional"],
            "PRONTA_PARA_ENVIO",
        )

        self.assertIsNone(
            submissao["data_envio"]
        )

    def test_responsavel_envio_vazio_deve_ser_rejeitado(
        self
    ):
        submissao = (
            self._preparar_submissao_para_envio()
        )

        with self.assertRaises(ValueError):
            enviar_submissao_homologacao(
                homologacao=self.homologacao_ativa,
                codigo_submissao=submissao["codigo"],
                canal_envio="PORTAL",
                data_envio="2026-08-01",
                responsavel_envio="   ",
            )

        self.assertEqual(
            submissao["status_operacional"],
            "PRONTA_PARA_ENVIO",
        )

        self.assertIsNone(
            submissao["responsavel_envio"]
        )

    def test_submissao_inexistente_nao_pode_ser_enviada(
        self
    ):
        with self.assertRaises(ValueError):
            enviar_submissao_homologacao(
                homologacao=self.homologacao_ativa,
                codigo_submissao=999,
                canal_envio="PORTAL",
                data_envio="2026-08-01",
                responsavel_envio="Carlos Souza",
            )

    def test_homologacao_terminal_nao_pode_enviar_submissao(
        self
    ):
        submissao = (
            self._preparar_submissao_para_envio()
        )

        self.homologacao_ativa["status"] = (
            StatusHomologacao.CANCELADA.value
        )

        quantidade_movimentacoes = len(
            self.homologacao_ativa["movimentacoes"]
        )

        with self.assertRaises(ValueError):
            enviar_submissao_homologacao(
                homologacao=self.homologacao_ativa,
                codigo_submissao=submissao["codigo"],
                canal_envio="PORTAL",
                data_envio="2026-08-01",
                responsavel_envio="Carlos Souza",
            )

        self.assertEqual(
            submissao["status_operacional"],
            "PRONTA_PARA_ENVIO",
        )

        self.assertIsNone(
            submissao["canal_envio"]
        )

        self.assertEqual(
            len(self.homologacao_ativa["movimentacoes"]),
            quantidade_movimentacoes,
        )

    def test_submissao_enviada_nao_pode_ser_enviada_novamente(
        self
    ):
        submissao = (
            self._preparar_submissao_para_envio()
        )

        enviar_submissao_homologacao(
            homologacao=self.homologacao_ativa,
            codigo_submissao=submissao["codigo"],
            canal_envio="PORTAL",
            data_envio="2026-08-01",
            responsavel_envio="Carlos Souza",
        )

        quantidade_movimentacoes = len(
            self.homologacao_ativa["movimentacoes"]
        )

        with self.assertRaises(ValueError):
            enviar_submissao_homologacao(
                homologacao=self.homologacao_ativa,
                codigo_submissao=submissao["codigo"],
                canal_envio="EMAIL",
                data_envio="2026-08-02",
                responsavel_envio="Ana Lima",
            )

        self.assertEqual(
            submissao["canal_envio"],
            "PORTAL",
        )

        self.assertEqual(
            submissao["data_envio"],
            "2026-08-01",
        )

        self.assertEqual(
            len(self.homologacao_ativa["movimentacoes"]),
            quantidade_movimentacoes,
        )

    def test_pacote_vazio_nao_pode_ser_enviado(self):
        submissao = (
            self._preparar_submissao_para_envio()
        )

        submissao["pacote_documental"] = []

        quantidade_movimentacoes = len(
            self.homologacao_ativa["movimentacoes"]
        )

        with self.assertRaises(ValueError):
            enviar_submissao_homologacao(
                homologacao=self.homologacao_ativa,
                codigo_submissao=submissao["codigo"],
                canal_envio="PORTAL",
                data_envio="2026-08-01",
                responsavel_envio="Carlos Souza",
            )

        self.assertEqual(
            submissao["status_operacional"],
            "PRONTA_PARA_ENVIO",
        )

        self.assertIsNone(
            submissao["canal_envio"]
        )

        self.assertEqual(
            len(self.homologacao_ativa["movimentacoes"]),
            quantidade_movimentacoes,
        )

    def test_deve_protocolar_submissao_enviada(self):
        submissao = (
            self._enviar_submissao_valida()
        )

        resultado = protocolar_submissao_homologacao(
            homologacao=self.homologacao_ativa,
            codigo_submissao=submissao["codigo"],
            protocolo="PROT-2026-001",
            data_protocolo="2026-08-02",
            responsavel="Ana Lima",
        )

        self.assertIs(
            resultado,
            self.homologacao_ativa,
        )

        self.assertEqual(
            submissao["status_operacional"],
            "PROTOCOLADA",
        )

        self.assertEqual(
            submissao["protocolo"],
            "PROT-2026-001",
        )

        self.assertEqual(
            submissao["data_protocolo"],
            "2026-08-02",
        )

        self.assertEqual(
            self.homologacao_ativa["responsavel_atual"],
            "Ana Lima",
        )

    def test_protocolacao_deve_normalizar_textos(self):
        submissao = (
            self._enviar_submissao_valida()
        )

        protocolar_submissao_homologacao(
            homologacao=self.homologacao_ativa,
            codigo_submissao=submissao["codigo"],
            protocolo="  PROT-2026-001  ",
            data_protocolo="2026-08-02",
            responsavel="  Ana Lima  ",
        )

        self.assertEqual(
            submissao["protocolo"],
            "PROT-2026-001",
        )

        self.assertEqual(
            self.homologacao_ativa["responsavel_atual"],
            "Ana Lima",
        )

    def test_protocolacao_deve_registrar_movimentacao(self):
        submissao = (
            self._enviar_submissao_valida()
        )

        protocolar_submissao_homologacao(
            homologacao=self.homologacao_ativa,
            codigo_submissao=submissao["codigo"],
            protocolo="PROT-2026-001",
            data_protocolo="2026-08-02",
            responsavel="Ana Lima",
        )

        movimentacao = self.homologacao_ativa[
            "movimentacoes"
        ][-1]

        self.assertEqual(
            movimentacao["tipo_evento"],
            "SUBMISSAO_PROTOCOLADA",
        )

        self.assertEqual(
            movimentacao["status_anterior"],
            "ENVIADA",
        )

        self.assertEqual(
            movimentacao["novo_status"],
            "PROTOCOLADA",
        )

        self.assertEqual(
            movimentacao["protocolo"],
            "PROT-2026-001",
        )

        self.assertEqual(
            movimentacao["codigo_submissao"],
            submissao["codigo"],
        )

    def test_submissao_nao_enviada_nao_pode_ser_protocolada(
        self
    ):
        submissao = (
            self._preparar_submissao_para_envio()
        )

        quantidade_movimentacoes = len(
            self.homologacao_ativa["movimentacoes"]
        )

        with self.assertRaises(ValueError):
            protocolar_submissao_homologacao(
                homologacao=self.homologacao_ativa,
                codigo_submissao=submissao["codigo"],
                protocolo="PROT-2026-001",
                data_protocolo="2026-08-02",
                responsavel="Ana Lima",
            )

        self.assertEqual(
            submissao["status_operacional"],
            "PRONTA_PARA_ENVIO",
        )

        self.assertIsNone(
            submissao["protocolo"]
        )

        self.assertEqual(
            len(self.homologacao_ativa["movimentacoes"]),
            quantidade_movimentacoes,
        )

    def test_protocolo_vazio_deve_ser_rejeitado(self):
        submissao = (
            self._enviar_submissao_valida()
        )

        quantidade_movimentacoes = len(
            self.homologacao_ativa["movimentacoes"]
        )

        with self.assertRaises(ValueError):
            protocolar_submissao_homologacao(
                homologacao=self.homologacao_ativa,
                codigo_submissao=submissao["codigo"],
                protocolo="   ",
                data_protocolo="2026-08-02",
                responsavel="Ana Lima",
            )

        self.assertEqual(
            submissao["status_operacional"],
            "ENVIADA",
        )

        self.assertIsNone(
            submissao["protocolo"]
        )

        self.assertEqual(
            len(self.homologacao_ativa["movimentacoes"]),
            quantidade_movimentacoes,
        )

    def test_data_protocolo_invalida_deve_ser_rejeitada(
        self
    ):
        submissao = (
            self._enviar_submissao_valida()
        )

        with self.assertRaises(ValueError):
            protocolar_submissao_homologacao(
                homologacao=self.homologacao_ativa,
                codigo_submissao=submissao["codigo"],
                protocolo="PROT-2026-001",
                data_protocolo="02/08/2026",
                responsavel="Ana Lima",
            )

        self.assertEqual(
            submissao["status_operacional"],
            "ENVIADA",
        )

        self.assertIsNone(
            submissao["data_protocolo"]
        )

    def test_data_protocolo_anterior_ao_envio_deve_ser_rejeitada(
        self
    ):
        submissao = (
            self._enviar_submissao_valida()
        )

        quantidade_movimentacoes = len(
            self.homologacao_ativa["movimentacoes"]
        )

        with self.assertRaises(ValueError):
            protocolar_submissao_homologacao(
                homologacao=self.homologacao_ativa,
                codigo_submissao=submissao["codigo"],
                protocolo="PROT-2026-001",
                data_protocolo="2026-07-31",
                responsavel="Ana Lima",
            )

        self.assertEqual(
            submissao["status_operacional"],
            "ENVIADA",
        )

        self.assertIsNone(
            submissao["protocolo"]
        )

        self.assertIsNone(
            submissao["data_protocolo"]
        )

        self.assertEqual(
            len(self.homologacao_ativa["movimentacoes"]),
            quantidade_movimentacoes,
        )

    def test_responsavel_protocolacao_vazio_deve_ser_rejeitado(
        self
    ):
        submissao = (
            self._enviar_submissao_valida()
        )

        with self.assertRaises(ValueError):
            protocolar_submissao_homologacao(
                homologacao=self.homologacao_ativa,
                codigo_submissao=submissao["codigo"],
                protocolo="PROT-2026-001",
                data_protocolo="2026-08-02",
                responsavel="   ",
            )

        self.assertEqual(
            submissao["status_operacional"],
            "ENVIADA",
        )

        self.assertIsNone(
            submissao["protocolo"]
        )

    def test_submissao_inexistente_nao_pode_ser_protocolada(
        self
    ):
        with self.assertRaises(ValueError):
            protocolar_submissao_homologacao(
                homologacao=self.homologacao_ativa,
                codigo_submissao=999,
                protocolo="PROT-2026-001",
                data_protocolo="2026-08-02",
                responsavel="Ana Lima",
            )

    def test_homologacao_terminal_nao_pode_protocolar_submissao(
        self
    ):
        submissao = (
            self._enviar_submissao_valida()
        )

        self.homologacao_ativa["status"] = (
            StatusHomologacao.CANCELADA.value
        )

        quantidade_movimentacoes = len(
            self.homologacao_ativa["movimentacoes"]
        )

        with self.assertRaises(ValueError):
            protocolar_submissao_homologacao(
                homologacao=self.homologacao_ativa,
                codigo_submissao=submissao["codigo"],
                protocolo="PROT-2026-001",
                data_protocolo="2026-08-02",
                responsavel="Ana Lima",
            )

        self.assertEqual(
            submissao["status_operacional"],
            "ENVIADA",
        )

        self.assertIsNone(
            submissao["protocolo"]
        )

        self.assertEqual(
            len(self.homologacao_ativa["movimentacoes"]),
            quantidade_movimentacoes,
        )

    def test_submissao_protocolada_nao_pode_ser_protocolada_novamente(
        self
    ):
        submissao = (
            self._enviar_submissao_valida()
        )

        protocolar_submissao_homologacao(
            homologacao=self.homologacao_ativa,
            codigo_submissao=submissao["codigo"],
            protocolo="PROT-2026-001",
            data_protocolo="2026-08-02",
            responsavel="Ana Lima",
        )

        quantidade_movimentacoes = len(
            self.homologacao_ativa["movimentacoes"]
        )

        with self.assertRaises(ValueError):
            protocolar_submissao_homologacao(
                homologacao=self.homologacao_ativa,
                codigo_submissao=submissao["codigo"],
                protocolo="PROT-2026-002",
                data_protocolo="2026-08-03",
                responsavel="Carlos Souza",
            )

        self.assertEqual(
            submissao["protocolo"],
            "PROT-2026-001",
        )

        self.assertEqual(
            submissao["data_protocolo"],
            "2026-08-02",
        )

        self.assertEqual(
            len(self.homologacao_ativa["movimentacoes"]),
            quantidade_movimentacoes,
        )

    def test_protocolacao_nao_deve_duplicar_lista_protocolos(
        self
    ):
        submissao = (
            self._enviar_submissao_valida()
        )

        protocolar_submissao_homologacao(
            homologacao=self.homologacao_ativa,
            codigo_submissao=submissao["codigo"],
            protocolo="PROT-2026-001",
            data_protocolo="2026-08-02",
            responsavel="Ana Lima",
        )

        self.assertEqual(
            self.homologacao_ativa["protocolos"],
            [],
        )

    def test_deve_adicionar_resposta_de_recebimento(self):
        submissao = (
            self._protocolar_submissao_valida()
        )

        resposta = self._criar_resposta_recebimento()

        resultado = adicionar_resposta_concessionaria(
            homologacao=self.homologacao_ativa,
            codigo_submissao=submissao["codigo"],
            resposta=resposta,
        )

        self.assertIs(
            resultado,
            self.homologacao_ativa,
        )

        self.assertEqual(
            len(submissao["respostas"]),
            1,
        )

        self.assertEqual(
            submissao["status_analise"],
            "RECEBIDA",
        )

    def test_resposta_deve_ser_armazenada_como_copia(self):
        submissao = (
            self._protocolar_submissao_valida()
        )

        resposta = self._criar_resposta_recebimento()

        adicionar_resposta_concessionaria(
            homologacao=self.homologacao_ativa,
            codigo_submissao=submissao["codigo"],
            resposta=resposta,
        )

        resposta["descricao"] = "Alteração externa."

        self.assertEqual(
            submissao["respostas"][0]["descricao"],
            "Pacote recebido pela concessionária.",
        )

    def test_resposta_deve_registrar_movimentacao(self):
        submissao = (
            self._protocolar_submissao_valida()
        )

        resposta = self._criar_resposta_recebimento()

        adicionar_resposta_concessionaria(
            homologacao=self.homologacao_ativa,
            codigo_submissao=submissao["codigo"],
            resposta=resposta,
        )

        movimentacao = self.homologacao_ativa[
            "movimentacoes"
        ][-1]

        self.assertEqual(
            movimentacao["tipo_evento"],
            "RESPOSTA_CONCESSIONARIA_REGISTRADA",
        )

        self.assertEqual(
            movimentacao["status_anterior"],
            "SEM_RESPOSTA",
        )

        self.assertEqual(
            movimentacao["novo_status"],
            "RECEBIDA",
        )

        self.assertEqual(
            movimentacao["codigo_resposta"],
            resposta["codigo"],
        )

    def test_resposta_pode_ser_registrada_apos_envio(
        self
    ):
        submissao = (
            self._enviar_submissao_valida()
        )

        resposta = self._criar_resposta_recebimento(
            data_resposta="2026-08-02",
            data_registro="2026-08-02",
        )

        adicionar_resposta_concessionaria(
            homologacao=self.homologacao_ativa,
            codigo_submissao=submissao["codigo"],
            resposta=resposta,
        )

        self.assertEqual(
            submissao["status_analise"],
            "RECEBIDA",
        )

    def test_deve_registrar_inicio_da_analise(self):
        submissao = (
            self
            ._protocolar_submissao_com_homologacao_sincronizada()
        )

        recebimento = self._criar_resposta_recebimento()

        adicionar_resposta_concessionaria(
            homologacao=self.homologacao_ativa,
            codigo_submissao=submissao["codigo"],
            resposta=recebimento,
        )

        inicio_analise = criar_dados_resposta_inicio_analise(
            codigo=2,
            numero_sequencial=2,
            data_resposta="2026-08-04",
            data_registro="2026-08-04",
            responsavel_registro="Carlos Souza",
            descricao="Análise técnica iniciada.",
        )

        adicionar_resposta_concessionaria(
            homologacao=self.homologacao_ativa,
            codigo_submissao=submissao["codigo"],
            resposta=inicio_analise,
        )

        self.assertEqual(
            submissao["status_analise"],
            "EM_ANALISE",
        )

        self.assertEqual(
            len(submissao["respostas"]),
            2,
        )

        self.assertEqual(
            self.homologacao_ativa["status"],
            StatusHomologacao.EM_ANALISE.value,
        )

        movimentacao_resposta = self.homologacao_ativa[
            "movimentacoes"
        ][-2]

        movimentacao_status = self.homologacao_ativa[
            "movimentacoes"
        ][-1]

        self.assertEqual(
            movimentacao_resposta["tipo_evento"],
            "RESPOSTA_CONCESSIONARIA_REGISTRADA",
        )

        self.assertEqual(
            movimentacao_status["tipo_evento"],
            "STATUS_HOMOLOGACAO_ALTERADO",
        )

        self.assertEqual(
            movimentacao_status["status_anterior"],
            StatusHomologacao.ENVIADA_A_CONCESSIONARIA.value,
        )

        self.assertEqual(
            movimentacao_status["novo_status"],
            StatusHomologacao.EM_ANALISE.value,
        )

    def test_deve_registrar_aprovacao_direta(self):
        submissao = (
            self
            ._protocolar_submissao_com_homologacao_sincronizada()
        )

        resposta = criar_dados_resposta_aprovacao(
            codigo=1,
            numero_sequencial=1,
            data_resposta="2026-08-10",
            data_registro="2026-08-10",
            responsavel_registro="Ana Lima",
            descricao="Projeto aprovado.",
            identificador_aprovacao="APR-2026-001",
        )

        adicionar_resposta_concessionaria(
            homologacao=self.homologacao_ativa,
            codigo_submissao=submissao["codigo"],
            resposta=resposta,
        )

        self.assertEqual(
            submissao["status_analise"],
            "APROVADA",
        )

        self.assertEqual(
            self.homologacao_ativa["status"],
            (
                StatusHomologacao
                .PARECER_DE_ACESSO_EMITIDO
                .value
            ),
        )

        movimentacao_resposta = self.homologacao_ativa[
            "movimentacoes"
        ][-2]

        movimentacao_status = self.homologacao_ativa[
            "movimentacoes"
        ][-1]

        self.assertEqual(
            movimentacao_status["status_anterior"],
            (
                StatusHomologacao
                .ENVIADA_A_CONCESSIONARIA
                .value
            ),
        )

        self.assertEqual(
            movimentacao_status["novo_status"],
            (
                StatusHomologacao
                .PARECER_DE_ACESSO_EMITIDO
                .value
            ),
        )

        self.assertEqual(
            movimentacao_status["codigo"],
            movimentacao_resposta["codigo"] + 1,
        )

    def test_deve_registrar_rejeicao_direta(self):
        submissao = (
            self
            ._protocolar_submissao_com_homologacao_sincronizada()
        )

        resposta = criar_dados_resposta_rejeicao(
            codigo=1,
            numero_sequencial=1,
            data_resposta="2026-08-10",
            data_registro="2026-08-10",
            responsavel_registro="Ana Lima",
            descricao="Solicitação rejeitada.",
            carater_rejeicao="DEFINITIVA",
        )

        adicionar_resposta_concessionaria(
            homologacao=self.homologacao_ativa,
            codigo_submissao=submissao["codigo"],
            resposta=resposta,
        )

        self.assertEqual(
            submissao["status_analise"],
            "REJEITADA",
        )

        self.assertEqual(
            self.homologacao_ativa["status"],
            StatusHomologacao.REJEITADA.value,
        )

        movimentacao_resposta = self.homologacao_ativa[
            "movimentacoes"
        ][-2]

        movimentacao_status = self.homologacao_ativa[
            "movimentacoes"
        ][-1]

        self.assertEqual(
            movimentacao_status["tipo_evento"],
            "STATUS_HOMOLOGACAO_ALTERADO",
        )

        self.assertEqual(
            movimentacao_status["novo_status"],
            StatusHomologacao.REJEITADA.value,
        )

        self.assertEqual(
            movimentacao_status["motivo"],
            "Solicitação rejeitada.",
        )

        self.assertEqual(
            movimentacao_status["codigo"],
            movimentacao_resposta["codigo"] + 1,
        )

    def test_evento_de_analise_incompativel_nao_deve_registrar_resposta(
        self
    ):
        submissao = (
            self
            ._protocolar_submissao_com_homologacao_sincronizada()
        )

        resposta = criar_dados_resposta_inicio_analise(
            codigo=1,
            numero_sequencial=1,
            data_resposta="2026-08-03",
            data_registro="2026-08-03",
            responsavel_registro="Ana Lima",
        )

        self.homologacao_ativa["status"] = (
            StatusHomologacao.EM_PREPARACAO.value
        )

        quantidade_movimentacoes = len(
            self.homologacao_ativa["movimentacoes"]
        )

        with self.assertRaisesRegex(
            ValueError,
            "não pode ser aplicado ao estado atual",
        ):
            adicionar_resposta_concessionaria(
                homologacao=self.homologacao_ativa,
                codigo_submissao=submissao["codigo"],
                resposta=resposta,
            )

        self.assertEqual(
            submissao["respostas"],
            [],
        )

        self.assertEqual(
            submissao["status_analise"],
            StatusAnaliseSubmissao.SEM_RESPOSTA.value,
        )

        self.assertEqual(
            len(self.homologacao_ativa["movimentacoes"]),
            quantidade_movimentacoes,
        )

        self.assertEqual(
            self.homologacao_ativa["status"],
            StatusHomologacao.EM_PREPARACAO.value,
        )

    def test_nao_deve_adicionar_resposta_com_codigo_duplicado(
        self
    ):
        submissao = (
            self._protocolar_submissao_valida()
        )

        primeira = self._criar_resposta_recebimento()

        adicionar_resposta_concessionaria(
            homologacao=self.homologacao_ativa,
            codigo_submissao=submissao["codigo"],
            resposta=primeira,
        )

        segunda = criar_dados_resposta_inicio_analise(
            codigo=1,
            numero_sequencial=2,
            data_resposta="2026-08-04",
            data_registro="2026-08-04",
            responsavel_registro="Ana Lima",
        )

        with self.assertRaises(ValueError):
            adicionar_resposta_concessionaria(
                homologacao=self.homologacao_ativa,
                codigo_submissao=submissao["codigo"],
                resposta=segunda,
            )

        self.assertEqual(
            len(submissao["respostas"]),
            1,
        )

        self.assertEqual(
            submissao["status_analise"],
            "RECEBIDA",
        )

    def test_sequencia_da_resposta_deve_ser_continua(
        self
    ):
        submissao = (
            self._protocolar_submissao_valida()
        )

        resposta = self._criar_resposta_recebimento(
            numero_sequencial=2,
        )

        with self.assertRaises(ValueError):
            adicionar_resposta_concessionaria(
                homologacao=self.homologacao_ativa,
                codigo_submissao=submissao["codigo"],
                resposta=resposta,
            )

        self.assertEqual(
            submissao["respostas"],
            [],
        )

    def test_resposta_anterior_ao_envio_deve_ser_rejeitada(
        self
    ):
        submissao = (
            self._protocolar_submissao_valida()
        )

        resposta = self._criar_resposta_recebimento(
            data_resposta="2026-07-31",
            data_registro="2026-08-03",
        )

        with self.assertRaises(ValueError):
            adicionar_resposta_concessionaria(
                homologacao=self.homologacao_ativa,
                codigo_submissao=submissao["codigo"],
                resposta=resposta,
            )

        self.assertEqual(
            submissao["status_analise"],
            "SEM_RESPOSTA",
        )

        self.assertEqual(
            submissao["respostas"],
            [],
        )

    def test_submissao_nao_enviada_nao_recebe_resposta(
        self
    ):
        submissao = (
            self._preparar_submissao_para_envio()
        )

        resposta = self._criar_resposta_recebimento()

        with self.assertRaises(ValueError):
            adicionar_resposta_concessionaria(
                homologacao=self.homologacao_ativa,
                codigo_submissao=submissao["codigo"],
                resposta=resposta,
            )

        self.assertEqual(
            submissao["respostas"],
            [],
        )

    def test_estado_terminal_da_analise_nao_recebe_nova_resposta(
        self
    ):
        submissao = (
            self
            ._protocolar_submissao_com_homologacao_sincronizada()
        )

        aprovacao = criar_dados_resposta_aprovacao(
            codigo=1,
            numero_sequencial=1,
            data_resposta="2026-08-10",
            data_registro="2026-08-10",
            responsavel_registro="Ana Lima",
        )

        adicionar_resposta_concessionaria(
            homologacao=self.homologacao_ativa,
            codigo_submissao=submissao["codigo"],
            resposta=aprovacao,
        )

        nova_resposta = criar_dados_resposta_inicio_analise(
            codigo=2,
            numero_sequencial=2,
            data_resposta="2026-08-11",
            data_registro="2026-08-11",
            responsavel_registro="Carlos Souza",
        )

        with self.assertRaises(ValueError):
            adicionar_resposta_concessionaria(
                homologacao=self.homologacao_ativa,
                codigo_submissao=submissao["codigo"],
                resposta=nova_resposta,
            )

        self.assertEqual(
            submissao["status_analise"],
            "APROVADA",
        )

        self.assertEqual(
            len(submissao["respostas"]),
            1,
        )

    def test_homologacao_terminal_nao_recebe_resposta(
        self
    ):
        submissao = (
            self._protocolar_submissao_valida()
        )

        self.homologacao_ativa["status"] = (
            StatusHomologacao.CANCELADA.value
        )

        resposta = self._criar_resposta_recebimento()

        quantidade_movimentacoes = len(
            self.homologacao_ativa["movimentacoes"]
        )

        with self.assertRaises(ValueError):
            adicionar_resposta_concessionaria(
                homologacao=self.homologacao_ativa,
                codigo_submissao=submissao["codigo"],
                resposta=resposta,
            )

        self.assertEqual(
            submissao["respostas"],
            [],
        )

        self.assertEqual(
            len(self.homologacao_ativa["movimentacoes"]),
            quantidade_movimentacoes,
        )

    def test_deve_adicionar_resposta_de_exigencia(self):
        submissao = (
            self._protocolar_submissao_com_homologacao_sincronizada()
        )

        resposta = (
            self._criar_resposta_exigencia()
        )

        resultado = (
            adicionar_resposta_exigencia_concessionaria(
                homologacao=self.homologacao_ativa,
                codigo_submissao=submissao["codigo"],
                resposta=resposta,
            )
        )

        self.assertIs(
            resultado,
            self.homologacao_ativa,
        )

        self.assertEqual(
            submissao["status_analise"],
            "COM_EXIGENCIA",
        )

        self.assertEqual(
            len(submissao["respostas"]),
            1,
        )

        resposta_armazenada = submissao[
            "respostas"
        ][0]

        self.assertEqual(
            resposta_armazenada["tipo"],
            "EXIGENCIA",
        )

        self.assertEqual(
            len(resposta_armazenada["exigencias"]),
            1,
        )

        self.assertEqual(
            self.homologacao_ativa["status"],
            StatusHomologacao.COM_EXIGENCIA.value,
        )

    def test_resposta_exigencia_deve_registrar_movimentacao(
        self
    ):
        submissao = (
            self._protocolar_submissao_com_homologacao_sincronizada()
        )

        resposta = (
            self._criar_resposta_exigencia()
        )

        adicionar_resposta_exigencia_concessionaria(
            homologacao=self.homologacao_ativa,
            codigo_submissao=submissao["codigo"],
            resposta=resposta,
        )

        movimentacao = self.homologacao_ativa[
            "movimentacoes"
        ][-2]

        self.assertEqual(
            movimentacao["tipo_evento"],
            "EXIGENCIAS_CONCESSIONARIA_REGISTRADAS",
        )

        self.assertEqual(
            movimentacao["status_anterior"],
            "SEM_RESPOSTA",
        )

        self.assertEqual(
            movimentacao["novo_status"],
            "COM_EXIGENCIA",
        )

        self.assertEqual(
            movimentacao["codigo_resposta"],
            resposta["codigo"],
        )

        self.assertEqual(
            movimentacao["codigos_exigencias"],
            [1],
        )

        movimentacao_status = self.homologacao_ativa[
            "movimentacoes"
        ][-1]

        self.assertEqual(
            movimentacao_status["tipo_evento"],
            "STATUS_HOMOLOGACAO_ALTERADO",
        )

        self.assertEqual(
            movimentacao_status["status_anterior"],
            StatusHomologacao.ENVIADA_A_CONCESSIONARIA.value,
        )

        self.assertEqual(
            movimentacao_status["novo_status"],
            StatusHomologacao.COM_EXIGENCIA.value,
        )

        self.assertEqual(
            movimentacao_status["codigo"],
            movimentacao["codigo"] + 1,
        )

    def test_deve_adicionar_multiplas_exigencias(self):
        submissao = (
            self._protocolar_submissao_com_homologacao_sincronizada()
        )

        primeira_exigencia = self._criar_exigencia(
            codigo=1,
            numero_sequencial=1,
        )

        segunda_exigencia = self._criar_exigencia(
            codigo=2,
            numero_sequencial=2,
            tipo="ESCLARECIMENTO",
            descricao=(
                "Informar a potência instalada correta."
            ),
            codigos_documentos_afetados=[],
        )

        resposta = self._criar_resposta_exigencia(
            exigencias=[
                primeira_exigencia,
                segunda_exigencia,
            ]
        )

        adicionar_resposta_exigencia_concessionaria(
            homologacao=self.homologacao_ativa,
            codigo_submissao=submissao["codigo"],
            resposta=resposta,
        )

        exigencias_armazenadas = submissao[
            "respostas"
        ][0]["exigencias"]

        self.assertEqual(
            len(exigencias_armazenadas),
            2,
        )

        self.assertEqual(
            exigencias_armazenadas[0]["codigo"],
            1,
        )

        self.assertEqual(
            exigencias_armazenadas[1]["codigo"],
            2,
        )

    def test_resposta_exigencia_deve_ser_copiada_com_seguranca(
        self
    ):
        submissao = (
            self._protocolar_submissao_com_homologacao_sincronizada()
        )

        resposta = (
            self._criar_resposta_exigencia()
        )

        adicionar_resposta_exigencia_concessionaria(
            homologacao=self.homologacao_ativa,
            codigo_submissao=submissao["codigo"],
            resposta=resposta,
        )

        resposta["exigencias"][0]["descricao"] = (
            "Descrição alterada externamente."
        )

        resposta["exigencias"][0][
            "codigos_documentos_afetados"
        ].append(999)

        exigencia_armazenada = submissao[
            "respostas"
        ][0]["exigencias"][0]

        self.assertEqual(
            exigencia_armazenada["descricao"],
            "Corrigir o documento apresentado.",
        )

        self.assertEqual(
            exigencia_armazenada[
                "codigos_documentos_afetados"
            ],
            [1],
        )

    def test_exigencia_nao_pode_referenciar_documento_inexistente(
        self
    ):
        submissao = (
            self._protocolar_submissao_valida()
        )

        exigencia = self._criar_exigencia(
            codigos_documentos_afetados=[999],
        )

        resposta = self._criar_resposta_exigencia(
            exigencias=[exigencia],
        )

        quantidade_movimentacoes = len(
            self.homologacao_ativa["movimentacoes"]
        )

        with self.assertRaises(ValueError):
            adicionar_resposta_exigencia_concessionaria(
                homologacao=self.homologacao_ativa,
                codigo_submissao=submissao["codigo"],
                resposta=resposta,
            )

        self.assertEqual(
            submissao["status_analise"],
            "SEM_RESPOSTA",
        )

        self.assertEqual(
            submissao["respostas"],
            [],
        )

        self.assertEqual(
            len(self.homologacao_ativa["movimentacoes"]),
            quantidade_movimentacoes,
        )

    def test_sequencia_das_exigencias_deve_ser_continua(
        self
    ):
        submissao = (
            self._protocolar_submissao_valida()
        )

        primeira_exigencia = self._criar_exigencia(
            codigo=1,
            numero_sequencial=1,
        )

        terceira_exigencia = self._criar_exigencia(
            codigo=2,
            numero_sequencial=3,
            codigos_documentos_afetados=[],
        )

        resposta = self._criar_resposta_exigencia(
            exigencias=[
                primeira_exigencia,
                terceira_exigencia,
            ],
        )

        with self.assertRaises(ValueError):
            adicionar_resposta_exigencia_concessionaria(
                homologacao=self.homologacao_ativa,
                codigo_submissao=submissao["codigo"],
                resposta=resposta,
            )

        self.assertEqual(
            submissao["respostas"],
            [],
        )

        self.assertEqual(
            submissao["status_analise"],
            "SEM_RESPOSTA",
        )

    def test_codigo_exigencia_deve_ser_unico_na_homologacao(
        self
    ):
        submissao = (
            self._protocolar_submissao_valida()
        )

        resposta_anterior = (
            self._criar_resposta_exigencia()
        )

        submissao_historica = {
            "codigo": 99,
            "respostas": [
                resposta_anterior
            ],
        }

        self.homologacao_ativa[
            "submissoes"
        ].append(submissao_historica)

        nova_exigencia = self._criar_exigencia(
            codigo=1,
            numero_sequencial=1,
        )

        nova_resposta = self._criar_resposta_exigencia(
            codigo=2,
            exigencias=[nova_exigencia],
        )

        with self.assertRaises(ValueError):
            adicionar_resposta_exigencia_concessionaria(
                homologacao=self.homologacao_ativa,
                codigo_submissao=submissao["codigo"],
                resposta=nova_resposta,
            )

        self.assertEqual(
            submissao["respostas"],
            [],
        )

    def test_operacao_de_exigencia_deve_rejeitar_outro_tipo(
        self
    ):
        submissao = (
            self._protocolar_submissao_valida()
        )

        resposta = self._criar_resposta_recebimento()

        with self.assertRaises(ValueError):
            adicionar_resposta_exigencia_concessionaria(
                homologacao=self.homologacao_ativa,
                codigo_submissao=submissao["codigo"],
                resposta=resposta,
            )

        self.assertEqual(
            submissao["respostas"],
            [],
        )

        self.assertEqual(
            submissao["status_analise"],
            "SEM_RESPOSTA",
        )

    def test_resposta_exigencia_anterior_ao_envio_deve_falhar(
        self
    ):
        submissao = (
            self._protocolar_submissao_valida()
        )

        resposta = self._criar_resposta_exigencia(
            data_resposta="2026-07-31",
            data_registro="2026-08-05",
        )

        with self.assertRaises(ValueError):
            adicionar_resposta_exigencia_concessionaria(
                homologacao=self.homologacao_ativa,
                codigo_submissao=submissao["codigo"],
                resposta=resposta,
            )

        self.assertEqual(
            submissao["respostas"],
            [],
        )

        self.assertEqual(
            submissao["status_analise"],
            "SEM_RESPOSTA",
        )

    def test_submissao_nao_enviada_nao_recebe_exigencia(
        self
    ):
        submissao = (
            self._preparar_submissao_para_envio()
        )

        resposta = (
            self._criar_resposta_exigencia()
        )

        with self.assertRaises(ValueError):
            adicionar_resposta_exigencia_concessionaria(
                homologacao=self.homologacao_ativa,
                codigo_submissao=submissao["codigo"],
                resposta=resposta,
            )

        self.assertEqual(
            submissao["respostas"],
            [],
        )

        self.assertEqual(
            submissao["status_analise"],
            "SEM_RESPOSTA",
        )

    def test_analise_aprovada_nao_pode_receber_exigencia(
        self
    ):
        submissao = (
            self
            ._protocolar_submissao_com_homologacao_sincronizada()
        )

        aprovacao = criar_dados_resposta_aprovacao(
            codigo=1,
            numero_sequencial=1,
            data_resposta="2026-08-05",
            data_registro="2026-08-05",
            responsavel_registro="Ana Lima",
        )

        adicionar_resposta_concessionaria(
            homologacao=self.homologacao_ativa,
            codigo_submissao=submissao["codigo"],
            resposta=aprovacao,
        )

        exigencia = self._criar_exigencia(
            codigo=2,
        )

        resposta_exigencia = self._criar_resposta_exigencia(
            codigo=2,
            numero_sequencial=2,
            exigencias=[exigencia],
            data_resposta="2026-08-06",
            data_registro="2026-08-06",
        )

        quantidade_movimentacoes = len(
            self.homologacao_ativa["movimentacoes"]
        )

        with self.assertRaises(ValueError):
            adicionar_resposta_exigencia_concessionaria(
                homologacao=self.homologacao_ativa,
                codigo_submissao=submissao["codigo"],
                resposta=resposta_exigencia,
            )

        self.assertEqual(
            submissao["status_analise"],
            "APROVADA",
        )

        self.assertEqual(
            len(submissao["respostas"]),
            1,
        )

        self.assertEqual(
            len(self.homologacao_ativa["movimentacoes"]),
            quantidade_movimentacoes,
        )

    def test_homologacao_terminal_nao_recebe_exigencia(
        self
    ):
        submissao = (
            self._protocolar_submissao_valida()
        )

        self.homologacao_ativa["status"] = (
            StatusHomologacao.CANCELADA.value
        )

        resposta = (
            self._criar_resposta_exigencia()
        )

        quantidade_movimentacoes = len(
            self.homologacao_ativa["movimentacoes"]
        )

        with self.assertRaises(ValueError):
            adicionar_resposta_exigencia_concessionaria(
                homologacao=self.homologacao_ativa,
                codigo_submissao=submissao["codigo"],
                resposta=resposta,
            )

        self.assertEqual(
            submissao["respostas"],
            [],
        )

        self.assertEqual(
            submissao["status_analise"],
            "SEM_RESPOSTA",
        )

        self.assertEqual(
            len(self.homologacao_ativa["movimentacoes"]),
            quantidade_movimentacoes,
        )

    def test_exigencias_nao_devem_ser_duplicadas_na_raiz(
        self
    ):
        submissao = (
            self._protocolar_submissao_com_homologacao_sincronizada()
        )

        resposta = (
            self._criar_resposta_exigencia()
        )

        adicionar_resposta_exigencia_concessionaria(
            homologacao=self.homologacao_ativa,
            codigo_submissao=submissao["codigo"],
            resposta=resposta,
        )

        self.assertEqual(
            self.homologacao_ativa["exigencias"],
            [],
        )

        self.assertEqual(
            len(
                submissao["respostas"][0]["exigencias"]
            ),
            1,
        )

    def test_deve_adicionar_complementacao_para_exigencia(
        self
    ):
        submissao_origem = (
            self._protocolar_submissao_com_homologacao_sincronizada()
        )

        exigencia = self._criar_exigencia(
            codigo=1,
            numero_sequencial=1,
            tipo="COMPLEMENTACAO_DOCUMENTAL",
            descricao="Apresentar documento complementar.",
        )

        resposta = self._criar_resposta_exigencia(
            codigo=1,
            numero_sequencial=1,
            exigencias=[exigencia],
        )

        adicionar_resposta_exigencia_concessionaria(
            homologacao=self.homologacao_ativa,
            codigo_submissao=submissao_origem["codigo"],
            resposta=resposta,
        )

        referencia = criar_referencia_documento(
            codigo_documento=1,
            numero_versao=1,
        )

        complementacao = criar_dados_submissao(
            codigo=2,
            numero_sequencial=2,
            tipo="COMPLEMENTACAO",
            data_criacao="2026-08-06",
            responsavel_criacao="Ana Lima",
            pacote_documental=[referencia],
            codigo_submissao_origem=(
                submissao_origem["codigo"]
            ),
            codigo_resposta_origem=resposta["codigo"],
            codigos_exigencias_relacionadas=[1],
        )

        resultado = adicionar_submissao_homologacao(
            homologacao=self.homologacao_ativa,
            submissao=complementacao,
            data_movimentacao="2026-08-06",
            responsavel="Ana Lima",
        )

        self.assertIs(
            resultado,
            self.homologacao_ativa,
        )

        self.assertEqual(
            len(self.homologacao_ativa["submissoes"]),
            2,
        )

        self.assertIs(
            self.homologacao_ativa["submissoes"][1],
            complementacao,
        )

        self.assertEqual(
            complementacao["codigo_submissao_origem"],
            submissao_origem["codigo"],
        )

        self.assertEqual(
            complementacao["codigo_resposta_origem"],
            resposta["codigo"],
        )

        self.assertEqual(
            complementacao[
                "codigos_exigencias_relacionadas"
            ],
            [1],
        )

        self.assertEqual(
            exigencia["status_atendimento"],
            "PENDENTE",
        )

        self.assertEqual(
            self.homologacao_ativa["status"],
            StatusHomologacao.EM_CORRECAO.value,
        )

        movimentacao_submissao = self.homologacao_ativa[
            "movimentacoes"
        ][-2]

        movimentacao_status = self.homologacao_ativa[
            "movimentacoes"
        ][-1]

        self.assertEqual(
            movimentacao_submissao["tipo_evento"],
            "SUBMISSAO_ADICIONADA",
        )

        self.assertEqual(
            movimentacao_status["tipo_evento"],
            "STATUS_HOMOLOGACAO_ALTERADO",
        )

        self.assertEqual(
            movimentacao_status["status_anterior"],
            StatusHomologacao.COM_EXIGENCIA.value,
        )

        self.assertEqual(
            movimentacao_status["novo_status"],
            StatusHomologacao.EM_CORRECAO.value,
        )

        self.assertEqual(
            movimentacao_status["codigo"],
            movimentacao_submissao["codigo"] + 1,
        )

    def test_exigencia_nao_pode_ter_dois_atendimentos_ativos(
        self
    ):
        submissao_origem = (
            self
            ._protocolar_submissao_com_homologacao_sincronizada()
        )

        exigencia = self._criar_exigencia(
            codigo=1,
            numero_sequencial=1,
            tipo="COMPLEMENTACAO_DOCUMENTAL",
            descricao="Apresentar documento complementar.",
        )

        resposta = self._criar_resposta_exigencia(
            codigo=1,
            numero_sequencial=1,
            exigencias=[exigencia],
        )

        adicionar_resposta_exigencia_concessionaria(
            homologacao=self.homologacao_ativa,
            codigo_submissao=submissao_origem["codigo"],
            resposta=resposta,
        )

        referencia = criar_referencia_documento(
            codigo_documento=1,
            numero_versao=1,
        )

        primeira_complementacao = criar_dados_submissao(
            codigo=2,
            numero_sequencial=2,
            tipo="COMPLEMENTACAO",
            data_criacao="2026-08-06",
            responsavel_criacao="Ana Lima",
            pacote_documental=[referencia],
            codigo_submissao_origem=(
                submissao_origem["codigo"]
            ),
            codigo_resposta_origem=resposta["codigo"],
            codigos_exigencias_relacionadas=[1],
        )

        adicionar_submissao_homologacao(
            homologacao=self.homologacao_ativa,
            submissao=primeira_complementacao,
            data_movimentacao="2026-08-06",
            responsavel="Ana Lima",
        )

        segunda_complementacao = criar_dados_submissao(
            codigo=3,
            numero_sequencial=3,
            tipo="COMPLEMENTACAO",
            data_criacao="2026-08-07",
            responsavel_criacao="Carlos Souza",
            pacote_documental=[referencia],
            codigo_submissao_origem=(
                submissao_origem["codigo"]
            ),
            codigo_resposta_origem=resposta["codigo"],
            codigos_exigencias_relacionadas=[1],
        )

        quantidade_movimentacoes = len(
            self.homologacao_ativa["movimentacoes"]
        )

        with self.assertRaisesRegex(
            ValueError,
            "já está relacionada a outra Submissão ativa",
        ):
            adicionar_submissao_homologacao(
                homologacao=self.homologacao_ativa,
                submissao=segunda_complementacao,
                data_movimentacao="2026-08-07",
                responsavel="Carlos Souza",
            )

        self.assertEqual(
            len(self.homologacao_ativa["submissoes"]),
            2,
        )

        self.assertEqual(
            len(self.homologacao_ativa["movimentacoes"]),
            quantidade_movimentacoes,
        )

    def test_envio_de_complementacao_deve_atender_exigencia(
        self
    ):
        submissao_origem = (
            self._protocolar_submissao_com_homologacao_sincronizada()
        )

        exigencia = self._criar_exigencia(
            codigo=1,
            numero_sequencial=1,
            tipo="COMPLEMENTACAO_DOCUMENTAL",
        )

        resposta = self._criar_resposta_exigencia(
            exigencias=[exigencia],
        )

        adicionar_resposta_exigencia_concessionaria(
            homologacao=self.homologacao_ativa,
            codigo_submissao=submissao_origem["codigo"],
            resposta=resposta,
        )

        complementacao = criar_dados_submissao(
            codigo=2,
            numero_sequencial=2,
            tipo="COMPLEMENTACAO",
            data_criacao="2026-08-06",
            responsavel_criacao="Ana Lima",
            pacote_documental=[
                criar_referencia_documento(1, 1)
            ],
            codigo_submissao_origem=(
                submissao_origem["codigo"]
            ),
            codigo_resposta_origem=resposta["codigo"],
            codigos_exigencias_relacionadas=[1],
        )

        adicionar_submissao_homologacao(
            homologacao=self.homologacao_ativa,
            submissao=complementacao,
            data_movimentacao="2026-08-06",
            responsavel="Ana Lima",
        )

        alterar_status_operacional_submissao(
            homologacao=self.homologacao_ativa,
            codigo_submissao=complementacao["codigo"],
            novo_status="PRONTA_PARA_ENVIO",
            data_movimentacao="2026-08-07",
            responsavel="Carlos Souza",
        )

        enviar_submissao_homologacao(
            homologacao=self.homologacao_ativa,
            codigo_submissao=complementacao["codigo"],
            canal_envio="PORTAL",
            data_envio="2026-08-08",
            responsavel_envio="Carlos Souza",
        )

        exigencia_armazenada = (
            submissao_origem["respostas"][0]["exigencias"][0]
        )

        self.assertEqual(
            exigencia_armazenada["status_atendimento"],
            "ATENDIDA",
        )

        self.assertEqual(
            exigencia_armazenada[
                "codigo_submissao_atendimento"
            ],
            complementacao["codigo"],
        )

        self.assertEqual(
            exigencia_armazenada["data_atendimento"],
            "2026-08-08",
        )

        self.assertEqual(
            exigencia_armazenada[
                "responsavel_atendimento"
            ],
            "Carlos Souza",
        )

        self.assertEqual(
            self.homologacao_ativa["status"],
            StatusHomologacao.REAPRESENTADA.value,
        )

        movimentacao_envio = self.homologacao_ativa[
            "movimentacoes"
        ][-2]

        movimentacao_status = self.homologacao_ativa[
            "movimentacoes"
        ][-1]

        self.assertEqual(
            movimentacao_envio["tipo_evento"],
            "SUBMISSAO_ENVIADA",
        )

        self.assertEqual(
            movimentacao_status["tipo_evento"],
            "STATUS_HOMOLOGACAO_ALTERADO",
        )

        self.assertEqual(
            movimentacao_status["status_anterior"],
            StatusHomologacao.EM_CORRECAO.value,
        )

        self.assertEqual(
            movimentacao_status["novo_status"],
            StatusHomologacao.REAPRESENTADA.value,
        )

        self.assertEqual(
            movimentacao_status["codigo"],
            movimentacao_envio["codigo"] + 1,
        )

    def test_falha_no_atendimento_nao_deve_enviar_submissao(
        self
    ):
        submissao_origem = (
            self
            ._protocolar_submissao_com_homologacao_sincronizada()
        )

        primeira_exigencia = self._criar_exigencia(
            codigo=1,
            numero_sequencial=1,
            tipo="COMPLEMENTACAO_DOCUMENTAL",
        )

        segunda_exigencia = self._criar_exigencia(
            codigo=2,
            numero_sequencial=2,
            tipo="COMPLEMENTACAO_DOCUMENTAL",
        )

        resposta = self._criar_resposta_exigencia(
            exigencias=[
                primeira_exigencia,
                segunda_exigencia,
            ],
        )

        adicionar_resposta_exigencia_concessionaria(
            homologacao=self.homologacao_ativa,
            codigo_submissao=submissao_origem["codigo"],
            resposta=resposta,
        )

        complementacao = criar_dados_submissao(
            codigo=2,
            numero_sequencial=2,
            tipo="COMPLEMENTACAO",
            data_criacao="2026-08-06",
            responsavel_criacao="Ana Lima",
            pacote_documental=[
                criar_referencia_documento(1, 1)
            ],
            codigo_submissao_origem=(
                submissao_origem["codigo"]
            ),
            codigo_resposta_origem=resposta["codigo"],
            codigos_exigencias_relacionadas=[1, 2],
        )

        adicionar_submissao_homologacao(
            homologacao=self.homologacao_ativa,
            submissao=complementacao,
            data_movimentacao="2026-08-06",
            responsavel="Ana Lima",
        )

        alterar_status_operacional_submissao(
            homologacao=self.homologacao_ativa,
            codigo_submissao=complementacao["codigo"],
            novo_status="PRONTA_PARA_ENVIO",
            data_movimentacao="2026-08-07",
            responsavel="Carlos Souza",
        )

        exigencias_armazenadas = (
            submissao_origem["respostas"][0]["exigencias"]
        )

        exigencias_armazenadas[1]["status_atendimento"] = (
            "ATENDIDA"
        )

        exigencias_armazenadas[1][
            "codigo_submissao_atendimento"
        ] = 99

        exigencias_armazenadas[1]["data_atendimento"] = (
            "2026-08-07"
        )

        exigencias_armazenadas[1][
            "responsavel_atendimento"
        ] = "Outro usuário"

        quantidade_movimentacoes = len(
            self.homologacao_ativa["movimentacoes"]
        )

        with self.assertRaises(ValueError):
            enviar_submissao_homologacao(
                homologacao=self.homologacao_ativa,
                codigo_submissao=complementacao["codigo"],
                canal_envio="PORTAL",
                data_envio="2026-08-08",
                responsavel_envio="Carlos Souza",
            )

        self.assertEqual(
            complementacao["status_operacional"],
            "PRONTA_PARA_ENVIO",
        )

        self.assertEqual(
            exigencias_armazenadas[0]["status_atendimento"],
            "PENDENTE",
        )

        self.assertEqual(
            len(self.homologacao_ativa["movimentacoes"]),
            quantidade_movimentacoes,
        )

    def test_deve_aplicar_evento_de_exigencia(
        self
    ):
        self.homologacao_ativa["status"] = (
            StatusHomologacao.EM_ANALISE.value
        )

        resultado = aplicar_evento_homologacao(
            homologacao=self.homologacao_ativa,
            evento=EventoHomologacao.EXIGENCIA_RECEBIDA,
            data_movimentacao="2026-08-05",
            responsavel="Ana Lima",
        )

        self.assertIs(
            resultado,
            self.homologacao_ativa,
        )

        self.assertEqual(
            self.homologacao_ativa["status"],
            StatusHomologacao.COM_EXIGENCIA.value,
        )

    def test_evento_deve_registrar_movimentacao(
        self
    ):
        self.homologacao_ativa["status"] = (
            StatusHomologacao.COM_EXIGENCIA.value
        )

        quantidade_anterior = len(
            self.homologacao_ativa["movimentacoes"]
        )

        aplicar_evento_homologacao(
            homologacao=self.homologacao_ativa,
            evento="SUBMISSAO_DERIVADA_CRIADA",
            data_movimentacao="2026-08-06",
            responsavel="Carlos Souza",
        )

        movimentacao = self.homologacao_ativa[
            "movimentacoes"
        ][-1]

        self.assertEqual(
            len(self.homologacao_ativa["movimentacoes"]),
            quantidade_anterior + 1,
        )

        self.assertEqual(
            movimentacao["status_anterior"],
            StatusHomologacao.COM_EXIGENCIA.value,
        )

        self.assertEqual(
            movimentacao["novo_status"],
            StatusHomologacao.EM_CORRECAO.value,
        )

        self.assertEqual(
            movimentacao["descricao"],
            (
                "Evento de negócio aplicado à Homologação: "
                "SUBMISSAO_DERIVADA_CRIADA."
            ),
        )

    def test_evento_incompativel_nao_deve_alterar_homologacao(
        self
    ):
        status_anterior = self.homologacao_ativa["status"]

        quantidade_movimentacoes = len(
            self.homologacao_ativa["movimentacoes"]
        )

        with self.assertRaisesRegex(
            ValueError,
            "não pode ser aplicado ao estado atual",
        ):
            aplicar_evento_homologacao(
                homologacao=self.homologacao_ativa,
                evento="SUBMISSAO_DERIVADA_ENVIADA",
                data_movimentacao="2026-08-06",
                responsavel="Ana Lima",
            )

        self.assertEqual(
            self.homologacao_ativa["status"],
            status_anterior,
        )

        self.assertEqual(
            len(self.homologacao_ativa["movimentacoes"]),
            quantidade_movimentacoes,
        )

    def test_evento_incompativel_nao_deve_registrar_exigencia(
        self
    ):
        submissao = (
            self._protocolar_submissao_valida()
        )

        resposta = (
            self._criar_resposta_exigencia()
        )

        status_anterior = self.homologacao_ativa["status"]

        quantidade_movimentacoes = len(
            self.homologacao_ativa["movimentacoes"]
        )

        with self.assertRaisesRegex(
            ValueError,
            "não pode ser aplicado ao estado atual",
        ):
            adicionar_resposta_exigencia_concessionaria(
                homologacao=self.homologacao_ativa,
                codigo_submissao=submissao["codigo"],
                resposta=resposta,
            )

        self.assertEqual(
            submissao["respostas"],
            [],
        )

        self.assertEqual(
            submissao["status_analise"],
            StatusAnaliseSubmissao.SEM_RESPOSTA.value,
        )

        self.assertEqual(
            self.homologacao_ativa["status"],
            status_anterior,
        )

        self.assertEqual(
            len(self.homologacao_ativa["movimentacoes"]),
            quantidade_movimentacoes,
        )

    def test_evento_incompativel_nao_deve_adicionar_submissao_derivada(
        self
    ):
        submissao_origem = (
            self
            ._protocolar_submissao_com_homologacao_sincronizada()
        )

        exigencia = self._criar_exigencia(
            codigo=1,
            numero_sequencial=1,
            tipo="COMPLEMENTACAO_DOCUMENTAL",
            descricao="Apresentar documento complementar.",
        )

        resposta = self._criar_resposta_exigencia(
            exigencias=[exigencia],
        )

        adicionar_resposta_exigencia_concessionaria(
            homologacao=self.homologacao_ativa,
            codigo_submissao=submissao_origem["codigo"],
            resposta=resposta,
        )

        referencia = criar_referencia_documento(
            codigo_documento=1,
            numero_versao=1,
        )

        complementacao = criar_dados_submissao(
            codigo=2,
            numero_sequencial=2,
            tipo="COMPLEMENTACAO",
            data_criacao="2026-08-06",
            responsavel_criacao="Ana Lima",
            pacote_documental=[referencia],
            codigo_submissao_origem=(
                submissao_origem["codigo"]
            ),
            codigo_resposta_origem=resposta["codigo"],
            codigos_exigencias_relacionadas=[1],
        )

        # Simula uma inconsistência externa no estado geral.
        #
        # A Submissão é localmente válida, mas o Evento
        # SUBMISSAO_DERIVADA_CRIADA somente pode ocorrer quando
        # a Homologação está em COM_EXIGENCIA.
        self.homologacao_ativa["status"] = (
            StatusHomologacao.EM_ANALISE.value
        )

        quantidade_submissoes = len(
            self.homologacao_ativa["submissoes"]
        )

        quantidade_movimentacoes = len(
            self.homologacao_ativa["movimentacoes"]
        )

        with self.assertRaisesRegex(
            ValueError,
            "não pode ser aplicado ao estado atual",
        ):
            adicionar_submissao_homologacao(
                homologacao=self.homologacao_ativa,
                submissao=complementacao,
                data_movimentacao="2026-08-06",
                responsavel="Ana Lima",
            )

        self.assertEqual(
            len(self.homologacao_ativa["submissoes"]),
            quantidade_submissoes,
        )

        self.assertNotIn(
            complementacao,
            self.homologacao_ativa["submissoes"],
        )

        self.assertEqual(
            len(self.homologacao_ativa["movimentacoes"]),
            quantidade_movimentacoes,
        )

        self.assertEqual(
            self.homologacao_ativa["status"],
            StatusHomologacao.EM_ANALISE.value,
        )

    def test_evento_incompativel_nao_deve_enviar_submissao_derivada(
        self
    ):
        submissao_origem = (
            self
            ._protocolar_submissao_com_homologacao_sincronizada()
        )

        exigencia = self._criar_exigencia(
            codigo=1,
            numero_sequencial=1,
            tipo="COMPLEMENTACAO_DOCUMENTAL",
            descricao="Apresentar documento complementar.",
        )

        resposta = self._criar_resposta_exigencia(
            exigencias=[exigencia],
        )

        adicionar_resposta_exigencia_concessionaria(
            homologacao=self.homologacao_ativa,
            codigo_submissao=submissao_origem["codigo"],
            resposta=resposta,
        )

        referencia = criar_referencia_documento(
            codigo_documento=1,
            numero_versao=1,
        )

        complementacao = criar_dados_submissao(
            codigo=2,
            numero_sequencial=2,
            tipo="COMPLEMENTACAO",
            data_criacao="2026-08-06",
            responsavel_criacao="Ana Lima",
            pacote_documental=[referencia],
            codigo_submissao_origem=(
                submissao_origem["codigo"]
            ),
            codigo_resposta_origem=resposta["codigo"],
            codigos_exigencias_relacionadas=[1],
        )

        adicionar_submissao_homologacao(
            homologacao=self.homologacao_ativa,
            submissao=complementacao,
            data_movimentacao="2026-08-06",
            responsavel="Ana Lima",
        )

        alterar_status_operacional_submissao(
            homologacao=self.homologacao_ativa,
            codigo_submissao=complementacao["codigo"],
            novo_status="PRONTA_PARA_ENVIO",
            data_movimentacao="2026-08-07",
            responsavel="Carlos Souza",
        )

        # Simula uma inconsistência no estado geral.
        self.homologacao_ativa["status"] = (
            StatusHomologacao.COM_EXIGENCIA.value
        )

        quantidade_movimentacoes = len(
            self.homologacao_ativa["movimentacoes"]
        )

        with self.assertRaisesRegex(
            ValueError,
            "não pode ser aplicado ao estado atual",
        ):
            enviar_submissao_homologacao(
                homologacao=self.homologacao_ativa,
                codigo_submissao=complementacao["codigo"],
                canal_envio="PORTAL",
                data_envio="2026-08-08",
                responsavel_envio="Carlos Souza",
            )

        self.assertEqual(
            complementacao["status_operacional"],
            "PRONTA_PARA_ENVIO",
        )

        self.assertIsNone(
            complementacao["canal_envio"]
        )

        self.assertEqual(
            exigencia["status_atendimento"],
            "PENDENTE",
        )

        self.assertEqual(
            len(self.homologacao_ativa["movimentacoes"]),
            quantidade_movimentacoes,
        )

        self.assertEqual(
            self.homologacao_ativa["status"],
            StatusHomologacao.COM_EXIGENCIA.value,
        )

    def test_fluxo_completo_de_exigencia_deve_terminar_aprovado(
        self
    ):
        """
        Valida uma rodada completa do processo:

        1. envio e protocolo da Submissão Inicial;
        2. início da análise pela concessionária;
        3. recebimento de uma Exigência;
        4. criação de uma Complementação;
        5. envio e protocolo da Complementação;
        6. reinício da análise;
        7. aprovação final.

        O teste também confirma:

        - atendimento da Exigência;
        - vínculo entre as Submissões;
        - sequência das Movimentações;
        - estado final da Homologação.
        """

        # ---------------------------------------------------------
        # 1. Submissão Inicial enviada e protocolada
        # ---------------------------------------------------------

        submissao_inicial = (
            self
            ._protocolar_submissao_com_homologacao_sincronizada()
        )

        self.assertEqual(
            self.homologacao_ativa["status"],
            (
                StatusHomologacao
                .ENVIADA_A_CONCESSIONARIA
                .value
            ),
        )

        # ---------------------------------------------------------
        # 2. A concessionária inicia a análise
        # ---------------------------------------------------------

        inicio_analise_inicial = (
            criar_dados_resposta_inicio_analise(
                codigo=1,
                numero_sequencial=1,
                data_resposta="2026-08-03",
                data_registro="2026-08-03",
                responsavel_registro="Ana Lima",
                descricao="Análise técnica iniciada.",
            )
        )

        adicionar_resposta_concessionaria(
            homologacao=self.homologacao_ativa,
            codigo_submissao=submissao_inicial["codigo"],
            resposta=inicio_analise_inicial,
        )

        self.assertEqual(
            self.homologacao_ativa["status"],
            StatusHomologacao.EM_ANALISE.value,
        )

        self.assertEqual(
            submissao_inicial["status_analise"],
            "EM_ANALISE",
        )

        # ---------------------------------------------------------
        # 3. A concessionária registra uma Exigência
        # ---------------------------------------------------------

        exigencia = self._criar_exigencia(
            codigo=1,
            numero_sequencial=1,
            tipo="COMPLEMENTACAO_DOCUMENTAL",
            descricao=(
                "Apresentar documento complementar."
            ),
        )

        resposta_exigencia = (
            self._criar_resposta_exigencia(
                codigo=2,
                numero_sequencial=2,
                exigencias=[exigencia],
                data_resposta="2026-08-05",
                data_registro="2026-08-05",
            )
        )

        adicionar_resposta_exigencia_concessionaria(
            homologacao=self.homologacao_ativa,
            codigo_submissao=submissao_inicial["codigo"],
            resposta=resposta_exigencia,
        )

        exigencia_armazenada = (
            submissao_inicial["respostas"][1]["exigencias"][0]
        )

        self.assertEqual(
            self.homologacao_ativa["status"],
            StatusHomologacao.COM_EXIGENCIA.value,
        )

        self.assertEqual(
            submissao_inicial["status_analise"],
            "COM_EXIGENCIA",
        )

        self.assertEqual(
            exigencia_armazenada["status_atendimento"],
            "PENDENTE",
        )

        # ---------------------------------------------------------
        # 4. Criação da Complementação
        # ---------------------------------------------------------

        referencia = criar_referencia_documento(
            codigo_documento=1,
            numero_versao=1,
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
                exigencia["codigo"]
            ],
        )

        adicionar_submissao_homologacao(
            homologacao=self.homologacao_ativa,
            submissao=complementacao,
            data_movimentacao="2026-08-06",
            responsavel="Ana Lima",
        )

        self.assertEqual(
            self.homologacao_ativa["status"],
            StatusHomologacao.EM_CORRECAO.value,
        )

        self.assertEqual(
            complementacao["codigo_submissao_origem"],
            submissao_inicial["codigo"],
        )

        self.assertEqual(
            complementacao["codigo_resposta_origem"],
            resposta_exigencia["codigo"],
        )

        # ---------------------------------------------------------
        # 5. Preparação e envio da Complementação
        # ---------------------------------------------------------

        alterar_status_operacional_submissao(
            homologacao=self.homologacao_ativa,
            codigo_submissao=complementacao["codigo"],
            novo_status="PRONTA_PARA_ENVIO",
            data_movimentacao="2026-08-07",
            responsavel="Carlos Souza",
        )

        enviar_submissao_homologacao(
            homologacao=self.homologacao_ativa,
            codigo_submissao=complementacao["codigo"],
            canal_envio="PORTAL",
            data_envio="2026-08-08",
            responsavel_envio="Carlos Souza",
        )

        self.assertEqual(
            self.homologacao_ativa["status"],
            StatusHomologacao.REAPRESENTADA.value,
        )

        self.assertEqual(
            complementacao["status_operacional"],
            "ENVIADA",
        )

        self.assertEqual(
            exigencia_armazenada["status_atendimento"],
            "ATENDIDA",
        )

        self.assertEqual(
            exigencia_armazenada["codigo_submissao_atendimento"],
            complementacao["codigo"],
        )

        self.assertEqual(
            exigencia_armazenada["data_atendimento"],
            "2026-08-08",
        )

        # ---------------------------------------------------------
        # 6. Protocolação da Complementação
        # ---------------------------------------------------------

        protocolar_submissao_homologacao(
            homologacao=self.homologacao_ativa,
            codigo_submissao=complementacao["codigo"],
            protocolo="PROT-2026-002",
            data_protocolo="2026-08-09",
            responsavel="Ana Lima",
        )

        self.assertEqual(
            complementacao["status_operacional"],
            "PROTOCOLADA",
        )

        # ---------------------------------------------------------
        # 7. Nova análise da concessionária
        # ---------------------------------------------------------

        nova_analise = criar_dados_resposta_inicio_analise(
            codigo=1,
            numero_sequencial=1,
            data_resposta="2026-08-10",
            data_registro="2026-08-10",
            responsavel_registro="Ana Lima",
            descricao=(
                "Análise da Complementação iniciada."
            ),
        )

        adicionar_resposta_concessionaria(
            homologacao=self.homologacao_ativa,
            codigo_submissao=complementacao["codigo"],
            resposta=nova_analise,
        )

        self.assertEqual(
            self.homologacao_ativa["status"],
            StatusHomologacao.EM_ANALISE.value,
        )

        self.assertEqual(
            complementacao["status_analise"],
            "EM_ANALISE",
        )

        # ---------------------------------------------------------
        # 8. Aprovação final
        # ---------------------------------------------------------

        aprovacao = criar_dados_resposta_aprovacao(
            codigo=2,
            numero_sequencial=2,
            data_resposta="2026-08-11",
            data_registro="2026-08-11",
            responsavel_registro="Ana Lima",
            descricao="Projeto aprovado.",
            identificador_aprovacao="APR-2026-001",
        )

        adicionar_resposta_concessionaria(
            homologacao=self.homologacao_ativa,
            codigo_submissao=complementacao["codigo"],
            resposta=aprovacao,
        )

        self.assertEqual(
            complementacao["status_analise"],
            "APROVADA",
        )

        self.assertEqual(
            self.homologacao_ativa["status"],
            (
                StatusHomologacao
                .PARECER_DE_ACESSO_EMITIDO
                .value
            ),
        )

        # ---------------------------------------------------------
        # 9. Integridade histórica
        # ---------------------------------------------------------

        self.assertEqual(
            len(self.homologacao_ativa["submissoes"]),
            2,
        )

        self.assertEqual(
            len(submissao_inicial["respostas"]),
            2,
        )

        self.assertEqual(
            len(complementacao["respostas"]),
            2,
        )

        codigos_movimentacoes = [
            movimentacao["codigo"]
            for movimentacao
            in self.homologacao_ativa["movimentacoes"]
        ]

        codigos_esperados = list(
            range(
                1,
                len(codigos_movimentacoes) + 1,
            )
        )

        self.assertEqual(
            codigos_movimentacoes,
            codigos_esperados,
        )

    # ========================================================
    # OPERAÇÕES DE CAMPO — INSTALAÇÃO
    # ========================================================

    def _planejar_instalacao_valida(
        self,
    ):
        """
        Coloca a Homologação no estado correto
        e registra um planejamento válido.
        """

        self.homologacao_ativa["status"] = (
            StatusHomologacao
            .PARECER_DE_ACESSO_EMITIDO
            .value
        )

        registrar_planejamento_instalacao(
            homologacao=self.homologacao_ativa,
            data_prevista="2026-08-20",
            responsavel_planejamento="Ana Lima",
            equipe_responsavel="Equipe Técnica A",
            data_movimentacao="2026-08-10",
        )

    def test_iniciar_instalacao(
        self,
    ):
        """
        Deve registrar o início da Instalação
        e preservar o status geral da Homologação.
        """

        self._planejar_instalacao_valida()

        resultado = iniciar_instalacao(
            homologacao=self.homologacao_ativa,
            data_inicio="2026-08-20",
            responsavel_inicio="Carlos Souza",
            data_movimentacao="2026-08-20",
        )

        instalacao = resultado[
            "operacoes_campo"
        ]["instalacao"]

        self.assertEqual(
            instalacao["status"],
            "EM_EXECUCAO",
        )

        self.assertEqual(
            instalacao["data_inicio"],
            "2026-08-20",
        )

        self.assertEqual(
            resultado["status"],
            StatusHomologacao
            .AGUARDANDO_INSTALACAO
            .value,
        )

        self.assertEqual(
            resultado["responsavel_atual"],
            "Carlos Souza",
        )

        self.assertEqual(
            resultado["movimentacoes"][-1][
                "tipo_evento"
            ],
            "INSTALACAO_INICIADA",
        )

    def test_nao_deve_iniciar_sem_planejamento(
        self,
    ):
        """
        Não deve ser possível iniciar uma Instalação
        que ainda não foi planejada.
        """

        self.homologacao_ativa["status"] = (
            StatusHomologacao
            .AGUARDANDO_INSTALACAO
            .value
        )

        with self.assertRaisesRegex(
            ValueError,
            "não possui",
        ):
            iniciar_instalacao(
                homologacao=self.homologacao_ativa,
                data_inicio="2026-08-20",
                responsavel_inicio=(
                    "Carlos Souza"
                ),
                data_movimentacao="2026-08-20",
            )

    def test_nao_deve_iniciar_instalacao_duas_vezes(
        self,
    ):
        """
        Uma Instalação em execução não pode
        ser iniciada novamente.
        """

        self._planejar_instalacao_valida()

        iniciar_instalacao(
            homologacao=self.homologacao_ativa,
            data_inicio="2026-08-20",
            responsavel_inicio="Carlos Souza",
            data_movimentacao="2026-08-20",
        )

        with self.assertRaisesRegex(
            ValueError,
            "planejada",
        ):
            iniciar_instalacao(
                homologacao=self.homologacao_ativa,
                data_inicio="2026-08-21",
                responsavel_inicio=(
                    "Carlos Souza"
                ),
                data_movimentacao="2026-08-21",
            )

    def test_inicio_exige_status_aguardando_instalacao(
        self,
    ):
        """
        A operação deve exigir o status geral correto.
        """

        with self.assertRaisesRegex(
            ValueError,
            "aguardando",
        ):
            iniciar_instalacao(
                homologacao=self.homologacao_ativa,
                data_inicio="2026-08-20",
                responsavel_inicio=(
                    "Carlos Souza"
                ),
                data_movimentacao="2026-08-20",
            )

    def test_falha_no_inicio_nao_deve_alterar_instalacao(
        self,
    ):
        """
        Uma falha deve preservar integralmente
        a Homologação e a Instalação reais.
        """

        self._planejar_instalacao_valida()

        instalacao_antes = (
            self.homologacao_ativa[
                "operacoes_campo"
            ]["instalacao"].copy()
        )

        responsavel_antes = (
            self.homologacao_ativa[
                "responsavel_atual"
            ]
        )

        quantidade_movimentacoes_antes = len(
            self.homologacao_ativa[
                "movimentacoes"
            ]
        )

        with self.assertRaises(
            ValueError
        ):
            iniciar_instalacao(
                homologacao=self.homologacao_ativa,
                data_inicio="20/08/2026",
                responsavel_inicio=(
                    "Carlos Souza"
                ),
                data_movimentacao="2026-08-20",
            )

        self.assertEqual(
            self.homologacao_ativa[
                "operacoes_campo"
            ]["instalacao"],
            instalacao_antes,
        )

        self.assertEqual(
            self.homologacao_ativa[
                "responsavel_atual"
            ],
            responsavel_antes,
        )

        self.assertEqual(
            len(
                self.homologacao_ativa[
                    "movimentacoes"
                ]
            ),
            quantidade_movimentacoes_antes,
        )

    def _iniciar_instalacao_valida(
        self,
    ):
        """
        Planeja e inicia uma Instalação válida.
        """

        self._planejar_instalacao_valida()

        iniciar_instalacao(
            homologacao=self.homologacao_ativa,
            data_inicio="2026-08-20",
            responsavel_inicio="Carlos Souza",
            data_movimentacao="2026-08-20",
        )

    def test_concluir_instalacao(
        self,
    ):
        """
        Deve concluir a Instalação e avançar
        o status geral da Homologação.
        """

        self._iniciar_instalacao_valida()

        resultado = concluir_instalacao(
            homologacao=self.homologacao_ativa,
            data_conclusao="2026-08-22",
            responsavel_conclusao="Carlos Souza",
            data_movimentacao="2026-08-22",
            observacoes=(
                "Instalação concluída sem ocorrências."
            ),
        )

        instalacao = resultado[
            "operacoes_campo"
        ]["instalacao"]

        self.assertEqual(
            instalacao["status"],
            "CONCLUIDA",
        )

        self.assertEqual(
            instalacao["data_conclusao"],
            "2026-08-22",
        )

        self.assertEqual(
            resultado["status"],
            StatusHomologacao
            .INSTALACAO_CONCLUIDA
            .value,
        )

        self.assertEqual(
            resultado["responsavel_atual"],
            "Carlos Souza",
        )

        self.assertEqual(
            resultado["movimentacoes"][-1][
                "tipo_evento"
            ],
            "INSTALACAO_CONCLUIDA",
        )

    def test_nao_deve_concluir_sem_inicio(
        self,
    ):
        """
        Uma Instalação planejada, mas não iniciada,
        não pode ser concluída.
        """

        self._planejar_instalacao_valida()

        with self.assertRaisesRegex(
            ValueError,
            "em execução",
        ):
            concluir_instalacao(
                homologacao=self.homologacao_ativa,
                data_conclusao="2026-08-22",
                responsavel_conclusao=(
                    "Carlos Souza"
                ),
                data_movimentacao="2026-08-22",
            )

    def test_nao_deve_concluir_instalacao_duas_vezes(
        self,
    ):
        """
        Uma Instalação concluída não pode
        ser concluída novamente.
        """

        self._iniciar_instalacao_valida()

        concluir_instalacao(
            homologacao=self.homologacao_ativa,
            data_conclusao="2026-08-22",
            responsavel_conclusao="Carlos Souza",
            data_movimentacao="2026-08-22",
        )

        with self.assertRaises(
            ValueError
        ):
            concluir_instalacao(
                homologacao=self.homologacao_ativa,
                data_conclusao="2026-08-23",
                responsavel_conclusao=(
                    "Carlos Souza"
                ),
                data_movimentacao="2026-08-23",
            )

    def test_falha_na_conclusao_nao_deve_alterar_homologacao(
        self,
    ):
        """
        Uma falha deve preservar os dados reais
        da Instalação e da Homologação.
        """

        self._iniciar_instalacao_valida()

        instalacao_antes = (
            self.homologacao_ativa[
                "operacoes_campo"
            ]["instalacao"].copy()
        )

        status_antes = (
            self.homologacao_ativa["status"]
        )

        quantidade_movimentacoes_antes = len(
            self.homologacao_ativa[
                "movimentacoes"
            ]
        )

        with self.assertRaises(
            ValueError
        ):
            concluir_instalacao(
                homologacao=self.homologacao_ativa,
                data_conclusao="19/08/2026",
                responsavel_conclusao=(
                    "Carlos Souza"
                ),
                data_movimentacao="2026-08-22",
            )

        self.assertEqual(
            self.homologacao_ativa[
                "operacoes_campo"
            ]["instalacao"],
            instalacao_antes,
        )

        self.assertEqual(
            self.homologacao_ativa["status"],
            status_antes,
        )

        self.assertEqual(
            len(
                self.homologacao_ativa[
                    "movimentacoes"
                ]
            ),
            quantidade_movimentacoes_antes,
        )

    def test_registrar_planejamento_instalacao(
        self,
    ):
        """
        Deve registrar a Instalação, avançar o estado
        e criar a Movimentação correspondente.
        """

        self.homologacao_ativa["status"] = (
            StatusHomologacao
            .PARECER_DE_ACESSO_EMITIDO
            .value
        )

        resultado = registrar_planejamento_instalacao(
            homologacao=self.homologacao_ativa,
            data_prevista="2026-08-20",
            responsavel_planejamento="Ana Lima",
            equipe_responsavel="Equipe Técnica A",
            data_movimentacao="2026-08-10",
            observacoes="Instalação programada.",
        )

        self.assertIs(
            resultado,
            self.homologacao_ativa,
        )

        instalacao = resultado[
            "operacoes_campo"
        ]["instalacao"]

        self.assertEqual(
            instalacao["status"],
            "PLANEJADA",
        )

        self.assertEqual(
            instalacao["data_prevista"],
            "2026-08-20",
        )

        self.assertEqual(
            resultado["status"],
            StatusHomologacao
            .AGUARDANDO_INSTALACAO
            .value,
        )

        self.assertEqual(
            resultado["responsavel_atual"],
            "Ana Lima",
        )

        self.assertEqual(
            resultado["movimentacoes"][-1][
                "tipo_evento"
            ],
            "INSTALACAO_PLANEJADA",
        )

    def test_nao_deve_registrar_dois_planejamentos(
        self,
    ):
        """
        Uma Homologação não pode possuir
        duas Instalações principais.
        """

        self.homologacao_ativa["status"] = (
            StatusHomologacao
            .PARECER_DE_ACESSO_EMITIDO
            .value
        )

        registrar_planejamento_instalacao(
            homologacao=self.homologacao_ativa,
            data_prevista="2026-08-20",
            responsavel_planejamento="Ana Lima",
            equipe_responsavel="Equipe Técnica A",
            data_movimentacao="2026-08-10",
        )

        with self.assertRaisesRegex(
            ValueError,
            "já possui",
        ):
            registrar_planejamento_instalacao(
                homologacao=self.homologacao_ativa,
                data_prevista="2026-08-25",
                responsavel_planejamento=(
                    "Carlos Souza"
                ),
                equipe_responsavel=(
                    "Equipe Técnica B"
                ),
                data_movimentacao="2026-08-11",
            )

    def test_planejamento_exige_estado_compativel(
        self,
    ):
        """
        A Instalação não pode ser planejada antes
        da emissão do parecer de acesso.
        """

        self.assertEqual(
            self.homologacao_ativa["status"],
            StatusHomologacao
            .EM_PREPARACAO
            .value,
        )

        with self.assertRaisesRegex(
            ValueError,
            "após a emissão",
        ):
            registrar_planejamento_instalacao(
                homologacao=self.homologacao_ativa,
                data_prevista="2026-08-20",
                responsavel_planejamento=(
                    "Ana Lima"
                ),
                equipe_responsavel=(
                    "Equipe Técnica A"
                ),
                data_movimentacao="2026-08-10",
            )

    def test_planejamento_deve_normalizar_registro_antigo(
        self,
    ):
        """
        Uma Homologação antiga sem operacoes_campo
        deve receber a nova estrutura somente após
        a validação completa da operação.
        """

        self.homologacao_ativa.pop(
            "operacoes_campo",
            None,
        )

        self.homologacao_ativa["status"] = (
            StatusHomologacao
            .AGUARDANDO_INSTALACAO
            .value
        )

        registrar_planejamento_instalacao(
            homologacao=self.homologacao_ativa,
            data_prevista="2026-08-20",
            responsavel_planejamento="Ana Lima",
            equipe_responsavel="Equipe Técnica A",
            data_movimentacao="2026-08-10",
        )

        self.assertIn(
            "operacoes_campo",
            self.homologacao_ativa,
        )

        self.assertIsNotNone(
            self.homologacao_ativa[
                "operacoes_campo"
            ]["instalacao"]
        )

    def test_falha_no_planejamento_nao_deve_alterar_homologacao(
        self,
    ):
        """
        Uma falha de validação não deve aplicar
        alterações parciais à Homologação.
        """

        self.homologacao_ativa.pop(
            "operacoes_campo",
            None,
        )

        self.homologacao_ativa["status"] = (
            StatusHomologacao
            .PARECER_DE_ACESSO_EMITIDO
            .value
        )

        status_antes = (
            self.homologacao_ativa["status"]
        )

        responsavel_antes = (
            self.homologacao_ativa[
                "responsavel_atual"
            ]
        )

        quantidade_movimentacoes_antes = len(
            self.homologacao_ativa[
                "movimentacoes"
            ]
        )

        with self.assertRaises(
            ValueError
        ):
            registrar_planejamento_instalacao(
                homologacao=self.homologacao_ativa,
                data_prevista="20/08/2026",
                responsavel_planejamento=(
                    "Ana Lima"
                ),
                equipe_responsavel=(
                    "Equipe Técnica A"
                ),
                data_movimentacao="2026-08-10",
            )

        self.assertNotIn(
            "operacoes_campo",
            self.homologacao_ativa,
        )

        self.assertEqual(
            self.homologacao_ativa["status"],
            status_antes,
        )

        self.assertEqual(
            self.homologacao_ativa[
                "responsavel_atual"
            ],
            responsavel_antes,
        )

        self.assertEqual(
            len(
                self.homologacao_ativa[
                    "movimentacoes"
                ]
            ),
            quantidade_movimentacoes_antes,
        )

    # ========================================================
    # OPERAÇÕES DE CAMPO — VISTORIA
    # ========================================================

    def _preparar_instalacao_concluida(
        self,
    ):
        """
        Prepara uma Homologação com
        Instalação integralmente concluída.
        """

        self._iniciar_instalacao_valida()

        concluir_instalacao(
            homologacao=self.homologacao_ativa,
            data_conclusao="2026-08-22",
            responsavel_conclusao=(
                "Carlos Souza"
            ),
            data_movimentacao="2026-08-22",
        )

    def _solicitar_vistoria_valida(
        self,
    ):
        """
        Prepara a Instalação concluída e registra
        uma solicitação válida de Vistoria.
        """

        self._preparar_instalacao_concluida()

        solicitar_vistoria(
            homologacao=self.homologacao_ativa,
            data_solicitacao="2026-08-25",
            responsavel_solicitacao="Ana Lima",
            protocolo="VST-2026-001",
            data_movimentacao="2026-08-25",
        )

    def _agendar_vistoria_valida(
        self,
    ):
        """
        Solicita e agenda uma Vistoria válida.
        """

        self._solicitar_vistoria_valida()

        agendar_vistoria(
            homologacao=self.homologacao_ativa,
            codigo_vistoria=1,
            data_agendamento="2026-08-30",
            responsavel_agendamento=(
                "Carlos Souza"
            ),
            data_movimentacao="2026-08-26",
        )

    def _realizar_vistoria_valida(
        self,
    ):
        """
        Solicita, agenda e registra
        a realização de uma Vistoria válida.
        """

        self._agendar_vistoria_valida()

        registrar_realizacao_vistoria(
            homologacao=self.homologacao_ativa,
            codigo_vistoria=1,
            data_realizacao="2026-08-30",
            responsavel_realizacao=(
                "Marcos Oliveira"
            ),
            data_movimentacao="2026-08-30",
        )

    def _reprovar_vistoria_valida(
        self,
    ):
        """
        Prepara uma Vistoria completa
        e registra sua reprovação.
        """

        self._realizar_vistoria_valida()

        reprovar_vistoria(
            homologacao=self.homologacao_ativa,
            codigo_vistoria=1,
            data_resultado="2026-09-01",
            responsavel_resultado="Ana Lima",
            motivo_reprovacao=(
                "Inversor sem identificação."
            ),
            data_movimentacao="2026-09-01",
        )

    def test_solicitar_primeira_vistoria(
        self,
    ):
        """
        Deve criar a primeira Vistoria, atualizar
        o status e registrar uma Movimentação.
        """

        self._preparar_instalacao_concluida()

        resultado = solicitar_vistoria(
            homologacao=self.homologacao_ativa,
            data_solicitacao="2026-08-25",
            responsavel_solicitacao="Ana Lima",
            protocolo="VST-2026-001",
            data_movimentacao="2026-08-25",
            observacoes="Primeira vistoria.",
        )

        vistorias = resultado[
            "operacoes_campo"
        ]["vistorias"]

        self.assertEqual(
            len(vistorias),
            1,
        )

        vistoria = vistorias[0]

        self.assertEqual(
            vistoria["codigo"],
            1,
        )

        self.assertEqual(
            vistoria["numero_sequencial"],
            1,
        )

        self.assertEqual(
            vistoria["status"],
            StatusVistoria.SOLICITADA.value,
        )

        self.assertEqual(
            resultado["status"],
            StatusHomologacao
            .VISTORIA_SOLICITADA
            .value,
        )

        self.assertEqual(
            resultado["responsavel_atual"],
            "Ana Lima",
        )

        self.assertEqual(
            resultado["movimentacoes"][-1][
                "tipo_evento"
            ],
            "VISTORIA_SOLICITADA",
        )

    def test_solicitacao_vistoria_exige_instalacao_concluida(
        self,
    ):
        """
        Não deve ser possível solicitar Vistoria
        antes da conclusão da Instalação.
        """

        with self.assertRaisesRegex(
            ValueError,
            "após a conclusão",
        ):
            solicitar_vistoria(
                homologacao=self.homologacao_ativa,
                data_solicitacao="2026-08-25",
                responsavel_solicitacao=(
                    "Ana Lima"
                ),
                protocolo="VST-2026-001",
                data_movimentacao="2026-08-25",
            )

    def test_nao_deve_solicitar_duas_primeiras_vistorias(
        self,
    ):
        """
        Uma nova solicitação não pode ocorrer enquanto
        a tentativa atual ainda estiver aberta.
        """

        self._preparar_instalacao_concluida()

        solicitar_vistoria(
            homologacao=self.homologacao_ativa,
            data_solicitacao="2026-08-25",
            responsavel_solicitacao="Ana Lima",
            protocolo="VST-2026-001",
            data_movimentacao="2026-08-25",
        )

        with self.assertRaises(
            ValueError
        ):
            solicitar_vistoria(
                homologacao=self.homologacao_ativa,
                data_solicitacao="2026-08-26",
                responsavel_solicitacao=(
                    "Ana Lima"
                ),
                protocolo="VST-2026-002",
                data_movimentacao="2026-08-26",
            )

    def test_solicitacao_deve_normalizar_registro_antigo(
        self,
    ):
        """
        Uma Homologação antiga sem operacoes_campo
        deve receber a estrutura somente depois
        da validação completa.
        """

        self.homologacao_ativa.pop(
            "operacoes_campo",
            None,
        )

        self.homologacao_ativa["status"] = (
            StatusHomologacao
            .INSTALACAO_CONCLUIDA
            .value
        )

        solicitar_vistoria(
            homologacao=self.homologacao_ativa,
            data_solicitacao="2026-08-25",
            responsavel_solicitacao="Ana Lima",
            protocolo="VST-2026-001",
            data_movimentacao="2026-08-25",
        )

        self.assertIn(
            "operacoes_campo",
            self.homologacao_ativa,
        )

        self.assertEqual(
            len(
                self.homologacao_ativa[
                    "operacoes_campo"
                ]["vistorias"]
            ),
            1,
        )

    def test_falha_na_solicitacao_nao_deve_alterar_homologacao(
        self,
    ):
        """
        Uma falha na criação da Vistoria não deve
        aplicar alterações parciais à Homologação.
        """

        self._preparar_instalacao_concluida()

        status_antes = (
            self.homologacao_ativa["status"]
        )

        responsavel_antes = (
            self.homologacao_ativa[
                "responsavel_atual"
            ]
        )

        quantidade_vistorias_antes = len(
            self.homologacao_ativa[
                "operacoes_campo"
            ]["vistorias"]
        )

        quantidade_movimentacoes_antes = len(
            self.homologacao_ativa[
                "movimentacoes"
            ]
        )

        with self.assertRaises(
            ValueError
        ):
            solicitar_vistoria(
                homologacao=self.homologacao_ativa,
                data_solicitacao="25/08/2026",
                responsavel_solicitacao=(
                    "Ana Lima"
                ),
                protocolo="VST-2026-001",
                data_movimentacao="2026-08-25",
            )

        self.assertEqual(
            self.homologacao_ativa["status"],
            status_antes,
        )

        self.assertEqual(
            self.homologacao_ativa[
                "responsavel_atual"
            ],
            responsavel_antes,
        )

        self.assertEqual(
            len(
                self.homologacao_ativa[
                    "operacoes_campo"
                ]["vistorias"]
            ),
            quantidade_vistorias_antes,
        )

        self.assertEqual(
            len(
                self.homologacao_ativa[
                    "movimentacoes"
                ]
            ),
            quantidade_movimentacoes_antes,
        )

    def _solicitar_vistoria_valida(
        self,
    ):
        """
        Prepara a Instalação concluída e registra
        uma solicitação válida de Vistoria.
        """

        self._preparar_instalacao_concluida()

        solicitar_vistoria(
            homologacao=self.homologacao_ativa,
            data_solicitacao="2026-08-25",
            responsavel_solicitacao="Ana Lima",
            protocolo="VST-2026-001",
            data_movimentacao="2026-08-25",
        )

    def test_agendamento_exige_vistoria_existente(
        self,
    ):
        """
        O agendamento deve exigir uma Vistoria
        existente na Homologação.
        """

        self._solicitar_vistoria_valida()

        with self.assertRaisesRegex(
            ValueError,
            "não encontrada",
        ):
            agendar_vistoria(
                homologacao=self.homologacao_ativa,
                codigo_vistoria=999,
                data_agendamento="2026-08-30",
                responsavel_agendamento=(
                    "Carlos Souza"
                ),
                data_movimentacao="2026-08-26",
            )

    def test_agendamento_exige_status_vistoria_solicitada(
        self,
    ):
        """
        A Homologação deve possuir uma solicitação
        de Vistoria aberta.
        """

        with self.assertRaisesRegex(
            ValueError,
            "solicitação",
        ):
            agendar_vistoria(
                homologacao=self.homologacao_ativa,
                codigo_vistoria=1,
                data_agendamento="2026-08-30",
                responsavel_agendamento=(
                    "Carlos Souza"
                ),
                data_movimentacao="2026-08-26",
            )

    def test_nao_deve_agendar_vistoria_duas_vezes(
        self,
    ):
        """
        Uma Vistoria agendada não pode
        ser agendada novamente.
        """

        self._solicitar_vistoria_valida()

        agendar_vistoria(
            homologacao=self.homologacao_ativa,
            codigo_vistoria=1,
            data_agendamento="2026-08-30",
            responsavel_agendamento=(
                "Carlos Souza"
            ),
            data_movimentacao="2026-08-26",
        )

        with self.assertRaises(
            ValueError
        ):
            agendar_vistoria(
                homologacao=self.homologacao_ativa,
                codigo_vistoria=1,
                data_agendamento="2026-08-31",
                responsavel_agendamento=(
                    "Carlos Souza"
                ),
                data_movimentacao="2026-08-27",
            )

    def test_falha_no_agendamento_nao_deve_alterar_homologacao(
        self,
    ):
        """
        Uma falha no agendamento deve preservar
        os dados reais da Vistoria e da Homologação.
        """

        self._solicitar_vistoria_valida()

        vistoria_antes = (
            self.homologacao_ativa[
                "operacoes_campo"
            ]["vistorias"][0].copy()
        )

        status_antes = (
            self.homologacao_ativa["status"]
        )

        responsavel_antes = (
            self.homologacao_ativa[
                "responsavel_atual"
            ]
        )

        quantidade_movimentacoes_antes = len(
            self.homologacao_ativa[
                "movimentacoes"
            ]
        )

        with self.assertRaises(
            ValueError
        ):
            agendar_vistoria(
                homologacao=self.homologacao_ativa,
                codigo_vistoria=1,
                data_agendamento="24/08/2026",
                responsavel_agendamento=(
                    "Carlos Souza"
                ),
                data_movimentacao="2026-08-26",
            )

        self.assertEqual(
            self.homologacao_ativa[
                "operacoes_campo"
            ]["vistorias"][0],
            vistoria_antes,
        )

        self.assertEqual(
            self.homologacao_ativa["status"],
            status_antes,
        )

        self.assertEqual(
            self.homologacao_ativa[
                "responsavel_atual"
            ],
            responsavel_antes,
        )

        self.assertEqual(
            len(
                self.homologacao_ativa[
                    "movimentacoes"
                ]
            ),
            quantidade_movimentacoes_antes,
        )

    def test_registrar_realizacao_vistoria(
        self,
    ):
        """
        Deve registrar a realização da Vistoria
        sem alterar o status geral da Homologação.
        """

        self._agendar_vistoria_valida()

        resultado = registrar_realizacao_vistoria(
            homologacao=self.homologacao_ativa,
            codigo_vistoria=1,
            data_realizacao="2026-08-30",
            responsavel_realizacao=(
                "Marcos Oliveira"
            ),
            data_movimentacao="2026-08-30",
            observacoes=(
                "Vistoria realizada no local."
            ),
        )

        vistoria = resultado[
            "operacoes_campo"
        ]["vistorias"][0]

        self.assertEqual(
            vistoria["status"],
            StatusVistoria.REALIZADA.value,
        )

        self.assertEqual(
            vistoria["data_realizacao"],
            "2026-08-30",
        )

        self.assertEqual(
            resultado["status"],
            StatusHomologacao
            .AGUARDANDO_VISTORIA
            .value,
        )

        self.assertEqual(
            resultado["responsavel_atual"],
            "Marcos Oliveira",
        )

        self.assertEqual(
            resultado["movimentacoes"][-1][
                "tipo_evento"
            ],
            "VISTORIA_REALIZADA",
        )

    def test_realizacao_exige_vistoria_existente(
        self,
    ):
        """
        A realização deve exigir uma Vistoria
        existente.
        """

        self._agendar_vistoria_valida()

        with self.assertRaisesRegex(
            ValueError,
            "não encontrada",
        ):
            registrar_realizacao_vistoria(
                homologacao=self.homologacao_ativa,
                codigo_vistoria=999,
                data_realizacao="2026-08-30",
                responsavel_realizacao=(
                    "Marcos Oliveira"
                ),
                data_movimentacao="2026-08-30",
            )

    def test_realizacao_exige_status_aguardando_vistoria(
        self,
    ):
        """
        A Homologação deve estar aguardando
        a realização da Vistoria.
        """

        with self.assertRaisesRegex(
            ValueError,
            "aguardando",
        ):
            registrar_realizacao_vistoria(
                homologacao=self.homologacao_ativa,
                codigo_vistoria=1,
                data_realizacao="2026-08-30",
                responsavel_realizacao=(
                    "Marcos Oliveira"
                ),
                data_movimentacao="2026-08-30",
            )

    def test_nao_deve_realizar_vistoria_duas_vezes(
        self,
    ):
        """
        Uma Vistoria já realizada não pode
        receber nova realização.
        """

        self._agendar_vistoria_valida()

        registrar_realizacao_vistoria(
            homologacao=self.homologacao_ativa,
            codigo_vistoria=1,
            data_realizacao="2026-08-30",
            responsavel_realizacao=(
                "Marcos Oliveira"
            ),
            data_movimentacao="2026-08-30",
        )

        with self.assertRaisesRegex(
            ValueError,
            "agendada",
        ):
            registrar_realizacao_vistoria(
                homologacao=self.homologacao_ativa,
                codigo_vistoria=1,
                data_realizacao="2026-08-31",
                responsavel_realizacao=(
                    "Marcos Oliveira"
                ),
                data_movimentacao="2026-08-31",
            )

    def test_falha_na_realizacao_nao_deve_alterar_homologacao(
        self,
    ):
        """
        Uma falha na realização deve preservar
        a Vistoria e a Homologação reais.
        """

        self._agendar_vistoria_valida()

        vistoria_antes = (
            self.homologacao_ativa[
                "operacoes_campo"
            ]["vistorias"][0].copy()
        )

        responsavel_antes = (
            self.homologacao_ativa[
                "responsavel_atual"
            ]
        )

        quantidade_movimentacoes_antes = len(
            self.homologacao_ativa[
                "movimentacoes"
            ]
        )

        with self.assertRaises(
            ValueError
        ):
            registrar_realizacao_vistoria(
                homologacao=self.homologacao_ativa,
                codigo_vistoria=1,
                data_realizacao="29/08/2026",
                responsavel_realizacao=(
                    "Marcos Oliveira"
                ),
                data_movimentacao="2026-08-30",
            )

        self.assertEqual(
            self.homologacao_ativa[
                "operacoes_campo"
            ]["vistorias"][0],
            vistoria_antes,
        )

        self.assertEqual(
            self.homologacao_ativa[
                "responsavel_atual"
            ],
            responsavel_antes,
        )

        self.assertEqual(
            len(
                self.homologacao_ativa[
                    "movimentacoes"
                ]
            ),
            quantidade_movimentacoes_antes,
        )

    def test_aprovar_vistoria(
        self,
    ):
        """
        Deve aprovar a Vistoria e atualizar
        o estado geral da Homologação.
        """

        self._realizar_vistoria_valida()

        resultado = aprovar_vistoria(
            homologacao=self.homologacao_ativa,
            codigo_vistoria=1,
            data_resultado="2026-09-01",
            responsavel_resultado="Ana Lima",
            data_movimentacao="2026-09-01",
            observacoes="Vistoria aprovada.",
        )

        vistoria = resultado[
            "operacoes_campo"
        ]["vistorias"][0]

        self.assertEqual(
            vistoria["status"],
            StatusVistoria.APROVADA.value,
        )

        self.assertEqual(
            vistoria["resultado"],
            "APROVADA",
        )

        self.assertEqual(
            resultado["status"],
            StatusHomologacao
            .VISTORIA_APROVADA
            .value,
        )

        self.assertEqual(
            resultado["responsavel_atual"],
            "Ana Lima",
        )

        self.assertEqual(
            resultado["movimentacoes"][-1][
                "tipo_evento"
            ],
            "VISTORIA_APROVADA",
        )

    def test_reprovar_vistoria(
        self,
    ):
        """
        Deve reprovar a Vistoria, registrar
        o motivo e atualizar a Homologação.
        """

        self._realizar_vistoria_valida()

        resultado = reprovar_vistoria(
            homologacao=self.homologacao_ativa,
            codigo_vistoria=1,
            data_resultado="2026-09-01",
            responsavel_resultado="Ana Lima",
            motivo_reprovacao=(
                "Inversor sem identificação."
            ),
            data_movimentacao="2026-09-01",
        )

        vistoria = resultado[
            "operacoes_campo"
        ]["vistorias"][0]

        self.assertEqual(
            vistoria["status"],
            StatusVistoria.REPROVADA.value,
        )

        self.assertEqual(
            vistoria["resultado"],
            "REPROVADA",
        )

        self.assertEqual(
            vistoria["motivo_reprovacao"],
            "Inversor sem identificação.",
        )

        self.assertEqual(
            resultado["status"],
            StatusHomologacao
            .VISTORIA_REPROVADA
            .value,
        )

        self.assertEqual(
            resultado["movimentacoes"][-1][
                "tipo_evento"
            ],
            "VISTORIA_REPROVADA",
        )

    def test_resultado_exige_vistoria_existente(
        self,
    ):
        """
        O resultado deve exigir uma Vistoria
        existente na Homologação.
        """

        self._realizar_vistoria_valida()

        with self.assertRaisesRegex(
            ValueError,
            "não encontrada",
        ):
            aprovar_vistoria(
                homologacao=self.homologacao_ativa,
                codigo_vistoria=999,
                data_resultado="2026-09-01",
                responsavel_resultado="Ana Lima",
                data_movimentacao="2026-09-01",
            )

    def test_aprovacao_exige_vistoria_realizada(
        self,
    ):
        """
        Uma Vistoria apenas agendada
        não pode ser aprovada.
        """

        self._agendar_vistoria_valida()

        with self.assertRaisesRegex(
            ValueError,
            "realizada",
        ):
            aprovar_vistoria(
                homologacao=self.homologacao_ativa,
                codigo_vistoria=1,
                data_resultado="2026-09-01",
                responsavel_resultado="Ana Lima",
                data_movimentacao="2026-09-01",
            )

    def test_nao_deve_registrar_resultado_duas_vezes(
        self,
    ):
        """
        Uma Vistoria já aprovada não pode
        receber outro resultado.
        """

        self._realizar_vistoria_valida()

        aprovar_vistoria(
            homologacao=self.homologacao_ativa,
            codigo_vistoria=1,
            data_resultado="2026-09-01",
            responsavel_resultado="Ana Lima",
            data_movimentacao="2026-09-01",
        )

        with self.assertRaises(
            ValueError
        ):
            reprovar_vistoria(
                homologacao=self.homologacao_ativa,
                codigo_vistoria=1,
                data_resultado="2026-09-02",
                responsavel_resultado="Ana Lima",
                motivo_reprovacao="Novo motivo.",
                data_movimentacao="2026-09-02",
            )

    def test_falha_na_aprovacao_nao_deve_alterar_homologacao(
        self,
    ):
        """
        Uma falha na aprovação deve preservar
        a Vistoria e a Homologação reais.
        """

        self._realizar_vistoria_valida()

        vistoria_antes = (
            self.homologacao_ativa[
                "operacoes_campo"
            ]["vistorias"][0].copy()
        )

        status_antes = (
            self.homologacao_ativa["status"]
        )

        quantidade_movimentacoes_antes = len(
            self.homologacao_ativa[
                "movimentacoes"
            ]
        )

        with self.assertRaises(
            ValueError
        ):
            aprovar_vistoria(
                homologacao=self.homologacao_ativa,
                codigo_vistoria=1,
                data_resultado="29/08/2026",
                responsavel_resultado="Ana Lima",
                data_movimentacao="2026-09-01",
            )

        self.assertEqual(
            self.homologacao_ativa[
                "operacoes_campo"
            ]["vistorias"][0],
            vistoria_antes,
        )

        self.assertEqual(
            self.homologacao_ativa["status"],
            status_antes,
        )

        self.assertEqual(
            len(
                self.homologacao_ativa[
                    "movimentacoes"
                ]
            ),
            quantidade_movimentacoes_antes,
        )

    def test_falha_na_reprovacao_nao_deve_alterar_homologacao(
        self,
    ):
        """
        Uma reprovação inválida deve preservar
        integralmente a Homologação.
        """

        self._realizar_vistoria_valida()

        vistoria_antes = (
            self.homologacao_ativa[
                "operacoes_campo"
            ]["vistorias"][0].copy()
        )

        status_antes = (
            self.homologacao_ativa["status"]
        )

        quantidade_movimentacoes_antes = len(
            self.homologacao_ativa[
                "movimentacoes"
            ]
        )

        with self.assertRaises(
            ValueError
        ):
            reprovar_vistoria(
                homologacao=self.homologacao_ativa,
                codigo_vistoria=1,
                data_resultado="2026-09-01",
                responsavel_resultado="Ana Lima",
                motivo_reprovacao=" ",
                data_movimentacao="2026-09-01",
            )

        self.assertEqual(
            self.homologacao_ativa[
                "operacoes_campo"
            ]["vistorias"][0],
            vistoria_antes,
        )

        self.assertEqual(
            self.homologacao_ativa["status"],
            status_antes,
        )

        self.assertEqual(
            len(
                self.homologacao_ativa[
                    "movimentacoes"
                ]
            ),
            quantidade_movimentacoes_antes,
        )

    def test_registrar_correcao_pos_vistoria(
        self,
    ):
        """
        Deve registrar a correção sem alterar
        a Vistoria reprovada.
        """

        self._reprovar_vistoria_valida()

        vistoria_antes = (
            self.homologacao_ativa[
                "operacoes_campo"
            ]["vistorias"][0].copy()
        )

        resultado = (
            registrar_correcao_pos_vistoria(
                homologacao=self.homologacao_ativa,
                codigo_vistoria=1,
                descricao_correcao=(
                    "Identificação do inversor instalada."
                ),
                responsavel_correcao=(
                    "Carlos Souza"
                ),
                data_movimentacao="2026-09-03",
            )
        )

        self.assertEqual(
            resultado["status"],
            StatusHomologacao
            .CORRECAO_POS_VISTORIA
            .value,
        )

        self.assertEqual(
            resultado[
                "operacoes_campo"
            ]["vistorias"][0],
            vistoria_antes,
        )

        self.assertEqual(
            resultado["movimentacoes"][-1][
                "tipo_evento"
            ],
            "CORRECAO_POS_VISTORIA",
        )

    def test_correcao_exige_vistoria_reprovada(
        self,
    ):
        """
        A correção não pode ser registrada
        sem uma reprovação anterior.
        """

        with self.assertRaisesRegex(
            ValueError,
            "reprovada",
        ):
            registrar_correcao_pos_vistoria(
                homologacao=self.homologacao_ativa,
                codigo_vistoria=1,
                descricao_correcao=(
                    "Correção executada."
                ),
                responsavel_correcao=(
                    "Carlos Souza"
                ),
                data_movimentacao="2026-09-03",
            )

    def test_falha_na_correcao_nao_deve_alterar_homologacao(
        self,
    ):
        """
        Uma correção inválida deve preservar
        integralmente a Homologação.
        """

        self._reprovar_vistoria_valida()

        status_antes = (
            self.homologacao_ativa["status"]
        )

        quantidade_movimentacoes_antes = len(
            self.homologacao_ativa[
                "movimentacoes"
            ]
        )

        with self.assertRaises(
            ValueError
        ):
            registrar_correcao_pos_vistoria(
                homologacao=self.homologacao_ativa,
                codigo_vistoria=1,
                descricao_correcao=" ",
                responsavel_correcao=(
                    "Carlos Souza"
                ),
                data_movimentacao="2026-09-03",
            )

        self.assertEqual(
            self.homologacao_ativa["status"],
            status_antes,
        )

        self.assertEqual(
            len(
                self.homologacao_ativa[
                    "movimentacoes"
                ]
            ),
            quantidade_movimentacoes_antes,
        )

    def test_deve_criar_segunda_vistoria_apos_correcao(
        self,
    ):
        """
        Após reprovação e correção, uma nova solicitação
        deve criar uma segunda Vistoria sem alterar
        a primeira.
        """

        self._reprovar_vistoria_valida()

        registrar_correcao_pos_vistoria(
            homologacao=self.homologacao_ativa,
            codigo_vistoria=1,
            descricao_correcao=(
                "Identificação do inversor instalada."
            ),
            responsavel_correcao="Carlos Souza",
            data_movimentacao="2026-09-03",
        )

        primeira_vistoria_antes = (
            self.homologacao_ativa[
                "operacoes_campo"
            ]["vistorias"][0].copy()
        )

        solicitar_vistoria(
            homologacao=self.homologacao_ativa,
            data_solicitacao="2026-09-05",
            responsavel_solicitacao="Ana Lima",
            protocolo="VST-2026-002",
            data_movimentacao="2026-09-05",
            observacoes="Segunda tentativa.",
        )

        vistorias = self.homologacao_ativa[
            "operacoes_campo"
        ]["vistorias"]

        self.assertEqual(
            len(vistorias),
            2,
        )

        self.assertEqual(
            vistorias[0],
            primeira_vistoria_antes,
        )

        self.assertEqual(
            vistorias[0]["status"],
            StatusVistoria.REPROVADA.value,
        )

        self.assertEqual(
            vistorias[1]["codigo"],
            2,
        )

        self.assertEqual(
            vistorias[1]["numero_sequencial"],
            2,
        )

        self.assertEqual(
            vistorias[1]["status"],
            StatusVistoria.SOLICITADA.value,
        )

        self.assertEqual(
            self.homologacao_ativa["status"],
            StatusHomologacao
            .VISTORIA_SOLICITADA
            .value,
        )

if __name__ == "__main__":
    unittest.main()