import unittest

from dataclasses import FrozenInstanceError
from datetime import date

from app.dominio.erros_dominio import (
    DadosObrigatoriosAusentes,
    OperacaoNaoPermitida,
    ValorInvalido,
)

from app.dominio.areas_atendimento import (
    criar_area_atendimento,
)

from app.dominio.servicos_empresa import (
    ModeloPrecificacao,
    ServicoOfertadoEmpresa,
)

from app.dominio.solicitacoes_servico import (
    ModalidadeSolicitacaoServico,
    OrigemSolicitacaoServico,
    SolicitacaoServico,
)

from app.dominio.propostas_servico import (
    PropostaServico,
    VersaoPropostaServico,
    alterar_status_proposta_servico,
    buscar_proposta_servico_por_codigo,
    converter_proposta_servico_para_dicionario,
    converter_versao_proposta_para_dicionario,
    criar_proposta_servico,
    criar_versao_proposta_servico,
    expirar_proposta_servico,
    listar_propostas_por_empresa,
    listar_propostas_por_servico_ofertado,
    listar_propostas_por_solicitacao,
    listar_propostas_por_status,
    registrar_nova_versao_proposta_servico,
    obter_proximo_numero_versao,
    obter_versao_atual_proposta,
    validar_contexto_proposta_servico,
    validar_permissao_alteracao_comercial,
    versao_proposta_esta_valida,
)

class TestVersaoPropostaServico(unittest.TestCase):

    def criar_versao_valida(self):
        return criar_versao_proposta_servico(
            numero=1,
            valor=1500,
            prazo_execucao_dias=10,
            validade=date(
                2026,
                9,
                15,
            ),
            descricao_tecnica=(
                "Execução completa do serviço."
            ),
            itens_incluidos=[
                "Mão de obra",
                "Deslocamento",
            ],
            itens_nao_incluidos=[
                "Materiais adicionais",
            ],
            garantias={
                "servico_dias": 90,
            },
            condicoes_comerciais={
                "forma_pagamento": "PIX",
            },
            observacoes=(
                "Execução mediante agendamento."
            ),
        )

    def test_criar_versao_proposta_servico(
        self,
    ):
        versao = self.criar_versao_valida()

        self.assertIsInstance(
            versao,
            VersaoPropostaServico,
        )

        self.assertEqual(
            versao.numero,
            1,
        )

        self.assertEqual(
            versao.valor,
            1500.0,
        )

        self.assertEqual(
            versao.prazo_execucao_dias,
            10,
        )

    def test_valor_deve_ser_positivo(
        self,
    ):
        for valor in (
            0,
            -1,
            True,
            "1500",
        ):
            with self.subTest(
                valor=valor
            ):
                with self.assertRaises(
                    ValorInvalido
                ):
                    criar_versao_proposta_servico(
                        numero=1,
                        valor=valor,
                        prazo_execucao_dias=10,
                        validade=date(
                            2026,
                            9,
                            15,
                        ),
                        descricao_tecnica="Serviço",
                    )

    def test_numero_versao_deve_ser_positivo(
        self,
    ):
        for numero in (
            0,
            -1,
            True,
            1.5,
        ):
            with self.subTest(
                numero=numero
            ):
                with self.assertRaises(
                    ValorInvalido
                ):
                    criar_versao_proposta_servico(
                        numero=numero,
                        valor=1500,
                        prazo_execucao_dias=10,
                        validade=date(
                            2026,
                            9,
                            15,
                        ),
                        descricao_tecnica="Serviço",
                    )

    def test_prazo_execucao_deve_ser_positivo(
        self,
    ):
        for prazo in (
            0,
            -1,
            True,
            10.5,
        ):
            with self.subTest(
                prazo=prazo
            ):
                with self.assertRaises(
                    ValorInvalido
                ):
                    criar_versao_proposta_servico(
                        numero=1,
                        valor=1500,
                        prazo_execucao_dias=prazo,
                        validade=date(
                            2026,
                            9,
                            15,
                        ),
                        descricao_tecnica="Serviço",
                    )

    def test_descricao_tecnica_obrigatoria(
        self,
    ):
        for descricao in (
            "",
            "   ",
        ):
            with self.subTest(
                descricao=descricao
            ):
                with self.assertRaises(
                    DadosObrigatoriosAusentes
                ):
                    criar_versao_proposta_servico(
                        numero=1,
                        valor=1500,
                        prazo_execucao_dias=10,
                        validade=date(
                            2026,
                            9,
                            15,
                        ),
                        descricao_tecnica=descricao,
                    )

    def test_versao_deve_ser_imutavel(
        self,
    ):
        versao = self.criar_versao_valida()

        with self.assertRaises(
            FrozenInstanceError
        ):
            versao.valor = 2000

    def test_listas_comerciais_sao_imutaveis(
        self,
    ):
        versao = self.criar_versao_valida()

        self.assertIsInstance(
            versao.itens_incluidos,
            tuple,
        )

        self.assertIsInstance(
            versao.itens_nao_incluidos,
            tuple,
        )

    def test_mapeamentos_comerciais_sao_protegidos(
        self,
    ):
        versao = self.criar_versao_valida()

        with self.assertRaises(
            TypeError
        ):
            versao.garantias[
                "servico_dias"
            ] = 180

        with self.assertRaises(
            TypeError
        ):
            versao.condicoes_comerciais[
                "forma_pagamento"
            ] = "Cartão"

    def test_versao_nao_compartilha_estruturas_externas(
        self,
    ):
        itens = [
            "Mão de obra",
        ]

        garantias = {
            "dias": 90,
        }

        versao = criar_versao_proposta_servico(
            numero=1,
            valor=1500,
            prazo_execucao_dias=10,
            validade=date(
                2026,
                9,
                15,
            ),
            descricao_tecnica="Serviço",
            itens_incluidos=itens,
            garantias=garantias,
        )

        itens.append(
            "Novo item"
        )

        garantias["dias"] = 180

        self.assertEqual(
            versao.itens_incluidos,
            (
                "Mão de obra",
            ),
        )

        self.assertEqual(
            versao.garantias["dias"],
            90,
        )

    def test_converter_versao_para_dicionario(
        self,
    ):
        versao = self.criar_versao_valida()

        dados = (
            converter_versao_proposta_para_dicionario(
                versao
            )
        )

        self.assertEqual(
            dados["numero"],
            1,
        )

        self.assertEqual(
            dados["valor"],
            1500.0,
        )

        self.assertEqual(
            dados["prazo_execucao_dias"],
            10,
        )

        self.assertEqual(
            dados["validade"],
            "2026-09-15",
        )

        self.assertEqual(
            dados["descricao_tecnica"],
            "Execução completa do serviço.",
        )

    def test_converter_versao_converte_colecoes(
        self,
    ):
        versao = self.criar_versao_valida()

        dados = (
            converter_versao_proposta_para_dicionario(
                versao
            )
        )

        self.assertIsInstance(
            dados["itens_incluidos"],
            list,
        )

        self.assertIsInstance(
            dados["itens_nao_incluidos"],
            list,
        )

        self.assertIsInstance(
            dados["garantias"],
            dict,
        )

        self.assertIsInstance(
            dados["condicoes_comerciais"],
            dict,
        )

    def test_dicionario_da_versao_nao_altera_original(
        self,
    ):
        versao = self.criar_versao_valida()

        dados = (
            converter_versao_proposta_para_dicionario(
                versao
            )
        )

        dados["itens_incluidos"].append(
            "Novo item"
        )

        dados["garantias"][
            "servico_dias"
        ] = 180

        dados["condicoes_comerciais"][
            "forma_pagamento"
        ] = "Cartão"

        self.assertNotIn(
            "Novo item",
            versao.itens_incluidos,
        )

        self.assertEqual(
            versao.garantias["servico_dias"],
            90,
        )

        self.assertEqual(
            versao.condicoes_comerciais[
                "forma_pagamento"
            ],
            "PIX",
        )

    def test_converter_versao_exige_versao_valida(
        self,
    ):
        with self.assertRaises(
            ValorInvalido
        ):
            converter_versao_proposta_para_dicionario(
                {
                    "numero": 1,
                }
            )

    def test_versao_com_validade_futura_esta_valida(
        self,
    ):
        versao = self.criar_versao_valida()

        resultado = versao_proposta_esta_valida(
            versao,
            data_referencia=date(
                2026,
                9,
                14,
            ),
        )

        self.assertTrue(
            resultado
        )

    def test_versao_permanece_valida_no_dia_da_validade(
        self,
    ):
        versao = self.criar_versao_valida()

        resultado = versao_proposta_esta_valida(
            versao,
            data_referencia=date(
                2026,
                9,
                15,
            ),
        )

        self.assertTrue(
            resultado
        )

    def test_versao_com_validade_passada_esta_expirada(
        self,
    ):
        versao = self.criar_versao_valida()

        resultado = versao_proposta_esta_valida(
            versao,
            data_referencia=date(
                2026,
                9,
                16,
            ),
        )

        self.assertFalse(
            resultado
        )

    def test_consulta_validade_exige_versao_valida(
        self,
    ):
        with self.assertRaises(
            ValorInvalido
        ):
            versao_proposta_esta_valida(
                {
                    "validade": date(
                        2026,
                        9,
                        15,
                    ),
                },
                data_referencia=date(
                    2026,
                    9,
                    14,
                ),
            )

    def test_consulta_validade_exige_data_referencia_valida(
        self,
    ):
        versao = self.criar_versao_valida()

        for data_referencia in (
            "2026-09-14",
            20260914,
            True,
        ):
            with self.subTest(
                data_referencia=data_referencia
            ):
                with self.assertRaises(
                    ValorInvalido
                ):
                    versao_proposta_esta_valida(
                        versao,
                        data_referencia=(
                            data_referencia
                        ),
                    )

    def test_consulta_validade_sem_data_referencia(
        self,
    ):
        versao = criar_versao_proposta_servico(
            numero=1,
            valor=1500,
            prazo_execucao_dias=10,
            validade=date.today(),
            descricao_tecnica="Serviço",
        )

        resultado = versao_proposta_esta_valida(
            versao
        )

        self.assertTrue(
            resultado
        )

    def test_item_nao_pode_ser_incluido_e_nao_incluido(
        self,
    ):
        with self.assertRaises(
            ValorInvalido
        ):
            criar_versao_proposta_servico(
                numero=1,
                valor=1500,
                prazo_execucao_dias=10,
                validade=date(
                    2026,
                    9,
                    15,
                ),
                descricao_tecnica="Serviço",
                itens_incluidos=[
                    "Deslocamento",
                ],
                itens_nao_incluidos=[
                    "Deslocamento",
                ],
            )

    def test_conflito_de_itens_ignora_maiusculas_minusculas(
        self,
    ):
        with self.assertRaises(
            ValorInvalido
        ):
            criar_versao_proposta_servico(
                numero=1,
                valor=1500,
                prazo_execucao_dias=10,
                validade=date(
                    2026,
                    9,
                    15,
                ),
                descricao_tecnica="Serviço",
                itens_incluidos=[
                    "Mão de obra",
                ],
                itens_nao_incluidos=[
                    "MÃO DE OBRA",
                ],
            )

    def test_conflito_de_itens_ignora_espacos_externos(
        self,
    ):
        with self.assertRaises(
            ValorInvalido
        ):
            criar_versao_proposta_servico(
                numero=1,
                valor=1500,
                prazo_execucao_dias=10,
                validade=date(
                    2026,
                    9,
                    15,
                ),
                descricao_tecnica="Serviço",
                itens_incluidos=[
                    "Deslocamento",
                ],
                itens_nao_incluidos=[
                    "   deslocamento   ",
                ],
            )

    def test_itens_comerciais_distintos_sao_permitidos(
        self,
    ):
        versao = criar_versao_proposta_servico(
            numero=1,
            valor=1500,
            prazo_execucao_dias=10,
            validade=date(
                2026,
                9,
                15,
            ),
            descricao_tecnica="Serviço",
            itens_incluidos=[
                "Mão de obra",
                "Deslocamento",
            ],
            itens_nao_incluidos=[
                "Materiais",
                "Taxas",
            ],
        )

        self.assertEqual(
            versao.itens_incluidos,
            (
                "Mão de obra",
                "Deslocamento",
            ),
        )

        self.assertEqual(
            versao.itens_nao_incluidos,
            (
                "Materiais",
                "Taxas",
            ),
        )

    def test_itens_incluidos_nao_permite_duplicidade(
        self,
    ):
        with self.assertRaises(
            ValorInvalido
        ):
            criar_versao_proposta_servico(
                numero=1,
                valor=1500,
                prazo_execucao_dias=10,
                validade=date(
                    2026,
                    9,
                    15,
                ),
                descricao_tecnica="Serviço",
                itens_incluidos=[
                    "Mão de obra",
                    "Mão de obra",
                ],
            )

    def test_itens_nao_incluidos_nao_permite_duplicidade(
        self,
    ):
        with self.assertRaises(
            ValorInvalido
        ):
            criar_versao_proposta_servico(
                numero=1,
                valor=1500,
                prazo_execucao_dias=10,
                validade=date(
                    2026,
                    9,
                    15,
                ),
                descricao_tecnica="Serviço",
                itens_nao_incluidos=[
                    "Materiais",
                    "Materiais",
                ],
            )

    def test_duplicidade_de_itens_ignora_maiusculas_minusculas(
        self,
    ):
        with self.assertRaises(
            ValorInvalido
        ):
            criar_versao_proposta_servico(
                numero=1,
                valor=1500,
                prazo_execucao_dias=10,
                validade=date(
                    2026,
                    9,
                    15,
                ),
                descricao_tecnica="Serviço",
                itens_incluidos=[
                    "Deslocamento",
                    "DESLOCAMENTO",
                ],
            )

    def test_duplicidade_de_itens_ignora_espacos_externos(
        self,
    ):
        with self.assertRaises(
            ValorInvalido
        ):
            criar_versao_proposta_servico(
                numero=1,
                valor=1500,
                prazo_execucao_dias=10,
                validade=date(
                    2026,
                    9,
                    15,
                ),
                descricao_tecnica="Serviço",
                itens_incluidos=[
                    "Deslocamento",
                    "   deslocamento   ",
                ],
            )

    def test_colecao_sem_duplicidade_preserva_itens(
        self,
    ):
        versao = criar_versao_proposta_servico(
            numero=1,
            valor=1500,
            prazo_execucao_dias=10,
            validade=date(
                2026,
                9,
                15,
            ),
            descricao_tecnica="Serviço",
            itens_incluidos=[
                "  Mão de obra  ",
                "Deslocamento",
            ],
        )

        self.assertEqual(
            versao.itens_incluidos,
            (
                "Mão de obra",
                "Deslocamento",
            ),
        )


class TestPropostaServico(unittest.TestCase):

    def criar_primeira_versao(self):
        return criar_versao_proposta_servico(
            numero=1,
            valor=1500,
            prazo_execucao_dias=10,
            validade=date(
                2026,
                9,
                15,
            ),
            descricao_tecnica=(
                "Execução completa do serviço."
            ),
        )

    def criar_proposta_valida(self):
        return criar_proposta_servico(
            codigo=1,
            codigo_solicitacao=10,
            codigo_empresa=20,
            codigo_servico_ofertado_empresa=30,
            primeira_versao=(
                self.criar_primeira_versao()
            ),
        )

    def criar_solicitacao_valida(
        self,
    ):
        return SolicitacaoServico(
            codigo=10,
            codigo_cliente=100,
            codigo_tipo_servico=200,
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
            status="RECEBENDO_PROPOSTAS",
        )

    def criar_solicitacao_direta_valida(
        self,
    ):
        return SolicitacaoServico(
            codigo=10,
            codigo_cliente=100,
            codigo_tipo_servico=200,
            modalidade=(
                ModalidadeSolicitacaoServico.DIRETA
            ),
            origem=(
                OrigemSolicitacaoServico.CLIENTE
            ),
            municipio="Caetité",
            uf="BA",
            dados_tecnicos={},
            codigo_empresa_destinataria=20,
            codigo_servico_ofertado_empresa=30,
            status="RECEBENDO_PROPOSTAS",
        )

    def criar_oferta_valida(
        self,
    ):
        return ServicoOfertadoEmpresa(
            codigo=30,
            codigo_empresa=20,
            codigo_tipo_servico=200,
            modelo_precificacao=(
                ModeloPrecificacao.SOB_CONSULTA
            ),
            valor=None,
            aceita_solicitacao_direta=True,
            participa_marketplace=True,
            area_atendimento=criar_area_atendimento(
                modalidade="NACIONAL",
            ),
            ativo=True,
        )

    def test_contexto_relacional_valido(
        self,
    ):
        proposta = self.criar_proposta_valida()
        solicitacao = self.criar_solicitacao_valida()
        oferta = self.criar_oferta_valida()

        resultado = validar_contexto_proposta_servico(
            proposta,
            solicitacao,
            oferta,
        )

        self.assertIsNone(
            resultado
        )

    def test_contexto_exige_proposta_valida(
        self,
    ):
        with self.assertRaises(
            TypeError
        ):
            validar_contexto_proposta_servico(
                {},
                self.criar_solicitacao_valida(),
                self.criar_oferta_valida(),
            )

    def test_contexto_exige_solicitacao_valida(
        self,
    ):
        with self.assertRaises(
            TypeError
        ):
            validar_contexto_proposta_servico(
                self.criar_proposta_valida(),
                {},
                self.criar_oferta_valida(),
            )

    def test_contexto_exige_oferta_valida(
        self,
    ):
        with self.assertRaises(
            TypeError
        ):
            validar_contexto_proposta_servico(
                self.criar_proposta_valida(),
                self.criar_solicitacao_valida(),
                {},
            )

    def test_proposta_deve_pertencer_a_solicitacao(
        self,
    ):
        proposta = self.criar_proposta_valida()
        solicitacao = self.criar_solicitacao_valida()

        solicitacao.codigo = 999

        with self.assertRaises(
            ValorInvalido
        ):
            validar_contexto_proposta_servico(
                proposta,
                solicitacao,
                self.criar_oferta_valida(),
            )

    def test_empresa_da_proposta_deve_ser_da_oferta(
        self,
    ):
        proposta = self.criar_proposta_valida()
        oferta = self.criar_oferta_valida()

        oferta.codigo_empresa = 999

        with self.assertRaises(
            ValorInvalido
        ):
            validar_contexto_proposta_servico(
                proposta,
                self.criar_solicitacao_valida(),
                oferta,
            )

    def test_oferta_deve_corresponder_ao_tipo_solicitado(
        self,
    ):
        oferta = self.criar_oferta_valida()

        oferta.codigo_tipo_servico = 999

        with self.assertRaises(
            ValorInvalido
        ):
            validar_contexto_proposta_servico(
                self.criar_proposta_valida(),
                self.criar_solicitacao_valida(),
                oferta,
            )

    def test_oferta_da_proposta_deve_corresponder(
        self,
    ):
        oferta = self.criar_oferta_valida()

        oferta.codigo = 999

        with self.assertRaises(
            ValorInvalido
        ):
            validar_contexto_proposta_servico(
                self.criar_proposta_valida(),
                self.criar_solicitacao_valida(),
                oferta,
            )

    def test_contexto_direto_valido(
        self,
    ):
        resultado = validar_contexto_proposta_servico(
            self.criar_proposta_valida(),
            self.criar_solicitacao_direta_valida(),
            self.criar_oferta_valida(),
        )

        self.assertIsNone(
            resultado
        )

    def test_direta_exige_empresa_destinataria(
        self,
    ):
        solicitacao = (
            self.criar_solicitacao_direta_valida()
        )

        solicitacao.codigo_empresa_destinataria = None

        with self.assertRaises(
            ValorInvalido
        ):
            validar_contexto_proposta_servico(
                self.criar_proposta_valida(),
                solicitacao,
                self.criar_oferta_valida(),
            )

    def test_direta_exige_oferta_na_solicitacao(
        self,
    ):
        solicitacao = (
            self.criar_solicitacao_direta_valida()
        )

        solicitacao.codigo_servico_ofertado_empresa = (
            None
        )

        with self.assertRaises(
            ValorInvalido
        ):
            validar_contexto_proposta_servico(
                self.criar_proposta_valida(),
                solicitacao,
                self.criar_oferta_valida(),
            )

    def test_direta_exige_empresa_destinataria_da_proposta(
        self,
    ):
        solicitacao = (
            self.criar_solicitacao_direta_valida()
        )

        solicitacao.codigo_empresa_destinataria = 999

        with self.assertRaises(
            ValorInvalido
        ):
            validar_contexto_proposta_servico(
                self.criar_proposta_valida(),
                solicitacao,
                self.criar_oferta_valida(),
            )

    def test_direta_exige_oferta_na_proposta(
        self,
    ):
        proposta = criar_proposta_servico(
            codigo=1,
            codigo_solicitacao=10,
            codigo_empresa=20,
            primeira_versao=(
                self.criar_primeira_versao()
            ),
        )

        with self.assertRaises(
            ValorInvalido
        ):
            validar_contexto_proposta_servico(
                proposta,
                self.criar_solicitacao_direta_valida(),
                self.criar_oferta_valida(),
            )

    def test_direta_exige_mesma_oferta_da_solicitacao(
        self,
    ):
        solicitacao = (
            self.criar_solicitacao_direta_valida()
        )

        solicitacao.codigo_servico_ofertado_empresa = (
            999
        )

        with self.assertRaises(
            ValorInvalido
        ):
            validar_contexto_proposta_servico(
                self.criar_proposta_valida(),
                solicitacao,
                self.criar_oferta_valida(),
            )

    def test_direta_exige_oferta_informada_da_solicitacao(
        self,
    ):
        oferta = self.criar_oferta_valida()

        oferta.codigo = 999

        with self.assertRaises(
            ValorInvalido
        ):
            validar_contexto_proposta_servico(
                self.criar_proposta_valida(),
                self.criar_solicitacao_direta_valida(),
                oferta,
            )

    def test_aberta_nao_permite_empresa_destinataria(
        self,
    ):
        solicitacao = self.criar_solicitacao_valida()

        solicitacao.codigo_empresa_destinataria = 20

        with self.assertRaises(
            ValorInvalido
        ):
            validar_contexto_proposta_servico(
                self.criar_proposta_valida(),
                solicitacao,
                self.criar_oferta_valida(),
            )

    def test_aberta_nao_permite_oferta_pre_vinculada(
        self,
    ):
        solicitacao = self.criar_solicitacao_valida()

        solicitacao.codigo_servico_ofertado_empresa = (
            30
        )

        with self.assertRaises(
            ValorInvalido
        ):
            validar_contexto_proposta_servico(
                self.criar_proposta_valida(),
                solicitacao,
                self.criar_oferta_valida(),
            )

    def test_aberta_exige_oferta_na_proposta(
        self,
    ):
        proposta = criar_proposta_servico(
            codigo=1,
            codigo_solicitacao=10,
            codigo_empresa=20,
            primeira_versao=(
                self.criar_primeira_versao()
            ),
        )

        with self.assertRaises(
            ValorInvalido
        ):
            validar_contexto_proposta_servico(
                proposta,
                self.criar_solicitacao_valida(),
                self.criar_oferta_valida(),
            )

    def test_aberta_rejeita_oferta_inativa(
        self,
    ):
        oferta = self.criar_oferta_valida()

        oferta.ativo = False

        with self.assertRaises(
            ValorInvalido
        ):
            validar_contexto_proposta_servico(
                self.criar_proposta_valida(),
                self.criar_solicitacao_valida(),
                oferta,
            )

    def test_aberta_exige_participacao_no_marketplace(
        self,
    ):
        oferta = self.criar_oferta_valida()

        oferta.participa_marketplace = False

        with self.assertRaises(
            ValorInvalido
        ):
            validar_contexto_proposta_servico(
                self.criar_proposta_valida(),
                self.criar_solicitacao_valida(),
                oferta,
            )

    def test_aberta_exige_area_atendimento(
        self,
    ):
        oferta = self.criar_oferta_valida()

        oferta.area_atendimento = None

        with self.assertRaises(
            ValorInvalido
        ):
            validar_contexto_proposta_servico(
                self.criar_proposta_valida(),
                self.criar_solicitacao_valida(),
                oferta,
            )

    def test_aberta_aceita_area_nacional(
        self,
    ):
        oferta = self.criar_oferta_valida()

        resultado = validar_contexto_proposta_servico(
            self.criar_proposta_valida(),
            self.criar_solicitacao_valida(),
            oferta,
        )

        self.assertIsNone(
            resultado
        )

    def test_aberta_aceita_municipio_atendido(
        self,
    ):
        oferta = self.criar_oferta_valida()

        oferta.area_atendimento = (
            criar_area_atendimento(
                modalidade="MUNICIPIOS",
                municipios=[
                    "Caetité",
                    "Guanambi",
                ],
            )
        )

        resultado = validar_contexto_proposta_servico(
            self.criar_proposta_valida(),
            self.criar_solicitacao_valida(),
            oferta,
        )

        self.assertIsNone(
            resultado
        )

    def test_aberta_rejeita_municipio_nao_atendido(
        self,
    ):
        oferta = self.criar_oferta_valida()

        oferta.area_atendimento = (
            criar_area_atendimento(
                modalidade="MUNICIPIOS",
                municipios=[
                    "Guanambi",
                    "Brumado",
                ],
            )
        )

        with self.assertRaises(
            ValorInvalido
        ):
            validar_contexto_proposta_servico(
                self.criar_proposta_valida(),
                self.criar_solicitacao_valida(),
                oferta,
            )

    def test_aberta_aceita_localidade_dentro_do_raio(
        self,
    ):
        oferta = self.criar_oferta_valida()

        oferta.area_atendimento = (
            criar_area_atendimento(
                modalidade="RAIO",
                municipio_base="Guanambi",
                uf_base="BA",
                raio_km=100,
            )
        )

        resultado = validar_contexto_proposta_servico(
            self.criar_proposta_valida(),
            self.criar_solicitacao_valida(),
            oferta,
            distancia_km=80,
        )

        self.assertIsNone(
            resultado
        )

    def test_aberta_rejeita_localidade_fora_do_raio(
        self,
    ):
        oferta = self.criar_oferta_valida()

        oferta.area_atendimento = (
            criar_area_atendimento(
                modalidade="RAIO",
                municipio_base="Guanambi",
                uf_base="BA",
                raio_km=100,
            )
        )

        with self.assertRaises(
            ValorInvalido
        ):
            validar_contexto_proposta_servico(
                self.criar_proposta_valida(),
                self.criar_solicitacao_valida(),
                oferta,
                distancia_km=120,
            )

    def test_aberta_area_raio_exige_distancia(
        self,
    ):
        oferta = self.criar_oferta_valida()

        oferta.area_atendimento = (
            criar_area_atendimento(
                modalidade="RAIO",
                municipio_base="Guanambi",
                uf_base="BA",
                raio_km=100,
            )
        )

        with self.assertRaises(
            DadosObrigatoriosAusentes
        ):
            validar_contexto_proposta_servico(
                self.criar_proposta_valida(),
                self.criar_solicitacao_valida(),
                oferta,
            )

    def test_direta_nao_exige_area_atendimento(
        self,
    ):
        oferta = self.criar_oferta_valida()

        oferta.area_atendimento = None

        resultado = validar_contexto_proposta_servico(
            self.criar_proposta_valida(),
            self.criar_solicitacao_direta_valida(),
            oferta,
        )

        self.assertIsNone(
            resultado
        )

    def test_contexto_aceita_solicitacao_recebendo_propostas(
        self,
    ):
        solicitacao = self.criar_solicitacao_valida()

        self.assertEqual(
            solicitacao.status,
            "RECEBENDO_PROPOSTAS",
        )

        resultado = validar_contexto_proposta_servico(
            self.criar_proposta_valida(),
            solicitacao,
            self.criar_oferta_valida(),
        )

        self.assertIsNone(
            resultado
        )

    def test_contexto_rejeita_status_sem_recebimento(
        self,
    ):
        status_bloqueados = (
            "EM_ELABORACAO",
            "PUBLICADA",
            "EM_ANALISE_PELO_CLIENTE",
            "ENCERRADA_COM_CONTRATACAO",
            "ENCERRADA_SEM_CONTRATACAO",
            "CANCELADA",
            "EXPIRADA",
        )

        for status in status_bloqueados:
            with self.subTest(
                status=status
            ):
                solicitacao = (
                    self.criar_solicitacao_valida()
                )

                solicitacao.status = status

                with self.assertRaises(
                    OperacaoNaoPermitida
                ):
                    validar_contexto_proposta_servico(
                        self.criar_proposta_valida(),
                        solicitacao,
                        self.criar_oferta_valida(),
                    )

    def test_status_incompativel_tem_prioridade_no_contexto(
        self,
    ):
        solicitacao = self.criar_solicitacao_valida()
        oferta = self.criar_oferta_valida()

        solicitacao.status = "CANCELADA"

        oferta.codigo_empresa = 999

        with self.assertRaises(
            OperacaoNaoPermitida
        ):
            validar_contexto_proposta_servico(
                self.criar_proposta_valida(),
                solicitacao,
                oferta,
            )

    def test_criar_proposta_servico(
        self,
    ):
        proposta = self.criar_proposta_valida()

        self.assertIsInstance(
            proposta,
            PropostaServico,
        )

        self.assertEqual(
            proposta.codigo,
            1,
        )

        self.assertEqual(
            proposta.codigo_solicitacao,
            10,
        )

        self.assertEqual(
            proposta.codigo_empresa,
            20,
        )

        self.assertEqual(
            proposta.codigo_servico_ofertado_empresa,
            30,
        )

    def test_proposta_inicia_no_status_inicial(
        self,
    ):
        proposta = self.criar_proposta_valida()

        self.assertEqual(
            proposta.status,
            "EM_ELABORACAO",
        )

    def test_proposta_inicia_com_primeira_versao(
        self,
    ):
        primeira_versao = (
            self.criar_primeira_versao()
        )

        proposta = criar_proposta_servico(
            codigo=1,
            codigo_solicitacao=10,
            codigo_empresa=20,
            primeira_versao=primeira_versao,
        )

        self.assertEqual(
            len(proposta.versoes),
            1,
        )

        self.assertIs(
            proposta.versoes[0],
            primeira_versao,
        )

        self.assertEqual(
            proposta.versoes[0].numero,
            1,
        )

    def test_primeira_versao_deve_ser_instancia_valida(
        self,
    ):
        with self.assertRaises(
            ValorInvalido
        ):
            criar_proposta_servico(
                codigo=1,
                codigo_solicitacao=10,
                codigo_empresa=20,
                primeira_versao={
                    "numero": 1,
                },
            )

    def test_primeira_versao_deve_possuir_numero_um(
        self,
    ):
        versao_2 = criar_versao_proposta_servico(
            numero=2,
            valor=1500,
            prazo_execucao_dias=10,
            validade=date(
                2026,
                9,
                15,
            ),
            descricao_tecnica="Serviço",
        )

        with self.assertRaises(
            ValorInvalido
        ):
            criar_proposta_servico(
                codigo=1,
                codigo_solicitacao=10,
                codigo_empresa=20,
                primeira_versao=versao_2,
            )

    def test_codigos_obrigatorios_devem_ser_positivos(
        self,
    ):
        primeira_versao = (
            self.criar_primeira_versao()
        )

        casos = (
            "codigo",
            "codigo_solicitacao",
            "codigo_empresa",
        )

        for campo in casos:
            for valor in (
                0,
                -1,
                True,
                "1",
                1.5,
            ):
                with self.subTest(
                    campo=campo,
                    valor=valor,
                ):
                    argumentos = {
                        "codigo": 1,
                        "codigo_solicitacao": 10,
                        "codigo_empresa": 20,
                        "primeira_versao": primeira_versao,
                    }

                    argumentos[campo] = valor

                    with self.assertRaises(
                        ValorInvalido
                    ):
                        criar_proposta_servico(
                            **argumentos
                        )

    def test_codigo_servico_ofertado_pode_ser_ausente(
        self,
    ):
        proposta = criar_proposta_servico(
            codigo=1,
            codigo_solicitacao=10,
            codigo_empresa=20,
            primeira_versao=(
                self.criar_primeira_versao()
            ),
        )

        self.assertIsNone(
            proposta.codigo_servico_ofertado_empresa
        )

    def test_codigo_servico_ofertado_deve_ser_positivo(
        self,
    ):
        for codigo in (
            0,
            -1,
            True,
            "30",
            1.5,
        ):
            with self.subTest(
                codigo=codigo
            ):
                with self.assertRaises(
                    ValorInvalido
                ):
                    criar_proposta_servico(
                        codigo=1,
                        codigo_solicitacao=10,
                        codigo_empresa=20,
                        codigo_servico_ofertado_empresa=(
                            codigo
                        ),
                        primeira_versao=(
                            self.criar_primeira_versao()
                        ),
                    )

    def test_versao_atual_inicial_e_primeira_versao(
        self,
    ):
        proposta = self.criar_proposta_valida()

        versao_atual = (
            obter_versao_atual_proposta(
                proposta
            )
        )

        self.assertIs(
            versao_atual,
            proposta.versoes[0],
        )

        self.assertEqual(
            versao_atual.numero,
            1,
        )

    def test_proximo_numero_versao_inicial_e_dois(
        self,
    ):
        proposta = self.criar_proposta_valida()

        self.assertEqual(
            obter_proximo_numero_versao(
                proposta
            ),
            2,
        )

    def test_versao_atual_e_ultima_versao_registrada(
        self,
    ):
        proposta = self.criar_proposta_valida()

        versao_1 = proposta.versoes[0]

        versao_2 = (
            registrar_nova_versao_proposta_servico(
                proposta=proposta,
                valor=1400,
                prazo_execucao_dias=12,
                validade=date(
                    2026,
                    9,
                    30,
                ),
                descricao_tecnica=(
                    "Condições comerciais revisadas."
                ),
            )
        )

        versao_atual = (
            obter_versao_atual_proposta(
                proposta
            )
        )

        self.assertIs(
            proposta.versoes[0],
            versao_1,
        )

        self.assertIs(
            proposta.versoes[1],
            versao_2,
        )

        self.assertIs(
            versao_atual,
            versao_2,
        )

        self.assertEqual(
            obter_proximo_numero_versao(
                proposta
            ),
            3,
        )

    def test_obter_versao_atual_nao_remove_historico(
        self,
    ):
        proposta = self.criar_proposta_valida()

        versao_1 = proposta.versoes[0]

        versao_2 = (
            registrar_nova_versao_proposta_servico(
                proposta=proposta,
                valor=1400,
                prazo_execucao_dias=12,
                validade=date(
                    2026,
                    9,
                    30,
                ),
                descricao_tecnica="Revisão.",
            )
        )

        obter_versao_atual_proposta(
            proposta
        )

        self.assertEqual(
            len(proposta.versoes),
            2,
        )

        self.assertIs(
            proposta.versoes[0],
            versao_1,
        )

        self.assertIs(
            proposta.versoes[1],
            versao_2,
        )

    def test_obter_versao_atual_e_consulta_pura(
        self,
    ):
        proposta = self.criar_proposta_valida()

        versoes_antes = proposta.versoes

        status_antes = proposta.status

        obter_versao_atual_proposta(
            proposta
        )

        self.assertEqual(
            proposta.versoes,
            versoes_antes,
        )

        self.assertEqual(
            proposta.status,
            status_antes,
        )

    def test_obter_versao_atual_exige_proposta_valida(
        self,
    ):
        with self.assertRaises(
            ValorInvalido
        ):
            obter_versao_atual_proposta(
                {
                    "codigo": 1,
                }
            )

    def test_obter_versao_atual_rejeita_historico_vazio(
        self,
    ):
        proposta = PropostaServico(
            codigo=1,
            codigo_solicitacao=10,
            codigo_empresa=20,
            codigo_servico_ofertado_empresa=None,
            _versoes=[],
            status="EM_ELABORACAO",
        )

        with self.assertRaises(
            ValorInvalido
        ):
            obter_versao_atual_proposta(
                proposta
            )

    def test_converter_proposta_para_dicionario(
        self,
    ):
        proposta = self.criar_proposta_valida()

        dados = (
            converter_proposta_servico_para_dicionario(
                proposta
            )
        )

        self.assertEqual(
            dados["codigo"],
            1,
        )

        self.assertEqual(
            dados["codigo_solicitacao"],
            10,
        )

        self.assertEqual(
            dados["codigo_empresa"],
            20,
        )

        self.assertEqual(
            dados[
                "codigo_servico_ofertado_empresa"
            ],
            30,
        )

        self.assertEqual(
            dados["status"],
            "EM_ELABORACAO",
        )

    def test_converter_proposta_serializa_historico(
        self,
    ):
        proposta = self.criar_proposta_valida()

        registrar_nova_versao_proposta_servico(
            proposta=proposta,
            valor=1400,
            prazo_execucao_dias=12,
            validade=date(
                2026,
                9,
                30,
            ),
            descricao_tecnica="Revisão.",
        )

        dados = (
            converter_proposta_servico_para_dicionario(
                proposta
            )
        )

        self.assertEqual(
            len(dados["versoes"]),
            2,
        )

        self.assertEqual(
            dados["versoes"][0]["numero"],
            1,
        )

        self.assertEqual(
            dados["versoes"][1]["numero"],
            2,
        )

        self.assertEqual(
            dados["versoes"][1]["validade"],
            "2026-09-30",
        )

    def test_dicionario_da_proposta_nao_altera_original(
        self,
    ):
        proposta = self.criar_proposta_valida()

        dados = (
            converter_proposta_servico_para_dicionario(
                proposta
            )
        )

        dados["versoes"][0][
            "itens_incluidos"
        ].append(
            "Item externo"
        )

        dados["status"] = "ACEITA"

        self.assertNotIn(
            "Item externo",
            proposta.versoes[0].itens_incluidos,
        )

        self.assertEqual(
            proposta.status,
            "EM_ELABORACAO",
        )

    def test_converter_proposta_exige_proposta_valida(
        self,
    ):
        with self.assertRaises(
            ValorInvalido
        ):
            converter_proposta_servico_para_dicionario(
                {
                    "codigo": 1,
                }
            )

    def test_converter_proposta_rejeita_historico_vazio(
        self,
    ):
        proposta = PropostaServico(
            codigo=1,
            codigo_solicitacao=10,
            codigo_empresa=20,
            codigo_servico_ofertado_empresa=None,
            _versoes=[],
            status="EM_ELABORACAO",
        )

        with self.assertRaises(
            ValorInvalido
        ):
            converter_proposta_servico_para_dicionario(
                proposta
            )

    def test_historico_publico_de_versoes_e_imutavel(
        self,
    ):
        proposta = self.criar_proposta_valida()

        self.assertIsInstance(
            proposta.versoes,
            tuple,
        )

        with self.assertRaises(
            AttributeError
        ):
            proposta.versoes.append(
                self.criar_primeira_versao()
            )

    def test_historico_publico_nao_expoe_lista_interna(
        self,
    ):
        proposta = self.criar_proposta_valida()

        historico = proposta.versoes

        historico += (
            self.criar_primeira_versao(),
        )

        self.assertEqual(
            len(historico),
            2,
        )

        self.assertEqual(
            len(proposta.versoes),
            1,
        )

    def test_historico_publico_preserva_identidade_das_versoes(
        self,
    ):
        proposta = self.criar_proposta_valida()

        versao_interna = proposta._versoes[0]
        versao_publica = proposta.versoes[0]

        self.assertIs(
            versao_publica,
            versao_interna,
        )

    def test_historico_publico_nao_pode_ser_substituido(
        self,
    ):
        proposta = self.criar_proposta_valida()

        with self.assertRaises(
            AttributeError
        ):
            proposta.versoes = []

    def test_proposta_em_elaboracao_permite_alteracao_comercial(
        self,
    ):
        proposta = self.criar_proposta_valida()

        resultado = (
            validar_permissao_alteracao_comercial(
                proposta
            )
        )

        self.assertIsNone(
            resultado
        )

    def test_proposta_em_revisao_permite_alteracao_comercial(
        self,
    ):
        proposta = self.criar_proposta_valida()
        proposta.status = "EM_REVISAO"

        resultado = (
            validar_permissao_alteracao_comercial(
                proposta
            )
        )

        self.assertIsNone(
            resultado
        )

    def test_validar_permissao_comercial_nao_altera_proposta(
        self,
    ):
        proposta = self.criar_proposta_valida()

        status_antes = proposta.status
        versoes_antes = proposta.versoes

        validar_permissao_alteracao_comercial(
            proposta
        )

        self.assertEqual(
            proposta.status,
            status_antes,
        )

        self.assertEqual(
            proposta.versoes,
            versoes_antes,
        )

    def test_estados_bloqueados_nao_permitem_alteracao_comercial(
        self,
    ):
        for status in (
            "ENVIADA",
            "REVISADA",
            "ACEITA",
            "RECUSADA",
            "NAO_SELECIONADA",
            "RETIRADA",
            "EXPIRADA",
        ):
            with self.subTest(
                status=status
            ):
                proposta = self.criar_proposta_valida()
                proposta.status = status

                with self.assertRaises(
                    OperacaoNaoPermitida
                ):
                    validar_permissao_alteracao_comercial(
                        proposta
                    )

    def test_permissao_bloqueada_nao_altera_proposta(
        self,
    ):
        proposta = self.criar_proposta_valida()
        proposta.status = "ENVIADA"

        status_antes = proposta.status
        versoes_antes = proposta.versoes

        with self.assertRaises(
            OperacaoNaoPermitida
        ):
            validar_permissao_alteracao_comercial(
                proposta
            )

        self.assertEqual(
            proposta.status,
            status_antes,
        )

        self.assertEqual(
            proposta.versoes,
            versoes_antes,
        )

    def test_permissao_alteracao_comercial_exige_proposta_valida(
        self,
    ):
        with self.assertRaises(
            ValorInvalido
        ):
            validar_permissao_alteracao_comercial(
                {}
            )

    def test_status_inexistente_bloqueia_alteracao_comercial(
        self,
    ):
        proposta = self.criar_proposta_valida()
        proposta.status = "INEXISTENTE"

        with self.assertRaises(
            OperacaoNaoPermitida
        ):
            validar_permissao_alteracao_comercial(
                proposta
            )

    def test_registrar_nova_versao_proposta_servico(
        self,
    ):
        proposta = self.criar_proposta_valida()

        nova_versao = (
            registrar_nova_versao_proposta_servico(
                proposta=proposta,
                valor=1400,
                prazo_execucao_dias=12,
                validade=date(
                    2026,
                    9,
                    30,
                ),
                descricao_tecnica=(
                    "Condições comerciais revisadas."
                ),
            )
        )

        self.assertIsInstance(
            nova_versao,
            VersaoPropostaServico,
        )

        self.assertEqual(
            nova_versao.numero,
            2,
        )

        self.assertEqual(
            len(proposta.versoes),
            2,
        )

        self.assertIs(
            proposta.versoes[-1],
            nova_versao,
        )

    def test_registrar_nova_versao_preserva_versao_anterior(
        self,
    ):
        proposta = self.criar_proposta_valida()

        versao_1 = proposta.versoes[0]

        numero_antes = versao_1.numero
        valor_antes = versao_1.valor
        prazo_antes = (
            versao_1.prazo_execucao_dias
        )
        validade_antes = versao_1.validade
        descricao_antes = (
            versao_1.descricao_tecnica
        )

        registrar_nova_versao_proposta_servico(
            proposta=proposta,
            valor=1400,
            prazo_execucao_dias=12,
            validade=date(
                2026,
                9,
                30,
            ),
            descricao_tecnica=(
                "Condições comerciais revisadas."
            ),
        )

        self.assertEqual(
            len(proposta.versoes),
            2,
        )

        self.assertIs(
            proposta.versoes[0],
            versao_1,
        )

        self.assertEqual(
            versao_1.numero,
            numero_antes,
        )

        self.assertEqual(
            versao_1.valor,
            valor_antes,
        )

        self.assertEqual(
            versao_1.prazo_execucao_dias,
            prazo_antes,
        )

        self.assertEqual(
            versao_1.validade,
            validade_antes,
        )

        self.assertEqual(
            versao_1.descricao_tecnica,
            descricao_antes,
        )

    def test_registrar_versoes_mantem_sequencia_numerica(
        self,
    ):
        proposta = self.criar_proposta_valida()

        versao_2 = (
            registrar_nova_versao_proposta_servico(
                proposta=proposta,
                valor=1400,
                prazo_execucao_dias=12,
                validade=date(
                    2026,
                    9,
                    30,
                ),
                descricao_tecnica="Revisão 1.",
            )
        )

        versao_3 = (
            registrar_nova_versao_proposta_servico(
                proposta=proposta,
                valor=1300,
                prazo_execucao_dias=15,
                validade=date(
                    2026,
                    10,
                    15,
                ),
                descricao_tecnica="Revisão 2.",
            )
        )

        self.assertEqual(
            tuple(
                versao.numero
                for versao in proposta.versoes
            ),
            (
                1,
                2,
                3,
            ),
        )

        self.assertEqual(
            versao_2.numero,
            2,
        )

        self.assertEqual(
            versao_3.numero,
            3,
        )

        self.assertIs(
            obter_versao_atual_proposta(
                proposta
            ),
            versao_3,
        )

        self.assertEqual(
            obter_proximo_numero_versao(
                proposta
            ),
            4,
        )

    def test_falha_ao_registrar_versao_nao_altera_historico(
        self,
    ):
        proposta = self.criar_proposta_valida()

        historico_antes = proposta.versoes

        with self.assertRaises(
            ValorInvalido
        ):
            registrar_nova_versao_proposta_servico(
                proposta=proposta,
                valor=0,
                prazo_execucao_dias=12,
                validade=date(
                    2026,
                    9,
                    30,
                ),
                descricao_tecnica="Revisão inválida.",
            )

        self.assertEqual(
            proposta.versoes,
            historico_antes,
        )

        self.assertEqual(
            len(proposta.versoes),
            1,
        )

        self.assertEqual(
            obter_proximo_numero_versao(
                proposta
            ),
            2,
        )

    def test_registrar_nova_versao_em_revisao(
        self,
    ):
        proposta = self.criar_proposta_valida()
        proposta.status = "EM_REVISAO"

        nova_versao = (
            registrar_nova_versao_proposta_servico(
                proposta=proposta,
                valor=1400,
                prazo_execucao_dias=12,
                validade=date(
                    2026,
                    9,
                    30,
                ),
                descricao_tecnica=(
                    "Condições revisadas."
                ),
            )
        )

        self.assertEqual(
            nova_versao.numero,
            2,
        )

        self.assertEqual(
            len(proposta.versoes),
            2,
        )

        self.assertIs(
            proposta.versoes[-1],
            nova_versao,
        )

    def test_registrar_nova_versao_nao_altera_status(
        self,
    ):
        proposta = self.criar_proposta_valida()
        proposta.status = "EM_REVISAO"

        status_antes = proposta.status

        registrar_nova_versao_proposta_servico(
            proposta=proposta,
            valor=1400,
            prazo_execucao_dias=12,
            validade=date(
                2026,
                9,
                30,
            ),
            descricao_tecnica=(
                "Condições revisadas."
            ),
        )

        self.assertEqual(
            proposta.status,
            status_antes,
        )

    def test_estados_bloqueados_nao_registram_nova_versao(
        self,
    ):
        for status in (
            "ENVIADA",
            "REVISADA",
            "ACEITA",
            "RECUSADA",
            "NAO_SELECIONADA",
            "RETIRADA",
            "EXPIRADA",
        ):
            with self.subTest(
                status=status
            ):
                proposta = self.criar_proposta_valida()
                proposta.status = status

                with self.assertRaises(
                    OperacaoNaoPermitida
                ):
                    registrar_nova_versao_proposta_servico(
                        proposta=proposta,
                        valor=1400,
                        prazo_execucao_dias=12,
                        validade=date(
                            2026,
                            9,
                            30,
                        ),
                        descricao_tecnica=(
                            "Condições revisadas."
                        ),
                    )

    def test_bloqueio_de_nova_versao_nao_altera_proposta(
        self,
    ):
        proposta = self.criar_proposta_valida()
        proposta.status = "ENVIADA"

        status_antes = proposta.status
        historico_antes = proposta.versoes

        with self.assertRaises(
            OperacaoNaoPermitida
        ):
            registrar_nova_versao_proposta_servico(
                proposta=proposta,
                valor=1400,
                prazo_execucao_dias=12,
                validade=date(
                    2026,
                    9,
                    30,
                ),
                descricao_tecnica=(
                    "Condições revisadas."
                ),
            )

        self.assertEqual(
            proposta.status,
            status_antes,
        )

        self.assertEqual(
            proposta.versoes,
            historico_antes,
        )

        self.assertEqual(
            obter_proximo_numero_versao(
                proposta
            ),
            2,
        )

    def test_status_inexistente_nao_registra_nova_versao(
        self,
    ):
        proposta = self.criar_proposta_valida()
        proposta.status = "INEXISTENTE"

        historico_antes = proposta.versoes

        with self.assertRaises(
            OperacaoNaoPermitida
        ):
            registrar_nova_versao_proposta_servico(
                proposta=proposta,
                valor=1400,
                prazo_execucao_dias=12,
                validade=date(
                    2026,
                    9,
                    30,
                ),
                descricao_tecnica=(
                    "Condições revisadas."
                ),
            )

        self.assertEqual(
            proposta.versoes,
            historico_antes,
        )

    def test_registrar_nova_versao_exige_proposta_valida(
        self,
    ):
        with self.assertRaises(
            ValorInvalido
        ):
            registrar_nova_versao_proposta_servico(
                proposta={},
                valor=1400,
                prazo_execucao_dias=12,
                validade=date(
                    2026,
                    9,
                    30,
                ),
                descricao_tecnica=(
                    "Condições revisadas."
                ),
            )

    def test_registrar_nova_versao_preserva_dados_comerciais(
        self,
    ):
        proposta = self.criar_proposta_valida()

        nova_versao = (
            registrar_nova_versao_proposta_servico(
                proposta=proposta,
                valor=1400,
                prazo_execucao_dias=12,
                validade=date(
                    2026,
                    9,
                    30,
                ),
                descricao_tecnica=(
                    "Condições comerciais revisadas."
                ),
                itens_incluidos=[
                    "Mão de obra",
                    "Deslocamento",
                ],
                itens_nao_incluidos=[
                    "Materiais adicionais",
                ],
                garantias={
                    "servico_dias": 120,
                },
                condicoes_comerciais={
                    "forma_pagamento": "PIX",
                },
                observacoes=(
                    "Execução mediante agendamento."
                ),
            )
        )

        self.assertEqual(
            nova_versao.valor,
            1400.0,
        )

        self.assertEqual(
            nova_versao.prazo_execucao_dias,
            12,
        )

        self.assertEqual(
            nova_versao.validade,
            date(
                2026,
                9,
                30,
            ),
        )

        self.assertEqual(
            nova_versao.descricao_tecnica,
            "Condições comerciais revisadas.",
        )

        self.assertEqual(
            nova_versao.itens_incluidos,
            (
                "Mão de obra",
                "Deslocamento",
            ),
        )

        self.assertEqual(
            nova_versao.itens_nao_incluidos,
            (
                "Materiais adicionais",
            ),
        )

        self.assertEqual(
            nova_versao.garantias[
                "servico_dias"
            ],
            120,
        )

        self.assertEqual(
            nova_versao.condicoes_comerciais[
                "forma_pagamento"
            ],
            "PIX",
        )

        self.assertEqual(
            nova_versao.observacoes,
            "Execução mediante agendamento.",
        )

    def test_nova_versao_nao_compartilha_estruturas_externas(
        self,
    ):
        proposta = self.criar_proposta_valida()

        itens_incluidos = [
            "Mão de obra",
        ]

        garantias = {
            "servico_dias": 90,
        }

        condicoes_comerciais = {
            "forma_pagamento": "PIX",
        }

        nova_versao = (
            registrar_nova_versao_proposta_servico(
                proposta=proposta,
                valor=1400,
                prazo_execucao_dias=12,
                validade=date(
                    2026,
                    9,
                    30,
                ),
                descricao_tecnica="Revisão.",
                itens_incluidos=itens_incluidos,
                garantias=garantias,
                condicoes_comerciais=(
                    condicoes_comerciais
                ),
            )
        )

        itens_incluidos.append(
            "Item posterior"
        )

        garantias["servico_dias"] = 180

        condicoes_comerciais[
            "forma_pagamento"
        ] = "Cartão"

        self.assertEqual(
            nova_versao.itens_incluidos,
            (
                "Mão de obra",
            ),
        )

        self.assertEqual(
            nova_versao.garantias[
                "servico_dias"
            ],
            90,
        )

        self.assertEqual(
            nova_versao.condicoes_comerciais[
                "forma_pagamento"
            ],
            "PIX",
        )

    def test_nova_versao_registrada_permanece_imutavel(
        self,
    ):
        proposta = self.criar_proposta_valida()

        nova_versao = (
            registrar_nova_versao_proposta_servico(
                proposta=proposta,
                valor=1400,
                prazo_execucao_dias=12,
                validade=date(
                    2026,
                    9,
                    30,
                ),
                descricao_tecnica="Revisão.",
                garantias={
                    "servico_dias": 90,
                },
            )
        )

        with self.assertRaises(
            FrozenInstanceError
        ):
            nova_versao.valor = 2000

        with self.assertRaises(
            TypeError
        ):
            nova_versao.garantias[
                "servico_dias"
            ] = 180

        self.assertIs(
            proposta.versoes[-1],
            nova_versao,
        )

    def test_alterar_status_executa_transicoes_permitidas(
        self,
    ):
        transicoes = (
            (
                "EM_ELABORACAO",
                "ENVIADA",
            ),
            (
                "EM_ELABORACAO",
                "RETIRADA",
            ),
            (
                "ENVIADA",
                "EM_REVISAO",
            ),
            (
                "ENVIADA",
                "RETIRADA",
            ),
            (
                "EM_REVISAO",
                "REVISADA",
            ),
            (
                "EM_REVISAO",
                "RETIRADA",
            ),
            (
                "REVISADA",
                "ENVIADA",
            ),
            (
                "REVISADA",
                "RETIRADA",
            ),
        )

        for status_atual, novo_status in transicoes:
            with self.subTest(
                status_atual=status_atual,
                novo_status=novo_status,
            ):
                proposta = self.criar_proposta_valida()
                proposta.status = status_atual

                alterar_status_proposta_servico(
                    proposta,
                    novo_status,
                )

                self.assertEqual(
                    proposta.status,
                    novo_status,
                )

    def test_aceite_exige_operacao_contextual(
        self,
    ):
        proposta = self.criar_proposta_valida()
        proposta.status = "ENVIADA"

        status_antes = proposta.status
        versoes_antes = proposta.versoes

        with self.assertRaises(
            OperacaoNaoPermitida
        ):
            alterar_status_proposta_servico(
                proposta,
                "ACEITA",
            )

        self.assertEqual(
            proposta.status,
            status_antes,
        )

        self.assertEqual(
            proposta.versoes,
            versoes_antes,
        )

    def test_nao_selecionada_exige_operacao_contextual(
        self,
    ):
        proposta = self.criar_proposta_valida()
        proposta.status = "ENVIADA"

        with self.assertRaises(
            OperacaoNaoPermitida
        ):
            alterar_status_proposta_servico(
                proposta,
                "NAO_SELECIONADA",
            )

        self.assertEqual(
            proposta.status,
            "ENVIADA",
        )

    def test_recusa_exige_operacao_contextual(
        self,
    ):
        proposta = self.criar_proposta_valida()
        proposta.status = "ENVIADA"

        with self.assertRaises(
            OperacaoNaoPermitida
        ):
            alterar_status_proposta_servico(
                proposta,
                "RECUSADA",
            )

        self.assertEqual(
            proposta.status,
            "ENVIADA",
        )

    def test_expiracao_exige_operacao_contextual(
        self,
    ):
        proposta = self.criar_proposta_valida()
        proposta.status = "ENVIADA"

        with self.assertRaises(
            OperacaoNaoPermitida
        ):
            alterar_status_proposta_servico(
                proposta,
                "EXPIRADA",
            )

        self.assertEqual(
            proposta.status,
            "ENVIADA",
        )

    def test_transicoes_contextuais_nao_alteram_proposta(
        self,
    ):
        for novo_status in (
            "ACEITA",
            "RECUSADA",
            "NAO_SELECIONADA",
            "EXPIRADA",
        ):
            with self.subTest(
                novo_status=novo_status
            ):
                proposta = self.criar_proposta_valida()
                proposta.status = "ENVIADA"

                status_antes = proposta.status
                versoes_antes = proposta.versoes

                with self.assertRaises(
                    OperacaoNaoPermitida
                ):
                    alterar_status_proposta_servico(
                        proposta,
                        novo_status,
                    )

                self.assertEqual(
                    proposta.status,
                    status_antes,
                )

                self.assertEqual(
                    proposta.versoes,
                    versoes_antes,
                )

    def test_expirar_proposta_enviada_com_validade_vencida(
        self,
    ):
        proposta = self.criar_proposta_valida()
        proposta.status = "ENVIADA"

        expirar_proposta_servico(
            proposta,
            data_referencia=date(
                2026,
                9,
                16,
            ),
        )

        self.assertEqual(
            proposta.status,
            "EXPIRADA",
        )

    def test_expirar_proposta_revisada_com_validade_vencida(
        self,
    ):
        proposta = self.criar_proposta_valida()
        proposta.status = "REVISADA"

        expirar_proposta_servico(
            proposta,
            data_referencia=date(
                2026,
                9,
                16,
            ),
        )

        self.assertEqual(
            proposta.status,
            "EXPIRADA",
        )

    def test_proposta_nao_expira_antes_da_validade(
        self,
    ):
        proposta = self.criar_proposta_valida()
        proposta.status = "ENVIADA"

        status_antes = proposta.status
        versoes_antes = proposta.versoes

        with self.assertRaises(
            OperacaoNaoPermitida
        ):
            expirar_proposta_servico(
                proposta,
                data_referencia=date(
                    2026,
                    9,
                    14,
                ),
            )

        self.assertEqual(
            proposta.status,
            status_antes,
        )

        self.assertEqual(
            proposta.versoes,
            versoes_antes,
        )

    def test_proposta_nao_expira_no_dia_da_validade(
        self,
    ):
        proposta = self.criar_proposta_valida()
        proposta.status = "ENVIADA"

        with self.assertRaises(
            OperacaoNaoPermitida
        ):
            expirar_proposta_servico(
                proposta,
                data_referencia=date(
                    2026,
                    9,
                    15,
                ),
            )

        self.assertEqual(
            proposta.status,
            "ENVIADA",
        )

    def test_proposta_vencida_em_estado_incompativel_nao_expira(
        self,
    ):
        proposta = self.criar_proposta_valida()
        proposta.status = "EM_ELABORACAO"

        with self.assertRaises(
            OperacaoNaoPermitida
        ):
            expirar_proposta_servico(
                proposta,
                data_referencia=date(
                    2026,
                    9,
                    16,
                ),
            )

        self.assertEqual(
            proposta.status,
            "EM_ELABORACAO",
        )

    def test_expirar_proposta_nao_altera_historico(
        self,
    ):
        proposta = self.criar_proposta_valida()
        proposta.status = "ENVIADA"

        versoes_antes = proposta.versoes
        versao_atual_antes = proposta.versoes[-1]

        expirar_proposta_servico(
            proposta,
            data_referencia=date(
                2026,
                9,
                16,
            ),
        )

        self.assertEqual(
            proposta.versoes,
            versoes_antes,
        )

        self.assertIs(
            proposta.versoes[-1],
            versao_atual_antes,
        )

    def test_expiracao_considera_apenas_versao_atual(
        self,
    ):
        proposta = self.criar_proposta_valida()
        proposta.status = "EM_REVISAO"

        registrar_nova_versao_proposta_servico(
            proposta=proposta,
            valor=1600,
            prazo_execucao_dias=12,
            validade=date(
                2026,
                10,
                15,
            ),
            descricao_tecnica=(
                "Condições comerciais revisadas."
            ),
        )

        proposta.status = "REVISADA"

        with self.assertRaises(
            OperacaoNaoPermitida
        ):
            expirar_proposta_servico(
                proposta,
                data_referencia=date(
                    2026,
                    9,
                    16,
                ),
            )

        self.assertEqual(
            proposta.status,
            "REVISADA",
        )

    def test_expirar_exige_proposta_valida(
        self,
    ):
        with self.assertRaises(
            ValorInvalido
        ):
            expirar_proposta_servico(
                {},
                data_referencia=date(
                    2026,
                    9,
                    16,
                ),
            )

    def test_expirar_exige_data_referencia_valida(
        self,
    ):
        proposta = self.criar_proposta_valida()
        proposta.status = "ENVIADA"

        for data_referencia in (
            "2026-09-16",
            20260916,
            True,
            [],
        ):
            with self.subTest(
                data_referencia=data_referencia
            ):
                with self.assertRaises(
                    ValorInvalido
                ):
                    expirar_proposta_servico(
                        proposta,
                        data_referencia=(
                            data_referencia
                        ),
                    )

                self.assertEqual(
                    proposta.status,
                    "ENVIADA",
                )

    def test_expirar_sem_data_referencia_usa_data_atual(
        self,
    ):
        proposta = criar_proposta_servico(
            codigo=1,
            codigo_solicitacao=10,
            codigo_empresa=20,
            codigo_servico_ofertado_empresa=30,
            primeira_versao=(
                criar_versao_proposta_servico(
                    numero=1,
                    valor=1500,
                    prazo_execucao_dias=10,
                    validade=date(
                        2000,
                        1,
                        1,
                    ),
                    descricao_tecnica="Serviço.",
                )
            ),
        )

        proposta.status = "ENVIADA"

        expirar_proposta_servico(
            proposta
        )

        self.assertEqual(
            proposta.status,
            "EXPIRADA",
        )

    def test_alterar_status_bloqueia_transicoes_invalidas(
        self,
    ):
        transicoes = (
            (
                "EM_ELABORACAO",
                "ACEITA",
            ),
            (
                "EM_ELABORACAO",
                "REVISADA",
            ),
            (
                "ENVIADA",
                "REVISADA",
            ),
            (
                "EM_REVISAO",
                "ACEITA",
            ),
            (
                "REVISADA",
                "EM_REVISAO",
            ),
        )

        for status_atual, novo_status in transicoes:
            with self.subTest(
                status_atual=status_atual,
                novo_status=novo_status,
            ):
                proposta = self.criar_proposta_valida()
                proposta.status = status_atual

                status_antes = proposta.status
                versoes_antes = proposta.versoes

                with self.assertRaises(
                    OperacaoNaoPermitida
                ):
                    alterar_status_proposta_servico(
                        proposta,
                        novo_status,
                    )

                self.assertEqual(
                    proposta.status,
                    status_antes,
                )

                self.assertEqual(
                    proposta.versoes,
                    versoes_antes,
                )

    def test_estados_terminais_nao_permitem_nova_transicao(
        self,
    ):
        for status in (
            "ACEITA",
            "RECUSADA",
            "NAO_SELECIONADA",
            "RETIRADA",
            "EXPIRADA",
        ):
            with self.subTest(
                status=status
            ):
                proposta = self.criar_proposta_valida()
                proposta.status = status

                with self.assertRaises(
                    OperacaoNaoPermitida
                ):
                    alterar_status_proposta_servico(
                        proposta,
                        "ENVIADA",
                    )

                self.assertEqual(
                    proposta.status,
                    status,
                )

    def test_proposta_nao_pode_transicionar_para_mesmo_status(
        self,
    ):
        proposta = self.criar_proposta_valida()

        with self.assertRaises(
            OperacaoNaoPermitida
        ):
            alterar_status_proposta_servico(
                proposta,
                "EM_ELABORACAO",
            )

        self.assertEqual(
            proposta.status,
            "EM_ELABORACAO",
        )

    def test_status_destino_inexistente_e_bloqueado(
        self,
    ):
        proposta = self.criar_proposta_valida()

        with self.assertRaises(
            OperacaoNaoPermitida
        ):
            alterar_status_proposta_servico(
                proposta,
                "INEXISTENTE",
            )

        self.assertEqual(
            proposta.status,
            "EM_ELABORACAO",
        )

    def test_status_atual_inexistente_bloqueia_transicao(
        self,
    ):
        proposta = self.criar_proposta_valida()
        proposta.status = "INEXISTENTE"

        with self.assertRaises(
            OperacaoNaoPermitida
        ):
            alterar_status_proposta_servico(
                proposta,
                "ENVIADA",
            )

        self.assertEqual(
            proposta.status,
            "INEXISTENTE",
        )

    def test_alterar_status_exige_proposta_valida(
        self,
    ):
        with self.assertRaises(
            ValorInvalido
        ):
            alterar_status_proposta_servico(
                {},
                "ENVIADA",
            )

    def test_alterar_status_exige_novo_status_textual(
        self,
    ):
        proposta = self.criar_proposta_valida()

        for novo_status in (
            None,
            2,
            True,
            [],
        ):
            with self.subTest(
                novo_status=novo_status
            ):
                with self.assertRaises(
                    ValorInvalido
                ):
                    alterar_status_proposta_servico(
                        proposta,
                        novo_status,
                    )

                self.assertEqual(
                    proposta.status,
                    "EM_ELABORACAO",
                )

    def test_buscar_proposta_por_codigo(
        self,
    ):
        proposta_1 = self.criar_proposta_valida()

        proposta_2 = criar_proposta_servico(
            codigo=2,
            codigo_solicitacao=20,
            codigo_empresa=30,
            primeira_versao=(
                self.criar_primeira_versao()
            ),
        )

        resultado = buscar_proposta_servico_por_codigo(
            [
                proposta_1,
                proposta_2,
            ],
            2,
        )

        self.assertIs(
            resultado,
            proposta_2,
        )

    def test_buscar_proposta_inexistente_retorna_none(
        self,
    ):
        proposta = self.criar_proposta_valida()

        resultado = buscar_proposta_servico_por_codigo(
            [proposta],
            999,
        )

        self.assertIsNone(
            resultado
        )

    def test_buscar_proposta_em_lista_vazia_retorna_none(
        self,
    ):
        resultado = buscar_proposta_servico_por_codigo(
            [],
            1,
        )

        self.assertIsNone(
            resultado
        )

    def test_buscar_proposta_exige_codigo_valido(
        self,
    ):
        for codigo in (
            0,
            -1,
            1.5,
            "1",
            True,
        ):
            with self.subTest(
                codigo=codigo
            ):
                with self.assertRaises(
                    ValorInvalido
                ):
                    buscar_proposta_servico_por_codigo(
                        [],
                        codigo,
                    )

    def test_listar_propostas_por_solicitacao(
        self,
    ):
        proposta_1 = self.criar_proposta_valida()

        proposta_2 = criar_proposta_servico(
            codigo=2,
            codigo_solicitacao=20,
            codigo_empresa=30,
            primeira_versao=(
                self.criar_primeira_versao()
            ),
        )

        resultado = listar_propostas_por_solicitacao(
            [
                proposta_1,
                proposta_2,
            ],
            proposta_1.codigo_solicitacao,
        )

        self.assertEqual(
            resultado,
            [
                proposta_1,
            ],
        )

    def test_listar_propostas_por_solicitacao_sem_resultado(
        self,
    ):
        resultado = listar_propostas_por_solicitacao(
            [],
            1,
        )

        self.assertEqual(
            resultado,
            [],
        )

    def test_listar_propostas_por_empresa(
        self,
    ):
        proposta_1 = self.criar_proposta_valida()

        proposta_2 = criar_proposta_servico(
            codigo=2,
            codigo_solicitacao=20,
            codigo_empresa=999,
            primeira_versao=(
                self.criar_primeira_versao()
            ),
        )

        resultado = listar_propostas_por_empresa(
            [
                proposta_1,
                proposta_2,
            ],
            proposta_1.codigo_empresa,
        )

        self.assertEqual(
            resultado,
            [
                proposta_1,
            ],
        )

    def test_listar_propostas_por_servico_ofertado(
        self,
    ):
        proposta_1 = criar_proposta_servico(
            codigo=1,
            codigo_solicitacao=10,
            codigo_empresa=20,
            codigo_servico_ofertado_empresa=30,
            primeira_versao=(
                self.criar_primeira_versao()
            ),
        )

        proposta_2 = criar_proposta_servico(
            codigo=2,
            codigo_solicitacao=10,
            codigo_empresa=21,
            primeira_versao=(
                self.criar_primeira_versao()
            ),
        )

        resultado = (
            listar_propostas_por_servico_ofertado(
                [
                    proposta_1,
                    proposta_2,
                ],
                30,
            )
        )

        self.assertEqual(
            resultado,
            [
                proposta_1,
            ],
        )

    def test_consultas_de_propostas_exigem_codigos_validos(
        self,
    ):
        consultas = (
            listar_propostas_por_solicitacao,
            listar_propostas_por_empresa,
            listar_propostas_por_servico_ofertado,
        )

        for consulta in consultas:
            for codigo in (
                0,
                -1,
                1.5,
                "1",
                True,
            ):
                with self.subTest(
                    consulta=consulta.__name__,
                    codigo=codigo,
                ):
                    with self.assertRaises(
                        ValorInvalido
                    ):
                        consulta(
                            [],
                            codigo,
                        )

    def test_listagens_de_propostas_retornam_nova_lista(
        self,
    ):
        proposta = self.criar_proposta_valida()

        propostas = [
            proposta,
        ]

        consultas = (
            (
                listar_propostas_por_solicitacao,
                proposta.codigo_solicitacao,
            ),
            (
                listar_propostas_por_empresa,
                proposta.codigo_empresa,
            ),
        )

        for consulta, codigo in consultas:
            with self.subTest(
                consulta=consulta.__name__
            ):
                resultado = consulta(
                    propostas,
                    codigo,
                )

                self.assertEqual(
                    resultado,
                    propostas,
                )

                self.assertIsNot(
                    resultado,
                    propostas,
                )

    def test_listar_propostas_por_status(
        self,
    ):
        proposta_1 = self.criar_proposta_valida()

        proposta_2 = criar_proposta_servico(
            codigo=2,
            codigo_solicitacao=20,
            codigo_empresa=30,
            primeira_versao=(
                self.criar_primeira_versao()
            ),
        )

        alterar_status_proposta_servico(
            proposta_2,
            "ENVIADA",
        )

        resultado = listar_propostas_por_status(
            [
                proposta_1,
                proposta_2,
            ],
            "ENVIADA",
        )

        self.assertEqual(
            resultado,
            [
                proposta_2,
            ],
        )

    def test_listar_propostas_por_status_normaliza_valor(
        self,
    ):
        proposta = self.criar_proposta_valida()

        alterar_status_proposta_servico(
            proposta,
            "ENVIADA",
        )

        resultado = listar_propostas_por_status(
            [
                proposta,
            ],
            "  enviada  ",
        )

        self.assertEqual(
            resultado,
            [
                proposta,
            ],
        )

    def test_listar_propostas_por_status_invalido(
        self,
    ):
        with self.assertRaises(
            ValorInvalido
        ):
            listar_propostas_por_status(
                [],
                "STATUS_INVENTADO",
            )

    def test_listar_propostas_por_status_exige_texto(
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
                with self.assertRaises(
                    ValorInvalido
                ):
                    listar_propostas_por_status(
                        [],
                        status,
                    )

    def test_listar_propostas_por_status_sem_resultado(
        self,
    ):
        proposta = self.criar_proposta_valida()

        propostas = [
            proposta,
        ]

        resultado = listar_propostas_por_status(
            propostas,
            "ENVIADA",
        )

        self.assertEqual(
            resultado,
            [],
        )

        self.assertIsNot(
            resultado,
            propostas,
        )






if __name__ == "__main__":
    unittest.main()