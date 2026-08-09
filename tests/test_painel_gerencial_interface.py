import unittest

from unittest.mock import patch

from app.interface import (
    painel_gerencial_interface,
)


class TestPainelGerencialInterface(
    unittest.TestCase
):
    """
    Testes da interface textual
    do Painel Gerencial.
    """

    @patch(
        "app.interface.painel_gerencial_interface."
        "painel_gerencial.obter_painel_gerencial"
    )
    def test_exibir_painel_gerencial(
        self,
        mock_obter,
    ):
        """
        Deve solicitar os indicadores
        à fachada.
        """

        mock_obter.return_value = {
            "visao_geral": {
                "total_projetos": 3,
                "total_homologacoes": 2,
                "homologacoes_em_andamento": 1,
                "homologacoes_concluidas": 1,
                "homologacoes_encerradas_sem_conclusao": 0,
            },
            "desempenho": {
                "taxa_conclusao": 50.0,
                "tempo_medio_conclusao_dias": 30.0,
                "homologacoes_com_exigencias_abertas": 1,
            },
            "distribuicao": {
                "projetos_por_empresa": [],
                "projetos_por_concessionaria": [],
            },
            "operacoes_campo": {
                "instalacoes_aguardando_execucao": 1,
                "vistorias_aguardando_resultado": 0,
                "ligacoes_aguardando_conclusao": 1,
            },
        }

        painel_gerencial_interface.exibir_painel_gerencial()

        mock_obter.assert_called_once_with(
            codigo_empresa=None
        )

    @patch(
        "app.interface.painel_gerencial_interface."
        "painel_gerencial.obter_painel_gerencial"
    )
    def test_exibir_painel_deve_repassar_empresa(
        self,
        mock_obter,
    ):
        mock_obter.return_value = {
            "visao_geral": {
                "total_projetos": 0,
                "total_homologacoes": 0,
                "homologacoes_em_andamento": 0,
                "homologacoes_concluidas": 0,
                "homologacoes_encerradas_sem_conclusao": 0,
            },
            "desempenho": {
                "taxa_conclusao": 0.0,
                "tempo_medio_conclusao_dias": 0.0,
                "homologacoes_com_exigencias_abertas": 0,
            },
            "distribuicao": {
                "projetos_por_empresa": [],
                "projetos_por_concessionaria": [],
            },
            "operacoes_campo": {
                "instalacoes_aguardando_execucao": 0,
                "vistorias_aguardando_resultado": 0,
                "ligacoes_aguardando_conclusao": 0,
            },
        }

        painel_gerencial_interface.exibir_painel_gerencial(
            codigo_empresa=10
        )

        mock_obter.assert_called_once_with(
            codigo_empresa=10
        )

    def test_formatar_percentual(
        self,
    ):
        self.assertEqual(
            painel_gerencial_interface
            ._formatar_percentual(
                57.142857
            ),
            "57,1%",
        )

    def test_formatar_dias(
        self,
    ):
        self.assertEqual(
            painel_gerencial_interface
            ._formatar_dias(
                38.25
            ),
            "38,2 dias",
        )

    @patch(
        "app.interface.painel_gerencial_interface."
        "_pausar"
    )
    @patch(
        "app.interface.painel_gerencial_interface."
        "exibir_painel_gerencial"
    )
    @patch(
        "builtins.input",
        side_effect=[
            "1",
            "0",
        ],
    )
    def test_menu_deve_abrir_visao_geral(
        self,
        mock_input,
        mock_exibir,
        mock_pausar,
    ):
        painel_gerencial_interface.menu_painel_gerencial()

        mock_exibir.assert_called_once_with()
        mock_pausar.assert_called_once_with()

    @patch(
        "app.interface.painel_gerencial_interface."
        "_pausar"
    )
    @patch(
        "app.interface.painel_gerencial_interface."
        "exibir_painel_gerencial"
    )
    @patch(
        "app.interface.painel_gerencial_interface."
        "ler_int",
        return_value=10,
    )
    @patch(
        "builtins.input",
        side_effect=[
            "2",
            "0",
        ],
    )
    def test_menu_deve_filtrar_por_empresa(
        self,
        mock_input,
        mock_ler_int,
        mock_exibir,
        mock_pausar,
    ):
        painel_gerencial_interface.menu_painel_gerencial()

        mock_exibir.assert_called_once_with(
            codigo_empresa=10
        )

        mock_pausar.assert_called_once_with()





