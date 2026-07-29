"""
Testes do repositório JSON de empresas.

Esses testes utilizam arquivos temporários.

O arquivo real:

    data/empresas.json

não será alterado durante a execução.
"""

import json
import tempfile
import unittest
from pathlib import Path

from app.dominio.empresas import criar_dados_empresa
from app.infraestrutura.repositorio_empresas_json import (
    carregar_empresas,
    salvar_empresas,
)


class TestRepositorioEmpresasJson(unittest.TestCase):
    """
    Testa o carregamento e a gravação das empresas em JSON.
    """

    def setUp(self):
        """
        Cria uma pasta temporária antes de cada teste.

        Cada teste recebe seu próprio arquivo, evitando interferência
        entre os casos testados.
        """

        self.diretorio_temporario = tempfile.TemporaryDirectory()

        self.caminho_arquivo = (
            Path(self.diretorio_temporario.name)
            / "empresas_teste.json"
        )

        self.empresa = criar_dados_empresa(
            codigo=1,
            razao_social="Solar Energia Bahia Ltda",
            nome_fantasia="Solar Bahia",
            cnpj="11.222.333/0001-81",
            email="contato@solarbahia.com.br",
            telefone="(77) 99999-9999",
        )

    def tearDown(self):
        """
        Remove a pasta temporária após cada teste.
        """

        self.diretorio_temporario.cleanup()

    # ========================================================
    # CARREGAMENTO
    # ========================================================

    def test_carregar_empresas_cria_arquivo_quando_nao_existe(self):
        """
        O repositório deve criar um arquivo vazio automaticamente.
        """

        self.assertFalse(
            self.caminho_arquivo.exists(),
        )

        empresas = carregar_empresas(
            self.caminho_arquivo,
        )

        self.assertEqual(
            empresas,
            [],
        )

        self.assertTrue(
            self.caminho_arquivo.exists(),
        )

    def test_arquivo_criado_contem_lista_vazia(self):
        """
        O arquivo criado automaticamente deve conter [].
        """

        carregar_empresas(
            self.caminho_arquivo,
        )

        with self.caminho_arquivo.open(
            mode="r",
            encoding="utf-8",
        ) as arquivo:
            dados = json.load(
                arquivo,
            )

        self.assertEqual(
            dados,
            [],
        )

    def test_carregar_lista_vazia(self):
        """
        Deve carregar corretamente um arquivo com uma lista vazia.
        """

        with self.caminho_arquivo.open(
            mode="w",
            encoding="utf-8",
        ) as arquivo:
            json.dump(
                [],
                arquivo,
            )

        empresas = carregar_empresas(
            self.caminho_arquivo,
        )

        self.assertEqual(
            empresas,
            [],
        )

    def test_carregar_empresas_salvas(self):
        """
        Deve recuperar os mesmos dados anteriormente salvos.
        """

        salvar_empresas(
            [self.empresa],
            self.caminho_arquivo,
        )

        empresas_carregadas = carregar_empresas(
            self.caminho_arquivo,
        )

        self.assertEqual(
            len(empresas_carregadas),
            1,
        )

        self.assertEqual(
            empresas_carregadas[0],
            self.empresa,
        )

    def test_carregar_preserva_caracteres_acentuados(self):
        """
        A leitura deve preservar caracteres da língua portuguesa.
        """

        salvar_empresas(
            [self.empresa],
            self.caminho_arquivo,
        )

        empresas_carregadas = carregar_empresas(
            self.caminho_arquivo,
        )

        self.assertEqual(
            empresas_carregadas[0]["razao_social"],
            "Solar Energia Bahia Ltda",
        )

        self.assertEqual(
            empresas_carregadas[0]["nome_fantasia"],
            "Solar Bahia",
        )

    def test_carregar_json_invalido(self):
        """
        Um arquivo com JSON inválido deve gerar ValueError.
        """

        with self.caminho_arquivo.open(
            mode="w",
            encoding="utf-8",
        ) as arquivo:
            arquivo.write(
                '{"codigo": 1'
            )

        with self.assertRaises(ValueError):
            carregar_empresas(
                self.caminho_arquivo,
            )

    def test_carregar_raiz_que_nao_seja_lista(self):
        """
        A raiz do arquivo deve ser uma lista.
        """

        with self.caminho_arquivo.open(
            mode="w",
            encoding="utf-8",
        ) as arquivo:
            json.dump(
                {
                    "codigo": 1,
                    "nome_fantasia": "Solar Bahia",
                },
                arquivo,
            )

        with self.assertRaises(ValueError):
            carregar_empresas(
                self.caminho_arquivo,
            )

    def test_carregar_lista_com_item_que_nao_seja_dicionario(self):
        """
        Cada item da lista deve ser um objeto JSON.
        """

        with self.caminho_arquivo.open(
            mode="w",
            encoding="utf-8",
        ) as arquivo:
            json.dump(
                [
                    {
                        "codigo": 1,
                        "nome_fantasia": "Solar Bahia",
                    },
                    "item inválido",
                ],
                arquivo,
                ensure_ascii=False,
            )

        with self.assertRaises(ValueError):
            carregar_empresas(
                self.caminho_arquivo,
            )

    # ========================================================
    # SALVAMENTO
    # ========================================================

    def test_salvar_empresas_cria_arquivo(self):
        """
        O salvamento deve criar o arquivo quando ele não existir.
        """

        self.assertFalse(
            self.caminho_arquivo.exists(),
        )

        salvar_empresas(
            [self.empresa],
            self.caminho_arquivo,
        )

        self.assertTrue(
            self.caminho_arquivo.exists(),
        )

    def test_salvar_empresas_cria_diretorios(self):
        """
        O salvamento deve criar as pastas necessárias.
        """

        caminho_em_subpastas = (
            Path(self.diretorio_temporario.name)
            / "dados"
            / "cadastros"
            / "empresas.json"
        )

        self.assertFalse(
            caminho_em_subpastas.parent.exists(),
        )

        salvar_empresas(
            [self.empresa],
            caminho_em_subpastas,
        )

        self.assertTrue(
            caminho_em_subpastas.exists(),
        )

    def test_salvar_lista_vazia(self):
        """
        Deve ser possível salvar uma lista sem empresas.
        """

        salvar_empresas(
            [],
            self.caminho_arquivo,
        )

        empresas_carregadas = carregar_empresas(
            self.caminho_arquivo,
        )

        self.assertEqual(
            empresas_carregadas,
            [],
        )

    def test_salvar_substitui_conteudo_anterior(self):
        """
        Um novo salvamento deve substituir o conteúdo do arquivo.
        """

        salvar_empresas(
            [self.empresa],
            self.caminho_arquivo,
        )

        salvar_empresas(
            [],
            self.caminho_arquivo,
        )

        empresas_carregadas = carregar_empresas(
            self.caminho_arquivo,
        )

        self.assertEqual(
            empresas_carregadas,
            [],
        )

    def test_salvar_varias_empresas(self):
        """
        Deve salvar e carregar mais de uma empresa.
        """

        segunda_empresa = criar_dados_empresa(
            codigo=2,
            razao_social="Energia do Sertão Ltda",
            nome_fantasia="Energia Sertão",
            cnpj="45.723.174/0001-10",
            email="contato@energiasertao.com.br",
            telefone="(77) 98888-7777",
        )

        salvar_empresas(
            [
                self.empresa,
                segunda_empresa,
            ],
            self.caminho_arquivo,
        )

        empresas_carregadas = carregar_empresas(
            self.caminho_arquivo,
        )

        self.assertEqual(
            len(empresas_carregadas),
            2,
        )

        self.assertEqual(
            empresas_carregadas[0]["codigo"],
            1,
        )

        self.assertEqual(
            empresas_carregadas[1]["codigo"],
            2,
        )

    def test_salvar_preserva_acentuacao_no_arquivo(self):
        """
        O arquivo deve armazenar caracteres acentuados diretamente.
        """

        empresa_acentuada = criar_dados_empresa(
            codigo=2,
            razao_social="Soluções Energéticas do Sertão Ltda",
            nome_fantasia="Soluções Sertão",
            cnpj="45.723.174/0001-10",
            email="contato@solucoes.com.br",
            telefone="(77) 98888-7777",
        )

        salvar_empresas(
            [empresa_acentuada],
            self.caminho_arquivo,
        )

        conteudo = self.caminho_arquivo.read_text(
            encoding="utf-8",
        )

        self.assertIn(
            "Soluções Energéticas do Sertão Ltda",
            conteudo,
        )

        self.assertNotIn(
            "\\u00e7",
            conteudo,
        )

    def test_salvar_rejeita_valor_que_nao_seja_lista(self):
        """
        A coleção de empresas deve ser uma lista.
        """

        with self.assertRaises(TypeError):
            salvar_empresas(
                {
                    "codigo": 1,
                    "nome_fantasia": "Solar Bahia",
                },
                self.caminho_arquivo,
            )

    def test_salvar_rejeita_item_que_nao_seja_dicionario(self):
        """
        Cada empresa deve ser representada por um dicionário.
        """

        with self.assertRaises(TypeError):
            salvar_empresas(
                [
                    self.empresa,
                    "empresa inválida",
                ],
                self.caminho_arquivo,
            )

    # ========================================================
    # INTEGRAÇÃO BÁSICA ENTRE DOMÍNIO E REPOSITÓRIO
    # ========================================================

    def test_empresa_criada_pelo_dominio_pode_ser_persistida(self):
        """
        Confirma a integração básica entre o domínio e a infraestrutura.
        """

        empresa = criar_dados_empresa(
            codigo=3,
            razao_social="Solar Oeste Engenharia Ltda",
            nome_fantasia="Solar Oeste",
            cnpj="12.345.678/0001-95",
            email="contato@solaroeste.com.br",
            telefone="(77) 97777-6666",
        )

        salvar_empresas(
            [empresa],
            self.caminho_arquivo,
        )

        empresas_carregadas = carregar_empresas(
            self.caminho_arquivo,
        )

        self.assertEqual(
            empresas_carregadas[0]["cnpj"],
            "12345678000195",
        )

        self.assertEqual(
            empresas_carregadas[0]["situacao"],
            "ATIVA",
        )


if __name__ == "__main__":
    unittest.main()