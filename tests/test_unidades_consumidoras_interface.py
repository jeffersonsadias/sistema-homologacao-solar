import unittest
from unittest.mock import patch

from app.dominio.concessionarias import (
    AreaAtuacao,
    Concessionaria,
    SituacaoConcessionaria,
)
from app.dominio.unidades_consumidoras import (
    EnderecoUnidade,
    SituacaoUnidadeConsumidora,
    TipoLigacao,
    TipoTitular,
    TitularConta,
    criar_unidade_consumidora,
)
from app.interface import (
    unidades_consumidoras_interface
    as interface,
)


class TestUnidadesConsumidorasInterface(
    unittest.TestCase
):
    """
    Testes da interface
    das Unidades Consumidoras.
    """

    def setUp(self):
        """
        Cria dados reutilizados pelos testes.
        """

        self.concessionaria = Concessionaria(
            codigo=1,
            nome=(
                "Companhia de Eletricidade "
                "do Estado da Bahia"
            ),
            nome_abreviado="Neoenergia Coelba",
            cnpj="15139629000194",
            situacao=(
                SituacaoConcessionaria.ATIVA
            ),
            areas_atuacao=[],
        )

        self.titular = TitularConta(
            nome="João da Silva",
            documento="12345678900",
            tipo=TipoTitular.PESSOA_FISICA,
        )

        self.endereco = EnderecoUnidade(
            logradouro="Rua das Flores",
            numero="100",
            bairro="Centro",
            cidade="Caetité",
            estado="BA",
            cep="46400000",
        )

        self.unidade = (
            criar_unidade_consumidora(
                codigo=1,
                numero_uc="703456789",
                codigo_cliente="900123",
                codigo_concessionaria=1,
                titular=self.titular,
                endereco=self.endereco,
                tipo_ligacao=(
                    TipoLigacao.TRIFASICA
                ),
                carga_instalada_kw=10.5,
            )
        )

    @patch("builtins.input", return_value="1")
    def test_selecionar_tipo_titular_pessoa_fisica(
        self,
        mock_input,
    ):
        resultado = (
            interface.selecionar_tipo_titular()
        )

        self.assertEqual(
            resultado,
            TipoTitular.PESSOA_FISICA,
        )

    @patch("builtins.input", return_value="2")
    def test_selecionar_tipo_ligacao_bifasica(
        self,
        mock_input,
    ):
        resultado = (
            interface.selecionar_tipo_ligacao()
        )

        self.assertEqual(
            resultado,
            TipoLigacao.BIFASICA,
        )

    @patch(
        "app.interface."
        "unidades_consumidoras_interface."
        "utils.ler_int",
        return_value=1,
    )
    def test_selecionar_concessionaria(
        self,
        mock_ler_int,
    ):
        resultado = (
            interface.selecionar_concessionaria(
                [self.concessionaria]
            )
        )

        self.assertIs(
            resultado,
            self.concessionaria,
        )

    def test_selecionar_concessionaria_lista_vazia(
        self,
    ):
        resultado = (
            interface.selecionar_concessionaria(
                []
            )
        )

        self.assertIsNone(resultado)

    @patch(
        "app.interface."
        "unidades_consumidoras_interface."
        "salvar_unidades_consumidoras"
    )
    @patch(
        "app.interface."
        "unidades_consumidoras_interface."
        "utils.ler_float",
        return_value=10.5,
    )
    @patch(
        "app.interface."
        "unidades_consumidoras_interface."
        "selecionar_tipo_ligacao",
        return_value=TipoLigacao.TRIFASICA,
    )
    @patch(
        "app.interface."
        "unidades_consumidoras_interface."
        "coletar_endereco"
    )
    @patch(
        "app.interface."
        "unidades_consumidoras_interface."
        "coletar_titular"
    )
    @patch(
        "app.interface."
        "unidades_consumidoras_interface."
        "selecionar_concessionaria"
    )
    @patch(
        "builtins.input",
        side_effect=[
            "703456789",
            "900123",
        ],
    )
    def test_cadastrar_unidade_consumidora(
        self,
        mock_input,
        mock_selecionar_concessionaria,
        mock_coletar_titular,
        mock_coletar_endereco,
        mock_tipo_ligacao,
        mock_ler_float,
        mock_salvar,
    ):
        unidades = []

        mock_selecionar_concessionaria.return_value = (
            self.concessionaria
        )

        mock_coletar_titular.return_value = (
            self.titular
        )

        mock_coletar_endereco.return_value = (
            self.endereco
        )

        resultado = (
            interface
            .cadastrar_unidade_consumidora(
                unidades,
                [self.concessionaria],
            )
        )

        self.assertEqual(
            len(unidades),
            1,
        )

        self.assertIs(
            resultado,
            unidades[0],
        )

        self.assertEqual(
            resultado.numero_uc,
            "703456789",
        )

        mock_salvar.assert_called_once_with(
            unidades
        )

    @patch(
        "app.interface."
        "unidades_consumidoras_interface."
        "selecionar_concessionaria"
    )
    @patch(
        "builtins.input",
        return_value="703456789",
    )
    def test_impedir_numero_uc_duplicado(
        self,
        mock_input,
        mock_selecionar_concessionaria,
    ):
        mock_selecionar_concessionaria.return_value = (
            self.concessionaria
        )

        unidades = [
            self.unidade,
        ]

        resultado = (
            interface
            .cadastrar_unidade_consumidora(
                unidades,
                [self.concessionaria],
            )
        )

        self.assertIsNone(resultado)

        self.assertEqual(
            len(unidades),
            1,
        )

    def test_listar_unidades_lista_vazia(self):
        resultado = (
            interface
            .listar_unidades_consumidoras(
                []
            )
        )

        self.assertEqual(
            resultado,
            [],
        )

    @patch(
        "app.interface."
        "unidades_consumidoras_interface."
        "exibir_unidade_consumidora"
    )
    def test_listar_unidades(
        self,
        mock_exibir,
    ):
        unidades = [
            self.unidade,
        ]

        resultado = (
            interface
            .listar_unidades_consumidoras(
                unidades
            )
        )

        self.assertIs(
            resultado,
            unidades,
        )

        mock_exibir.assert_called_once_with(
            self.unidade,
            None,
        )

    @patch(
        "app.interface."
        "unidades_consumidoras_interface."
        "utils.ler_int",
        return_value=1,
    )
    def test_selecionar_unidade_por_codigo(
        self,
        mock_ler_int,
    ):
        resultado = (
            interface
            .selecionar_unidade_por_codigo(
                [self.unidade]
            )
        )

        self.assertIs(
            resultado,
            self.unidade,
        )

    @patch(
        "app.interface."
        "unidades_consumidoras_interface."
        "salvar_unidades_consumidoras"
    )
    @patch(
        "app.interface."
        "unidades_consumidoras_interface."
        "selecionar_unidade_por_codigo"
    )
    @patch(
        "builtins.input",
        side_effect=[
            "2",
            "Conta encerrada.",
        ],
    )
    def test_inativar_unidade(
        self,
        mock_input,
        mock_selecionar,
        mock_salvar,
    ):
        unidades = [
            self.unidade,
        ]

        mock_selecionar.return_value = (
            self.unidade
        )

        resultado = (
            interface.alterar_situacao_unidade(
                unidades
            )
        )

        self.assertIs(
            resultado,
            self.unidade,
        )

        self.assertEqual(
            self.unidade.situacao,
            SituacaoUnidadeConsumidora.INATIVA,
        )

        mock_salvar.assert_called_once_with(
            unidades
        )


if __name__ == "__main__":
    unittest.main()