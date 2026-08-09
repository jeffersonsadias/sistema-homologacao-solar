"""
Testes da interface de terminal de Homologações.

As funções da fachada e as entradas do terminal são
simuladas para impedir alterações nos dados reais.
"""

import unittest
from unittest.mock import patch

from app.interface import homologacoes_interface


class TestHomologacoesInterface(
    unittest.TestCase
):
    """
    Testes dos fluxos iniciais da interface.
    """

    @patch(
        "app.interface.homologacoes_interface."
        "_exibir_homologacao"
    )
    @patch(
        "app.interface.homologacoes_interface."
        "homologacoes.criar_homologacao"
    )
    @patch(
        "app.interface.homologacoes_interface."
        "ler_int",
        side_effect=[
            1,
            10,
            2,
        ],
    )
    @patch(
        "builtins.input",
        side_effect=[
            "2026-08-03",
            "Ana Lima",
            "Processo inicial.",
        ],
    )
    def test_cadastrar_homologacao(
        self,
        mock_input,
        mock_ler_int,
        mock_criar,
        mock_exibir,
    ):
        homologacao_criada = {
            "codigo": 1,
        }

        mock_criar.return_value = (
            homologacao_criada
        )

        (
            homologacoes_interface
            .cadastrar_homologacao_interface()
        )

        mock_criar.assert_called_once_with(
            codigo_empresa=1,
            codigo_projeto=10,
            codigo_concessionaria=2,
            data_abertura="2026-08-03",
            responsavel_abertura="Ana Lima",
            observacoes="Processo inicial.",
        )

        mock_exibir.assert_called_once_with(
            homologacao_criada
        )

    @patch(
        "builtins.print"
    )
    @patch(
        "app.interface.homologacoes_interface."
        "homologacoes.criar_homologacao",
        side_effect=ValueError(
            "Projeto já possui Homologação."
        ),
    )
    @patch(
        "app.interface.homologacoes_interface."
        "ler_int",
        side_effect=[
            1,
            10,
            2,
        ],
    )
    @patch(
        "builtins.input",
        side_effect=[
            "2026-08-03",
            "Ana Lima",
            "",
        ],
    )
    def test_cadastro_invalido_exibe_erro(
        self,
        mock_input,
        mock_ler_int,
        mock_criar,
        mock_print,
    ):
        (
            homologacoes_interface
            .cadastrar_homologacao_interface()
        )

        mock_print.assert_any_call(
            "\nNão foi possível criar a Homologação: "
            "Projeto já possui Homologação."
        )

    @patch(
        "app.interface.homologacoes_interface."
        "_exibir_homologacao"
    )
    @patch(
        "app.interface.homologacoes_interface."
        "homologacoes.listar_homologacoes"
    )
    @patch(
        "app.interface.homologacoes_interface."
        "ler_int",
        return_value=1,
    )
    def test_listar_homologacoes(
        self,
        mock_ler_int,
        mock_listar,
        mock_exibir,
    ):
        primeira = {
            "codigo": 1,
        }

        segunda = {
            "codigo": 2,
        }

        mock_listar.return_value = [
            primeira,
            segunda,
        ]

        (
            homologacoes_interface
            .listar_homologacoes_interface()
        )

        mock_listar.assert_called_once_with(
            codigo_empresa=1,
        )

        self.assertEqual(
            mock_exibir.call_count,
            2,
        )

        mock_exibir.assert_any_call(
            primeira
        )

        mock_exibir.assert_any_call(
            segunda
        )

    @patch(
        "builtins.print"
    )
    @patch(
        "app.interface.homologacoes_interface."
        "homologacoes.listar_homologacoes",
        return_value=[],
    )
    @patch(
        "app.interface.homologacoes_interface."
        "ler_int",
        return_value=1,
    )
    def test_listar_sem_homologacoes(
        self,
        mock_ler_int,
        mock_listar,
        mock_print,
    ):
        (
            homologacoes_interface
            .listar_homologacoes_interface()
        )

        mock_print.assert_any_call(
            "\nNenhuma Homologação encontrada "
            "para esta Empresa."
        )

    @patch(
        "app.interface.homologacoes_interface."
        "_exibir_homologacao"
    )
    @patch(
        "app.interface.homologacoes_interface."
        "homologacoes.buscar_homologacao"
    )
    @patch(
        "app.interface.homologacoes_interface."
        "ler_int",
        side_effect=[
            1,
            5,
        ],
    )
    def test_buscar_homologacao(
        self,
        mock_ler_int,
        mock_buscar,
        mock_exibir,
    ):
        homologacao_encontrada = {
            "codigo": 5,
        }

        mock_buscar.return_value = (
            homologacao_encontrada
        )

        (
            homologacoes_interface
            .buscar_homologacao_interface()
        )

        mock_buscar.assert_called_once_with(
            codigo_homologacao=5,
            codigo_empresa=1,
        )

        mock_exibir.assert_called_once_with(
            homologacao_encontrada
        )

    @patch(
        "builtins.print"
    )
    @patch(
        "app.interface.homologacoes_interface."
        "homologacoes.buscar_homologacao",
        return_value=None,
    )
    @patch(
        "app.interface.homologacoes_interface."
        "ler_int",
        side_effect=[
            1,
            999,
        ],
    )
    def test_buscar_homologacao_inexistente(
        self,
        mock_ler_int,
        mock_buscar,
        mock_print,
    ):
        (
            homologacoes_interface
            .buscar_homologacao_interface()
        )

        mock_print.assert_any_call(
            "\nHomologação não encontrada."
        )

    @patch(
        "app.interface.homologacoes_interface."
        "_exibir_instalacao"
    )
    @patch(
        "app.interface.homologacoes_interface."
        "homologacoes.planejar_instalacao"
    )
    @patch(
        "app.interface.homologacoes_interface."
        "ler_int",
        side_effect=[
            10,
            5,
        ],
    )
    @patch(
        "builtins.input",
        side_effect=[
            "2026-08-20",
            "Ana Lima",
            "Equipe Técnica A",
            "2026-08-10",
            "Instalação programada.",
        ],
    )
    def test_planejar_instalacao_interface(
        self,
        mock_input,
        mock_ler_int,
        mock_planejar,
        mock_exibir,
    ):
        """
        Deve coletar os dados, chamar a fachada
        e exibir a Instalação planejada.
        """

        homologacao_atualizada = {
            "codigo": 5,
        }

        mock_planejar.return_value = (
            homologacao_atualizada
        )

        (
            homologacoes_interface
            .planejar_instalacao_interface()
        )

        mock_planejar.assert_called_once_with(
            codigo_homologacao=5,
            codigo_empresa=10,
            data_prevista="2026-08-20",
            responsavel_planejamento="Ana Lima",
            equipe_responsavel="Equipe Técnica A",
            data_movimentacao="2026-08-10",
            observacoes="Instalação programada.",
        )

        mock_exibir.assert_called_once_with(
            homologacao_atualizada
        )

    @patch(
        "builtins.print"
    )
    @patch(
        "app.interface.homologacoes_interface."
        "_exibir_instalacao"
    )
    @patch(
        "app.interface.homologacoes_interface."
        "homologacoes.planejar_instalacao",
        side_effect=ValueError(
            "Estado incompatível."
        ),
    )
    @patch(
        "app.interface.homologacoes_interface."
        "ler_int",
        side_effect=[
            10,
            5,
        ],
    )
    @patch(
        "builtins.input",
        side_effect=[
            "2026-08-20",
            "Ana Lima",
            "Equipe Técnica A",
            "2026-08-10",
            "",
        ],
    )
    def test_planejamento_invalido_exibe_erro(
        self,
        mock_input,
        mock_ler_int,
        mock_planejar,
        mock_exibir,
        mock_print,
    ):
        """
        Uma falha da fachada deve ser apresentada
        sem exibir uma Instalação.
        """

        (
            homologacoes_interface
            .planejar_instalacao_interface()
        )

        mock_exibir.assert_not_called()

        mock_print.assert_any_call(
            "\nNão foi possível planejar "
            "a Instalação: Estado incompatível."
        )

    @patch(
        "app.interface.homologacoes_interface."
        "_exibir_instalacao"
    )
    @patch(
        "app.interface.homologacoes_interface."
        "homologacoes.iniciar_execucao_instalacao"
    )
    @patch(
        "app.interface.homologacoes_interface."
        "ler_int",
        side_effect=[
            10,
            5,
        ],
    )
    @patch(
        "builtins.input",
        side_effect=[
            "2026-08-20",
            "Carlos Souza",
            "2026-08-20",
        ],
    )
    def test_iniciar_instalacao_interface(
        self,
        mock_input,
        mock_ler_int,
        mock_iniciar,
        mock_exibir,
    ):
        """
        Deve registrar o início da Instalação
        por meio da fachada.
        """

        homologacao_atualizada = {
            "codigo": 5,
        }

        mock_iniciar.return_value = (
            homologacao_atualizada
        )

        (
            homologacoes_interface
            .iniciar_instalacao_interface()
        )

        mock_iniciar.assert_called_once_with(
            codigo_homologacao=5,
            codigo_empresa=10,
            data_inicio="2026-08-20",
            responsavel_inicio="Carlos Souza",
            data_movimentacao="2026-08-20",
        )

        mock_exibir.assert_called_once_with(
            homologacao_atualizada
        )

    @patch(
        "app.interface.homologacoes_interface."
        "_exibir_instalacao"
    )
    @patch(
        "app.interface.homologacoes_interface."
        "homologacoes.concluir_execucao_instalacao"
    )
    @patch(
        "app.interface.homologacoes_interface."
        "ler_int",
        side_effect=[
            10,
            5,
        ],
    )
    @patch(
        "builtins.input",
        side_effect=[
            "2026-08-22",
            "Carlos Souza",
            "2026-08-22",
            "Instalação concluída.",
        ],
    )
    def test_concluir_instalacao_interface(
        self,
        mock_input,
        mock_ler_int,
        mock_concluir,
        mock_exibir,
    ):
        """
        Deve registrar a conclusão da Instalação
        por meio da fachada.
        """

        homologacao_atualizada = {
            "codigo": 5,
        }

        mock_concluir.return_value = (
            homologacao_atualizada
        )

        (
            homologacoes_interface
            .concluir_instalacao_interface()
        )

        mock_concluir.assert_called_once_with(
            codigo_homologacao=5,
            codigo_empresa=10,
            data_conclusao="2026-08-22",
            responsavel_conclusao="Carlos Souza",
            data_movimentacao="2026-08-22",
            observacoes="Instalação concluída.",
        )

        mock_exibir.assert_called_once_with(
            homologacao_atualizada
        )

    @patch(
        "app.interface.homologacoes_interface."
        "_pausar"
    )
    @patch(
        "app.interface.homologacoes_interface."
        "planejar_instalacao_interface"
    )
    @patch(
        "builtins.input",
        side_effect=[
            "1",
            "0",
        ],
    )
    def test_menu_instalacao_deve_abrir_planejamento(
        self,
        mock_input,
        mock_planejar,
        mock_pausar,
    ):
        """
        A opção 1 deve abrir
        o planejamento da Instalação.
        """

        homologacoes_interface.menu_instalacao()

        mock_planejar.assert_called_once_with()
        mock_pausar.assert_called_once_with()

    @patch(
        "app.interface.homologacoes_interface."
        "_pausar"
    )
    @patch(
        "app.interface.homologacoes_interface."
        "iniciar_instalacao_interface"
    )
    @patch(
        "builtins.input",
        side_effect=[
            "2",
            "0",
        ],
    )
    def test_menu_instalacao_deve_abrir_inicio(
        self,
        mock_input,
        mock_iniciar,
        mock_pausar,
    ):
        """
        A opção 2 deve abrir
        o início da Instalação.
        """

        homologacoes_interface.menu_instalacao()

        mock_iniciar.assert_called_once_with()
        mock_pausar.assert_called_once_with()

    @patch(
        "app.interface.homologacoes_interface."
        "_pausar"
    )
    @patch(
        "app.interface.homologacoes_interface."
        "concluir_instalacao_interface"
    )
    @patch(
        "builtins.input",
        side_effect=[
            "3",
            "0",
        ],
    )
    def test_menu_instalacao_deve_abrir_conclusao(
        self,
        mock_input,
        mock_concluir,
        mock_pausar,
    ):
        """
        A opção 3 deve abrir
        a conclusão da Instalação.
        """

        homologacoes_interface.menu_instalacao()

        mock_concluir.assert_called_once_with()
        mock_pausar.assert_called_once_with()

    # ========================================================
    # OPERAÇÕES DE CAMPO — VISTORIA
    # ========================================================

    @patch(
        "app.interface.homologacoes_interface."
        "_exibir_vistorias"
    )
    @patch(
        "app.interface.homologacoes_interface."
        "homologacoes.solicitar_nova_vistoria"
    )
    @patch(
        "app.interface.homologacoes_interface."
        "ler_int",
        side_effect=[
            10,
            5,
        ],
    )
    @patch(
        "builtins.input",
        side_effect=[
            "2026-08-25",
            "Ana Lima",
            "VST-2026-001",
            "2026-08-25",
            "Primeira tentativa.",
        ],
    )
    def test_solicitar_vistoria_interface(
        self,
        mock_input,
        mock_ler_int,
        mock_solicitar,
        mock_exibir,
    ):
        """
        Deve coletar os dados, solicitar
        a Vistoria e exibir o resultado.
        """

        homologacao_atualizada = {
            "codigo": 5,
        }

        mock_solicitar.return_value = (
            homologacao_atualizada
        )

        (
            homologacoes_interface
            .solicitar_vistoria_interface()
        )

        mock_solicitar.assert_called_once_with(
            codigo_homologacao=5,
            codigo_empresa=10,
            data_solicitacao="2026-08-25",
            responsavel_solicitacao="Ana Lima",
            protocolo="VST-2026-001",
            data_movimentacao="2026-08-25",
            observacoes="Primeira tentativa.",
        )

        mock_exibir.assert_called_once_with(
            homologacao_atualizada
        )

    @patch(
        "builtins.print"
    )
    @patch(
        "app.interface.homologacoes_interface."
        "_exibir_vistorias"
    )
    @patch(
        "app.interface.homologacoes_interface."
        "homologacoes.solicitar_nova_vistoria",
        side_effect=ValueError(
            "Estado incompatível."
        ),
    )
    @patch(
        "app.interface.homologacoes_interface."
        "ler_int",
        side_effect=[
            10,
            5,
        ],
    )
    @patch(
        "builtins.input",
        side_effect=[
            "2026-08-25",
            "Ana Lima",
            "VST-2026-001",
            "2026-08-25",
            "",
        ],
    )
    def test_solicitacao_vistoria_invalida_exibe_erro(
        self,
        mock_input,
        mock_ler_int,
        mock_solicitar,
        mock_exibir,
        mock_print,
    ):
        """
        Uma falha da fachada deve ser apresentada
        sem exibir as Vistorias.
        """

        (
            homologacoes_interface
            .solicitar_vistoria_interface()
        )

        mock_exibir.assert_not_called()

        mock_print.assert_any_call(
            "\nNão foi possível solicitar "
            "a Vistoria: Estado incompatível."
        )

    @patch(
        "app.interface.homologacoes_interface."
        "_exibir_vistorias"
    )
    @patch(
        "app.interface.homologacoes_interface."
        "homologacoes.agendar_vistoria_homologacao"
    )
    @patch(
        "app.interface.homologacoes_interface."
        "ler_int",
        side_effect=[
            10,
            5,
            1,
        ],
    )
    @patch(
        "builtins.input",
        side_effect=[
            "2026-08-30",
            "Carlos Souza",
            "2026-08-26",
            "Visita programada.",
        ],
    )
    def test_agendar_vistoria_interface(
        self,
        mock_input,
        mock_ler_int,
        mock_agendar,
        mock_exibir,
    ):
        """
        Deve coletar os dados, agendar
        a Vistoria e exibir o resultado.
        """

        homologacao_atualizada = {
            "codigo": 5,
        }

        mock_agendar.return_value = (
            homologacao_atualizada
        )

        (
            homologacoes_interface
            .agendar_vistoria_interface()
        )

        mock_agendar.assert_called_once_with(
            codigo_homologacao=5,
            codigo_empresa=10,
            codigo_vistoria=1,
            data_agendamento="2026-08-30",
            responsavel_agendamento=(
                "Carlos Souza"
            ),
            data_movimentacao="2026-08-26",
            observacoes="Visita programada.",
        )

        mock_exibir.assert_called_once_with(
            homologacao_atualizada
        )

    @patch(
        "app.interface.homologacoes_interface."
        "_exibir_vistorias"
    )
    @patch(
        "app.interface.homologacoes_interface."
        "homologacoes."
        "registrar_realizacao_vistoria_homologacao"
    )
    @patch(
        "app.interface.homologacoes_interface."
        "ler_int",
        side_effect=[
            10,
            5,
            1,
        ],
    )
    @patch(
        "builtins.input",
        side_effect=[
            "2026-08-30",
            "Marcos Oliveira",
            "2026-08-30",
            "Vistoria realizada no local.",
        ],
    )
    def test_registrar_realizacao_vistoria_interface(
        self,
        mock_input,
        mock_ler_int,
        mock_realizar,
        mock_exibir,
    ):
        """
        Deve coletar os dados, registrar
        a realização e exibir o resultado.
        """

        homologacao_atualizada = {
            "codigo": 5,
        }

        mock_realizar.return_value = (
            homologacao_atualizada
        )

        (
            homologacoes_interface
            .registrar_realizacao_vistoria_interface()
        )

        mock_realizar.assert_called_once_with(
            codigo_homologacao=5,
            codigo_empresa=10,
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

        mock_exibir.assert_called_once_with(
            homologacao_atualizada
        )

    @patch(
        "builtins.print"
    )
    @patch(
        "app.interface.homologacoes_interface."
        "_exibir_vistorias"
    )
    @patch(
        "app.interface.homologacoes_interface."
        "homologacoes.agendar_vistoria_homologacao",
        side_effect=ValueError(
            "Vistoria não encontrada."
        ),
    )
    @patch(
        "app.interface.homologacoes_interface."
        "ler_int",
        side_effect=[
            10,
            5,
            999,
        ],
    )
    @patch(
        "builtins.input",
        side_effect=[
            "2026-08-30",
            "Carlos Souza",
            "2026-08-26",
            "",
        ],
    )
    def test_agendamento_vistoria_invalido_exibe_erro(
        self,
        mock_input,
        mock_ler_int,
        mock_agendar,
        mock_exibir,
        mock_print,
    ):
        """
        Uma falha no agendamento deve ser
        apresentada sem exibir as Vistorias.
        """

        (
            homologacoes_interface
            .agendar_vistoria_interface()
        )

        mock_exibir.assert_not_called()

        mock_print.assert_any_call(
            "\nNão foi possível agendar "
            "a Vistoria: Vistoria não encontrada."
        )

    @patch(
        "app.interface.homologacoes_interface."
        "_exibir_vistorias"
    )
    @patch(
        "app.interface.homologacoes_interface."
        "homologacoes.aprovar_vistoria_homologacao"
    )
    @patch(
        "app.interface.homologacoes_interface."
        "ler_int",
        side_effect=[
            10,
            5,
            1,
        ],
    )
    @patch(
        "builtins.input",
        side_effect=[
            "2026-09-01",
            "Ana Lima",
            "2026-09-01",
            "Vistoria aprovada.",
        ],
    )
    def test_aprovar_vistoria_interface(
        self,
        mock_input,
        mock_ler_int,
        mock_aprovar,
        mock_exibir,
    ):
        """
        Deve registrar a aprovação por meio
        da fachada e exibir o resultado.
        """

        homologacao_atualizada = {
            "codigo": 5,
        }

        mock_aprovar.return_value = (
            homologacao_atualizada
        )

        (
            homologacoes_interface
            .aprovar_vistoria_interface()
        )

        mock_aprovar.assert_called_once_with(
            codigo_homologacao=5,
            codigo_empresa=10,
            codigo_vistoria=1,
            data_resultado="2026-09-01",
            responsavel_resultado="Ana Lima",
            data_movimentacao="2026-09-01",
            observacoes="Vistoria aprovada.",
        )

        mock_exibir.assert_called_once_with(
            homologacao_atualizada
        )

    @patch(
        "app.interface.homologacoes_interface."
        "_exibir_vistorias"
    )
    @patch(
        "app.interface.homologacoes_interface."
        "homologacoes.reprovar_vistoria_homologacao"
    )
    @patch(
        "app.interface.homologacoes_interface."
        "ler_int",
        side_effect=[
            10,
            5,
            1,
        ],
    )
    @patch(
        "builtins.input",
        side_effect=[
            "2026-09-01",
            "Ana Lima",
            "Inversor sem identificação.",
            "2026-09-01",
            "Necessária regularização.",
        ],
    )
    def test_reprovar_vistoria_interface(
        self,
        mock_input,
        mock_ler_int,
        mock_reprovar,
        mock_exibir,
    ):
        """
        Deve registrar a reprovação por meio
        da fachada e exibir o resultado.
        """

        homologacao_atualizada = {
            "codigo": 5,
        }

        mock_reprovar.return_value = (
            homologacao_atualizada
        )

        (
            homologacoes_interface
            .reprovar_vistoria_interface()
        )

        mock_reprovar.assert_called_once_with(
            codigo_homologacao=5,
            codigo_empresa=10,
            codigo_vistoria=1,
            data_resultado="2026-09-01",
            responsavel_resultado="Ana Lima",
            motivo_reprovacao=(
                "Inversor sem identificação."
            ),
            data_movimentacao="2026-09-01",
            observacoes=(
                "Necessária regularização."
            ),
        )

        mock_exibir.assert_called_once_with(
            homologacao_atualizada
        )

    @patch(
        "app.interface.homologacoes_interface."
        "_exibir_vistorias"
    )
    @patch(
        "app.interface.homologacoes_interface."
        "homologacoes."
        "registrar_correcao_pos_vistoria_homologacao"
    )
    @patch(
        "app.interface.homologacoes_interface."
        "ler_int",
        side_effect=[
            10,
            5,
            1,
        ],
    )
    @patch(
        "builtins.input",
        side_effect=[
            "Identificação do inversor instalada.",
            "Carlos Souza",
            "2026-09-03",
        ],
    )
    def test_registrar_correcao_pos_vistoria_interface(
        self,
        mock_input,
        mock_ler_int,
        mock_correcao,
        mock_exibir,
    ):
        """
        Deve registrar a correção pós-vistoria
        por meio da fachada.
        """

        homologacao_atualizada = {
            "codigo": 5,
        }

        mock_correcao.return_value = (
            homologacao_atualizada
        )

        (
            homologacoes_interface
            .registrar_correcao_pos_vistoria_interface()
        )

        mock_correcao.assert_called_once_with(
            codigo_homologacao=5,
            codigo_empresa=10,
            codigo_vistoria=1,
            descricao_correcao=(
                "Identificação do inversor instalada."
            ),
            responsavel_correcao="Carlos Souza",
            data_movimentacao="2026-09-03",
        )

        mock_exibir.assert_called_once_with(
            homologacao_atualizada
        )

    @patch(
        "builtins.print"
    )
    @patch(
        "app.interface.homologacoes_interface."
        "_exibir_vistorias"
    )
    @patch(
        "app.interface.homologacoes_interface."
        "homologacoes.reprovar_vistoria_homologacao",
        side_effect=ValueError(
            "Motivo da reprovação é obrigatório."
        ),
    )
    @patch(
        "app.interface.homologacoes_interface."
        "ler_int",
        side_effect=[
            10,
            5,
            1,
        ],
    )
    @patch(
        "builtins.input",
        side_effect=[
            "2026-09-01",
            "Ana Lima",
            "",
            "2026-09-01",
            "",
        ],
    )
    def test_reprovacao_vistoria_invalida_exibe_erro(
        self,
        mock_input,
        mock_ler_int,
        mock_reprovar,
        mock_exibir,
        mock_print,
    ):
        """
        Uma falha na reprovação deve ser
        apresentada sem exibir as Vistorias.
        """

        (
            homologacoes_interface
            .reprovar_vistoria_interface()
        )

        mock_exibir.assert_not_called()

        mock_print.assert_any_call(
            "\nNão foi possível reprovar "
            "a Vistoria: "
            "Motivo da reprovação é obrigatório."
        )

    @patch(
        "app.interface.homologacoes_interface."
        "_pausar"
    )
    @patch(
        "app.interface.homologacoes_interface."
        "solicitar_vistoria_interface"
    )
    @patch(
        "builtins.input",
        side_effect=[
            "1",
            "0",
        ],
    )
    def test_menu_vistoria_deve_abrir_solicitacao(
        self,
        mock_input,
        mock_solicitar,
        mock_pausar,
    ):
        """
        A opção 1 deve abrir
        a solicitação da Vistoria.
        """

        homologacoes_interface.menu_vistoria()

        mock_solicitar.assert_called_once_with()
        mock_pausar.assert_called_once_with()

    @patch(
        "app.interface.homologacoes_interface."
        "_pausar"
    )
    @patch(
        "app.interface.homologacoes_interface."
        "agendar_vistoria_interface"
    )
    @patch(
        "builtins.input",
        side_effect=[
            "2",
            "0",
        ],
    )
    def test_menu_vistoria_deve_abrir_agendamento(
        self,
        mock_input,
        mock_agendar,
        mock_pausar,
    ):
        """
        A opção 2 deve abrir
        o agendamento da Vistoria.
        """

        homologacoes_interface.menu_vistoria()

        mock_agendar.assert_called_once_with()
        mock_pausar.assert_called_once_with()

    @patch(
        "app.interface.homologacoes_interface."
        "_pausar"
    )
    @patch(
        "app.interface.homologacoes_interface."
        "registrar_realizacao_vistoria_interface"
    )
    @patch(
        "builtins.input",
        side_effect=[
            "3",
            "0",
        ],
    )
    def test_menu_vistoria_deve_abrir_realizacao(
        self,
        mock_input,
        mock_realizar,
        mock_pausar,
    ):
        """
        A opção 3 deve abrir
        a realização da Vistoria.
        """

        homologacoes_interface.menu_vistoria()

        mock_realizar.assert_called_once_with()
        mock_pausar.assert_called_once_with()

    @patch(
        "app.interface.homologacoes_interface."
        "_pausar"
    )
    @patch(
        "app.interface.homologacoes_interface."
        "aprovar_vistoria_interface"
    )
    @patch(
        "builtins.input",
        side_effect=[
            "4",
            "0",
        ],
    )
    def test_menu_vistoria_deve_abrir_aprovacao(
        self,
        mock_input,
        mock_aprovar,
        mock_pausar,
    ):
        """
        A opção 4 deve abrir
        a aprovação da Vistoria.
        """

        homologacoes_interface.menu_vistoria()

        mock_aprovar.assert_called_once_with()
        mock_pausar.assert_called_once_with()

    @patch(
        "app.interface.homologacoes_interface."
        "_pausar"
    )
    @patch(
        "app.interface.homologacoes_interface."
        "reprovar_vistoria_interface"
    )
    @patch(
        "builtins.input",
        side_effect=[
            "5",
            "0",
        ],
    )
    def test_menu_vistoria_deve_abrir_reprovacao(
        self,
        mock_input,
        mock_reprovar,
        mock_pausar,
    ):
        """
        A opção 5 deve abrir
        a reprovação da Vistoria.
        """

        homologacoes_interface.menu_vistoria()

        mock_reprovar.assert_called_once_with()
        mock_pausar.assert_called_once_with()

    @patch(
        "app.interface.homologacoes_interface."
        "_pausar"
    )
    @patch(
        "app.interface.homologacoes_interface."
        "registrar_correcao_pos_vistoria_interface"
    )
    @patch(
        "builtins.input",
        side_effect=[
            "6",
            "0",
        ],
    )
    def test_menu_vistoria_deve_abrir_correcao(
        self,
        mock_input,
        mock_correcao,
        mock_pausar,
    ):
        """
        A opção 6 deve abrir
        a correção pós-vistoria.
        """

        homologacoes_interface.menu_vistoria()

        mock_correcao.assert_called_once_with()
        mock_pausar.assert_called_once_with()

    # ========================================================
    # OPERAÇÕES DE CAMPO — LIGAÇÃO E ENERGIZAÇÃO
    # ========================================================

    @patch(
        "app.interface.homologacoes_interface."
        "_exibir_ligacao"
    )
    @patch(
        "app.interface.homologacoes_interface."
        "homologacoes.solicitar_ligacao_homologacao"
    )
    @patch(
        "app.interface.homologacoes_interface."
        "ler_int",
        side_effect=[
            10,
            5,
        ],
    )
    @patch(
        "builtins.input",
        side_effect=[
            "2026-09-05",
            "Ana Lima",
            "LIG-2026-001",
            "2026-09-05",
            "Solicitação enviada.",
        ],
    )
    def test_solicitar_ligacao_interface(
        self,
        mock_input,
        mock_ler_int,
        mock_solicitar,
        mock_exibir,
    ):
        homologacao_atualizada = {
            "codigo": 5,
        }

        mock_solicitar.return_value = (
            homologacao_atualizada
        )

        (
            homologacoes_interface
            .solicitar_ligacao_interface()
        )

        mock_solicitar.assert_called_once_with(
            codigo_homologacao=5,
            codigo_empresa=10,
            data_solicitacao="2026-09-05",
            responsavel_solicitacao="Ana Lima",
            protocolo="LIG-2026-001",
            data_movimentacao="2026-09-05",
            observacoes="Solicitação enviada.",
        )

        mock_exibir.assert_called_once_with(
            homologacao_atualizada
        )

    @patch(
        "app.interface.homologacoes_interface."
        "_exibir_ligacao"
    )
    @patch(
        "app.interface.homologacoes_interface."
        "homologacoes.agendar_ligacao_homologacao"
    )
    @patch(
        "app.interface.homologacoes_interface."
        "ler_int",
        side_effect=[
            10,
            5,
        ],
    )
    @patch(
        "builtins.input",
        side_effect=[
            "2026-09-10",
            "Carlos Souza",
            "2026-09-06",
            "Ligação programada.",
        ],
    )
    def test_agendar_ligacao_interface(
        self,
        mock_input,
        mock_ler_int,
        mock_agendar,
        mock_exibir,
    ):
        homologacao_atualizada = {
            "codigo": 5,
        }

        mock_agendar.return_value = (
            homologacao_atualizada
        )

        (
            homologacoes_interface
            .agendar_ligacao_interface()
        )

        mock_agendar.assert_called_once_with(
            codigo_homologacao=5,
            codigo_empresa=10,
            data_agendamento="2026-09-10",
            responsavel_agendamento="Carlos Souza",
            data_movimentacao="2026-09-06",
            observacoes="Ligação programada.",
        )

        mock_exibir.assert_called_once_with(
            homologacao_atualizada
        )

    @patch(
        "app.interface.homologacoes_interface."
        "_exibir_ligacao"
    )
    @patch(
        "app.interface.homologacoes_interface."
        "homologacoes.concluir_ligacao_homologacao"
    )
    @patch(
        "app.interface.homologacoes_interface."
        "ler_int",
        side_effect=[
            10,
            5,
        ],
    )
    @patch(
        "builtins.input",
        side_effect=[
            "2026-09-10",
            "Equipe da Concessionária",
            "2026-09-10",
            "Sistema energizado.",
        ],
    )
    def test_concluir_ligacao_interface(
        self,
        mock_input,
        mock_ler_int,
        mock_concluir,
        mock_exibir,
    ):
        homologacao_atualizada = {
            "codigo": 5,
        }

        mock_concluir.return_value = (
            homologacao_atualizada
        )

        (
            homologacoes_interface
            .concluir_ligacao_interface()
        )

        mock_concluir.assert_called_once_with(
            codigo_homologacao=5,
            codigo_empresa=10,
            data_ligacao="2026-09-10",
            responsavel_ligacao=(
                "Equipe da Concessionária"
            ),
            data_movimentacao="2026-09-10",
            observacoes="Sistema energizado.",
        )

        mock_exibir.assert_called_once_with(
            homologacao_atualizada
        )

    @patch(
        "builtins.print"
    )
    @patch(
        "app.interface.homologacoes_interface."
        "_exibir_ligacao"
    )
    @patch(
        "app.interface.homologacoes_interface."
        "homologacoes.concluir_ligacao_homologacao",
        side_effect=ValueError(
            "Somente uma Ligação agendada "
            "pode ser concluída."
        ),
    )
    @patch(
        "app.interface.homologacoes_interface."
        "ler_int",
        side_effect=[
            10,
            5,
        ],
    )
    @patch(
        "builtins.input",
        side_effect=[
            "2026-09-10",
            "Equipe da Concessionária",
            "2026-09-10",
            "",
        ],
    )
    def test_conclusao_ligacao_invalida_exibe_erro(
        self,
        mock_input,
        mock_ler_int,
        mock_concluir,
        mock_exibir,
        mock_print,
    ):
        (
            homologacoes_interface
            .concluir_ligacao_interface()
        )

        mock_exibir.assert_not_called()

        mock_print.assert_any_call(
            "\nNão foi possível registrar "
            "a Ligação: Somente uma Ligação "
            "agendada pode ser concluída."
        )

    @patch(
        "app.interface.homologacoes_interface."
        "_pausar"
    )
    @patch(
        "app.interface.homologacoes_interface."
        "solicitar_ligacao_interface"
    )
    @patch(
        "builtins.input",
        side_effect=[
            "1",
            "0",
        ],
    )
    def test_menu_ligacao_deve_abrir_solicitacao(
        self,
        mock_input,
        mock_solicitar,
        mock_pausar,
    ):
        homologacoes_interface.menu_ligacao()

        mock_solicitar.assert_called_once_with()
        mock_pausar.assert_called_once_with()

    @patch(
        "app.interface.homologacoes_interface."
        "_pausar"
    )
    @patch(
        "app.interface.homologacoes_interface."
        "agendar_ligacao_interface"
    )
    @patch(
        "builtins.input",
        side_effect=[
            "2",
            "0",
        ],
    )
    def test_menu_ligacao_deve_abrir_agendamento(
        self,
        mock_input,
        mock_agendar,
        mock_pausar,
    ):
        homologacoes_interface.menu_ligacao()

        mock_agendar.assert_called_once_with()
        mock_pausar.assert_called_once_with()

    @patch(
        "app.interface.homologacoes_interface."
        "_pausar"
    )
    @patch(
        "app.interface.homologacoes_interface."
        "concluir_ligacao_interface"
    )
    @patch(
        "builtins.input",
        side_effect=[
            "3",
            "0",
        ],
    )
    def test_menu_ligacao_deve_abrir_conclusao(
        self,
        mock_input,
        mock_concluir,
        mock_pausar,
    ):
        homologacoes_interface.menu_ligacao()

        mock_concluir.assert_called_once_with()
        mock_pausar.assert_called_once_with()

    @patch(
        "builtins.print"
    )
    @patch(
        "builtins.input",
        return_value="0",
    )
    def test_menu_homologacoes_deve_exibir_gestao_ligacao(
        self,
        mock_input,
        mock_print,
    ):
        homologacoes_interface.menu_homologacoes()

        mock_print.assert_any_call(
            "6 - Gerenciar Ligação e Energização"
        )

    @patch(
        "app.interface.homologacoes_interface."
        "menu_ligacao"
    )
    @patch(
        "builtins.input",
        side_effect=[
            "6",
            "0",
        ],
    )
    def test_menu_deve_abrir_gestao_ligacao(
        self,
        mock_input,
        mock_menu_ligacao,
    ):
        homologacoes_interface.menu_homologacoes()

        mock_menu_ligacao.assert_called_once_with()

    # ========================================================
    # TESTES DE ENCERRAMENTO
    # ========================================================

    @patch(
        "app.interface.homologacoes_interface."
        "_exibir_homologacao"
    )
    @patch(
        "app.interface.homologacoes_interface."
        "homologacoes.concluir_homologacao_fachada"
    )
    @patch(
        "app.interface.homologacoes_interface."
        "ler_int",
        side_effect=[
            10,
            5,
        ],
    )
    @patch(
        "builtins.input",
        side_effect=[
            "2026-09-11",
            "Ana Lima",
            "Processo encerrado.",
        ],
    )
    def test_concluir_homologacao_interface(
        self,
        mock_input,
        mock_ler_int,
        mock_concluir,
        mock_exibir,
    ):
        homologacao_atualizada = {
            "codigo": 5,
            "status": "CONCLUIDA",
        }

        mock_concluir.return_value = (
            homologacao_atualizada
        )

        (
            homologacoes_interface
            .concluir_homologacao_interface()
        )

        mock_concluir.assert_called_once_with(
            codigo_homologacao=5,
            codigo_empresa=10,
            data_conclusao="2026-09-11",
            responsavel_conclusao="Ana Lima",
            observacoes="Processo encerrado.",
        )

        mock_exibir.assert_called_once_with(
            homologacao_atualizada
        )

    @patch(
        "builtins.print"
    )
    @patch(
        "app.interface.homologacoes_interface."
        "_exibir_homologacao"
    )
    @patch(
        "app.interface.homologacoes_interface."
        "homologacoes.concluir_homologacao_fachada",
        side_effect=ValueError(
            "A Homologação somente pode ser concluída "
            "quando o sistema estiver ligado."
        ),
    )
    @patch(
        "app.interface.homologacoes_interface."
        "ler_int",
        side_effect=[
            10,
            5,
        ],
    )
    @patch(
        "builtins.input",
        side_effect=[
            "2026-09-11",
            "Ana Lima",
            "",
        ],
    )
    def test_encerramento_invalido_exibe_erro(
        self,
        mock_input,
        mock_ler_int,
        mock_concluir,
        mock_exibir,
        mock_print,
    ):
        (
            homologacoes_interface
            .concluir_homologacao_interface()
        )

        mock_exibir.assert_not_called()

        mock_print.assert_any_call(
            "\nNão foi possível concluir "
            "a Homologação: "
            "A Homologação somente pode ser concluída "
            "quando o sistema estiver ligado."
        )

    @patch(
        "builtins.print"
    )
    @patch(
        "builtins.input",
        return_value="0",
    )
    def test_menu_homologacoes_deve_exibir_encerramento(
        self,
        mock_input,
        mock_print,
    ):
        homologacoes_interface.menu_homologacoes()

        mock_print.assert_any_call(
            "7 - Encerrar Homologação"
        )

    @patch(
        "app.interface.homologacoes_interface."
        "_pausar"
    )
    @patch(
        "app.interface.homologacoes_interface."
        "concluir_homologacao_interface"
    )
    @patch(
        "builtins.input",
        side_effect=[
            "7",
            "0",
        ],
    )
    def test_menu_deve_abrir_encerramento(
        self,
        mock_input,
        mock_concluir,
        mock_pausar,
    ):
        homologacoes_interface.menu_homologacoes()

        mock_concluir.assert_called_once_with()
        mock_pausar.assert_called_once_with()

    # ========================================================
    # TESTES GERAIS — MENU DE HOMOLOGAÇÕES
    # ========================================================

    @patch(
        "builtins.print"
    )
    @patch(
        "builtins.input",
        return_value="0",
    )
    def test_menu_homologacoes_deve_exibir_gestao_instalacao(
        self,
        mock_input,
        mock_print,
    ):
        """
        O menu de Homologações deve apresentar
        corretamente a opção de Gestão da Instalação.
        """

        homologacoes_interface.menu_homologacoes()

        mock_print.assert_any_call(
            "4 - Gerenciar Instalação"
        )

    @patch(
        "builtins.print"
    )
    @patch(
        "builtins.input",
        return_value="0",
    )
    def test_menu_homologacoes_deve_exibir_gestao_vistoria(
        self,
        mock_input,
        mock_print,
    ):
        """
        O menu de Homologações deve apresentar
        corretamente a Gestão da Vistoria.
        """

        homologacoes_interface.menu_homologacoes()

        mock_print.assert_any_call(
            "5 - Gerenciar Vistoria"
        )

    @patch(
        "app.interface.homologacoes_interface."
        "cadastrar_homologacao_interface"
    )
    @patch(
        "app.interface.homologacoes_interface."
        "_pausar"
    )
    @patch(
        "builtins.input",
        side_effect=[
            "1",
            "0",
        ],
    )
    def test_menu_deve_abrir_cadastro(
        self,
        mock_input,
        mock_pausar,
        mock_cadastrar,
    ):
        homologacoes_interface.menu_homologacoes()

        mock_cadastrar.assert_called_once_with()
        mock_pausar.assert_called_once_with()

    @patch(
        "app.interface.homologacoes_interface."
        "listar_homologacoes_interface"
    )
    @patch(
        "app.interface.homologacoes_interface."
        "_pausar"
    )
    @patch(
        "builtins.input",
        side_effect=[
            "2",
            "0",
        ],
    )
    def test_menu_deve_abrir_listagem(
        self,
        mock_input,
        mock_pausar,
        mock_listar,
    ):
        homologacoes_interface.menu_homologacoes()

        mock_listar.assert_called_once_with()

    @patch(
        "app.interface.homologacoes_interface."
        "buscar_homologacao_interface"
    )
    @patch(
        "app.interface.homologacoes_interface."
        "_pausar"
    )
    @patch(
        "builtins.input",
        side_effect=[
            "3",
            "0",
        ],
    )
    def test_menu_deve_abrir_busca(
        self,
        mock_input,
        mock_pausar,
        mock_buscar,
    ):
        homologacoes_interface.menu_homologacoes()

        mock_buscar.assert_called_once_with()

    @patch(
        "app.interface.homologacoes_interface."
        "menu_instalacao"
    )
    @patch(
        "builtins.input",
        side_effect=[
            "4",
            "0",
        ],
    )
    def test_menu_deve_abrir_gestao_instalacao(
        self,
        mock_input,
        mock_menu_instalacao,
    ):
        """
        A opção 4 deve abrir o submenu
        de Gestão da Instalação.
        """

        homologacoes_interface.menu_homologacoes()

        mock_menu_instalacao.assert_called_once_with()

    @patch(
        "app.interface.homologacoes_interface."
        "menu_vistoria"
    )
    @patch(
        "builtins.input",
        side_effect=[
            "5",
            "0",
        ],
    )
    def test_menu_deve_abrir_gestao_vistoria(
        self,
        mock_input,
        mock_menu_vistoria,
    ):
        """
        A opção 5 deve abrir o submenu
        de Gestão da Vistoria.
        """

        homologacoes_interface.menu_homologacoes()

        mock_menu_vistoria.assert_called_once_with()

if __name__ == "__main__":
    unittest.main()