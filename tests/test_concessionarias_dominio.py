import unittest
from unittest.mock import patch

from app.dominio.concessionarias import (
    AreaAtuacao,
    Concessionaria,
    buscar_concessionaria_por_codigo,
    buscar_concessionarias_por_nome,
    codigo_concessionaria_existe,
    converter_concessionaria_para_dicionario,
    criar_concessionaria,
    normalizar_cnpj,
    normalizar_situacao_concessionaria,
    reconstruir_concessionaria,
    validar_duplicidade_concessionaria,
)
from app.dominio.erros_dominio import (
    DadosObrigatoriosAusentes,
    RegistroDuplicado,
    ValorInvalido,
)
from app.dominio.status import (
    SituacaoConcessionaria,
)


class TestConcessionariasDominio(
    unittest.TestCase
):
    """
    Testes do domínio e do agregado Concessionária.
    """

    def setUp(self):
        """
        Cria Concessionárias reutilizadas nos testes.
        """

        self.coelba = criar_concessionaria(
            codigo=1,
            nome=(
                "Companhia de Eletricidade "
                "do Estado da Bahia"
            ),
            nome_abreviado="Neoenergia Coelba",
            cnpj="15.139.629/0001-94",
        )

        self.cemig = criar_concessionaria(
            codigo=2,
            nome=(
                "Companhia Energética "
                "de Minas Gerais"
            ),
            nome_abreviado="Cemig",
            cnpj="17.155.730/0001-64",
        )

        self.lista_concessionarias = [
            self.coelba,
            self.cemig,
        ]

    def test_criar_concessionaria(self):
        """
        Deve criar uma Concessionária
        com os dados básicos.
        """

        concessionaria = criar_concessionaria(
            codigo=3,
            nome=(
                "Companhia de Eletricidade "
                "do Estado da Bahia"
            ),
            nome_abreviado="Neoenergia Coelba",
            cnpj="15.139.629/0001-94",
        )

        self.assertIsInstance(
            concessionaria,
            Concessionaria,
        )

        self.assertEqual(
            concessionaria.codigo,
            3,
        )

        self.assertEqual(
            concessionaria.nome,
            (
                "Companhia de Eletricidade "
                "do Estado da Bahia"
            ),
        )

        self.assertEqual(
            concessionaria.nome_abreviado,
            "Neoenergia Coelba",
        )

        self.assertEqual(
            concessionaria.cnpj,
            "15139629000194",
        )

        self.assertEqual(
            concessionaria.situacao,
            SituacaoConcessionaria.ATIVA,
        )

        self.assertEqual(
            concessionaria.areas_atuacao,
            [],
        )

    @patch(
        "app.dominio.concessionarias."
        "obter_data_hora_atual"
    )
    def test_criar_concessionaria_define_datas_iguais(
        self,
        mock_obter_data_hora_atual,
    ):
        """
        Deve usar a mesma data para cadastro
        e atualização na criação.
        """

        mock_obter_data_hora_atual.return_value = (
            "2026-07-27T10:00:00"
        )

        concessionaria = criar_concessionaria(
            codigo=3,
            nome="Concessionária Teste",
            nome_abreviado="Teste",
        )

        self.assertEqual(
            concessionaria.data_cadastro,
            "2026-07-27T10:00:00",
        )

        self.assertEqual(
            concessionaria.data_atualizacao,
            "2026-07-27T10:00:00",
        )

    def test_nome_obrigatorio(self):
        """
        Não deve permitir Concessionária sem nome.
        """

        with self.assertRaises(
            DadosObrigatoriosAusentes
        ):
            criar_concessionaria(
                codigo=1,
                nome="",
                nome_abreviado=(
                    "Concessionária Teste"
                ),
            )

    def test_nome_abreviado_obrigatorio(self):
        """
        Não deve permitir Concessionária
        sem nome abreviado.
        """

        with self.assertRaises(
            DadosObrigatoriosAusentes
        ):
            criar_concessionaria(
                codigo=1,
                nome="Concessionária Teste",
                nome_abreviado="   ",
            )

    def test_codigo_deve_ser_inteiro_positivo(
        self,
    ):
        """
        O código deve ser inteiro
        e maior que zero.
        """

        codigos_invalidos = [
            0,
            -1,
            1.5,
            "1",
            True,
        ]

        for codigo in codigos_invalidos:
            with self.subTest(codigo=codigo):
                with self.assertRaises(
                    ValorInvalido
                ):
                    criar_concessionaria(
                        codigo=codigo,
                        nome=(
                            "Concessionária Teste"
                        ),
                        nome_abreviado="Teste",
                    )

    def test_normalizar_cnpj(self):
        """
        Deve remover a pontuação do CNPJ.
        """

        cnpj = normalizar_cnpj(
            "15.139.629/0001-94"
        )

        self.assertEqual(
            cnpj,
            "15139629000194",
        )

    def test_cnpj_deve_possuir_14_digitos(
        self,
    ):
        """
        Não deve aceitar CNPJ
        com quantidade inválida de dígitos.
        """

        with self.assertRaises(ValorInvalido):
            normalizar_cnpj("123")

    def test_cnpj_pode_ser_omitido(self):
        """
        O CNPJ pode ser omitido
        nesta primeira versão.
        """

        concessionaria = criar_concessionaria(
            codigo=3,
            nome="Concessionária Teste",
            nome_abreviado="Teste",
        )

        self.assertIsNone(
            concessionaria.cnpj
        )

    def test_cnpj_vazio_retorna_none(self):
        """
        Deve interpretar CNPJ vazio
        como não informado.
        """

        self.assertIsNone(
            normalizar_cnpj("")
        )

        self.assertIsNone(
            normalizar_cnpj("   ")
        )

    def test_adicionar_area_atuacao(self):
        """
        Deve adicionar uma Área de Atuação
        à Concessionária.
        """

        area = self.coelba.adicionar_area_atuacao(
            estado="Bahia",
            municipio="Caetité",
        )

        self.assertIsInstance(
            area,
            AreaAtuacao,
        )

        self.assertEqual(
            area.estado,
            "Bahia",
        )

        self.assertEqual(
            area.municipio,
            "Caetité",
        )

        self.assertTrue(area.ativa)

        self.assertEqual(
            len(self.coelba.areas_atuacao),
            1,
        )

    def test_buscar_area_atuacao(self):
        """
        Deve buscar uma Área de Atuação
        por estado e município.
        """

        area_adicionada = (
            self.coelba.adicionar_area_atuacao(
                estado="Bahia",
                municipio="Guanambi",
            )
        )

        resultado = (
            self.coelba.buscar_area_atuacao(
                estado="bahia",
                municipio="GUANAMBI",
            )
        )

        self.assertIs(
            resultado,
            area_adicionada,
        )

    def test_buscar_area_atuacao_inexistente(
        self,
    ):
        """
        Deve retornar None quando a Área
        de Atuação não existir.
        """

        resultado = (
            self.coelba.buscar_area_atuacao(
                estado="Bahia",
                municipio="Caetité",
            )
        )

        self.assertIsNone(resultado)

    def test_nao_permitir_area_atuacao_duplicada(
        self,
    ):
        """
        Não deve permitir a mesma combinação
        de estado e município duas vezes.
        """

        self.coelba.adicionar_area_atuacao(
            estado="Bahia",
            municipio="Caetité",
        )

        with self.assertRaises(
            RegistroDuplicado
        ):
            self.coelba.adicionar_area_atuacao(
                estado="bahia",
                municipio="caetité",
            )

    def test_area_atuacao_exige_estado(self):
        """
        O estado da Área de Atuação
        é obrigatório.
        """

        with self.assertRaises(
            DadosObrigatoriosAusentes
        ):
            self.coelba.adicionar_area_atuacao(
                estado="",
                municipio="Caetité",
            )

    def test_area_atuacao_exige_municipio(
        self,
    ):
        """
        O município da Área de Atuação
        é obrigatório.
        """

        with self.assertRaises(
            DadosObrigatoriosAusentes
        ):
            self.coelba.adicionar_area_atuacao(
                estado="Bahia",
                municipio="",
            )

    def test_inativar_area_atuacao(self):
        """
        Deve inativar uma Área de Atuação.
        """

        self.coelba.adicionar_area_atuacao(
            estado="Bahia",
            municipio="Caetité",
        )

        area_inativa = (
            self.coelba.inativar_area_atuacao(
                estado="Bahia",
                municipio="Caetité",
            )
        )

        self.assertFalse(
            area_inativa.ativa
        )

        self.assertFalse(
            self.coelba.areas_atuacao[0].ativa
        )

    def test_ativar_area_atuacao(self):
        """
        Deve reativar uma Área de Atuação.
        """

        self.coelba.adicionar_area_atuacao(
            estado="Bahia",
            municipio="Caetité",
        )

        self.coelba.inativar_area_atuacao(
            estado="Bahia",
            municipio="Caetité",
        )

        area_ativa = (
            self.coelba.ativar_area_atuacao(
                estado="Bahia",
                municipio="Caetité",
            )
        )

        self.assertTrue(
            area_ativa.ativa
        )

    def test_inativar_area_inexistente(self):
        """
        Deve rejeitar a inativação
        de uma Área inexistente.
        """

        with self.assertRaises(ValorInvalido):
            self.coelba.inativar_area_atuacao(
                estado="Bahia",
                municipio="Caetité",
            )

    def test_ativar_area_inexistente(self):
        """
        Deve rejeitar a ativação
        de uma Área inexistente.
        """

        with self.assertRaises(ValorInvalido):
            self.coelba.ativar_area_atuacao(
                estado="Bahia",
                municipio="Caetité",
            )

    def test_alterar_situacao_concessionaria(
        self,
    ):
        """
        Deve alterar a situação pelas
        operações públicas da entidade.
        """

        resultado_suspensao = (
            self.coelba.suspender()
        )

        self.assertIs(
            resultado_suspensao,
            self.coelba,
        )

        self.assertEqual(
            self.coelba.situacao,
            SituacaoConcessionaria.SUSPENSA,
        )

        resultado_inativacao = (
            self.coelba.inativar()
        )

        self.assertIs(
            resultado_inativacao,
            self.coelba,
        )

        self.assertEqual(
            self.coelba.situacao,
            SituacaoConcessionaria.INATIVA,
        )

        resultado_ativacao = (
            self.coelba.ativar()
        )

        self.assertIs(
            resultado_ativacao,
            self.coelba,
        )

        self.assertEqual(
            self.coelba.situacao,
            SituacaoConcessionaria.ATIVA,
        )

    def test_normalizar_situacao_enum(self):
        """
        Deve aceitar uma situação
        que já seja uma instância do Enum.
        """

        resultado = (
            normalizar_situacao_concessionaria(
                SituacaoConcessionaria.ATIVA
            )
        )

        self.assertEqual(
            resultado,
            SituacaoConcessionaria.ATIVA,
        )

    def test_normalizar_situacao_string(self):
        """
        Deve converter uma string válida
        para o Enum correspondente.
        """

        resultado = (
            normalizar_situacao_concessionaria(
                "SUSPENSA"
            )
        )

        self.assertEqual(
            resultado,
            SituacaoConcessionaria.SUSPENSA,
        )

    def test_rejeitar_situacao_invalida(self):
        """
        Deve rejeitar uma situação inexistente.
        """

        with self.assertRaises(ValorInvalido):
            normalizar_situacao_concessionaria(
                "EXCLUIDA"
            )

    def test_buscar_concessionaria_por_codigo(
        self,
    ):
        """
        Deve retornar a Concessionária
        correspondente ao código.
        """

        resultado = (
            buscar_concessionaria_por_codigo(
                self.lista_concessionarias,
                1,
            )
        )

        self.assertIs(
            resultado,
            self.coelba,
        )

    def test_buscar_codigo_inexistente(self):
        """
        Deve retornar None quando
        o código não existir.
        """

        resultado = (
            buscar_concessionaria_por_codigo(
                self.lista_concessionarias,
                99,
            )
        )

        self.assertIsNone(resultado)

    def test_codigo_concessionaria_existe(
        self,
    ):
        """
        Deve informar se o código existe.
        """

        self.assertTrue(
            codigo_concessionaria_existe(
                self.lista_concessionarias,
                1,
            )
        )

        self.assertFalse(
            codigo_concessionaria_existe(
                self.lista_concessionarias,
                99,
            )
        )

    def test_buscar_concessionarias_por_nome(
        self,
    ):
        """
        Deve buscar pelo nome completo
        ou pelo nome abreviado.
        """

        resultado_nome = (
            buscar_concessionarias_por_nome(
                self.lista_concessionarias,
                "eletricidade",
            )
        )

        self.assertEqual(
            resultado_nome,
            [self.coelba],
        )

        resultado_nome_abreviado = (
            buscar_concessionarias_por_nome(
                self.lista_concessionarias,
                "COELBA",
            )
        )

        self.assertEqual(
            resultado_nome_abreviado,
            [self.coelba],
        )

    def test_busca_por_nome_obrigatoria(self):
        """
        Deve rejeitar uma consulta vazia.
        """

        with self.assertRaises(
            DadosObrigatoriosAusentes
        ):
            buscar_concessionarias_por_nome(
                self.lista_concessionarias,
                "",
            )

    def test_validar_codigo_duplicado(self):
        """
        Deve rejeitar código já cadastrado.
        """

        with self.assertRaises(
            RegistroDuplicado
        ):
            validar_duplicidade_concessionaria(
                self.lista_concessionarias,
                codigo=1,
            )

    def test_validar_cnpj_duplicado(self):
        """
        Deve rejeitar CNPJ já cadastrado.
        """

        with self.assertRaises(
            RegistroDuplicado
        ):
            validar_duplicidade_concessionaria(
                self.lista_concessionarias,
                codigo=3,
                cnpj="15.139.629/0001-94",
            )

    def test_validar_dados_sem_duplicidade(
        self,
    ):
        """
        Não deve lançar erro quando
        código e CNPJ estiverem disponíveis.
        """

        resultado = (
            validar_duplicidade_concessionaria(
                self.lista_concessionarias,
                codigo=3,
                cnpj="12.345.678/0001-90",
            )
        )

        self.assertIsNone(resultado)

    def test_reconstruir_concessionaria(self):
        """
        Deve reconstruir uma Concessionária
        a partir de dados persistidos.
        """

        concessionaria = reconstruir_concessionaria(
            codigo=3,
            nome="Concessionária Teste",
            nome_abreviado="Teste",
            cnpj="12.345.678/0001-90",
            situacao="SUSPENSA",
            areas_atuacao=[
                {
                    "estado": "Bahia",
                    "municipio": "Guanambi",
                    "ativa": True,
                },
                {
                    "estado": "Bahia",
                    "municipio": "Caetité",
                    "ativa": False,
                },
            ],
            data_cadastro=(
                "2026-07-20T10:00:00"
            ),
            data_atualizacao=(
                "2026-07-21T11:00:00"
            ),
        )

        self.assertIsInstance(
            concessionaria,
            Concessionaria,
        )

        self.assertEqual(
            concessionaria.situacao,
            SituacaoConcessionaria.SUSPENSA,
        )

        self.assertEqual(
            len(concessionaria.areas_atuacao),
            2,
        )

        self.assertTrue(
            concessionaria.areas_atuacao[0].ativa
        )

        self.assertFalse(
            concessionaria.areas_atuacao[1].ativa
        )

        self.assertEqual(
            concessionaria.data_cadastro,
            "2026-07-20T10:00:00",
        )

        self.assertEqual(
            concessionaria.data_atualizacao,
            "2026-07-21T11:00:00",
        )

    def test_reconstruir_com_area_duplicada(
        self,
    ):
        """
        Deve rejeitar Áreas de Atuação
        duplicadas nos dados persistidos.
        """

        with self.assertRaises(
            RegistroDuplicado
        ):
            reconstruir_concessionaria(
                codigo=3,
                nome="Concessionária Teste",
                nome_abreviado="Teste",
                areas_atuacao=[
                    {
                        "estado": "Bahia",
                        "municipio": "Caetité",
                    },
                    {
                        "estado": "bahia",
                        "municipio": "caetité",
                    },
                ],
            )

    def test_reconstruir_com_area_invalida(
        self,
    ):
        """
        Deve rejeitar dados inválidos
        de Área de Atuação.
        """

        with self.assertRaises(
            ValorInvalido
        ):
            reconstruir_concessionaria(
                codigo=3,
                nome="Concessionária Teste",
                nome_abreviado="Teste",
                areas_atuacao=[
                    "Bahia / Caetité"
                ],
            )

    def test_converter_concessionaria_para_dicionario(
        self,
    ):
        """
        Deve converter a entidade e seus
        Enums para dados apropriados ao JSON.
        """

        self.coelba.adicionar_area_atuacao(
            estado="Bahia",
            municipio="Guanambi",
        )

        dados = (
            converter_concessionaria_para_dicionario(
                self.coelba
            )
        )

        self.assertIsInstance(
            dados,
            dict,
        )

        self.assertEqual(
            dados["codigo"],
            1,
        )

        self.assertEqual(
            dados["situacao"],
            "ATIVA",
        )

        self.assertEqual(
            dados["areas_atuacao"][0]["estado"],
            "Bahia",
        )

        self.assertEqual(
            dados["areas_atuacao"][0]["municipio"],
            "Guanambi",
        )

        self.assertTrue(
            dados["areas_atuacao"][0]["ativa"]
        )

    def test_converter_objeto_invalido(self):
        """
        Deve rejeitar um objeto
        que não seja uma Concessionária.
        """

        with self.assertRaises(ValorInvalido):
            converter_concessionaria_para_dicionario(
                {}
            )


if __name__ == "__main__":
    unittest.main()