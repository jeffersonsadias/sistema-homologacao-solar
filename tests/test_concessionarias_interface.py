import unittest
from unittest.mock import patch

from app.dominio.concessionarias import (
    AreaAtuacao,
    criar_concessionaria,
)
from app.dominio.status import (
    SituacaoConcessionaria,
)
from app.interface import (
    concessionarias_interface,
)


class TestConcessionariasInterface(
    unittest.TestCase
):
    """
    Testes da interface de Concessionárias.

    Entradas, saídas e persistência são simuladas
    para impedir interação real com o terminal
    e com o arquivo concessionarias.json.
    """

    def setUp(self):
        """
        Cria uma lista vazia antes de cada teste.
        """

        self.lista_concessionarias = []

        self.coelba = criar_concessionaria(
            codigo=1,
            nome=(
                "Companhia de Eletricidade "
                "do Estado da Bahia"
            ),
            nome_abreviado="Neoenergia Coelba",
            cnpj="15.139.629/0001-94",
        )

    @patch(
        "app.interface.concessionarias_interface."
        "salvar_concessionarias"
    )
    @patch(
        "builtins.input"
    )
    def test_cadastrar_concessionaria(
        self,
        mock_input,
        mock_salvar,
    ):
        """
        Deve cadastrar e salvar
        uma nova Concessionária.
        """

        mock_input.side_effect = [
            "Companhia de Eletricidade "
            "do Estado da Bahia",
            "Neoenergia Coelba",
            "15.139.629/0001-94",
        ]

        resultado = (
            concessionarias_interface
            .cadastrar_concessionaria(
                self.lista_concessionarias
            )
        )

        self.assertIsNotNone(resultado)

        self.assertEqual(
            len(self.lista_concessionarias),
            1,
        )

        self.assertEqual(
            resultado.codigo,
            1,
        )

        self.assertEqual(
            resultado.nome_abreviado,
            "Neoenergia Coelba",
        )

        mock_salvar.assert_called_once_with(
            self.lista_concessionarias
        )

    @patch(
        "app.interface.concessionarias_interface."
        "salvar_concessionarias"
    )
    @patch(
        "builtins.input"
    )
    def test_cadastro_invalido_nao_salva(
        self,
        mock_input,
        mock_salvar,
    ):
        """
        Não deve salvar quando os dados
        do cadastro forem inválidos.
        """

        mock_input.side_effect = [
            "",
            "Teste",
            "",
        ]

        resultado = (
            concessionarias_interface
            .cadastrar_concessionaria(
                self.lista_concessionarias
            )
        )

        self.assertIsNone(resultado)

        self.assertEqual(
            self.lista_concessionarias,
            [],
        )

        mock_salvar.assert_not_called()

    @patch(
        "app.interface.concessionarias_interface."
        "salvar_concessionarias"
    )
    @patch(
        "app.interface.concessionarias_interface."
        "utils.ler_int"
    )
    @patch(
        "builtins.input"
    )
    def test_adicionar_area_atuacao(
        self,
        mock_input,
        mock_ler_int,
        mock_salvar,
    ):
        """
        Deve adicionar e salvar
        uma Área de Atuação.
        """

        self.lista_concessionarias.append(
            self.coelba
        )

        mock_ler_int.return_value = 1

        mock_input.side_effect = [
            "Bahia",
            "Caetité",
        ]

        resultado = (
            concessionarias_interface
            .adicionar_area_atuacao(
                self.lista_concessionarias
            )
        )

        self.assertIsInstance(
            resultado,
            AreaAtuacao,
        )

        self.assertEqual(
            len(self.coelba.areas_atuacao),
            1,
        )

        mock_salvar.assert_called_once_with(
            self.lista_concessionarias
        )

    @patch(
        "app.interface.concessionarias_interface."
        "salvar_concessionarias"
    )
    @patch(
        "app.interface.concessionarias_interface."
        "utils.ler_int"
    )
    @patch(
        "builtins.input"
    )
    def test_alterar_situacao_para_suspensa(
        self,
        mock_input,
        mock_ler_int,
        mock_salvar,
    ):
        """
        Deve suspender e salvar
        a Concessionária.
        """

        self.lista_concessionarias.append(
            self.coelba
        )

        mock_ler_int.return_value = 1
        mock_input.return_value = "3"

        resultado = (
            concessionarias_interface
            .alterar_situacao_concessionaria(
                self.lista_concessionarias
            )
        )

        self.assertIs(
            resultado,
            self.coelba,
        )

        self.assertEqual(
            self.coelba.situacao,
            SituacaoConcessionaria.SUSPENSA,
        )

        mock_salvar.assert_called_once_with(
            self.lista_concessionarias
        )

    @patch(
        "app.interface.concessionarias_interface."
        "utils.ler_int"
    )
    def test_selecionar_codigo_inexistente(
        self,
        mock_ler_int,
    ):
        """
        Deve retornar None quando o código
        da Concessionária não existir.
        """

        mock_ler_int.return_value = 99

        resultado = (
            concessionarias_interface
            .selecionar_concessionaria_por_codigo(
                self.lista_concessionarias
            )
        )

        self.assertIsNone(resultado)

    @patch(
        "app.interface.concessionarias_interface."
        "utils.ler_int"
    )
    def test_selecionar_concessionaria(
        self,
        mock_ler_int,
    ):
        """
        Deve retornar a Concessionária
        correspondente ao código.
        """

        self.lista_concessionarias.append(
            self.coelba
        )

        mock_ler_int.return_value = 1

        resultado = (
            concessionarias_interface
            .selecionar_concessionaria_por_codigo(
                self.lista_concessionarias
            )
        )

        self.assertIs(
            resultado,
            self.coelba,
        )

    @patch(
        "app.interface.concessionarias_interface."
        "exibir_concessionaria"
    )
    @patch(
        "builtins.input"
    )
    def test_buscar_por_nome(
        self,
        mock_input,
        mock_exibir,
    ):
        """
        Deve buscar e exibir
        uma Concessionária pelo nome.
        """

        self.lista_concessionarias.append(
            self.coelba
        )

        mock_input.side_effect = [
            "2",
            "coelba",
        ]

        resultado = (
            concessionarias_interface
            .buscar_concessionaria(
                self.lista_concessionarias
            )
        )

        self.assertEqual(
            resultado,
            [self.coelba],
        )

        mock_exibir.assert_called_once_with(
            self.coelba
        )

    @patch(
        "app.interface.concessionarias_interface."
        "salvar_concessionarias"
    )
    @patch(
        "app.interface.concessionarias_interface."
        "utils.ler_int"
    )
    @patch(
        "builtins.input"
    )
    def test_inativar_area_atuacao(
        self,
        mock_input,
        mock_ler_int,
        mock_salvar,
    ):
        """
        Deve inativar e salvar
        uma Área de Atuação.
        """

        self.coelba.adicionar_area_atuacao(
            estado="Bahia",
            municipio="Caetité",
        )

        self.lista_concessionarias.append(
            self.coelba
        )

        mock_ler_int.return_value = 1

        mock_input.side_effect = [
            "Bahia",
            "Caetité",
            "2",
        ]

        resultado = (
            concessionarias_interface
            .alterar_situacao_area_atuacao(
                self.lista_concessionarias
            )
        )

        self.assertIsNotNone(resultado)

        self.assertFalse(resultado.ativa)

        mock_salvar.assert_called_once_with(
            self.lista_concessionarias
        )


if __name__ == "__main__":
    unittest.main()