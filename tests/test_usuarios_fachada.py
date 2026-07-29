"""
Testes da fachada de Usuários.

Este arquivo testa:

- carregamento e manipulação da coleção em memória;
- geração de códigos;
- cadastro de Usuários;
- validação da Empresa;
- bloqueio de cadastro em Empresa inativa;
- unicidade global do e-mail;
- salvamento após cadastro;
- buscas por código e e-mail;
- isolamento entre Empresas;
- listagem por Empresa;
- listagem de Usuários ativos;
- listagem por perfil;
- quantidade de Usuários;
- consultas de situação e perfil;
- exposição pública de perfis e situações.

Os testes não utilizam o arquivo real:

    data/usuarios.json

A coleção da fachada é substituída temporariamente
e as dependências externas são simuladas com mocks.
"""

import unittest
from unittest.mock import patch

from app import usuarios
from app.dominio import usuarios as usuarios_dominio


class TestGeracaoCodigoUsuario(
    unittest.TestCase
):
    """
    Testes da geração interna
    de códigos de Usuário.
    """

    def setUp(
        self,
    ):
        """
        Guarda a coleção real e substitui
        por uma lista controlada.
        """

        self.usuarios_originais = usuarios.usuarios

        usuarios.usuarios = []

    def tearDown(
        self,
    ):
        """
        Restaura a coleção original.
        """

        usuarios.usuarios = (
            self.usuarios_originais
        )

    def test_primeiro_codigo_deve_ser_um(
        self,
    ):
        """
        Uma coleção vazia deve gerar código 1.
        """

        resultado = usuarios._gerar_proximo_codigo()

        self.assertEqual(
            resultado,
            1,
        )

    def test_proximo_codigo_deve_ser_maior_codigo_mais_um(
        self,
    ):
        """
        O próximo código deve considerar
        o maior código existente.
        """

        usuarios.usuarios = [
            {
                "codigo": 1,
            },
            {
                "codigo": 3,
            },
            {
                "codigo": 7,
            },
        ]

        resultado = usuarios._gerar_proximo_codigo()

        self.assertEqual(
            resultado,
            8,
        )

    def test_geracao_nao_utiliza_quantidade_de_itens(
        self,
    ):
        """
        A geração não deve utilizar len() + 1,
        pois podem existir lacunas nos códigos.
        """

        usuarios.usuarios = [
            {
                "codigo": 2,
            },
            {
                "codigo": 10,
            },
        ]

        resultado = usuarios._gerar_proximo_codigo()

        self.assertEqual(
            resultado,
            11,
        )

    def test_ignorar_codigo_booleano(
        self,
    ):
        """
        Booleanos não devem ser considerados
        códigos numéricos válidos.
        """

        usuarios.usuarios = [
            {
                "codigo": True,
            },
        ]

        resultado = usuarios._gerar_proximo_codigo()

        self.assertEqual(
            resultado,
            1,
        )

    def test_ignorar_codigo_textual(
        self,
    ):
        """
        Códigos em formato de texto
        devem ser ignorados.
        """

        usuarios.usuarios = [
            {
                "codigo": "10",
            },
        ]

        resultado = usuarios._gerar_proximo_codigo()

        self.assertEqual(
            resultado,
            1,
        )

    def test_ignorar_codigo_zero_ou_negativo(
        self,
    ):
        """
        Apenas códigos positivos
        devem ser considerados.
        """

        usuarios.usuarios = [
            {
                "codigo": 0,
            },
            {
                "codigo": -5,
            },
        ]

        resultado = usuarios._gerar_proximo_codigo()

        self.assertEqual(
            resultado,
            1,
        )

    def test_ignorar_item_que_nao_seja_dicionario(
        self,
    ):
        """
        Itens inválidos na coleção
        devem ser ignorados.
        """

        usuarios.usuarios = [
            "item inválido",
            {
                "codigo": 4,
            },
        ]

        resultado = usuarios._gerar_proximo_codigo()

        self.assertEqual(
            resultado,
            5,
        )


class TestCadastroUsuario(
    unittest.TestCase
):
    """
    Testes do cadastro de Usuários.
    """

    def setUp(
        self,
    ):
        """
        Guarda a coleção real e utiliza
        uma lista vazia controlada.
        """

        self.usuarios_originais = usuarios.usuarios

        usuarios.usuarios = []

        self.empresa_ativa = {
            "codigo": 10,
            "razao_social": "Empresa Solar Ltda.",
            "nome_fantasia": "Empresa Solar",
            "situacao": "ATIVA",
        }

    def tearDown(
        self,
    ):
        """
        Restaura a coleção original.
        """

        usuarios.usuarios = (
            self.usuarios_originais
        )

    @patch(
        "app.usuarios.salvar_usuarios"
    )
    @patch(
        "app.usuarios."
        "empresas.empresa_esta_ativa",
        return_value=True,
    )
    @patch(
        "app.usuarios."
        "empresas.obter_empresa"
    )
    def test_cadastrar_usuario_valido(
        self,
        mock_obter_empresa,
        mock_empresa_esta_ativa,
        mock_salvar_usuarios,
    ):
        """
        Deve cadastrar um Usuário válido,
        adicioná-lo à coleção e salvá-lo.
        """

        mock_obter_empresa.return_value = (
            self.empresa_ativa
        )

        resultado = usuarios.cadastrar_usuario(
            codigo_empresa=10,
            nome="Ana Souza",
            email="ana@empresa.com.br",
            perfil="ADMINISTRADOR",
        )

        self.assertEqual(
            resultado["codigo"],
            1,
        )

        self.assertEqual(
            resultado["codigo_empresa"],
            10,
        )

        self.assertEqual(
            resultado["nome"],
            "Ana Souza",
        )

        self.assertEqual(
            resultado["email"],
            "ana@empresa.com.br",
        )

        self.assertEqual(
            resultado["perfil"],
            (
                usuarios_dominio
                .PERFIL_USUARIO_ADMINISTRADOR
            ),
        )

        self.assertEqual(
            resultado["situacao"],
            (
                usuarios_dominio
                .SITUACAO_USUARIO_ATIVO
            ),
        )

        self.assertEqual(
            len(usuarios.usuarios),
            1,
        )

        self.assertIs(
            usuarios.usuarios[0],
            resultado,
        )

        mock_salvar_usuarios.assert_called_once_with(
            usuarios.usuarios
        )

    @patch(
        "app.usuarios.salvar_usuarios"
    )
    @patch(
        "app.usuarios."
        "empresas.empresa_esta_ativa",
        return_value=True,
    )
    @patch(
        "app.usuarios."
        "empresas.obter_empresa"
    )
    def test_cadastrar_usuario_gera_proximo_codigo(
        self,
        mock_obter_empresa,
        mock_empresa_esta_ativa,
        mock_salvar_usuarios,
    ):
        """
        O cadastro deve gerar o código seguinte
        ao maior código já existente.
        """

        mock_obter_empresa.return_value = (
            self.empresa_ativa
        )

        usuarios.usuarios = [
            {
                "codigo": 2,
                "codigo_empresa": 10,
                "nome": "Usuário anterior",
                "email": "anterior@empresa.com.br",
                "perfil": "GESTOR",
                "situacao": "ATIVO",
            },
            {
                "codigo": 8,
                "codigo_empresa": 10,
                "nome": "Outro usuário",
                "email": "outro@empresa.com.br",
                "perfil": "CONSULTA",
                "situacao": "ATIVO",
            },
        ]

        resultado = usuarios.cadastrar_usuario(
            codigo_empresa=10,
            nome="Ana Souza",
            email="ana@empresa.com.br",
            perfil="GESTOR",
        )

        self.assertEqual(
            resultado["codigo"],
            9,
        )

        mock_salvar_usuarios.assert_called_once_with(
            usuarios.usuarios
        )

    @patch(
        "app.usuarios.salvar_usuarios"
    )
    @patch(
        "app.usuarios."
        "empresas.empresa_esta_ativa",
        return_value=True,
    )
    @patch(
        "app.usuarios."
        "empresas.obter_empresa"
    )
    def test_cadastro_normaliza_dados(
        self,
        mock_obter_empresa,
        mock_empresa_esta_ativa,
        mock_salvar_usuarios,
    ):
        """
        A fachada deve utilizar o domínio,
        permitindo a normalização dos dados.
        """

        mock_obter_empresa.return_value = (
            self.empresa_ativa
        )

        resultado = usuarios.cadastrar_usuario(
            codigo_empresa=10,
            nome="  Ana   Maria   Souza  ",
            email="  ANA@EMPRESA.COM.BR  ",
            perfil="  gestor  ",
        )

        self.assertEqual(
            resultado["nome"],
            "Ana Maria Souza",
        )

        self.assertEqual(
            resultado["email"],
            "ana@empresa.com.br",
        )

        self.assertEqual(
            resultado["perfil"],
            usuarios_dominio.PERFIL_USUARIO_GESTOR,
        )

    @patch(
        "app.usuarios.salvar_usuarios"
    )
    @patch(
        "app.usuarios."
        "empresas.empresa_esta_ativa"
    )
    @patch(
        "app.usuarios."
        "empresas.obter_empresa",
        side_effect=ValueError(
            "Empresa com código 999 não encontrada."
        ),
    )
    def test_rejeitar_empresa_inexistente(
        self,
        mock_obter_empresa,
        mock_empresa_esta_ativa,
        mock_salvar_usuarios,
    ):
        """
        Não deve ser possível cadastrar
        Usuário para Empresa inexistente.
        """

        with self.assertRaisesRegex(
            ValueError,
            "Empresa com código 999 não encontrada",
        ):
            usuarios.cadastrar_usuario(
                codigo_empresa=999,
                nome="Ana Souza",
                email="ana@empresa.com.br",
                perfil="GESTOR",
            )

        self.assertEqual(
            usuarios.usuarios,
            [],
        )

        mock_obter_empresa.assert_called_once_with(
            999
        )

        mock_empresa_esta_ativa.assert_not_called()

        mock_salvar_usuarios.assert_not_called()

    @patch(
        "app.usuarios.salvar_usuarios"
    )
    @patch(
        "app.usuarios."
        "empresas.empresa_esta_ativa",
        return_value=False,
    )
    @patch(
        "app.usuarios."
        "empresas.obter_empresa"
    )
    def test_rejeitar_empresa_inativa(
        self,
        mock_obter_empresa,
        mock_empresa_esta_ativa,
        mock_salvar_usuarios,
    ):
        """
        Novos Usuários não podem ser cadastrados
        para Empresa que não esteja ativa.
        """

        mock_obter_empresa.return_value = {
            "codigo": 10,
            "situacao": "INATIVA",
        }

        with self.assertRaisesRegex(
            ValueError,
            "não esteja ativa",
        ):
            usuarios.cadastrar_usuario(
                codigo_empresa=10,
                nome="Ana Souza",
                email="ana@empresa.com.br",
                perfil="GESTOR",
            )

        self.assertEqual(
            usuarios.usuarios,
            [],
        )

        mock_salvar_usuarios.assert_not_called()

    @patch(
        "app.usuarios.salvar_usuarios"
    )
    @patch(
        "app.usuarios."
        "empresas.empresa_esta_ativa",
        return_value=False,
    )
    @patch(
        "app.usuarios."
        "empresas.obter_empresa"
    )
    def test_rejeitar_empresa_suspensa(
        self,
        mock_obter_empresa,
        mock_empresa_esta_ativa,
        mock_salvar_usuarios,
    ):
        """
        Uma Empresa suspensa também não deve
        receber novos Usuários.
        """

        mock_obter_empresa.return_value = {
            "codigo": 10,
            "situacao": "SUSPENSA",
        }

        with self.assertRaises(ValueError):
            usuarios.cadastrar_usuario(
                codigo_empresa=10,
                nome="Ana Souza",
                email="ana@empresa.com.br",
                perfil="GESTOR",
            )

        mock_salvar_usuarios.assert_not_called()

    @patch(
        "app.usuarios.salvar_usuarios"
    )
    @patch(
        "app.usuarios."
        "empresas.empresa_esta_ativa",
        return_value=True,
    )
    @patch(
        "app.usuarios."
        "empresas.obter_empresa"
    )
    def test_rejeitar_email_duplicado(
        self,
        mock_obter_empresa,
        mock_empresa_esta_ativa,
        mock_salvar_usuarios,
    ):
        """
        Um e-mail já existente não pode
        ser cadastrado novamente.
        """

        mock_obter_empresa.return_value = (
            self.empresa_ativa
        )

        usuarios.usuarios = [
            {
                "codigo": 1,
                "codigo_empresa": 10,
                "nome": "Ana Souza",
                "email": "ana@empresa.com.br",
                "perfil": "GESTOR",
                "situacao": "ATIVO",
            },
        ]

        with self.assertRaisesRegex(
            ValueError,
            "Já existe um usuário",
        ):
            usuarios.cadastrar_usuario(
                codigo_empresa=10,
                nome="Outra Ana",
                email="ana@empresa.com.br",
                perfil="CONSULTA",
            )

        self.assertEqual(
            len(usuarios.usuarios),
            1,
        )

        mock_salvar_usuarios.assert_not_called()

    @patch(
        "app.usuarios.salvar_usuarios"
    )
    @patch(
        "app.usuarios."
        "empresas.empresa_esta_ativa",
        return_value=True,
    )
    @patch(
        "app.usuarios."
        "empresas.obter_empresa"
    )
    def test_email_duplicado_ignora_maiusculas_e_espacos(
        self,
        mock_obter_empresa,
        mock_empresa_esta_ativa,
        mock_salvar_usuarios,
    ):
        """
        A unicidade do e-mail deve considerar
        a normalização feita pelo domínio.
        """

        mock_obter_empresa.return_value = (
            self.empresa_ativa
        )

        usuarios.usuarios = [
            {
                "codigo": 1,
                "codigo_empresa": 20,
                "nome": "Ana Souza",
                "email": "ana@empresa.com.br",
                "perfil": "GESTOR",
                "situacao": "ATIVO",
            },
        ]

        with self.assertRaisesRegex(
            ValueError,
            "Já existe um usuário",
        ):
            usuarios.cadastrar_usuario(
                codigo_empresa=10,
                nome="Outra Ana",
                email="  ANA@EMPRESA.COM.BR  ",
                perfil="CONSULTA",
            )

        mock_salvar_usuarios.assert_not_called()

    @patch(
        "app.usuarios.salvar_usuarios"
    )
    @patch(
        "app.usuarios."
        "empresas.empresa_esta_ativa",
        return_value=True,
    )
    @patch(
        "app.usuarios."
        "empresas.obter_empresa"
    )
    def test_email_e_unico_entre_empresas(
        self,
        mock_obter_empresa,
        mock_empresa_esta_ativa,
        mock_salvar_usuarios,
    ):
        """
        Um e-mail cadastrado na Empresa 20
        não pode ser reutilizado na Empresa 10.
        """

        mock_obter_empresa.return_value = (
            self.empresa_ativa
        )

        usuarios.usuarios = [
            {
                "codigo": 1,
                "codigo_empresa": 20,
                "nome": "Ana Souza",
                "email": "ana@empresa.com.br",
                "perfil": "GESTOR",
                "situacao": "ATIVO",
            },
        ]

        with self.assertRaises(ValueError):
            usuarios.cadastrar_usuario(
                codigo_empresa=10,
                nome="Ana da Empresa 10",
                email="ana@empresa.com.br",
                perfil="ADMINISTRADOR",
            )

        mock_salvar_usuarios.assert_not_called()

    @patch(
        "app.usuarios.salvar_usuarios"
    )
    @patch(
        "app.usuarios."
        "empresas.empresa_esta_ativa",
        return_value=True,
    )
    @patch(
        "app.usuarios."
        "empresas.obter_empresa"
    )
    def test_dados_invalidos_nao_sao_salvos(
        self,
        mock_obter_empresa,
        mock_empresa_esta_ativa,
        mock_salvar_usuarios,
    ):
        """
        Quando o domínio rejeita os dados,
        nada deve ser acrescentado ou salvo.
        """

        mock_obter_empresa.return_value = (
            self.empresa_ativa
        )

        with self.assertRaises(ValueError):
            usuarios.cadastrar_usuario(
                codigo_empresa=10,
                nome="Ana Souza",
                email="email-invalido",
                perfil="GESTOR",
            )

        self.assertEqual(
            usuarios.usuarios,
            [],
        )

        mock_salvar_usuarios.assert_not_called()


class TestConsultasUsuariosFachada(
    unittest.TestCase
):
    """
    Testes das consultas públicas
    da fachada de Usuários.
    """

    def setUp(
        self,
    ):
        """
        Cria uma coleção com Usuários
        de Empresas diferentes.
        """

        self.usuarios_originais = usuarios.usuarios

        self.usuario_ativo_empresa_10 = {
            "codigo": 1,
            "codigo_empresa": 10,
            "nome": "Ana Souza",
            "email": "ana@empresa10.com.br",
            "perfil": (
                usuarios_dominio
                .PERFIL_USUARIO_ADMINISTRADOR
            ),
            "situacao": (
                usuarios_dominio
                .SITUACAO_USUARIO_ATIVO
            ),
        }

        self.usuario_inativo_empresa_10 = {
            "codigo": 2,
            "codigo_empresa": 10,
            "nome": "Bruno Lima",
            "email": "bruno@empresa10.com.br",
            "perfil": (
                usuarios_dominio
                .PERFIL_USUARIO_OPERACIONAL
            ),
            "situacao": (
                usuarios_dominio
                .SITUACAO_USUARIO_INATIVO
            ),
        }

        self.usuario_cancelado_empresa_10 = {
            "codigo": 3,
            "codigo_empresa": 10,
            "nome": "Carlos Mendes",
            "email": "carlos@empresa10.com.br",
            "perfil": (
                usuarios_dominio
                .PERFIL_USUARIO_CONSULTA
            ),
            "situacao": (
                usuarios_dominio
                .SITUACAO_USUARIO_CANCELADO
            ),
        }

        self.usuario_empresa_20 = {
            "codigo": 4,
            "codigo_empresa": 20,
            "nome": "Daniel Santos",
            "email": "daniel@empresa20.com.br",
            "perfil": (
                usuarios_dominio
                .PERFIL_USUARIO_GESTOR
            ),
            "situacao": (
                usuarios_dominio
                .SITUACAO_USUARIO_ATIVO
            ),
        }

        usuarios.usuarios = [
            self.usuario_inativo_empresa_10,
            self.usuario_empresa_20,
            self.usuario_cancelado_empresa_10,
            self.usuario_ativo_empresa_10,
        ]

    def tearDown(
        self,
    ):
        """
        Restaura a coleção original.
        """

        usuarios.usuarios = (
            self.usuarios_originais
        )

    def test_obter_usuario(
        self,
    ):
        """
        Deve retornar o Usuário quando
        código e Empresa coincidirem.
        """

        resultado = usuarios.obter_usuario(
            codigo_usuario=1,
            codigo_empresa=10,
        )

        self.assertIs(
            resultado,
            self.usuario_ativo_empresa_10,
        )

    def test_buscar_usuario_funciona_como_alias(
        self,
    ):
        """
        buscar_usuario() deve encaminhar
        para a mesma consulta pública.
        """

        resultado = usuarios.buscar_usuario(
            codigo_usuario=2,
            codigo_empresa=10,
        )

        self.assertIs(
            resultado,
            self.usuario_inativo_empresa_10,
        )

    def test_obter_usuario_inexistente_retorna_none(
        self,
    ):
        """
        Usuário inexistente deve retornar None.
        """

        resultado = usuarios.obter_usuario(
            codigo_usuario=999,
            codigo_empresa=10,
        )

        self.assertIsNone(
            resultado
        )

    def test_obter_usuario_respeita_empresa(
        self,
    ):
        """
        Um Usuário de outra Empresa
        não deve ser retornado.
        """

        resultado = usuarios.obter_usuario(
            codigo_usuario=4,
            codigo_empresa=10,
        )

        self.assertIsNone(
            resultado
        )

    def test_obter_usuario_na_empresa_correta(
        self,
    ):
        """
        O Usuário deve ser encontrado
        quando a Empresa correta é informada.
        """

        resultado = usuarios.obter_usuario(
            codigo_usuario=4,
            codigo_empresa=20,
        )

        self.assertIs(
            resultado,
            self.usuario_empresa_20,
        )

    def test_buscar_usuario_por_email(
        self,
    ):
        """
        Deve localizar o Usuário pelo e-mail.
        """

        resultado = (
            usuarios.buscar_usuario_por_email(
                "ana@empresa10.com.br"
            )
        )

        self.assertIs(
            resultado,
            self.usuario_ativo_empresa_10,
        )

    def test_buscar_usuario_por_email_normaliza_entrada(
        self,
    ):
        """
        A busca por e-mail deve ignorar
        espaços e diferenças de caixa.
        """

        resultado = (
            usuarios.buscar_usuario_por_email(
                "  ANA@EMPRESA10.COM.BR  "
            )
        )

        self.assertIs(
            resultado,
            self.usuario_ativo_empresa_10,
        )

    def test_buscar_email_inexistente_retorna_none(
        self,
    ):
        """
        E-mail não cadastrado deve retornar None.
        """

        resultado = (
            usuarios.buscar_usuario_por_email(
                "inexistente@empresa.com.br"
            )
        )

        self.assertIsNone(
            resultado
        )

    def test_usuario_existe(
        self,
    ):
        """
        Deve retornar True quando o Usuário
        pertence à Empresa informada.
        """

        resultado = usuarios.usuario_existe(
            codigo_usuario=1,
            codigo_empresa=10,
        )

        self.assertTrue(
            resultado
        )

    def test_usuario_nao_existe_em_outra_empresa(
        self,
    ):
        """
        Um Usuário existente deve ser tratado
        como inexistente em outra Empresa.
        """

        resultado = usuarios.usuario_existe(
            codigo_usuario=4,
            codigo_empresa=10,
        )

        self.assertFalse(
            resultado
        )

    def test_email_usuario_existe(
        self,
    ):
        """
        Deve retornar True para e-mail cadastrado.
        """

        resultado = usuarios.email_usuario_existe(
            "bruno@empresa10.com.br"
        )

        self.assertTrue(
            resultado
        )

    def test_email_usuario_nao_existe(
        self,
    ):
        """
        Deve retornar False para e-mail
        ainda não cadastrado.
        """

        resultado = usuarios.email_usuario_existe(
            "novo@empresa.com.br"
        )

        self.assertFalse(
            resultado
        )


class TestListagensUsuariosFachada(
    unittest.TestCase
):
    """
    Testes das listagens públicas.
    """

    def setUp(
        self,
    ):
        """
        Prepara Usuários de duas Empresas.
        """

        self.usuarios_originais = usuarios.usuarios

        self.empresa_10 = {
            "codigo": 10,
            "nome_fantasia": "Empresa Dez",
            "situacao": "ATIVA",
        }

        self.usuario_ana = {
            "codigo": 1,
            "codigo_empresa": 10,
            "nome": "Ana Souza",
            "email": "ana@empresa10.com.br",
            "perfil": (
                usuarios_dominio
                .PERFIL_USUARIO_ADMINISTRADOR
            ),
            "situacao": (
                usuarios_dominio
                .SITUACAO_USUARIO_ATIVO
            ),
        }

        self.usuario_bruno = {
            "codigo": 2,
            "codigo_empresa": 10,
            "nome": "Bruno Lima",
            "email": "bruno@empresa10.com.br",
            "perfil": (
                usuarios_dominio
                .PERFIL_USUARIO_OPERACIONAL
            ),
            "situacao": (
                usuarios_dominio
                .SITUACAO_USUARIO_INATIVO
            ),
        }

        self.usuario_carlos = {
            "codigo": 3,
            "codigo_empresa": 10,
            "nome": "Carlos Mendes",
            "email": "carlos@empresa10.com.br",
            "perfil": (
                usuarios_dominio
                .PERFIL_USUARIO_OPERACIONAL
            ),
            "situacao": (
                usuarios_dominio
                .SITUACAO_USUARIO_ATIVO
            ),
        }

        self.usuario_outra_empresa = {
            "codigo": 4,
            "codigo_empresa": 20,
            "nome": "Daniel Santos",
            "email": "daniel@empresa20.com.br",
            "perfil": (
                usuarios_dominio
                .PERFIL_USUARIO_GESTOR
            ),
            "situacao": (
                usuarios_dominio
                .SITUACAO_USUARIO_ATIVO
            ),
        }

        usuarios.usuarios = [
            self.usuario_outra_empresa,
            self.usuario_carlos,
            self.usuario_bruno,
            self.usuario_ana,
        ]

    def tearDown(
        self,
    ):
        """
        Restaura a coleção original.
        """

        usuarios.usuarios = (
            self.usuarios_originais
        )

    @patch(
        "app.usuarios."
        "empresas.obter_empresa"
    )
    def test_listar_usuarios_da_empresa(
        self,
        mock_obter_empresa,
    ):
        """
        Deve listar somente Usuários
        da Empresa informada.
        """

        mock_obter_empresa.return_value = (
            self.empresa_10
        )

        resultado = usuarios.listar_usuarios(
            codigo_empresa=10
        )

        self.assertEqual(
            resultado,
            [
                self.usuario_ana,
                self.usuario_bruno,
                self.usuario_carlos,
            ],
        )

        self.assertNotIn(
            self.usuario_outra_empresa,
            resultado,
        )

    @patch(
        "app.usuarios."
        "empresas.obter_empresa",
        side_effect=ValueError(
            "Empresa com código 999 não encontrada."
        ),
    )
    def test_listar_usuarios_rejeita_empresa_inexistente(
        self,
        mock_obter_empresa,
    ):
        """
        Empresa inexistente deve gerar ValueError,
        e não apenas uma lista vazia.
        """

        with self.assertRaisesRegex(
            ValueError,
            "Empresa com código 999 não encontrada",
        ):
            usuarios.listar_usuarios(
                codigo_empresa=999
            )

        mock_obter_empresa.assert_called_once_with(
            999
        )

    @patch(
        "app.usuarios."
        "empresas.obter_empresa"
    )
    def test_empresa_sem_usuarios_retorna_lista_vazia(
        self,
        mock_obter_empresa,
    ):
        """
        Empresa existente sem Usuários
        deve retornar lista vazia.
        """

        mock_obter_empresa.return_value = (
            self.empresa_10
        )

        resultado = usuarios.listar_usuarios(
            codigo_empresa=30
        )

        self.assertEqual(
            resultado,
            [],
        )

    @patch(
        "app.usuarios."
        "empresas.obter_empresa"
    )
    def test_listar_usuarios_ativos(
        self,
        mock_obter_empresa,
    ):
        """
        Deve retornar somente Usuários ativos
        da Empresa informada.
        """

        mock_obter_empresa.return_value = (
            self.empresa_10
        )

        resultado = (
            usuarios.listar_usuarios_ativos(
                codigo_empresa=10
            )
        )

        self.assertEqual(
            resultado,
            [
                self.usuario_ana,
                self.usuario_carlos,
            ],
        )

    @patch(
        "app.usuarios."
        "empresas.obter_empresa"
    )
    def test_listar_usuarios_por_perfil(
        self,
        mock_obter_empresa,
    ):
        """
        Deve retornar somente Usuários
        com o perfil solicitado.
        """

        mock_obter_empresa.return_value = (
            self.empresa_10
        )

        resultado = (
            usuarios.listar_usuarios_por_perfil(
                codigo_empresa=10,
                perfil="operacional",
            )
        )

        self.assertEqual(
            resultado,
            [
                self.usuario_bruno,
                self.usuario_carlos,
            ],
        )

    @patch(
        "app.usuarios."
        "empresas.obter_empresa"
    )
    def test_listar_perfil_inexistente_retorna_lista_vazia(
        self,
        mock_obter_empresa,
    ):
        """
        Um perfil válido sem Usuários
        deve retornar lista vazia.
        """

        mock_obter_empresa.return_value = (
            self.empresa_10
        )

        resultado = (
            usuarios.listar_usuarios_por_perfil(
                codigo_empresa=10,
                perfil="GESTOR",
            )
        )

        self.assertEqual(
            resultado,
            [],
        )

    @patch(
        "app.usuarios."
        "empresas.obter_empresa"
    )
    def test_listar_perfil_invalido_gera_erro(
        self,
        mock_obter_empresa,
    ):
        """
        Perfil fora da coleção oficial
        deve ser rejeitado pelo domínio.
        """

        mock_obter_empresa.return_value = (
            self.empresa_10
        )

        with self.assertRaises(ValueError):
            usuarios.listar_usuarios_por_perfil(
                codigo_empresa=10,
                perfil="SUPERUSUARIO",
            )

    @patch(
        "app.usuarios."
        "empresas.obter_empresa"
    )
    def test_quantidade_usuarios(
        self,
        mock_obter_empresa,
    ):
        """
        Deve retornar a quantidade de Usuários
        vinculados à Empresa.
        """

        mock_obter_empresa.return_value = (
            self.empresa_10
        )

        resultado = usuarios.quantidade_usuarios(
            codigo_empresa=10
        )

        self.assertEqual(
            resultado,
            3,
        )


class TestPerfilESituacaoUsuariosFachada(
    unittest.TestCase
):
    """
    Testes das consultas de perfil
    e situação pela fachada.
    """

    def setUp(
        self,
    ):
        """
        Prepara Usuários em estados distintos.
        """

        self.usuarios_originais = usuarios.usuarios

        self.usuario_ativo = {
            "codigo": 1,
            "codigo_empresa": 10,
            "nome": "Ana Souza",
            "email": "ana@empresa.com.br",
            "perfil": (
                usuarios_dominio
                .PERFIL_USUARIO_ADMINISTRADOR
            ),
            "situacao": (
                usuarios_dominio
                .SITUACAO_USUARIO_ATIVO
            ),
        }

        self.usuario_cancelado = {
            "codigo": 2,
            "codigo_empresa": 10,
            "nome": "Carlos Souza",
            "email": "carlos@empresa.com.br",
            "perfil": (
                usuarios_dominio
                .PERFIL_USUARIO_CONSULTA
            ),
            "situacao": (
                usuarios_dominio
                .SITUACAO_USUARIO_CANCELADO
            ),
        }

        self.usuario_outra_empresa = {
            "codigo": 3,
            "codigo_empresa": 20,
            "nome": "Daniel Souza",
            "email": "daniel@empresa.com.br",
            "perfil": (
                usuarios_dominio
                .PERFIL_USUARIO_GESTOR
            ),
            "situacao": (
                usuarios_dominio
                .SITUACAO_USUARIO_ATIVO
            ),
        }

        usuarios.usuarios = [
            self.usuario_ativo,
            self.usuario_cancelado,
            self.usuario_outra_empresa,
        ]

    def tearDown(
        self,
    ):
        """
        Restaura a coleção original.
        """

        usuarios.usuarios = (
            self.usuarios_originais
        )

    def test_usuario_esta_ativo(
        self,
    ):
        """
        Deve retornar True para Usuário ativo.
        """

        resultado = usuarios.usuario_esta_ativo(
            codigo_usuario=1,
            codigo_empresa=10,
        )

        self.assertTrue(
            resultado
        )

    def test_usuario_cancelado_nao_esta_ativo(
        self,
    ):
        """
        Deve retornar False para Usuário
        que não esteja ativo.
        """

        resultado = usuarios.usuario_esta_ativo(
            codigo_usuario=2,
            codigo_empresa=10,
        )

        self.assertFalse(
            resultado
        )

    def test_usuario_esta_cancelado(
        self,
    ):
        """
        Deve retornar True para Usuário cancelado.
        """

        resultado = (
            usuarios.usuario_esta_cancelado(
                codigo_usuario=2,
                codigo_empresa=10,
            )
        )

        self.assertTrue(
            resultado
        )

    def test_usuario_ativo_nao_esta_cancelado(
        self,
    ):
        """
        Deve retornar False para Usuário ativo.
        """

        resultado = (
            usuarios.usuario_esta_cancelado(
                codigo_usuario=1,
                codigo_empresa=10,
            )
        )

        self.assertFalse(
            resultado
        )

    def test_usuario_possui_perfil(
        self,
    ):
        """
        Deve retornar True quando o perfil
        corresponde ao Usuário.
        """

        resultado = usuarios.usuario_possui_perfil(
            codigo_usuario=1,
            codigo_empresa=10,
            perfil="administrador",
        )

        self.assertTrue(
            resultado
        )

    def test_usuario_nao_possui_perfil(
        self,
    ):
        """
        Deve retornar False quando o perfil
        não corresponde ao Usuário.
        """

        resultado = usuarios.usuario_possui_perfil(
            codigo_usuario=1,
            codigo_empresa=10,
            perfil="GESTOR",
        )

        self.assertFalse(
            resultado
        )

    def test_consulta_usuario_inexistente_gera_erro(
        self,
    ):
        """
        Consultar situação de Usuário inexistente
        deve gerar ValueError.
        """

        with self.assertRaisesRegex(
            ValueError,
            "Usuário não encontrado",
        ):
            usuarios.usuario_esta_ativo(
                codigo_usuario=999,
                codigo_empresa=10,
            )

    def test_consulta_nao_acessa_usuario_de_outra_empresa(
        self,
    ):
        """
        Um Usuário existente em outra Empresa
        deve ser tratado como não encontrado.
        """

        with self.assertRaisesRegex(
            ValueError,
            "Usuário não encontrado",
        ):
            usuarios.usuario_esta_ativo(
                codigo_usuario=3,
                codigo_empresa=10,
            )

    def test_consulta_cancelamento_usuario_inexistente(
        self,
    ):
        """
        Consultar cancelamento de Usuário inexistente
        deve gerar ValueError.
        """

        with self.assertRaises(ValueError):
            usuarios.usuario_esta_cancelado(
                codigo_usuario=999,
                codigo_empresa=10,
            )

    def test_consulta_perfil_usuario_inexistente(
        self,
    ):
        """
        Consultar perfil de Usuário inexistente
        deve gerar ValueError.
        """

        with self.assertRaises(ValueError):
            usuarios.usuario_possui_perfil(
                codigo_usuario=999,
                codigo_empresa=10,
                perfil="GESTOR",
            )


class TestFuncoesApoioUsuariosFachada(
    unittest.TestCase
):
    """
    Testes das funções de apoio
    disponibilizadas para a Interface.
    """

    def test_obter_perfis_usuario(
        self,
    ):
        """
        A fachada deve expor os perfis
        oficiais do domínio.
        """

        resultado = usuarios.obter_perfis_usuario()

        self.assertEqual(
            resultado,
            usuarios_dominio.PERFIS_USUARIO,
        )

    def test_obter_situacoes_usuario(
        self,
    ):
        """
        A fachada deve expor as situações
        oficiais do domínio.
        """

        resultado = usuarios.obter_situacoes_usuario()

        self.assertEqual(
            resultado,
            usuarios_dominio.SITUACOES_USUARIO,
        )

    def test_perfis_sao_retornados_como_tupla(
        self,
    ):
        """
        A coleção pública de perfis
        deve ser imutável por estrutura.
        """

        resultado = usuarios.obter_perfis_usuario()

        self.assertIsInstance(
            resultado,
            tuple,
        )

    def test_situacoes_sao_retornadas_como_tupla(
        self,
    ):
        """
        A coleção pública de situações
        deve ser imutável por estrutura.
        """

        resultado = usuarios.obter_situacoes_usuario()

        self.assertIsInstance(
            resultado,
            tuple,
        )

class TestAlteracaoSituacaoUsuarioFachada(
    unittest.TestCase
):
    """
    Testes da alteração de situação
    de Usuários pela fachada.
    """

    def setUp(
        self,
    ):
        """
        Substitui temporariamente a coleção
        real de Usuários por uma coleção controlada.
        """

        self.usuarios_originais = (
            usuarios.usuarios
        )

        self.usuario_empresa_10 = {
            "codigo": 1,
            "codigo_empresa": 10,
            "nome": "Ana Souza",
            "email": "ana@empresa.com.br",
            "perfil": "GESTOR",
            "situacao": "ATIVO",
            "data_cadastro": (
                "2026-07-28T10:00:00"
            ),
            "data_atualizacao": (
                "2026-07-28T10:00:00"
            ),
        }

        self.usuario_empresa_20 = {
            "codigo": 2,
            "codigo_empresa": 20,
            "nome": "Bruno Lima",
            "email": "bruno@empresa.com.br",
            "perfil": "OPERACIONAL",
            "situacao": "ATIVO",
            "data_cadastro": (
                "2026-07-28T11:00:00"
            ),
            "data_atualizacao": (
                "2026-07-28T11:00:00"
            ),
        }

        usuarios.usuarios = [
            self.usuario_empresa_10,
            self.usuario_empresa_20,
        ]

    def tearDown(
        self,
    ):
        """
        Restaura a coleção original
        após cada teste.
        """

        usuarios.usuarios = (
            self.usuarios_originais
        )

    @patch(
        "app.usuarios.salvar_usuarios"
    )
    @patch(
        "app.usuarios."
        "usuarios_dominio."
        "alterar_situacao_usuario"
    )
    @patch(
        "app.usuarios."
        "empresas.empresa_esta_ativa",
        return_value=True,
    )
    @patch(
        "app.usuarios."
        "empresas.obter_empresa"
    )
    def test_alterar_situacao_usuario_com_sucesso(
        self,
        mock_obter_empresa,
        mock_empresa_esta_ativa,
        mock_alterar_dominio,
        mock_salvar_usuarios,
    ):
        """
        A fachada deve localizar o Usuário,
        chamar o domínio e salvar a coleção.
        """

        empresa = {
            "codigo": 10,
            "nome_fantasia": "Empresa Solar",
            "situacao": "ATIVA",
        }

        mock_obter_empresa.return_value = empresa

        usuario_atualizado = {
            **self.usuario_empresa_10,
            "situacao": "BLOQUEADO",
            "data_atualizacao": (
                "2026-07-28T14:00:00"
            ),
        }

        mock_alterar_dominio.return_value = (
            usuario_atualizado
        )

        resultado = (
            usuarios.alterar_situacao_usuario(
                codigo_empresa=10,
                codigo_usuario=1,
                nova_situacao="BLOQUEADO",
            )
        )

        mock_obter_empresa.assert_called_once_with(
            10
        )

        (
            mock_empresa_esta_ativa
            .assert_called_once_with(
                10
            )
        )

        (
            mock_alterar_dominio
            .assert_called_once_with(
                usuario=self.usuario_empresa_10,
                nova_situacao="BLOQUEADO",
            )
        )

        mock_salvar_usuarios.assert_called_once_with(
            usuarios.usuarios
        )

        self.assertIs(
            resultado,
            usuario_atualizado,
        )

    @patch(
        "app.usuarios.salvar_usuarios"
    )
    @patch(
        "app.usuarios."
        "usuarios_dominio."
        "alterar_situacao_usuario"
    )
    @patch(
        "app.usuarios."
        "empresas.empresa_esta_ativa",
        return_value=True,
    )
    @patch(
        "app.usuarios."
        "empresas.obter_empresa"
    )
    def test_alterar_situacao_normaliza_codigo(
        self,
        mock_obter_empresa,
        mock_empresa_esta_ativa,
        mock_alterar_dominio,
        mock_salvar_usuarios,
    ):
        """
        A fachada deve encaminhar corretamente
        os dados para o domínio.
        """

        mock_obter_empresa.return_value = {
            "codigo": 10,
            "situacao": "ATIVA",
        }

        mock_alterar_dominio.return_value = (
            self.usuario_empresa_10
        )

        usuarios.alterar_situacao_usuario(
            codigo_empresa=10,
            codigo_usuario=1,
            nova_situacao="  inativo  ",
        )

        (
            mock_alterar_dominio
            .assert_called_once_with(
                usuario=self.usuario_empresa_10,
                nova_situacao="  inativo  ",
            )
        )

    @patch(
        "app.usuarios.salvar_usuarios"
    )
    @patch(
        "app.usuarios."
        "usuarios_dominio."
        "alterar_situacao_usuario"
    )
    @patch(
        "app.usuarios."
        "empresas.obter_empresa",
        side_effect=ValueError(
            "Empresa com código 999 não encontrada."
        ),
    )
    def test_rejeitar_empresa_inexistente(
        self,
        mock_obter_empresa,
        mock_alterar_dominio,
        mock_salvar_usuarios,
    ):
        """
        Empresa inexistente deve impedir
        qualquer alteração.
        """

        with self.assertRaisesRegex(
            ValueError,
            "Empresa com código 999 não encontrada",
        ):
            usuarios.alterar_situacao_usuario(
                codigo_empresa=999,
                codigo_usuario=1,
                nova_situacao="INATIVO",
            )

        mock_obter_empresa.assert_called_once_with(
            999
        )

        mock_alterar_dominio.assert_not_called()

        mock_salvar_usuarios.assert_not_called()

    @patch(
        "app.usuarios.salvar_usuarios"
    )
    @patch(
        "app.usuarios."
        "usuarios_dominio."
        "alterar_situacao_usuario"
    )
    @patch(
        "app.usuarios."
        "empresas.empresa_esta_ativa",
        return_value=False,
    )
    @patch(
        "app.usuarios."
        "empresas.obter_empresa"
    )
    def test_rejeitar_empresa_inativa(
        self,
        mock_obter_empresa,
        mock_empresa_esta_ativa,
        mock_alterar_dominio,
        mock_salvar_usuarios,
    ):
        """
        Uma Empresa inativa não deve
        alterar seus Usuários.
        """

        mock_obter_empresa.return_value = {
            "codigo": 10,
            "nome_fantasia": "Empresa Solar",
            "situacao": "INATIVA",
        }

        with self.assertRaisesRegex(
            ValueError,
            "Empresa deve estar ativa",
        ):
            usuarios.alterar_situacao_usuario(
                codigo_empresa=10,
                codigo_usuario=1,
                nova_situacao="INATIVO",
            )

        (
            mock_empresa_esta_ativa
            .assert_called_once_with(
                10
            )
        )

        mock_alterar_dominio.assert_not_called()

        mock_salvar_usuarios.assert_not_called()

    @patch(
        "app.usuarios.salvar_usuarios"
    )
    @patch(
        "app.usuarios."
        "usuarios_dominio."
        "alterar_situacao_usuario"
    )
    @patch(
        "app.usuarios."
        "empresas.empresa_esta_ativa",
        return_value=True,
    )
    @patch(
        "app.usuarios."
        "empresas.obter_empresa"
    )
    def test_rejeitar_usuario_inexistente(
        self,
        mock_obter_empresa,
        mock_empresa_esta_ativa,
        mock_alterar_dominio,
        mock_salvar_usuarios,
    ):
        """
        Código inexistente deve gerar erro.
        """

        mock_obter_empresa.return_value = {
            "codigo": 10,
            "situacao": "ATIVA",
        }

        with self.assertRaisesRegex(
            ValueError,
            "Usuário com código 999 não encontrado",
        ):
            usuarios.alterar_situacao_usuario(
                codigo_empresa=10,
                codigo_usuario=999,
                nova_situacao="INATIVO",
            )

        mock_alterar_dominio.assert_not_called()

        mock_salvar_usuarios.assert_not_called()

    @patch(
        "app.usuarios.salvar_usuarios"
    )
    @patch(
        "app.usuarios."
        "usuarios_dominio."
        "alterar_situacao_usuario"
    )
    @patch(
        "app.usuarios."
        "empresas.empresa_esta_ativa",
        return_value=True,
    )
    @patch(
        "app.usuarios."
        "empresas.obter_empresa"
    )
    def test_impedir_alteracao_de_usuario_de_outra_empresa(
        self,
        mock_obter_empresa,
        mock_empresa_esta_ativa,
        mock_alterar_dominio,
        mock_salvar_usuarios,
    ):
        """
        Um Usuário existente, mas pertencente
        a outra Empresa, deve ser tratado
        como inexistente no contexto solicitado.
        """

        mock_obter_empresa.return_value = {
            "codigo": 10,
            "situacao": "ATIVA",
        }

        with self.assertRaisesRegex(
            ValueError,
            "Usuário com código 2 não encontrado",
        ):
            usuarios.alterar_situacao_usuario(
                codigo_empresa=10,
                codigo_usuario=2,
                nova_situacao="BLOQUEADO",
            )

        mock_alterar_dominio.assert_not_called()

        mock_salvar_usuarios.assert_not_called()

    @patch(
        "app.usuarios.salvar_usuarios"
    )
    @patch(
        "app.usuarios."
        "usuarios_dominio."
        "alterar_situacao_usuario",
        side_effect=ValueError(
            "Transição de situação não permitida: "
            "CANCELADO → ATIVO."
        ),
    )
    @patch(
        "app.usuarios."
        "empresas.empresa_esta_ativa",
        return_value=True,
    )
    @patch(
        "app.usuarios."
        "empresas.obter_empresa"
    )
    def test_propagar_erro_do_dominio(
        self,
        mock_obter_empresa,
        mock_empresa_esta_ativa,
        mock_alterar_dominio,
        mock_salvar_usuarios,
    ):
        """
        A fachada não deve esconder
        uma transição rejeitada pelo domínio.
        """

        mock_obter_empresa.return_value = {
            "codigo": 10,
            "situacao": "ATIVA",
        }

        self.usuario_empresa_10[
            "situacao"
        ] = "CANCELADO"

        with self.assertRaisesRegex(
            ValueError,
            "Transição de situação não permitida",
        ):
            usuarios.alterar_situacao_usuario(
                codigo_empresa=10,
                codigo_usuario=1,
                nova_situacao="ATIVO",
            )

        mock_salvar_usuarios.assert_not_called()

    @patch(
        "app.usuarios.salvar_usuarios",
        side_effect=OSError(
            "Falha ao salvar arquivo."
        ),
    )
    @patch(
        "app.usuarios."
        "usuarios_dominio."
        "alterar_situacao_usuario"
    )
    @patch(
        "app.usuarios."
        "empresas.empresa_esta_ativa",
        return_value=True,
    )
    @patch(
        "app.usuarios."
        "empresas.obter_empresa"
    )
    def test_propagar_erro_de_persistencia(
        self,
        mock_obter_empresa,
        mock_empresa_esta_ativa,
        mock_alterar_dominio,
        mock_salvar_usuarios,
    ):
        """
        Erros do repositório não devem
        ser silenciosamente ignorados.
        """

        mock_obter_empresa.return_value = {
            "codigo": 10,
            "situacao": "ATIVA",
        }

        mock_alterar_dominio.return_value = (
            self.usuario_empresa_10
        )

        with self.assertRaisesRegex(
            OSError,
            "Falha ao salvar arquivo",
        ):
            usuarios.alterar_situacao_usuario(
                codigo_empresa=10,
                codigo_usuario=1,
                nova_situacao="INATIVO",
            )

        mock_salvar_usuarios.assert_called_once_with(
            usuarios.usuarios
        )

class TestOperacoesSituacaoUsuarioFachada(
    unittest.TestCase
):
    """
    Testes das operações semânticas
    de situação do Usuário.
    """

    @patch(
        "app.usuarios.alterar_situacao_usuario"
    )
    def test_ativar_usuario(
        self,
        mock_alterar_situacao,
    ):
        """
        ativar_usuario() deve reutilizar
        alterar_situacao_usuario() com ATIVO.
        """

        usuario_atualizado = {
            "codigo": 1,
            "codigo_empresa": 10,
            "situacao": "ATIVO",
        }

        mock_alterar_situacao.return_value = (
            usuario_atualizado
        )

        resultado = usuarios.ativar_usuario(
            codigo_empresa=10,
            codigo_usuario=1,
        )

        mock_alterar_situacao.assert_called_once_with(
            codigo_empresa=10,
            codigo_usuario=1,
            nova_situacao="ATIVO",
        )

        self.assertIs(
            resultado,
            usuario_atualizado,
        )

    @patch(
        "app.usuarios.alterar_situacao_usuario"
    )
    def test_inativar_usuario(
        self,
        mock_alterar_situacao,
    ):
        """
        inativar_usuario() deve reutilizar
        alterar_situacao_usuario() com INATIVO.
        """

        usuario_atualizado = {
            "codigo": 1,
            "codigo_empresa": 10,
            "situacao": "INATIVO",
        }

        mock_alterar_situacao.return_value = (
            usuario_atualizado
        )

        resultado = usuarios.inativar_usuario(
            codigo_empresa=10,
            codigo_usuario=1,
        )

        mock_alterar_situacao.assert_called_once_with(
            codigo_empresa=10,
            codigo_usuario=1,
            nova_situacao="INATIVO",
        )

        self.assertIs(
            resultado,
            usuario_atualizado,
        )

    @patch(
        "app.usuarios.alterar_situacao_usuario"
    )
    def test_bloquear_usuario(
        self,
        mock_alterar_situacao,
    ):
        """
        bloquear_usuario() deve reutilizar
        alterar_situacao_usuario() com BLOQUEADO.
        """

        usuario_atualizado = {
            "codigo": 1,
            "codigo_empresa": 10,
            "situacao": "BLOQUEADO",
        }

        mock_alterar_situacao.return_value = (
            usuario_atualizado
        )

        resultado = usuarios.bloquear_usuario(
            codigo_empresa=10,
            codigo_usuario=1,
        )

        mock_alterar_situacao.assert_called_once_with(
            codigo_empresa=10,
            codigo_usuario=1,
            nova_situacao="BLOQUEADO",
        )

        self.assertIs(
            resultado,
            usuario_atualizado,
        )

    @patch(
        "app.usuarios.alterar_situacao_usuario"
    )
    def test_cancelar_usuario(
        self,
        mock_alterar_situacao,
    ):
        """
        cancelar_usuario() deve reutilizar
        alterar_situacao_usuario() com CANCELADO.
        """

        usuario_atualizado = {
            "codigo": 1,
            "codigo_empresa": 10,
            "situacao": "CANCELADO",
        }

        mock_alterar_situacao.return_value = (
            usuario_atualizado
        )

        resultado = usuarios.cancelar_usuario(
            codigo_empresa=10,
            codigo_usuario=1,
        )

        mock_alterar_situacao.assert_called_once_with(
            codigo_empresa=10,
            codigo_usuario=1,
            nova_situacao="CANCELADO",
        )

        self.assertIs(
            resultado,
            usuario_atualizado,
        )

    @patch(
        "app.usuarios.alterar_situacao_usuario",
        side_effect=ValueError(
            "Transição de situação não permitida."
        ),
    )
    def test_operacao_semantica_propaga_erro(
        self,
        mock_alterar_situacao,
    ):
        """
        As funções semânticas não devem
        esconder erros da operação principal.
        """

        with self.assertRaisesRegex(
            ValueError,
            "Transição de situação não permitida",
        ):
            usuarios.ativar_usuario(
                codigo_empresa=10,
                codigo_usuario=1,
            )

if __name__ == "__main__":
    unittest.main()