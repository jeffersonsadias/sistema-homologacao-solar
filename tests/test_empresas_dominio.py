"""
Testes do domínio de empresas.

Esses testes verificam apenas regras de negócio e transformação
dos dados. Nenhum arquivo JSON é lido ou gravado aqui.
"""

import unittest

from app.dominio.empresas import (
    SITUACAO_EMPRESA_ATIVA,
    SITUACAO_EMPRESA_INATIVA,
    SITUACAO_EMPRESA_SUSPENSA,
    SITUACAO_EMPRESA_CANCELADA,
    TRANSICOES_SITUACAO_EMPRESA,
    criar_dados_empresa,
    buscar_empresa_por_codigo,
    buscar_empresa_por_cnpj,
    codigo_empresa_existe,
    cnpj_empresa_existe,
    ordenar_empresas_por_nome,
    empresa_esta_ativa,
    empresa_esta_cancelada,
    obter_transicoes_permitidas_empresa,
    transicao_situacao_empresa_permitida,
    alterar_situacao_empresa,
    ativar_empresa,
    inativar_empresa,
    suspender_empresa,
    cancelar_empresa,
    atualizar_dados_empresa,
)


class TestEmpresasDominio(unittest.TestCase):
    """
    Testa as funções públicas do domínio de empresas.
    """

    def setUp(self):
        """
        Cria dados reutilizados por vários testes.

        O método setUp é executado antes de cada teste.
        """

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

        self.empresas = [
            self.empresa_solar_bahia,
            self.empresa_energia_sertao,
        ]

    # ========================================================
    # CRIAÇÃO DA EMPRESA
    # ========================================================

    def test_criar_dados_empresa(self):
        """
        Verifica se a empresa é criada com os campos esperados.
        """

        empresa = criar_dados_empresa(
            codigo=3,
            razao_social="Solar Oeste Engenharia Ltda",
            nome_fantasia="Solar Oeste",
            cnpj="12.345.678/0001-95",
            email="contato@solaroeste.com.br",
            telefone="(77) 97777-6666",
        )

        self.assertEqual(
            empresa["codigo"],
            3,
        )

        self.assertEqual(
            empresa["razao_social"],
            "Solar Oeste Engenharia Ltda",
        )

        self.assertEqual(
            empresa["nome_fantasia"],
            "Solar Oeste",
        )

        self.assertEqual(
            empresa["cnpj"],
            "12345678000195",
        )

        self.assertEqual(
            empresa["email"],
            "contato@solaroeste.com.br",
        )

        self.assertEqual(
            empresa["telefone"],
            "77977776666",
        )

        self.assertEqual(
            empresa["situacao"],
            SITUACAO_EMPRESA_ATIVA,
        )

        self.assertIn(
            "data_cadastro",
            empresa,
        )

        self.assertIn(
            "data_atualizacao",
            empresa,
        )

    def test_criar_empresa_normaliza_textos(self):
        """
        Verifica se espaços excessivos são removidos.
        """

        empresa = criar_dados_empresa(
            codigo=3,
            razao_social="  Solar   Oeste   Ltda  ",
            nome_fantasia="  Solar   Oeste  ",
            cnpj="12.345.678/0001-95",
            email="  CONTATO@SOLAROESTE.COM.BR  ",
            telefone="  (77) 97777-6666  ",
        )

        self.assertEqual(
            empresa["razao_social"],
            "Solar Oeste Ltda",
        )

        self.assertEqual(
            empresa["nome_fantasia"],
            "Solar Oeste",
        )

        self.assertEqual(
            empresa["email"],
            "contato@solaroeste.com.br",
        )

        self.assertEqual(
            empresa["telefone"],
            "77977776666",
        )

    def test_criar_empresa_com_codigo_invalido(self):
        """
        O código deve ser um número inteiro maior que zero.
        """

        with self.assertRaises(ValueError):
            criar_dados_empresa(
                codigo=0,
                razao_social="Empresa Teste Ltda",
                nome_fantasia="Empresa Teste",
                cnpj="12.345.678/0001-95",
                email="contato@empresa.com.br",
                telefone="77999999999",
            )

    def test_criar_empresa_com_codigo_nao_inteiro(self):
        """
        O código não pode ser texto ou outro tipo de dado.
        """

        with self.assertRaises(TypeError):
            criar_dados_empresa(
                codigo="1",
                razao_social="Empresa Teste Ltda",
                nome_fantasia="Empresa Teste",
                cnpj="12.345.678/0001-95",
                email="contato@empresa.com.br",
                telefone="77999999999",
            )

    def test_criar_empresa_sem_razao_social(self):
        """
        A razão social é obrigatória.
        """

        with self.assertRaises(ValueError):
            criar_dados_empresa(
                codigo=3,
                razao_social="   ",
                nome_fantasia="Empresa Teste",
                cnpj="12.345.678/0001-95",
                email="contato@empresa.com.br",
                telefone="77999999999",
            )

    def test_criar_empresa_sem_nome_fantasia(self):
        """
        O nome fantasia é obrigatório.
        """

        with self.assertRaises(ValueError):
            criar_dados_empresa(
                codigo=3,
                razao_social="Empresa Teste Ltda",
                nome_fantasia="",
                cnpj="12.345.678/0001-95",
                email="contato@empresa.com.br",
                telefone="77999999999",
            )

    def test_criar_empresa_com_cnpj_incompleto(self):
        """
        O CNPJ deve possuir 14 números.
        """

        with self.assertRaises(ValueError):
            criar_dados_empresa(
                codigo=3,
                razao_social="Empresa Teste Ltda",
                nome_fantasia="Empresa Teste",
                cnpj="12.345.678/0001",
                email="contato@empresa.com.br",
                telefone="77999999999",
            )

    def test_criar_empresa_com_cnpj_invalido(self):
        """
        O CNPJ deve possuir dígitos verificadores válidos.
        """

        with self.assertRaises(ValueError):
            criar_dados_empresa(
                codigo=3,
                razao_social="Empresa Teste Ltda",
                nome_fantasia="Empresa Teste",
                cnpj="12.345.678/0001-00",
                email="contato@empresa.com.br",
                telefone="77999999999",
            )

    def test_criar_empresa_com_cnpj_repetido(self):
        """
        CNPJ formado por números repetidos deve ser rejeitado.
        """

        with self.assertRaises(ValueError):
            criar_dados_empresa(
                codigo=3,
                razao_social="Empresa Teste Ltda",
                nome_fantasia="Empresa Teste",
                cnpj="11.111.111/1111-11",
                email="contato@empresa.com.br",
                telefone="77999999999",
            )

    def test_criar_empresa_com_email_invalido(self):
        """
        O e-mail deve possuir uma estrutura mínima válida.
        """

        with self.assertRaises(ValueError):
            criar_dados_empresa(
                codigo=3,
                razao_social="Empresa Teste Ltda",
                nome_fantasia="Empresa Teste",
                cnpj="12.345.678/0001-95",
                email="email-invalido",
                telefone="77999999999",
            )

    def test_criar_empresa_sem_telefone(self):
        """
        O telefone é obrigatório.
        """

        with self.assertRaises(ValueError):
            criar_dados_empresa(
                codigo=3,
                razao_social="Empresa Teste Ltda",
                nome_fantasia="Empresa Teste",
                cnpj="12.345.678/0001-95",
                email="contato@empresa.com.br",
                telefone="",
            )

    # ========================================================
    # BUSCAS
    # ========================================================

    def test_buscar_empresa_por_codigo(self):
        """
        Deve retornar a empresa correspondente ao código.
        """

        empresa_encontrada = buscar_empresa_por_codigo(
            self.empresas,
            2,
        )

        self.assertIsNotNone(
            empresa_encontrada,
        )

        self.assertEqual(
            empresa_encontrada["nome_fantasia"],
            "Energia Sertão",
        )

    def test_buscar_empresa_por_codigo_inexistente(self):
        """
        Deve retornar None quando a empresa não existir.
        """

        empresa_encontrada = buscar_empresa_por_codigo(
            self.empresas,
            999,
        )

        self.assertIsNone(
            empresa_encontrada,
        )

    def test_buscar_empresa_por_cnpj_formatado(self):
        """
        A busca deve aceitar CNPJ com máscara.
        """

        empresa_encontrada = buscar_empresa_por_cnpj(
            self.empresas,
            "11.222.333/0001-81",
        )

        self.assertIsNotNone(
            empresa_encontrada,
        )

        self.assertEqual(
            empresa_encontrada["codigo"],
            1,
        )

    def test_buscar_empresa_por_cnpj_sem_formatacao(self):
        """
        A busca deve aceitar CNPJ contendo apenas números.
        """

        empresa_encontrada = buscar_empresa_por_cnpj(
            self.empresas,
            "45723174000110",
        )

        self.assertIsNotNone(
            empresa_encontrada,
        )

        self.assertEqual(
            empresa_encontrada["codigo"],
            2,
        )

    def test_buscar_empresa_por_cnpj_inexistente(self):
        """
        Deve retornar None quando não houver empresa com o CNPJ.
        """

        empresa_encontrada = buscar_empresa_por_cnpj(
            self.empresas,
            "98.765.432/0001-98",
        )

        self.assertIsNone(
            empresa_encontrada,
        )

    # ========================================================
    # VERIFICAÇÕES DE EXISTÊNCIA
    # ========================================================

    def test_codigo_empresa_existe(self):
        """
        Deve retornar True quando o código existir.
        """

        resultado = codigo_empresa_existe(
            self.empresas,
            1,
        )

        self.assertTrue(
            resultado,
        )

    def test_codigo_empresa_nao_existe(self):
        """
        Deve retornar False quando o código não existir.
        """

        resultado = codigo_empresa_existe(
            self.empresas,
            100,
        )

        self.assertFalse(
            resultado,
        )

    def test_cnpj_empresa_existe(self):
        """
        Deve retornar True quando o CNPJ existir.
        """

        resultado = cnpj_empresa_existe(
            self.empresas,
            "11.222.333/0001-81",
        )

        self.assertTrue(
            resultado,
        )

    def test_cnpj_empresa_nao_existe(self):
        """
        Deve retornar False quando o CNPJ não existir.
        """

        resultado = cnpj_empresa_existe(
            self.empresas,
            "98.765.432/0001-98",
        )

        self.assertFalse(
            resultado,
        )

    # ========================================================
    # ORDENAÇÃO
    # ========================================================

    def test_ordenar_empresas_por_nome(self):
        """
        Deve retornar uma nova lista ordenada pelo nome fantasia.
        """

        empresas_desordenadas = [
            self.empresa_solar_bahia,
            self.empresa_energia_sertao,
        ]

        empresas_ordenadas = ordenar_empresas_por_nome(
            empresas_desordenadas,
        )

        self.assertEqual(
            empresas_ordenadas[0]["nome_fantasia"],
            "Energia Sertão",
        )

        self.assertEqual(
            empresas_ordenadas[1]["nome_fantasia"],
            "Solar Bahia",
        )

    def test_ordenar_empresas_nao_altera_lista_original(self):
        """
        A função deve preservar a ordem da lista recebida.
        """

        empresas_desordenadas = [
            self.empresa_solar_bahia,
            self.empresa_energia_sertao,
        ]

        ordenar_empresas_por_nome(
            empresas_desordenadas,
        )

        self.assertEqual(
            empresas_desordenadas[0]["nome_fantasia"],
            "Solar Bahia",
        )

    # ========================================================
    # SITUAÇÃO DA EMPRESA
    # ========================================================

    def test_empresa_criada_esta_ativa(self):
        """
        Uma empresa nova deve iniciar ativa.
        """

        resultado = empresa_esta_ativa(
            self.empresa_solar_bahia,
        )

        self.assertTrue(
            resultado,
        )

    def test_empresa_inativa_nao_esta_ativa(self):
        """
        Uma empresa inativada não deve ser considerada ativa.
        """

        inativar_empresa(
            self.empresa_solar_bahia,
        )

        resultado = empresa_esta_ativa(
            self.empresa_solar_bahia,
        )

        self.assertFalse(
            resultado,
        )

    def test_alterar_situacao_empresa(self):
        """
        Deve alterar a situação para um valor reconhecido.
        """

        empresa = alterar_situacao_empresa(
            self.empresa_solar_bahia,
            SITUACAO_EMPRESA_SUSPENSA,
        )

        self.assertEqual(
            empresa["situacao"],
            SITUACAO_EMPRESA_SUSPENSA,
        )

    def test_alterar_para_situacao_invalida(self):
        """
        Situações desconhecidas devem ser rejeitadas.
        """

        with self.assertRaises(ValueError):
            alterar_situacao_empresa(
                self.empresa_solar_bahia,
                "EM_ANALISE",
            )

    def test_inativar_empresa(self):
        """
        Deve alterar a situação para INATIVA.
        """

        empresa = inativar_empresa(
            self.empresa_solar_bahia,
        )

        self.assertEqual(
            empresa["situacao"],
            SITUACAO_EMPRESA_INATIVA,
        )

    def test_suspender_empresa(self):
        """
        Deve alterar a situação para SUSPENSA.
        """

        empresa = suspender_empresa(
            self.empresa_solar_bahia,
        )

        self.assertEqual(
            empresa["situacao"],
            SITUACAO_EMPRESA_SUSPENSA,
        )

    def test_cancelar_empresa(self):
        """
        Deve alterar a situação para CANCELADA.
        """

        empresa = cancelar_empresa(
            self.empresa_solar_bahia,
        )

        self.assertEqual(
            empresa["situacao"],
            SITUACAO_EMPRESA_CANCELADA,
        )

    def test_ativar_empresa(self):
        """
        Uma empresa inativa deve poder ser reativada.
        """

        inativar_empresa(
            self.empresa_solar_bahia,
        )

        empresa = ativar_empresa(
            self.empresa_solar_bahia,
        )

        self.assertEqual(
            empresa["situacao"],
            SITUACAO_EMPRESA_ATIVA,
        )

    def test_alteracao_de_situacao_atualiza_data(self):
        """
        A alteração da situação deve manter o campo de atualização.
        """

        empresa = suspender_empresa(
            self.empresa_solar_bahia,
        )

        self.assertIn(
            "data_atualizacao",
            empresa,
        )

        self.assertIsInstance(
            empresa["data_atualizacao"],
            str,
        )

        # ========================================================
    # MÁQUINA DE ESTADOS
    # ========================================================

    def test_transicoes_da_empresa_ativa(self):
        """
        Uma empresa ativa pode ser inativada, suspensa ou cancelada.
        """

        transicoes = obter_transicoes_permitidas_empresa(
            SITUACAO_EMPRESA_ATIVA,
        )

        self.assertEqual(
            transicoes,
            (
                SITUACAO_EMPRESA_INATIVA,
                SITUACAO_EMPRESA_SUSPENSA,
                SITUACAO_EMPRESA_CANCELADA,
            ),
        )

    def test_transicoes_da_empresa_inativa(self):
        """
        Uma empresa inativa pode ser ativada ou cancelada.
        """

        transicoes = obter_transicoes_permitidas_empresa(
            SITUACAO_EMPRESA_INATIVA,
        )

        self.assertEqual(
            transicoes,
            (
                SITUACAO_EMPRESA_ATIVA,
                SITUACAO_EMPRESA_CANCELADA,
            ),
        )

    def test_transicoes_da_empresa_suspensa(self):
        """
        Uma empresa suspensa pode ser ativada, inativada ou cancelada.
        """

        transicoes = obter_transicoes_permitidas_empresa(
            SITUACAO_EMPRESA_SUSPENSA,
        )

        self.assertEqual(
            transicoes,
            (
                SITUACAO_EMPRESA_ATIVA,
                SITUACAO_EMPRESA_INATIVA,
                SITUACAO_EMPRESA_CANCELADA,
            ),
        )

    def test_empresa_cancelada_nao_possui_transicoes(self):
        """
        CANCELADA é uma situação terminal.
        """

        transicoes = obter_transicoes_permitidas_empresa(
            SITUACAO_EMPRESA_CANCELADA,
        )

        self.assertEqual(
            transicoes,
            (),
        )

    def test_transicao_ativa_para_suspensa_e_permitida(self):
        """
        Deve reconhecer uma transição válida.
        """

        resultado = transicao_situacao_empresa_permitida(
            SITUACAO_EMPRESA_ATIVA,
            SITUACAO_EMPRESA_SUSPENSA,
        )

        self.assertTrue(
            resultado,
        )

    def test_transicao_inativa_para_suspensa_nao_e_permitida(self):
        """
        Uma empresa inativa não pode ser suspensa diretamente.
        """

        resultado = transicao_situacao_empresa_permitida(
            SITUACAO_EMPRESA_INATIVA,
            SITUACAO_EMPRESA_SUSPENSA,
        )

        self.assertFalse(
            resultado,
        )

    def test_cancelar_empresa_cria_estado_terminal(self):
        """
        Uma empresa cancelada não pode ser reativada.
        """

        cancelar_empresa(
            self.empresa_solar_bahia,
        )

        self.assertTrue(
            empresa_esta_cancelada(
                self.empresa_solar_bahia,
            )
        )

        with self.assertRaises(ValueError):
            ativar_empresa(
                self.empresa_solar_bahia,
            )

    def test_empresa_cancelada_nao_pode_ser_inativada(self):
        """
        CANCELADA não pode ser alterada para INATIVA.
        """

        cancelar_empresa(
            self.empresa_solar_bahia,
        )

        with self.assertRaises(ValueError):
            inativar_empresa(
                self.empresa_solar_bahia,
            )

    def test_empresa_cancelada_nao_pode_ser_suspensa(self):
        """
        CANCELADA não pode ser alterada para SUSPENSA.
        """

        cancelar_empresa(
            self.empresa_solar_bahia,
        )

        with self.assertRaises(ValueError):
            suspender_empresa(
                self.empresa_solar_bahia,
            )

    def test_empresa_ativa_nao_pode_ser_ativada_novamente(self):
        """
        Alterações redundantes devem ser rejeitadas.
        """

        with self.assertRaises(ValueError):
            ativar_empresa(
                self.empresa_solar_bahia,
            )

    def test_empresa_inativa_nao_pode_ser_inativada_novamente(self):
        """
        Não deve registrar uma transição sem mudança real.
        """

        inativar_empresa(
            self.empresa_solar_bahia,
        )

        with self.assertRaises(ValueError):
            inativar_empresa(
                self.empresa_solar_bahia,
            )

    def test_empresa_inativa_nao_pode_ser_suspensa_diretamente(self):
        """
        A suspensão deve partir de uma empresa ativa.
        """

        inativar_empresa(
            self.empresa_solar_bahia,
        )

        with self.assertRaises(ValueError):
            suspender_empresa(
                self.empresa_solar_bahia,
            )

    def test_empresa_suspensa_pode_ser_inativada(self):
        """
        Uma empresa suspensa pode ser encerrada operacionalmente.
        """

        suspender_empresa(
            self.empresa_solar_bahia,
        )

        empresa = inativar_empresa(
            self.empresa_solar_bahia,
        )

        self.assertEqual(
            empresa["situacao"],
            SITUACAO_EMPRESA_INATIVA,
        )

    def test_empresa_suspensa_pode_ser_reativada(self):
        """
        Uma suspensão temporária pode ser encerrada com reativação.
        """

        suspender_empresa(
            self.empresa_solar_bahia,
        )

        empresa = ativar_empresa(
            self.empresa_solar_bahia,
        )

        self.assertEqual(
            empresa["situacao"],
            SITUACAO_EMPRESA_ATIVA,
        )

    def test_alterar_situacao_rejeita_empresa_sem_situacao(self):
        """
        A entidade precisa possuir uma situação atual.
        """

        empresa_sem_situacao = {
            "codigo": 1,
            "nome_fantasia": "Empresa Teste",
        }

        with self.assertRaises(ValueError):
            alterar_situacao_empresa(
                empresa_sem_situacao,
                SITUACAO_EMPRESA_INATIVA,
            )

    def test_alterar_situacao_rejeita_objeto_invalido(self):
        """
        A empresa deve ser representada por um dicionário.
        """

        with self.assertRaises(TypeError):
            alterar_situacao_empresa(
                "empresa inválida",
                SITUACAO_EMPRESA_INATIVA,
            )

    def test_mapa_de_transicoes_possui_todas_as_situacoes(self):
        """
        Toda situação reconhecida deve estar presente no mapa.
        """

        self.assertIn(
            SITUACAO_EMPRESA_ATIVA,
            TRANSICOES_SITUACAO_EMPRESA,
        )

        self.assertIn(
            SITUACAO_EMPRESA_INATIVA,
            TRANSICOES_SITUACAO_EMPRESA,
        )

        self.assertIn(
            SITUACAO_EMPRESA_SUSPENSA,
            TRANSICOES_SITUACAO_EMPRESA,
        )

        self.assertIn(
            SITUACAO_EMPRESA_CANCELADA,
            TRANSICOES_SITUACAO_EMPRESA,
        )

        # ========================================================
    # ATUALIZAÇÃO DOS DADOS CADASTRAIS
    # ========================================================

    def test_atualizar_todos_os_dados_da_empresa(self):
        """
        Deve atualizar todos os campos cadastrais permitidos.
        """

        empresa_atualizada = atualizar_dados_empresa(
            empresa=self.empresa_solar_bahia,
            razao_social="Solar Bahia Engenharia Ltda",
            nome_fantasia="Solar Bahia Engenharia",
            email="NOVO@SOLARBAHIA.COM.BR",
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

    def test_atualizar_apenas_nome_fantasia(self):
        """
        Campos não informados devem ser preservados.
        """

        cnpj_original = self.empresa_solar_bahia["cnpj"]
        email_original = self.empresa_solar_bahia["email"]

        empresa_atualizada = atualizar_dados_empresa(
            empresa=self.empresa_solar_bahia,
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

    def test_atualizar_empresa_normaliza_textos(self):
        """
        A edição deve aplicar as mesmas normalizações do cadastro.
        """

        empresa_atualizada = atualizar_dados_empresa(
            empresa=self.empresa_solar_bahia,
            razao_social="  Solar   Bahia   Engenharia Ltda  ",
            nome_fantasia="  Solar   Bahia  ",
        )

        self.assertEqual(
            empresa_atualizada["razao_social"],
            "Solar Bahia Engenharia Ltda",
        )

        self.assertEqual(
            empresa_atualizada["nome_fantasia"],
            "Solar Bahia",
        )

    def test_atualizar_empresa_sem_informar_campos(self):
        """
        A operação exige pelo menos um campo para atualização.
        """

        with self.assertRaises(ValueError):
            atualizar_dados_empresa(
                empresa=self.empresa_solar_bahia,
            )

    def test_atualizar_empresa_com_email_invalido(self):
        """
        O novo e-mail deve ser validado pelo domínio.
        """

        with self.assertRaises(ValueError):
            atualizar_dados_empresa(
                empresa=self.empresa_solar_bahia,
                email="email-invalido",
            )

    def test_atualizar_empresa_com_telefone_vazio(self):
        """
        O telefone não pode ser removido.
        """

        with self.assertRaises(ValueError):
            atualizar_dados_empresa(
                empresa=self.empresa_solar_bahia,
                telefone="",
            )

    def test_atualizar_empresa_com_razao_social_vazia(self):
        """
        A razão social continua sendo obrigatória.
        """

        with self.assertRaises(ValueError):
            atualizar_dados_empresa(
                empresa=self.empresa_solar_bahia,
                razao_social="   ",
            )

    def test_atualizar_empresa_com_nome_fantasia_vazio(self):
        """
        O nome fantasia continua sendo obrigatório.
        """

        with self.assertRaises(ValueError):
            atualizar_dados_empresa(
                empresa=self.empresa_solar_bahia,
                nome_fantasia="",
            )

    def test_atualizar_empresa_rejeita_objeto_invalido(self):
        """
        A empresa deve ser um dicionário.
        """

        with self.assertRaises(TypeError):
            atualizar_dados_empresa(
                empresa="empresa inválida",
                nome_fantasia="Novo Nome",
            )

    def test_atualizar_empresa_rejeita_dados_incompletos(self):
        """
        A entidade precisa possuir sua estrutura mínima.
        """

        empresa_incompleta = {
            "codigo": 1,
            "nome_fantasia": "Empresa Incompleta",
        }

        with self.assertRaises(ValueError):
            atualizar_dados_empresa(
                empresa=empresa_incompleta,
                nome_fantasia="Novo Nome",
            )

    def test_atualizar_empresa_preserva_cnpj(self):
        """
        O CNPJ não participa da edição cadastral comum.
        """

        cnpj_original = self.empresa_solar_bahia["cnpj"]

        atualizar_dados_empresa(
            empresa=self.empresa_solar_bahia,
            razao_social="Nova Razão Social Ltda",
        )

        self.assertEqual(
            self.empresa_solar_bahia["cnpj"],
            cnpj_original,
        )

    def test_atualizar_empresa_mantem_codigo(self):
        """
        O código interno da empresa não pode ser alterado.
        """

        codigo_original = self.empresa_solar_bahia["codigo"]

        atualizar_dados_empresa(
            empresa=self.empresa_solar_bahia,
            nome_fantasia="Novo Nome Fantasia",
        )

        self.assertEqual(
            self.empresa_solar_bahia["codigo"],
            codigo_original,
        )

    def test_atualizar_empresa_mantem_situacao(self):
        """
        A edição cadastral não deve alterar a situação.
        """

        situacao_original = self.empresa_solar_bahia["situacao"]

        atualizar_dados_empresa(
            empresa=self.empresa_solar_bahia,
            email="novo@email.com.br",
        )

        self.assertEqual(
            self.empresa_solar_bahia["situacao"],
            situacao_original,
        )

    def test_atualizar_empresa_atualiza_data(self):
        """
        A edição deve manter o campo de data de atualização.
        """

        empresa_atualizada = atualizar_dados_empresa(
            empresa=self.empresa_solar_bahia,
            telefone="(77) 90000-0000",
        )

        self.assertIn(
            "data_atualizacao",
            empresa_atualizada,
        )

        self.assertIsInstance(
            empresa_atualizada["data_atualizacao"],
            str,
        )

if __name__ == "__main__":
    unittest.main()