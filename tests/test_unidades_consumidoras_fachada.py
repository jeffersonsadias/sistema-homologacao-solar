import unittest
from unittest.mock import patch

from app import unidades_consumidoras
from app.dominio.unidades_consumidoras import (
    EnderecoUnidade,
    TipoLigacao,
    TipoTitular,
    TitularConta,
    criar_unidade_consumidora,
)


class TestUnidadesConsumidorasFachada(
    unittest.TestCase
):
    """
    Testes da fachada de Unidades Consumidoras.
    """

    def setUp(self):
        """
        Preserva a lista original e substitui
        por uma lista controlada pelos testes.
        """

        self.lista_original = (
            unidades_consumidoras
            .unidades_consumidoras
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

        unidades_consumidoras.unidades_consumidoras = [
            self.unidade
        ]

    def tearDown(self):
        """
        Restaura a lista original.
        """

        unidades_consumidoras.unidades_consumidoras = (
            self.lista_original
        )

    @patch(
        "app.unidades_consumidoras."
        "interface.cadastrar_unidade_consumidora"
    )
    def test_cadastrar_unidade_consumidora(
        self,
        mock_cadastrar,
    ):
        """
        Deve encaminhar a lista de Unidades
        Consumidoras e as Concessionárias
        para a camada de interface.
        """

        concessionarias = [
            object()
        ]

        unidades_consumidoras.cadastrar_unidade_consumidora(
            concessionarias
        )

        mock_cadastrar.assert_called_once_with(
            unidades_consumidoras
            .unidades_consumidoras,
            concessionarias,
        )

    @patch(
        "app.unidades_consumidoras."
        "interface.listar_unidades_consumidoras"
    )
    def test_listar_unidades_consumidoras(
        self,
        mock_listar,
    ):
        """
        Deve encaminhar as listas necessárias
        para a interface de listagem.
        """

        concessionarias = [
            object()
        ]

        unidades_consumidoras.listar_unidades_consumidoras(
            concessionarias
        )

        mock_listar.assert_called_once_with(
            unidades_consumidoras
            .unidades_consumidoras,
            concessionarias,
        )

    @patch(
        "app.unidades_consumidoras."
        "interface.buscar_unidade_consumidora"
    )
    def test_buscar_unidade_consumidora(
        self,
        mock_buscar,
    ):
        """
        Deve encaminhar as listas necessárias
        para a interface de busca.
        """

        concessionarias = [
            object()
        ]

        unidades_consumidoras.buscar_unidade_consumidora(
            concessionarias
        )

        mock_buscar.assert_called_once_with(
            unidades_consumidoras
            .unidades_consumidoras,
            concessionarias,
        )

    @patch(
        "app.unidades_consumidoras."
        "interface.selecionar_unidade_por_codigo"
    )
    def test_selecionar_unidade_por_codigo(
        self,
        mock_selecionar,
    ):
        """
        Deve encaminhar a lista de Unidades
        Consumidoras para a interface de seleção.
        """

        unidades_consumidoras.selecionar_unidade_por_codigo()

        mock_selecionar.assert_called_once_with(
            unidades_consumidoras
            .unidades_consumidoras
        )

    @patch(
        "app.unidades_consumidoras."
        "interface.alterar_situacao_unidade"
    )
    def test_alterar_situacao_unidade(
        self,
        mock_alterar,
    ):
        """
        Deve encaminhar a lista de Unidades
        Consumidoras para alteração de situação.
        """

        unidades_consumidoras.alterar_situacao_unidade()

        mock_alterar.assert_called_once_with(
            unidades_consumidoras
            .unidades_consumidoras
        )

    @patch(
        "app.unidades_consumidoras."
        "interface.menu_unidades_consumidoras"
    )
    def test_abrir_menu_unidades_consumidoras(
        self,
        mock_menu,
    ):
        """
        Deve abrir o menu de Unidades Consumidoras
        com as listas necessárias.
        """

        concessionarias = [
            object()
        ]

        unidades_consumidoras.abrir_menu_unidades_consumidoras(
            concessionarias
        )

        mock_menu.assert_called_once_with(
            unidades_consumidoras
            .unidades_consumidoras,
            concessionarias,
        )

    @patch(
        "app.unidades_consumidoras."
        "buscar_unidade_por_codigo_dominio"
    )
    def test_obter_unidade_consumidora_por_codigo(
        self,
        mock_buscar_unidade,
    ):
        """
        Deve enviar ao domínio primeiro
        a coleção de Unidades Consumidoras
        e depois o código pesquisado.
        """

        unidade_encontrada = object()

        mock_buscar_unidade.return_value = (
            unidade_encontrada
        )

        resultado = (
            unidades_consumidoras
            .obter_unidade_consumidora_por_codigo(
                123456789
            )
        )

        mock_buscar_unidade.assert_called_once_with(
            unidades_consumidoras
            .unidades_consumidoras,
            123456789,
        )

        self.assertIs(
            resultado,
            unidade_encontrada,
        )


if __name__ == "__main__":
    unittest.main()