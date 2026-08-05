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
        "builtins.input",
        return_value="",
    )
    @patch(
        "builtins.print"
    )
    @patch(
        "app.interface.painel_operacional_interface."
        "_obter_data_hora_consulta"
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
        mock_data_hora,
        mock_print,
        mock_input,
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
            .exibir_painel_operacional()
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

        mock_input.assert_called_once_with(
            "\nPressione Enter para voltar..."
        )


if __name__ == "__main__":
    unittest.main()