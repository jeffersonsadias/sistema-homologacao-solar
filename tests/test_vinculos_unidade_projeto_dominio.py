import unittest

from app.dominio.status import (
    PapelUnidadeProjeto,
)

from app.dominio.vinculos_unidade_projeto import (
    SituacaoVinculoUnidadeProjeto,
    buscar_vinculo_da_unidade_no_projeto,
    buscar_vinculo_por_codigo,
    criar_vinculo_unidade_projeto,
    listar_unidades_beneficiarias_do_projeto,
    listar_vinculos_do_projeto,
    obter_unidade_geradora_do_projeto,
)


class TestVinculosUnidadeProjetoDominio(
    unittest.TestCase
):
    """
    Testes das regras de domínio dos vínculos
    entre Projetos e Unidades Consumidoras.
    """

    def setUp(self):
        """
        Cria uma lista vazia antes
        da execução de cada teste.
        """

        self.vinculos = []

    def test_criar_vinculo_geradora(self):
        """
        Deve criar um vínculo ativo
        com papel de Geradora.
        """

        vinculo = criar_vinculo_unidade_projeto(
            codigo=1,
            codigo_projeto=10,
            codigo_unidade_consumidora=20,
            papel=PapelUnidadeProjeto.GERADORA,
            vinculos_existentes=self.vinculos,
        )

        self.assertEqual(
            vinculo.codigo,
            1,
        )

        self.assertEqual(
            vinculo.codigo_projeto,
            10,
        )

        self.assertEqual(
            vinculo.codigo_unidade_consumidora,
            20,
        )

        self.assertEqual(
            vinculo.papel,
            PapelUnidadeProjeto.GERADORA,
        )

        self.assertEqual(
            vinculo.situacao,
            SituacaoVinculoUnidadeProjeto.ATIVO,
        )

    def test_nao_permitir_duas_geradoras_ativas(self):
        """
        Um Projeto não deve possuir duas
        Unidades Geradoras ativas.
        """

        primeira_geradora = (
            criar_vinculo_unidade_projeto(
                codigo=1,
                codigo_projeto=10,
                codigo_unidade_consumidora=20,
                papel=(
                    PapelUnidadeProjeto.GERADORA
                ),
                vinculos_existentes=self.vinculos,
            )
        )

        self.vinculos.append(
            primeira_geradora
        )

        with self.assertRaises(
            ValueError
        ):
            criar_vinculo_unidade_projeto(
                codigo=2,
                codigo_projeto=10,
                codigo_unidade_consumidora=21,
                papel=(
                    PapelUnidadeProjeto.GERADORA
                ),
                vinculos_existentes=self.vinculos,
            )

    def test_permitir_varias_beneficiarias(self):
        """
        Um Projeto pode possuir várias
        Unidades Beneficiárias.
        """

        primeira = (
            criar_vinculo_unidade_projeto(
                codigo=1,
                codigo_projeto=10,
                codigo_unidade_consumidora=20,
                papel=(
                    PapelUnidadeProjeto.BENEFICIARIA
                ),
                vinculos_existentes=self.vinculos,
            )
        )

        self.vinculos.append(
            primeira
        )

        segunda = (
            criar_vinculo_unidade_projeto(
                codigo=2,
                codigo_projeto=10,
                codigo_unidade_consumidora=21,
                papel=(
                    PapelUnidadeProjeto.BENEFICIARIA
                ),
                vinculos_existentes=self.vinculos,
            )
        )

        self.vinculos.append(
            segunda
        )

        beneficiarias = (
            listar_unidades_beneficiarias_do_projeto(
                10,
                self.vinculos,
            )
        )

        self.assertEqual(
            len(beneficiarias),
            2,
        )

    def test_nao_permitir_unidade_duplicada(self):
        """
        Uma mesma Unidade não pode possuir
        dois vínculos ativos no mesmo Projeto.
        """

        vinculo = criar_vinculo_unidade_projeto(
            codigo=1,
            codigo_projeto=10,
            codigo_unidade_consumidora=20,
            papel=PapelUnidadeProjeto.BENEFICIARIA,
            vinculos_existentes=self.vinculos,
        )

        self.vinculos.append(
            vinculo
        )

        with self.assertRaises(
            ValueError
        ):
            criar_vinculo_unidade_projeto(
                codigo=2,
                codigo_projeto=10,
                codigo_unidade_consumidora=20,
                papel=(
                    PapelUnidadeProjeto.GERADORA
                ),
                vinculos_existentes=self.vinculos,
            )

    def test_buscar_vinculo_por_codigo(self):
        """
        Deve localizar um vínculo
        pelo seu código interno.
        """

        vinculo = criar_vinculo_unidade_projeto(
            codigo=1,
            codigo_projeto=10,
            codigo_unidade_consumidora=20,
            papel=PapelUnidadeProjeto.GERADORA,
            vinculos_existentes=self.vinculos,
        )

        self.vinculos.append(
            vinculo
        )

        resultado = buscar_vinculo_por_codigo(
            1,
            self.vinculos,
        )

        self.assertIs(
            resultado,
            vinculo,
        )

    def test_buscar_vinculo_inexistente(self):
        """
        Deve retornar None quando
        o vínculo não existir.
        """

        resultado = buscar_vinculo_por_codigo(
            999,
            self.vinculos,
        )

        self.assertIsNone(
            resultado
        )

    def test_listar_vinculos_do_projeto(self):
        """
        Deve retornar somente os vínculos
        pertencentes ao Projeto informado.
        """

        vinculo_projeto_10 = (
            criar_vinculo_unidade_projeto(
                codigo=1,
                codigo_projeto=10,
                codigo_unidade_consumidora=20,
                papel=(
                    PapelUnidadeProjeto.GERADORA
                ),
                vinculos_existentes=self.vinculos,
            )
        )

        self.vinculos.append(
            vinculo_projeto_10
        )

        vinculo_projeto_11 = (
            criar_vinculo_unidade_projeto(
                codigo=2,
                codigo_projeto=11,
                codigo_unidade_consumidora=21,
                papel=(
                    PapelUnidadeProjeto.GERADORA
                ),
                vinculos_existentes=self.vinculos,
            )
        )

        self.vinculos.append(
            vinculo_projeto_11
        )

        resultado = listar_vinculos_do_projeto(
            10,
            self.vinculos,
        )

        self.assertEqual(
            resultado,
            [
                vinculo_projeto_10,
            ],
        )

    def test_obter_geradora_do_projeto(self):
        """
        Deve retornar a Unidade Geradora
        vinculada ao Projeto.
        """

        geradora = criar_vinculo_unidade_projeto(
            codigo=1,
            codigo_projeto=10,
            codigo_unidade_consumidora=20,
            papel=PapelUnidadeProjeto.GERADORA,
            vinculos_existentes=self.vinculos,
        )

        self.vinculos.append(
            geradora
        )

        resultado = (
            obter_unidade_geradora_do_projeto(
                10,
                self.vinculos,
            )
        )

        self.assertIs(
            resultado,
            geradora,
        )

    def test_vinculo_inativo_nao_deve_ser_retornado(self):
        """
        Consultas ativas não devem retornar
        vínculos que foram inativados.
        """

        vinculo = criar_vinculo_unidade_projeto(
            codigo=1,
            codigo_projeto=10,
            codigo_unidade_consumidora=20,
            papel=PapelUnidadeProjeto.GERADORA,
            vinculos_existentes=self.vinculos,
        )

        vinculo.inativar()

        self.vinculos.append(
            vinculo
        )

        resultado = (
            obter_unidade_geradora_do_projeto(
                10,
                self.vinculos,
            )
        )

        self.assertIsNone(
            resultado
        )

    def test_buscar_unidade_no_projeto(self):
        """
        Deve localizar o vínculo da Unidade
        dentro de determinado Projeto.
        """

        vinculo = criar_vinculo_unidade_projeto(
            codigo=1,
            codigo_projeto=10,
            codigo_unidade_consumidora=20,
            papel=PapelUnidadeProjeto.BENEFICIARIA,
            vinculos_existentes=self.vinculos,
        )

        self.vinculos.append(
            vinculo
        )

        resultado = (
            buscar_vinculo_da_unidade_no_projeto(
                codigo_projeto=10,
                codigo_unidade_consumidora=20,
                vinculos=self.vinculos,
            )
        )

        self.assertIs(
            resultado,
            vinculo,
        )


if __name__ == "__main__":
    unittest.main()