import unittest
from datetime import date, datetime

from app.dominio.contratacoes_servico import (
    ContratacaoServico,
    SnapshotContratacaoServico,
)

from app.dominio.erros_dominio import (
    OperacaoNaoPermitida,
    ValorInvalido,
)

from app.dominio.privacidade_servicos import (
    AutorizacaoContato,
    MotivoAutorizacaoContato,
    autorizacao_contato_esta_ativa,
    buscar_autorizacao_contato_por_codigo,
    criar_autorizacao_contato_proposta_aceita,
    criar_autorizacao_contato_solicitacao_direta,
    listar_autorizacoes_ativas,
    listar_autorizacoes_por_cliente,
    listar_autorizacoes_por_contratacao,
    listar_autorizacoes_por_empresa,
    listar_autorizacoes_por_solicitacao,
    pode_visualizar_contato_cliente,
    revogar_autorizacao_contato,
)

from app.dominio.solicitacoes_servico import (
    ModalidadeSolicitacaoServico,
    OrigemSolicitacaoServico,
    SolicitacaoServico,
)


class TestPrivacidadeServicos(
    unittest.TestCase
):
    def criar_solicitacao_direta(self):
        return SolicitacaoServico(
            codigo=10,
            codigo_cliente=20,
            codigo_tipo_servico=30,
            modalidade=(
                ModalidadeSolicitacaoServico.DIRETA
            ),
            origem=(
                OrigemSolicitacaoServico.CLIENTE
            ),
            municipio="Caetité",
            uf="BA",
            dados_tecnicos={},
            codigo_empresa_destinataria=40,
            codigo_servico_ofertado_empresa=50,
        )

    def criar_solicitacao_aberta(self):
        return SolicitacaoServico(
            codigo=10,
            codigo_cliente=20,
            codigo_tipo_servico=30,
            modalidade=(
                ModalidadeSolicitacaoServico.ABERTA
            ),
            origem=(
                OrigemSolicitacaoServico.CLIENTE
            ),
            municipio="Caetité",
            uf="BA",
            dados_tecnicos={},
            codigo_empresa_destinataria=None,
            codigo_servico_ofertado_empresa=None,
        )

    def criar_contratacao_valida(self):
        snapshot = SnapshotContratacaoServico(
            numero_versao_proposta=1,
            valor_contratado=1000.0,
            prazo_execucao_dias=10,
            descricao_tecnica="Serviço contratado",
            itens_incluidos=(),
            itens_nao_incluidos=(),
            garantias={},
            condicoes_comerciais={},
            observacoes=None,
        )

        return ContratacaoServico(
            codigo=60,
            codigo_solicitacao=10,
            codigo_cliente=20,
            codigo_tipo_servico=30,
            codigo_empresa=40,
            codigo_servico_ofertado_empresa=50,
            codigo_proposta=70,
            snapshot=snapshot,
            data_limite_formalizacao=date(
                2026,
                12,
                31,
            ),
            processo_operacional=None,
            status="EM_FORMALIZACAO",
        )

    def criar_autorizacao_direta(
        self,
        codigo=1,
    ):
        return (
            criar_autorizacao_contato_solicitacao_direta(
                codigo,
                self.criar_solicitacao_direta(),
                datetime(2026, 8, 21, 10, 0),
            )
        )

    def criar_autorizacao_aberta(
        self,
        codigo=1,
    ):
        return (
            criar_autorizacao_contato_proposta_aceita(
                codigo,
                self.criar_solicitacao_aberta(),
                self.criar_contratacao_valida(),
                datetime(2026, 8, 21, 11, 0),
            )
        )

    def test_criar_autorizacao_solicitacao_direta(
        self,
    ):
        autorizacao = (
            criar_autorizacao_contato_solicitacao_direta(
                1,
                self.criar_solicitacao_direta(),
                datetime(2026, 8, 21, 10, 0),
            )
        )

        self.assertIsInstance(
            autorizacao,
            AutorizacaoContato,
        )

        self.assertEqual(
            autorizacao.codigo_empresa,
            40,
        )

        self.assertEqual(
            autorizacao.codigo_cliente,
            20,
        )

        self.assertEqual(
            autorizacao.codigo_solicitacao,
            10,
        )

        self.assertIsNone(
            autorizacao.codigo_contratacao
        )

        self.assertEqual(
            autorizacao.motivo,
            (
                MotivoAutorizacaoContato
                .SOLICITACAO_DIRETA
            ),
        )

        self.assertTrue(
            autorizacao.ativo
        )

    def test_autorizacao_direta_usa_empresa_destinataria(
        self,
    ):
        solicitacao = (
            self.criar_solicitacao_direta()
        )

        solicitacao.codigo_empresa_destinataria = 99

        autorizacao = (
            criar_autorizacao_contato_solicitacao_direta(
                1,
                solicitacao,
                datetime(2026, 8, 21, 10, 0),
            )
        )

        self.assertEqual(
            autorizacao.codigo_empresa,
            99,
        )

    def test_rejeita_autorizacao_direta_para_solicitacao_aberta(
        self,
    ):
        with self.assertRaises(
            ValorInvalido
        ):
            criar_autorizacao_contato_solicitacao_direta(
                1,
                self.criar_solicitacao_aberta(),
                datetime(2026, 8, 21, 10, 0),
            )

    def test_criar_autorizacao_proposta_aceita(
        self,
    ):
        autorizacao = (
            criar_autorizacao_contato_proposta_aceita(
                1,
                self.criar_solicitacao_aberta(),
                self.criar_contratacao_valida(),
                datetime(2026, 8, 21, 11, 0),
            )
        )

        self.assertEqual(
            autorizacao.codigo_empresa,
            40,
        )

        self.assertEqual(
            autorizacao.codigo_contratacao,
            60,
        )

        self.assertEqual(
            autorizacao.motivo,
            (
                MotivoAutorizacaoContato
                .PROPOSTA_ACEITA
            ),
        )

        self.assertTrue(
            autorizacao.ativo
        )

    def test_autorizacao_proposta_aceita_usa_empresa_da_contratacao(
        self,
    ):
        contratacao = (
            self.criar_contratacao_valida()
        )

        contratacao.codigo_empresa = 77

        autorizacao = (
            criar_autorizacao_contato_proposta_aceita(
                1,
                self.criar_solicitacao_aberta(),
                contratacao,
                datetime(2026, 8, 21, 11, 0),
            )
        )

        self.assertEqual(
            autorizacao.codigo_empresa,
            77,
        )

    def test_rejeita_contratacao_de_outra_solicitacao(
        self,
    ):
        contratacao = (
            self.criar_contratacao_valida()
        )

        contratacao.codigo_solicitacao = 999

        with self.assertRaises(
            ValorInvalido
        ):
            criar_autorizacao_contato_proposta_aceita(
                1,
                self.criar_solicitacao_aberta(),
                contratacao,
                datetime(2026, 8, 21, 11, 0),
            )

    def test_rejeita_contratacao_de_outro_cliente(
        self,
    ):
        contratacao = (
            self.criar_contratacao_valida()
        )

        contratacao.codigo_cliente = 999

        with self.assertRaises(
            ValorInvalido
        ):
            criar_autorizacao_contato_proposta_aceita(
                1,
                self.criar_solicitacao_aberta(),
                contratacao,
                datetime(2026, 8, 21, 11, 0),
            )

    def test_rejeita_proposta_aceita_para_solicitacao_direta(
        self,
    ):
        with self.assertRaises(
            ValorInvalido
        ):
            criar_autorizacao_contato_proposta_aceita(
                1,
                self.criar_solicitacao_direta(),
                self.criar_contratacao_valida(),
                datetime(2026, 8, 21, 11, 0),
            )

    def test_autorizacao_nasce_ativa(
        self,
    ):
        autorizacao = (
            criar_autorizacao_contato_solicitacao_direta(
                1,
                self.criar_solicitacao_direta(),
                datetime(2026, 8, 21, 10, 0),
            )
        )

        self.assertTrue(
            autorizacao_contato_esta_ativa(
                autorizacao
            )
        )

        self.assertIsNone(
            autorizacao.data_hora_revogacao
        )

    def test_revogar_autorizacao(
        self,
    ):
        autorizacao = (
            criar_autorizacao_contato_solicitacao_direta(
                1,
                self.criar_solicitacao_direta(),
                datetime(2026, 8, 21, 10, 0),
            )
        )

        revogar_autorizacao_contato(
            autorizacao,
            datetime(2026, 8, 21, 12, 0),
        )

        self.assertFalse(
            autorizacao.ativo
        )

        self.assertEqual(
            autorizacao.data_hora_revogacao,
            datetime(2026, 8, 21, 12, 0),
        )

    def test_rejeita_revogacao_anterior_a_liberacao(
        self,
    ):
        autorizacao = (
            criar_autorizacao_contato_solicitacao_direta(
                1,
                self.criar_solicitacao_direta(),
                datetime(2026, 8, 21, 10, 0),
            )
        )

        with self.assertRaises(
            ValorInvalido
        ):
            revogar_autorizacao_contato(
                autorizacao,
                datetime(2026, 8, 21, 9, 59),
            )

        self.assertTrue(
            autorizacao.ativo
        )

        self.assertIsNone(
            autorizacao.data_hora_revogacao
        )

    def test_rejeita_revogacao_repetida(
        self,
    ):
        autorizacao = (
            criar_autorizacao_contato_solicitacao_direta(
                1,
                self.criar_solicitacao_direta(),
                datetime(2026, 8, 21, 10, 0),
            )
        )

        revogar_autorizacao_contato(
            autorizacao,
            datetime(2026, 8, 21, 12, 0),
        )

        with self.assertRaises(
            OperacaoNaoPermitida
        ):
            revogar_autorizacao_contato(
                autorizacao,
                datetime(2026, 8, 21, 13, 0),
            )

        self.assertEqual(
            autorizacao.data_hora_revogacao,
            datetime(2026, 8, 21, 12, 0),
        )

    def test_rejeita_codigo_autorizacao_invalido(
        self,
    ):
        solicitacao = (
            self.criar_solicitacao_direta()
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
                    criar_autorizacao_contato_solicitacao_direta(
                        codigo,
                        solicitacao,
                        datetime(
                            2026,
                            8,
                            21,
                            10,
                            0,
                        ),
                    )

    def test_rejeita_data_hora_liberacao_invalida(
        self,
    ):
        solicitacao = (
            self.criar_solicitacao_direta()
        )

        for valor in (
            None,
            "2026-08-21 10:00",
            date(2026, 8, 21),
            1,
        ):
            with self.subTest(
                valor=valor
            ):
                with self.assertRaises(
                    ValorInvalido
                ):
                    criar_autorizacao_contato_solicitacao_direta(
                        1,
                        solicitacao,
                        valor,
                    )

    def test_empresa_destinataria_pode_visualizar_contato_direto(
        self,
    ):
        solicitacao = (
            self.criar_solicitacao_direta()
        )

        autorizacao = (
            criar_autorizacao_contato_solicitacao_direta(
                1,
                solicitacao,
                datetime(2026, 8, 21, 10, 0),
            )
        )

        resultado = pode_visualizar_contato_cliente(
            solicitacao,
            40,
            (autorizacao,),
        )

        self.assertTrue(
            resultado
        )

    def test_outra_empresa_nao_visualiza_contato_direto(
        self,
    ):
        solicitacao = (
            self.criar_solicitacao_direta()
        )

        autorizacao = (
            criar_autorizacao_contato_solicitacao_direta(
                1,
                solicitacao,
                datetime(2026, 8, 21, 10, 0),
            )
        )

        resultado = pode_visualizar_contato_cliente(
            solicitacao,
            99,
            (autorizacao,),
        )

        self.assertFalse(
            resultado
        )

    def test_solicitacao_direta_sem_autorizacao_nao_libera_contato(
        self,
    ):
        resultado = pode_visualizar_contato_cliente(
            self.criar_solicitacao_direta(),
            40,
            (),
        )

        self.assertFalse(
            resultado
        )

    def test_solicitacao_aberta_sem_aceite_nao_libera_contato(
        self,
    ):
        resultado = pode_visualizar_contato_cliente(
            self.criar_solicitacao_aberta(),
            40,
            (),
        )

        self.assertFalse(
            resultado
        )

    def test_empresa_vencedora_pode_visualizar_contato_aberto(
        self,
    ):
        solicitacao = (
            self.criar_solicitacao_aberta()
        )

        autorizacao = (
            criar_autorizacao_contato_proposta_aceita(
                1,
                solicitacao,
                self.criar_contratacao_valida(),
                datetime(2026, 8, 21, 11, 0),
            )
        )

        resultado = pode_visualizar_contato_cliente(
            solicitacao,
            40,
            (autorizacao,),
        )

        self.assertTrue(
            resultado
        )

    def test_empresa_nao_vencedora_nao_visualiza_contato_aberto(
        self,
    ):
        solicitacao = (
            self.criar_solicitacao_aberta()
        )

        autorizacao = (
            criar_autorizacao_contato_proposta_aceita(
                1,
                solicitacao,
                self.criar_contratacao_valida(),
                datetime(2026, 8, 21, 11, 0),
            )
        )

        resultado = pode_visualizar_contato_cliente(
            solicitacao,
            99,
            (autorizacao,),
        )

        self.assertFalse(
            resultado
        )

    def test_autorizacao_revogada_remove_acesso(
        self,
    ):
        solicitacao = (
            self.criar_solicitacao_aberta()
        )

        autorizacao = (
            criar_autorizacao_contato_proposta_aceita(
                1,
                solicitacao,
                self.criar_contratacao_valida(),
                datetime(2026, 8, 21, 11, 0),
            )
        )

        revogar_autorizacao_contato(
            autorizacao,
            datetime(2026, 8, 21, 12, 0),
        )

        resultado = pode_visualizar_contato_cliente(
            solicitacao,
            40,
            (autorizacao,),
        )

        self.assertFalse(
            resultado
        )

    def test_motivo_incompativel_nao_libera_contato(
        self,
    ):
        solicitacao = (
            self.criar_solicitacao_aberta()
        )

        autorizacao = (
            self.criar_autorizacao_direta()
        )

        resultado = pode_visualizar_contato_cliente(
            solicitacao,
            40,
            (autorizacao,),
        )

        self.assertFalse(
            resultado
        )

    def test_buscar_autorizacao_por_codigo(
        self,
    ):
        autorizacao_1 = (
            self.criar_autorizacao_direta(
                codigo=1
            )
        )

        autorizacao_2 = (
            self.criar_autorizacao_aberta(
                codigo=2
            )
        )

        resultado = (
            buscar_autorizacao_contato_por_codigo(
                (
                    autorizacao_1,
                    autorizacao_2,
                ),
                2,
            )
        )

        self.assertIs(
            resultado,
            autorizacao_2,
        )

    def test_buscar_autorizacao_inexistente_retorna_none(
        self,
    ):
        resultado = (
            buscar_autorizacao_contato_por_codigo(
                (
                    self.criar_autorizacao_direta(),
                ),
                999,
            )
        )

        self.assertIsNone(
            resultado
        )

    def test_listar_autorizacoes_por_cliente(
        self,
    ):
        autorizacao_1 = (
            self.criar_autorizacao_direta(
                codigo=1
            )
        )

        autorizacao_2 = (
            self.criar_autorizacao_aberta(
                codigo=2
            )
        )

        resultado = listar_autorizacoes_por_cliente(
            (
                autorizacao_1,
                autorizacao_2,
            ),
            20,
        )

        self.assertEqual(
            resultado,
            [
                autorizacao_1,
                autorizacao_2,
            ],
        )

    def test_listar_autorizacoes_por_empresa(
        self,
    ):
        autorizacao = (
            self.criar_autorizacao_aberta()
        )

        resultado = listar_autorizacoes_por_empresa(
            (autorizacao,),
            40,
        )

        self.assertEqual(
            resultado,
            [autorizacao],
        )

    def test_listar_autorizacoes_por_solicitacao(
        self,
    ):
        autorizacao = (
            self.criar_autorizacao_direta()
        )

        resultado = (
            listar_autorizacoes_por_solicitacao(
                (autorizacao,),
                10,
            )
        )

        self.assertEqual(
            resultado,
            [autorizacao],
        )

    def test_listar_autorizacoes_por_contratacao(
        self,
    ):
        direta = (
            self.criar_autorizacao_direta(
                codigo=1
            )
        )

        aberta = (
            self.criar_autorizacao_aberta(
                codigo=2
            )
        )

        resultado = (
            listar_autorizacoes_por_contratacao(
                (
                    direta,
                    aberta,
                ),
                60,
            )
        )

        self.assertEqual(
            resultado,
            [aberta],
        )

    def test_listar_autorizacoes_ativas(
        self,
    ):
        ativa = (
            self.criar_autorizacao_direta(
                codigo=1
            )
        )

        revogada = (
            self.criar_autorizacao_aberta(
                codigo=2
            )
        )

        revogar_autorizacao_contato(
            revogada,
            datetime(2026, 8, 21, 12, 0),
        )

        resultado = listar_autorizacoes_ativas(
            (
                ativa,
                revogada,
            )
        )

        self.assertEqual(
            resultado,
            [ativa],
        )

    def test_permissao_rejeita_codigo_empresa_invalido(
        self,
    ):
        solicitacao = (
            self.criar_solicitacao_direta()
        )

        for codigo in (
            0,
            -1,
            True,
            "40",
            None,
        ):
            with self.subTest(
                codigo=codigo
            ):
                with self.assertRaises(
                    ValorInvalido
                ):
                    pode_visualizar_contato_cliente(
                        solicitacao,
                        codigo,
                        (),
                    )

    def test_consultas_rejeitam_colecao_invalida(
        self,
    ):
        for autorizacoes in (
            None,
            "autorizacoes",
            123,
        ):
            with self.subTest(
                autorizacoes=autorizacoes
            ):
                with self.assertRaises(
                    ValorInvalido
                ):
                    listar_autorizacoes_ativas(
                        autorizacoes
                    )

    def test_consultas_rejeitam_item_invalido(
        self,
    ):
        with self.assertRaises(
            ValorInvalido
        ):
            listar_autorizacoes_ativas(
                (
                    self.criar_autorizacao_direta(),
                    object(),
                )
            )

    def test_rejeita_autorizacao_ativa_com_data_revogacao(
        self,
    ):
        autorizacao = (
            self.criar_autorizacao_direta()
        )

        autorizacao.data_hora_revogacao = datetime(
            2026,
            8,
            21,
            12,
            0,
        )

        with self.assertRaises(
            ValorInvalido
        ):
            autorizacao_contato_esta_ativa(
                autorizacao
            )

    def test_rejeita_autorizacao_inativa_sem_data_revogacao(
        self,
    ):
        autorizacao = (
            self.criar_autorizacao_direta()
        )

        autorizacao.ativo = False

        with self.assertRaises(
            ValorInvalido
        ):
            autorizacao_contato_esta_ativa(
                autorizacao
            )

    def test_rejeita_revogacao_anterior_em_entidade_adulterada(
        self,
    ):
        autorizacao = (
            self.criar_autorizacao_direta()
        )

        autorizacao.ativo = False
        autorizacao.data_hora_revogacao = datetime(
            2026,
            8,
            21,
            9,
            0,
        )

        with self.assertRaises(
            ValorInvalido
        ):
            listar_autorizacoes_ativas(
                (autorizacao,)
            )

    def test_rejeita_solicitacao_direta_com_contratacao(
        self,
    ):
        autorizacao = (
            self.criar_autorizacao_direta()
        )

        autorizacao.codigo_contratacao = 60

        with self.assertRaises(
            ValorInvalido
        ):
            listar_autorizacoes_ativas(
                (autorizacao,)
            )

    def test_rejeita_proposta_aceita_sem_contratacao(
        self,
    ):
        autorizacao = (
            self.criar_autorizacao_aberta()
        )

        autorizacao.codigo_contratacao = None

        with self.assertRaises(
            ValorInvalido
        ):
            listar_autorizacoes_ativas(
                (autorizacao,)
            )

    def test_rejeita_motivo_adulterado(
        self,
    ):
        autorizacao = (
            self.criar_autorizacao_direta()
        )

        autorizacao.motivo = "SOLICITACAO_DIRETA"

        with self.assertRaises(
            ValorInvalido
        ):
            listar_autorizacoes_ativas(
                (autorizacao,)
            )

    def test_rejeita_codigo_estrutural_adulterado(
        self,
    ):
        autorizacao = (
            self.criar_autorizacao_direta()
        )

        autorizacao.codigo_empresa = 0

        with self.assertRaises(
            ValorInvalido
        ):
            listar_autorizacoes_ativas(
                (autorizacao,)
            )

    def test_permissao_rejeita_autorizacao_corrompida(
        self,
    ):
        solicitacao = (
            self.criar_solicitacao_direta()
        )

        autorizacao = (
            criar_autorizacao_contato_solicitacao_direta(
                1,
                solicitacao,
                datetime(2026, 8, 21, 10, 0),
            )
        )

        autorizacao.ativo = False
        autorizacao.data_hora_revogacao = None

        with self.assertRaises(
            ValorInvalido
        ):
            pode_visualizar_contato_cliente(
                solicitacao,
                40,
                (autorizacao,),
            )

    def test_revogacao_rejeita_entidade_corrompida_sem_mutar(
        self,
    ):
        autorizacao = (
            self.criar_autorizacao_direta()
        )

        autorizacao.codigo_cliente = 0

        with self.assertRaises(
            ValorInvalido
        ):
            revogar_autorizacao_contato(
                autorizacao,
                datetime(2026, 8, 21, 12, 0),
            )

        self.assertTrue(
            autorizacao.ativo
        )

        self.assertIsNone(
            autorizacao.data_hora_revogacao
        )

    def test_multiplas_autorizacoes_ativas_validas_sao_aceitas(
        self,
    ):
        solicitacao = (
            self.criar_solicitacao_direta()
        )

        autorizacao_1 = (
            criar_autorizacao_contato_solicitacao_direta(
                1,
                solicitacao,
                datetime(2026, 8, 21, 10, 0),
            )
        )

        autorizacao_2 = (
            criar_autorizacao_contato_solicitacao_direta(
                2,
                solicitacao,
                datetime(2026, 8, 21, 11, 0),
            )
        )

        resultado = pode_visualizar_contato_cliente(
            solicitacao,
            40,
            (
                autorizacao_1,
                autorizacao_2,
            ),
        )

        self.assertTrue(
            resultado
        )

    def test_historico_revogado_e_nova_autorizacao_ativa(
        self,
    ):
        solicitacao = (
            self.criar_solicitacao_direta()
        )

        antiga = (
            criar_autorizacao_contato_solicitacao_direta(
                1,
                solicitacao,
                datetime(2026, 8, 21, 9, 0),
            )
        )

        revogar_autorizacao_contato(
            antiga,
            datetime(2026, 8, 21, 10, 0),
        )

        atual = (
            criar_autorizacao_contato_solicitacao_direta(
                2,
                solicitacao,
                datetime(2026, 8, 21, 11, 0),
            )
        )

        resultado = pode_visualizar_contato_cliente(
            solicitacao,
            40,
            (
                antiga,
                atual,
            ),
        )

        self.assertTrue(
            resultado
        )

if __name__ == "__main__":
    unittest.main()