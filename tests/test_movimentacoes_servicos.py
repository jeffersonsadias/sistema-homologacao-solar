import unittest
from dataclasses import FrozenInstanceError
from datetime import date, datetime
from types import MappingProxyType

from app.dominio.erros_dominio import (
    DadosObrigatoriosAusentes,
    ValorInvalido,
)

from app.dominio.movimentacoes_servicos import (
    MovimentacaoServico,
    TipoAtorMovimentacaoServico,
    buscar_movimentacao_por_codigo,
    criar_movimentacao_alteracao_status,
    criar_movimentacao_evento_contextual,
    criar_movimentacao_servico,
    listar_movimentacoes_por_ator,
    listar_movimentacoes_por_entidade,
    listar_movimentacoes_por_periodo,
    listar_movimentacoes_por_tipo_evento,
)


class TestMovimentacoesServicos(
    unittest.TestCase
):
    def criar_movimentacao_valida(
        self,
        **alteracoes,
    ):
        dados = {
            "codigo": 1,
            "entidade_tipo": "SOLICITACAO_SERVICO",
            "entidade_codigo": 10,
            "tipo_evento": "STATUS_ALTERADO",
            "data_hora": datetime(
                2026,
                8,
                21,
                10,
                0,
            ),
            "ator_tipo": "CLIENTE",
            "ator_codigo": 20,
            "descricao": (
                "Solicitação publicada pelo Cliente."
            ),
            "status_anterior": "EM_ELABORACAO",
            "status_novo": "PUBLICADA",
            "dados_anteriores": {
                "status": "EM_ELABORACAO",
            },
            "dados_novos": {
                "status": "PUBLICADA",
            },
        }

        dados.update(
            alteracoes
        )

        return criar_movimentacao_servico(
            **dados
        )

    def test_criar_movimentacao_servico(
        self,
    ):
        movimentacao = (
            self.criar_movimentacao_valida()
        )

        self.assertIsInstance(
            movimentacao,
            MovimentacaoServico,
        )

        self.assertEqual(
            movimentacao.codigo,
            1,
        )

        self.assertEqual(
            movimentacao.entidade_codigo,
            10,
        )

    def test_movimentacao_e_imutavel(
        self,
    ):
        movimentacao = (
            self.criar_movimentacao_valida()
        )

        with self.assertRaises(
            FrozenInstanceError
        ):
            movimentacao.tipo_evento = (
                "OUTRO_EVENTO"
            )

    def test_normaliza_tipo_entidade(
        self,
    ):
        movimentacao = (
            self.criar_movimentacao_valida(
                entidade_tipo=(
                    "  solicitacao_servico  "
                )
            )
        )

        self.assertEqual(
            movimentacao.entidade_tipo,
            "SOLICITACAO_SERVICO",
        )

    def test_normaliza_tipo_evento(
        self,
    ):
        movimentacao = (
            self.criar_movimentacao_valida(
                tipo_evento=(
                    "  status_alterado  "
                )
            )
        )

        self.assertEqual(
            movimentacao.tipo_evento,
            "STATUS_ALTERADO",
        )

    def test_normaliza_status(
        self,
    ):
        movimentacao = (
            self.criar_movimentacao_valida(
                status_anterior=(
                    "  em_elaboracao  "
                ),
                status_novo=(
                    "  publicada  "
                ),
            )
        )

        self.assertEqual(
            movimentacao.status_anterior,
            "EM_ELABORACAO",
        )

        self.assertEqual(
            movimentacao.status_novo,
            "PUBLICADA",
        )

    def test_status_pode_ser_ausente_em_evento_contextual(
        self,
    ):
        movimentacao = (
            self.criar_movimentacao_valida(
                tipo_evento="SOLICITACAO_PUBLICADA",
                status_anterior=None,
                status_novo=None,
                dados_anteriores={},
                dados_novos={},
            )
        )

        self.assertIsNone(
            movimentacao.status_anterior
        )

        self.assertIsNone(
            movimentacao.status_novo
        )

    def test_normaliza_descricao(
        self,
    ):
        movimentacao = (
            self.criar_movimentacao_valida(
                descricao=(
                    "  Solicitação   publicada  "
                )
            )
        )

        self.assertEqual(
            movimentacao.descricao,
            "Solicitação publicada",
        )

    def test_cliente_exige_codigo_ator(
        self,
    ):
        with self.assertRaises(
            DadosObrigatoriosAusentes
        ):
            self.criar_movimentacao_valida(
                ator_tipo="CLIENTE",
                ator_codigo=None,
            )

    def test_empresa_exige_codigo_ator(
        self,
    ):
        with self.assertRaises(
            DadosObrigatoriosAusentes
        ):
            self.criar_movimentacao_valida(
                ator_tipo="EMPRESA",
                ator_codigo=None,
            )

    def test_plataforma_nao_possui_codigo_ator(
        self,
    ):
        movimentacao = (
            self.criar_movimentacao_valida(
                ator_tipo="PLATAFORMA",
                ator_codigo=None,
            )
        )

        self.assertEqual(
            movimentacao.ator_tipo,
            (
                TipoAtorMovimentacaoServico
                .PLATAFORMA
            ),
        )

        self.assertIsNone(
            movimentacao.ator_codigo
        )

    def test_sistema_nao_possui_codigo_ator(
        self,
    ):
        movimentacao = (
            self.criar_movimentacao_valida(
                ator_tipo="SISTEMA",
                ator_codigo=None,
            )
        )

        self.assertEqual(
            movimentacao.ator_tipo,
            (
                TipoAtorMovimentacaoServico
                .SISTEMA
            ),
        )

    def test_rejeita_codigo_em_ator_institucional(
        self,
    ):
        for ator_tipo in (
            "PLATAFORMA",
            "SISTEMA",
        ):
            with self.subTest(
                ator_tipo=ator_tipo
            ):
                with self.assertRaises(
                    ValorInvalido
                ):
                    self.criar_movimentacao_valida(
                        ator_tipo=ator_tipo,
                        ator_codigo=99,
                    )

    def test_normaliza_tipo_ator(
        self,
    ):
        movimentacao = (
            self.criar_movimentacao_valida(
                ator_tipo="  empresa  ",
                ator_codigo=40,
            )
        )

        self.assertEqual(
            movimentacao.ator_tipo,
            TipoAtorMovimentacaoServico.EMPRESA,
        )

    def test_rejeita_tipo_ator_invalido(
        self,
    ):
        for ator_tipo in (
            "",
            "ADMIN",
            None,
            1,
        ):
            with self.subTest(
                ator_tipo=ator_tipo
            ):
                with self.assertRaises(
                    (
                        ValorInvalido,
                        DadosObrigatoriosAusentes,
                    )
                ):
                    self.criar_movimentacao_valida(
                        ator_tipo=ator_tipo,
                    )

    def test_snapshots_sao_imutaveis(
        self,
    ):
        movimentacao = (
            self.criar_movimentacao_valida()
        )

        self.assertIsInstance(
            movimentacao.dados_anteriores,
            MappingProxyType,
        )

        self.assertIsInstance(
            movimentacao.dados_novos,
            MappingProxyType,
        )

        with self.assertRaises(
            TypeError
        ):
            movimentacao.dados_novos[
                "status"
            ] = "ALTERADO"

    def test_snapshots_nao_compartilham_dicionario_externo(
        self,
    ):
        dados_novos = {
            "status": "PUBLICADA",
        }

        movimentacao = (
            self.criar_movimentacao_valida(
                dados_novos=dados_novos
            )
        )

        dados_novos["status"] = "CORROMPIDO"

        self.assertEqual(
            movimentacao.dados_novos["status"],
            "PUBLICADA",
        )

    def test_snapshots_ausentes_viram_mapeamento_vazio(
        self,
    ):
        movimentacao = (
            self.criar_movimentacao_valida(
                tipo_evento="SOLICITACAO_PUBLICADA",
                status_anterior=None,
                status_novo=None,
                dados_anteriores=None,
                dados_novos=None,
            )
        )

        self.assertEqual(
            dict(
                movimentacao.dados_anteriores
            ),
            {},
        )

        self.assertEqual(
            dict(
                movimentacao.dados_novos
            ),
            {},
        )

    def test_rejeita_snapshot_invalido(
        self,
    ):
        for valor in (
            [],
            "dados",
            123,
        ):
            with self.subTest(
                valor=valor
            ):
                with self.assertRaises(
                    ValorInvalido
                ):
                    self.criar_movimentacao_valida(
                        dados_novos=valor
                    )

    def test_rejeita_codigo_movimentacao_invalido(
        self,
    ):
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
                    self.criar_movimentacao_valida(
                        codigo=codigo
                    )

    def test_rejeita_codigo_entidade_invalido(
        self,
    ):
        for codigo in (
            0,
            -1,
            True,
            "10",
            None,
        ):
            with self.subTest(
                codigo=codigo
            ):
                with self.assertRaises(
                    ValorInvalido
                ):
                    self.criar_movimentacao_valida(
                        entidade_codigo=codigo
                    )

    def test_rejeita_tipo_entidade_vazio(
        self,
    ):
        with self.assertRaises(
            DadosObrigatoriosAusentes
        ):
            self.criar_movimentacao_valida(
                entidade_tipo="   "
            )

    def test_rejeita_tipo_evento_vazio(
        self,
    ):
        with self.assertRaises(
            DadosObrigatoriosAusentes
        ):
            self.criar_movimentacao_valida(
                tipo_evento="   "
            )

    def test_rejeita_descricao_vazia(
        self,
    ):
        with self.assertRaises(
            DadosObrigatoriosAusentes
        ):
            self.criar_movimentacao_valida(
                descricao="   "
            )

    def test_rejeita_data_hora_invalida(
        self,
    ):
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
                    self.criar_movimentacao_valida(
                        data_hora=valor
                    )

    def test_criar_movimentacao_alteracao_status(
        self,
    ):
        movimentacao = (
            criar_movimentacao_alteracao_status(
                codigo=2,
                entidade_tipo="SOLICITACAO_SERVICO",
                entidade_codigo=10,
                data_hora=datetime(
                    2026,
                    8,
                    21,
                    11,
                    0,
                ),
                ator_tipo="CLIENTE",
                ator_codigo=20,
                status_anterior="EM_ELABORACAO",
                status_novo="PUBLICADA",
                descricao="Solicitação publicada.",
            )
        )

        self.assertEqual(
            movimentacao.tipo_evento,
            "STATUS_ALTERADO",
        )

        self.assertEqual(
            movimentacao.status_anterior,
            "EM_ELABORACAO",
        )

        self.assertEqual(
            movimentacao.status_novo,
            "PUBLICADA",
        )

    def test_alteracao_status_normaliza_estados(
        self,
    ):
        movimentacao = (
            criar_movimentacao_alteracao_status(
                codigo=2,
                entidade_tipo="SOLICITACAO_SERVICO",
                entidade_codigo=10,
                data_hora=datetime(
                    2026,
                    8,
                    21,
                    11,
                    0,
                ),
                ator_tipo="CLIENTE",
                ator_codigo=20,
                status_anterior="  em_elaboracao ",
                status_novo=" publicada ",
                descricao="Solicitação publicada.",
            )
        )

        self.assertEqual(
            movimentacao.status_anterior,
            "EM_ELABORACAO",
        )

        self.assertEqual(
            movimentacao.status_novo,
            "PUBLICADA",
        )

    def test_alteracao_status_exige_status_anterior(
        self,
    ):
        with self.assertRaises(
            (
                ValorInvalido,
                DadosObrigatoriosAusentes,
            )
        ):
            criar_movimentacao_alteracao_status(
                codigo=2,
                entidade_tipo="SOLICITACAO_SERVICO",
                entidade_codigo=10,
                data_hora=datetime(
                    2026,
                    8,
                    21,
                    11,
                    0,
                ),
                ator_tipo="CLIENTE",
                ator_codigo=20,
                status_anterior=None,
                status_novo="PUBLICADA",
                descricao="Solicitação publicada.",
            )

    def test_alteracao_status_exige_status_novo(
        self,
    ):
        with self.assertRaises(
            (
                ValorInvalido,
                DadosObrigatoriosAusentes,
            )
        ):
            criar_movimentacao_alteracao_status(
                codigo=2,
                entidade_tipo="SOLICITACAO_SERVICO",
                entidade_codigo=10,
                data_hora=datetime(
                    2026,
                    8,
                    21,
                    11,
                    0,
                ),
                ator_tipo="CLIENTE",
                ator_codigo=20,
                status_anterior="EM_ELABORACAO",
                status_novo=None,
                descricao="Solicitação publicada.",
            )

    def test_alteracao_status_rejeita_estados_iguais(
        self,
    ):
        with self.assertRaises(
            ValorInvalido
        ):
            criar_movimentacao_alteracao_status(
                codigo=2,
                entidade_tipo="SOLICITACAO_SERVICO",
                entidade_codigo=10,
                data_hora=datetime(
                    2026,
                    8,
                    21,
                    11,
                    0,
                ),
                ator_tipo="CLIENTE",
                ator_codigo=20,
                status_anterior="PUBLICADA",
                status_novo=" publicada ",
                descricao="Alteração inválida.",
            )

    def test_alteracao_status_injeta_estados_nos_snapshots(
        self,
    ):
        movimentacao = (
            criar_movimentacao_alteracao_status(
                codigo=2,
                entidade_tipo="PROPOSTA_SERVICO",
                entidade_codigo=30,
                data_hora=datetime(
                    2026,
                    8,
                    21,
                    11,
                    0,
                ),
                ator_tipo="EMPRESA",
                ator_codigo=40,
                status_anterior="ENVIADA",
                status_novo="ACEITA",
                descricao="Proposta aceita.",
                dados_anteriores={
                    "valor": 1000,
                },
                dados_novos={
                    "valor": 1000,
                },
            )
        )

        self.assertEqual(
            movimentacao.dados_anteriores[
                "status"
            ],
            "ENVIADA",
        )

        self.assertEqual(
            movimentacao.dados_novos[
                "status"
            ],
            "ACEITA",
        )

        self.assertEqual(
            movimentacao.dados_novos[
                "valor"
            ],
            1000,
        )

    def test_alteracao_status_corrige_status_contraditorio_no_snapshot(
        self,
    ):
        movimentacao = (
            criar_movimentacao_alteracao_status(
                codigo=2,
                entidade_tipo="PROPOSTA_SERVICO",
                entidade_codigo=30,
                data_hora=datetime(
                    2026,
                    8,
                    21,
                    11,
                    0,
                ),
                ator_tipo="EMPRESA",
                ator_codigo=40,
                status_anterior="ENVIADA",
                status_novo="ACEITA",
                descricao="Proposta aceita.",
                dados_anteriores={
                    "status": "ERRADO",
                },
                dados_novos={
                    "status": "ERRADO",
                },
            )
        )

        self.assertEqual(
            movimentacao.dados_anteriores[
                "status"
            ],
            "ENVIADA",
        )

        self.assertEqual(
            movimentacao.dados_novos[
                "status"
            ],
            "ACEITA",
        )

    def test_criar_movimentacao_evento_contextual(
        self,
    ):
        movimentacao = (
            criar_movimentacao_evento_contextual(
                codigo=3,
                entidade_tipo="AUTORIZACAO_CONTATO",
                entidade_codigo=50,
                tipo_evento="CONTATO_LIBERADO",
                data_hora=datetime(
                    2026,
                    8,
                    21,
                    12,
                    0,
                ),
                ator_tipo="SISTEMA",
                ator_codigo=None,
                descricao=(
                    "Contato liberado para a Empresa."
                ),
                dados_novos={
                    "ativo": True,
                },
            )
        )

        self.assertEqual(
            movimentacao.tipo_evento,
            "CONTATO_LIBERADO",
        )

        self.assertIsNone(
            movimentacao.status_anterior
        )

        self.assertIsNone(
            movimentacao.status_novo
        )

    def test_evento_contextual_normaliza_tipo_evento(
        self,
    ):
        movimentacao = (
            criar_movimentacao_evento_contextual(
                codigo=3,
                entidade_tipo="CONTRATACAO_SERVICO",
                entidade_codigo=60,
                tipo_evento=(
                    "  contratacao_criada  "
                ),
                data_hora=datetime(
                    2026,
                    8,
                    21,
                    12,
                    0,
                ),
                ator_tipo="SISTEMA",
                ator_codigo=None,
                descricao="Contratação criada.",
            )
        )

        self.assertEqual(
            movimentacao.tipo_evento,
            "CONTRATACAO_CRIADA",
        )

    def test_evento_contextual_rejeita_status_alterado(
        self,
    ):
        with self.assertRaises(
            ValorInvalido
        ):
            criar_movimentacao_evento_contextual(
                codigo=3,
                entidade_tipo="SOLICITACAO_SERVICO",
                entidade_codigo=10,
                tipo_evento="STATUS_ALTERADO",
                data_hora=datetime(
                    2026,
                    8,
                    21,
                    12,
                    0,
                ),
                ator_tipo="SISTEMA",
                ator_codigo=None,
                descricao="Evento inválido.",
            )

    def test_evento_contextual_preserva_snapshots(
        self,
    ):
        anteriores = {
            "ativo": True,
        }

        novos = {
            "ativo": False,
        }

        movimentacao = (
            criar_movimentacao_evento_contextual(
                codigo=3,
                entidade_tipo="AUTORIZACAO_CONTATO",
                entidade_codigo=50,
                tipo_evento="CONTATO_REVOGADO",
                data_hora=datetime(
                    2026,
                    8,
                    21,
                    12,
                    0,
                ),
                ator_tipo="SISTEMA",
                ator_codigo=None,
                descricao="Contato revogado.",
                dados_anteriores=anteriores,
                dados_novos=novos,
            )
        )

        anteriores["ativo"] = False
        novos["ativo"] = True

        self.assertTrue(
            movimentacao.dados_anteriores[
                "ativo"
            ]
        )

        self.assertFalse(
            movimentacao.dados_novos[
                "ativo"
            ]
        )

    def test_eventos_contextuais_distintos_sao_aceitos(
        self,
    ):
        eventos = (
            "PROPOSTA_ACEITA",
            "CONTRATACAO_CRIADA",
            "PROCESSO_OPERACIONAL_GERADO",
            "EXECUCAO_REGISTRADA",
            "CONTATO_LIBERADO",
            "CONTATO_REVOGADO",
            "CONCLUSAO_CONTESTADA",
        )

        for indice, evento in enumerate(
            eventos,
            start=1,
        ):
            with self.subTest(
                evento=evento
            ):
                movimentacao = (
                    criar_movimentacao_evento_contextual(
                        codigo=indice,
                        entidade_tipo=(
                            "SERVICO_PLATAFORMA"
                        ),
                        entidade_codigo=10,
                        tipo_evento=evento,
                        data_hora=datetime(
                            2026,
                            8,
                            21,
                            12,
                            0,
                        ),
                        ator_tipo="SISTEMA",
                        ator_codigo=None,
                        descricao=(
                            "Evento contextual registrado."
                        ),
                    )
                )

                self.assertEqual(
                    movimentacao.tipo_evento,
                    evento,
                )

    def criar_colecao_movimentacoes(
        self,
    ):
        return (
            self.criar_movimentacao_valida(
                codigo=1,
                entidade_tipo="SOLICITACAO_SERVICO",
                entidade_codigo=10,
                tipo_evento="SOLICITACAO_PUBLICADA",
                ator_tipo="CLIENTE",
                ator_codigo=20,
                data_hora=datetime(
                    2026, 8, 21, 10, 0
                ),
                status_anterior=None,
                status_novo=None,
                dados_anteriores={},
                dados_novos={},
            ),
            self.criar_movimentacao_valida(
                codigo=2,
                entidade_tipo="SOLICITACAO_SERVICO",
                entidade_codigo=10,
                tipo_evento="STATUS_ALTERADO",
                ator_tipo="EMPRESA",
                ator_codigo=40,
                data_hora=datetime(
                    2026, 8, 21, 11, 0
                ),
            ),
            self.criar_movimentacao_valida(
                codigo=3,
                entidade_tipo="PROPOSTA_SERVICO",
                entidade_codigo=10,
                tipo_evento="PROPOSTA_ACEITA",
                ator_tipo="CLIENTE",
                ator_codigo=20,
                data_hora=datetime(
                    2026, 8, 21, 12, 0
                ),
                status_anterior=None,
                status_novo=None,
                dados_anteriores={},
                dados_novos={},
            ),
            self.criar_movimentacao_valida(
                codigo=4,
                entidade_tipo="AUTORIZACAO_CONTATO",
                entidade_codigo=50,
                tipo_evento="CONTATO_LIBERADO",
                ator_tipo="SISTEMA",
                ator_codigo=None,
                data_hora=datetime(
                    2026, 8, 21, 13, 0
                ),
                status_anterior=None,
                status_novo=None,
                dados_anteriores={},
                dados_novos={},
            ),
        )

    def test_buscar_movimentacao_por_codigo(
        self,
    ):
        movimentacoes = (
            self.criar_colecao_movimentacoes()
        )

        resultado = buscar_movimentacao_por_codigo(
            movimentacoes,
            3,
        )

        self.assertIsNotNone(
            resultado
        )

        self.assertEqual(
            resultado.codigo,
            3,
        )

    def test_buscar_movimentacao_inexistente_retorna_none(
        self,
    ):
        resultado = buscar_movimentacao_por_codigo(
            self.criar_colecao_movimentacoes(),
            99,
        )

        self.assertIsNone(
            resultado
        )

    def test_listar_movimentacoes_por_entidade(
        self,
    ):
        resultado = listar_movimentacoes_por_entidade(
            self.criar_colecao_movimentacoes(),
            "solicitacao_servico",
            10,
        )

        self.assertEqual(
            tuple(
                item.codigo
                for item in resultado
            ),
            (1, 2),
        )

    def test_consulta_entidade_considera_tipo_e_codigo(
        self,
    ):
        resultado = listar_movimentacoes_por_entidade(
            self.criar_colecao_movimentacoes(),
            "PROPOSTA_SERVICO",
            10,
        )

        self.assertEqual(
            tuple(
                item.codigo
                for item in resultado
            ),
            (3,),
        )

    def test_listar_movimentacoes_por_tipo_evento(
        self,
    ):
        resultado = (
            listar_movimentacoes_por_tipo_evento(
                self.criar_colecao_movimentacoes(),
                "  proposta_aceita ",
            )
        )

        self.assertEqual(
            tuple(
                item.codigo
                for item in resultado
            ),
            (3,),
        )

    def test_listar_movimentacoes_por_cliente(
        self,
    ):
        resultado = listar_movimentacoes_por_ator(
            self.criar_colecao_movimentacoes(),
            "cliente",
            20,
        )

        self.assertEqual(
            tuple(
                item.codigo
                for item in resultado
            ),
            (1, 3),
        )

    def test_listar_movimentacoes_por_empresa(
        self,
    ):
        resultado = listar_movimentacoes_por_ator(
            self.criar_colecao_movimentacoes(),
            "EMPRESA",
            40,
        )

        self.assertEqual(
            tuple(
                item.codigo
                for item in resultado
            ),
            (2,),
        )

    def test_listar_movimentacoes_por_sistema(
        self,
    ):
        resultado = listar_movimentacoes_por_ator(
            self.criar_colecao_movimentacoes(),
            "SISTEMA",
        )

        self.assertEqual(
            tuple(
                item.codigo
                for item in resultado
            ),
            (4,),
        )

    def test_listar_movimentacoes_por_periodo(
        self,
    ):
        resultado = listar_movimentacoes_por_periodo(
            self.criar_colecao_movimentacoes(),
            datetime(2026, 8, 21, 11, 0),
            datetime(2026, 8, 21, 12, 0),
        )

        self.assertEqual(
            tuple(
                item.codigo
                for item in resultado
            ),
            (2, 3),
        )

    def test_periodo_inclui_extremidades(
        self,
    ):
        resultado = listar_movimentacoes_por_periodo(
            self.criar_colecao_movimentacoes(),
            datetime(2026, 8, 21, 10, 0),
            datetime(2026, 8, 21, 13, 0),
        )

        self.assertEqual(
            len(resultado),
            4,
        )

    def test_periodo_rejeita_fim_anterior_inicio(
        self,
    ):
        with self.assertRaises(
            ValorInvalido
        ):
            listar_movimentacoes_por_periodo(
                self.criar_colecao_movimentacoes(),
                datetime(2026, 8, 21, 13, 0),
                datetime(2026, 8, 21, 10, 0),
            )

    def test_consultas_sem_resultado_retornam_tupla_vazia(
        self,
    ):
        resultado = (
            listar_movimentacoes_por_tipo_evento(
                self.criar_colecao_movimentacoes(),
                "EVENTO_INEXISTENTE",
            )
        )

        self.assertEqual(
            resultado,
            (),
        )

    def test_consultas_preservam_ordem_da_colecao(
        self,
    ):
        resultado = listar_movimentacoes_por_ator(
            self.criar_colecao_movimentacoes(),
            "CLIENTE",
            20,
        )

        self.assertEqual(
            tuple(
                item.codigo
                for item in resultado
            ),
            (1, 3),
        )

    def test_consultas_retornam_tupla(
        self,
    ):
        resultado = listar_movimentacoes_por_entidade(
            self.criar_colecao_movimentacoes(),
            "SOLICITACAO_SERVICO",
            10,
        )

        self.assertIsInstance(
            resultado,
            tuple,
        )

    def test_consultas_rejeitam_colecao_invalida(
        self,
    ):
        for valor in (
            None,
            "movimentacoes",
            123,
            {},
        ):
            with self.subTest(
                valor=valor
            ):
                with self.assertRaises(
                    ValorInvalido
                ):
                    buscar_movimentacao_por_codigo(
                        valor,
                        1,
                    )

    def test_consultas_rejeitam_item_invalido(
        self,
    ):
        movimentacao = (
            self.criar_movimentacao_valida()
        )

        with self.assertRaises(
            ValorInvalido
        ):
            listar_movimentacoes_por_entidade(
                (
                    movimentacao,
                    object(),
                ),
                "SOLICITACAO_SERVICO",
                10,
            )

    def test_consulta_ator_respeita_regra_do_codigo(
        self,
    ):
        with self.assertRaises(
            DadosObrigatoriosAusentes
        ):
            listar_movimentacoes_por_ator(
                self.criar_colecao_movimentacoes(),
                "CLIENTE",
            )

        with self.assertRaises(
            ValorInvalido
        ):
            listar_movimentacoes_por_ator(
                self.criar_colecao_movimentacoes(),
                "SISTEMA",
                1,
            )

    def test_factory_generica_rejeita_status_alterado_sem_estados(
        self,
    ):
        with self.assertRaises(
            DadosObrigatoriosAusentes
        ):
            self.criar_movimentacao_valida(
                tipo_evento="STATUS_ALTERADO",
                status_anterior=None,
                status_novo=None,
            )

    def test_factory_generica_rejeita_status_alterado_com_estados_iguais(
        self,
    ):
        with self.assertRaises(
            ValorInvalido
        ):
            self.criar_movimentacao_valida(
                status_anterior="PUBLICADA",
                status_novo=" publicada ",
                dados_anteriores={
                    "status": "PUBLICADA",
                },
                dados_novos={
                    "status": "PUBLICADA",
                },
            )

    def test_factory_generica_rejeita_evento_contextual_com_estados(
        self,
    ):
        with self.assertRaises(
            ValorInvalido
        ):
            self.criar_movimentacao_valida(
                tipo_evento="PROPOSTA_ACEITA",
            )

    def test_factory_generica_rejeita_snapshot_anterior_incoerente(
        self,
    ):
        with self.assertRaises(
            ValorInvalido
        ):
            self.criar_movimentacao_valida(
                dados_anteriores={
                    "status": "CANCELADA",
                },
            )

    def test_factory_generica_rejeita_snapshot_novo_incoerente(
        self,
    ):
        with self.assertRaises(
            ValorInvalido
        ):
            self.criar_movimentacao_valida(
                dados_novos={
                    "status": "CANCELADA",
                },
            )

    def test_consulta_rejeita_movimentacao_com_codigo_adulterado(
        self,
    ):
        movimentacao = (
            self.criar_movimentacao_valida()
        )

        object.__setattr__(
            movimentacao,
            "codigo",
            0,
        )

        with self.assertRaises(
            ValorInvalido
        ):
            buscar_movimentacao_por_codigo(
                (movimentacao,),
                1,
            )

    def test_consulta_rejeita_tipo_evento_adulterado(
        self,
    ):
        movimentacao = (
            self.criar_movimentacao_valida()
        )

        object.__setattr__(
            movimentacao,
            "tipo_evento",
            " evento_invalido ",
        )

        with self.assertRaises(
            ValorInvalido
        ):
            listar_movimentacoes_por_tipo_evento(
                (movimentacao,),
                "STATUS_ALTERADO",
            )

    def test_consulta_rejeita_ator_adulterado(
        self,
    ):
        movimentacao = (
            self.criar_movimentacao_valida()
        )

        object.__setattr__(
            movimentacao,
            "ator_codigo",
            None,
        )

        with self.assertRaises(
            DadosObrigatoriosAusentes
        ):
            listar_movimentacoes_por_entidade(
                (movimentacao,),
                "SOLICITACAO_SERVICO",
                10,
            )

    def test_consulta_rejeita_status_alterado_sem_status_anterior(
        self,
    ):
        movimentacao = (
            self.criar_movimentacao_valida()
        )

        object.__setattr__(
            movimentacao,
            "status_anterior",
            None,
        )

        with self.assertRaises(
            (
                ValorInvalido,
                DadosObrigatoriosAusentes,
            )
        ):
            listar_movimentacoes_por_entidade(
                (movimentacao,),
                "SOLICITACAO_SERVICO",
                10,
            )

    def test_consulta_rejeita_snapshot_adulterado(
        self,
    ):
        movimentacao = (
            self.criar_movimentacao_valida()
        )

        object.__setattr__(
            movimentacao,
            "dados_novos",
            {
                "status": "CANCELADA",
            },
        )

        with self.assertRaises(
            ValorInvalido
        ):
            listar_movimentacoes_por_entidade(
                (movimentacao,),
                "SOLICITACAO_SERVICO",
                10,
            )

    def test_consulta_rejeita_data_hora_adulterada(
        self,
    ):
        movimentacao = (
            self.criar_movimentacao_valida()
        )

        object.__setattr__(
            movimentacao,
            "data_hora",
            "2026-08-21",
        )

        with self.assertRaises(
            ValorInvalido
        ):
            listar_movimentacoes_por_periodo(
                (movimentacao,),
                datetime(2026, 8, 21, 0, 0),
                datetime(2026, 8, 22, 0, 0),
            )

    def test_consulta_rejeita_evento_contextual_adulterado_com_status(
        self,
    ):
        movimentacao = (
            criar_movimentacao_evento_contextual(
                codigo=99,
                entidade_tipo="AUTORIZACAO_CONTATO",
                entidade_codigo=50,
                tipo_evento="CONTATO_LIBERADO",
                data_hora=datetime(
                    2026, 8, 21, 12, 0
                ),
                ator_tipo="SISTEMA",
                ator_codigo=None,
                descricao="Contato liberado.",
            )
        )

        object.__setattr__(
            movimentacao,
            "status_novo",
            "ATIVO",
        )

        with self.assertRaises(
            ValorInvalido
        ):
            buscar_movimentacao_por_codigo(
                (movimentacao,),
                99,
            )

if __name__ == "__main__":
    unittest.main()