import json
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from app.dominio.unidades_consumidoras import (
    EnderecoUnidade,
    SituacaoUnidadeConsumidora,
    TipoLigacao,
    TipoTitular,
    TitularConta,
    criar_unidade_consumidora,
)
from app.infraestrutura import (
    repositorio_unidades_consumidoras_json
    as repositorio,
)


class TestRepositorioUnidadesConsumidorasJson(
    unittest.TestCase
):
    """
    Testes do repositório JSON
    das Unidades Consumidoras.
    """

    def setUp(self):
        """
        Cria um diretório temporário
        para evitar alterações no arquivo real.
        """

        self.diretorio_temporario = (
            tempfile.TemporaryDirectory()
        )

        self.caminho_temporario = (
            Path(
                self.diretorio_temporario.name
            )
            / "unidades_consumidoras.json"
        )

        self.patch_caminho = patch.object(
            repositorio,
            "CAMINHO_ARQUIVO",
            self.caminho_temporario,
        )

        self.patch_caminho.start()

        titular = TitularConta(
            nome="João da Silva",
            documento="12345678900",
            tipo=TipoTitular.PESSOA_FISICA,
        )

        endereco = EnderecoUnidade(
            logradouro="Rua das Flores",
            numero="100",
            bairro="Centro",
            cidade="Caetité",
            estado="BA",
            cep="46400000",
            complemento="Casa",
        )

        self.unidade = (
            criar_unidade_consumidora(
                codigo=1,
                numero_uc="703456789",
                codigo_cliente="900123",
                codigo_concessionaria=1,
                titular=titular,
                endereco=endereco,
                tipo_ligacao=(
                    TipoLigacao.TRIFASICA
                ),
                carga_instalada_kw=10.5,
            )
        )

    def tearDown(self):
        """
        Encerra o patch e remove
        o diretório temporário.
        """

        self.patch_caminho.stop()

        self.diretorio_temporario.cleanup()

    def test_salvar_unidades_consumidoras(self):
        """
        Deve salvar os dados no arquivo JSON.
        """

        repositorio.salvar_unidades_consumidoras(
            [self.unidade]
        )

        self.assertTrue(
            self.caminho_temporario.exists()
        )

        with open(
            self.caminho_temporario,
            "r",
            encoding="utf-8",
        ) as arquivo:
            dados = json.load(arquivo)

        self.assertEqual(
            len(dados),
            1,
        )

        self.assertEqual(
            dados[0]["codigo"],
            1,
        )

        self.assertEqual(
            dados[0]["numero_uc"],
            "703456789",
        )

        self.assertEqual(
            dados[0]["tipo_ligacao"],
            "TRIFASICA",
        )

        self.assertEqual(
            dados[0]["situacao"],
            "ATIVA",
        )

    def test_carregar_unidades_consumidoras(self):
        """
        Deve reconstruir objetos do domínio
        a partir do arquivo JSON.
        """

        repositorio.salvar_unidades_consumidoras(
            [self.unidade]
        )

        unidades = (
            repositorio
            .carregar_unidades_consumidoras()
        )

        self.assertEqual(
            len(unidades),
            1,
        )

        unidade_carregada = unidades[0]

        self.assertEqual(
            unidade_carregada.codigo,
            1,
        )

        self.assertEqual(
            unidade_carregada.numero_uc,
            "703456789",
        )

        self.assertEqual(
            unidade_carregada.titular.nome,
            "João da Silva",
        )

        self.assertEqual(
            unidade_carregada.endereco.cidade,
            "Caetité",
        )

        self.assertEqual(
            unidade_carregada.tipo_ligacao,
            TipoLigacao.TRIFASICA,
        )

        self.assertEqual(
            unidade_carregada.situacao,
            SituacaoUnidadeConsumidora.ATIVA,
        )

    def test_preservar_historico(self):
        """
        Deve salvar e reconstruir
        o histórico de alterações.
        """

        self.unidade.alterar_carga_instalada(
            15.0,
            motivo="Ampliação de carga.",
        )

        repositorio.salvar_unidades_consumidoras(
            [self.unidade]
        )

        unidades = (
            repositorio
            .carregar_unidades_consumidoras()
        )

        unidade_carregada = unidades[0]

        self.assertEqual(
            len(
                unidade_carregada
                .historico_alteracoes
            ),
            1,
        )

        registro = (
            unidade_carregada
            .historico_alteracoes[0]
        )

        self.assertEqual(
            registro.valor_anterior,
            "10.5",
        )

        self.assertEqual(
            registro.valor_novo,
            "15.0",
        )

        self.assertEqual(
            registro.motivo,
            "Ampliação de carga.",
        )

    def test_carregar_quando_arquivo_nao_existe(
        self,
    ):
        """
        Deve retornar lista vazia quando
        o arquivo ainda não existir.
        """

        resultado = (
            repositorio
            .carregar_unidades_consumidoras()
        )

        self.assertEqual(
            resultado,
            [],
        )

    def test_carregar_arquivo_vazio(self):
        """
        Deve retornar lista vazia quando
        o arquivo estiver vazio.
        """

        self.caminho_temporario.write_text(
            "",
            encoding="utf-8",
        )

        resultado = (
            repositorio
            .carregar_unidades_consumidoras()
        )

        self.assertEqual(
            resultado,
            [],
        )

    def test_carregar_json_invalido(self):
        """
        Deve retornar lista vazia quando
        o conteúdo não for um JSON válido.
        """

        self.caminho_temporario.write_text(
            "conteúdo inválido",
            encoding="utf-8",
        )

        resultado = (
            repositorio
            .carregar_unidades_consumidoras()
        )

        self.assertEqual(
            resultado,
            [],
        )

    def test_carregar_estrutura_que_nao_seja_lista(
        self,
    ):
        """
        Deve retornar lista vazia quando
        a estrutura principal do JSON
        não for uma lista.
        """

        self.caminho_temporario.write_text(
            '{"codigo": 1}',
            encoding="utf-8",
        )

        resultado = (
            repositorio
            .carregar_unidades_consumidoras()
        )

        self.assertEqual(
            resultado,
            [],
        )


if __name__ == "__main__":
    unittest.main()