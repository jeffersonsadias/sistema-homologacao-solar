import unittest

from app.dominio.areas_atendimento import (
    AreaAtendimento,
    ModalidadeAreaAtendimento,
    area_atende_localidade,
    criar_area_atendimento,
)

from app.dominio.erros_dominio import (
    DadosObrigatoriosAusentes,
    ValorInvalido,
)


class TestAreasAtendimentoDominio(
    unittest.TestCase
):
    """
    Testes das regras de Área de Atendimento.
    """

    def test_criar_area_por_raio(
        self,
    ):
        area = criar_area_atendimento(
            modalidade="RAIO",
            municipio_base="Caetité",
            uf_base="ba",
            raio_km=150,
        )

        self.assertIsInstance(
            area,
            AreaAtendimento,
        )

        self.assertEqual(
            area.modalidade,
            ModalidadeAreaAtendimento.RAIO,
        )

        self.assertEqual(
            area.municipio_base,
            "Caetité",
        )

        self.assertEqual(
            area.uf_base,
            "BA",
        )

        self.assertEqual(
            area.raio_km,
            150.0,
        )

        self.assertEqual(
            area.municipios,
            (),
        )

    def test_raio_exige_municipio_base(
        self,
    ):
        with self.assertRaises(
            DadosObrigatoriosAusentes
        ):
            criar_area_atendimento(
                modalidade="RAIO",
                municipio_base="",
                uf_base="BA",
                raio_km=100,
            )

    def test_raio_exige_uf(
        self,
    ):
        with self.assertRaises(
            DadosObrigatoriosAusentes
        ):
            criar_area_atendimento(
                modalidade="RAIO",
                municipio_base="Caetité",
                uf_base="",
                raio_km=100,
            )

    def test_uf_deve_possuir_duas_letras(
        self,
    ):
        with self.assertRaises(
            ValorInvalido
        ):
            criar_area_atendimento(
                modalidade="RAIO",
                municipio_base="Caetité",
                uf_base="BAHIA",
                raio_km=100,
            )

    def test_raio_deve_ser_maior_que_zero(
        self,
    ):
        for raio in (
            0,
            -1,
        ):
            with self.subTest(
                raio=raio
            ):
                with self.assertRaises(
                    ValorInvalido
                ):
                    criar_area_atendimento(
                        modalidade="RAIO",
                        municipio_base="Caetité",
                        uf_base="BA",
                        raio_km=raio,
                    )

    def test_raio_deve_ser_numerico(
        self,
    ):
        for raio in (
            "100",
            True,
        ):
            with self.subTest(
                raio=raio
            ):
                with self.assertRaises(
                    ValorInvalido
                ):
                    criar_area_atendimento(
                        modalidade="RAIO",
                        municipio_base="Caetité",
                        uf_base="BA",
                        raio_km=raio,
                    )

    def test_raio_nao_aceita_lista_de_municipios(
        self,
    ):
        with self.assertRaises(
            ValorInvalido
        ):
            criar_area_atendimento(
                modalidade="RAIO",
                municipio_base="Caetité",
                uf_base="BA",
                raio_km=100,
                municipios=[
                    "Guanambi",
                ],
            )

    def test_criar_area_por_municipios(
        self,
    ):
        area = criar_area_atendimento(
            modalidade="MUNICIPIOS",
            municipios=[
                "Caetité",
                "Guanambi",
            ],
        )

        self.assertEqual(
            area.modalidade,
            ModalidadeAreaAtendimento.MUNICIPIOS,
        )

        self.assertEqual(
            area.municipios,
            (
                "Caetité",
                "Guanambi",
            ),
        )

        self.assertIsNone(
            area.municipio_base
        )

        self.assertIsNone(
            area.uf_base
        )

        self.assertIsNone(
            area.raio_km
        )

    def test_municipios_exige_lista(
        self,
    ):
        with self.assertRaises(
            DadosObrigatoriosAusentes
        ):
            criar_area_atendimento(
                modalidade="MUNICIPIOS",
                municipios=[],
            )

    def test_municipios_remove_duplicidades(
        self,
    ):
        area = criar_area_atendimento(
            modalidade="MUNICIPIOS",
            municipios=[
                "Caetité",
                "caetité",
                "Guanambi",
            ],
        )

        self.assertEqual(
            area.municipios,
            (
                "Caetité",
                "Guanambi",
            ),
        )

    def test_municipios_nao_aceita_configuracao_de_raio(
        self,
    ):
        with self.assertRaises(
            ValorInvalido
        ):
            criar_area_atendimento(
                modalidade="MUNICIPIOS",
                municipios=[
                    "Caetité",
                ],
                raio_km=100,
            )

    def test_criar_area_nacional(
        self,
    ):
        area = criar_area_atendimento(
            modalidade="NACIONAL",
        )

        self.assertEqual(
            area.modalidade,
            ModalidadeAreaAtendimento.NACIONAL,
        )

        self.assertIsNone(
            area.municipio_base
        )

        self.assertIsNone(
            area.uf_base
        )

        self.assertIsNone(
            area.raio_km
        )

        self.assertEqual(
            area.municipios,
            (),
        )

    def test_nacional_nao_aceita_configuracao_adicional(
        self,
    ):
        with self.assertRaises(
            ValorInvalido
        ):
            criar_area_atendimento(
                modalidade="NACIONAL",
                municipio_base="Caetité",
            )

    def test_modalidade_invalida(
        self,
    ):
        with self.assertRaises(
            ValorInvalido
        ):
            criar_area_atendimento(
                modalidade="INEXISTENTE",
            )

    def test_area_nacional_atende_localidade(
        self,
    ):
        area = criar_area_atendimento(
            modalidade="NACIONAL",
        )

        resultado = area_atende_localidade(
            area,
            municipio="Caetité",
            uf="BA",
        )

        self.assertTrue(
            resultado
        )

    def test_area_municipios_atende_municipio_configurado(
        self,
    ):
        area = criar_area_atendimento(
            modalidade="MUNICIPIOS",
            municipios=[
                "Caetité",
                "Guanambi",
            ],
        )

        resultado = area_atende_localidade(
            area,
            municipio="Guanambi",
            uf="BA",
        )

        self.assertTrue(
            resultado
        )

    def test_area_municipios_ignora_maiusculas_minusculas(
        self,
    ):
        area = criar_area_atendimento(
            modalidade="MUNICIPIOS",
            municipios=[
                "Caetité",
            ],
        )

        resultado = area_atende_localidade(
            area,
            municipio="CAETITÉ",
            uf="BA",
        )

        self.assertTrue(
            resultado
        )

    def test_area_municipios_rejeita_municipio_nao_configurado(
        self,
    ):
        area = criar_area_atendimento(
            modalidade="MUNICIPIOS",
            municipios=[
                "Caetité",
                "Guanambi",
            ],
        )

        resultado = area_atende_localidade(
            area,
            municipio="Brumado",
            uf="BA",
        )

        self.assertFalse(
            resultado
        )

    def test_area_raio_atende_distancia_dentro_limite(
        self,
    ):
        area = criar_area_atendimento(
            modalidade="RAIO",
            municipio_base="Caetité",
            uf_base="BA",
            raio_km=150,
        )

        resultado = area_atende_localidade(
            area,
            municipio="Guanambi",
            uf="BA",
            distancia_km=100,
        )

        self.assertTrue(
            resultado
        )

    def test_area_raio_atende_distancia_no_limite(
        self,
    ):
        area = criar_area_atendimento(
            modalidade="RAIO",
            municipio_base="Caetité",
            uf_base="BA",
            raio_km=150,
        )

        resultado = area_atende_localidade(
            area,
            municipio="Guanambi",
            uf="BA",
            distancia_km=150,
        )

        self.assertTrue(
            resultado
        )

    def test_area_raio_rejeita_distancia_fora_limite(
        self,
    ):
        area = criar_area_atendimento(
            modalidade="RAIO",
            municipio_base="Caetité",
            uf_base="BA",
            raio_km=150,
        )

        resultado = area_atende_localidade(
            area,
            municipio="Salvador",
            uf="BA",
            distancia_km=600,
        )

        self.assertFalse(
            resultado
        )

    def test_area_raio_exige_distancia(
        self,
    ):
        area = criar_area_atendimento(
            modalidade="RAIO",
            municipio_base="Caetité",
            uf_base="BA",
            raio_km=150,
        )

        with self.assertRaises(
            DadosObrigatoriosAusentes
        ):
            area_atende_localidade(
                area,
                municipio="Guanambi",
                uf="BA",
            )

    def test_distancia_deve_ser_numerica(
        self,
    ):
        area = criar_area_atendimento(
            modalidade="RAIO",
            municipio_base="Caetité",
            uf_base="BA",
            raio_km=150,
        )

        for distancia in (
            "100",
            True,
        ):
            with self.subTest(
                distancia=distancia
            ):
                with self.assertRaises(
                    ValorInvalido
                ):
                    area_atende_localidade(
                        area,
                        municipio="Guanambi",
                        uf="BA",
                        distancia_km=distancia,
                    )

    def test_distancia_nao_pode_ser_negativa(
        self,
    ):
        area = criar_area_atendimento(
            modalidade="RAIO",
            municipio_base="Caetité",
            uf_base="BA",
            raio_km=150,
        )

        with self.assertRaises(
            ValorInvalido
        ):
            area_atende_localidade(
                area,
                municipio="Guanambi",
                uf="BA",
                distancia_km=-1,
            )

    def test_area_raio_rejeita_uf_diferente(
        self,
    ):
        area = criar_area_atendimento(
            modalidade="RAIO",
            municipio_base="Caetité",
            uf_base="BA",
            raio_km=150,
        )

        resultado = area_atende_localidade(
            area,
            municipio="Localidade",
            uf="MG",
            distancia_km=100,
        )

        self.assertFalse(
            resultado
        )




if __name__ == "__main__":
    unittest.main()