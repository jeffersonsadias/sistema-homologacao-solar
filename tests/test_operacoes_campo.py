"""
Testes da estrutura das Operações de Campo.
"""

import unittest

from app.dominio.operacoes_campo import (
    StatusInstalacao,
    criar_dados_operacoes_campo,
    criar_dados_planejamento_instalacao,
    preparar_conclusao_instalacao,
    preparar_inicio_instalacao,
    validar_instalacao,
    validar_operacoes_campo,
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