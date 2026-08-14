import unittest

from app.dominio.areas_atendimento import (
    AreaAtendimento,
    ModalidadeAreaAtendimento,
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


if __name__ == "__main__":
    unittest.main()