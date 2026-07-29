"""
Testes do repositório JSON de Usuários.

Este arquivo testa:

- criação automática do diretório;
- criação automática do arquivo;
- carregamento de lista vazia;
- salvamento de usuários;
- carregamento de usuários;
- preservação de acentos;
- validação da estrutura principal;
- rejeição de itens inválidos;
- tratamento de JSON inválido.

Os testes utilizam diretórios temporários.

Dessa forma, o arquivo real:

    data/usuarios.json

não é criado, alterado ou removido durante os testes.
"""

import json
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from app.infraestrutura import (
    repositorio_usuarios_json,
)


class TestRepositorioUsuariosJson(
    unittest.TestCase
):
    """
    Testes do repositório JSON
    responsável pelos Usuários.
    """

    def setUp(
        self,
    ):
        """
        Cria um diretório temporário
        antes de cada teste.

        Também substitui o caminho real
        do repositório por um caminho
        localizado dentro desse diretório.
        """

        self.diretorio_temporario = (
            tempfile.TemporaryDirectory()
        )

        self.caminho_temporario = (
            Path(
                self.diretorio_temporario.name
            )
            / "data"
            / "usuarios.json"
        )

        self.patch_caminho = patch.object(
            repositorio_usuarios_json,
            "CAMINHO_ARQUIVO_USUARIOS",
            self.caminho_temporario,
        )

        self.patch_caminho.start()

    def tearDown(
        self,
    ):
        """
        Restaura o caminho original
        e remove o diretório temporário.
        """

        self.patch_caminho.stop()

        self.diretorio_temporario.cleanup()

    def test_criar_diretorio_automaticamente(
        self,
    ):
        """
        O diretório de dados deve ser criado
        automaticamente quando não existir.
        """

        self.assertFalse(
            self.caminho_temporario.parent.exists()
        )

        repositorio_usuarios_json.carregar_usuarios()

        self.assertTrue(
            self.caminho_temporario.parent.exists()
        )

    def test_criar_arquivo_automaticamente(
        self,
    ):
        """
        O arquivo de Usuários deve ser criado
        automaticamente quando não existir.
        """

        self.assertFalse(
            self.caminho_temporario.exists()
        )

        repositorio_usuarios_json.carregar_usuarios()

        self.assertTrue(
            self.caminho_temporario.exists()
        )

    def test_arquivo_inicial_contem_lista_vazia(
        self,
    ):
        """
        Um arquivo criado automaticamente
        deve conter uma lista JSON vazia.
        """

        repositorio_usuarios_json.carregar_usuarios()

        conteudo = (
            self.caminho_temporario.read_text(
                encoding="utf-8"
            )
        )

        dados = json.loads(
            conteudo
        )

        self.assertEqual(
            dados,
            [],
        )

    def test_carregar_usuarios_retorna_lista_vazia(
        self,
    ):
        """
        Quando nenhum usuário estiver cadastrado,
        o carregamento deve retornar uma lista vazia.
        """

        resultado = (
            repositorio_usuarios_json
            .carregar_usuarios()
        )

        self.assertEqual(
            resultado,
            [],
        )

    def test_salvar_usuarios_cria_arquivo(
        self,
    ):
        """
        O salvamento deve criar o arquivo
        quando ele ainda não existir.
        """

        usuarios = [
            {
                "codigo": 1,
                "codigo_empresa": 10,
                "nome": "Ana Souza",
                "email": "ana@empresa.com.br",
                "perfil": "ADMINISTRADOR",
                "situacao": "ATIVO",
            },
        ]

        repositorio_usuarios_json.salvar_usuarios(
            usuarios
        )

        self.assertTrue(
            self.caminho_temporario.exists()
        )

    def test_salvar_e_carregar_usuarios(
        self,
    ):
        """
        Os usuários salvos devem ser recuperados
        com a mesma estrutura e os mesmos valores.
        """

        usuarios = [
            {
                "codigo": 1,
                "codigo_empresa": 10,
                "nome": "Ana Souza",
                "email": "ana@empresa.com.br",
                "perfil": "ADMINISTRADOR",
                "situacao": "ATIVO",
            },
            {
                "codigo": 2,
                "codigo_empresa": 10,
                "nome": "Bruno Lima",
                "email": "bruno@empresa.com.br",
                "perfil": "OPERACIONAL",
                "situacao": "INATIVO",
            },
        ]

        repositorio_usuarios_json.salvar_usuarios(
            usuarios
        )

        resultado = (
            repositorio_usuarios_json
            .carregar_usuarios()
        )

        self.assertEqual(
            resultado,
            usuarios,
        )

    def test_salvar_substitui_conteudo_anterior(
        self,
    ):
        """
        Um novo salvamento deve substituir
        integralmente o conteúdo anterior.
        """

        usuarios_iniciais = [
            {
                "codigo": 1,
                "codigo_empresa": 10,
                "nome": "Ana Souza",
            },
        ]

        novos_usuarios = [
            {
                "codigo": 2,
                "codigo_empresa": 20,
                "nome": "Carlos Santos",
            },
        ]

        repositorio_usuarios_json.salvar_usuarios(
            usuarios_iniciais
        )

        repositorio_usuarios_json.salvar_usuarios(
            novos_usuarios
        )

        resultado = (
            repositorio_usuarios_json
            .carregar_usuarios()
        )

        self.assertEqual(
            resultado,
            novos_usuarios,
        )

        self.assertNotIn(
            usuarios_iniciais[0],
            resultado,
        )

    def test_preservar_caracteres_acentuados(
        self,
    ):
        """
        Caracteres acentuados devem permanecer
        legíveis no arquivo JSON.
        """

        usuarios = [
            {
                "codigo": 1,
                "codigo_empresa": 10,
                "nome": "João Araújo",
                "email": "joao@empresa.com.br",
                "perfil": "GESTOR",
                "situacao": "ATIVO",
            },
        ]

        repositorio_usuarios_json.salvar_usuarios(
            usuarios
        )

        conteudo = (
            self.caminho_temporario.read_text(
                encoding="utf-8"
            )
        )

        self.assertIn(
            "João Araújo",
            conteudo,
        )

        self.assertNotIn(
            "\\u00e3",
            conteudo,
        )

    def test_json_salvo_possui_indentacao(
        self,
    ):
        """
        O arquivo salvo deve possuir indentação
        para facilitar leitura e manutenção.
        """

        usuarios = [
            {
                "codigo": 1,
                "codigo_empresa": 10,
                "nome": "Ana Souza",
            },
        ]

        repositorio_usuarios_json.salvar_usuarios(
            usuarios
        )

        conteudo = (
            self.caminho_temporario.read_text(
                encoding="utf-8"
            )
        )

        self.assertIn(
            '\n    {',
            conteudo,
        )

        self.assertIn(
            '"codigo": 1',
            conteudo,
        )

    def test_carregar_json_invalido(
        self,
    ):
        """
        Um arquivo com JSON inválido
        deve produzir ValueError.
        """

        self.caminho_temporario.parent.mkdir(
            parents=True,
            exist_ok=True,
        )

        self.caminho_temporario.write_text(
            """
            [
                {
                    "codigo": 1,
                }
            ]
            """,
            encoding="utf-8",
        )

        with self.assertRaisesRegex(
            ValueError,
            "JSON inválido",
        ):
            (
                repositorio_usuarios_json
                .carregar_usuarios()
            )

    def test_carregar_estrutura_raiz_invalida(
        self,
    ):
        """
        A raiz do arquivo deve ser uma lista.

        Um objeto JSON contendo a chave
        'usuarios' deve ser rejeitado.
        """

        self.caminho_temporario.parent.mkdir(
            parents=True,
            exist_ok=True,
        )

        conteudo = {
            "usuarios": [],
        }

        self.caminho_temporario.write_text(
            json.dumps(
                conteudo,
                ensure_ascii=False,
                indent=4,
            ),
            encoding="utf-8",
        )

        with self.assertRaisesRegex(
            ValueError,
            "deve conter uma lista",
        ):
            (
                repositorio_usuarios_json
                .carregar_usuarios()
            )

    def test_carregar_item_invalido_na_lista(
        self,
    ):
        """
        Cada item da lista deve ser
        representado por um dicionário.
        """

        self.caminho_temporario.parent.mkdir(
            parents=True,
            exist_ok=True,
        )

        conteudo = [
            {
                "codigo": 1,
                "nome": "Ana Souza",
            },
            "item inválido",
        ]

        self.caminho_temporario.write_text(
            json.dumps(
                conteudo,
                ensure_ascii=False,
                indent=4,
            ),
            encoding="utf-8",
        )

        with self.assertRaisesRegex(
            ValueError,
            "índice 1",
        ):
            (
                repositorio_usuarios_json
                .carregar_usuarios()
            )

    def test_salvar_estrutura_raiz_invalida(
        self,
    ):
        """
        O salvamento deve rejeitar uma coleção
        que não seja uma lista.
        """

        with self.assertRaisesRegex(
            ValueError,
            "deve conter uma lista",
        ):
            repositorio_usuarios_json.salvar_usuarios(
                {
                    "usuarios": [],
                }
            )

    def test_salvar_lista_com_item_invalido(
        self,
    ):
        """
        O salvamento deve rejeitar uma lista
        contendo item que não seja dicionário.
        """

        usuarios = [
            {
                "codigo": 1,
                "nome": "Ana Souza",
            },
            123,
        ]

        with self.assertRaisesRegex(
            ValueError,
            "índice 1",
        ):
            repositorio_usuarios_json.salvar_usuarios(
                usuarios
            )

    def test_salvar_lista_vazia(
        self,
    ):
        """
        O repositório deve permitir salvar
        uma coleção vazia de Usuários.
        """

        repositorio_usuarios_json.salvar_usuarios(
            []
        )

        resultado = (
            repositorio_usuarios_json
            .carregar_usuarios()
        )

        self.assertEqual(
            resultado,
            [],
        )

    def test_carregamento_retorna_lista(
        self,
    ):
        """
        O resultado do carregamento deve
        sempre ser uma lista válida.
        """

        resultado = (
            repositorio_usuarios_json
            .carregar_usuarios()
        )

        self.assertIsInstance(
            resultado,
            list,
        )

    def test_carregamento_retorna_dicionarios(
        self,
    ):
        """
        Cada usuário carregado deve ser
        representado por um dicionário.
        """

        usuarios = [
            {
                "codigo": 1,
                "codigo_empresa": 10,
                "nome": "Ana Souza",
            },
        ]

        repositorio_usuarios_json.salvar_usuarios(
            usuarios
        )

        resultado = (
            repositorio_usuarios_json
            .carregar_usuarios()
        )

        self.assertIsInstance(
            resultado[0],
            dict,
        )

    def test_salvar_nao_altera_lista_recebida(
        self,
    ):
        """
        A função de salvamento não deve
        modificar a coleção recebida.
        """

        usuarios = [
            {
                "codigo": 1,
                "codigo_empresa": 10,
                "nome": "Ana Souza",
            },
        ]

        copia_original = [
            usuario.copy()
            for usuario in usuarios
        ]

        repositorio_usuarios_json.salvar_usuarios(
            usuarios
        )

        self.assertEqual(
            usuarios,
            copia_original,
        )


if __name__ == "__main__":
    unittest.main()