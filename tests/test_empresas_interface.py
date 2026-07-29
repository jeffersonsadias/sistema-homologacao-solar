"""
Testes da interface de terminal de Empresas.

Estes testes verificam principalmente:

- formatação para exibição;
- leitura de campos opcionais;
- encaminhamento das alterações de situação;
- comportamento das telas;
- comunicação com a fachada.

A persistência real não é utilizada.
"""

import unittest
from unittest.mock import patch

from app.dominio.empresas import (
    SITUACAO_EMPRESA_ATIVA,
    SITUACAO_EMPRESA_CANCELADA,
    SITUACAO_EMPRESA_INATIVA,
    SITUACAO_EMPRESA_SUSPENSA,
)
from app.interface import empresas_interface


class TestEmpresasInterface(unittest.TestCase):
    """
    Testa as partes verificáveis da interface de Empresas.
    """

    def setUp(self):
        """
        Cria uma empresa padrão utilizada nos testes.
        """

        self.empresa = {
            "codigo": 1,
            "razao_social": "Solar Energia Bahia Ltda",
            "nome_fantasia": "Solar Bahia",
            "cnpj": "11222333000181",
            "email": "contato@solarbahia.com.br",
            "telefone": "77999999999",
            "situacao": SITUACAO_EMPRESA_ATIVA,
            "data_cadastro": "2026-07-28T10:00:00",
            "data_atualizacao": "2026-07-28T10:00:00",
        }

    # ========================================================
    # FORMATAÇÃO
    # ========================================================

    def test_formatar_cnpj(self):
        """
        Deve formatar um CNPJ com 14 dígitos.
        """

        resultado = empresas_interface._formatar_cnpj(
            "11222333000181",
        )

        self.assertEqual(
            resultado,
            "11.222.333/0001-81",
        )

    def test_formatar_cnpj_com_tamanho_invalido(self):
        """
        Valores fora do padrão devem ser preservados.
        """

        resultado = empresas_interface._formatar_cnpj(
            "123",
        )

        self.assertEqual(
            resultado,
            "123",
        )

    def test_formatar_telefone_celular(self):
        """
        Deve formatar um telefone com 11 dígitos.
        """

        resultado = empresas_interface._formatar_telefone(
            "77999999999",
        )

        self.assertEqual(
            resultado,
            "(77) 99999-9999",
        )

    def test_formatar_telefone_fixo(self):
        """
        Deve formatar um telefone com 10 dígitos.
        """

        resultado = empresas_interface._formatar_telefone(
            "7734567890",
        )

        self.assertEqual(
            resultado,
            "(77) 3456-7890",
        )

    def test_formatar_telefone_com_tamanho_desconhecido(self):
        """
        Valores fora dos formatos conhecidos devem ser preservados.
        """

        resultado = empresas_interface._formatar_telefone(
            "12345",
        )

        self.assertEqual(
            resultado,
            "12345",
        )

    # ========================================================
    # LEITURA DE CAMPO OPCIONAL
    # ========================================================

    @patch("builtins.input", return_value="")
    def test_ler_campo_opcional_preserva_valor(
        self,
        input_mock,
    ):
        """
        Enter sem conteúdo deve resultar em None.
        """

        resultado = empresas_interface._ler_campo_opcional(
            "Novo nome",
            "Nome Atual",
        )

        self.assertIsNone(
            resultado,
        )

        input_mock.assert_called_once_with(
            "Novo nome [Nome Atual]: "
        )

    @patch(
        "builtins.input",
        return_value="  Novo Nome  ",
    )
    def test_ler_campo_opcional_retorna_valor_digitado(
        self,
        input_mock,
    ):
        """
        Um valor digitado deve ser retornado sem espaços externos.
        """

        resultado = empresas_interface._ler_campo_opcional(
            "Novo nome",
            "Nome Atual",
        )

        self.assertEqual(
            resultado,
            "Novo Nome",
        )

    # ========================================================
    # EXECUÇÃO DA ALTERAÇÃO DE SITUAÇÃO
    # ========================================================

    @patch(
        "app.interface.empresas_interface.empresas.ativar_empresa"
    )
    def test_executar_alteracao_para_ativa(
        self,
        ativar_empresa_mock,
    ):
        """
        A situação ATIVA deve chamar a função correta da fachada.
        """

        ativar_empresa_mock.return_value = self.empresa

        resultado = (
            empresas_interface._executar_alteracao_situacao(
                codigo_empresa=1,
                nova_situacao=SITUACAO_EMPRESA_ATIVA,
            )
        )

        ativar_empresa_mock.assert_called_once_with(
            1,
        )

        self.assertEqual(
            resultado,
            self.empresa,
        )

    @patch(
        "app.interface.empresas_interface.empresas.inativar_empresa"
    )
    def test_executar_alteracao_para_inativa(
        self,
        inativar_empresa_mock,
    ):
        """
        A situação INATIVA deve chamar a função correta.
        """

        inativar_empresa_mock.return_value = self.empresa

        empresas_interface._executar_alteracao_situacao(
            codigo_empresa=1,
            nova_situacao=SITUACAO_EMPRESA_INATIVA,
        )

        inativar_empresa_mock.assert_called_once_with(
            1,
        )

    @patch(
        "app.interface.empresas_interface.empresas.suspender_empresa"
    )
    def test_executar_alteracao_para_suspensa(
        self,
        suspender_empresa_mock,
    ):
        """
        A situação SUSPENSA deve chamar a função correta.
        """

        suspender_empresa_mock.return_value = self.empresa

        empresas_interface._executar_alteracao_situacao(
            codigo_empresa=1,
            nova_situacao=SITUACAO_EMPRESA_SUSPENSA,
        )

        suspender_empresa_mock.assert_called_once_with(
            1,
        )

    @patch(
        "app.interface.empresas_interface.empresas.cancelar_empresa"
    )
    def test_executar_alteracao_para_cancelada(
        self,
        cancelar_empresa_mock,
    ):
        """
        A situação CANCELADA deve chamar a função correta.
        """

        cancelar_empresa_mock.return_value = self.empresa

        empresas_interface._executar_alteracao_situacao(
            codigo_empresa=1,
            nova_situacao=SITUACAO_EMPRESA_CANCELADA,
        )

        cancelar_empresa_mock.assert_called_once_with(
            1,
        )

    def test_executar_alteracao_com_situacao_desconhecida(self):
        """
        Uma situação sem operação associada deve ser rejeitada.
        """

        with self.assertRaises(ValueError):
            empresas_interface._executar_alteracao_situacao(
                codigo_empresa=1,
                nova_situacao="EM_ANALISE",
            )

    # ========================================================
    # SELEÇÃO DE EMPRESA
    # ========================================================

    @patch(
        "app.interface.empresas_interface.empresas.buscar_empresa"
    )
    @patch(
        "app.interface.empresas_interface.ler_int",
        return_value=1,
    )
    def test_selecionar_empresa_encontrada(
        self,
        ler_int_mock,
        buscar_empresa_mock,
    ):
        """
        Deve retornar a empresa localizada pela fachada.
        """

        buscar_empresa_mock.return_value = self.empresa

        resultado = empresas_interface._selecionar_empresa()

        ler_int_mock.assert_called_once_with(
            "Informe o código da empresa: "
        )

        buscar_empresa_mock.assert_called_once_with(
            1,
        )

        self.assertEqual(
            resultado,
            self.empresa,
        )

    @patch("builtins.print")
    @patch(
        "app.interface.empresas_interface.empresas.buscar_empresa",
        return_value=None,
    )
    @patch(
        "app.interface.empresas_interface.ler_int",
        return_value=999,
    )
    def test_selecionar_empresa_inexistente(
        self,
        ler_int_mock,
        buscar_empresa_mock,
        print_mock,
    ):
        """
        Deve retornar None quando a empresa não for encontrada.
        """

        resultado = empresas_interface._selecionar_empresa()

        self.assertIsNone(
            resultado,
        )

        buscar_empresa_mock.assert_called_once_with(
            999,
        )

        print_mock.assert_any_call(
            "\nEmpresa não encontrada."
        )

    # ========================================================
    # CADASTRO PELA INTERFACE
    # ========================================================

    @patch(
        "app.interface.empresas_interface."
        "_pressionar_enter_para_continuar"
    )
    @patch(
        "app.interface.empresas_interface._exibir_empresa"
    )
    @patch(
        "app.interface.empresas_interface.empresas.cadastrar_empresa"
    )
    @patch(
        "builtins.input",
        side_effect=[
            "Solar Energia Bahia Ltda",
            "Solar Bahia",
            "11.222.333/0001-81",
            "contato@solarbahia.com.br",
            "(77) 99999-9999",
        ],
    )
    def test_cadastrar_empresa_interface(
        self,
        input_mock,
        cadastrar_empresa_mock,
        exibir_empresa_mock,
        continuar_mock,
    ):
        """
        A interface deve encaminhar os dados para a fachada.
        """

        cadastrar_empresa_mock.return_value = self.empresa

        empresas_interface.cadastrar_empresa_interface()

        cadastrar_empresa_mock.assert_called_once_with(
            razao_social="Solar Energia Bahia Ltda",
            nome_fantasia="Solar Bahia",
            cnpj="11.222.333/0001-81",
            email="contato@solarbahia.com.br",
            telefone="(77) 99999-9999",
        )

        exibir_empresa_mock.assert_called_once_with(
            self.empresa,
        )

        continuar_mock.assert_called_once()

    @patch(
        "app.interface.empresas_interface."
        "_pressionar_enter_para_continuar"
    )
    @patch(
        "app.interface.empresas_interface.empresas.cadastrar_empresa",
        side_effect=ValueError("CNPJ inválido."),
    )
    @patch(
        "builtins.input",
        side_effect=[
            "Empresa Teste Ltda",
            "Empresa Teste",
            "CNPJ inválido",
            "contato@empresa.com.br",
            "77999999999",
        ],
    )
    def test_cadastrar_empresa_interface_trata_erro(
        self,
        input_mock,
        cadastrar_empresa_mock,
        continuar_mock,
    ):
        """
        Erros da fachada devem ser tratados pela interface.
        """

        with patch("builtins.print") as print_mock:
            empresas_interface.cadastrar_empresa_interface()

        print_mock.assert_any_call(
            "\nNão foi possível cadastrar a empresa: "
            "CNPJ inválido."
        )

        continuar_mock.assert_called_once()

    # ========================================================
    # LISTAGEM
    # ========================================================

    @patch(
        "app.interface.empresas_interface."
        "_pressionar_enter_para_continuar"
    )
    @patch(
        "app.interface.empresas_interface._exibir_empresa_resumida"
    )
    @patch(
        "app.interface.empresas_interface.empresas.listar_empresas"
    )
    def test_listar_empresas_interface(
        self,
        listar_empresas_mock,
        exibir_resumida_mock,
        continuar_mock,
    ):
        """
        Deve exibir cada empresa retornada pela fachada.
        """

        listar_empresas_mock.return_value = [
            self.empresa,
        ]

        empresas_interface.listar_empresas_interface()

        listar_empresas_mock.assert_called_once_with(
            ordenar_por_nome=True,
        )

        exibir_resumida_mock.assert_called_once_with(
            self.empresa,
        )

        continuar_mock.assert_called_once()

    @patch(
        "app.interface.empresas_interface."
        "_pressionar_enter_para_continuar"
    )
    @patch(
        "app.interface.empresas_interface.empresas.listar_empresas",
        return_value=[],
    )
    def test_listar_empresas_interface_sem_registros(
        self,
        listar_empresas_mock,
        continuar_mock,
    ):
        """
        Deve tratar corretamente uma coleção vazia.
        """

        with patch("builtins.print") as print_mock:
            empresas_interface.listar_empresas_interface()

        print_mock.assert_any_call(
            "\nNenhuma empresa cadastrada."
        )

        continuar_mock.assert_called_once()


if __name__ == "__main__":
    unittest.main()