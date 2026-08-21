import unittest
from dataclasses import FrozenInstanceError
from datetime import date, time

from app.dominio.contratacoes_servico import (
    ContratacaoServico,
    SnapshotContratacaoServico,
)

from app.dominio.erros_dominio import (
    ValorInvalido,
)

from app.dominio.ordens_servico_pos_venda import (
    RESULTADOS_EXECUCAO,
    ExecucaoOrdemServico,
    OrdemServicoPosVenda,
    alterar_status_ordem_servico,
    buscar_ordem_servico_por_codigo,
    confirmar_conclusao_ordem_servico,
    contestar_conclusao_ordem_servico,
    criar_execucao_ordem_servico,
    criar_ordem_servico_pos_venda,
    listar_ordens_por_cliente,
    listar_ordens_por_contratacao,
    listar_ordens_por_empresa,
    listar_ordens_por_status,
    listar_ordens_por_tipo_servico,
    registrar_execucao_ordem_servico,
    resolver_contestacao_ordem_servico,
)

from app.dominio.status_ordem_servico import (
    STATUS_INICIAL,
)

class TestOrdensServicoPosVenda(
    unittest.TestCase
):
    """
    Testes do núcleo da Ordem de Serviço
    Pós-venda.
    """

    def criar_contratacao_valida(self):
        snapshot = SnapshotContratacaoServico(
            numero_versao_proposta=1,
            valor_contratado=1000.0,
            prazo_execucao_dias=10,
            descricao_tecnica=(
                "Serviço contratado"
            ),
            itens_incluidos=(
                "Item 1",
            ),
            itens_nao_incluidos=(),
            garantias={},
            condicoes_comerciais={},
            observacoes=None,
        )

        return ContratacaoServico(
            codigo=10,
            codigo_solicitacao=20,
            codigo_cliente=30,
            codigo_tipo_servico=40,
            codigo_empresa=50,
            codigo_servico_ofertado_empresa=60,
            codigo_proposta=70,
            snapshot=snapshot,
            data_limite_formalizacao=date(
                2026,
                12,
                31,
            ),
            processo_operacional=None,
            status="CONFIRMADA",
        )

    def criar_execucao_valida(
        self,
        numero=1,
        resultado="RESOLVIDO",
    ):
        return criar_execucao_ordem_servico(
            numero=numero,
            data_execucao=date(
                2026,
                8,
                20,
            ),
            responsaveis=(
                "Técnico 1",
                "Técnico 2",
            ),
            hora_inicio=time(
                9,
                0,
            ),
            hora_fim=time(
                11,
                30,
            ),
            descricao_executada=(
                "Inspeção e manutenção"
            ),
            diagnostico=(
                "Conector com mau contato"
            ),
            solucao_aplicada=(
                "Conector substituído"
            ),
            materiais_utilizados=(
                "Conector MC4",
            ),
            observacoes=(
                "Sistema normalizado"
            ),
            resultado=resultado,
        )

    def criar_ordem_em_execucao(self):
        ordem = criar_ordem_servico_pos_venda(
            1,
            self.criar_contratacao_valida(),
            "Atendimento técnico",
        )

        alterar_status_ordem_servico(
            ordem,
            "EM_TRIAGEM",
        )

        alterar_status_ordem_servico(
            ordem,
            "AGUARDANDO_AGENDAMENTO",
        )

        alterar_status_ordem_servico(
            ordem,
            "AGENDADA",
        )

        alterar_status_ordem_servico(
            ordem,
            "EM_EXECUCAO",
        )

        return ordem

    def criar_ordens_para_consulta(self):
        contratacao_1 = (
            self.criar_contratacao_valida()
        )

        contratacao_2 = (
            self.criar_contratacao_valida()
        )

        contratacao_2.codigo = 11
        contratacao_2.codigo_cliente = 31
        contratacao_2.codigo_empresa = 51
        contratacao_2.codigo_tipo_servico = 41

        ordem_1 = criar_ordem_servico_pos_venda(
            1,
            contratacao_1,
            "Primeira ordem",
        )

        ordem_2 = criar_ordem_servico_pos_venda(
            2,
            contratacao_1,
            "Segunda ordem",
        )

        ordem_3 = criar_ordem_servico_pos_venda(
            3,
            contratacao_2,
            "Terceira ordem",
        )

        alterar_status_ordem_servico(
            ordem_2,
            "EM_TRIAGEM",
        )

        alterar_status_ordem_servico(
            ordem_3,
            "EM_TRIAGEM",
        )

        return (
            ordem_1,
            ordem_2,
            ordem_3,
        )

    def test_criar_ordem_servico_pos_venda(
        self,
    ):
        contratacao = (
            self.criar_contratacao_valida()
        )

        ordem = criar_ordem_servico_pos_venda(
            1,
            contratacao,
            "Inspeção do sistema fotovoltaico",
        )

        self.assertIsInstance(
            ordem,
            OrdemServicoPosVenda,
        )

        self.assertEqual(
            ordem.codigo,
            1,
        )

        self.assertEqual(
            ordem.status,
            STATUS_INICIAL,
        )

    def test_ordem_inicia_aberta(
        self,
    ):
        ordem = criar_ordem_servico_pos_venda(
            1,
            self.criar_contratacao_valida(),
            "Atendimento técnico",
        )

        self.assertEqual(
            ordem.status,
            "ABERTA",
        )

    def test_ordem_preserva_codigo_contratacao(
        self,
    ):
        ordem = criar_ordem_servico_pos_venda(
            1,
            self.criar_contratacao_valida(),
            "Atendimento técnico",
        )

        self.assertEqual(
            ordem.codigo_contratacao,
            10,
        )

    def test_ordem_preserva_cliente(
        self,
    ):
        ordem = criar_ordem_servico_pos_venda(
            1,
            self.criar_contratacao_valida(),
            "Atendimento técnico",
        )

        self.assertEqual(
            ordem.codigo_cliente,
            30,
        )

    def test_ordem_preserva_empresa(
        self,
    ):
        ordem = criar_ordem_servico_pos_venda(
            1,
            self.criar_contratacao_valida(),
            "Atendimento técnico",
        )

        self.assertEqual(
            ordem.codigo_empresa,
            50,
        )

    def test_ordem_preserva_tipo_servico(
        self,
    ):
        ordem = criar_ordem_servico_pos_venda(
            1,
            self.criar_contratacao_valida(),
            "Atendimento técnico",
        )

        self.assertEqual(
            ordem.codigo_tipo_servico,
            40,
        )

    def test_descricao_e_normalizada(
        self,
    ):
        ordem = criar_ordem_servico_pos_venda(
            1,
            self.criar_contratacao_valida(),
            "  Atendimento técnico  ",
        )

        self.assertEqual(
            ordem.descricao,
            "Atendimento técnico",
        )

    def test_rejeita_codigo_invalido(
        self,
    ):
        contratacao = (
            self.criar_contratacao_valida()
        )

        for codigo in (
            0,
            -1,
            True,
            "1",
            None,
        ):
            with self.subTest(
                codigo=codigo
            ):
                with self.assertRaises(
                    ValorInvalido
                ):
                    criar_ordem_servico_pos_venda(
                        codigo,
                        contratacao,
                        "Atendimento técnico",
                    )

    def test_rejeita_contratacao_invalida(
        self,
    ):
        with self.assertRaises(
            TypeError
        ):
            criar_ordem_servico_pos_venda(
                1,
                object(),
                "Atendimento técnico",
            )

    def test_rejeita_descricao_nao_textual(
        self,
    ):
        with self.assertRaises(
            ValorInvalido
        ):
            criar_ordem_servico_pos_venda(
                1,
                self.criar_contratacao_valida(),
                123,
            )

    def test_rejeita_descricao_vazia(
        self,
    ):
        contratacao = (
            self.criar_contratacao_valida()
        )

        for descricao in (
            "",
            "   ",
        ):
            with self.subTest(
                descricao=descricao
            ):
                with self.assertRaises(
                    ValorInvalido
                ):
                    criar_ordem_servico_pos_venda(
                        1,
                        contratacao,
                        descricao,
                    )

    def test_ordem_inicia_sem_execucoes(
        self,
    ):
        ordem = criar_ordem_servico_pos_venda(
            1,
            self.criar_contratacao_valida(),
            "Atendimento técnico",
        )

        self.assertEqual(
            ordem.execucoes,
            (),
        )

    def test_criar_execucao_ordem_servico(
        self,
    ):
        execucao = (
            self.criar_execucao_valida()
        )

        self.assertIsInstance(
            execucao,
            ExecucaoOrdemServico,
        )

        self.assertEqual(
            execucao.numero,
            1,
        )

        self.assertEqual(
            execucao.resultado,
            "RESOLVIDO",
        )

    def test_execucao_normaliza_dados_textuais(
        self,
    ):
        execucao = criar_execucao_ordem_servico(
            numero=1,
            data_execucao=date(2026, 8, 20),
            responsaveis=(
                "  Técnico 1  ",
            ),
            hora_inicio=time(9, 0),
            hora_fim=time(10, 0),
            descricao_executada=(
                "  Inspeção  "
            ),
            diagnostico="  Falha  ",
            solucao_aplicada="  Ajuste  ",
            materiais_utilizados=(
                "  Conector  ",
            ),
            observacoes="  OK  ",
            resultado="  resolvido  ",
        )

        self.assertEqual(
            execucao.responsaveis,
            ("Técnico 1",),
        )

        self.assertEqual(
            execucao.descricao_executada,
            "Inspeção",
        )

        self.assertEqual(
            execucao.diagnostico,
            "Falha",
        )

        self.assertEqual(
            execucao.solucao_aplicada,
            "Ajuste",
        )

        self.assertEqual(
            execucao.materiais_utilizados,
            ("Conector",),
        )

        self.assertEqual(
            execucao.observacoes,
            "OK",
        )

        self.assertEqual(
            execucao.resultado,
            "RESOLVIDO",
        )

    def test_execucao_permite_campos_opcionais_ausentes(
        self,
    ):
        execucao = criar_execucao_ordem_servico(
            numero=1,
            data_execucao=date(2026, 8, 20),
            responsaveis=("Técnico",),
            hora_inicio=time(9, 0),
            hora_fim=time(10, 0),
            descricao_executada="Inspeção",
            resultado="NAO_RESOLVIDO",
        )

        self.assertIsNone(
            execucao.diagnostico
        )

        self.assertIsNone(
            execucao.solucao_aplicada
        )

        self.assertEqual(
            execucao.materiais_utilizados,
            (),
        )

        self.assertIsNone(
            execucao.observacoes
        )

    def test_resultados_execucao_sao_aceitos(
        self,
    ):
        for resultado in RESULTADOS_EXECUCAO:
            with self.subTest(
                resultado=resultado
            ):
                execucao = (
                    self.criar_execucao_valida(
                        resultado=resultado
                    )
                )

                self.assertEqual(
                    execucao.resultado,
                    resultado,
                )

    def test_rejeita_resultado_execucao_invalido(
        self,
    ):
        for resultado in (
            "",
            "DESCONHECIDO",
            None,
            1,
        ):
            with self.subTest(
                resultado=resultado
            ):
                with self.assertRaises(
                    ValorInvalido
                ):
                    self.criar_execucao_valida(
                        resultado=resultado
                    )

    def test_rejeita_execucao_sem_responsavel(
        self,
    ):
        with self.assertRaises(
            ValorInvalido
        ):
            criar_execucao_ordem_servico(
                numero=1,
                data_execucao=date(2026, 8, 20),
                responsaveis=(),
                hora_inicio=time(9, 0),
                hora_fim=time(10, 0),
                descricao_executada="Inspeção",
                resultado="RESOLVIDO",
            )

    def test_rejeita_horario_final_nao_posterior(
        self,
    ):
        for hora_fim in (
            time(9, 0),
            time(8, 59),
        ):
            with self.subTest(
                hora_fim=hora_fim
            ):
                with self.assertRaises(
                    ValorInvalido
                ):
                    criar_execucao_ordem_servico(
                        numero=1,
                        data_execucao=date(
                            2026,
                            8,
                            20,
                        ),
                        responsaveis=(
                            "Técnico",
                        ),
                        hora_inicio=time(9, 0),
                        hora_fim=hora_fim,
                        descricao_executada=(
                            "Inspeção"
                        ),
                        resultado="RESOLVIDO",
                    )

    def test_execucao_e_imutavel(
        self,
    ):
        execucao = (
            self.criar_execucao_valida()
        )

        with self.assertRaises(
            FrozenInstanceError
        ):
            execucao.resultado = (
                "NAO_RESOLVIDO"
            )

    def test_registrar_execucao_na_ordem(
        self,
    ):
        ordem = self.criar_ordem_em_execucao()

        execucao = (
            self.criar_execucao_valida()
        )

        registrar_execucao_ordem_servico(
            ordem,
            execucao,
        )

        self.assertEqual(
            ordem.execucoes,
            (execucao,),
        )

        self.assertEqual(
            ordem.status,
            "AGUARDANDO_CONFIRMACAO_CLIENTE",
        )

    def test_ordem_permite_multiplas_execucoes(
        self,
    ):
        ordem = self.criar_ordem_em_execucao()

        execucao_1 = (
            self.criar_execucao_valida(
                numero=1,
                resultado="RETORNO_NECESSARIO",
            )
        )

        registrar_execucao_ordem_servico(
            ordem,
            execucao_1,
        )

        self.assertEqual(
            ordem.status,
            "RETORNO_NECESSARIO",
        )

        alterar_status_ordem_servico(
            ordem,
            "AGUARDANDO_AGENDAMENTO",
        )

        alterar_status_ordem_servico(
            ordem,
            "AGENDADA",
        )

        alterar_status_ordem_servico(
            ordem,
            "EM_EXECUCAO",
        )

        execucao_2 = (
            self.criar_execucao_valida(
                numero=2,
                resultado="RESOLVIDO",
            )
        )

        registrar_execucao_ordem_servico(
            ordem,
            execucao_2,
        )

        self.assertEqual(
            ordem.execucoes,
            (
                execucao_1,
                execucao_2,
            ),
        )

        self.assertEqual(
            ordem.status,
            "AGUARDANDO_CONFIRMACAO_CLIENTE",
        )

    def test_rejeita_numero_execucao_fora_da_sequencia(
        self,
    ):
        ordem = self.criar_ordem_em_execucao()

        execucao = (
            self.criar_execucao_valida(
                numero=2
            )
        )

        with self.assertRaises(
            ValorInvalido
        ):
            registrar_execucao_ordem_servico(
                ordem,
                execucao,
            )

        self.assertEqual(
            ordem.execucoes,
            (),
        )

    def test_registro_rejeita_ordem_invalida(
        self,
    ):
        with self.assertRaises(
            TypeError
        ):
            registrar_execucao_ordem_servico(
                object(),
                self.criar_execucao_valida(),
            )

    def test_registro_rejeita_execucao_invalida(
        self,
    ):
        ordem = criar_ordem_servico_pos_venda(
            1,
            self.criar_contratacao_valida(),
            "Atendimento técnico",
        )

        with self.assertRaises(
            TypeError
        ):
            registrar_execucao_ordem_servico(
                ordem,
                object(),
            )

    def test_falha_no_registro_preserva_historico(
        self,
    ):
        ordem = self.criar_ordem_em_execucao()

        execucao_1 = (
            self.criar_execucao_valida(
                numero=1
            )
        )

        registrar_execucao_ordem_servico(
            ordem,
            execucao_1,
        )

        execucao_invalida = (
            self.criar_execucao_valida(
                numero=3
            )
        )

        with self.assertRaises(
            ValorInvalido
        ):
            registrar_execucao_ordem_servico(
                ordem,
                execucao_invalida,
            )

        self.assertEqual(
            ordem.execucoes,
            (execucao_1,),
        )

    def test_alterar_status_fluxo_local(
        self,
    ):
        ordem = criar_ordem_servico_pos_venda(
            1,
            self.criar_contratacao_valida(),
            "Atendimento técnico",
        )

        alterar_status_ordem_servico(
            ordem,
            "EM_TRIAGEM",
        )

        self.assertEqual(
            ordem.status,
            "EM_TRIAGEM",
        )

    def test_alterar_status_normaliza_valor(
        self,
    ):
        ordem = criar_ordem_servico_pos_venda(
            1,
            self.criar_contratacao_valida(),
            "Atendimento técnico",
        )

        alterar_status_ordem_servico(
            ordem,
            "  em_triagem  ",
        )

        self.assertEqual(
            ordem.status,
            "EM_TRIAGEM",
        )

    def test_rejeita_status_inexistente(
        self,
    ):
        ordem = criar_ordem_servico_pos_venda(
            1,
            self.criar_contratacao_valida(),
            "Atendimento técnico",
        )

        with self.assertRaises(
            ValorInvalido
        ):
            alterar_status_ordem_servico(
                ordem,
                "INEXISTENTE",
            )

        self.assertEqual(
            ordem.status,
            STATUS_INICIAL,
        )

    def test_rejeita_transicao_local_invalida(
        self,
    ):
        ordem = criar_ordem_servico_pos_venda(
            1,
            self.criar_contratacao_valida(),
            "Atendimento técnico",
        )

        with self.assertRaises(
            ValorInvalido
        ):
            alterar_status_ordem_servico(
                ordem,
                "EM_EXECUCAO",
            )

        self.assertEqual(
            ordem.status,
            STATUS_INICIAL,
        )

    def test_transicao_contextual_nao_pode_ser_generica(
        self,
    ):
        ordem = self.criar_ordem_em_execucao()

        with self.assertRaises(
            ValorInvalido
        ):
            alterar_status_ordem_servico(
                ordem,
                "AGUARDANDO_CONFIRMACAO_CLIENTE",
            )

        self.assertEqual(
            ordem.status,
            "EM_EXECUCAO",
        )

    def test_execucao_resolvida_aguarda_confirmacao_cliente(
        self,
    ):
        ordem = self.criar_ordem_em_execucao()
        execucao = self.criar_execucao_valida(
            resultado="RESOLVIDO"
        )

        registrar_execucao_ordem_servico(
            ordem,
            execucao,
        )

        self.assertEqual(
            ordem.status,
            "AGUARDANDO_CONFIRMACAO_CLIENTE",
        )

        self.assertEqual(
            ordem.execucoes,
            (execucao,),
        )

    def test_execucao_nao_resolvida_exige_retorno(
        self,
    ):
        for resultado in (
            "PARCIALMENTE_RESOLVIDO",
            "NAO_RESOLVIDO",
            "RETORNO_NECESSARIO",
        ):
            with self.subTest(
                resultado=resultado
            ):
                ordem = (
                    self.criar_ordem_em_execucao()
                )

                execucao = (
                    self.criar_execucao_valida(
                        resultado=resultado
                    )
                )

                registrar_execucao_ordem_servico(
                    ordem,
                    execucao,
                )

                self.assertEqual(
                    ordem.status,
                    "RETORNO_NECESSARIO",
                )

    def test_rejeita_execucao_fora_de_em_execucao(
        self,
    ):
        ordem = criar_ordem_servico_pos_venda(
            1,
            self.criar_contratacao_valida(),
            "Atendimento técnico",
        )

        with self.assertRaises(
            ValorInvalido
        ):
            registrar_execucao_ordem_servico(
                ordem,
                self.criar_execucao_valida(),
            )

        self.assertEqual(
            ordem.execucoes,
            (),
        )

        self.assertEqual(
            ordem.status,
            STATUS_INICIAL,
        )

    def test_cliente_confirma_conclusao(
        self,
    ):
        ordem = self.criar_ordem_em_execucao()

        registrar_execucao_ordem_servico(
            ordem,
            self.criar_execucao_valida(),
        )

        confirmar_conclusao_ordem_servico(
            ordem
        )

        self.assertEqual(
            ordem.status,
            "CONCLUIDA",
        )

    def test_cliente_contesta_conclusao(
        self,
    ):
        ordem = self.criar_ordem_em_execucao()

        registrar_execucao_ordem_servico(
            ordem,
            self.criar_execucao_valida(),
        )

        contestar_conclusao_ordem_servico(
            ordem
        )

        self.assertEqual(
            ordem.status,
            "EM_ANALISE_DE_CONTESTACAO",
        )

    def test_contestacao_pode_exigir_retorno(
        self,
    ):
        ordem = self.criar_ordem_em_execucao()

        registrar_execucao_ordem_servico(
            ordem,
            self.criar_execucao_valida(),
        )

        contestar_conclusao_ordem_servico(
            ordem
        )

        resolver_contestacao_ordem_servico(
            ordem,
            requer_retorno=True,
        )

        self.assertEqual(
            ordem.status,
            "RETORNO_NECESSARIO",
        )

    def test_contestacao_pode_confirmar_conclusao(
        self,
    ):
        ordem = self.criar_ordem_em_execucao()

        registrar_execucao_ordem_servico(
            ordem,
            self.criar_execucao_valida(),
        )

        contestar_conclusao_ordem_servico(
            ordem
        )

        resolver_contestacao_ordem_servico(
            ordem,
            requer_retorno=False,
        )

        self.assertEqual(
            ordem.status,
            "CONCLUIDA",
        )

    def test_resolver_contestacao_exige_booleano(
        self,
    ):
        ordem = self.criar_ordem_em_execucao()

        registrar_execucao_ordem_servico(
            ordem,
            self.criar_execucao_valida(),
        )

        contestar_conclusao_ordem_servico(
            ordem
        )

        with self.assertRaises(
            ValorInvalido
        ):
            resolver_contestacao_ordem_servico(
                ordem,
                requer_retorno="sim",
            )

        self.assertEqual(
            ordem.status,
            "EM_ANALISE_DE_CONTESTACAO",
        )

    def test_falha_contextual_preserva_execucao_e_status(
        self,
    ):
        ordem = self.criar_ordem_em_execucao()

        execucao = self.criar_execucao_valida(
            numero=2,
            resultado="RESOLVIDO",
        )

        with self.assertRaises(
            ValorInvalido
        ):
            registrar_execucao_ordem_servico(
                ordem,
                execucao,
            )

        self.assertEqual(
            ordem.execucoes,
            (),
        )

        self.assertEqual(
            ordem.status,
            "EM_EXECUCAO",
        )

    def test_buscar_ordem_servico_por_codigo(
        self,
    ):
        ordens = (
            self.criar_ordens_para_consulta()
        )

        resultado = buscar_ordem_servico_por_codigo(
            ordens,
            2,
        )

        self.assertIs(
            resultado,
            ordens[1],
        )

    def test_buscar_ordem_inexistente_retorna_none(
        self,
    ):
        ordens = (
            self.criar_ordens_para_consulta()
        )

        resultado = buscar_ordem_servico_por_codigo(
            ordens,
            999,
        )

        self.assertIsNone(
            resultado
        )

    def test_listar_ordens_por_contratacao(
        self,
    ):
        ordens = (
            self.criar_ordens_para_consulta()
        )

        resultado = listar_ordens_por_contratacao(
            ordens,
            10,
        )

        self.assertEqual(
            resultado,
            [
                ordens[0],
                ordens[1],
            ],
        )

    def test_listar_ordens_por_cliente(
        self,
    ):
        ordens = (
            self.criar_ordens_para_consulta()
        )

        resultado = listar_ordens_por_cliente(
            ordens,
            30,
        )

        self.assertEqual(
            resultado,
            [
                ordens[0],
                ordens[1],
            ],
        )

    def test_listar_ordens_por_empresa(
        self,
    ):
        ordens = (
            self.criar_ordens_para_consulta()
        )

        resultado = listar_ordens_por_empresa(
            ordens,
            51,
        )

        self.assertEqual(
            resultado,
            [
                ordens[2],
            ],
        )

    def test_listar_ordens_por_tipo_servico(
        self,
    ):
        ordens = (
            self.criar_ordens_para_consulta()
        )

        resultado = listar_ordens_por_tipo_servico(
            ordens,
            41,
        )

        self.assertEqual(
            resultado,
            [
                ordens[2],
            ],
        )

    def test_listar_ordens_por_status(
        self,
    ):
        ordens = (
            self.criar_ordens_para_consulta()
        )

        resultado = listar_ordens_por_status(
            ordens,
            "EM_TRIAGEM",
        )

        self.assertEqual(
            resultado,
            [
                ordens[1],
                ordens[2],
            ],
        )

    def test_listar_ordens_por_status_normaliza_valor(
        self,
    ):
        ordens = (
            self.criar_ordens_para_consulta()
        )

        resultado = listar_ordens_por_status(
            ordens,
            "  em_triagem  ",
        )

        self.assertEqual(
            resultado,
            [
                ordens[1],
                ordens[2],
            ],
        )

    def test_consultas_sem_resultado_retornam_lista_vazia(
        self,
    ):
        ordens = (
            self.criar_ordens_para_consulta()
        )

        self.assertEqual(
            listar_ordens_por_cliente(
                ordens,
                999,
            ),
            [],
        )

        self.assertEqual(
            listar_ordens_por_empresa(
                ordens,
                999,
            ),
            [],
        )

    def test_consultas_preservam_ordem_original(
        self,
    ):
        ordens = (
            self.criar_ordens_para_consulta()
        )

        resultado = listar_ordens_por_status(
            ordens,
            "EM_TRIAGEM",
        )

        self.assertIs(
            resultado[0],
            ordens[1],
        )

        self.assertIs(
            resultado[1],
            ordens[2],
        )

    def test_consultas_nao_alteram_colecao_original(
        self,
    ):
        ordens = list(
            self.criar_ordens_para_consulta()
        )

        estado_original = list(ordens)

        listar_ordens_por_cliente(
            ordens,
            30,
        )

        self.assertEqual(
            ordens,
            estado_original,
        )

    def test_consultas_rejeitam_colecao_invalida(
        self,
    ):
        for ordens in (
            None,
            "ordens",
            123,
        ):
            with self.subTest(
                ordens=ordens
            ):
                with self.assertRaises(
                    ValorInvalido
                ):
                    buscar_ordem_servico_por_codigo(
                        ordens,
                        1,
                    )

    def test_consultas_rejeitam_item_invalido_na_colecao(
        self,
    ):
        ordem = criar_ordem_servico_pos_venda(
            1,
            self.criar_contratacao_valida(),
            "Atendimento técnico",
        )

        with self.assertRaises(
            ValorInvalido
        ):
            listar_ordens_por_cliente(
                (
                    ordem,
                    object(),
                ),
                30,
            )

    def test_consultas_rejeitam_codigo_filtro_invalido(
        self,
    ):
        ordens = (
            self.criar_ordens_para_consulta()
        )

        for codigo in (
            0,
            -1,
            True,
            "1",
            None,
        ):
            with self.subTest(
                codigo=codigo
            ):
                with self.assertRaises(
                    ValorInvalido
                ):
                    listar_ordens_por_empresa(
                        ordens,
                        codigo,
                    )

    def test_consulta_rejeita_status_invalido(
        self,
    ):
        ordens = (
            self.criar_ordens_para_consulta()
        )

        for status in (
            "",
            "INEXISTENTE",
            None,
            1,
        ):
            with self.subTest(
                status=status
            ):
                with self.assertRaises(
                    ValorInvalido
                ):
                    listar_ordens_por_status(
                        ordens,
                        status,
                    )

    def test_operacao_rejeita_status_armazenado_invalido(
        self,
    ):
        ordem = criar_ordem_servico_pos_venda(
            1,
            self.criar_contratacao_valida(),
            "Atendimento técnico",
        )

        ordem.status = "INEXISTENTE"

        with self.assertRaises(
            ValorInvalido
        ):
            alterar_status_ordem_servico(
                ordem,
                "EM_TRIAGEM",
            )

        self.assertEqual(
            ordem.status,
            "INEXISTENTE",
        )

    def test_operacao_rejeita_status_armazenado_nao_normalizado(
        self,
    ):
        ordem = criar_ordem_servico_pos_venda(
            1,
            self.criar_contratacao_valida(),
            "Atendimento técnico",
        )

        ordem.status = " aberta "

        with self.assertRaises(
            ValorInvalido
        ):
            alterar_status_ordem_servico(
                ordem,
                "EM_TRIAGEM",
            )

        self.assertEqual(
            ordem.status,
            " aberta ",
        )

    def test_operacao_rejeita_codigo_estrutural_corrompido(
        self,
    ):
        ordem = criar_ordem_servico_pos_venda(
            1,
            self.criar_contratacao_valida(),
            "Atendimento técnico",
        )

        ordem.codigo_empresa = 0

        with self.assertRaises(
            ValorInvalido
        ):
            alterar_status_ordem_servico(
                ordem,
                "EM_TRIAGEM",
            )

        self.assertEqual(
            ordem.status,
            STATUS_INICIAL,
        )

    def test_registro_rejeita_historico_nao_tupla(
        self,
    ):
        ordem = self.criar_ordem_em_execucao()
        ordem.execucoes = []

        execucao = self.criar_execucao_valida()

        with self.assertRaises(
            ValorInvalido
        ):
            registrar_execucao_ordem_servico(
                ordem,
                execucao,
            )

        self.assertEqual(
            ordem.execucoes,
            [],
        )

        self.assertEqual(
            ordem.status,
            "EM_EXECUCAO",
        )

    def test_registro_rejeita_item_invalido_no_historico(
        self,
    ):
        ordem = self.criar_ordem_em_execucao()
        ordem.execucoes = (
            object(),
        )

        with self.assertRaises(
            ValorInvalido
        ):
            registrar_execucao_ordem_servico(
                ordem,
                self.criar_execucao_valida(
                    numero=2
                ),
            )

        self.assertEqual(
            ordem.status,
            "EM_EXECUCAO",
        )

    def test_registro_rejeita_historico_com_numeracao_corrompida(
        self,
    ):
        ordem = self.criar_ordem_em_execucao()

        execucao_corrompida = (
            self.criar_execucao_valida(
                numero=2
            )
        )

        ordem.execucoes = (
            execucao_corrompida,
        )

        with self.assertRaises(
            ValorInvalido
        ):
            registrar_execucao_ordem_servico(
                ordem,
                self.criar_execucao_valida(
                    numero=2
                ),
            )

        self.assertEqual(
            ordem.execucoes,
            (execucao_corrompida,),
        )

        self.assertEqual(
            ordem.status,
            "EM_EXECUCAO",
        )

    def test_confirmacao_rejeita_status_sem_execucao_resolvida(
        self,
    ):
        ordem = criar_ordem_servico_pos_venda(
            1,
            self.criar_contratacao_valida(),
            "Atendimento técnico",
        )

        ordem.status = (
            "AGUARDANDO_CONFIRMACAO_CLIENTE"
        )

        with self.assertRaises(
            ValorInvalido
        ):
            confirmar_conclusao_ordem_servico(
                ordem
            )

        self.assertEqual(
            ordem.status,
            "AGUARDANDO_CONFIRMACAO_CLIENTE",
        )

    def test_contestacao_rejeita_historico_incompativel(
        self,
    ):
        ordem = self.criar_ordem_em_execucao()

        execucao = self.criar_execucao_valida(
            resultado="NAO_RESOLVIDO"
        )

        ordem.execucoes = (execucao,)
        ordem.status = (
            "AGUARDANDO_CONFIRMACAO_CLIENTE"
        )

        with self.assertRaises(
            ValorInvalido
        ):
            contestar_conclusao_ordem_servico(
                ordem
            )

        self.assertEqual(
            ordem.status,
            "AGUARDANDO_CONFIRMACAO_CLIENTE",
        )

    def test_retorno_necessario_exige_historico(
        self,
    ):
        ordem = criar_ordem_servico_pos_venda(
            1,
            self.criar_contratacao_valida(),
            "Atendimento técnico",
        )

        ordem.status = "RETORNO_NECESSARIO"

        with self.assertRaises(
            ValorInvalido
        ):
            alterar_status_ordem_servico(
                ordem,
                "AGUARDANDO_AGENDAMENTO",
            )

        self.assertEqual(
            ordem.status,
            "RETORNO_NECESSARIO",
        )

    def test_consulta_rejeita_ordem_corrompida(
        self,
    ):
        ordem = criar_ordem_servico_pos_venda(
            1,
            self.criar_contratacao_valida(),
            "Atendimento técnico",
        )

        ordem.codigo_cliente = 0

        with self.assertRaises(
            ValorInvalido
        ):
            listar_ordens_por_cliente(
                (ordem,),
                30,
            )

    def test_falha_de_integridade_preserva_agregado(
        self,
    ):
        ordem = self.criar_ordem_em_execucao()

        execucao = self.criar_execucao_valida(
            numero=2
        )

        ordem.execucoes = (
            execucao,
        )

        estado_execucoes = ordem.execucoes
        estado_status = ordem.status

        with self.assertRaises(
            ValorInvalido
        ):
            registrar_execucao_ordem_servico(
                ordem,
                self.criar_execucao_valida(
                    numero=2
                ),
            )

        self.assertIs(
            ordem.execucoes,
            estado_execucoes,
        )

        self.assertEqual(
            ordem.status,
            estado_status,
        )

if __name__ == "__main__":
    unittest.main()