import unittest

from unittest.mock import patch

from app import painel_gerencial

class TestPainelGerencialFachada(
    unittest.TestCase
):
    """
    Testes da fachada
    do Painel Gerencial.
    """

    @patch(
        "app.painel_gerencial."
        "gerar_indicadores_painel_gerencial"
    )
    @patch(
        "app.painel_gerencial."
        "carregar_concessionarias"
    )
    @patch(
        "app.painel_gerencial."
        "carregar_empresas"
    )
    @patch(
        "app.painel_gerencial."
        "carregar_homologacoes"
    )
    @patch(
        "app.painel_gerencial."
        "carregar_projetos"
    )
    def test_deve_carregar_dados_e_delegar_ao_dominio(
        self,
        mock_projetos,
        mock_homologacoes,
        mock_empresas,
        mock_concessionarias,
        mock_gerar,
    ):
        projetos = [
            {
                "codigo": 1,
                "codigo_empresa": 10,
            }
        ]

        homologacoes = [
            {
                "codigo": 1,
                "codigo_empresa": 10,
            }
        ]

        mock_projetos.return_value = projetos
        mock_homologacoes.return_value = (
            homologacoes
        )
        mock_empresas.return_value = []
        mock_concessionarias.return_value = []

        mock_gerar.return_value = {
            "visao_geral": {},
            "desempenho": {},
            "distribuicao": {
                "projetos_por_empresa": {},
                "projetos_por_concessionaria": {},
            },
            "operacoes_campo": {},
        }

        painel_gerencial.obter_painel_gerencial()

        mock_gerar.assert_called_once_with(
            projetos=projetos,
            homologacoes=homologacoes,
        )

    @patch(
        "app.painel_gerencial."
        "gerar_indicadores_painel_gerencial"
    )
    @patch(
        "app.painel_gerencial."
        "carregar_concessionarias",
        return_value=[],
    )
    @patch(
        "app.painel_gerencial."
        "carregar_empresas",
        return_value=[],
    )
    @patch(
        "app.painel_gerencial."
        "carregar_homologacoes"
    )
    @patch(
        "app.painel_gerencial."
        "carregar_projetos"
    )
    def test_deve_filtrar_dados_por_empresa(
        self,
        mock_projetos,
        mock_homologacoes,
        mock_empresas,
        mock_concessionarias,
        mock_gerar,
    ):
        mock_projetos.return_value = [
            {
                "codigo": 1,
                "codigo_empresa": 10,
            },
            {
                "codigo": 2,
                "codigo_empresa": 20,
            },
        ]

        mock_homologacoes.return_value = [
            {
                "codigo": 1,
                "codigo_empresa": 10,
            },
            {
                "codigo": 2,
                "codigo_empresa": 20,
            },
        ]

        mock_gerar.return_value = {
            "visao_geral": {},
            "desempenho": {},
            "distribuicao": {
                "projetos_por_empresa": {},
                "projetos_por_concessionaria": {},
            },
            "operacoes_campo": {},
        }

        painel_gerencial.obter_painel_gerencial(
            codigo_empresa=10
        )

        mock_gerar.assert_called_once_with(
            projetos=[
                {
                    "codigo": 1,
                    "codigo_empresa": 10,
                }
            ],
            homologacoes=[
                {
                    "codigo": 1,
                    "codigo_empresa": 10,
                }
            ],
        )

    @patch(
        "app.painel_gerencial."
        "gerar_indicadores_painel_gerencial"
    )
    @patch(
        "app.painel_gerencial."
        "carregar_concessionarias",
        return_value=[],
    )
    @patch(
        "app.painel_gerencial."
        "carregar_empresas"
    )
    @patch(
        "app.painel_gerencial."
        "carregar_homologacoes",
        return_value=[],
    )
    @patch(
        "app.painel_gerencial."
        "carregar_projetos",
        return_value=[],
    )
    def test_deve_enriquecer_distribuicao_por_empresa(
        self,
        mock_projetos,
        mock_homologacoes,
        mock_empresas,
        mock_concessionarias,
        mock_gerar,
    ):
        mock_empresas.return_value = [
            {
                "codigo": 10,
                "nome": "Solar Alfa",
            },
            {
                "codigo": 20,
                "nome": "Energia Beta",
            },
        ]

        mock_gerar.return_value = {
            "visao_geral": {},
            "desempenho": {},
            "distribuicao": {
                "projetos_por_empresa": {
                    10: 3,
                    20: 1,
                },
                "projetos_por_concessionaria": {},
            },
            "operacoes_campo": {},
        }

        resultado = (
            painel_gerencial
            .obter_painel_gerencial()
        )

        self.assertEqual(
            resultado["distribuicao"][
                "projetos_por_empresa"
            ],
            [
                {
                    "codigo": 10,
                    "nome": "Solar Alfa",
                    "quantidade": 3,
                },
                {
                    "codigo": 20,
                    "nome": "Energia Beta",
                    "quantidade": 1,
                },
            ],
        )

    @patch(
        "app.painel_gerencial."
        "gerar_indicadores_painel_gerencial"
    )
    @patch(
        "app.painel_gerencial."
        "carregar_concessionarias"
    )
    @patch(
        "app.painel_gerencial."
        "carregar_empresas",
        return_value=[],
    )
    @patch(
        "app.painel_gerencial."
        "carregar_homologacoes",
        return_value=[],
    )
    @patch(
        "app.painel_gerencial."
        "carregar_projetos",
        return_value=[],
    )
    def test_deve_enriquecer_e_ordenar_concessionarias(
        self,
        mock_projetos,
        mock_homologacoes,
        mock_empresas,
        mock_concessionarias,
        mock_gerar,
    ):
        mock_concessionarias.return_value = [
            {
                "codigo": 100,
                "nome": "Concessionária A",
            },
            {
                "codigo": 200,
                "nome": "Concessionária B",
            },
        ]

        mock_gerar.return_value = {
            "visao_geral": {},
            "desempenho": {},
            "distribuicao": {
                "projetos_por_empresa": {},
                "projetos_por_concessionaria": {
                    100: 2,
                    200: 5,
                },
            },
            "operacoes_campo": {},
        }

        resultado = (
            painel_gerencial
            .obter_painel_gerencial()
        )

        self.assertEqual(
            resultado["distribuicao"][
                "projetos_por_concessionaria"
            ][0],
            {
                "codigo": 200,
                "nome": "Concessionária B",
                "quantidade": 5,
            },
        )

    def test_busca_nome_empresa_deve_ter_fallback(
        self,
    ):
        resultado = (
            painel_gerencial
            ._buscar_nome_empresa(
                empresas=[],
                codigo_empresa=99,
            )
        )

        self.assertEqual(
            resultado,
            "Empresa 99",
        )


