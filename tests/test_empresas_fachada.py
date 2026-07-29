"""
Testes da fachada de empresas.

Estes testes verificam a coordenação entre:

- fachada;
- domínio;
- persistência.

O arquivo real data/empresas.json não será alterado.
"""

import unittest
from unittest.mock import patch

from app import empresas
from app.dominio.empresas import (
    SITUACAO_EMPRESA_ATIVA,
    SITUACAO_EMPRESA_CANCELADA,
    SITUACAO_EMPRESA_INATIVA,
    SITUACAO_EMPRESA_SUSPENSA,
    criar_dados_empresa,
)


class TestEmpresasFachada(unittest.TestCase):
    """
    Testa as funções públicas da fachada de empresas.
    """

    def setUp(self):
        """
        Substitui temporariamente a coleção real da fachada.

        Também guarda a referência original para restaurá-la
        depois de cada teste.
        """

        self.empresas_originais = empresas.empresas

        empresas.empresas = []

        self.empresa_solar_bahia = criar_dados_empresa(
            codigo=1,
            razao_social="Solar Energia Bahia Ltda",
            nome_fantasia="Solar Bahia",
            cnpj="11.222.333/0001-81",
            email="contato@solarbahia.com.br",
            telefone="(77) 99999-9999",
        )

        self.empresa_energia_sertao = criar_dados_empresa(
            codigo=2,
            razao_social="Energia do Sertão Ltda",
            nome_fantasia="Energia Sertão",
            cnpj="45.723.174/0001-10",
            email="contato@energiasertao.com.br",
            telefone="(77) 98888-7777",
        )

    def tearDown(self):
        """
        Restaura a coleção original após cada teste.
        """

        empresas.empresas = self.empresas_originais

    # ========================================================
    # CADASTRO
    # ========================================================

    @patch("app.empresas.salvar_empresas")
    def test_cadastrar_empresa(self, salvar_empresas_mock):
        """
        Deve cadastrar uma nova empresa na coleção.
        """

        empresa_cadastrada = empresas.cadastrar_empresa(
            razao_social="Solar Oeste Engenharia Ltda",
            nome_fantasia="Solar Oeste",
            cnpj="12.345.678/0001-95",
            email="contato@solaroeste.com.br",
            telefone="(77) 97777-6666",
        )

        self.assertEqual(
            empresa_cadastrada["codigo"],
            1,
        )

        self.assertEqual(
            empresa_cadastrada["razao_social"],
            "Solar Oeste Engenharia Ltda",
        )

        self.assertEqual(
            empresa_cadastrada["nome_fantasia"],
            "Solar Oeste",
        )

        self.assertEqual(
            empresa_cadastrada["cnpj"],
            "12345678000195",
        )

        self.assertEqual(
            empresa_cadastrada["situacao"],
            SITUACAO_EMPRESA_ATIVA,
        )

        self.assertEqual(
            len(empresas.empresas),
            1,
        )

        salvar_empresas_mock.assert_called_once_with(
            empresas.empresas,
        )

    @patch("app.empresas.salvar_empresas")
    def test_cadastrar_empresa_gera_codigo_sequencial(
        self,
        salvar_empresas_mock,
    ):
        """
        O novo código deve ser gerado com base na coleção atual.
        """

        empresas.empresas = [
            self.empresa_solar_bahia,
            self.empresa_energia_sertao,
        ]

        empresa_cadastrada = empresas.cadastrar_empresa(
            razao_social="Solar Oeste Engenharia Ltda",
            nome_fantasia="Solar Oeste",
            cnpj="12.345.678/0001-95",
            email="contato@solaroeste.com.br",
            telefone="(77) 97777-6666",
        )

        self.assertEqual(
            empresa_cadastrada["codigo"],
            3,
        )

        salvar_empresas_mock.assert_called_once_with(
            empresas.empresas,
        )

    @patch("app.empresas.salvar_empresas")
    def test_cadastrar_empresa_com_codigos_nao_sequenciais(
        self,
        salvar_empresas_mock,
    ):
        """
        A geração deve considerar o maior código existente.
        """

        empresa_codigo_cinco = criar_dados_empresa(
            codigo=5,
            razao_social="Empresa Cinco Ltda",
            nome_fantasia="Empresa Cinco",
            cnpj="19.131.243/0001-97",
            email="contato@empresacinco.com.br",
            telefone="(77) 96666-5555",
        )

        empresas.empresas = [
            self.empresa_solar_bahia,
            empresa_codigo_cinco,
        ]

        empresa_cadastrada = empresas.cadastrar_empresa(
            razao_social="Solar Oeste Engenharia Ltda",
            nome_fantasia="Solar Oeste",
            cnpj="12.345.678/0001-95",
            email="contato@solaroeste.com.br",
            telefone="(77) 97777-6666",
        )

        self.assertEqual(
            empresa_cadastrada["codigo"],
            6,
        )

        salvar_empresas_mock.assert_called_once_with(
            empresas.empresas,
        )

    @patch("app.empresas.salvar_empresas")
    def test_cadastrar_empresa_salva_alteracoes(
        self,
        salvar_empresas_mock,
    ):
        """
        O cadastro deve solicitar a persistência da coleção.
        """

        empresas.cadastrar_empresa(
            razao_social="Solar Oeste Engenharia Ltda",
            nome_fantasia="Solar Oeste",
            cnpj="12.345.678/0001-95",
            email="contato@solaroeste.com.br",
            telefone="(77) 97777-6666",
        )

        salvar_empresas_mock.assert_called_once_with(
            empresas.empresas,
        )

    @patch("app.empresas.salvar_empresas")
    def test_cadastrar_empresa_rejeita_cnpj_duplicado(
        self,
        salvar_empresas_mock,
    ):
        """
        Não deve permitir duas empresas com o mesmo CNPJ.
        """

        empresas.empresas = [
            self.empresa_solar_bahia,
        ]

        with self.assertRaises(ValueError):
            empresas.cadastrar_empresa(
                razao_social="Outra Razão Social Ltda",
                nome_fantasia="Outra Empresa",
                cnpj="11.222.333/0001-81",
                email="outro@email.com.br",
                telefone="(77) 97777-6666",
            )

        self.assertEqual(
            len(empresas.empresas),
            1,
        )

        salvar_empresas_mock.assert_not_called()

    @patch("app.empresas.salvar_empresas")
    def test_cadastrar_empresa_rejeita_cnpj_duplicado_sem_mascara(
        self,
        salvar_empresas_mock,
    ):
        """
        A verificação de duplicidade deve ignorar a máscara.
        """

        empresas.empresas = [
            self.empresa_solar_bahia,
        ]

        with self.assertRaises(ValueError):
            empresas.cadastrar_empresa(
                razao_social="Outra Empresa Ltda",
                nome_fantasia="Outra Empresa",
                cnpj="11222333000181",
                email="outro@email.com.br",
                telefone="77977776666",
            )

        salvar_empresas_mock.assert_not_called()

    @patch("app.empresas.salvar_empresas")
    def test_cadastro_invalido_nao_altera_colecao(
        self,
        salvar_empresas_mock,
    ):
        """
        Dados inválidos não devem gerar cadastro parcial.
        """

        with self.assertRaises(ValueError):
            empresas.cadastrar_empresa(
                razao_social="Empresa Teste Ltda",
                nome_fantasia="Empresa Teste",
                cnpj="CNPJ inválido",
                email="contato@empresa.com.br",
                telefone="77999999999",
            )

        self.assertEqual(
            empresas.empresas,
            [],
        )

        salvar_empresas_mock.assert_not_called()

    # ========================================================
    # BUSCAS
    # ========================================================

    def test_buscar_empresa(self):
        """
        Deve localizar uma empresa pelo código.
        """

        empresas.empresas = [
            self.empresa_solar_bahia,
            self.empresa_energia_sertao,
        ]

        empresa_encontrada = empresas.buscar_empresa(
            2,
        )

        self.assertIsNotNone(
            empresa_encontrada,
        )

        self.assertEqual(
            empresa_encontrada["nome_fantasia"],
            "Energia Sertão",
        )

    def test_buscar_empresa_inexistente(self):
        """
        Deve retornar None quando a empresa não existir.
        """

        empresas.empresas = [
            self.empresa_solar_bahia,
        ]

        empresa_encontrada = empresas.buscar_empresa(
            999,
        )

        self.assertIsNone(
            empresa_encontrada,
        )

    def test_obter_empresa(self):
        """
        Deve retornar obrigatoriamente uma empresa existente.
        """

        empresas.empresas = [
            self.empresa_solar_bahia,
        ]

        empresa_encontrada = empresas.obter_empresa(
            1,
        )

        self.assertEqual(
            empresa_encontrada["codigo"],
            1,
        )

    def test_obter_empresa_inexistente(self):
        """
        Deve gerar ValueError quando a empresa não existir.
        """

        empresas.empresas = [
            self.empresa_solar_bahia,
        ]

        with self.assertRaises(ValueError):
            empresas.obter_empresa(
                999,
            )

    def test_buscar_empresa_com_cnpj(self):
        """
        Deve localizar uma empresa pelo CNPJ.
        """

        empresas.empresas = [
            self.empresa_solar_bahia,
        ]

        empresa_encontrada = empresas.buscar_empresa_com_cnpj(
            "11.222.333/0001-81",
        )

        self.assertIsNotNone(
            empresa_encontrada,
        )

        self.assertEqual(
            empresa_encontrada["codigo"],
            1,
        )

    def test_buscar_empresa_com_cnpj_inexistente(self):
        """
        Deve retornar None quando o CNPJ não estiver cadastrado.
        """

        empresas.empresas = [
            self.empresa_solar_bahia,
        ]

        empresa_encontrada = empresas.buscar_empresa_com_cnpj(
            "98.765.432/0001-98",
        )

        self.assertIsNone(
            empresa_encontrada,
        )

    # ========================================================
    # LISTAGENS
    # ========================================================

    def test_listar_empresas(self):
        """
        Deve retornar todas as empresas cadastradas.
        """

        empresas.empresas = [
            self.empresa_solar_bahia,
            self.empresa_energia_sertao,
        ]

        resultado = empresas.listar_empresas()

        self.assertEqual(
            len(resultado),
            2,
        )

    def test_listar_empresas_retorna_nova_lista(self):
        """
        A lista retornada não deve ser a coleção interna.
        """

        empresas.empresas = [
            self.empresa_solar_bahia,
        ]

        resultado = empresas.listar_empresas()

        self.assertIsNot(
            resultado,
            empresas.empresas,
        )

    def test_alterar_lista_retornada_nao_altera_colecao(self):
        """
        Adicionar itens à lista retornada não deve alterar a fachada.
        """

        empresas.empresas = [
            self.empresa_solar_bahia,
        ]

        resultado = empresas.listar_empresas()

        resultado.append(
            self.empresa_energia_sertao,
        )

        self.assertEqual(
            len(resultado),
            2,
        )

        self.assertEqual(
            len(empresas.empresas),
            1,
        )

    def test_listar_empresas_ordenadas_por_nome(self):
        """
        Deve ordenar as empresas pelo nome fantasia.
        """

        empresas.empresas = [
            self.empresa_solar_bahia,
            self.empresa_energia_sertao,
        ]

        resultado = empresas.listar_empresas(
            ordenar_por_nome=True,
        )

        self.assertEqual(
            resultado[0]["nome_fantasia"],
            "Energia Sertão",
        )

        self.assertEqual(
            resultado[1]["nome_fantasia"],
            "Solar Bahia",
        )

    def test_listar_empresas_ativas(self):
        """
        Deve retornar somente empresas ativas.
        """

        self.empresa_energia_sertao["situacao"] = (
            SITUACAO_EMPRESA_INATIVA
        )

        empresas.empresas = [
            self.empresa_solar_bahia,
            self.empresa_energia_sertao,
        ]

        resultado = empresas.listar_empresas_ativas()

        self.assertEqual(
            len(resultado),
            1,
        )

        self.assertEqual(
            resultado[0]["codigo"],
            1,
        )

    def test_listar_empresas_por_situacao(self):
        """
        Deve filtrar empresas pela situação informada.
        """

        self.empresa_solar_bahia["situacao"] = (
            SITUACAO_EMPRESA_SUSPENSA
        )

        empresas.empresas = [
            self.empresa_solar_bahia,
            self.empresa_energia_sertao,
        ]

        resultado = empresas.listar_empresas_por_situacao(
            "suspensa",
        )

        self.assertEqual(
            len(resultado),
            1,
        )

        self.assertEqual(
            resultado[0]["codigo"],
            1,
        )

    def test_listar_empresas_por_situacao_invalida(self):
        """
        Situações desconhecidas devem ser rejeitadas.
        """

        with self.assertRaises(ValueError):
            empresas.listar_empresas_por_situacao(
                "EM_ANALISE",
            )

    def test_quantidade_empresas(self):
        """
        Deve retornar a quantidade total de empresas.
        """

        empresas.empresas = [
            self.empresa_solar_bahia,
            self.empresa_energia_sertao,
        ]

        resultado = empresas.quantidade_empresas()

        self.assertEqual(
            resultado,
            2,
        )

    def test_empresa_existe(self):
        """
        Deve retornar True quando a empresa existir.
        """

        empresas.empresas = [
            self.empresa_solar_bahia,
        ]

        resultado = empresas.empresa_existe(
            1,
        )

        self.assertTrue(
            resultado,
        )

    def test_empresa_nao_existe(self):
        """
        Deve retornar False quando a empresa não existir.
        """

        empresas.empresas = [
            self.empresa_solar_bahia,
        ]

        resultado = empresas.empresa_existe(
            999,
        )

        self.assertFalse(
            resultado,
        )

    # ========================================================
    # ALTERAÇÃO DE SITUAÇÃO
    # ========================================================

    @patch("app.empresas.salvar_empresas")
    def test_inativar_empresa(
        self,
        salvar_empresas_mock,
    ):
        """
        Deve inativar e persistir a empresa.
        """

        empresas.empresas = [
            self.empresa_solar_bahia,
        ]

        empresa_alterada = empresas.inativar_empresa(
            1,
        )

        self.assertEqual(
            empresa_alterada["situacao"],
            SITUACAO_EMPRESA_INATIVA,
        )

        salvar_empresas_mock.assert_called_once_with(
            empresas.empresas,
        )

    @patch("app.empresas.salvar_empresas")
    def test_suspender_empresa(
        self,
        salvar_empresas_mock,
    ):
        """
        Deve suspender e persistir a empresa.
        """

        empresas.empresas = [
            self.empresa_solar_bahia,
        ]

        empresa_alterada = empresas.suspender_empresa(
            1,
        )

        self.assertEqual(
            empresa_alterada["situacao"],
            SITUACAO_EMPRESA_SUSPENSA,
        )

        salvar_empresas_mock.assert_called_once_with(
            empresas.empresas,
        )

    @patch("app.empresas.salvar_empresas")
    def test_cancelar_empresa(
        self,
        salvar_empresas_mock,
    ):
        """
        Deve cancelar e persistir a empresa.
        """

        empresas.empresas = [
            self.empresa_solar_bahia,
        ]

        empresa_alterada = empresas.cancelar_empresa(
            1,
        )

        self.assertEqual(
            empresa_alterada["situacao"],
            SITUACAO_EMPRESA_CANCELADA,
        )

        salvar_empresas_mock.assert_called_once_with(
            empresas.empresas,
        )

    @patch("app.empresas.salvar_empresas")
    def test_ativar_empresa(
        self,
        salvar_empresas_mock,
    ):
        """
        Deve ativar e persistir a empresa.
        """

        self.empresa_solar_bahia["situacao"] = (
            SITUACAO_EMPRESA_INATIVA
        )

        empresas.empresas = [
            self.empresa_solar_bahia,
        ]

        empresa_alterada = empresas.ativar_empresa(
            1,
        )

        self.assertEqual(
            empresa_alterada["situacao"],
            SITUACAO_EMPRESA_ATIVA,
        )

        salvar_empresas_mock.assert_called_once_with(
            empresas.empresas,
        )

    @patch("app.empresas.salvar_empresas")
    def test_inativar_empresa_inexistente(
        self,
        salvar_empresas_mock,
    ):
        """
        Não deve persistir quando a empresa não existir.
        """

        empresas.empresas = [
            self.empresa_solar_bahia,
        ]

        with self.assertRaises(ValueError):
            empresas.inativar_empresa(
                999,
            )

        salvar_empresas_mock.assert_not_called()

    @patch("app.empresas.salvar_empresas")
    def test_suspender_empresa_inexistente(
        self,
        salvar_empresas_mock,
    ):
        """
        A suspensão exige uma empresa existente.
        """

        with self.assertRaises(ValueError):
            empresas.suspender_empresa(
                999,
            )

        salvar_empresas_mock.assert_not_called()

    @patch("app.empresas.salvar_empresas")
    def test_cancelar_empresa_inexistente(
        self,
        salvar_empresas_mock,
    ):
        """
        O cancelamento exige uma empresa existente.
        """

        with self.assertRaises(ValueError):
            empresas.cancelar_empresa(
                999,
            )

        salvar_empresas_mock.assert_not_called()

    @patch("app.empresas.salvar_empresas")
    def test_ativar_empresa_inexistente(
        self,
        salvar_empresas_mock,
    ):
        """
        A ativação exige uma empresa existente.
        """

        with self.assertRaises(ValueError):
            empresas.ativar_empresa(
                999,
            )

        salvar_empresas_mock.assert_not_called()

        # ========================================================
    # REGRAS DE TRANSIÇÃO NA FACHADA
    # ========================================================

    @patch("app.empresas.salvar_empresas")
    def test_ativar_empresa_ja_ativa_nao_persiste(
        self,
        salvar_empresas_mock,
    ):
        """
        Uma transição inválida não deve gerar persistência.
        """

        empresas.empresas = [
            self.empresa_solar_bahia,
        ]

        with self.assertRaises(ValueError):
            empresas.ativar_empresa(
                1,
            )

        salvar_empresas_mock.assert_not_called()

    @patch("app.empresas.salvar_empresas")
    def test_empresa_cancelada_nao_pode_ser_reativada_na_fachada(
        self,
        salvar_empresas_mock,
    ):
        """
        A fachada deve respeitar o estado terminal CANCELADA.
        """

        self.empresa_solar_bahia["situacao"] = (
            SITUACAO_EMPRESA_CANCELADA
        )

        empresas.empresas = [
            self.empresa_solar_bahia,
        ]

        with self.assertRaises(ValueError):
            empresas.ativar_empresa(
                1,
            )

        salvar_empresas_mock.assert_not_called()

    @patch("app.empresas.salvar_empresas")
    def test_empresa_inativa_nao_pode_ser_suspensa_na_fachada(
        self,
        salvar_empresas_mock,
    ):
        """
        INATIVA não pode avançar diretamente para SUSPENSA.
        """

        self.empresa_solar_bahia["situacao"] = (
            SITUACAO_EMPRESA_INATIVA
        )

        empresas.empresas = [
            self.empresa_solar_bahia,
        ]

        with self.assertRaises(ValueError):
            empresas.suspender_empresa(
                1,
            )

        salvar_empresas_mock.assert_not_called()

    @patch("app.empresas.salvar_empresas")
    def test_empresa_suspensa_pode_ser_reativada_na_fachada(
        self,
        salvar_empresas_mock,
    ):
        """
        Uma empresa suspensa pode retornar ao estado ATIVA.
        """

        self.empresa_solar_bahia["situacao"] = (
            SITUACAO_EMPRESA_SUSPENSA
        )

        empresas.empresas = [
            self.empresa_solar_bahia,
        ]

        empresa_alterada = empresas.ativar_empresa(
            1,
        )

        self.assertEqual(
            empresa_alterada["situacao"],
            SITUACAO_EMPRESA_ATIVA,
        )

        salvar_empresas_mock.assert_called_once_with(
            empresas.empresas,
        )

    # ========================================================
    # EDIÇÃO DOS DADOS CADASTRAIS
    # ========================================================

    @patch("app.empresas.salvar_empresas")
    def test_editar_empresa(
        self,
        salvar_empresas_mock,
    ):
        """
        Deve editar uma empresa existente e persistir a coleção.
        """

        empresas.empresas = [
            self.empresa_solar_bahia,
        ]

        empresa_atualizada = empresas.editar_empresa(
            codigo_empresa=1,
            razao_social="Solar Bahia Engenharia Ltda",
            nome_fantasia="Solar Bahia Engenharia",
            email="novo@solarbahia.com.br",
            telefone="(77) 98888-0000",
        )

        self.assertEqual(
            empresa_atualizada["razao_social"],
            "Solar Bahia Engenharia Ltda",
        )

        self.assertEqual(
            empresa_atualizada["nome_fantasia"],
            "Solar Bahia Engenharia",
        )

        self.assertEqual(
            empresa_atualizada["email"],
            "novo@solarbahia.com.br",
        )

        self.assertEqual(
            empresa_atualizada["telefone"],
            "77988880000",
        )

        salvar_empresas_mock.assert_called_once_with(
            empresas.empresas,
        )

    @patch("app.empresas.salvar_empresas")
    def test_editar_apenas_um_campo(
        self,
        salvar_empresas_mock,
    ):
        """
        Deve preservar os campos que não foram informados.
        """

        empresas.empresas = [
            self.empresa_solar_bahia,
        ]

        cnpj_original = self.empresa_solar_bahia["cnpj"]
        email_original = self.empresa_solar_bahia["email"]

        empresa_atualizada = empresas.editar_empresa(
            codigo_empresa=1,
            nome_fantasia="Solar Bahia Premium",
        )

        self.assertEqual(
            empresa_atualizada["nome_fantasia"],
            "Solar Bahia Premium",
        )

        self.assertEqual(
            empresa_atualizada["cnpj"],
            cnpj_original,
        )

        self.assertEqual(
            empresa_atualizada["email"],
            email_original,
        )

        salvar_empresas_mock.assert_called_once_with(
            empresas.empresas,
        )

    @patch("app.empresas.salvar_empresas")
    def test_editar_empresa_inexistente(
        self,
        salvar_empresas_mock,
    ):
        """
        Não deve persistir quando a empresa não existir.
        """

        empresas.empresas = [
            self.empresa_solar_bahia,
        ]

        with self.assertRaises(ValueError):
            empresas.editar_empresa(
                codigo_empresa=999,
                nome_fantasia="Novo Nome",
            )

        salvar_empresas_mock.assert_not_called()

    @patch("app.empresas.salvar_empresas")
    def test_editar_empresa_sem_campos(
        self,
        salvar_empresas_mock,
    ):
        """
        Não deve persistir quando nenhuma alteração for informada.
        """

        empresas.empresas = [
            self.empresa_solar_bahia,
        ]

        with self.assertRaises(ValueError):
            empresas.editar_empresa(
                codigo_empresa=1,
            )

        salvar_empresas_mock.assert_not_called()

    @patch("app.empresas.salvar_empresas")
    def test_editar_empresa_com_email_invalido(
        self,
        salvar_empresas_mock,
    ):
        """
        Uma edição inválida não deve ser persistida.
        """

        empresas.empresas = [
            self.empresa_solar_bahia,
        ]

        with self.assertRaises(ValueError):
            empresas.editar_empresa(
                codigo_empresa=1,
                email="email-invalido",
            )

        salvar_empresas_mock.assert_not_called()

    @patch("app.empresas.salvar_empresas")
    def test_editar_empresa_preserva_cnpj(
        self,
        salvar_empresas_mock,
    ):
        """
        A edição cadastral não deve alterar o CNPJ.
        """

        empresas.empresas = [
            self.empresa_solar_bahia,
        ]

        cnpj_original = self.empresa_solar_bahia["cnpj"]

        empresa_atualizada = empresas.editar_empresa(
            codigo_empresa=1,
            razao_social="Nova Razão Social Ltda",
        )

        self.assertEqual(
            empresa_atualizada["cnpj"],
            cnpj_original,
        )

        salvar_empresas_mock.assert_called_once_with(
            empresas.empresas,
        )

    # ========================================================
    # CONSULTA DAS TRANSIÇÕES PERMITIDAS
    # ========================================================

    def test_listar_transicoes_de_empresa_ativa(self):
        """
        A fachada deve retornar as transições disponíveis
        para uma empresa ativa.
        """

        empresas.empresas = [
            self.empresa_solar_bahia,
        ]

        transicoes = empresas.listar_transicoes_permitidas(
            1,
        )

        self.assertEqual(
            transicoes,
            (
                SITUACAO_EMPRESA_INATIVA,
                SITUACAO_EMPRESA_SUSPENSA,
                SITUACAO_EMPRESA_CANCELADA,
            ),
        )

    def test_listar_transicoes_de_empresa_inativa(self):
        """
        Uma empresa inativa pode ser ativada ou cancelada.
        """

        self.empresa_solar_bahia["situacao"] = (
            SITUACAO_EMPRESA_INATIVA
        )

        empresas.empresas = [
            self.empresa_solar_bahia,
        ]

        transicoes = empresas.listar_transicoes_permitidas(
            1,
        )

        self.assertEqual(
            transicoes,
            (
                SITUACAO_EMPRESA_ATIVA,
                SITUACAO_EMPRESA_CANCELADA,
            ),
        )

    def test_listar_transicoes_de_empresa_suspensa(self):
        """
        Uma empresa suspensa pode ser ativada, inativada
        ou cancelada.
        """

        self.empresa_solar_bahia["situacao"] = (
            SITUACAO_EMPRESA_SUSPENSA
        )

        empresas.empresas = [
            self.empresa_solar_bahia,
        ]

        transicoes = empresas.listar_transicoes_permitidas(
            1,
        )

        self.assertEqual(
            transicoes,
            (
                SITUACAO_EMPRESA_ATIVA,
                SITUACAO_EMPRESA_INATIVA,
                SITUACAO_EMPRESA_CANCELADA,
            ),
        )

    def test_listar_transicoes_de_empresa_cancelada(self):
        """
        Uma empresa cancelada não possui transições.
        """

        self.empresa_solar_bahia["situacao"] = (
            SITUACAO_EMPRESA_CANCELADA
        )

        empresas.empresas = [
            self.empresa_solar_bahia,
        ]

        transicoes = empresas.listar_transicoes_permitidas(
            1,
        )

        self.assertEqual(
            transicoes,
            (),
        )

    def test_listar_transicoes_de_empresa_inexistente(self):
        """
        A consulta exige uma empresa existente.
        """

        empresas.empresas = [
            self.empresa_solar_bahia,
        ]

        with self.assertRaises(ValueError):
            empresas.listar_transicoes_permitidas(
                999,
            )

if __name__ == "__main__":
    unittest.main()