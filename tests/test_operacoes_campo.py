"""
Testes da estrutura das Operações de Campo.
"""

import unittest

from app.dominio.operacoes_campo import (
    StatusInstalacao,
    StatusLigacao,
    StatusVistoria,
    buscar_ultima_vistoria,
    buscar_vistoria_por_codigo,
    buscar_vistoria_por_numero_sequencial,
    criar_dados_ligacao_solicitada,
    criar_dados_operacoes_campo,
    criar_dados_planejamento_instalacao,
    criar_dados_vistoria_solicitada,
    gerar_proximo_codigo_vistoria,
    gerar_proximo_numero_sequencial_vistoria,
    preparar_agendamento_vistoria,
    preparar_aprovacao_vistoria,
    preparar_realizacao_vistoria,
    preparar_reprovacao_vistoria,
    preparar_conclusao_instalacao,
    preparar_inicio_instalacao,
    preparar_agendamento_ligacao,
    preparar_conclusao_ligacao,
    validar_instalacao,
    validar_ligacao,
    validar_operacoes_campo,
    validar_vistoria,
)


class TestOperacoesCampo(unittest.TestCase):
    """
    Testes da criação e validação
    das Operações de Campo.
    """

    def test_criar_dados_operacoes_campo(
        self,
    ):
        """
        Deve criar a estrutura inicial
        das Operações de Campo.
        """

        operacoes_campo = (
            criar_dados_operacoes_campo()
        )

        self.assertEqual(
            operacoes_campo,
            {
                "instalacao": None,
                "vistorias": [],
                "ligacao": None,
            },
        )

    def test_vistorias_devem_possuir_lista_propria(
        self,
    ):
        """
        Duas estruturas diferentes não devem
        compartilhar a mesma lista de Vistorias.
        """

        primeira = (
            criar_dados_operacoes_campo()
        )

        segunda = (
            criar_dados_operacoes_campo()
        )

        self.assertIsNot(
            primeira["vistorias"],
            segunda["vistorias"],
        )

    def test_validar_operacoes_campo(
        self,
    ):
        """
        Uma estrutura completa deve ser válida.
        """

        operacoes_campo = (
            criar_dados_operacoes_campo()
        )

        resultado = validar_operacoes_campo(
            operacoes_campo
        )

        self.assertIsNone(
            resultado
        )

    def test_operacoes_campo_devem_ser_dicionario(
        self,
    ):
        """
        Uma estrutura de outro tipo deve ser rejeitada.
        """

        with self.assertRaises(
            TypeError
        ):
            validar_operacoes_campo(
                []
            )

    def test_campo_obrigatorio_ausente_deve_gerar_erro(
        self,
    ):
        """
        A ausência de um campo estrutural
        deve invalidar as Operações de Campo.
        """

        with self.assertRaisesRegex(
            ValueError,
            "campo ausente",
        ):
            validar_operacoes_campo(
                {
                    "instalacao": None,
                    "vistorias": [],
                }
            )

    def test_vistorias_devem_formar_lista(
        self,
    ):
        """
        Vistorias não podem ser armazenadas
        em outro tipo de coleção.
        """

        with self.assertRaisesRegex(
            TypeError,
            "Vistorias",
        ):
            validar_operacoes_campo(
                {
                    "instalacao": None,
                    "vistorias": {},
                    "ligacao": None,
                }
            )

    def test_instalacao_deve_ser_dicionario_ou_none(
        self,
    ):
        """
        Uma Instalação preenchida deve ser
        representada por um dicionário.
        """

        with self.assertRaisesRegex(
            TypeError,
            "Instalação",
        ):
            validar_operacoes_campo(
                {
                    "instalacao": [],
                    "vistorias": [],
                    "ligacao": None,
                }
            )

    def test_ligacao_deve_ser_dicionario_ou_none(
        self,
    ):
        """
        Uma Ligação preenchida deve ser
        representada por um dicionário.
        """

        with self.assertRaisesRegex(
            TypeError,
            "Ligação",
        ):
            validar_operacoes_campo(
                {
                    "instalacao": None,
                    "vistorias": [],
                    "ligacao": [],
                }
            )

class TestLigacao(
    unittest.TestCase
):
    """
    Testes da estrutura da Ligação
    e Energização.
    """

    def test_status_ligacao_devem_ser_oficiais(
        self,
    ):
        """
        Deve possuir os estados internos
        previstos para a Ligação.
        """

        self.assertEqual(
            StatusLigacao.SOLICITADA.value,
            "SOLICITADA",
        )

        self.assertEqual(
            StatusLigacao.AGENDADA.value,
            "AGENDADA",
        )

        self.assertEqual(
            StatusLigacao.CONCLUIDA.value,
            "CONCLUIDA",
        )

    def test_criar_ligacao_solicitada(
        self,
    ):
        """
        Deve criar uma Ligação com
        status SOLICITADA.
        """

        ligacao = (
            criar_dados_ligacao_solicitada(
                data_solicitacao="2026-09-05",
                responsavel_solicitacao=(
                    "Ana Lima"
                ),
                protocolo="LIG-2026-001",
                observacoes=(
                    "Solicitação protocolada."
                ),
            )
        )

        self.assertEqual(
            ligacao["status"],
            StatusLigacao.SOLICITADA.value,
        )

        self.assertEqual(
            ligacao["data_solicitacao"],
            "2026-09-05",
        )

        self.assertEqual(
            ligacao["protocolo"],
            "LIG-2026-001",
        )

        self.assertIsNone(
            ligacao["data_agendamento"]
        )

        self.assertIsNone(
            ligacao["data_ligacao"]
        )

    def test_ligacao_deve_normalizar_textos(
        self,
    ):
        """
        Os textos devem ser armazenados
        sem espaços externos.
        """

        ligacao = (
            criar_dados_ligacao_solicitada(
                data_solicitacao="2026-09-05",
                responsavel_solicitacao=(
                    "  Ana Lima  "
                ),
                protocolo="  LIG-001  ",
                observacoes=(
                    "  Ligação solicitada.  "
                ),
            )
        )

        self.assertEqual(
            ligacao[
                "responsavel_solicitacao"
            ],
            "Ana Lima",
        )

        self.assertEqual(
            ligacao["protocolo"],
            "LIG-001",
        )

        self.assertEqual(
            ligacao["observacoes"],
            "Ligação solicitada.",
        )

    def test_validar_ligacao_solicitada(
        self,
    ):
        """
        Uma Ligação solicitada corretamente
        deve ser válida.
        """

        ligacao = (
            criar_dados_ligacao_solicitada(
                data_solicitacao="2026-09-05",
                responsavel_solicitacao=(
                    "Ana Lima"
                ),
                protocolo="LIG-2026-001",
            )
        )

        resultado = validar_ligacao(
            ligacao
        )

        self.assertIsNone(
            resultado
        )

    def test_status_ligacao_invalido(
        self,
    ):
        """
        Um status não oficial deve ser rejeitado.
        """

        ligacao = (
            criar_dados_ligacao_solicitada(
                data_solicitacao="2026-09-05",
                responsavel_solicitacao=(
                    "Ana Lima"
                ),
                protocolo="LIG-2026-001",
            )
        )

        ligacao["status"] = "CANCELADA"

        with self.assertRaisesRegex(
            ValueError,
            "Status de Ligação inválido",
        ):
            validar_ligacao(
                ligacao
            )

    def test_ligacao_campo_obrigatorio_ausente(
        self,
    ):
        """
        Uma estrutura incompleta
        deve ser rejeitada.
        """

        ligacao = (
            criar_dados_ligacao_solicitada(
                data_solicitacao="2026-09-05",
                responsavel_solicitacao=(
                    "Ana Lima"
                ),
                protocolo="LIG-2026-001",
            )
        )

        del ligacao["protocolo"]

        with self.assertRaisesRegex(
            ValueError,
            "campo ausente",
        ):
            validar_ligacao(
                ligacao
            )

    def test_ligacao_solicitada_nao_pode_ter_agendamento(
        self,
    ):
        """
        Uma Ligação ainda solicitada não pode
        possuir dados de agendamento.
        """

        ligacao = (
            criar_dados_ligacao_solicitada(
                data_solicitacao="2026-09-05",
                responsavel_solicitacao=(
                    "Ana Lima"
                ),
                protocolo="LIG-2026-001",
            )
        )

        ligacao["data_agendamento"] = (
            "2026-09-10"
        )

        ligacao[
            "responsavel_agendamento"
        ] = "Carlos Souza"

        with self.assertRaisesRegex(
            ValueError,
            "não pode possuir",
        ):
            validar_ligacao(
                ligacao
            )

    def test_operacoes_campo_deve_validar_ligacao(
        self,
    ):
        """
        A validação das Operações de Campo deve
        validar a Ligação armazenada.
        """

        operacoes_campo = (
            criar_dados_operacoes_campo()
        )

        operacoes_campo["ligacao"] = (
            criar_dados_ligacao_solicitada(
                data_solicitacao="2026-09-05",
                responsavel_solicitacao=(
                    "Ana Lima"
                ),
                protocolo="LIG-2026-001",
            )
        )

        resultado = validar_operacoes_campo(
            operacoes_campo
        )

        self.assertIsNone(
            resultado
        )

class TestAgendamentoLigacao(
    unittest.TestCase
):
    """
    Testes do agendamento da Ligação.
    """

    def setUp(self):
        self.ligacao = (
            criar_dados_ligacao_solicitada(
                data_solicitacao="2026-09-05",
                responsavel_solicitacao=(
                    "Ana Lima"
                ),
                protocolo="LIG-2026-001",
                observacoes=(
                    "Aguardando agendamento."
                ),
            )
        )

    def test_preparar_agendamento_ligacao(
        self,
    ):
        resultado = preparar_agendamento_ligacao(
            ligacao=self.ligacao,
            data_agendamento="2026-09-10",
            responsavel_agendamento=(
                "Carlos Souza"
            ),
            observacoes="Ligação agendada.",
        )

        self.assertEqual(
            resultado["status"],
            StatusLigacao.AGENDADA.value,
        )

        self.assertEqual(
            resultado["data_agendamento"],
            "2026-09-10",
        )

        self.assertEqual(
            resultado[
                "responsavel_agendamento"
            ],
            "Carlos Souza",
        )

    def test_agendamento_nao_deve_alterar_original(
        self,
    ):
        preparar_agendamento_ligacao(
            ligacao=self.ligacao,
            data_agendamento="2026-09-10",
            responsavel_agendamento=(
                "Carlos Souza"
            ),
        )

        self.assertEqual(
            self.ligacao["status"],
            StatusLigacao.SOLICITADA.value,
        )

        self.assertIsNone(
            self.ligacao["data_agendamento"]
        )

    def test_agendamento_anterior_a_solicitacao(
        self,
    ):
        with self.assertRaisesRegex(
            ValueError,
            "anterior",
        ):
            preparar_agendamento_ligacao(
                ligacao=self.ligacao,
                data_agendamento="2026-09-04",
                responsavel_agendamento=(
                    "Carlos Souza"
                ),
            )

    def test_nao_deve_agendar_duas_vezes(
        self,
    ):
        ligacao_agendada = (
            preparar_agendamento_ligacao(
                ligacao=self.ligacao,
                data_agendamento="2026-09-10",
                responsavel_agendamento=(
                    "Carlos Souza"
                ),
            )
        )

        with self.assertRaisesRegex(
            ValueError,
            "solicitada",
        ):
            preparar_agendamento_ligacao(
                ligacao=ligacao_agendada,
                data_agendamento="2026-09-11",
                responsavel_agendamento=(
                    "Carlos Souza"
                ),
            )

class TestConclusaoLigacao(
    unittest.TestCase
):
    """
    Testes da conclusão da Ligação
    e Energização.
    """

    def setUp(self):
        ligacao_solicitada = (
            criar_dados_ligacao_solicitada(
                data_solicitacao="2026-09-05",
                responsavel_solicitacao=(
                    "Ana Lima"
                ),
                protocolo="LIG-2026-001",
                observacoes=(
                    "Aguardando execução."
                ),
            )
        )

        self.ligacao = (
            preparar_agendamento_ligacao(
                ligacao=ligacao_solicitada,
                data_agendamento="2026-09-10",
                responsavel_agendamento=(
                    "Carlos Souza"
                ),
            )
        )

    def test_preparar_conclusao_ligacao(
        self,
    ):
        resultado = preparar_conclusao_ligacao(
            ligacao=self.ligacao,
            data_ligacao="2026-09-10",
            responsavel_ligacao=(
                "Equipe da Concessionária"
            ),
            observacoes=(
                "Sistema energizado."
            ),
        )

        self.assertEqual(
            resultado["status"],
            StatusLigacao.CONCLUIDA.value,
        )

        self.assertEqual(
            resultado["data_ligacao"],
            "2026-09-10",
        )

        self.assertEqual(
            resultado[
                "responsavel_ligacao"
            ],
            "Equipe da Concessionária",
        )

    def test_conclusao_nao_deve_alterar_original(
        self,
    ):
        preparar_conclusao_ligacao(
            ligacao=self.ligacao,
            data_ligacao="2026-09-10",
            responsavel_ligacao=(
                "Equipe da Concessionária"
            ),
        )

        self.assertEqual(
            self.ligacao["status"],
            StatusLigacao.AGENDADA.value,
        )

        self.assertIsNone(
            self.ligacao["data_ligacao"]
        )

    def test_nao_deve_concluir_ligacao_solicitada(
        self,
    ):
        ligacao_solicitada = (
            criar_dados_ligacao_solicitada(
                data_solicitacao="2026-09-05",
                responsavel_solicitacao=(
                    "Ana Lima"
                ),
                protocolo="LIG-2026-001",
            )
        )

        with self.assertRaisesRegex(
            ValueError,
            "agendada",
        ):
            preparar_conclusao_ligacao(
                ligacao=ligacao_solicitada,
                data_ligacao="2026-09-10",
                responsavel_ligacao=(
                    "Equipe da Concessionária"
                ),
            )

    def test_ligacao_nao_pode_anteceder_agendamento(
        self,
    ):
        with self.assertRaisesRegex(
            ValueError,
            "anterior",
        ):
            preparar_conclusao_ligacao(
                ligacao=self.ligacao,
                data_ligacao="2026-09-09",
                responsavel_ligacao=(
                    "Equipe da Concessionária"
                ),
            )

    def test_nao_deve_concluir_ligacao_duas_vezes(
        self,
    ):
        ligacao_concluida = (
            preparar_conclusao_ligacao(
                ligacao=self.ligacao,
                data_ligacao="2026-09-10",
                responsavel_ligacao=(
                    "Equipe da Concessionária"
                ),
            )
        )

        with self.assertRaisesRegex(
            ValueError,
            "agendada",
        ):
            preparar_conclusao_ligacao(
                ligacao=ligacao_concluida,
                data_ligacao="2026-09-11",
                responsavel_ligacao=(
                    "Equipe da Concessionária"
                ),
            )

class TestVistoria(
    unittest.TestCase
):
    """
    Testes da criação, validação
    e consulta das Vistorias.
    """

    def setUp(self):
        """
        Cria uma Vistoria solicitada padrão.
        """

        self.vistoria = (
            criar_dados_vistoria_solicitada(
                codigo=1,
                numero_sequencial=1,
                data_solicitacao="2026-08-25",
                responsavel_solicitacao=(
                    "Ana Lima"
                ),
                protocolo="VST-2026-001",
                observacoes=(
                    "Primeira vistoria."
                ),
            )
        )

    def test_criar_vistoria_solicitada(
        self,
    ):
        """
        Deve criar uma Vistoria com
        status SOLICITADA.
        """

        self.assertEqual(
            self.vistoria["codigo"],
            1,
        )

        self.assertEqual(
            self.vistoria[
                "numero_sequencial"
            ],
            1,
        )

        self.assertEqual(
            self.vistoria["status"],
            StatusVistoria.SOLICITADA.value,
        )

        self.assertEqual(
            self.vistoria["protocolo"],
            "VST-2026-001",
        )

        self.assertIsNone(
            self.vistoria["data_agendamento"]
        )

        self.assertIsNone(
            self.vistoria["resultado"]
        )

    def test_vistoria_deve_normalizar_textos(
        self,
    ):
        """
        Os textos devem ser armazenados
        sem espaços externos.
        """

        vistoria = (
            criar_dados_vistoria_solicitada(
                codigo=1,
                numero_sequencial=1,
                data_solicitacao="2026-08-25",
                responsavel_solicitacao=(
                    "  Ana Lima  "
                ),
                protocolo="  VST-001  ",
                observacoes="  Primeira.  ",
            )
        )

        self.assertEqual(
            vistoria[
                "responsavel_solicitacao"
            ],
            "Ana Lima",
        )

        self.assertEqual(
            vistoria["protocolo"],
            "VST-001",
        )

        self.assertEqual(
            vistoria["observacoes"],
            "Primeira.",
        )

    def test_validar_vistoria_solicitada(
        self,
    ):
        """
        Uma Vistoria solicitada corretamente
        deve ser válida.
        """

        resultado = validar_vistoria(
            self.vistoria
        )

        self.assertIsNone(
            resultado
        )

    def test_status_vistoria_invalido(
        self,
    ):
        """
        Um status não oficial deve ser rejeitado.
        """

        self.vistoria["status"] = (
            "CANCELADA"
        )

        with self.assertRaisesRegex(
            ValueError,
            "Status de Vistoria inválido",
        ):
            validar_vistoria(
                self.vistoria
            )

    def test_vistoria_solicitada_nao_pode_ter_agendamento(
        self,
    ):
        """
        Uma Vistoria solicitada ainda não pode
        possuir dados de agendamento.
        """

        self.vistoria["data_agendamento"] = (
            "2026-08-30"
        )

        self.vistoria[
            "responsavel_agendamento"
        ] = "Carlos Souza"

        with self.assertRaisesRegex(
            ValueError,
            "não pode possuir",
        ):
            validar_vistoria(
                self.vistoria
            )

    def test_campo_obrigatorio_ausente(
        self,
    ):
        """
        A estrutura incompleta deve ser rejeitada.
        """

        del self.vistoria["protocolo"]

        with self.assertRaisesRegex(
            ValueError,
            "campo ausente",
        ):
            validar_vistoria(
                self.vistoria
            )

    def test_gerar_proximo_codigo_vistoria(
        self,
    ):
        """
        Deve gerar o código após o maior
        código já existente.
        """

        resultado = (
            gerar_proximo_codigo_vistoria(
                [
                    {
                        "codigo": 2,
                    },
                    {
                        "codigo": 5,
                    },
                    {
                        "codigo": 3,
                    },
                ]
            )
        )

        self.assertEqual(
            resultado,
            6,
        )

    def test_gerar_primeiro_codigo_vistoria(
        self,
    ):
        """
        A primeira Vistoria deve receber código 1.
        """

        self.assertEqual(
            gerar_proximo_codigo_vistoria(
                []
            ),
            1,
        )

    def test_gerar_proximo_numero_sequencial(
        self,
    ):
        """
        Deve gerar a próxima tentativa
        após o maior número sequencial.
        """

        resultado = (
            gerar_proximo_numero_sequencial_vistoria(
                [
                    {
                        "numero_sequencial": 1,
                    },
                    {
                        "numero_sequencial": 2,
                    },
                ]
            )
        )

        self.assertEqual(
            resultado,
            3,
        )

    def test_buscar_vistoria_por_codigo(
        self,
    ):
        """
        Deve localizar a Vistoria
        pelo código interno.
        """

        resultado = buscar_vistoria_por_codigo(
            [
                self.vistoria,
            ],
            1,
        )

        self.assertIs(
            resultado,
            self.vistoria,
        )

    def test_buscar_vistoria_por_numero_sequencial(
        self,
    ):
        """
        Deve localizar a tentativa
        pelo número sequencial.
        """

        resultado = (
            buscar_vistoria_por_numero_sequencial(
                [
                    self.vistoria,
                ],
                1,
            )
        )

        self.assertIs(
            resultado,
            self.vistoria,
        )

    def test_busca_inexistente_deve_retornar_none(
        self,
    ):
        """
        Consultas sem correspondência
        devem retornar None.
        """

        self.assertIsNone(
            buscar_vistoria_por_codigo(
                [
                    self.vistoria,
                ],
                999,
            )
        )

    def test_buscar_ultima_vistoria(
        self,
    ):
        """
        Deve retornar a tentativa com o maior
        número sequencial.
        """

        segunda_vistoria = (
            criar_dados_vistoria_solicitada(
                codigo=2,
                numero_sequencial=2,
                data_solicitacao="2026-09-10",
                responsavel_solicitacao=(
                    "Ana Lima"
                ),
                protocolo="VST-2026-002",
            )
        )

        resultado = buscar_ultima_vistoria(
            [
                segunda_vistoria,
                self.vistoria,
            ]
        )

        self.assertIs(
            resultado,
            segunda_vistoria,
        )

    def test_buscar_ultima_vistoria_lista_vazia(
        self,
    ):
        """
        Uma coleção vazia não possui
        última Vistoria.
        """

        self.assertIsNone(
            buscar_ultima_vistoria(
                []
            )
        )

    def test_operacoes_campo_deve_validar_vistorias(
        self,
    ):
        """
        A validação das Operações de Campo deve
        validar cada Vistoria armazenada.
        """

        operacoes_campo = (
            criar_dados_operacoes_campo()
        )

        operacoes_campo[
            "vistorias"
        ].append(
            self.vistoria
        )

        resultado = validar_operacoes_campo(
            operacoes_campo
        )

        self.assertIsNone(
            resultado
        )

class TestAgendamentoVistoria(
    unittest.TestCase
):
    """
    Testes do agendamento da Vistoria.
    """

    def setUp(self):
        """
        Cria uma Vistoria solicitada padrão.
        """

        self.vistoria = (
            criar_dados_vistoria_solicitada(
                codigo=1,
                numero_sequencial=1,
                data_solicitacao="2026-08-25",
                responsavel_solicitacao=(
                    "Ana Lima"
                ),
                protocolo="VST-2026-001",
                observacoes=(
                    "Aguardando agendamento."
                ),
            )
        )

    def test_preparar_agendamento_vistoria(
        self,
    ):
        """
        Deve retornar uma cópia da Vistoria
        com status AGENDADA.
        """

        resultado = preparar_agendamento_vistoria(
            vistoria=self.vistoria,
            data_agendamento="2026-08-30",
            responsavel_agendamento=(
                "Carlos Souza"
            ),
            observacoes="Vistoria agendada.",
        )

        self.assertEqual(
            resultado["status"],
            StatusVistoria.AGENDADA.value,
        )

        self.assertEqual(
            resultado["data_agendamento"],
            "2026-08-30",
        )

        self.assertEqual(
            resultado[
                "responsavel_agendamento"
            ],
            "Carlos Souza",
        )

        self.assertEqual(
            resultado["observacoes"],
            "Vistoria agendada.",
        )

    def test_agendamento_nao_deve_alterar_original(
        self,
    ):
        """
        A preparação não deve modificar
        a Vistoria recebida.
        """

        preparar_agendamento_vistoria(
            vistoria=self.vistoria,
            data_agendamento="2026-08-30",
            responsavel_agendamento=(
                "Carlos Souza"
            ),
        )

        self.assertEqual(
            self.vistoria["status"],
            StatusVistoria.SOLICITADA.value,
        )

        self.assertIsNone(
            self.vistoria["data_agendamento"]
        )

    def test_agendamento_deve_normalizar_responsavel(
        self,
    ):
        """
        O responsável deve ser armazenado
        sem espaços externos.
        """

        resultado = preparar_agendamento_vistoria(
            vistoria=self.vistoria,
            data_agendamento="2026-08-30",
            responsavel_agendamento=(
                "  Carlos Souza  "
            ),
        )

        self.assertEqual(
            resultado[
                "responsavel_agendamento"
            ],
            "Carlos Souza",
        )

    def test_agendamento_deve_preservar_observacao(
        self,
    ):
        """
        Quando nenhuma nova observação for informada,
        o conteúdo anterior deve ser preservado.
        """

        resultado = preparar_agendamento_vistoria(
            vistoria=self.vistoria,
            data_agendamento="2026-08-30",
            responsavel_agendamento=(
                "Carlos Souza"
            ),
        )

        self.assertEqual(
            resultado["observacoes"],
            "Aguardando agendamento.",
        )

    def test_nao_deve_agendar_vistoria_agendada(
        self,
    ):
        """
        Uma Vistoria já agendada não pode
        ser agendada novamente.
        """

        vistoria_agendada = (
            preparar_agendamento_vistoria(
                vistoria=self.vistoria,
                data_agendamento="2026-08-30",
                responsavel_agendamento=(
                    "Carlos Souza"
                ),
            )
        )

        with self.assertRaisesRegex(
            ValueError,
            "solicitada",
        ):
            preparar_agendamento_vistoria(
                vistoria=vistoria_agendada,
                data_agendamento="2026-08-31",
                responsavel_agendamento=(
                    "Carlos Souza"
                ),
            )

    def test_data_agendamento_invalida(
        self,
    ):
        """
        A data deve utilizar o formato ISO.
        """

        with self.assertRaisesRegex(
            ValueError,
            "AAAA-MM-DD",
        ):
            preparar_agendamento_vistoria(
                vistoria=self.vistoria,
                data_agendamento="30/08/2026",
                responsavel_agendamento=(
                    "Carlos Souza"
                ),
            )

    def test_agendamento_anterior_a_solicitacao(
        self,
    ):
        """
        O agendamento não pode ser anterior
        à solicitação da Vistoria.
        """

        with self.assertRaisesRegex(
            ValueError,
            "anterior",
        ):
            preparar_agendamento_vistoria(
                vistoria=self.vistoria,
                data_agendamento="2026-08-24",
                responsavel_agendamento=(
                    "Carlos Souza"
                ),
            )

    def test_responsavel_agendamento_obrigatorio(
        self,
    ):
        """
        O agendamento deve possuir responsável.
        """

        with self.assertRaisesRegex(
            ValueError,
            "Responsável",
        ):
            preparar_agendamento_vistoria(
                vistoria=self.vistoria,
                data_agendamento="2026-08-30",
                responsavel_agendamento=" ",
            )

class TestRealizacaoVistoria(
    unittest.TestCase
):
    """
    Testes do registro da realização
    da Vistoria.
    """

    def setUp(self):
        """
        Cria uma Vistoria agendada padrão.
        """

        vistoria_solicitada = (
            criar_dados_vistoria_solicitada(
                codigo=1,
                numero_sequencial=1,
                data_solicitacao="2026-08-25",
                responsavel_solicitacao=(
                    "Ana Lima"
                ),
                protocolo="VST-2026-001",
                observacoes=(
                    "Aguardando realização."
                ),
            )
        )

        self.vistoria = (
            preparar_agendamento_vistoria(
                vistoria=vistoria_solicitada,
                data_agendamento="2026-08-30",
                responsavel_agendamento=(
                    "Carlos Souza"
                ),
            )
        )

    def test_preparar_realizacao_vistoria(
        self,
    ):
        """
        Deve retornar uma cópia da Vistoria
        com status REALIZADA.
        """

        resultado = preparar_realizacao_vistoria(
            vistoria=self.vistoria,
            data_realizacao="2026-08-30",
            responsavel_realizacao=(
                "Marcos Oliveira"
            ),
            observacoes=(
                "Vistoria realizada no local."
            ),
        )

        self.assertEqual(
            resultado["status"],
            StatusVistoria.REALIZADA.value,
        )

        self.assertEqual(
            resultado["data_realizacao"],
            "2026-08-30",
        )

        self.assertEqual(
            resultado[
                "responsavel_realizacao"
            ],
            "Marcos Oliveira",
        )

        self.assertIsNone(
            resultado["resultado"]
        )

        self.assertIsNone(
            resultado["motivo_reprovacao"]
        )

    def test_realizacao_nao_deve_alterar_original(
        self,
    ):
        """
        A preparação deve preservar
        a Vistoria recebida.
        """

        preparar_realizacao_vistoria(
            vistoria=self.vistoria,
            data_realizacao="2026-08-30",
            responsavel_realizacao=(
                "Marcos Oliveira"
            ),
        )

        self.assertEqual(
            self.vistoria["status"],
            StatusVistoria.AGENDADA.value,
        )

        self.assertIsNone(
            self.vistoria["data_realizacao"]
        )

    def test_realizacao_deve_normalizar_responsavel(
        self,
    ):
        """
        O responsável deve ser armazenado
        sem espaços externos.
        """

        resultado = preparar_realizacao_vistoria(
            vistoria=self.vistoria,
            data_realizacao="2026-08-30",
            responsavel_realizacao=(
                "  Marcos Oliveira  "
            ),
        )

        self.assertEqual(
            resultado[
                "responsavel_realizacao"
            ],
            "Marcos Oliveira",
        )

    def test_realizacao_deve_preservar_observacao(
        self,
    ):
        """
        Sem nova observação, o conteúdo
        anterior deve ser preservado.
        """

        resultado = preparar_realizacao_vistoria(
            vistoria=self.vistoria,
            data_realizacao="2026-08-30",
            responsavel_realizacao=(
                "Marcos Oliveira"
            ),
        )

        self.assertEqual(
            resultado["observacoes"],
            "Aguardando realização.",
        )

    def test_nao_deve_realizar_vistoria_solicitada(
        self,
    ):
        """
        Uma Vistoria ainda não agendada
        não pode ser realizada.
        """

        vistoria_solicitada = (
            criar_dados_vistoria_solicitada(
                codigo=1,
                numero_sequencial=1,
                data_solicitacao="2026-08-25",
                responsavel_solicitacao=(
                    "Ana Lima"
                ),
                protocolo="VST-2026-001",
            )
        )

        with self.assertRaisesRegex(
            ValueError,
            "agendada",
        ):
            preparar_realizacao_vistoria(
                vistoria=vistoria_solicitada,
                data_realizacao="2026-08-30",
                responsavel_realizacao=(
                    "Marcos Oliveira"
                ),
            )

    def test_nao_deve_realizar_vistoria_duas_vezes(
        self,
    ):
        """
        Uma Vistoria realizada não pode
        ser realizada novamente.
        """

        vistoria_realizada = (
            preparar_realizacao_vistoria(
                vistoria=self.vistoria,
                data_realizacao="2026-08-30",
                responsavel_realizacao=(
                    "Marcos Oliveira"
                ),
            )
        )

        with self.assertRaisesRegex(
            ValueError,
            "agendada",
        ):
            preparar_realizacao_vistoria(
                vistoria=vistoria_realizada,
                data_realizacao="2026-08-31",
                responsavel_realizacao=(
                    "Marcos Oliveira"
                ),
            )

    def test_data_realizacao_invalida(
        self,
    ):
        """
        A data deve utilizar o formato ISO.
        """

        with self.assertRaisesRegex(
            ValueError,
            "AAAA-MM-DD",
        ):
            preparar_realizacao_vistoria(
                vistoria=self.vistoria,
                data_realizacao="30/08/2026",
                responsavel_realizacao=(
                    "Marcos Oliveira"
                ),
            )

    def test_realizacao_anterior_ao_agendamento(
        self,
    ):
        """
        A realização não pode ser anterior
        à data agendada.
        """

        with self.assertRaisesRegex(
            ValueError,
            "anterior",
        ):
            preparar_realizacao_vistoria(
                vistoria=self.vistoria,
                data_realizacao="2026-08-29",
                responsavel_realizacao=(
                    "Marcos Oliveira"
                ),
            )

    def test_responsavel_realizacao_obrigatorio(
        self,
    ):
        """
        A realização deve possuir responsável.
        """

        with self.assertRaisesRegex(
            ValueError,
            "Responsável",
        ):
            preparar_realizacao_vistoria(
                vistoria=self.vistoria,
                data_realizacao="2026-08-30",
                responsavel_realizacao=" ",
            )

class TestResultadoVistoria(
    unittest.TestCase
):
    """
    Testes do resultado formal
    da Vistoria.
    """

    def setUp(self):
        """
        Cria uma Vistoria realizada padrão.
        """

        vistoria_solicitada = (
            criar_dados_vistoria_solicitada(
                codigo=1,
                numero_sequencial=1,
                data_solicitacao="2026-08-25",
                responsavel_solicitacao=(
                    "Ana Lima"
                ),
                protocolo="VST-2026-001",
                observacoes=(
                    "Aguardando resultado."
                ),
            )
        )

        vistoria_agendada = (
            preparar_agendamento_vistoria(
                vistoria=vistoria_solicitada,
                data_agendamento="2026-08-30",
                responsavel_agendamento=(
                    "Carlos Souza"
                ),
            )
        )

        self.vistoria = (
            preparar_realizacao_vistoria(
                vistoria=vistoria_agendada,
                data_realizacao="2026-08-30",
                responsavel_realizacao=(
                    "Marcos Oliveira"
                ),
            )
        )

    def test_preparar_aprovacao_vistoria(
        self,
    ):
        """
        Deve criar uma cópia aprovada
        com os dados do resultado.
        """

        resultado = preparar_aprovacao_vistoria(
            vistoria=self.vistoria,
            data_resultado="2026-09-01",
            responsavel_resultado="Ana Lima",
            observacoes="Vistoria aprovada.",
        )

        self.assertEqual(
            resultado["status"],
            StatusVistoria.APROVADA.value,
        )

        self.assertEqual(
            resultado["resultado"],
            "APROVADA",
        )

        self.assertEqual(
            resultado["data_resultado"],
            "2026-09-01",
        )

        self.assertEqual(
            resultado["responsavel_resultado"],
            "Ana Lima",
        )

        self.assertIsNone(
            resultado["motivo_reprovacao"]
        )

    def test_preparar_reprovacao_vistoria(
        self,
    ):
        """
        Deve criar uma cópia reprovada
        com motivo obrigatório.
        """

        resultado = preparar_reprovacao_vistoria(
            vistoria=self.vistoria,
            data_resultado="2026-09-01",
            responsavel_resultado="Ana Lima",
            motivo_reprovacao=(
                "Inversor sem identificação."
            ),
        )

        self.assertEqual(
            resultado["status"],
            StatusVistoria.REPROVADA.value,
        )

        self.assertEqual(
            resultado["resultado"],
            "REPROVADA",
        )

        self.assertEqual(
            resultado["motivo_reprovacao"],
            "Inversor sem identificação.",
        )

    def test_resultado_nao_deve_alterar_original(
        self,
    ):
        """
        A preparação deve preservar
        a Vistoria original.
        """

        preparar_aprovacao_vistoria(
            vistoria=self.vistoria,
            data_resultado="2026-09-01",
            responsavel_resultado="Ana Lima",
        )

        self.assertEqual(
            self.vistoria["status"],
            StatusVistoria.REALIZADA.value,
        )

        self.assertIsNone(
            self.vistoria["resultado"]
        )

    def test_aprovacao_exige_vistoria_realizada(
        self,
    ):
        """
        Uma Vistoria ainda agendada
        não pode ser aprovada.
        """

        vistoria_solicitada = (
            criar_dados_vistoria_solicitada(
                codigo=2,
                numero_sequencial=2,
                data_solicitacao="2026-09-10",
                responsavel_solicitacao=(
                    "Ana Lima"
                ),
                protocolo="VST-2026-002",
            )
        )

        with self.assertRaisesRegex(
            ValueError,
            "realizada",
        ):
            preparar_aprovacao_vistoria(
                vistoria=vistoria_solicitada,
                data_resultado="2026-09-11",
                responsavel_resultado=(
                    "Ana Lima"
                ),
            )

    def test_reprovacao_exige_motivo(
        self,
    ):
        """
        Uma reprovação deve possuir motivo.
        """

        with self.assertRaisesRegex(
            ValueError,
            "Motivo",
        ):
            preparar_reprovacao_vistoria(
                vistoria=self.vistoria,
                data_resultado="2026-09-01",
                responsavel_resultado=(
                    "Ana Lima"
                ),
                motivo_reprovacao=" ",
            )

    def test_resultado_nao_pode_anteceder_realizacao(
        self,
    ):
        """
        O resultado não pode ser anterior
        à realização da Vistoria.
        """

        with self.assertRaisesRegex(
            ValueError,
            "anterior",
        ):
            preparar_aprovacao_vistoria(
                vistoria=self.vistoria,
                data_resultado="2026-08-29",
                responsavel_resultado=(
                    "Ana Lima"
                ),
            )

    def test_responsavel_resultado_obrigatorio(
        self,
    ):
        """
        O resultado deve possuir responsável.
        """

        with self.assertRaisesRegex(
            ValueError,
            "Responsável",
        ):
            preparar_aprovacao_vistoria(
                vistoria=self.vistoria,
                data_resultado="2026-09-01",
                responsavel_resultado=" ",
            )

    def test_nao_deve_aprovar_duas_vezes(
        self,
    ):
        """
        Uma Vistoria aprovada não pode
        receber novo resultado.
        """

        vistoria_aprovada = (
            preparar_aprovacao_vistoria(
                vistoria=self.vistoria,
                data_resultado="2026-09-01",
                responsavel_resultado=(
                    "Ana Lima"
                ),
            )
        )

        with self.assertRaisesRegex(
            ValueError,
            "realizada",
        ):
            preparar_aprovacao_vistoria(
                vistoria=vistoria_aprovada,
                data_resultado="2026-09-02",
                responsavel_resultado=(
                    "Ana Lima"
                ),
            )

class TestPlanejamentoInstalacao(
    unittest.TestCase
):
    """
    Testes da criação e validação
    do planejamento da Instalação.
    """

    def setUp(self):
        """
        Cria uma Instalação planejada padrão.
        """

        self.instalacao = (
            criar_dados_planejamento_instalacao(
                data_prevista="2026-08-20",
                responsavel_planejamento=(
                    "Ana Lima"
                ),
                equipe_responsavel=(
                    "Equipe Técnica A"
                ),
                observacoes=(
                    "Instalação programada."
                ),
            )
        )

    def test_criar_planejamento_instalacao(
        self,
    ):
        """
        Deve criar uma Instalação
        com status PLANEJADA.
        """

        self.assertEqual(
            self.instalacao["status"],
            StatusInstalacao.PLANEJADA.value,
        )

        self.assertEqual(
            self.instalacao["data_prevista"],
            "2026-08-20",
        )

        self.assertEqual(
            self.instalacao[
                "equipe_responsavel"
            ],
            "Equipe Técnica A",
        )

        self.assertIsNone(
            self.instalacao["data_inicio"]
        )

        self.assertIsNone(
            self.instalacao["data_conclusao"]
        )

    def test_planejamento_deve_normalizar_textos(
        self,
    ):
        """
        Os textos devem ser armazenados
        sem espaços externos.
        """

        instalacao = (
            criar_dados_planejamento_instalacao(
                data_prevista="2026-08-20",
                responsavel_planejamento=(
                    "  Ana Lima  "
                ),
                equipe_responsavel=(
                    "  Equipe Técnica A  "
                ),
                observacoes="  Programada.  ",
            )
        )

        self.assertEqual(
            instalacao[
                "responsavel_planejamento"
            ],
            "Ana Lima",
        )

        self.assertEqual(
            instalacao[
                "equipe_responsavel"
            ],
            "Equipe Técnica A",
        )

        self.assertEqual(
            instalacao["observacoes"],
            "Programada.",
        )

    def test_observacoes_vazias_devem_virar_none(
        self,
    ):
        """
        Um texto vazio não deve ser armazenado
        como observação válida.
        """

        instalacao = (
            criar_dados_planejamento_instalacao(
                data_prevista="2026-08-20",
                responsavel_planejamento=(
                    "Ana Lima"
                ),
                equipe_responsavel=(
                    "Equipe Técnica A"
                ),
                observacoes="   ",
            )
        )

        self.assertIsNone(
            instalacao["observacoes"]
        )

    def test_data_prevista_invalida_deve_gerar_erro(
        self,
    ):
        """
        A data deve utilizar o formato ISO.
        """

        with self.assertRaisesRegex(
            ValueError,
            "AAAA-MM-DD",
        ):
            criar_dados_planejamento_instalacao(
                data_prevista="20/08/2026",
                responsavel_planejamento=(
                    "Ana Lima"
                ),
                equipe_responsavel=(
                    "Equipe Técnica A"
                ),
            )

    def test_responsavel_obrigatorio(
        self,
    ):
        """
        O planejamento deve possuir responsável.
        """

        with self.assertRaisesRegex(
            ValueError,
            "Responsável",
        ):
            criar_dados_planejamento_instalacao(
                data_prevista="2026-08-20",
                responsavel_planejamento=" ",
                equipe_responsavel=(
                    "Equipe Técnica A"
                ),
            )

    def test_equipe_obrigatoria(
        self,
    ):
        """
        O planejamento deve possuir
        equipe responsável.
        """

        with self.assertRaisesRegex(
            ValueError,
            "Equipe",
        ):
            criar_dados_planejamento_instalacao(
                data_prevista="2026-08-20",
                responsavel_planejamento=(
                    "Ana Lima"
                ),
                equipe_responsavel=" ",
            )

    def test_validar_instalacao_planejada(
        self,
    ):
        """
        Uma Instalação planejada corretamente
        deve ser válida.
        """

        resultado = validar_instalacao(
            self.instalacao
        )

        self.assertIsNone(
            resultado
        )

    def test_instalacao_planejada_nao_pode_ter_inicio(
        self,
    ):
        """
        Uma Instalação ainda planejada não pode
        possuir dados de início.
        """

        self.instalacao["data_inicio"] = (
            "2026-08-20"
        )

        self.instalacao["responsavel_inicio"] = (
            "Carlos Souza"
        )

        with self.assertRaisesRegex(
            ValueError,
            "não pode possuir",
        ):
            validar_instalacao(
                self.instalacao
            )

    def test_status_instalacao_invalido(
        self,
    ):
        """
        Um status fora do conjunto oficial
        deve ser rejeitado.
        """

        self.instalacao["status"] = (
            "CANCELADA"
        )

        with self.assertRaisesRegex(
            ValueError,
            "Status de Instalação inválido",
        ):
            validar_instalacao(
                self.instalacao
            )

    def test_campo_obrigatorio_ausente(
        self,
    ):
        """
        A estrutura incompleta deve ser rejeitada.
        """

        del self.instalacao[
            "equipe_responsavel"
        ]

        with self.assertRaisesRegex(
            ValueError,
            "campo ausente",
        ):
            validar_instalacao(
                self.instalacao
            )

class TestInicioInstalacao(
    unittest.TestCase
):
    """
    Testes do início da execução
    da Instalação.
    """

    def setUp(self):
        """
        Cria uma Instalação planejada padrão.
        """

        self.instalacao = (
            criar_dados_planejamento_instalacao(
                data_prevista="2026-08-20",
                responsavel_planejamento=(
                    "Ana Lima"
                ),
                equipe_responsavel=(
                    "Equipe Técnica A"
                ),
            )
        )

    def test_preparar_inicio_instalacao(
        self,
    ):
        """
        Deve criar uma cópia em execução
        com os dados de início.
        """

        resultado = preparar_inicio_instalacao(
            instalacao=self.instalacao,
            data_inicio="2026-08-20",
            responsavel_inicio="Carlos Souza",
        )

        self.assertEqual(
            resultado["status"],
            StatusInstalacao.EM_EXECUCAO.value,
        )

        self.assertEqual(
            resultado["data_inicio"],
            "2026-08-20",
        )

        self.assertEqual(
            resultado["responsavel_inicio"],
            "Carlos Souza",
        )

    def test_inicio_nao_deve_alterar_instalacao_original(
        self,
    ):
        """
        A preparação deve preservar
        a Instalação recebida.
        """

        preparar_inicio_instalacao(
            instalacao=self.instalacao,
            data_inicio="2026-08-20",
            responsavel_inicio="Carlos Souza",
        )

        self.assertEqual(
            self.instalacao["status"],
            StatusInstalacao.PLANEJADA.value,
        )

        self.assertIsNone(
            self.instalacao["data_inicio"]
        )

    def test_inicio_deve_normalizar_responsavel(
        self,
    ):
        """
        O responsável deve ser armazenado
        sem espaços externos.
        """

        resultado = preparar_inicio_instalacao(
            instalacao=self.instalacao,
            data_inicio="2026-08-20",
            responsavel_inicio=(
                "  Carlos Souza  "
            ),
        )

        self.assertEqual(
            resultado["responsavel_inicio"],
            "Carlos Souza",
        )

    def test_nao_deve_iniciar_instalacao_em_execucao(
        self,
    ):
        """
        Uma Instalação já iniciada
        não pode ser iniciada novamente.
        """

        instalacao_em_execucao = (
            preparar_inicio_instalacao(
                instalacao=self.instalacao,
                data_inicio="2026-08-20",
                responsavel_inicio=(
                    "Carlos Souza"
                ),
            )
        )

        with self.assertRaisesRegex(
            ValueError,
            "planejada",
        ):
            preparar_inicio_instalacao(
                instalacao=(
                    instalacao_em_execucao
                ),
                data_inicio="2026-08-21",
                responsavel_inicio=(
                    "Carlos Souza"
                ),
            )

    def test_data_inicio_invalida(
        self,
    ):
        """
        A data deve utilizar o formato ISO.
        """

        with self.assertRaisesRegex(
            ValueError,
            "AAAA-MM-DD",
        ):
            preparar_inicio_instalacao(
                instalacao=self.instalacao,
                data_inicio="20/08/2026",
                responsavel_inicio=(
                    "Carlos Souza"
                ),
            )

    def test_data_inicio_anterior_a_prevista(
        self,
    ):
        """
        O início não pode ocorrer antes
        da data prevista.
        """

        with self.assertRaisesRegex(
            ValueError,
            "anterior",
        ):
            preparar_inicio_instalacao(
                instalacao=self.instalacao,
                data_inicio="2026-08-19",
                responsavel_inicio=(
                    "Carlos Souza"
                ),
            )

    def test_responsavel_inicio_obrigatorio(
        self,
    ):
        """
        O início deve possuir responsável.
        """

        with self.assertRaisesRegex(
            ValueError,
            "Responsável",
        ):
            preparar_inicio_instalacao(
                instalacao=self.instalacao,
                data_inicio="2026-08-20",
                responsavel_inicio=" ",
            )

class TestConclusaoInstalacao(
    unittest.TestCase
):
    """
    Testes da conclusão da Instalação.
    """

    def setUp(self):
        """
        Cria uma Instalação em execução.
        """

        instalacao_planejada = (
            criar_dados_planejamento_instalacao(
                data_prevista="2026-08-20",
                responsavel_planejamento=(
                    "Ana Lima"
                ),
                equipe_responsavel=(
                    "Equipe Técnica A"
                ),
                observacoes=(
                    "Instalação programada."
                ),
            )
        )

        self.instalacao = (
            preparar_inicio_instalacao(
                instalacao=instalacao_planejada,
                data_inicio="2026-08-20",
                responsavel_inicio=(
                    "Carlos Souza"
                ),
            )
        )

    def test_preparar_conclusao_instalacao(
        self,
    ):
        """
        Deve retornar uma cópia concluída
        com os dados de encerramento.
        """

        resultado = preparar_conclusao_instalacao(
            instalacao=self.instalacao,
            data_conclusao="2026-08-22",
            responsavel_conclusao="Carlos Souza",
            observacoes=(
                "Instalação concluída."
            ),
        )

        self.assertEqual(
            resultado["status"],
            StatusInstalacao.CONCLUIDA.value,
        )

        self.assertEqual(
            resultado["data_conclusao"],
            "2026-08-22",
        )

        self.assertEqual(
            resultado[
                "responsavel_conclusao"
            ],
            "Carlos Souza",
        )

        self.assertEqual(
            resultado["observacoes"],
            "Instalação concluída.",
        )

    def test_conclusao_nao_deve_alterar_original(
        self,
    ):
        """
        A preparação não deve modificar
        a Instalação recebida.
        """

        preparar_conclusao_instalacao(
            instalacao=self.instalacao,
            data_conclusao="2026-08-22",
            responsavel_conclusao=(
                "Carlos Souza"
            ),
        )

        self.assertEqual(
            self.instalacao["status"],
            StatusInstalacao.EM_EXECUCAO.value,
        )

        self.assertIsNone(
            self.instalacao["data_conclusao"]
        )

    def test_conclusao_deve_preservar_observacao_anterior(
        self,
    ):
        """
        Quando nenhuma nova observação for informada,
        o conteúdo anterior deve ser preservado.
        """

        resultado = preparar_conclusao_instalacao(
            instalacao=self.instalacao,
            data_conclusao="2026-08-22",
            responsavel_conclusao=(
                "Carlos Souza"
            ),
        )

        self.assertEqual(
            resultado["observacoes"],
            "Instalação programada.",
        )

    def test_nao_deve_concluir_instalacao_planejada(
        self,
    ):
        """
        Uma Instalação ainda não iniciada
        não pode ser concluída.
        """

        instalacao_planejada = (
            criar_dados_planejamento_instalacao(
                data_prevista="2026-08-20",
                responsavel_planejamento=(
                    "Ana Lima"
                ),
                equipe_responsavel=(
                    "Equipe Técnica A"
                ),
            )
        )

        with self.assertRaisesRegex(
            ValueError,
            "em execução",
        ):
            preparar_conclusao_instalacao(
                instalacao=instalacao_planejada,
                data_conclusao="2026-08-22",
                responsavel_conclusao=(
                    "Carlos Souza"
                ),
            )

    def test_data_conclusao_anterior_ao_inicio(
        self,
    ):
        """
        A conclusão não pode ocorrer antes
        do início da Instalação.
        """

        with self.assertRaisesRegex(
            ValueError,
            "anterior",
        ):
            preparar_conclusao_instalacao(
                instalacao=self.instalacao,
                data_conclusao="2026-08-19",
                responsavel_conclusao=(
                    "Carlos Souza"
                ),
            )

    def test_data_conclusao_invalida(
        self,
    ):
        """
        A data deve utilizar o formato ISO.
        """

        with self.assertRaisesRegex(
            ValueError,
            "AAAA-MM-DD",
        ):
            preparar_conclusao_instalacao(
                instalacao=self.instalacao,
                data_conclusao="22/08/2026",
                responsavel_conclusao=(
                    "Carlos Souza"
                ),
            )

    def test_responsavel_conclusao_obrigatorio(
        self,
    ):
        """
        A conclusão deve possuir responsável.
        """

        with self.assertRaisesRegex(
            ValueError,
            "Responsável",
        ):
            preparar_conclusao_instalacao(
                instalacao=self.instalacao,
                data_conclusao="2026-08-22",
                responsavel_conclusao=" ",
            )

if __name__ == "__main__":
    unittest.main()