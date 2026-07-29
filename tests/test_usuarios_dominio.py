"""
Testes das regras de domínio relacionadas aos Usuários.

Este arquivo testa:

- criação de usuários;
- normalização dos dados;
- validação de códigos;
- validação de nome;
- validação de e-mail;
- validação de perfil;
- validação de situação;
- busca por código;
- busca por e-mail;
- isolamento entre empresas;
- verificação de existência;
- listagem dos usuários de uma empresa;
- consultas de perfil e situação.

Nenhum teste deste arquivo acessa arquivos JSON,
fachadas, interfaces ou o menu principal.
"""

import unittest
from datetime import datetime

from app.dominio import usuarios
from app.dominio import usuarios as usuarios_dominio


class TestCriarDadosUsuario(
    unittest.TestCase
):
    """
    Testes relacionados à criação
    dos dados de um Usuário.
    """

    def test_criar_dados_usuario_valido(
        self,
    ):
        """
        Deve criar um usuário com todos
        os campos obrigatórios.
        """

        usuario = usuarios.criar_dados_usuario(
            codigo=1,
            codigo_empresa=10,
            nome="Ana Souza",
            email="ana@empresa.com.br",
            perfil=(
                usuarios
                .PERFIL_USUARIO_ADMINISTRADOR
            ),
        )

        self.assertEqual(
            usuario["codigo"],
            1,
        )

        self.assertEqual(
            usuario["codigo_empresa"],
            10,
        )

        self.assertEqual(
            usuario["nome"],
            "Ana Souza",
        )

        self.assertEqual(
            usuario["email"],
            "ana@empresa.com.br",
        )

        self.assertEqual(
            usuario["perfil"],
            (
                usuarios
                .PERFIL_USUARIO_ADMINISTRADOR
            ),
        )

        self.assertEqual(
            usuario["situacao"],
            usuarios.SITUACAO_USUARIO_ATIVO,
        )

        self.assertIn(
            "data_cadastro",
            usuario,
        )

        self.assertIn(
            "data_atualizacao",
            usuario,
        )

    def test_criar_usuario_define_situacao_inicial_ativa(
        self,
    ):
        """
        Quando nenhuma situação for informada,
        o usuário deve começar como ATIVO.
        """

        usuario = usuarios.criar_dados_usuario(
            codigo=1,
            codigo_empresa=10,
            nome="Ana Souza",
            email="ana@empresa.com.br",
            perfil=usuarios.PERFIL_USUARIO_GESTOR,
        )

        self.assertEqual(
            usuario["situacao"],
            usuarios.SITUACAO_INICIAL_USUARIO,
        )

        self.assertEqual(
            usuario["situacao"],
            usuarios.SITUACAO_USUARIO_ATIVO,
        )

    def test_criar_usuario_com_situacao_informada(
        self,
    ):
        """
        Deve aceitar uma situação válida
        informada explicitamente.
        """

        usuario = usuarios.criar_dados_usuario(
            codigo=1,
            codigo_empresa=10,
            nome="Ana Souza",
            email="ana@empresa.com.br",
            perfil=usuarios.PERFIL_USUARIO_GESTOR,
            situacao=(
                usuarios
                .SITUACAO_USUARIO_INATIVO
            ),
        )

        self.assertEqual(
            usuario["situacao"],
            usuarios.SITUACAO_USUARIO_INATIVO,
        )

    def test_criar_usuario_normaliza_nome(
        self,
    ):
        """
        Espaços externos e duplicados
        devem ser removidos do nome.
        """

        usuario = usuarios.criar_dados_usuario(
            codigo=1,
            codigo_empresa=10,
            nome="  Ana   Maria   Souza  ",
            email="ana@empresa.com.br",
            perfil=usuarios.PERFIL_USUARIO_GESTOR,
        )

        self.assertEqual(
            usuario["nome"],
            "Ana Maria Souza",
        )

    def test_criar_usuario_normaliza_email(
        self,
    ):
        """
        O e-mail deve ser armazenado sem espaços
        externos e com letras minúsculas.
        """

        usuario = usuarios.criar_dados_usuario(
            codigo=1,
            codigo_empresa=10,
            nome="Ana Souza",
            email="  ANA.SOUZA@EMPRESA.COM.BR  ",
            perfil=usuarios.PERFIL_USUARIO_GESTOR,
        )

        self.assertEqual(
            usuario["email"],
            "ana.souza@empresa.com.br",
        )

    def test_criar_usuario_normaliza_perfil(
        self,
    ):
        """
        O perfil deve ser normalizado
        para letras maiúsculas.
        """

        usuario = usuarios.criar_dados_usuario(
            codigo=1,
            codigo_empresa=10,
            nome="Ana Souza",
            email="ana@empresa.com.br",
            perfil="  gestor  ",
        )

        self.assertEqual(
            usuario["perfil"],
            usuarios.PERFIL_USUARIO_GESTOR,
        )

    def test_criar_usuario_normaliza_situacao(
        self,
    ):
        """
        A situação deve ser normalizada
        para letras maiúsculas.
        """

        usuario = usuarios.criar_dados_usuario(
            codigo=1,
            codigo_empresa=10,
            nome="Ana Souza",
            email="ana@empresa.com.br",
            perfil=usuarios.PERFIL_USUARIO_GESTOR,
            situacao="  bloqueado  ",
        )

        self.assertEqual(
            usuario["situacao"],
            usuarios.SITUACAO_USUARIO_BLOQUEADO,
        )

    def test_datas_de_criacao_sao_iguais(
        self,
    ):
        """
        Na criação, data_cadastro e
        data_atualizacao devem ser iguais.
        """

        usuario = usuarios.criar_dados_usuario(
            codigo=1,
            codigo_empresa=10,
            nome="Ana Souza",
            email="ana@empresa.com.br",
            perfil=usuarios.PERFIL_USUARIO_GESTOR,
        )

        self.assertEqual(
            usuario["data_cadastro"],
            usuario["data_atualizacao"],
        )

    def test_datas_utilizam_formato_iso(
        self,
    ):
        """
        As datas devem poder ser interpretadas
        pelo formato ISO utilizado pelo Python.
        """

        usuario = usuarios.criar_dados_usuario(
            codigo=1,
            codigo_empresa=10,
            nome="Ana Souza",
            email="ana@empresa.com.br",
            perfil=usuarios.PERFIL_USUARIO_GESTOR,
        )

        data_convertida = datetime.fromisoformat(
            usuario["data_cadastro"]
        )

        self.assertIsInstance(
            data_convertida,
            datetime,
        )


class TestValidacoesCriacaoUsuario(
    unittest.TestCase
):
    """
    Testes de rejeição de dados inválidos
    durante a criação de um Usuário.
    """

    def test_codigo_usuario_deve_ser_inteiro(
        self,
    ):
        """
        Código textual deve ser rejeitado.
        """

        with self.assertRaises(TypeError):
            usuarios.criar_dados_usuario(
                codigo="1",
                codigo_empresa=10,
                nome="Ana Souza",
                email="ana@empresa.com.br",
                perfil=(
                    usuarios
                    .PERFIL_USUARIO_GESTOR
                ),
            )

    def test_codigo_usuario_nao_aceita_booleano(
        self,
    ):
        """
        Booleanos não devem ser aceitos como códigos,
        apesar de bool ser uma subclasse de int.
        """

        with self.assertRaises(TypeError):
            usuarios.criar_dados_usuario(
                codigo=True,
                codigo_empresa=10,
                nome="Ana Souza",
                email="ana@empresa.com.br",
                perfil=(
                    usuarios
                    .PERFIL_USUARIO_GESTOR
                ),
            )

    def test_codigo_usuario_deve_ser_maior_que_zero(
        self,
    ):
        """
        Código zero deve ser rejeitado.
        """

        with self.assertRaises(ValueError):
            usuarios.criar_dados_usuario(
                codigo=0,
                codigo_empresa=10,
                nome="Ana Souza",
                email="ana@empresa.com.br",
                perfil=(
                    usuarios
                    .PERFIL_USUARIO_GESTOR
                ),
            )

    def test_codigo_usuario_negativo_deve_ser_rejeitado(
        self,
    ):
        """
        Código negativo deve ser rejeitado.
        """

        with self.assertRaises(ValueError):
            usuarios.criar_dados_usuario(
                codigo=-1,
                codigo_empresa=10,
                nome="Ana Souza",
                email="ana@empresa.com.br",
                perfil=(
                    usuarios
                    .PERFIL_USUARIO_GESTOR
                ),
            )

    def test_codigo_empresa_deve_ser_inteiro(
        self,
    ):
        """
        O código da empresa deve ser inteiro.
        """

        with self.assertRaises(TypeError):
            usuarios.criar_dados_usuario(
                codigo=1,
                codigo_empresa="10",
                nome="Ana Souza",
                email="ana@empresa.com.br",
                perfil=(
                    usuarios
                    .PERFIL_USUARIO_GESTOR
                ),
            )

    def test_codigo_empresa_nao_aceita_booleano(
        self,
    ):
        """
        Booleanos não devem ser aceitos
        como códigos de empresa.
        """

        with self.assertRaises(TypeError):
            usuarios.criar_dados_usuario(
                codigo=1,
                codigo_empresa=False,
                nome="Ana Souza",
                email="ana@empresa.com.br",
                perfil=(
                    usuarios
                    .PERFIL_USUARIO_GESTOR
                ),
            )

    def test_codigo_empresa_deve_ser_maior_que_zero(
        self,
    ):
        """
        O código da empresa deve ser positivo.
        """

        with self.assertRaises(ValueError):
            usuarios.criar_dados_usuario(
                codigo=1,
                codigo_empresa=0,
                nome="Ana Souza",
                email="ana@empresa.com.br",
                perfil=(
                    usuarios
                    .PERFIL_USUARIO_GESTOR
                ),
            )

    def test_nome_deve_ser_texto(
        self,
    ):
        """
        O nome não pode ser numérico.
        """

        with self.assertRaises(TypeError):
            usuarios.criar_dados_usuario(
                codigo=1,
                codigo_empresa=10,
                nome=123,
                email="ana@empresa.com.br",
                perfil=(
                    usuarios
                    .PERFIL_USUARIO_GESTOR
                ),
            )

    def test_nome_vazio_deve_ser_rejeitado(
        self,
    ):
        """
        O nome é obrigatório.
        """

        with self.assertRaises(ValueError):
            usuarios.criar_dados_usuario(
                codigo=1,
                codigo_empresa=10,
                nome="",
                email="ana@empresa.com.br",
                perfil=(
                    usuarios
                    .PERFIL_USUARIO_GESTOR
                ),
            )

    def test_nome_apenas_com_espacos_deve_ser_rejeitado(
        self,
    ):
        """
        Um nome formado apenas por espaços
        deve ser considerado vazio.
        """

        with self.assertRaises(ValueError):
            usuarios.criar_dados_usuario(
                codigo=1,
                codigo_empresa=10,
                nome="     ",
                email="ana@empresa.com.br",
                perfil=(
                    usuarios
                    .PERFIL_USUARIO_GESTOR
                ),
            )

    def test_email_deve_ser_texto(
        self,
    ):
        """
        O e-mail deve ser uma string.
        """

        with self.assertRaises(TypeError):
            usuarios.criar_dados_usuario(
                codigo=1,
                codigo_empresa=10,
                nome="Ana Souza",
                email=123,
                perfil=(
                    usuarios
                    .PERFIL_USUARIO_GESTOR
                ),
            )

    def test_email_vazio_deve_ser_rejeitado(
        self,
    ):
        """
        O e-mail é obrigatório.
        """

        with self.assertRaises(ValueError):
            usuarios.criar_dados_usuario(
                codigo=1,
                codigo_empresa=10,
                nome="Ana Souza",
                email="",
                perfil=(
                    usuarios
                    .PERFIL_USUARIO_GESTOR
                ),
            )

    def test_email_sem_arroba_deve_ser_rejeitado(
        self,
    ):
        """
        Um endereço sem arroba é inválido.
        """

        with self.assertRaises(ValueError):
            usuarios.criar_dados_usuario(
                codigo=1,
                codigo_empresa=10,
                nome="Ana Souza",
                email="anaempresa.com.br",
                perfil=(
                    usuarios
                    .PERFIL_USUARIO_GESTOR
                ),
            )

    def test_email_sem_parte_local_deve_ser_rejeitado(
        self,
    ):
        """
        Deve existir conteúdo antes da arroba.
        """

        with self.assertRaises(ValueError):
            usuarios.criar_dados_usuario(
                codigo=1,
                codigo_empresa=10,
                nome="Ana Souza",
                email="@empresa.com.br",
                perfil=(
                    usuarios
                    .PERFIL_USUARIO_GESTOR
                ),
            )

    def test_email_sem_dominio_deve_ser_rejeitado(
        self,
    ):
        """
        Deve existir um domínio depois da arroba.
        """

        with self.assertRaises(ValueError):
            usuarios.criar_dados_usuario(
                codigo=1,
                codigo_empresa=10,
                nome="Ana Souza",
                email="ana@",
                perfil=(
                    usuarios
                    .PERFIL_USUARIO_GESTOR
                ),
            )

    def test_email_sem_ponto_no_dominio_deve_ser_rejeitado(
        self,
    ):
        """
        O domínio deve conter pelo menos um ponto.
        """

        with self.assertRaises(ValueError):
            usuarios.criar_dados_usuario(
                codigo=1,
                codigo_empresa=10,
                nome="Ana Souza",
                email="ana@empresa",
                perfil=(
                    usuarios
                    .PERFIL_USUARIO_GESTOR
                ),
            )

    def test_perfil_deve_ser_texto(
        self,
    ):
        """
        O perfil deve ser uma string.
        """

        with self.assertRaises(TypeError):
            usuarios.criar_dados_usuario(
                codigo=1,
                codigo_empresa=10,
                nome="Ana Souza",
                email="ana@empresa.com.br",
                perfil=1,
            )

    def test_perfil_invalido_deve_ser_rejeitado(
        self,
    ):
        """
        Um perfil fora da coleção oficial
        deve ser rejeitado.
        """

        with self.assertRaises(ValueError):
            usuarios.criar_dados_usuario(
                codigo=1,
                codigo_empresa=10,
                nome="Ana Souza",
                email="ana@empresa.com.br",
                perfil="SUPERUSUARIO",
            )

    def test_situacao_deve_ser_texto(
        self,
    ):
        """
        A situação deve ser uma string.
        """

        with self.assertRaises(TypeError):
            usuarios.criar_dados_usuario(
                codigo=1,
                codigo_empresa=10,
                nome="Ana Souza",
                email="ana@empresa.com.br",
                perfil=(
                    usuarios
                    .PERFIL_USUARIO_GESTOR
                ),
                situacao=1,
            )

    def test_situacao_invalida_deve_ser_rejeitada(
        self,
    ):
        """
        Uma situação fora da coleção oficial
        deve ser rejeitada.
        """

        with self.assertRaises(ValueError):
            usuarios.criar_dados_usuario(
                codigo=1,
                codigo_empresa=10,
                nome="Ana Souza",
                email="ana@empresa.com.br",
                perfil=(
                    usuarios
                    .PERFIL_USUARIO_GESTOR
                ),
                situacao="AFASTADO",
            )


class TestConsultasUsuario(
    unittest.TestCase
):
    """
    Testes de busca e existência de Usuários.
    """

    def setUp(
        self,
    ):
        """
        Cria uma coleção independente
        para cada teste.
        """

        self.usuario_empresa_10 = {
            "codigo": 1,
            "codigo_empresa": 10,
            "nome": "Ana Souza",
            "email": "ana@empresa10.com.br",
            "perfil": (
                usuarios
                .PERFIL_USUARIO_ADMINISTRADOR
            ),
            "situacao": (
                usuarios
                .SITUACAO_USUARIO_ATIVO
            ),
        }

        self.outro_usuario_empresa_10 = {
            "codigo": 2,
            "codigo_empresa": 10,
            "nome": "Bruno Lima",
            "email": "bruno@empresa10.com.br",
            "perfil": (
                usuarios
                .PERFIL_USUARIO_OPERACIONAL
            ),
            "situacao": (
                usuarios
                .SITUACAO_USUARIO_INATIVO
            ),
        }

        self.usuario_empresa_20 = {
            "codigo": 3,
            "codigo_empresa": 20,
            "nome": "Carlos Santos",
            "email": "carlos@empresa20.com.br",
            "perfil": (
                usuarios
                .PERFIL_USUARIO_GESTOR
            ),
            "situacao": (
                usuarios
                .SITUACAO_USUARIO_BLOQUEADO
            ),
        }

        self.usuarios = [
            self.usuario_empresa_10,
            self.outro_usuario_empresa_10,
            self.usuario_empresa_20,
        ]

    def test_buscar_usuario_por_codigo(
        self,
    ):
        """
        Deve retornar o usuário quando o código
        e a empresa correspondem.
        """

        resultado = (
            usuarios.buscar_usuario_por_codigo(
                usuarios=self.usuarios,
                codigo_usuario=1,
                codigo_empresa=10,
            )
        )

        self.assertIs(
            resultado,
            self.usuario_empresa_10,
        )

    def test_buscar_usuario_inexistente_retorna_none(
        self,
    ):
        """
        Código inexistente deve retornar None.
        """

        resultado = (
            usuarios.buscar_usuario_por_codigo(
                usuarios=self.usuarios,
                codigo_usuario=999,
                codigo_empresa=10,
            )
        )

        self.assertIsNone(
            resultado
        )

    def test_busca_respeita_isolamento_entre_empresas(
        self,
    ):
        """
        Um usuário existente não pode ser retornado
        dentro do contexto de outra empresa.

        Esta é uma das regras centrais de segurança
        do domínio da plataforma.
        """

        resultado = (
            usuarios.buscar_usuario_por_codigo(
                usuarios=self.usuarios,
                codigo_usuario=3,
                codigo_empresa=10,
            )
        )

        self.assertIsNone(
            resultado
        )

    def test_busca_retorna_usuario_na_empresa_correta(
        self,
    ):
        """
        O mesmo usuário deve ser encontrado quando
        a empresa correta for informada.
        """

        resultado = (
            usuarios.buscar_usuario_por_codigo(
                usuarios=self.usuarios,
                codigo_usuario=3,
                codigo_empresa=20,
            )
        )

        self.assertIs(
            resultado,
            self.usuario_empresa_20,
        )

    def test_buscar_usuario_por_email(
        self,
    ):
        """
        Deve localizar um usuário por seu e-mail.
        """

        resultado = (
            usuarios.buscar_usuario_por_email(
                self.usuarios,
                "ana@empresa10.com.br",
            )
        )

        self.assertIs(
            resultado,
            self.usuario_empresa_10,
        )

    def test_buscar_usuario_por_email_normaliza_entrada(
        self,
    ):
        """
        A busca por e-mail deve ignorar
        espaços externos e diferenças de caixa.
        """

        resultado = (
            usuarios.buscar_usuario_por_email(
                self.usuarios,
                "  ANA@EMPRESA10.COM.BR  ",
            )
        )

        self.assertIs(
            resultado,
            self.usuario_empresa_10,
        )

    def test_buscar_email_inexistente_retorna_none(
        self,
    ):
        """
        E-mail não cadastrado deve retornar None.
        """

        resultado = (
            usuarios.buscar_usuario_por_email(
                self.usuarios,
                "inexistente@empresa.com.br",
            )
        )

        self.assertIsNone(
            resultado
        )

    def test_codigo_usuario_existe(
        self,
    ):
        """
        Deve retornar True quando o código existe.
        """

        resultado = usuarios.codigo_usuario_existe(
            self.usuarios,
            2,
        )

        self.assertTrue(
            resultado
        )

    def test_codigo_usuario_nao_existe(
        self,
    ):
        """
        Deve retornar False quando o código
        não existe.
        """

        resultado = usuarios.codigo_usuario_existe(
            self.usuarios,
            999,
        )

        self.assertFalse(
            resultado
        )

    def test_email_usuario_existe(
        self,
    ):
        """
        Deve retornar True quando o e-mail
        já está cadastrado.
        """

        resultado = usuarios.email_usuario_existe(
            self.usuarios,
            "bruno@empresa10.com.br",
        )

        self.assertTrue(
            resultado
        )

    def test_email_usuario_existe_normaliza_entrada(
        self,
    ):
        """
        A verificação deve ignorar espaços
        externos e diferenças de caixa.
        """

        resultado = usuarios.email_usuario_existe(
            self.usuarios,
            "  BRUNO@EMPRESA10.COM.BR  ",
        )

        self.assertTrue(
            resultado
        )

    def test_email_usuario_nao_existe(
        self,
    ):
        """
        Deve retornar False para um e-mail
        ainda não cadastrado.
        """

        resultado = usuarios.email_usuario_existe(
            self.usuarios,
            "novo@empresa.com.br",
        )

        self.assertFalse(
            resultado
        )

    def test_busca_ignora_item_que_nao_seja_dicionario(
        self,
    ):
        """
        Itens inválidos dentro da coleção
        devem ser ignorados pela busca.
        """

        colecao = [
            "item inválido",
            self.usuario_empresa_10,
        ]

        resultado = (
            usuarios.buscar_usuario_por_codigo(
                usuarios=colecao,
                codigo_usuario=1,
                codigo_empresa=10,
            )
        )

        self.assertIs(
            resultado,
            self.usuario_empresa_10,
        )

    def test_colecao_usuarios_deve_ser_lista(
        self,
    ):
        """
        Uma coleção que não seja lista
        deve ser rejeitada.
        """

        with self.assertRaises(TypeError):
            usuarios.buscar_usuario_por_codigo(
                usuarios={},
                codigo_usuario=1,
                codigo_empresa=10,
            )


class TestListarUsuariosDaEmpresa(
    unittest.TestCase
):
    """
    Testes da listagem isolada
    por Empresa.
    """

    def setUp(
        self,
    ):
        """
        Cria usuários de empresas diferentes
        e fora da ordem alfabética.
        """

        self.usuario_zuleica = {
            "codigo": 1,
            "codigo_empresa": 10,
            "nome": "Zuleica Souza",
            "email": "zuleica@empresa.com.br",
        }

        self.usuario_ana = {
            "codigo": 2,
            "codigo_empresa": 10,
            "nome": "Ana Lima",
            "email": "ana@empresa.com.br",
        }

        self.usuario_bruno = {
            "codigo": 3,
            "codigo_empresa": 10,
            "nome": "bruno Costa",
            "email": "bruno@empresa.com.br",
        }

        self.usuario_outra_empresa = {
            "codigo": 4,
            "codigo_empresa": 20,
            "nome": "Carlos Santos",
            "email": "carlos@outraempresa.com.br",
        }

        self.usuarios = [
            self.usuario_zuleica,
            self.usuario_outra_empresa,
            self.usuario_bruno,
            self.usuario_ana,
        ]

    def test_lista_somente_usuarios_da_empresa(
        self,
    ):
        """
        A listagem não pode incluir usuários
        pertencentes a outra empresa.
        """

        resultado = (
            usuarios.listar_usuarios_da_empresa(
                self.usuarios,
                codigo_empresa=10,
            )
        )

        self.assertEqual(
            len(resultado),
            3,
        )

        self.assertNotIn(
            self.usuario_outra_empresa,
            resultado,
        )

    def test_lista_usuarios_ordenados_por_nome(
        self,
    ):
        """
        Os usuários da empresa devem ser
        ordenados alfabeticamente pelo nome.
        """

        resultado = (
            usuarios.listar_usuarios_da_empresa(
                self.usuarios,
                codigo_empresa=10,
            )
        )

        nomes = [
            usuario["nome"]
            for usuario in resultado
        ]

        self.assertEqual(
            nomes,
            [
                "Ana Lima",
                "bruno Costa",
                "Zuleica Souza",
            ],
        )

    def test_empresa_sem_usuarios_retorna_lista_vazia(
        self,
    ):
        """
        Uma empresa sem usuários deve produzir
        uma lista vazia.
        """

        resultado = (
            usuarios.listar_usuarios_da_empresa(
                self.usuarios,
                codigo_empresa=999,
            )
        )

        self.assertEqual(
            resultado,
            [],
        )

    def test_listagem_retorna_nova_lista(
        self,
    ):
        """
        A função deve retornar uma nova lista,
        sem devolver a coleção original.
        """

        resultado = (
            usuarios.listar_usuarios_da_empresa(
                self.usuarios,
                codigo_empresa=10,
            )
        )

        self.assertIsNot(
            resultado,
            self.usuarios,
        )

    def test_listagem_nao_altera_ordem_da_colecao_original(
        self,
    ):
        """
        A ordenação não deve modificar
        a lista recebida.
        """

        ordem_original = list(
            self.usuarios
        )

        usuarios.listar_usuarios_da_empresa(
            self.usuarios,
            codigo_empresa=10,
        )

        self.assertEqual(
            self.usuarios,
            ordem_original,
        )


class TestPerfilESituacaoUsuario(
    unittest.TestCase
):
    """
    Testes das funções de consulta
    sobre perfil e situação.
    """

    def setUp(
        self,
    ):
        """
        Cria usuários com estados diferentes.
        """

        self.usuario_ativo = {
            "codigo": 1,
            "codigo_empresa": 10,
            "nome": "Ana Souza",
            "perfil": (
                usuarios
                .PERFIL_USUARIO_ADMINISTRADOR
            ),
            "situacao": (
                usuarios
                .SITUACAO_USUARIO_ATIVO
            ),
        }

        self.usuario_cancelado = {
            "codigo": 2,
            "codigo_empresa": 10,
            "nome": "Carlos Souza",
            "perfil": (
                usuarios
                .PERFIL_USUARIO_CONSULTA
            ),
            "situacao": (
                usuarios
                .SITUACAO_USUARIO_CANCELADO
            ),
        }

    def test_usuario_esta_ativo(
        self,
    ):
        """
        Deve retornar True para usuário ativo.
        """

        resultado = usuarios.usuario_esta_ativo(
            self.usuario_ativo
        )

        self.assertTrue(
            resultado
        )

    def test_usuario_nao_esta_ativo(
        self,
    ):
        """
        Deve retornar False quando a situação
        não for ATIVO.
        """

        resultado = usuarios.usuario_esta_ativo(
            self.usuario_cancelado
        )

        self.assertFalse(
            resultado
        )

    def test_usuario_esta_cancelado(
        self,
    ):
        """
        Deve retornar True para usuário cancelado.
        """

        resultado = (
            usuarios.usuario_esta_cancelado(
                self.usuario_cancelado
            )
        )

        self.assertTrue(
            resultado
        )

    def test_usuario_nao_esta_cancelado(
        self,
    ):
        """
        Deve retornar False para usuário
        que não esteja cancelado.
        """

        resultado = (
            usuarios.usuario_esta_cancelado(
                self.usuario_ativo
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
        informado corresponde ao usuário.
        """

        resultado = usuarios.usuario_possui_perfil(
            self.usuario_ativo,
            "administrador",
        )

        self.assertTrue(
            resultado
        )

    def test_usuario_nao_possui_perfil(
        self,
    ):
        """
        Deve retornar False quando os perfis
        forem diferentes.
        """

        resultado = usuarios.usuario_possui_perfil(
            self.usuario_ativo,
            usuarios.PERFIL_USUARIO_GESTOR,
        )

        self.assertFalse(
            resultado
        )

    def test_consulta_situacao_exige_dicionario(
        self,
    ):
        """
        As funções de situação devem rejeitar
        um objeto que não seja dicionário.
        """

        with self.assertRaises(TypeError):
            usuarios.usuario_esta_ativo(
                "usuário inválido"
            )

    def test_consulta_cancelamento_exige_dicionario(
        self,
    ):
        """
        A consulta de cancelamento deve rejeitar
        um objeto que não seja dicionário.
        """

        with self.assertRaises(TypeError):
            usuarios.usuario_esta_cancelado(
                []
            )

    def test_consulta_perfil_exige_dicionario(
        self,
    ):
        """
        A consulta de perfil deve rejeitar
        um objeto que não seja dicionário.
        """

        with self.assertRaises(TypeError):
            usuarios.usuario_possui_perfil(
                None,
                usuarios.PERFIL_USUARIO_GESTOR,
            )

    def test_consulta_rejeita_perfil_invalido(
        self,
    ):
        """
        Mesmo em uma consulta, o perfil informado
        deve pertencer à coleção oficial.
        """

        with self.assertRaises(ValueError):
            usuarios.usuario_possui_perfil(
                self.usuario_ativo,
                "SUPERUSUARIO",
            )


class TestConstantesUsuario(
    unittest.TestCase
):
    """
    Testes das coleções oficiais
    de perfis e situações.
    """

    def test_perfis_usuario_contem_perfis_oficiais(
        self,
    ):
        """
        A coleção de perfis deve conter
        os quatro perfis iniciais.
        """

        self.assertEqual(
            usuarios.PERFIS_USUARIO,
            (
                usuarios
                .PERFIL_USUARIO_ADMINISTRADOR,
                usuarios.PERFIL_USUARIO_GESTOR,
                usuarios.PERFIL_USUARIO_OPERACIONAL,
                usuarios.PERFIL_USUARIO_CONSULTA,
            ),
        )

    def test_situacoes_usuario_contem_situacoes_oficiais(
        self,
    ):
        """
        A coleção de situações deve conter
        os quatro estados iniciais.
        """

        self.assertEqual(
            usuarios.SITUACOES_USUARIO,
            (
                usuarios.SITUACAO_USUARIO_ATIVO,
                usuarios.SITUACAO_USUARIO_INATIVO,
                usuarios.SITUACAO_USUARIO_BLOQUEADO,
                usuarios.SITUACAO_USUARIO_CANCELADO,
            ),
        )

class TestTransicoesSituacaoUsuario(
    unittest.TestCase
):
    """
    Testes das regras de transição
    de situação do Usuário.
    """

    def setUp(
        self,
    ):
        """
        Cria um Usuário válido para
        os testes de mudança de situação.
        """

        self.usuario = {
            "codigo": 1,
            "codigo_empresa": 10,
            "nome": "Ana Souza",
            "email": "ana@empresa.com.br",
            "perfil": (
                usuarios_dominio
                .PERFIL_USUARIO_GESTOR
            ),
            "situacao": (
                usuarios_dominio
                .SITUACAO_USUARIO_ATIVO
            ),
            "data_cadastro": (
                "2026-07-28T10:00:00"
            ),
            "data_atualizacao": (
                "2026-07-28T10:00:00"
            ),
        }

    def test_ativo_pode_ser_inativado(
        self,
    ):
        """
        Usuário ativo pode passar
        para a situação inativa.
        """

        resultado = (
            usuarios_dominio
            .transicao_situacao_usuario_permitida(
                situacao_atual="ATIVO",
                nova_situacao="INATIVO",
            )
        )

        self.assertTrue(
            resultado
        )

    def test_ativo_pode_ser_bloqueado(
        self,
    ):
        """
        Usuário ativo pode ser bloqueado.
        """

        resultado = (
            usuarios_dominio
            .transicao_situacao_usuario_permitida(
                situacao_atual="ATIVO",
                nova_situacao="BLOQUEADO",
            )
        )

        self.assertTrue(
            resultado
        )

    def test_ativo_pode_ser_cancelado(
        self,
    ):
        """
        Usuário ativo pode ser cancelado.
        """

        resultado = (
            usuarios_dominio
            .transicao_situacao_usuario_permitida(
                situacao_atual="ATIVO",
                nova_situacao="CANCELADO",
            )
        )

        self.assertTrue(
            resultado
        )

    def test_inativo_pode_ser_ativado(
        self,
    ):
        """
        Usuário inativo pode voltar
        para a situação ativa.
        """

        resultado = (
            usuarios_dominio
            .transicao_situacao_usuario_permitida(
                situacao_atual="INATIVO",
                nova_situacao="ATIVO",
            )
        )

        self.assertTrue(
            resultado
        )

    def test_inativo_pode_ser_bloqueado(
        self,
    ):
        """
        Usuário inativo pode ser bloqueado.
        """

        resultado = (
            usuarios_dominio
            .transicao_situacao_usuario_permitida(
                situacao_atual="INATIVO",
                nova_situacao="BLOQUEADO",
            )
        )

        self.assertTrue(
            resultado
        )

    def test_bloqueado_pode_ser_ativado(
        self,
    ):
        """
        Usuário bloqueado pode ser desbloqueado
        por meio da ativação.
        """

        resultado = (
            usuarios_dominio
            .transicao_situacao_usuario_permitida(
                situacao_atual="BLOQUEADO",
                nova_situacao="ATIVO",
            )
        )

        self.assertTrue(
            resultado
        )

    def test_bloqueado_pode_ser_inativado(
        self,
    ):
        """
        Usuário bloqueado pode ser inativado.
        """

        resultado = (
            usuarios_dominio
            .transicao_situacao_usuario_permitida(
                situacao_atual="BLOQUEADO",
                nova_situacao="INATIVO",
            )
        )

        self.assertTrue(
            resultado
        )

    def test_cancelado_nao_pode_ser_ativado(
        self,
    ):
        """
        Usuário cancelado não pode
        retornar à situação ativa.
        """

        resultado = (
            usuarios_dominio
            .transicao_situacao_usuario_permitida(
                situacao_atual="CANCELADO",
                nova_situacao="ATIVO",
            )
        )

        self.assertFalse(
            resultado
        )

    def test_cancelado_nao_pode_ser_inativado(
        self,
    ):
        """
        Usuário cancelado não pode
        passar para inativo.
        """

        resultado = (
            usuarios_dominio
            .transicao_situacao_usuario_permitida(
                situacao_atual="CANCELADO",
                nova_situacao="INATIVO",
            )
        )

        self.assertFalse(
            resultado
        )

    def test_nao_permitir_mesma_situacao(
        self,
    ):
        """
        Não deve existir transição
        para a situação atual.
        """

        resultado = (
            usuarios_dominio
            .transicao_situacao_usuario_permitida(
                situacao_atual="ATIVO",
                nova_situacao="ATIVO",
            )
        )

        self.assertFalse(
            resultado
        )

    def test_rejeitar_situacao_atual_invalida(
        self,
    ):
        """
        Situação atual fora da coleção oficial
        deve gerar ValueError.
        """

        with self.assertRaisesRegex(
            ValueError,
            "Situação atual inválida",
        ):
            (
                usuarios_dominio
                .transicao_situacao_usuario_permitida(
                    situacao_atual="DESCONHECIDO",
                    nova_situacao="ATIVO",
                )
            )

    def test_rejeitar_nova_situacao_invalida(
        self,
    ):
        """
        Nova situação fora da coleção oficial
        deve gerar ValueError.
        """

        with self.assertRaisesRegex(
            ValueError,
            "Nova situação inválida",
        ):
            (
                usuarios_dominio
                .transicao_situacao_usuario_permitida(
                    situacao_atual="ATIVO",
                    nova_situacao="DESCONHECIDO",
                )
            )

    def test_alterar_situacao_usuario(
        self,
    ):
        """
        Uma transição válida deve alterar
        a situação do Usuário.
        """

        resultado = (
            usuarios_dominio
            .alterar_situacao_usuario(
                usuario=self.usuario,
                nova_situacao="INATIVO",
            )
        )

        self.assertIs(
            resultado,
            self.usuario,
        )

        self.assertEqual(
            resultado["situacao"],
            "INATIVO",
        )

    def test_alterar_situacao_normaliza_entrada(
        self,
    ):
        """
        A nova situação deve aceitar
        espaços e letras minúsculas.
        """

        resultado = (
            usuarios_dominio
            .alterar_situacao_usuario(
                usuario=self.usuario,
                nova_situacao="  bloqueado  ",
            )
        )

        self.assertEqual(
            resultado["situacao"],
            "BLOQUEADO",
        )

    def test_alterar_situacao_atualiza_data(
        self,
    ):
        """
        Uma alteração válida deve atualizar
        data_atualizacao.
        """

        data_anterior = (
            self.usuario["data_atualizacao"]
        )

        resultado = (
            usuarios_dominio
            .alterar_situacao_usuario(
                usuario=self.usuario,
                nova_situacao="INATIVO",
            )
        )

        self.assertNotEqual(
            resultado["data_atualizacao"],
            data_anterior,
        )

    def test_alteracao_invalida_nao_modifica_usuario(
        self,
    ):
        """
        Uma transição inválida não deve
        modificar os dados do Usuário.
        """

        self.usuario["situacao"] = "CANCELADO"

        dados_anteriores = self.usuario.copy()

        with self.assertRaisesRegex(
            ValueError,
            "Transição de situação não permitida",
        ):
            (
                usuarios_dominio
                .alterar_situacao_usuario(
                    usuario=self.usuario,
                    nova_situacao="ATIVO",
                )
            )

        self.assertEqual(
            self.usuario,
            dados_anteriores,
        )

    def test_rejeitar_usuario_que_nao_seja_dicionario(
        self,
    ):
        """
        O Usuário recebido deve ser
        obrigatoriamente um dicionário.
        """

        with self.assertRaisesRegex(
            TypeError,
            "Usuário deve ser um dicionário",
        ):
            (
                usuarios_dominio
                .alterar_situacao_usuario(
                    usuario="Usuário inválido",
                    nova_situacao="INATIVO",
                )
            )

    def test_rejeitar_usuario_sem_situacao(
        self,
    ):
        """
        Um Usuário sem situação não pode
        ter seu estado alterado.
        """

        self.usuario.pop(
            "situacao"
        )

        with self.assertRaisesRegex(
            ValueError,
            "Situação atual do Usuário inválida",
        ):
            (
                usuarios_dominio
                .alterar_situacao_usuario(
                    usuario=self.usuario,
                    nova_situacao="INATIVO",
                )
            )

if __name__ == "__main__":
    unittest.main()