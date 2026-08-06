"""
Testes da interface do Painel Operacional.

As consultas públicas das fachadas e o relógio
são simulados para produzir resultados previsíveis.
"""

import unittest
from datetime import datetime
from unittest.mock import patch

from app.interface import painel_operacional_interface


class TestPainelOperacionalInterface(
    unittest.TestCase
):
    """
    Testes da apresentação dos indicadores gerais.
    """

    @patch(
        "builtins.print"
    )
    @patch(
        "app.interface.painel_operacional_interface."
        "_obter_data_hora_consulta"
    )
    @patch(
    "app.interface.painel_operacional_interface."
    "homologacoes.quantidade_total_pendencias",
    return_value=15,
    )
    @patch(
        "app.interface.painel_operacional_interface."
        "homologacoes."
        "quantidade_homologacoes_sem_responsavel_atual",
        return_value=1,
    )
    @patch(
        "app.interface.painel_operacional_interface."
        "homologacoes."
        "quantidade_homologacoes_pendentes_de_resposta",
        return_value=5,
    )
    @patch(
        "app.interface.painel_operacional_interface."
        "homologacoes."
        "quantidade_homologacoes_pendentes_de_envio",
        return_value=3,
    )
    @patch(
        "app.interface.painel_operacional_interface."
        "homologacoes."
        "quantidade_homologacoes_com_exigencias_abertas",
        return_value=2,
    )
    @patch(
        "app.interface.painel_operacional_interface."
        "homologacoes."
        "quantidade_homologacoes_aguardando_documentacao",
        return_value=4,
    )
    @patch(
        "app.interface.painel_operacional_interface."
        "projetos.quantidade_projetos_com_status",
        side_effect=[
            8,
            4,
            2,
            5,
            7,
        ],
    )
    @patch(
        "app.interface.painel_operacional_interface."
        "homologacoes.quantidade_homologacoes",
        return_value=1,
    )
    @patch(
        "app.interface.painel_operacional_interface."
        "projetos.quantidade_projetos",
        return_value=26,
    )
    @patch(
        "app.interface.painel_operacional_interface."
        "orcamentos.quantidade_orcamentos",
        return_value=3,
    )
    @patch(
        "app.interface.painel_operacional_interface."
        "empresas.quantidade_empresas",
        return_value=2,
    )
    @patch(
        "app.interface.painel_operacional_interface."
        "clientes.quantidade_clientes",
        return_value=4,
    )
    def test_exibir_painel_operacional(
        self,
        mock_quantidade_clientes,
        mock_quantidade_empresas,
        mock_quantidade_orcamentos,
        mock_quantidade_projetos,
        mock_quantidade_homologacoes,
        mock_quantidade_por_status,
        mock_aguardando_documentacao,
        mock_exigencias_abertas,
        mock_pendentes_envio,
        mock_pendentes_resposta,
        mock_sem_responsavel,
        mock_total_pendencias,
        mock_data_hora,
        mock_print,
    ):
        
        """
        Deve exibir os totais gerais, os indicadores
        de Projetos e a data da consulta.
        """

        mock_data_hora.return_value = datetime(
            2026,
            8,
            4,
            21,
            45,
            30,
        )

        (
            painel_operacional_interface
            ._exibir_dashboard_operacional()
        )

        mock_quantidade_clientes.assert_called_once_with()
        mock_quantidade_empresas.assert_called_once_with()
        mock_quantidade_orcamentos.assert_called_once_with()
        mock_quantidade_homologacoes.assert_called_once_with()

        self.assertEqual(
            mock_quantidade_projetos.call_count,
            2,
        )

        self.assertEqual(
            mock_quantidade_por_status.call_args_list,
            [
                unittest.mock.call(
                    "Aguardando documentação"
                ),
                unittest.mock.call(
                    "Em análise pela distribuidora"
                ),
                unittest.mock.call(
                    "Correção solicitada"
                ),
                unittest.mock.call(
                    "Aprovado"
                ),
                unittest.mock.call(
                    "Homologado"
                ),
            ],
        )

        mock_aguardando_documentacao.assert_called_once_with()

        mock_exigencias_abertas.assert_called_once_with()

        mock_pendentes_envio.assert_called_once_with()

        mock_pendentes_resposta.assert_called_once_with()

        mock_sem_responsavel.assert_called_once_with()

        mock_total_pendencias.assert_called_once_with()

        mock_print.assert_any_call(
            "Aguardando documentação.........     8"
        )

        mock_print.assert_any_call(
            "Em análise......................     4"
        )

        mock_print.assert_any_call(
            "Com exigência...................     2"
        )

        mock_print.assert_any_call(
            "Aprovados.......................     5"
        )

        mock_print.assert_any_call(
            "Homologados.....................     7"
        )

        mock_print.assert_any_call(
            "Total geral.....................    26"
        )

        mock_print.assert_any_call(
            "Consulta realizada em: "
            "04/08/2026 21:45:30"
        )

        mock_print.assert_any_call(
            "PENDÊNCIAS DE HOMOLOGAÇÃO"
        )

        mock_print.assert_any_call(
            "Aguardando documentação.........     4"
        )

        mock_print.assert_any_call(
            "Com exigências abertas..........     2"
        )

        mock_print.assert_any_call(
            "Aguardando envio................     3"
        )

        mock_print.assert_any_call(
            "Aguardando resposta.............     5"
        )

        mock_print.assert_any_call(
            "Sem responsável.................     1"
        )

        mock_print.assert_any_call(
            "Total de pendências.............    15"
        )

    @patch(
        "app.interface.painel_operacional_interface."
        "consultas_rapidas_interface."
        "menu_consultas_rapidas"
    )
    @patch(
        "app.interface.painel_operacional_interface."
        "_exibir_dashboard_operacional"
    )
    @patch(
        "builtins.input",
        side_effect=[
            "1",
            "0",
        ],
    )
    def test_painel_deve_abrir_consultas_rapidas(
        self,
        mock_input,
        mock_exibir_dashboard,
        mock_menu_consultas,
    ):
        """
        A opção 1 deve abrir o menu
        de Consultas Rápidas.
        """

        (
            painel_operacional_interface
            .exibir_painel_operacional()
        )

        mock_menu_consultas.assert_called_once_with()

        self.assertEqual(
            mock_exibir_dashboard.call_count,
            2,
        )

    @patch(
        "app.interface.painel_operacional_interface."
        "_exibir_dashboard_operacional"
    )
    @patch(
        "builtins.input",
        return_value="0",
    )
    def test_painel_deve_voltar_ao_menu_principal(
        self,
        mock_input,
        mock_exibir_dashboard,
    ):
        """
        A opção 0 deve encerrar
        o Painel Operacional.
        """

        resultado = (
            painel_operacional_interface
            .exibir_painel_operacional()
        )

        self.assertIsNone(
            resultado
        )

        mock_exibir_dashboard.assert_called_once_with()

    @patch(
        "builtins.print"
    )
    @patch(
        "app.interface.painel_operacional_interface."
        "_exibir_dashboard_operacional"
    )
    @patch(
        "builtins.input",
        side_effect=[
            "99",
            "",
            "0",
        ],
    )
    def test_painel_deve_tratar_opcao_invalida(
        self,
        mock_input,
        mock_exibir_dashboard,
        mock_print,
    ):
        """
        Uma opção inválida deve exibir erro
        e manter o Painel em execução.
        """

        (
            painel_operacional_interface
            .exibir_painel_operacional()
        )

        mock_print.assert_any_call(
            "\nOpção inválida."
        )

        self.assertEqual(
            mock_exibir_dashboard.call_count,
            2,
        )

        self.assertEqual(
            mock_input.call_args_list,
            [
                unittest.mock.call(
                    "\nEscolha uma opção: "
                ),
                unittest.mock.call(
                    "\nPressione Enter para continuar..."
                ),
                unittest.mock.call(
                    "\nEscolha uma opção: "
                ),
            ],
        )

if __name__ == "__main__":
    unittest.main()