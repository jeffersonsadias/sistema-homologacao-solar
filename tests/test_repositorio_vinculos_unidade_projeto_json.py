import json
import tempfile
import unittest
from datetime import datetime
from pathlib import Path

from app.dominio.status import (
    PapelUnidadeProjeto,
)

from app.dominio.vinculos_unidade_projeto import (
    SituacaoVinculoUnidadeProjeto,
    VinculoUnidadeProjeto,
)

from app.infraestrutura.repositorio_vinculos_unidade_projeto_json import (
        carregar_vinculos_unidade_projeto,
        converter_vinculo_para_dicionario,
        reconstruir_vinculo_do_dicionario,
        salvar_vinculos_unidade_projeto,
    )


class TestRepositorioVinculosUnidadeProjetoJson(
    unittest.TestCase
):
    """
    Testes do repositório JSON
    dos vínculos entre Projetos
    e Unidades Consumidoras.
    """

    def setUp(self):
        """
        Cria um diretório temporário
        antes de cada teste.
        """

        self.diretorio_temporario = (
            tempfile.TemporaryDirectory()
        )

        self.caminho_arquivo = Path(
            self.diretorio_temporario.name
        ) / "vinculos.json"

        agora = datetime.now()

        self.vinculo = VinculoUnidadeProjeto(
            codigo=1,
            codigo_projeto=10,
            codigo_unidade_consumidora=20,
            papel=PapelUnidadeProjeto.GERADORA,
            situacao=(
                SituacaoVinculoUnidadeProjeto.ATIVO
            ),
            data_vinculo=agora,
            data_atualizacao=agora,
            observacoes=(
                "Unidade principal do projeto."
            ),
        )

    def tearDown(self):
        """
        Remove o diretório temporário
        depois de cada teste.
        """

        self.diretorio_temporario.cleanup()

    def test_salvar_vinculos(self):
        """
        Deve criar o arquivo JSON
        com os dados dos vínculos.
        """

        salvar_vinculos_unidade_projeto(
            [
                self.vinculo,
            ],
            self.caminho_arquivo,
        )

        self.assertTrue(
            self.caminho_arquivo.exists()
        )

        with self.caminho_arquivo.open(
            "r",
            encoding="utf-8",
        ) as arquivo:
            dados = json.load(
                arquivo
            )

        self.assertEqual(
            len(dados),
            1,
        )

        self.assertEqual(
            dados[0]["codigo"],
            1,
        )

        self.assertEqual(
            dados[0]["papel"],
            PapelUnidadeProjeto.GERADORA.value,
        )

        self.assertEqual(
            dados[0]["situacao"],
            (
                SituacaoVinculoUnidadeProjeto
                .ATIVO
                .value
            ),
        )

    def test_carregar_vinculos(self):
        """
        Deve reconstruir corretamente
        os objetos armazenados.
        """

        salvar_vinculos_unidade_projeto(
            [
                self.vinculo,
            ],
            self.caminho_arquivo,
        )

        resultado = (
            carregar_vinculos_unidade_projeto(
                self.caminho_arquivo
            )
        )

        self.assertEqual(
            len(resultado),
            1,
        )

        vinculo_carregado = resultado[0]

        self.assertIsInstance(
            vinculo_carregado,
            VinculoUnidadeProjeto,
        )

        self.assertEqual(
            vinculo_carregado.codigo,
            1,
        )

        self.assertEqual(
            vinculo_carregado.codigo_projeto,
            10,
        )

        self.assertEqual(
            vinculo_carregado
            .codigo_unidade_consumidora,
            20,
        )

        self.assertEqual(
            vinculo_carregado.papel,
            PapelUnidadeProjeto.GERADORA,
        )

        self.assertEqual(
            vinculo_carregado.situacao,
            SituacaoVinculoUnidadeProjeto.ATIVO,
        )

        self.assertEqual(
            vinculo_carregado.observacoes,
            "Unidade principal do projeto.",
        )

    def test_converter_vinculo_para_dicionario(
        self,
    ):
        """
        Deve converter enums e datas
        para valores compatíveis com JSON.
        """

        resultado = (
            converter_vinculo_para_dicionario(
                self.vinculo
            )
        )

        self.assertEqual(
            resultado["codigo"],
            1,
        )

        self.assertEqual(
            resultado["papel"],
            PapelUnidadeProjeto.GERADORA.value,
        )

        self.assertEqual(
            resultado["situacao"],
            (
                SituacaoVinculoUnidadeProjeto
                .ATIVO
                .value
            ),
        )

        self.assertEqual(
            resultado["data_vinculo"],
            self.vinculo.data_vinculo.isoformat(),
        )

    def test_reconstruir_vinculo_do_dicionario(
        self,
    ):
        """
        Deve reconstruir o objeto
        a partir de um dicionário.
        """

        dados = (
            converter_vinculo_para_dicionario(
                self.vinculo
            )
        )

        resultado = (
            reconstruir_vinculo_do_dicionario(
                dados
            )
        )

        self.assertIsInstance(
            resultado,
            VinculoUnidadeProjeto,
        )

        self.assertEqual(
            resultado.papel,
            PapelUnidadeProjeto.GERADORA,
        )

        self.assertEqual(
            resultado.situacao,
            SituacaoVinculoUnidadeProjeto.ATIVO,
        )

    def test_arquivo_inexistente(self):
        """
        Deve retornar uma lista vazia
        quando o arquivo não existir.
        """

        resultado = (
            carregar_vinculos_unidade_projeto(
                self.caminho_arquivo
            )
        )

        self.assertEqual(
            resultado,
            [],
        )

    def test_arquivo_vazio(self):
        """
        Deve retornar uma lista vazia
        quando o arquivo estiver vazio.
        """

        self.caminho_arquivo.write_text(
            "",
            encoding="utf-8",
        )

        resultado = (
            carregar_vinculos_unidade_projeto(
                self.caminho_arquivo
            )
        )

        self.assertEqual(
            resultado,
            [],
        )

    def test_json_invalido(self):
        """
        Deve retornar uma lista vazia
        quando o conteúdo JSON for inválido.
        """

        self.caminho_arquivo.write_text(
            "{ conteúdo inválido",
            encoding="utf-8",
        )

        resultado = (
            carregar_vinculos_unidade_projeto(
                self.caminho_arquivo
            )
        )

        self.assertEqual(
            resultado,
            [],
        )


if __name__ == "__main__":
    unittest.main()