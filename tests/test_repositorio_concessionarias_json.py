import json
import tempfile
import unittest
from pathlib import Path

from app.dominio.concessionarias import (
    AreaAtuacao,
    Concessionaria,
    criar_concessionaria,
)
from app.dominio.erros_dominio import (
    DadosObrigatoriosAusentes,
    ValorInvalido,
)
from app.dominio.status import (
    SituacaoConcessionaria,
)
from app.infraestrutura.repositorio_concessionarias_json import (
    carregar_concessionarias,
    salvar_concessionarias,
)


class TestRepositorioConcessionariasJson(
    unittest.TestCase
):
    """
    Testes da persistência JSON
    das Concessionárias.

    Os testes utilizam uma pasta temporária
    para não alterar o arquivo real:

        data/concessionarias.json
    """

    def setUp(self):
        """
        Cria uma pasta e um arquivo temporários
        antes de cada teste.
        """

        self.pasta_temporaria = (
            tempfile.TemporaryDirectory()
        )

        self.caminho_arquivo = (
            Path(self.pasta_temporaria.name)
            / "concessionarias.json"
        )

        self.coelba = criar_concessionaria(
            codigo=1,
            nome=(
                "Companhia de Eletricidade "
                "do Estado da Bahia"
            ),
            nome_abreviado="Neoenergia Coelba",
            cnpj="15.139.629/0001-94",
        )

        self.coelba.adicionar_area_atuacao(
            estado="Bahia",
            municipio="Caetité",
        )

    def tearDown(self):
        """
        Remove a pasta temporária
        depois de cada teste.
        """

        self.pasta_temporaria.cleanup()

    def test_carregar_arquivo_inexistente(
        self,
    ):
        """
        Deve retornar uma lista vazia
        quando o arquivo não existir.
        """

        resultado = carregar_concessionarias(
            self.caminho_arquivo
        )

        self.assertEqual(
            resultado,
            [],
        )

    def test_carregar_arquivo_vazio(self):
        """
        Deve retornar uma lista vazia
        quando o arquivo estiver vazio.
        """

        self.caminho_arquivo.write_text(
            "",
            encoding="utf-8",
        )

        resultado = carregar_concessionarias(
            self.caminho_arquivo
        )

        self.assertEqual(
            resultado,
            [],
        )

    def test_carregar_lista_json_vazia(
        self,
    ):
        """
        Deve retornar uma lista vazia
        quando o JSON contiver uma lista vazia.
        """

        self.caminho_arquivo.write_text(
            "[]",
            encoding="utf-8",
        )

        resultado = carregar_concessionarias(
            self.caminho_arquivo
        )

        self.assertEqual(
            resultado,
            [],
        )

    def test_salvar_concessionarias(self):
        """
        Deve salvar as Concessionárias
        no arquivo JSON.
        """

        caminho_salvo = salvar_concessionarias(
            [self.coelba],
            self.caminho_arquivo,
        )

        self.assertEqual(
            caminho_salvo,
            self.caminho_arquivo,
        )

        self.assertTrue(
            self.caminho_arquivo.exists()
        )

        conteudo = self.caminho_arquivo.read_text(
            encoding="utf-8"
        )

        dados = json.loads(conteudo)

        self.assertIsInstance(
            dados,
            list,
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
            dados[0]["situacao"],
            "ATIVA",
        )

        self.assertEqual(
            dados[0]["cnpj"],
            "15139629000194",
        )

        self.assertEqual(
            dados[0]["areas_atuacao"][0]["estado"],
            "Bahia",
        )

        self.assertEqual(
            dados[0]["areas_atuacao"][0]["municipio"],
            "Caetité",
        )

        self.assertTrue(
            dados[0]["areas_atuacao"][0]["ativa"]
        )

    def test_salvar_cria_diretorio(
        self,
    ):
        """
        Deve criar automaticamente
        o diretório do arquivo.
        """

        caminho = (
            Path(self.pasta_temporaria.name)
            / "nova_pasta"
            / "concessionarias.json"
        )

        salvar_concessionarias(
            [self.coelba],
            caminho,
        )

        self.assertTrue(
            caminho.exists()
        )

    def test_salvar_lista_vazia(self):
        """
        Deve salvar corretamente
        uma lista vazia.
        """

        salvar_concessionarias(
            [],
            self.caminho_arquivo,
        )

        conteudo = self.caminho_arquivo.read_text(
            encoding="utf-8"
        )

        dados = json.loads(conteudo)

        self.assertEqual(
            dados,
            [],
        )

    def test_carregar_concessionarias(self):
        """
        Deve reconstruir as entidades
        armazenadas no JSON.
        """

        dados = [
            {
                "codigo": 1,
                "nome": (
                    "Companhia de Eletricidade "
                    "do Estado da Bahia"
                ),
                "nome_abreviado": (
                    "Neoenergia Coelba"
                ),
                "cnpj": "15139629000194",
                "situacao": "SUSPENSA",
                "areas_atuacao": [
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
                "data_cadastro": (
                    "2026-07-20T10:00:00"
                ),
                "data_atualizacao": (
                    "2026-07-21T11:00:00"
                ),
            }
        ]

        self.caminho_arquivo.write_text(
            json.dumps(
                dados,
                ensure_ascii=False,
                indent=4,
            ),
            encoding="utf-8",
        )

        resultado = carregar_concessionarias(
            self.caminho_arquivo
        )

        self.assertEqual(
            len(resultado),
            1,
        )

        concessionaria = resultado[0]

        self.assertIsInstance(
            concessionaria,
            Concessionaria,
        )

        self.assertEqual(
            concessionaria.codigo,
            1,
        )

        self.assertEqual(
            concessionaria.situacao,
            SituacaoConcessionaria.SUSPENSA,
        )

        self.assertEqual(
            len(concessionaria.areas_atuacao),
            2,
        )

        self.assertIsInstance(
            concessionaria.areas_atuacao[0],
            AreaAtuacao,
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

    def test_salvar_e_carregar_concessionarias(
        self,
    ):
        """
        Deve preservar os principais dados
        após o ciclo completo de persistência.
        """

        self.coelba.suspender()

        salvar_concessionarias(
            [self.coelba],
            self.caminho_arquivo,
        )

        resultado = carregar_concessionarias(
            self.caminho_arquivo
        )

        concessionaria_carregada = resultado[0]

        self.assertEqual(
            concessionaria_carregada.codigo,
            self.coelba.codigo,
        )

        self.assertEqual(
            concessionaria_carregada.nome,
            self.coelba.nome,
        )

        self.assertEqual(
            concessionaria_carregada.nome_abreviado,
            self.coelba.nome_abreviado,
        )

        self.assertEqual(
            concessionaria_carregada.cnpj,
            self.coelba.cnpj,
        )

        self.assertEqual(
            concessionaria_carregada.situacao,
            SituacaoConcessionaria.SUSPENSA,
        )

        self.assertEqual(
            concessionaria_carregada.areas_atuacao,
            self.coelba.areas_atuacao,
        )

        self.assertEqual(
            concessionaria_carregada.data_cadastro,
            self.coelba.data_cadastro,
        )

        self.assertEqual(
            concessionaria_carregada.data_atualizacao,
            self.coelba.data_atualizacao,
        )

    def test_rejeitar_conteudo_principal_invalido(
        self,
    ):
        """
        Deve rejeitar um JSON cujo conteúdo
        principal não seja uma lista.
        """

        self.caminho_arquivo.write_text(
            json.dumps(
                {
                    "codigo": 1,
                    "nome": "Concessionária Teste",
                }
            ),
            encoding="utf-8",
        )

        with self.assertRaises(ValueError):
            carregar_concessionarias(
                self.caminho_arquivo
            )

    def test_rejeitar_registro_que_nao_seja_objeto(
        self,
    ):
        """
        Deve rejeitar elementos da lista
        que não sejam objetos JSON.
        """

        self.caminho_arquivo.write_text(
            json.dumps(
                [
                    "Concessionária Teste"
                ]
            ),
            encoding="utf-8",
        )

        with self.assertRaises(ValueError):
            carregar_concessionarias(
                self.caminho_arquivo
            )

    def test_rejeitar_json_malformado(self):
        """
        Deve propagar JSONDecodeError
        quando o JSON estiver malformado.
        """

        self.caminho_arquivo.write_text(
            "{conteudo invalido",
            encoding="utf-8",
        )

        with self.assertRaises(
            json.JSONDecodeError
        ):
            carregar_concessionarias(
                self.caminho_arquivo
            )

    def test_rejeitar_dados_obrigatorios_ausentes(
        self,
    ):
        """
        Deve preservar as validações do domínio
        durante o carregamento.
        """

        dados = [
            {
                "codigo": 1,
                "nome": "",
                "nome_abreviado": "Teste",
                "situacao": "ATIVA",
            }
        ]

        self.caminho_arquivo.write_text(
            json.dumps(dados),
            encoding="utf-8",
        )

        with self.assertRaises(
            DadosObrigatoriosAusentes
        ):
            carregar_concessionarias(
                self.caminho_arquivo
            )

    def test_rejeitar_situacao_invalida(
        self,
    ):
        """
        Deve preservar a validação da situação
        durante o carregamento.
        """

        dados = [
            {
                "codigo": 1,
                "nome": "Concessionária Teste",
                "nome_abreviado": "Teste",
                "situacao": "EXCLUIDA",
            }
        ]

        self.caminho_arquivo.write_text(
            json.dumps(dados),
            encoding="utf-8",
        )

        with self.assertRaises(ValorInvalido):
            carregar_concessionarias(
                self.caminho_arquivo
            )


if __name__ == "__main__":
    unittest.main()