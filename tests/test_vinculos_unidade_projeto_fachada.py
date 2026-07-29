"""
Testes da fachada pública dos vínculos
entre Projetos e Unidades Consumidoras.
"""

import unittest
from unittest.mock import patch

from app import vinculos_unidade_projeto

from app.dominio.status import (
    PapelUnidadeProjeto,
)

from app.dominio.vinculos_unidade_projeto import (
    SituacaoVinculoUnidadeProjeto,
    criar_vinculo_unidade_projeto
    as criar_vinculo_dominio,
)


class TestVinculosUnidadeProjetoFachada(
    unittest.TestCase
):
    """
    Testes da fachada pública dos vínculos
    entre Projetos e Unidades Consumidoras.
    """

    def setUp(self):
        """
        Guarda a lista original de vínculos
        e cria uma lista vazia para cada teste.

        Isso impede que os testes utilizem
        ou modifiquem os dados reais carregados
        do arquivo JSON.
        """

        self.lista_original = (
            vinculos_unidade_projeto
            .vinculos_unidade_projeto
        )

        vinculos_unidade_projeto\
            .vinculos_unidade_projeto = []

    def tearDown(self):
        """
        Restaura a lista original depois
        da execução de cada teste.
        """

        vinculos_unidade_projeto\
            .vinculos_unidade_projeto = (
                self.lista_original
            )

    def test_obter_vinculos_unidade_projeto(
        self,
    ):
        """
        Deve retornar exatamente a lista
        mantida internamente pela fachada.
        """

        resultado = (
            vinculos_unidade_projeto
            .obter_vinculos_unidade_projeto()
        )

        self.assertIs(
            resultado,
            vinculos_unidade_projeto
            .vinculos_unidade_projeto,
        )

    def test_gerar_primeiro_codigo(self):
        """
        Deve gerar o código 1 quando
        ainda não houver vínculos.
        """

        resultado = (
            vinculos_unidade_projeto
            .gerar_proximo_codigo()
        )

        self.assertEqual(
            resultado,
            1,
        )

    @patch(
        "app.vinculos_unidade_projeto."
        "unidades_consumidoras."
        "obter_unidade_consumidora_por_codigo"
    )
    @patch(
        "app.vinculos_unidade_projeto."
        "projetos."
        "buscar_projeto"
    )
    @patch(
        "app.vinculos_unidade_projeto."
        "salvar_vinculos_unidade_projeto"
    )
    def test_vincular_unidade_geradora(
        self,
        mock_salvar,
        mock_buscar_projeto,
        mock_buscar_unidade,
    ):
        """
        Deve validar as entidades, criar,
        adicionar e salvar um vínculo
        de Unidade Geradora.
        """

        mock_buscar_projeto.return_value = (
            object()
        )

        mock_buscar_unidade.return_value = (
            object()
        )

        resultado = (
            vinculos_unidade_projeto
            .vincular_unidade_geradora(
                codigo_projeto=10,
                codigo_unidade_consumidora=20,
                observacoes=(
                    "Geradora principal"
                ),
            )
        )

        mock_buscar_projeto\
            .assert_called_once_with(
                10
            )

        mock_buscar_unidade\
            .assert_called_once_with(
                20
            )

        self.assertEqual(
            resultado.codigo,
            1,
        )

        self.assertEqual(
            resultado.codigo_projeto,
            10,
        )

        self.assertEqual(
            resultado
            .codigo_unidade_consumidora,
            20,
        )

        self.assertEqual(
            resultado.papel,
            PapelUnidadeProjeto.GERADORA,
        )

        self.assertEqual(
            resultado.situacao,
            SituacaoVinculoUnidadeProjeto.ATIVO,
        )

        self.assertEqual(
            resultado.observacoes,
            "Geradora principal",
        )

        self.assertEqual(
            len(
                vinculos_unidade_projeto
                .vinculos_unidade_projeto
            ),
            1,
        )

        mock_salvar.assert_called_once_with(
            vinculos_unidade_projeto
            .vinculos_unidade_projeto
        )

    @patch(
        "app.vinculos_unidade_projeto."
        "unidades_consumidoras."
        "obter_unidade_consumidora_por_codigo"
    )
    @patch(
        "app.vinculos_unidade_projeto."
        "projetos."
        "buscar_projeto"
    )
    @patch(
        "app.vinculos_unidade_projeto."
        "salvar_vinculos_unidade_projeto"
    )
    def test_vincular_unidade_beneficiaria(
        self,
        mock_salvar,
        mock_buscar_projeto,
        mock_buscar_unidade,
    ):
        """
        Deve validar as entidades, criar,
        adicionar e salvar um vínculo
        de Unidade Beneficiária.
        """

        mock_buscar_projeto.return_value = (
            object()
        )

        mock_buscar_unidade.return_value = (
            object()
        )

        resultado = (
            vinculos_unidade_projeto
            .vincular_unidade_beneficiaria(
                codigo_projeto=10,
                codigo_unidade_consumidora=21,
            )
        )

        mock_buscar_projeto\
            .assert_called_once_with(
                10
            )

        mock_buscar_unidade\
            .assert_called_once_with(
                21
            )

        self.assertEqual(
            resultado.codigo,
            1,
        )

        self.assertEqual(
            resultado.codigo_projeto,
            10,
        )

        self.assertEqual(
            resultado
            .codigo_unidade_consumidora,
            21,
        )

        self.assertEqual(
            resultado.papel,
            PapelUnidadeProjeto.BENEFICIARIA,
        )

        self.assertEqual(
            resultado.situacao,
            SituacaoVinculoUnidadeProjeto.ATIVO,
        )

        self.assertEqual(
            len(
                vinculos_unidade_projeto
                .vinculos_unidade_projeto
            ),
            1,
        )

        mock_salvar.assert_called_once_with(
            vinculos_unidade_projeto
            .vinculos_unidade_projeto
        )

    @patch(
        "app.vinculos_unidade_projeto."
        "unidades_consumidoras."
        "obter_unidade_consumidora_por_codigo"
    )
    @patch(
        "app.vinculos_unidade_projeto."
        "projetos."
        "buscar_projeto"
    )
    @patch(
        "app.vinculos_unidade_projeto."
        "salvar_vinculos_unidade_projeto"
    )
    def test_gerar_codigo_sequencial(
        self,
        mock_salvar,
        mock_buscar_projeto,
        mock_buscar_unidade,
    ):
        """
        Deve gerar códigos sequenciais
        para os novos vínculos.
        """

        mock_buscar_projeto.return_value = (
            object()
        )

        mock_buscar_unidade.return_value = (
            object()
        )

        primeiro = (
            vinculos_unidade_projeto
            .vincular_unidade_geradora(
                codigo_projeto=10,
                codigo_unidade_consumidora=20,
            )
        )

        segundo = (
            vinculos_unidade_projeto
            .vincular_unidade_beneficiaria(
                codigo_projeto=10,
                codigo_unidade_consumidora=21,
            )
        )

        self.assertEqual(
            primeiro.codigo,
            1,
        )

        self.assertEqual(
            segundo.codigo,
            2,
        )

        self.assertEqual(
            mock_buscar_projeto.call_count,
            2,
        )

        self.assertEqual(
            mock_buscar_unidade.call_count,
            2,
        )

        self.assertEqual(
            mock_salvar.call_count,
            2,
        )

    @patch(
        "app.vinculos_unidade_projeto."
        "unidades_consumidoras."
        "obter_unidade_consumidora_por_codigo"
    )
    @patch(
        "app.vinculos_unidade_projeto."
        "projetos."
        "buscar_projeto"
    )
    @patch(
        "app.vinculos_unidade_projeto."
        "salvar_vinculos_unidade_projeto"
    )
    def test_inativar_vinculo(
        self,
        mock_salvar,
        mock_buscar_projeto,
        mock_buscar_unidade,
    ):
        """
        Deve inativar e salvar
        um vínculo existente.
        """

        mock_buscar_projeto.return_value = (
            object()
        )

        mock_buscar_unidade.return_value = (
            object()
        )

        vinculo = (
            vinculos_unidade_projeto
            .vincular_unidade_geradora(
                codigo_projeto=10,
                codigo_unidade_consumidora=20,
            )
        )

        mock_salvar.reset_mock()

        resultado = (
            vinculos_unidade_projeto
            .inativar_vinculo(
                vinculo.codigo
            )
        )

        self.assertIs(
            resultado,
            vinculo,
        )

        self.assertEqual(
            resultado.situacao,
            SituacaoVinculoUnidadeProjeto.INATIVO,
        )

        mock_salvar.assert_called_once_with(
            vinculos_unidade_projeto
            .vinculos_unidade_projeto
        )

    @patch(
        "app.vinculos_unidade_projeto."
        "unidades_consumidoras."
        "obter_unidade_consumidora_por_codigo"
    )
    @patch(
        "app.vinculos_unidade_projeto."
        "projetos."
        "buscar_projeto"
    )
    @patch(
        "app.vinculos_unidade_projeto."
        "salvar_vinculos_unidade_projeto"
    )
    def test_ativar_vinculo(
        self,
        mock_salvar,
        mock_buscar_projeto,
        mock_buscar_unidade,
    ):
        """
        Deve ativar e salvar
        um vínculo inativo.
        """

        mock_buscar_projeto.return_value = (
            object()
        )

        mock_buscar_unidade.return_value = (
            object()
        )

        vinculo = (
            vinculos_unidade_projeto
            .vincular_unidade_geradora(
                codigo_projeto=10,
                codigo_unidade_consumidora=20,
            )
        )

        vinculo.inativar()

        mock_salvar.reset_mock()

        resultado = (
            vinculos_unidade_projeto
            .ativar_vinculo(
                vinculo.codigo
            )
        )

        self.assertIs(
            resultado,
            vinculo,
        )

        self.assertEqual(
            resultado.situacao,
            SituacaoVinculoUnidadeProjeto.ATIVO,
        )

        mock_salvar.assert_called_once_with(
            vinculos_unidade_projeto
            .vinculos_unidade_projeto
        )

    @patch(
        "app.vinculos_unidade_projeto."
        "unidades_consumidoras."
        "obter_unidade_consumidora_por_codigo"
    )
    @patch(
        "app.vinculos_unidade_projeto."
        "projetos."
        "buscar_projeto"
    )
    @patch(
        "app.vinculos_unidade_projeto."
        "salvar_vinculos_unidade_projeto"
    )
    def test_alterar_observacoes(
        self,
        mock_salvar,
        mock_buscar_projeto,
        mock_buscar_unidade,
    ):
        """
        Deve alterar as observações
        e salvar o vínculo.
        """

        mock_buscar_projeto.return_value = (
            object()
        )

        mock_buscar_unidade.return_value = (
            object()
        )

        vinculo = (
            vinculos_unidade_projeto
            .vincular_unidade_geradora(
                codigo_projeto=10,
                codigo_unidade_consumidora=20,
            )
        )

        mock_salvar.reset_mock()

        resultado = (
            vinculos_unidade_projeto
            .alterar_observacoes(
                vinculo.codigo,
                "  Observação atualizada.  ",
            )
        )

        self.assertIs(
            resultado,
            vinculo,
        )

        self.assertEqual(
            resultado.observacoes,
            "Observação atualizada.",
        )

        mock_salvar.assert_called_once_with(
            vinculos_unidade_projeto
            .vinculos_unidade_projeto
        )

    @patch(
        "app.vinculos_unidade_projeto."
        "salvar_vinculos_unidade_projeto"
    )
    def test_inativar_vinculo_inexistente(
        self,
        mock_salvar,
    ):
        """
        Deve retornar None e não salvar
        quando o vínculo não existir.
        """

        resultado = (
            vinculos_unidade_projeto
            .inativar_vinculo(
                999
            )
        )

        self.assertIsNone(
            resultado
        )

        mock_salvar.assert_not_called()

    @patch(
        "app.vinculos_unidade_projeto."
        "salvar_vinculos_unidade_projeto"
    )
    def test_ativar_vinculo_inexistente(
        self,
        mock_salvar,
    ):
        """
        Deve retornar None e não salvar
        quando o vínculo não existir.
        """

        resultado = (
            vinculos_unidade_projeto
            .ativar_vinculo(
                999
            )
        )

        self.assertIsNone(
            resultado
        )

        mock_salvar.assert_not_called()

    @patch(
        "app.vinculos_unidade_projeto."
        "salvar_vinculos_unidade_projeto"
    )
    def test_alterar_observacoes_vinculo_inexistente(
        self,
        mock_salvar,
    ):
        """
        Deve retornar None e não salvar
        quando o vínculo não existir.
        """

        resultado = (
            vinculos_unidade_projeto
            .alterar_observacoes(
                999,
                "Nova observação",
            )
        )

        self.assertIsNone(
            resultado
        )

        mock_salvar.assert_not_called()

    @patch(
        "app.vinculos_unidade_projeto."
        "unidades_consumidoras."
        "obter_unidade_consumidora_por_codigo"
    )
    @patch(
        "app.vinculos_unidade_projeto."
        "projetos."
        "buscar_projeto"
    )
    @patch(
        "app.vinculos_unidade_projeto."
        "salvar_vinculos_unidade_projeto"
    )
    def test_nao_permitir_duas_geradoras(
        self,
        mock_salvar,
        mock_buscar_projeto,
        mock_buscar_unidade,
    ):
        """
        Deve impedir duas Unidades
        Geradoras ativas no mesmo Projeto.
        """

        mock_buscar_projeto.return_value = (
            object()
        )

        mock_buscar_unidade.return_value = (
            object()
        )

        vinculos_unidade_projeto\
            .vincular_unidade_geradora(
                codigo_projeto=10,
                codigo_unidade_consumidora=20,
            )

        with self.assertRaisesRegex(
            ValueError,
            "já possui uma Unidade Geradora ativa",
        ):
            (
                vinculos_unidade_projeto
                .vincular_unidade_geradora(
                    codigo_projeto=10,
                    codigo_unidade_consumidora=21,
                )
            )

        self.assertEqual(
            len(
                vinculos_unidade_projeto
                .vinculos_unidade_projeto
            ),
            1,
        )

        mock_salvar.assert_called_once()

    @patch(
        "app.vinculos_unidade_projeto."
        "projetos."
        "buscar_projeto"
    )
    @patch(
        "app.vinculos_unidade_projeto."
        "salvar_vinculos_unidade_projeto"
    )
    def test_nao_criar_vinculo_com_projeto_inexistente(
        self,
        mock_salvar,
        mock_buscar_projeto,
    ):
        """
        Não deve criar vínculo quando
        o Projeto informado não existir.
        """

        mock_buscar_projeto.return_value = None

        with self.assertRaisesRegex(
            ValueError,
            "Projeto informado não existe",
        ):
            (
                vinculos_unidade_projeto
                .vincular_unidade_geradora(
                    codigo_projeto=999,
                    codigo_unidade_consumidora=20,
                )
            )

        self.assertEqual(
            vinculos_unidade_projeto
            .vinculos_unidade_projeto,
            [],
        )

        mock_buscar_projeto\
            .assert_called_once_with(
                999
            )

        mock_salvar.assert_not_called()

    @patch(
        "app.vinculos_unidade_projeto."
        "unidades_consumidoras."
        "obter_unidade_consumidora_por_codigo"
    )
    @patch(
        "app.vinculos_unidade_projeto."
        "projetos."
        "buscar_projeto"
    )
    @patch(
        "app.vinculos_unidade_projeto."
        "salvar_vinculos_unidade_projeto"
    )
    def test_nao_criar_vinculo_com_unidade_inexistente(
        self,
        mock_salvar,
        mock_buscar_projeto,
        mock_buscar_unidade,
    ):
        """
        Não deve criar vínculo quando
        a Unidade Consumidora não existir.
        """

        mock_buscar_projeto.return_value = (
            object()
        )

        mock_buscar_unidade.return_value = None

        with self.assertRaisesRegex(
            ValueError,
            "Unidade Consumidora informada "
            "não existe",
        ):
            (
                vinculos_unidade_projeto
                .vincular_unidade_geradora(
                    codigo_projeto=10,
                    codigo_unidade_consumidora=999,
                )
            )

        self.assertEqual(
            vinculos_unidade_projeto
            .vinculos_unidade_projeto,
            [],
        )

        mock_buscar_projeto\
            .assert_called_once_with(
                10
            )

        mock_buscar_unidade\
            .assert_called_once_with(
                999
            )

        mock_salvar.assert_not_called()

    @patch(
        "app.vinculos_unidade_projeto."
        "salvar_vinculos_unidade_projeto"
    )
    def test_nao_reativar_segunda_geradora(
        self,
        mock_salvar,
    ):
        """
        Não deve reativar uma Geradora
        quando o Projeto já possuir
        outra Geradora ativa.
        """

        primeira_geradora = (
            criar_vinculo_dominio(
                codigo=1,
                codigo_projeto=10,
                codigo_unidade_consumidora=20,
                papel=(
                    PapelUnidadeProjeto.GERADORA
                ),
                vinculos_existentes=[],
            )
        )

        primeira_geradora.inativar()

        segunda_geradora = (
            criar_vinculo_dominio(
                codigo=2,
                codigo_projeto=10,
                codigo_unidade_consumidora=21,
                papel=(
                    PapelUnidadeProjeto.GERADORA
                ),
                vinculos_existentes=[],
            )
        )

        vinculos_unidade_projeto\
            .vinculos_unidade_projeto.extend(
                [
                    primeira_geradora,
                    segunda_geradora,
                ]
            )

        with self.assertRaisesRegex(
            ValueError,
            "já possui uma Unidade Geradora ativa",
        ):
            (
                vinculos_unidade_projeto
                .ativar_vinculo(
                    primeira_geradora.codigo
                )
            )

        self.assertFalse(
            primeira_geradora.esta_ativo()
        )

        mock_salvar.assert_not_called()


if __name__ == "__main__":
    unittest.main()