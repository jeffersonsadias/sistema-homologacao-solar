"""
Testes da interface de Usuários.

Este arquivo testa:

- leitura de códigos;
- leitura de textos obrigatórios;
- seleção de perfis;
- seleção de Empresa;
- exibição de Usuários;
- cadastro pela interface;
- busca por código;
- busca por e-mail;
- listagens;
- quantidade de Usuários;
- encaminhamento das opções do menu.

Os testes não:

- utilizam arquivos JSON reais;
- cadastram Empresas reais;
- alteram a coleção real de Usuários;
- exigem digitação manual;
- dependem do terminal real.

As entradas, saídas e chamadas externas
são simuladas com mocks.
"""

import unittest
from unittest.mock import call
from unittest.mock import patch

from app.interface import usuarios_interface


class TestLeituraCodigo(
    unittest.TestCase
):
    """
    Testes da função interna _ler_codigo().
    """

    @patch(
        "builtins.input",
        return_value="10",
    )
    def test_ler_codigo_valido(
        self,
        mock_input,
    ):
        """
        Um número inteiro positivo
        deve ser retornado normalmente.
        """

        resultado = usuarios_interface._ler_codigo(
            "Código: "
        )

        self.assertEqual(
            resultado,
            10,
        )

        mock_input.assert_called_once_with(
            "Código: "
        )

    @patch(
        "builtins.print"
    )
    @patch(
        "builtins.input",
        side_effect=[
            "texto",
            "5",
        ],
    )
    def test_repetir_quando_codigo_nao_for_inteiro(
        self,
        mock_input,
        mock_print,
    ):
        """
        Uma entrada não numérica deve ser rejeitada,
        solicitando um novo valor.
        """

        resultado = usuarios_interface._ler_codigo(
            "Código: "
        )

        self.assertEqual(
            resultado,
            5,
        )

        self.assertEqual(
            mock_input.call_count,
            2,
        )

        mock_print.assert_any_call(
            "\nDigite um número inteiro válido."
        )

    @patch(
        "builtins.print"
    )
    @patch(
        "builtins.input",
        side_effect=[
            "0",
            "-2",
            "7",
        ],
    )
    def test_repetir_quando_codigo_nao_for_positivo(
        self,
        mock_input,
        mock_print,
    ):
        """
        Zero e números negativos
        não devem ser aceitos.
        """

        resultado = usuarios_interface._ler_codigo(
            "Código: "
        )

        self.assertEqual(
            resultado,
            7,
        )

        self.assertEqual(
            mock_input.call_count,
            3,
        )

        self.assertEqual(
            mock_print.call_count,
            2,
        )

        mock_print.assert_called_with(
            "\nO código deve ser maior que zero."
        )

    @patch(
        "builtins.input",
        return_value="  12  ",
    )
    def test_ler_codigo_remove_espacos(
        self,
        mock_input,
    ):
        """
        Espaços ao redor da entrada
        devem ser removidos.
        """

        resultado = usuarios_interface._ler_codigo(
            "Código: "
        )

        self.assertEqual(
            resultado,
            12,
        )


class TestLeituraTextoObrigatorio(
    unittest.TestCase
):
    """
    Testes de _ler_texto_obrigatorio().
    """

    @patch(
        "builtins.input",
        return_value="Ana Souza",
    )
    def test_ler_texto_valido(
        self,
        mock_input,
    ):
        """
        Um texto preenchido deve ser retornado.
        """

        resultado = (
            usuarios_interface
            ._ler_texto_obrigatorio(
                "Nome: "
            )
        )

        self.assertEqual(
            resultado,
            "Ana Souza",
        )

    @patch(
        "builtins.input",
        return_value="  Ana Souza  ",
    )
    def test_ler_texto_remove_espacos_externos(
        self,
        mock_input,
    ):
        """
        Espaços externos devem ser removidos.
        """

        resultado = (
            usuarios_interface
            ._ler_texto_obrigatorio(
                "Nome: "
            )
        )

        self.assertEqual(
            resultado,
            "Ana Souza",
        )

    @patch(
        "builtins.print"
    )
    @patch(
        "builtins.input",
        side_effect=[
            "",
            "   ",
            "Ana Souza",
        ],
    )
    def test_repetir_quando_texto_estiver_vazio(
        self,
        mock_input,
        mock_print,
    ):
        """
        Entradas vazias devem ser rejeitadas.
        """

        resultado = (
            usuarios_interface
            ._ler_texto_obrigatorio(
                "Nome: "
            )
        )

        self.assertEqual(
            resultado,
            "Ana Souza",
        )

        self.assertEqual(
            mock_input.call_count,
            3,
        )

        self.assertEqual(
            mock_print.call_count,
            2,
        )


class TestSelecaoPerfil(
    unittest.TestCase
):
    """
    Testes da seleção de perfil.
    """

    @patch(
        "app.interface."
        "usuarios_interface."
        "usuarios.obter_perfis_usuario",
        return_value=(
            "ADMINISTRADOR",
            "GESTOR",
            "OPERACIONAL",
            "CONSULTA",
        ),
    )
    @patch(
        "builtins.input",
        return_value="2",
    )
    @patch(
        "builtins.print"
    )
    def test_selecionar_perfil_valido(
        self,
        mock_print,
        mock_input,
        mock_obter_perfis,
    ):
        """
        A opção numérica deve retornar
        o perfil correspondente.
        """

        resultado = (
            usuarios_interface
            ._selecionar_perfil()
        )

        self.assertEqual(
            resultado,
            "GESTOR",
        )

        mock_obter_perfis.assert_called_once_with()

    @patch(
        "app.interface."
        "usuarios_interface."
        "usuarios.obter_perfis_usuario",
        return_value=(
            "ADMINISTRADOR",
            "GESTOR",
        ),
    )
    @patch(
        "builtins.input",
        side_effect=[
            "texto",
            "1",
        ],
    )
    @patch(
        "builtins.print"
    )
    def test_repetir_quando_opcao_nao_for_numerica(
        self,
        mock_print,
        mock_input,
        mock_obter_perfis,
    ):
        """
        Uma opção textual deve ser rejeitada.
        """

        resultado = (
            usuarios_interface
            ._selecionar_perfil()
        )

        self.assertEqual(
            resultado,
            "ADMINISTRADOR",
        )

        mock_print.assert_any_call(
            "\nDigite o número correspondente "
            "ao perfil."
        )

    @patch(
        "app.interface."
        "usuarios_interface."
        "usuarios.obter_perfis_usuario",
        return_value=(
            "ADMINISTRADOR",
            "GESTOR",
        ),
    )
    @patch(
        "builtins.input",
        side_effect=[
            "0",
            "3",
            "2",
        ],
    )
    @patch(
        "builtins.print"
    )
    def test_repetir_quando_opcao_estiver_fora_da_lista(
        self,
        mock_print,
        mock_input,
        mock_obter_perfis,
    ):
        """
        Opções fora da faixa disponível
        devem ser rejeitadas.
        """

        resultado = (
            usuarios_interface
            ._selecionar_perfil()
        )

        self.assertEqual(
            resultado,
            "GESTOR",
        )

        self.assertEqual(
            mock_input.call_count,
            3,
        )

        mock_print.assert_any_call(
            "\nOpção de perfil inválida."
        )


class TestSelecaoEmpresa(
    unittest.TestCase
):
    """
    Testes da seleção de Empresa.
    """

    @patch(
        "app.interface."
        "usuarios_interface."
        "empresas.obter_empresa"
    )
    @patch(
        "app.interface."
        "usuarios_interface."
        "_ler_codigo",
        return_value=10,
    )
    def test_selecionar_empresa(
        self,
        mock_ler_codigo,
        mock_obter_empresa,
    ):
        """
        A interface deve solicitar o código
        e delegar a busca à fachada de Empresas.
        """

        empresa = {
            "codigo": 10,
            "nome_fantasia": "Empresa Solar",
            "situacao": "ATIVA",
        }

        mock_obter_empresa.return_value = empresa

        resultado = (
            usuarios_interface
            ._selecionar_empresa()
        )

        self.assertIs(
            resultado,
            empresa,
        )

        mock_ler_codigo.assert_called_once_with(
            "Código da Empresa: "
        )

        mock_obter_empresa.assert_called_once_with(
            10
        )


class TestExibicaoUsuarios(
    unittest.TestCase
):
    """
    Testes das funções de apresentação.
    """

    def setUp(
        self,
    ):
        """
        Cria um Usuário controlado.
        """

        self.usuario = {
            "codigo": 1,
            "codigo_empresa": 10,
            "nome": "Ana Souza",
            "email": "ana@empresa.com.br",
            "perfil": "GESTOR",
            "situacao": "ATIVO",
            "data_cadastro": "2026-07-28T10:00:00",
            "data_atualizacao": "2026-07-28T10:00:00",
        }

    @patch(
        "builtins.print"
    )
    def test_exibir_usuario(
        self,
        mock_print,
    ):
        """
        Todos os principais dados do Usuário
        devem ser enviados para exibição.
        """

        usuarios_interface._exibir_usuario(
            self.usuario
        )

        mock_print.assert_any_call(
            "Código: 1"
        )

        mock_print.assert_any_call(
            "Código da Empresa: 10"
        )

        mock_print.assert_any_call(
            "Nome: Ana Souza"
        )

        mock_print.assert_any_call(
            "E-mail: ana@empresa.com.br"
        )

        mock_print.assert_any_call(
            "Perfil: GESTOR"
        )

        mock_print.assert_any_call(
            "Situação: ATIVO"
        )

    @patch(
        "builtins.print"
    )
    def test_exibir_lista_vazia(
        self,
        mock_print,
    ):
        """
        Uma lista vazia deve apresentar
        mensagem apropriada.
        """

        usuarios_interface._exibir_lista_usuarios(
            []
        )

        mock_print.assert_called_once_with(
            "\nNenhum Usuário encontrado."
        )

    @patch(
        "app.interface."
        "usuarios_interface."
        "_exibir_usuario"
    )
    @patch(
        "builtins.print"
    )
    def test_exibir_lista_usuarios(
        self,
        mock_print,
        mock_exibir_usuario,
    ):
        """
        Cada Usuário da lista deve ser exibido.
        """

        segundo_usuario = {
            **self.usuario,
            "codigo": 2,
            "nome": "Bruno Lima",
        }

        lista = [
            self.usuario,
            segundo_usuario,
        ]

        usuarios_interface._exibir_lista_usuarios(
            lista
        )

        mock_print.assert_any_call(
            "\nQuantidade de Usuários: 2"
        )

        self.assertEqual(
            mock_exibir_usuario.call_count,
            2,
        )

        mock_exibir_usuario.assert_has_calls(
            [
                call(self.usuario),
                call(segundo_usuario),
            ]
        )


class TestCadastroUsuarioInterface(
    unittest.TestCase
):
    """
    Testes do fluxo de cadastro.
    """

    def setUp(
        self,
    ):
        """
        Cria dados simulados.
        """

        self.empresa = {
            "codigo": 10,
            "nome_fantasia": "Empresa Solar",
            "situacao": "ATIVA",
        }

        self.usuario = {
            "codigo": 1,
            "codigo_empresa": 10,
            "nome": "Ana Souza",
            "email": "ana@empresa.com.br",
            "perfil": "GESTOR",
            "situacao": "ATIVO",
        }

    @patch(
        "app.interface."
        "usuarios_interface."
        "_exibir_usuario"
    )
    @patch(
        "app.interface."
        "usuarios_interface."
        "usuarios.cadastrar_usuario"
    )
    @patch(
        "app.interface."
        "usuarios_interface."
        "_selecionar_perfil",
        return_value="GESTOR",
    )
    @patch(
        "app.interface."
        "usuarios_interface."
        "_ler_texto_obrigatorio",
        side_effect=[
            "Ana Souza",
            "ana@empresa.com.br",
        ],
    )
    @patch(
        "app.interface."
        "usuarios_interface."
        "_exibir_empresa_selecionada"
    )
    @patch(
        "app.interface."
        "usuarios_interface."
        "_selecionar_empresa"
    )
    @patch(
        "builtins.print"
    )
    def test_cadastrar_usuario_com_sucesso(
        self,
        mock_print,
        mock_selecionar_empresa,
        mock_exibir_empresa,
        mock_ler_texto,
        mock_selecionar_perfil,
        mock_cadastrar_usuario,
        mock_exibir_usuario,
    ):
        """
        A interface deve coletar os dados
        e chamar corretamente a fachada.
        """

        mock_selecionar_empresa.return_value = (
            self.empresa
        )

        mock_cadastrar_usuario.return_value = (
            self.usuario
        )

        (
            usuarios_interface
            .cadastrar_usuario_interface()
        )

        mock_cadastrar_usuario.assert_called_once_with(
            codigo_empresa=10,
            nome="Ana Souza",
            email="ana@empresa.com.br",
            perfil="GESTOR",
        )

        mock_exibir_usuario.assert_called_once_with(
            self.usuario
        )

        mock_print.assert_any_call(
            "\nUsuário cadastrado com sucesso."
        )

    @patch(
        "app.interface."
        "usuarios_interface."
        "_exibir_usuario"
    )
    @patch(
        "app.interface."
        "usuarios_interface."
        "_selecionar_empresa",
        side_effect=ValueError(
            "Empresa não encontrada."
        ),
    )
    @patch(
        "builtins.print"
    )
    def test_cadastro_trata_empresa_inexistente(
        self,
        mock_print,
        mock_selecionar_empresa,
        mock_exibir_usuario,
    ):
        """
        Erros da fachada devem ser apresentados
        sem interromper o programa.
        """

        (
            usuarios_interface
            .cadastrar_usuario_interface()
        )

        mock_print.assert_any_call(
            "\nNão foi possível cadastrar "
            "o Usuário: Empresa não encontrada."
        )

        mock_exibir_usuario.assert_not_called()


class TestBuscaUsuarioInterface(
    unittest.TestCase
):
    """
    Testes dos fluxos de busca.
    """

    def setUp(
        self,
    ):
        """
        Prepara os dados controlados.
        """

        self.empresa = {
            "codigo": 10,
            "nome_fantasia": "Empresa Solar",
            "situacao": "ATIVA",
        }

        self.usuario = {
            "codigo": 1,
            "codigo_empresa": 10,
            "nome": "Ana Souza",
            "email": "ana@empresa.com.br",
            "perfil": "GESTOR",
            "situacao": "ATIVO",
        }

    @patch(
        "app.interface."
        "usuarios_interface."
        "_exibir_usuario"
    )
    @patch(
        "app.interface."
        "usuarios_interface."
        "usuarios.obter_usuario"
    )
    @patch(
        "app.interface."
        "usuarios_interface."
        "_ler_codigo",
        return_value=1,
    )
    @patch(
        "app.interface."
        "usuarios_interface."
        "_exibir_empresa_selecionada"
    )
    @patch(
        "app.interface."
        "usuarios_interface."
        "_selecionar_empresa"
    )
    @patch(
        "builtins.print"
    )
    def test_buscar_usuario_encontrado(
        self,
        mock_print,
        mock_selecionar_empresa,
        mock_exibir_empresa,
        mock_ler_codigo,
        mock_obter_usuario,
        mock_exibir_usuario,
    ):
        """
        Um Usuário encontrado deve ser exibido.
        """

        mock_selecionar_empresa.return_value = (
            self.empresa
        )

        mock_obter_usuario.return_value = (
            self.usuario
        )

        usuarios_interface.buscar_usuario_interface()

        mock_obter_usuario.assert_called_once_with(
            codigo_usuario=1,
            codigo_empresa=10,
        )

        mock_exibir_usuario.assert_called_once_with(
            self.usuario
        )

    @patch(
        "app.interface."
        "usuarios_interface."
        "_exibir_usuario"
    )
    @patch(
        "app.interface."
        "usuarios_interface."
        "usuarios.obter_usuario",
        return_value=None,
    )
    @patch(
        "app.interface."
        "usuarios_interface."
        "_ler_codigo",
        return_value=999,
    )
    @patch(
        "app.interface."
        "usuarios_interface."
        "_exibir_empresa_selecionada"
    )
    @patch(
        "app.interface."
        "usuarios_interface."
        "_selecionar_empresa"
    )
    @patch(
        "builtins.print"
    )
    def test_buscar_usuario_nao_encontrado(
        self,
        mock_print,
        mock_selecionar_empresa,
        mock_exibir_empresa,
        mock_ler_codigo,
        mock_obter_usuario,
        mock_exibir_usuario,
    ):
        """
        Uma busca sem resultado deve apresentar
        mensagem apropriada.
        """

        mock_selecionar_empresa.return_value = (
            self.empresa
        )

        usuarios_interface.buscar_usuario_interface()

        mock_print.assert_any_call(
            "\nUsuário não encontrado nesta Empresa."
        )

        mock_exibir_usuario.assert_not_called()

    @patch(
        "app.interface."
        "usuarios_interface."
        "_exibir_usuario"
    )
    @patch(
        "app.interface."
        "usuarios_interface."
        "usuarios.buscar_usuario_por_email"
    )
    @patch(
        "app.interface."
        "usuarios_interface."
        "_ler_texto_obrigatorio",
        return_value="ana@empresa.com.br",
    )
    @patch(
        "builtins.print"
    )
    def test_buscar_usuario_por_email(
        self,
        mock_print,
        mock_ler_texto,
        mock_buscar_email,
        mock_exibir_usuario,
    ):
        """
        A interface deve encaminhar
        corretamente a busca por e-mail.
        """

        mock_buscar_email.return_value = (
            self.usuario
        )

        (
            usuarios_interface
            .buscar_usuario_por_email_interface()
        )

        mock_buscar_email.assert_called_once_with(
            "ana@empresa.com.br"
        )

        mock_exibir_usuario.assert_called_once_with(
            self.usuario
        )


class TestListagensUsuariosInterface(
    unittest.TestCase
):
    """
    Testes das listagens da interface.
    """

    def setUp(
        self,
    ):
        """
        Prepara Empresa e Usuário simulados.
        """

        self.empresa = {
            "codigo": 10,
            "nome_fantasia": "Empresa Solar",
            "situacao": "ATIVA",
        }

        self.lista_usuarios = [
            {
                "codigo": 1,
                "codigo_empresa": 10,
                "nome": "Ana Souza",
                "email": "ana@empresa.com.br",
                "perfil": "GESTOR",
                "situacao": "ATIVO",
            },
        ]

    @patch(
        "app.interface."
        "usuarios_interface."
        "_exibir_lista_usuarios"
    )
    @patch(
        "app.interface."
        "usuarios_interface."
        "usuarios.listar_usuarios"
    )
    @patch(
        "app.interface."
        "usuarios_interface."
        "_exibir_empresa_selecionada"
    )
    @patch(
        "app.interface."
        "usuarios_interface."
        "_selecionar_empresa"
    )
    @patch(
        "builtins.print"
    )
    def test_listar_todos_os_usuarios(
        self,
        mock_print,
        mock_selecionar_empresa,
        mock_exibir_empresa,
        mock_listar_usuarios,
        mock_exibir_lista,
    ):
        """
        A listagem geral deve chamar
        a fachada com a Empresa selecionada.
        """

        mock_selecionar_empresa.return_value = (
            self.empresa
        )

        mock_listar_usuarios.return_value = (
            self.lista_usuarios
        )

        usuarios_interface.listar_usuarios_interface()

        mock_listar_usuarios.assert_called_once_with(
            codigo_empresa=10
        )

        mock_exibir_lista.assert_called_once_with(
            self.lista_usuarios
        )

    @patch(
        "app.interface."
        "usuarios_interface."
        "_exibir_lista_usuarios"
    )
    @patch(
        "app.interface."
        "usuarios_interface."
        "usuarios.listar_usuarios_ativos"
    )
    @patch(
        "app.interface."
        "usuarios_interface."
        "_exibir_empresa_selecionada"
    )
    @patch(
        "app.interface."
        "usuarios_interface."
        "_selecionar_empresa"
    )
    @patch(
        "builtins.print"
    )
    def test_listar_usuarios_ativos(
        self,
        mock_print,
        mock_selecionar_empresa,
        mock_exibir_empresa,
        mock_listar_ativos,
        mock_exibir_lista,
    ):
        """
        A listagem de ativos deve chamar
        a função pública correspondente.
        """

        mock_selecionar_empresa.return_value = (
            self.empresa
        )

        mock_listar_ativos.return_value = (
            self.lista_usuarios
        )

        (
            usuarios_interface
            .listar_usuarios_ativos_interface()
        )

        mock_listar_ativos.assert_called_once_with(
            codigo_empresa=10
        )

        mock_exibir_lista.assert_called_once_with(
            self.lista_usuarios
        )

    @patch(
        "app.interface."
        "usuarios_interface."
        "_exibir_lista_usuarios"
    )
    @patch(
        "app.interface."
        "usuarios_interface."
        "usuarios.listar_usuarios_por_perfil"
    )
    @patch(
        "app.interface."
        "usuarios_interface."
        "_selecionar_perfil",
        return_value="GESTOR",
    )
    @patch(
        "app.interface."
        "usuarios_interface."
        "_exibir_empresa_selecionada"
    )
    @patch(
        "app.interface."
        "usuarios_interface."
        "_selecionar_empresa"
    )
    @patch(
        "builtins.print"
    )
    def test_listar_usuarios_por_perfil(
        self,
        mock_print,
        mock_selecionar_empresa,
        mock_exibir_empresa,
        mock_selecionar_perfil,
        mock_listar_por_perfil,
        mock_exibir_lista,
    ):
        """
        A interface deve encaminhar
        Empresa e perfil para a fachada.
        """

        mock_selecionar_empresa.return_value = (
            self.empresa
        )

        mock_listar_por_perfil.return_value = (
            self.lista_usuarios
        )

        (
            usuarios_interface
            .listar_usuarios_por_perfil_interface()
        )

        (
            mock_listar_por_perfil
            .assert_called_once_with(
                codigo_empresa=10,
                perfil="GESTOR",
            )
        )

        mock_exibir_lista.assert_called_once_with(
            self.lista_usuarios
        )


class TestQuantidadeUsuariosInterface(
    unittest.TestCase
):
    """
    Testes da consulta de quantidade.
    """

    @patch(
        "app.interface."
        "usuarios_interface."
        "usuarios.quantidade_usuarios",
        return_value=3,
    )
    @patch(
        "app.interface."
        "usuarios_interface."
        "_exibir_empresa_selecionada"
    )
    @patch(
        "app.interface."
        "usuarios_interface."
        "_selecionar_empresa"
    )
    @patch(
        "builtins.print"
    )
    def test_mostrar_quantidade_usuarios(
        self,
        mock_print,
        mock_selecionar_empresa,
        mock_exibir_empresa,
        mock_quantidade,
    ):
        """
        A quantidade retornada pela fachada
        deve ser apresentada ao operador.
        """

        empresa = {
            "codigo": 10,
            "nome_fantasia": "Empresa Solar",
            "situacao": "ATIVA",
        }

        mock_selecionar_empresa.return_value = empresa

        (
            usuarios_interface
            .mostrar_quantidade_usuarios_interface()
        )

        mock_quantidade.assert_called_once_with(
            codigo_empresa=10
        )

        mock_print.assert_any_call(
            "\nA Empresa possui "
            "3 Usuário(s) cadastrado(s)."
        )


class TestMenuUsuarios(
    unittest.TestCase
):
    """
    Testes do encaminhamento do menu.
    """

    @patch(
        "app.interface."
        "usuarios_interface."
        "_pausar"
    )
    @patch(
        "app.interface."
        "usuarios_interface."
        "cadastrar_usuario_interface"
    )
    @patch(
        "builtins.input",
        side_effect=[
            "1",
            "0",
        ],
    )
    @patch(
        "builtins.print"
    )
    def test_menu_encaminha_cadastro(
        self,
        mock_print,
        mock_input,
        mock_cadastrar,
        mock_pausar,
    ):
        """
        A opção 1 deve abrir
        o cadastro de Usuário.
        """

        usuarios_interface.menu_usuarios()

        mock_cadastrar.assert_called_once_with()

        mock_pausar.assert_called_once_with()

    @patch(
        "app.interface."
        "usuarios_interface."
        "_pausar"
    )
    @patch(
        "app.interface."
        "usuarios_interface."
        "listar_usuarios_interface"
    )
    @patch(
        "builtins.input",
        side_effect=[
            "4",
            "0",
        ],
    )
    @patch(
        "builtins.print"
    )
    def test_menu_encaminha_listagem(
        self,
        mock_print,
        mock_input,
        mock_listar,
        mock_pausar,
    ):
        """
        A opção 4 deve abrir
        a listagem geral.
        """

        usuarios_interface.menu_usuarios()

        mock_listar.assert_called_once_with()

        mock_pausar.assert_called_once_with()

    @patch(
        "builtins.input",
        return_value="0",
    )
    @patch(
        "builtins.print"
    )
    def test_menu_retorna_com_opcao_zero(
        self,
        mock_print,
        mock_input,
    ):
        """
        A opção zero deve encerrar
        somente o menu de Usuários.
        """

        resultado = usuarios_interface.menu_usuarios()

        self.assertIsNone(
            resultado
        )

        mock_input.assert_called_once_with(
            "\nEscolha uma opção: "
        )

    @patch(
        "builtins.input",
        side_effect=[
            "99",
            "0",
        ],
    )
    @patch(
        "builtins.print"
    )
    def test_menu_rejeita_opcao_invalida(
        self,
        mock_print,
        mock_input,
    ):
        """
        Uma opção inválida deve apresentar
        mensagem e manter o menu em execução.
        """

        usuarios_interface.menu_usuarios()

        mock_print.assert_any_call(
            "\nOpção inválida."
        )

        self.assertEqual(
            mock_input.call_count,
            2,
        )


    @patch(
        "app.interface."
        "usuarios_interface."
        "_pausar"
    )
    @patch(
        "app.interface."
        "usuarios_interface."
        "ativar_usuario_interface"
    )
    @patch(
        "builtins.input",
        side_effect=[
            "8",
            "0",
        ],
    )
    @patch(
        "builtins.print"
    )
    def test_menu_encaminha_ativacao(
        self,
        mock_print,
        mock_input,
        mock_ativar,
        mock_pausar,
    ):
        """
        A opção 8 deve abrir
        a ativação de Usuário.
        """

        usuarios_interface.menu_usuarios()

        mock_ativar.assert_called_once_with()
        mock_pausar.assert_called_once_with()

    @patch(
        "app.interface."
        "usuarios_interface."
        "_pausar"
    )
    @patch(
        "app.interface."
        "usuarios_interface."
        "inativar_usuario_interface"
    )
    @patch(
        "builtins.input",
        side_effect=[
            "9",
            "0",
        ],
    )
    @patch(
        "builtins.print"
    )
    def test_menu_encaminha_inativacao(
        self,
        mock_print,
        mock_input,
        mock_inativar,
        mock_pausar,
    ):
        """
        A opção 9 deve abrir
        a inativação de Usuário.
        """

        usuarios_interface.menu_usuarios()

        mock_inativar.assert_called_once_with()
        mock_pausar.assert_called_once_with()

    @patch(
        "app.interface."
        "usuarios_interface."
        "_pausar"
    )
    @patch(
        "app.interface."
        "usuarios_interface."
        "bloquear_usuario_interface"
    )
    @patch(
        "builtins.input",
        side_effect=[
            "10",
            "0",
        ],
    )
    @patch(
        "builtins.print"
    )
    def test_menu_encaminha_bloqueio(
        self,
        mock_print,
        mock_input,
        mock_bloquear,
        mock_pausar,
    ):
        """
        A opção 10 deve abrir
        o bloqueio de Usuário.
        """

        usuarios_interface.menu_usuarios()

        mock_bloquear.assert_called_once_with()
        mock_pausar.assert_called_once_with()

    @patch(
        "app.interface."
        "usuarios_interface."
        "_pausar"
    )
    @patch(
        "app.interface."
        "usuarios_interface."
        "cancelar_usuario_interface"
    )
    @patch(
        "builtins.input",
        side_effect=[
            "11",
            "0",
        ],
    )
    @patch(
        "builtins.print"
    )
    def test_menu_encaminha_cancelamento(
        self,
        mock_print,
        mock_input,
        mock_cancelar,
        mock_pausar,
    ):
        """
        A opção 11 deve abrir
        o cancelamento de Usuário.
        """

        usuarios_interface.menu_usuarios()

        mock_cancelar.assert_called_once_with()
        mock_pausar.assert_called_once_with()


class TestAlteracaoSituacaoUsuarioInterface(
    unittest.TestCase
):
    """
    Testes das operações de alteração
    de situação pela interface.
    """

    @patch(
        "app.interface.usuarios_interface."
        "_exibir_usuario"
    )
    @patch(
        "app.interface.usuarios_interface."
        "_ler_codigo",
        return_value=5,
    )
    @patch(
        "app.interface.usuarios_interface."
        "_exibir_empresa_selecionada"
    )
    @patch(
        "app.interface.usuarios_interface."
        "_selecionar_empresa"
    )
    @patch(
        "app.interface.usuarios_interface."
        "usuarios.ativar_usuario"
    )
    def test_ativar_usuario_interface(
        self,
        mock_ativar_usuario,
        mock_selecionar_empresa,
        mock_exibir_empresa,
        mock_ler_codigo,
        mock_exibir_usuario,
    ):
        """
        A interface deve selecionar a Empresa,
        ler o código e chamar a fachada.
        """

        empresa = {
            "codigo": 10,
            "nome_fantasia": "Empresa Solar",
        }

        usuario_atualizado = {
            "codigo": 5,
            "codigo_empresa": 10,
            "nome": "Ana Souza",
            "situacao": "ATIVO",
        }

        mock_selecionar_empresa.return_value = empresa
        mock_ativar_usuario.return_value = (
            usuario_atualizado
        )

        usuarios_interface.ativar_usuario_interface()

        mock_selecionar_empresa.assert_called_once_with()

        mock_exibir_empresa.assert_called_once_with(
            empresa
        )

        mock_ler_codigo.assert_called_once_with(
            "\nCódigo do Usuário: "
        )

        mock_ativar_usuario.assert_called_once_with(
            codigo_empresa=10,
            codigo_usuario=5,
        )

        mock_exibir_usuario.assert_called_once_with(
            usuario_atualizado
        )

    @patch(
        "app.interface.usuarios_interface."
        "_exibir_usuario"
    )
    @patch(
        "app.interface.usuarios_interface."
        "_ler_codigo",
        return_value=5,
    )
    @patch(
        "app.interface.usuarios_interface."
        "_exibir_empresa_selecionada"
    )
    @patch(
        "app.interface.usuarios_interface."
        "_selecionar_empresa"
    )
    @patch(
        "app.interface.usuarios_interface."
        "usuarios.inativar_usuario"
    )
    def test_inativar_usuario_interface(
        self,
        mock_inativar_usuario,
        mock_selecionar_empresa,
        mock_exibir_empresa,
        mock_ler_codigo,
        mock_exibir_usuario,
    ):
        """
        A interface deve chamar a operação
        semântica de inativação.
        """

        empresa = {
            "codigo": 10,
            "nome_fantasia": "Empresa Solar",
        }

        usuario_atualizado = {
            "codigo": 5,
            "codigo_empresa": 10,
            "situacao": "INATIVO",
        }

        mock_selecionar_empresa.return_value = empresa
        mock_inativar_usuario.return_value = (
            usuario_atualizado
        )

        usuarios_interface.inativar_usuario_interface()

        mock_inativar_usuario.assert_called_once_with(
            codigo_empresa=10,
            codigo_usuario=5,
        )

        mock_exibir_usuario.assert_called_once_with(
            usuario_atualizado
        )

    @patch(
        "app.interface.usuarios_interface."
        "_exibir_usuario"
    )
    @patch(
        "app.interface.usuarios_interface."
        "_ler_codigo",
        return_value=5,
    )
    @patch(
        "app.interface.usuarios_interface."
        "_exibir_empresa_selecionada"
    )
    @patch(
        "app.interface.usuarios_interface."
        "_selecionar_empresa"
    )
    @patch(
        "app.interface.usuarios_interface."
        "usuarios.bloquear_usuario"
    )
    def test_bloquear_usuario_interface(
        self,
        mock_bloquear_usuario,
        mock_selecionar_empresa,
        mock_exibir_empresa,
        mock_ler_codigo,
        mock_exibir_usuario,
    ):
        """
        A interface deve chamar a operação
        semântica de bloqueio.
        """

        empresa = {
            "codigo": 10,
            "nome_fantasia": "Empresa Solar",
        }

        usuario_atualizado = {
            "codigo": 5,
            "codigo_empresa": 10,
            "situacao": "BLOQUEADO",
        }

        mock_selecionar_empresa.return_value = empresa
        mock_bloquear_usuario.return_value = (
            usuario_atualizado
        )

        usuarios_interface.bloquear_usuario_interface()

        mock_bloquear_usuario.assert_called_once_with(
            codigo_empresa=10,
            codigo_usuario=5,
        )

        mock_exibir_usuario.assert_called_once_with(
            usuario_atualizado
        )

    @patch(
        "app.interface.usuarios_interface."
        "_exibir_usuario"
    )
    @patch(
        "app.interface.usuarios_interface."
        "_ler_codigo",
        return_value=5,
    )
    @patch(
        "app.interface.usuarios_interface."
        "_exibir_empresa_selecionada"
    )
    @patch(
        "app.interface.usuarios_interface."
        "_selecionar_empresa"
    )
    @patch(
        "app.interface.usuarios_interface."
        "usuarios.cancelar_usuario"
    )
    def test_cancelar_usuario_interface(
        self,
        mock_cancelar_usuario,
        mock_selecionar_empresa,
        mock_exibir_empresa,
        mock_ler_codigo,
        mock_exibir_usuario,
    ):
        """
        A interface deve chamar a operação
        semântica de cancelamento.
        """

        empresa = {
            "codigo": 10,
            "nome_fantasia": "Empresa Solar",
        }

        usuario_atualizado = {
            "codigo": 5,
            "codigo_empresa": 10,
            "situacao": "CANCELADO",
        }

        mock_selecionar_empresa.return_value = empresa
        mock_cancelar_usuario.return_value = (
            usuario_atualizado
        )

        usuarios_interface.cancelar_usuario_interface()

        mock_cancelar_usuario.assert_called_once_with(
            codigo_empresa=10,
            codigo_usuario=5,
        )

        mock_exibir_usuario.assert_called_once_with(
            usuario_atualizado
        )

    @patch(
        "app.interface.usuarios_interface."
        "_exibir_usuario"
    )
    @patch(
        "app.interface.usuarios_interface."
        "_ler_codigo",
        return_value=5,
    )
    @patch(
        "app.interface.usuarios_interface."
        "_exibir_empresa_selecionada"
    )
    @patch(
        "app.interface.usuarios_interface."
        "_selecionar_empresa"
    )
    @patch(
        "app.interface.usuarios_interface."
        "usuarios.ativar_usuario",
        side_effect=ValueError(
            "Transição de situação não permitida."
        ),
    )
    @patch(
        "builtins.print"
    )
    def test_exibir_erro_ao_ativar_usuario(
        self,
        mock_print,
        mock_ativar_usuario,
        mock_selecionar_empresa,
        mock_exibir_empresa,
        mock_ler_codigo,
        mock_exibir_usuario,
    ):
        """
        Erros da fachada devem ser apresentados
        ao operador e interromper o fluxo.
        """

        mock_selecionar_empresa.return_value = {
            "codigo": 10,
            "nome_fantasia": "Empresa Solar",
        }

        usuarios_interface.ativar_usuario_interface()

        mock_exibir_usuario.assert_not_called()

        mensagens = [
            chamada.args[0]
            for chamada in mock_print.call_args_list
            if chamada.args
        ]

        self.assertTrue(
            any(
                "Não foi possível ativar o Usuário"
                in mensagem
                for mensagem in mensagens
            )
        )

        self.assertTrue(
            any(
                "Transição de situação não permitida"
                in mensagem
                for mensagem in mensagens
            )
        )

    @patch(
        "app.interface.usuarios_interface."
        "_exibir_usuario"
    )
    @patch(
        "app.interface.usuarios_interface."
        "_ler_codigo"
    )
    @patch(
        "app.interface.usuarios_interface."
        "_exibir_empresa_selecionada"
    )
    @patch(
        "app.interface.usuarios_interface."
        "_selecionar_empresa",
        side_effect=ValueError(
            "Nenhuma Empresa ativa encontrada."
        ),
    )
    @patch(
        "app.interface.usuarios_interface."
        "usuarios.bloquear_usuario"
    )
    @patch(
        "builtins.print"
    )
    def test_interromper_fluxo_quando_empresa_for_invalida(
        self,
        mock_print,
        mock_bloquear_usuario,
        mock_selecionar_empresa,
        mock_exibir_empresa,
        mock_ler_codigo,
        mock_exibir_usuario,
    ):
        """
        Se a seleção da Empresa falhar,
        nenhuma operação posterior deve ocorrer.
        """

        usuarios_interface.bloquear_usuario_interface()

        mock_ler_codigo.assert_not_called()
        mock_bloquear_usuario.assert_not_called()
        mock_exibir_usuario.assert_not_called()

        mensagens = [
            chamada.args[0]
            for chamada in mock_print.call_args_list
            if chamada.args
        ]

        self.assertTrue(
            any(
                "Nenhuma Empresa ativa encontrada"
                in mensagem
                for mensagem in mensagens
            )
        )

    @patch(
        "app.interface.usuarios_interface."
        "_selecionar_empresa"
    )
    def test_rejeitar_operacao_interna_invalida(
        self,
        mock_selecionar_empresa,
    ):
        """
        A função interna deve rejeitar
        operações que não estejam previstas.
        """

        mock_selecionar_empresa.return_value = {
            "codigo": 10,
            "nome_fantasia": "Empresa Solar",
        }

        with patch(
            "app.interface.usuarios_interface."
            "_exibir_empresa_selecionada"
        ), patch(
            "app.interface.usuarios_interface."
            "_ler_codigo",
            return_value=5,
        ), patch(
            "builtins.print"
        ) as mock_print:
            usuarios_interface \
                ._alterar_situacao_usuario_interface(
                    "SUSPENDER"
                )

        mensagens = [
            chamada.args[0]
            for chamada in mock_print.call_args_list
            if chamada.args
        ]

        self.assertTrue(
            any(
                "Operação de situação inválida"
                in mensagem
                for mensagem in mensagens
            )
        )

if __name__ == "__main__":
    unittest.main()