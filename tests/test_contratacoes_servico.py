import unittest
from dataclasses import FrozenInstanceError
from datetime import date

from app.dominio.contratacoes_servico import (
    ContratacaoServico,
    ReferenciaProcessoOperacional,
    SnapshotContratacaoServico,
    alterar_status_contratacao_servico,
    buscar_contratacao_servico_por_codigo,
    criar_contratacao_servico,
    criar_snapshot_contratacao_servico,
    expirar_contratacao_servico,
    listar_contratacoes_por_cliente,
    listar_contratacoes_por_empresa,
    listar_contratacoes_por_processo_operacional,
    listar_contratacoes_por_proposta,
    listar_contratacoes_por_solicitacao,
    listar_contratacoes_por_status,
    listar_contratacoes_por_tipo_servico,
    registrar_processo_operacional,
)

from app.dominio.erros_dominio import (
    ValorInvalido,
)

from app.dominio.propostas_servico import (
    criar_proposta_servico,
    criar_versao_proposta_servico,
)

from app.dominio.solicitacoes_servico import (
    ModalidadeSolicitacaoServico,
    OrigemSolicitacaoServico,
    SolicitacaoServico,
)

from app.dominio.status_contratacao_servico import (
    STATUS_INICIAL,
)


class TestContratacoesServico(unittest.TestCase):

    def setUp(self):
        self.solicitacao = SolicitacaoServico(
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
            status="RECEBENDO_PROPOSTAS",
        )

        self.versao = (
            criar_versao_proposta_servico(
                numero=1,
                valor=15000,
                prazo_execucao_dias=30,
                validade=date(2026, 12, 31),
                descricao_tecnica=(
                    "Execução completa do serviço"
                ),
                itens_incluidos=[
                    "Projeto",
                    "Instalação",
                ],
                itens_nao_incluidos=[
                    "Adequação do padrão",
                ],
                garantias={
                    "instalacao": "12 meses",
                },
                condicoes_comerciais={
                    "entrada": "30%",
                },
                observacoes="Condição negociada",
            )
        )

        self.proposta = criar_proposta_servico(
            codigo=40,
            codigo_solicitacao=10,
            codigo_empresa=50,
            codigo_servico_ofertado_empresa=60,
            primeira_versao=self.versao,
        )

    def criar_contratacao_valida(self):
        return criar_contratacao_servico(
            codigo=1,
            solicitacao=self.solicitacao,
            proposta=self.proposta,
            versao_contratada=self.versao,
        )

    def criar_contratacoes_para_consulta(self):
        contratacao_1 = (
            self.criar_contratacao_valida()
        )

        contratacao_2 = (
            self.criar_contratacao_valida()
        )

        contratacao_2.codigo = 2
        contratacao_2.codigo_solicitacao = 11
        contratacao_2.codigo_cliente = 21
        contratacao_2.codigo_tipo_servico = 31
        contratacao_2.codigo_empresa = 51
        contratacao_2.codigo_proposta = 41
        contratacao_2.status = "CONFIRMADA"

        contratacao_3 = (
            self.criar_contratacao_valida()
        )

        contratacao_3.codigo = 3
        contratacao_3.status = "CONFIRMADA"

        registrar_processo_operacional(
            contratacao_3,
            "PROJETO",
            100,
        )

        return [
            contratacao_1,
            contratacao_2,
            contratacao_3,
        ]

    def test_criar_snapshot_contratacao(self):
        snapshot = (
            criar_snapshot_contratacao_servico(
                self.versao
            )
        )

        self.assertIsInstance(
            snapshot,
            SnapshotContratacaoServico,
        )

        self.assertEqual(
            snapshot.numero_versao_proposta,
            1,
        )

        self.assertEqual(
            snapshot.valor_contratado,
            15000.0,
        )

        self.assertEqual(
            snapshot.prazo_execucao_dias,
            30,
        )

    def test_snapshot_preserva_condicoes_comerciais(self):
        snapshot = (
            criar_snapshot_contratacao_servico(
                self.versao
            )
        )

        self.assertEqual(
            snapshot.itens_incluidos,
            (
                "Projeto",
                "Instalação",
            ),
        )

        self.assertEqual(
            snapshot.itens_nao_incluidos,
            (
                "Adequação do padrão",
            ),
        )

        self.assertEqual(
            dict(snapshot.garantias),
            {
                "instalacao": "12 meses",
            },
        )

        self.assertEqual(
            dict(snapshot.condicoes_comerciais),
            {
                "entrada": "30%",
            },
        )

    def test_snapshot_nao_compartilha_mapeamentos(self):
        snapshot = (
            criar_snapshot_contratacao_servico(
                self.versao
            )
        )

        self.assertIsNot(
            snapshot.garantias,
            self.versao.garantias,
        )

        self.assertIsNot(
            snapshot.condicoes_comerciais,
            self.versao.condicoes_comerciais,
        )

    def test_snapshot_rejeita_versao_invalida(self):
        with self.assertRaises(
            ValorInvalido
        ):
            criar_snapshot_contratacao_servico(
                object()
            )

    def test_criar_contratacao_servico(self):
        contratacao = criar_contratacao_servico(
            codigo=1,
            solicitacao=self.solicitacao,
            proposta=self.proposta,
            versao_contratada=self.versao,
        )

        self.assertIsInstance(
            contratacao,
            ContratacaoServico,
        )

        self.assertEqual(
            contratacao.codigo,
            1,
        )

        self.assertEqual(
            contratacao.codigo_solicitacao,
            10,
        )

        self.assertEqual(
            contratacao.codigo_cliente,
            20,
        )

        self.assertEqual(
            contratacao.codigo_tipo_servico,
            30,
        )

        self.assertEqual(
            contratacao.codigo_empresa,
            50,
        )

        self.assertEqual(
            contratacao.codigo_servico_ofertado_empresa,
            60,
        )

        self.assertEqual(
            contratacao.codigo_proposta,
            40,
        )

        self.assertEqual(
            contratacao.status,
            STATUS_INICIAL,
        )

    def test_contratacao_congela_snapshot(self):
        contratacao = criar_contratacao_servico(
            codigo=1,
            solicitacao=self.solicitacao,
            proposta=self.proposta,
            versao_contratada=self.versao,
        )

        self.assertIsNot(
            contratacao.snapshot,
            self.versao,
        )

        self.assertEqual(
            contratacao.snapshot.numero_versao_proposta,
            self.versao.numero,
        )

        self.assertEqual(
            contratacao.snapshot.valor_contratado,
            self.versao.valor,
        )

    def test_rejeita_codigo_contratacao_invalido(self):
        with self.assertRaises(
            ValorInvalido
        ):
            criar_contratacao_servico(
                codigo=0,
                solicitacao=self.solicitacao,
                proposta=self.proposta,
                versao_contratada=self.versao,
            )

    def test_rejeita_solicitacao_invalida(self):
        with self.assertRaises(
            TypeError
        ):
            criar_contratacao_servico(
                codigo=1,
                solicitacao=object(),
                proposta=self.proposta,
                versao_contratada=self.versao,
            )

    def test_rejeita_proposta_invalida(self):
        with self.assertRaises(
            TypeError
        ):
            criar_contratacao_servico(
                codigo=1,
                solicitacao=self.solicitacao,
                proposta=object(),
                versao_contratada=self.versao,
            )

    def test_rejeita_versao_invalida(self):
        with self.assertRaises(
            TypeError
        ):
            criar_contratacao_servico(
                codigo=1,
                solicitacao=self.solicitacao,
                proposta=self.proposta,
                versao_contratada=object(),
            )

    def test_rejeita_proposta_de_outra_solicitacao(self):
        proposta = criar_proposta_servico(
            codigo=41,
            codigo_solicitacao=999,
            codigo_empresa=50,
            codigo_servico_ofertado_empresa=60,
            primeira_versao=self.versao,
        )

        with self.assertRaises(
            ValorInvalido
        ):
            criar_contratacao_servico(
                codigo=1,
                solicitacao=self.solicitacao,
                proposta=proposta,
                versao_contratada=self.versao,
            )

    def test_rejeita_versao_de_outra_proposta(self):
        outra_versao = (
            criar_versao_proposta_servico(
                numero=1,
                valor=20000,
                prazo_execucao_dias=45,
                validade=date(2026, 12, 31),
                descricao_tecnica="Outra proposta",
            )
        )

        with self.assertRaises(
            ValorInvalido
        ):
            criar_contratacao_servico(
                codigo=1,
                solicitacao=self.solicitacao,
                proposta=self.proposta,
                versao_contratada=outra_versao,
            )

    def test_alterar_status_confirma_contratacao(
        self,
    ):
        contratacao = (
            self.criar_contratacao_valida()
        )

        alterar_status_contratacao_servico(
            contratacao,
            "CONFIRMADA",
        )

        self.assertEqual(
            contratacao.status,
            "CONFIRMADA",
        )

    def test_alterar_status_normaliza_valor(
        self,
    ):
        contratacao = (
            self.criar_contratacao_valida()
        )

        alterar_status_contratacao_servico(
            contratacao,
            "  confirmada  ",
        )

        self.assertEqual(
            contratacao.status,
            "CONFIRMADA",
        )

    def test_fluxo_local_da_contratacao(
        self,
    ):
        contratacao = (
            self.criar_contratacao_valida()
        )

        alterar_status_contratacao_servico(
            contratacao,
            "CONFIRMADA",
        )

        self.assertEqual(
            contratacao.status,
            "CONFIRMADA",
        )

        registrar_processo_operacional(
            contratacao,
            "PROJETO",
            100,
        )

        alterar_status_contratacao_servico(
            contratacao,
            "EM_ANDAMENTO",
        )

        self.assertEqual(
            contratacao.status,
            "EM_ANDAMENTO",
        )

        alterar_status_contratacao_servico(
            contratacao,
            "CONCLUIDA",
        )

        self.assertEqual(
            contratacao.status,
            "CONCLUIDA",
        )

    def test_cancelamento_em_estados_permitidos(
        self,
    ):
        estados = (
            "EM_FORMALIZACAO",
            "CONFIRMADA",
            "PROCESSO_GERADO",
            "EM_ANDAMENTO",
        )

        for status in estados:
            with self.subTest(
                status=status
            ):
                contratacao = (
                    self.criar_contratacao_valida()
                )

                if status in {
                    "PROCESSO_GERADO",
                    "EM_ANDAMENTO",
                }:
                    alterar_status_contratacao_servico(
                        contratacao,
                        "CONFIRMADA",
                    )

                    registrar_processo_operacional(
                        contratacao,
                        "PROJETO",
                        100,
                    )

                    if status == "EM_ANDAMENTO":
                        alterar_status_contratacao_servico(
                            contratacao,
                            "EM_ANDAMENTO",
                        )
                else:
                    contratacao.status = status

                alterar_status_contratacao_servico(
                    contratacao,
                    "CANCELADA",
                )

                self.assertEqual(
                    contratacao.status,
                    "CANCELADA",
                )

    def test_expiracao_exige_operacao_contextual(
        self,
    ):
        contratacao = (
            self.criar_contratacao_valida()
        )

        with self.assertRaises(
            ValorInvalido
        ):
            alterar_status_contratacao_servico(
                contratacao,
                "EXPIRADA",
            )

        self.assertEqual(
            contratacao.status,
            STATUS_INICIAL,
        )

    def test_processo_gerado_exige_operacao_contextual(
        self,
    ):
        contratacao = (
            self.criar_contratacao_valida()
        )

        alterar_status_contratacao_servico(
            contratacao,
            "CONFIRMADA",
        )

        with self.assertRaises(
            ValorInvalido
        ):
            alterar_status_contratacao_servico(
                contratacao,
                "PROCESSO_GERADO",
            )

        self.assertEqual(
            contratacao.status,
            "CONFIRMADA",
        )

    def test_transicao_invalida_preserva_status(
        self,
    ):
        contratacao = (
            self.criar_contratacao_valida()
        )

        status_anterior = (
            contratacao.status
        )

        with self.assertRaises(
            ValorInvalido
        ):
            alterar_status_contratacao_servico(
                contratacao,
                "CONCLUIDA",
            )

        self.assertEqual(
            contratacao.status,
            status_anterior,
        )

    def test_status_inexistente_preserva_contratacao(
        self,
    ):
        contratacao = (
            self.criar_contratacao_valida()
        )

        with self.assertRaises(
            ValorInvalido
        ):
            alterar_status_contratacao_servico(
                contratacao,
                "STATUS_INEXISTENTE",
            )

        self.assertEqual(
            contratacao.status,
            STATUS_INICIAL,
        )

    def test_alterar_status_exige_status_textual(
        self,
    ):
        for status in (
            None,
            1,
            True,
            [],
        ):
            with self.subTest(
                status=status
            ):
                contratacao = (
                    self.criar_contratacao_valida()
                )

                with self.assertRaises(
                    ValorInvalido
                ):
                    alterar_status_contratacao_servico(
                        contratacao,
                        status,
                    )

                self.assertEqual(
                    contratacao.status,
                    STATUS_INICIAL,
                )

    def test_alterar_status_exige_contratacao(
        self,
    ):
        with self.assertRaises(
            TypeError
        ):
            alterar_status_contratacao_servico(
                object(),
                "CONFIRMADA",
            )

    def test_contratacao_preserva_data_limite_formalizacao(
        self,
    ):
        contratacao = (
            self.criar_contratacao_valida()
        )

        self.assertEqual(
            contratacao.data_limite_formalizacao,
            date(2026, 12, 31),
        )

    def test_expirar_contratacao_apos_prazo(
        self,
    ):
        contratacao = (
            self.criar_contratacao_valida()
        )

        expirar_contratacao_servico(
            contratacao,
            date(2027, 1, 1),
        )

        self.assertEqual(
            contratacao.status,
            "EXPIRADA",
        )

    def test_nao_expira_no_ultimo_dia_do_prazo(
        self,
    ):
        contratacao = (
            self.criar_contratacao_valida()
        )

        with self.assertRaises(
            ValorInvalido
        ):
            expirar_contratacao_servico(
                contratacao,
                date(2026, 12, 31),
            )

        self.assertEqual(
            contratacao.status,
            STATUS_INICIAL,
        )

    def test_nao_expira_antes_do_prazo(
        self,
    ):
        contratacao = (
            self.criar_contratacao_valida()
        )

        with self.assertRaises(
            ValorInvalido
        ):
            expirar_contratacao_servico(
                contratacao,
                date(2026, 12, 30),
            )

        self.assertEqual(
            contratacao.status,
            STATUS_INICIAL,
        )

    def test_contratacao_confirmada_nao_expira(
        self,
    ):
        contratacao = (
            self.criar_contratacao_valida()
        )

        alterar_status_contratacao_servico(
            contratacao,
            "CONFIRMADA",
        )

        with self.assertRaises(
            ValorInvalido
        ):
            expirar_contratacao_servico(
                contratacao,
                date(2027, 1, 1),
            )

        self.assertEqual(
            contratacao.status,
            "CONFIRMADA",
        )

    def test_expirar_exige_data_valida(
        self,
    ):
        contratacao = (
            self.criar_contratacao_valida()
        )

        for valor in (
            None,
            "2027-01-01",
            1,
            True,
        ):
            with self.subTest(
                valor=valor
            ):
                with self.assertRaises(
                    ValorInvalido
                ):
                    expirar_contratacao_servico(
                        contratacao,
                        valor,
                    )

    def test_contratacao_inicia_sem_processo_operacional(
        self,
    ):
        contratacao = (
            self.criar_contratacao_valida()
        )

        self.assertIsNone(
            contratacao.processo_operacional
        )

    def test_registrar_processo_operacional(
        self,
    ):
        contratacao = (
            self.criar_contratacao_valida()
        )

        alterar_status_contratacao_servico(
            contratacao,
            "CONFIRMADA",
        )

        registrar_processo_operacional(
            contratacao,
            "projeto",
            100,
        )

        self.assertIsInstance(
            contratacao.processo_operacional,
            ReferenciaProcessoOperacional,
        )

        self.assertEqual(
            contratacao.processo_operacional.tipo,
            "PROJETO",
        )

        self.assertEqual(
            contratacao.processo_operacional.codigo,
            100,
        )

        self.assertEqual(
            contratacao.status,
            "PROCESSO_GERADO",
        )

    def test_nao_registra_processo_antes_da_confirmacao(
        self,
    ):
        contratacao = (
            self.criar_contratacao_valida()
        )

        with self.assertRaises(
            ValorInvalido
        ):
            registrar_processo_operacional(
                contratacao,
                "PROJETO",
                100,
            )

        self.assertIsNone(
            contratacao.processo_operacional
        )

        self.assertEqual(
            contratacao.status,
            STATUS_INICIAL,
        )

    def test_nao_registra_segundo_processo_operacional(
        self,
    ):
        contratacao = (
            self.criar_contratacao_valida()
        )

        alterar_status_contratacao_servico(
            contratacao,
            "CONFIRMADA",
        )

        registrar_processo_operacional(
            contratacao,
            "PROJETO",
            100,
        )

        with self.assertRaises(
            ValorInvalido
        ):
            registrar_processo_operacional(
                contratacao,
                "ORDEM_SERVICO",
                200,
            )

        self.assertEqual(
            contratacao.processo_operacional.codigo,
            100,
        )

        self.assertEqual(
            contratacao.status,
            "PROCESSO_GERADO",
        )

    def test_codigo_processo_invalido_preserva_contratacao(
        self,
    ):
        contratacao = (
            self.criar_contratacao_valida()
        )

        alterar_status_contratacao_servico(
            contratacao,
            "CONFIRMADA",
        )

        with self.assertRaises(
            ValorInvalido
        ):
            registrar_processo_operacional(
                contratacao,
                "PROJETO",
                0,
            )

        self.assertIsNone(
            contratacao.processo_operacional
        )

        self.assertEqual(
            contratacao.status,
            "CONFIRMADA",
        )

    def test_tipo_processo_invalido_preserva_contratacao(
        self,
    ):
        contratacao = (
            self.criar_contratacao_valida()
        )

        alterar_status_contratacao_servico(
            contratacao,
            "CONFIRMADA",
        )

        for tipo in (
            None,
            "",
            "   ",
            1,
            True,
        ):
            with self.subTest(
                tipo=tipo
            ):
                with self.assertRaises(
                    ValorInvalido
                ):
                    registrar_processo_operacional(
                        contratacao,
                        tipo,
                        100,
                    )

                self.assertIsNone(
                    contratacao.processo_operacional
                )

                self.assertEqual(
                    contratacao.status,
                    "CONFIRMADA",
                )

    def test_buscar_contratacao_por_codigo(
        self,
    ):
        contratacoes = (
            self.criar_contratacoes_para_consulta()
        )

        resultado = (
            buscar_contratacao_servico_por_codigo(
                contratacoes,
                2,
            )
        )

        self.assertIs(
            resultado,
            contratacoes[1],
        )

    def test_buscar_contratacao_inexistente_retorna_none(
        self,
    ):
        contratacoes = (
            self.criar_contratacoes_para_consulta()
        )

        resultado = (
            buscar_contratacao_servico_por_codigo(
                contratacoes,
                999,
            )
        )

        self.assertIsNone(
            resultado
        )

    def test_listar_contratacoes_por_solicitacao(
        self,
    ):
        contratacoes = (
            self.criar_contratacoes_para_consulta()
        )

        resultado = (
            listar_contratacoes_por_solicitacao(
                contratacoes,
                10,
            )
        )

        self.assertEqual(
            [item.codigo for item in resultado],
            [1, 3],
        )

    def test_listar_contratacoes_por_cliente(
        self,
    ):
        contratacoes = (
            self.criar_contratacoes_para_consulta()
        )

        resultado = listar_contratacoes_por_cliente(
            contratacoes,
            20,
        )

        self.assertEqual(
            [item.codigo for item in resultado],
            [1, 3],
        )

    def test_listar_contratacoes_por_empresa(
        self,
    ):
        contratacoes = (
            self.criar_contratacoes_para_consulta()
        )

        resultado = listar_contratacoes_por_empresa(
            contratacoes,
            50,
        )

        self.assertEqual(
            [item.codigo for item in resultado],
            [1, 3],
        )

    def test_listar_contratacoes_por_tipo_servico(
        self,
    ):
        contratacoes = (
            self.criar_contratacoes_para_consulta()
        )

        resultado = (
            listar_contratacoes_por_tipo_servico(
                contratacoes,
                30,
            )
        )

        self.assertEqual(
            [item.codigo for item in resultado],
            [1, 3],
        )

    def test_listar_contratacoes_por_proposta(
        self,
    ):
        contratacoes = (
            self.criar_contratacoes_para_consulta()
        )

        resultado = listar_contratacoes_por_proposta(
            contratacoes,
            40,
        )

        self.assertEqual(
            [item.codigo for item in resultado],
            [1, 3],
        )

    def test_listar_contratacoes_por_status_normaliza(
        self,
    ):
        contratacoes = (
            self.criar_contratacoes_para_consulta()
        )

        resultado = listar_contratacoes_por_status(
            contratacoes,
            "  confirmada  ",
        )

        self.assertEqual(
            [item.codigo for item in resultado],
            [2],
        )

    def test_listar_contratacoes_por_processo_operacional(
        self,
    ):
        contratacoes = (
            self.criar_contratacoes_para_consulta()
        )

        resultado = (
            listar_contratacoes_por_processo_operacional(
                contratacoes,
                " projeto ",
                100,
            )
        )

        self.assertEqual(
            [item.codigo for item in resultado],
            [3],
        )

    def test_consulta_multipla_pode_retornar_lista_vazia(
        self,
    ):
        contratacoes = (
            self.criar_contratacoes_para_consulta()
        )

        resultado = listar_contratacoes_por_empresa(
            contratacoes,
            999,
        )

        self.assertEqual(
            resultado,
            [],
        )

    def test_consulta_multipla_retorna_nova_lista(
        self,
    ):
        contratacoes = (
            self.criar_contratacoes_para_consulta()
        )

        resultado = (
            listar_contratacoes_por_solicitacao(
                contratacoes,
                10,
            )
        )

        self.assertIsNot(
            resultado,
            contratacoes,
        )

    def test_consulta_nao_altera_colecao_original(
        self,
    ):
        contratacoes = (
            self.criar_contratacoes_para_consulta()
        )

        ordem_original = [
            item.codigo
            for item in contratacoes
        ]

        listar_contratacoes_por_empresa(
            contratacoes,
            50,
        )

        self.assertEqual(
            [
                item.codigo
                for item in contratacoes
            ],
            ordem_original,
        )

    def test_consultas_rejeitam_codigo_invalido(
        self,
    ):
        contratacoes = (
            self.criar_contratacoes_para_consulta()
        )

        consultas = (
            buscar_contratacao_servico_por_codigo,
            listar_contratacoes_por_solicitacao,
            listar_contratacoes_por_cliente,
            listar_contratacoes_por_empresa,
            listar_contratacoes_por_tipo_servico,
            listar_contratacoes_por_proposta,
        )

        for consulta in consultas:
            for codigo in (
                0,
                -1,
                True,
                "1",
            ):
                with self.subTest(
                    consulta=consulta.__name__,
                    codigo=codigo,
                ):
                    with self.assertRaises(
                        ValorInvalido
                    ):
                        consulta(
                            contratacoes,
                            codigo,
                        )

    def test_consulta_por_status_rejeita_valor_invalido(
        self,
    ):
        contratacoes = (
            self.criar_contratacoes_para_consulta()
        )

        for status in (
            None,
            "",
            "   ",
            1,
            True,
        ):
            with self.subTest(
                status=status
            ):
                with self.assertRaises(
                    ValorInvalido
                ):
                    listar_contratacoes_por_status(
                        contratacoes,
                        status,
                    )

    def test_consulta_por_processo_rejeita_filtros_invalidos(
        self,
    ):
        contratacoes = (
            self.criar_contratacoes_para_consulta()
        )

        with self.assertRaises(
            ValorInvalido
        ):
            listar_contratacoes_por_processo_operacional(
                contratacoes,
                "",
                100,
            )

        with self.assertRaises(
            ValorInvalido
        ):
            listar_contratacoes_por_processo_operacional(
                contratacoes,
                "PROJETO",
                0,
            )

    def test_snapshot_nao_permite_alterar_atributo(
        self,
    ):
        snapshot = criar_snapshot_contratacao_servico(
            self.versao
        )

        with self.assertRaises(
            FrozenInstanceError
        ):
            snapshot.valor_contratado = 1

    def test_snapshot_nao_permite_alterar_garantias(
        self,
    ):
        snapshot = criar_snapshot_contratacao_servico(
            self.versao
        )

        with self.assertRaises(
            TypeError
        ):
            snapshot.garantias["instalacao"] = (
                "24 meses"
            )

    def test_snapshot_nao_permite_alterar_condicoes_comerciais(
        self,
    ):
        snapshot = criar_snapshot_contratacao_servico(
            self.versao
        )

        with self.assertRaises(
            TypeError
        ):
            snapshot.condicoes_comerciais["entrada"] = (
                "50%"
            )

    def test_referencia_processo_operacional_e_imutavel(
        self,
    ):
        referencia = ReferenciaProcessoOperacional(
            tipo="PROJETO",
            codigo=100,
        )

        with self.assertRaises(
            FrozenInstanceError
        ):
            referencia.codigo = 200

    def test_consulta_rejeita_colecao_none(
        self,
    ):
        with self.assertRaises(
            ValorInvalido
        ):
            listar_contratacoes_por_empresa(
                None,
                50,
            )

    def test_consulta_rejeita_colecao_textual(
        self,
    ):
        with self.assertRaises(
            ValorInvalido
        ):
            listar_contratacoes_por_empresa(
                "contratacoes",
                50,
            )

    def test_consulta_rejeita_colecao_nao_iteravel(
        self,
    ):
        with self.assertRaises(
            ValorInvalido
        ):
            listar_contratacoes_por_empresa(
                123,
                50,
            )

    def test_consulta_rejeita_elemento_invalido(
        self,
    ):
        contratacao = (
            self.criar_contratacao_valida()
        )

        with self.assertRaises(
            ValorInvalido
        ):
            listar_contratacoes_por_empresa(
                [
                    contratacao,
                    object(),
                ],
                50,
            )

    def test_consulta_aceita_colecao_vazia(
        self,
    ):
        resultado = listar_contratacoes_por_empresa(
            [],
            50,
        )

        self.assertEqual(
            resultado,
            [],
        )

    def test_operacao_rejeita_status_operacional_sem_processo(
        self,
    ):
        contratacao = (
            self.criar_contratacao_valida()
        )

        contratacao.status = "PROCESSO_GERADO"

        with self.assertRaises(
            ValorInvalido
        ):
            alterar_status_contratacao_servico(
                contratacao,
                "EM_ANDAMENTO",
            )

        self.assertEqual(
            contratacao.status,
            "PROCESSO_GERADO",
        )

    def test_operacao_rejeita_processo_em_formalizacao(
        self,
    ):
        contratacao = (
            self.criar_contratacao_valida()
        )

        contratacao.processo_operacional = (
            ReferenciaProcessoOperacional(
                tipo="PROJETO",
                codigo=100,
            )
        )

        with self.assertRaises(
            ValorInvalido
        ):
            alterar_status_contratacao_servico(
                contratacao,
                "CONFIRMADA",
            )

        self.assertEqual(
            contratacao.status,
            STATUS_INICIAL,
        )

    def test_operacao_rejeita_snapshot_invalido(
        self,
    ):
        contratacao = (
            self.criar_contratacao_valida()
        )

        contratacao.snapshot = object()

        with self.assertRaises(
            ValorInvalido
        ):
            alterar_status_contratacao_servico(
                contratacao,
                "CONFIRMADA",
            )

        self.assertEqual(
            contratacao.status,
            STATUS_INICIAL,
        )

    def test_expiracao_rejeita_data_limite_invalida(
        self,
    ):
        contratacao = (
            self.criar_contratacao_valida()
        )

        contratacao.data_limite_formalizacao = (
            "2026-12-31"
        )

        with self.assertRaises(
            ValorInvalido
        ):
            expirar_contratacao_servico(
                contratacao,
                date(2027, 1, 1),
            )

        self.assertEqual(
            contratacao.status,
            STATUS_INICIAL,
        )

    def test_operacao_rejeita_status_armazenado_nao_normalizado(
        self,
    ):
        contratacao = (
            self.criar_contratacao_valida()
        )

        contratacao.status = " confirmada "

        with self.assertRaises(
            ValorInvalido
        ):
            alterar_status_contratacao_servico(
                contratacao,
                "CANCELADA",
            )

        self.assertEqual(
            contratacao.status,
            " confirmada ",
        )

    def test_operacao_rejeita_referencia_processo_invalida(
        self,
    ):
        contratacao = (
            self.criar_contratacao_valida()
        )

        alterar_status_contratacao_servico(
            contratacao,
            "CONFIRMADA",
        )

        contratacao.processo_operacional = object()

        with self.assertRaises(
            ValorInvalido
        ):
            registrar_processo_operacional(
                contratacao,
                "PROJETO",
                100,
            )

        self.assertEqual(
            contratacao.status,
            "CONFIRMADA",
        )

if __name__ == "__main__":
    unittest.main()