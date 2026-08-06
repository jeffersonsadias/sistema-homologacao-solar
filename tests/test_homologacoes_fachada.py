"""
Testes da fachada de Homologações.

Os testes verificam a coordenação entre:

- fachadas externas;
- domínio;
- persistência;
- coleção mantida em memória.

O arquivo real homologacoes.json não será alterado.
"""

import unittest
from unittest.mock import patch

from app import homologacoes


class TestHomologacoesFachada(unittest.TestCase):
    """
    Testes das operações públicas da fachada.
    """

    def setUp(self):
        """
        Substitui temporariamente a coleção real.
        """

        self.homologacoes_originais = (
            homologacoes.homologacoes
        )

        homologacoes.homologacoes = []

    def tearDown(self):
        """
        Restaura a coleção original.
        """

        homologacoes.homologacoes = (
            self.homologacoes_originais
        )

    # ========================================================
    # CONSULTAS
    # ========================================================

    def test_buscar_homologacao_existente(self):
        homologacao = {
            "codigo": 1,
            "codigo_empresa": 10,
        }

        homologacoes.homologacoes = [
            homologacao
        ]

        resultado = homologacoes.buscar_homologacao(
            codigo_homologacao=1,
        )

        self.assertIs(
            resultado,
            homologacao,
        )

    def test_buscar_homologacao_inexistente(self):
        resultado = homologacoes.buscar_homologacao(
            codigo_homologacao=999,
        )

        self.assertIsNone(
            resultado
        )

    def test_busca_deve_respeitar_empresa(self):
        homologacao = {
            "codigo": 1,
            "codigo_empresa": 10,
        }

        homologacoes.homologacoes = [
            homologacao
        ]

        resultado = homologacoes.buscar_homologacao(
            codigo_homologacao=1,
            codigo_empresa=20,
        )

        self.assertIsNone(
            resultado
        )

    def test_obter_homologacao_existente(self):
        homologacao = {
            "codigo": 1,
            "codigo_empresa": 10,
        }

        homologacoes.homologacoes = [
            homologacao
        ]

        resultado = homologacoes.obter_homologacao(
            codigo_homologacao=1,
            codigo_empresa=10,
        )

        self.assertIs(
            resultado,
            homologacao,
        )

    def test_obter_homologacao_inexistente(self):
        with self.assertRaisesRegex(
            ValueError,
            "não encontrada",
        ):
            homologacoes.obter_homologacao(
                codigo_homologacao=999,
            )

    def test_listar_homologacoes_retorna_nova_lista(self):
        homologacao = {
            "codigo": 1,
            "codigo_empresa": 10,
        }

        homologacoes.homologacoes = [
            homologacao
        ]

        resultado = homologacoes.listar_homologacoes()

        self.assertEqual(
            resultado,
            homologacoes.homologacoes,
        )

        self.assertIsNot(
            resultado,
            homologacoes.homologacoes,
        )

    def test_listar_homologacoes_da_empresa(self):
        homologacoes.homologacoes = [
            {
                "codigo": 1,
                "codigo_empresa": 10,
            },
            {
                "codigo": 2,
                "codigo_empresa": 20,
            },
        ]

        resultado = homologacoes.listar_homologacoes(
            codigo_empresa=10,
        )

        self.assertEqual(
            len(resultado),
            1,
        )

        self.assertEqual(
            resultado[0]["codigo"],
            1,
        )

    @patch(
        "app.homologacoes."
        "buscar_por_concessionaria_no_dominio"
    )
    def test_listar_homologacoes_por_concessionaria(
        self,
        mock_buscar,
    ):
        """
        Deve encaminhar ao domínio a busca por
        Concessionária e Empresa.
        """

        homologacoes_encontradas = [
            {
                "codigo": 1,
                "codigo_empresa": 10,
                "codigo_concessionaria": 30,
            }
        ]

        mock_buscar.return_value = (
            homologacoes_encontradas
        )

        resultado = (
            homologacoes
            .listar_homologacoes_por_concessionaria(
                codigo_concessionaria=30,
                codigo_empresa=10,
            )
        )

        mock_buscar.assert_called_once_with(
            homologacoes=homologacoes.homologacoes,
            codigo_concessionaria=30,
            codigo_empresa=10,
        )

        self.assertEqual(
            resultado,
            homologacoes_encontradas,
        )

    @patch(
        "app.homologacoes."
        "buscar_por_status_no_dominio"
    )
    def test_listar_homologacoes_por_status(
        self,
        mock_buscar,
    ):
        """
        Deve encaminhar ao domínio a busca
        por status e Empresa.
        """

        homologacoes_encontradas = [
            {
                "codigo": 1,
                "codigo_empresa": 10,
                "status": "EM_ANALISE",
            }
        ]

        mock_buscar.return_value = (
            homologacoes_encontradas
        )

        resultado = (
            homologacoes
            .listar_homologacoes_por_status(
                status="EM_ANALISE",
                codigo_empresa=10,
            )
        )

        mock_buscar.assert_called_once_with(
            homologacoes=homologacoes.homologacoes,
            status="EM_ANALISE",
            codigo_empresa=10,
        )

        self.assertEqual(
            resultado,
            homologacoes_encontradas,
        )

    @patch(
        "app.homologacoes."
        "buscar_ativa_por_projeto_no_dominio"
    )
    def test_buscar_homologacao_por_projeto(
        self,
        mock_buscar,
    ):
        homologacao_esperada = {
            "codigo": 1,
        }

        mock_buscar.return_value = (
            homologacao_esperada
        )

        resultado = (
            homologacoes
            .buscar_homologacao_por_projeto(
                codigo_projeto=5,
                codigo_empresa=10,
            )
        )

        mock_buscar.assert_called_once_with(
            homologacoes=homologacoes.homologacoes,
            codigo_projeto=5,
            codigo_empresa=10,
        )

        self.assertEqual(
            resultado,
            homologacao_esperada,
        )

    def test_quantidade_homologacoes(self):
        """
        Deve retornar a quantidade total de Homologações.
        """

        homologacoes.homologacoes = [
            {
                "codigo": 1,
                "codigo_empresa": 10,
            },
            {
                "codigo": 2,
                "codigo_empresa": 20,
            },
        ]

        resultado = homologacoes.quantidade_homologacoes()

        self.assertEqual(
            resultado,
            2,
        )

    def test_quantidade_homologacoes_da_empresa(self):
        """
        Deve contar somente as Homologações
        pertencentes à Empresa informada.
        """

        homologacoes.homologacoes = [
            {
                "codigo": 1,
                "codigo_empresa": 10,
            },
            {
                "codigo": 2,
                "codigo_empresa": 10,
            },
            {
                "codigo": 3,
                "codigo_empresa": 20,
            },
        ]

        resultado = homologacoes.quantidade_homologacoes(
            codigo_empresa=10,
        )

        self.assertEqual(
            resultado,
            2,
        )

    @patch(
        "app.homologacoes."
        "quantidade_homologacoes_por_status"
    )
    def test_quantidade_homologacoes_aguardando_documentacao(
        self,
        mock_quantidade,
    ):
        """
        Deve delegar ao domínio a contagem de Homologações
        aguardando documentação.
        """

        mock_quantidade.return_value = 3

        resultado = (
            homologacoes
            .quantidade_homologacoes_aguardando_documentacao()
        )

        mock_quantidade.assert_called_once_with(
            homologacoes=homologacoes.homologacoes,
            status=(
                homologacoes
                .StatusHomologacao
                .AGUARDANDO_DOCUMENTACAO
            ),
        )

        self.assertEqual(
            resultado,
            3,
        )

    @patch(
        "app.homologacoes."
        "quantidade_homologacoes_com_exigencia_aberta"
    )
    def test_quantidade_homologacoes_com_exigencias_abertas(
        self,
        mock_quantidade,
    ):
        mock_quantidade.return_value = 2

        resultado = (
            homologacoes
            .quantidade_homologacoes_com_exigencias_abertas()
        )

        mock_quantidade.assert_called_once_with(
            homologacoes.homologacoes
        )

        self.assertEqual(
            resultado,
            2,
        )

    @patch(
        "app.homologacoes."
        "quantidade_homologacoes_aguardando_envio"
    )
    def test_quantidade_homologacoes_pendentes_de_envio(
        self,
        mock_quantidade,
    ):
        mock_quantidade.return_value = 4

        resultado = (
            homologacoes
            .quantidade_homologacoes_pendentes_de_envio()
        )

        mock_quantidade.assert_called_once_with(
            homologacoes.homologacoes
        )

        self.assertEqual(
            resultado,
            4,
        )

    @patch(
        "app.homologacoes."
        "quantidade_homologacoes_aguardando_resposta"
    )
    def test_quantidade_homologacoes_pendentes_de_resposta(
        self,
        mock_quantidade,
    ):
        mock_quantidade.return_value = 5

        resultado = (
            homologacoes
            .quantidade_homologacoes_pendentes_de_resposta()
        )

        mock_quantidade.assert_called_once_with(
            homologacoes.homologacoes
        )

        self.assertEqual(
            resultado,
            5,
        )

    @patch(
        "app.homologacoes."
        "quantidade_homologacoes_sem_responsavel"
    )
    def test_quantidade_homologacoes_sem_responsavel_atual(
        self,
        mock_quantidade,
    ):
        mock_quantidade.return_value = 1

        resultado = (
            homologacoes
            .quantidade_homologacoes_sem_responsavel_atual()
        )

        mock_quantidade.assert_called_once_with(
            homologacoes.homologacoes
        )

        self.assertEqual(
            resultado,
            1,
        )

    @patch(
        "app.homologacoes."
        "quantidade_total_pendencias_homologacao"
    )
    def test_quantidade_total_pendencias(
        self,
        mock_quantidade,
    ):
        mock_quantidade.return_value = 15

        resultado = (
            homologacoes
            .quantidade_total_pendencias()
        )

        mock_quantidade.assert_called_once_with(
            homologacoes.homologacoes
        )

        self.assertEqual(
            resultado,
            15,
        )

    # ========================================================
    # CADASTRO
    # ========================================================

    @patch("app.homologacoes._salvar_alteracoes")
    @patch(
        "app.homologacoes."
        "_validar_dependencias_da_homologacao"
    )
    def test_criar_homologacao(
        self,
        mock_validar_dependencias,
        mock_salvar,
    ):
        resultado = homologacoes.criar_homologacao(
            codigo_empresa=10,
            codigo_projeto=20,
            codigo_concessionaria=30,
            data_abertura="2026-08-03",
            responsavel_abertura="Ana Lima",
        )

        mock_validar_dependencias.assert_called_once_with(
            codigo_empresa=10,
            codigo_projeto=20,
            codigo_concessionaria=30,
        )

        self.assertEqual(
            resultado["codigo"],
            1,
        )

        self.assertEqual(
            resultado["codigo_empresa"],
            10,
        )

        self.assertEqual(
            resultado["codigo_projeto"],
            20,
        )

        self.assertEqual(
            len(homologacoes.homologacoes),
            1,
        )

        mock_salvar.assert_called_once_with()

    @patch("app.homologacoes._salvar_alteracoes")
    @patch(
        "app.homologacoes."
        "_validar_dependencias_da_homologacao"
    )
    def test_criar_homologacao_gera_codigo_sequencial(
        self,
        mock_validar_dependencias,
        mock_salvar,
    ):
        homologacoes.homologacoes = [
            {
                "codigo": 5,
                "codigo_empresa": 10,
                "codigo_projeto": 1,
                "status": "CONCLUIDA",
            }
        ]

        resultado = homologacoes.criar_homologacao(
            codigo_empresa=10,
            codigo_projeto=2,
            codigo_concessionaria=30,
            data_abertura="2026-08-03",
            responsavel_abertura="Ana Lima",
        )

        self.assertEqual(
            resultado["codigo"],
            6,
        )

        mock_salvar.assert_called_once_with()

    @patch("app.homologacoes._salvar_alteracoes")
    @patch(
        "app.homologacoes."
        "_validar_dependencias_da_homologacao"
    )
    def test_nao_deve_criar_segunda_homologacao_ativa(
        self,
        mock_validar_dependencias,
        mock_salvar,
    ):
        homologacoes.homologacoes = [
            {
                "codigo": 1,
                "codigo_empresa": 10,
                "codigo_projeto": 20,
                "status": "EM_PREPARACAO",
            }
        ]

        with self.assertRaisesRegex(
            ValueError,
            "já possui uma Homologação ativa",
        ):
            homologacoes.criar_homologacao(
                codigo_empresa=10,
                codigo_projeto=20,
                codigo_concessionaria=30,
                data_abertura="2026-08-03",
                responsavel_abertura="Ana Lima",
            )

        self.assertEqual(
            len(homologacoes.homologacoes),
            1,
        )

        mock_salvar.assert_not_called()

    @patch("app.homologacoes.salvar_homologacoes")
    def test_salvar_alteracoes_utiliza_repositorio(
        self,
        mock_salvar,
    ):
        homologacoes.homologacoes = [
            {
                "codigo": 1,
            }
        ]

        homologacoes._salvar_alteracoes()

        mock_salvar.assert_called_once_with(
            homologacoes.homologacoes
        )

    # ========================================================
    # DEPENDÊNCIAS EXTERNAS
    # ========================================================

    @patch(
        "app.homologacoes."
        "concessionarias.obter_concessionaria"
    )
    @patch(
        "app.homologacoes.projetos.buscar_projeto"
    )
    @patch(
        "app.homologacoes.empresas.empresa_esta_ativa"
    )
    @patch(
        "app.homologacoes.empresas.obter_empresa"
    )
    def test_validar_dependencias(
        self,
        mock_obter_empresa,
        mock_empresa_ativa,
        mock_buscar_projeto,
        mock_obter_concessionaria,
    ):
        mock_empresa_ativa.return_value = True

        mock_buscar_projeto.return_value = {
            "codigo": 20,
        }

        homologacoes._validar_dependencias_da_homologacao(
            codigo_empresa=10,
            codigo_projeto=20,
            codigo_concessionaria=30,
        )

        mock_obter_empresa.assert_called_once_with(
            10
        )

        mock_empresa_ativa.assert_called_once_with(
            10
        )

        mock_buscar_projeto.assert_called_once_with(
            20
        )

        mock_obter_concessionaria.assert_called_once_with(
            30
        )

    @patch(
        "app.homologacoes.empresas.empresa_esta_ativa"
    )
    @patch(
        "app.homologacoes.empresas.obter_empresa"
    )
    def test_empresa_inativa_deve_ser_rejeitada(
        self,
        mock_obter_empresa,
        mock_empresa_ativa,
    ):
        mock_empresa_ativa.return_value = False

        with self.assertRaisesRegex(
            ValueError,
            "Empresa que não esteja ativa",
        ):
            homologacoes._validar_dependencias_da_homologacao(
                codigo_empresa=10,
                codigo_projeto=20,
                codigo_concessionaria=30,
            )

    @patch(
        "app.homologacoes.projetos.buscar_projeto"
    )
    @patch(
        "app.homologacoes.empresas.empresa_esta_ativa"
    )
    @patch(
        "app.homologacoes.empresas.obter_empresa"
    )
    def test_projeto_inexistente_deve_ser_rejeitado(
        self,
        mock_obter_empresa,
        mock_empresa_ativa,
        mock_buscar_projeto,
    ):
        mock_empresa_ativa.return_value = True
        mock_buscar_projeto.return_value = None

        with self.assertRaisesRegex(
            ValueError,
            "Projeto com código 20 não encontrado",
        ):
            homologacoes._validar_dependencias_da_homologacao(
                codigo_empresa=10,
                codigo_projeto=20,
                codigo_concessionaria=30,
            )


if __name__ == "__main__":
    unittest.main()