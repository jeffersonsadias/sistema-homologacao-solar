import unittest

from app.dominio.status import (
    FaseProcesso,
    PapelUnidadeProjeto,
    SituacaoConcessionaria,
    SituacaoProcesso,
    SituacaoUnidadeConsumidora,
)


class TestStatusSprint2(unittest.TestCase):
    """
    Testes das enumerações utilizadas no domínio da Sprint 2.
    """

    def test_situacao_processo_possui_valores_esperados(self):
        """
        A situação do Processo deve possuir os valores básicos
        definidos para a primeira implementação.
        """

        valores_esperados = {
            "RASCUNHO",
            "EM_PREPARACAO",
            "ATIVO",
            "SUSPENSO",
            "CONCLUIDO",
            "REJEITADO",
            "CANCELADO",
            "ARQUIVADO",
        }

        valores_encontrados = {
            situacao.value
            for situacao in SituacaoProcesso
        }

        self.assertEqual(valores_encontrados, valores_esperados)

    def test_fase_processo_inicia_em_cadastro_inicial(self):
        """
        O primeiro fluxo funcional começa pela fase
        CADASTRO_INICIAL.
        """

        self.assertEqual(
            FaseProcesso.CADASTRO_INICIAL.value,
            "CADASTRO_INICIAL",
        )

    def test_enum_pode_ser_criada_a_partir_de_string(self):
        """
        Os enums devem aceitar a reconstrução a partir do valor
        armazenado no JSON.
        """

        situacao = SituacaoProcesso("ATIVO")

        self.assertEqual(situacao, SituacaoProcesso.ATIVO)

    def test_valor_do_enum_pode_ser_salvo_como_string(self):
        """
        A propriedade value deve fornecer uma string adequada
        para persistência.
        """

        valor = SituacaoConcessionaria.ATIVA.value

        self.assertIsInstance(valor, str)
        self.assertEqual(valor, "ATIVA")

    def test_unidade_possui_situacao_separada_do_papel(self):
        """
        A situação cadastral da Unidade Consumidora e seu papel
        no Projeto devem ser conceitos distintos.
        """

        situacao = SituacaoUnidadeConsumidora.ATIVA
        papel = PapelUnidadeProjeto.GERADORA

        self.assertEqual(situacao.value, "ATIVA")
        self.assertEqual(papel.value, "GERADORA")
        self.assertNotEqual(situacao.value, papel.value)

    def test_papeis_disponiveis_da_unidade_no_projeto(self):
        """
        Nesta primeira implementação, uma Unidade pode atuar como
        Geradora ou Beneficiária em um Projeto.
        """

        papeis_esperados = {
            "GERADORA",
            "BENEFICIARIA",
        }

        papeis_encontrados = {
            papel.value
            for papel in PapelUnidadeProjeto
        }

        self.assertEqual(papeis_encontrados, papeis_esperados)


if __name__ == "__main__":
    unittest.main()