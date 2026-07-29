"""
Testes da interface de terminal dos vínculos
entre Projetos e Unidades Consumidoras.
"""

import unittest
from datetime import datetime
from types import SimpleNamespace
from unittest.mock import patch

from app.dominio.status import (
    PapelUnidadeProjeto,
)

from app.dominio.vinculos_unidade_projeto import (
    SituacaoVinculoUnidadeProjeto,
)

from app.interface import (
    vinculos_unidade_projeto_interface
    as interface_vinculos,
)


class TestVinculosUnidadeProjetoInterface(
    unittest.TestCase
):
    """
    Testes das funções responsáveis
    pela interação com o terminal.
    """

    def criar_vinculo_exemplo(
        self,
        codigo=1,
        codigo_projeto=10,
        codigo_unidade=20,
        papel=PapelUnidadeProjeto.GERADORA,
        situacao=(
            SituacaoVinculoUnidadeProjeto.ATIVO
        ),
        observacoes="",
    ):
        """
        Cria um objeto simples que imita
        um vínculo para uso nos testes.

        O SimpleNamespace permite criar
        um objeto com atributos sem utilizar
        diretamente a função de domínio.
        """

        agora = datetime(
            2026,
            7,
            27,
            14,
            30,
        )

        return SimpleNamespace(
            codigo=codigo,
            codigo_projeto=codigo_projeto,
            codigo_unidade_consumidora=(
                codigo_unidade
            ),
            papel=papel,
            situacao=situacao,
            data_vinculo=agora,
            data_atualizacao=agora,
            observacoes=observacoes,
        )

    # ========================================================
    # TESTES DA LEITURA DE CÓDIGOS
    # ========================================================

    @patch(
        "builtins.input",
        return_value="10",
    )
    def test_ler_codigo_valido(
        self,
        _mock_input,
    ):
        """
        Deve converter uma entrada válida
        em número inteiro.
        """

        resultado = (
            interface_vinculos
            ._ler_codigo(
                "Código: "
            )
        )

        self.assertEqual(
            resultado,
            10,
        )

    @patch(
        "builtins.print"
    )
    @patch(
        "builtins.input",
        side_effect=[
            "abc",
            "-2",
            "0",
            "15",
        ],
    )
    def test_ler_codigo_repete_ate_receber_valor_valido(
        self,
        _mock_input,
        mock_print,
    ):
        """
        Deve continuar solicitando o código
        enquanto a entrada for inválida.
        """

        resultado = (
            interface_vinculos
            ._ler_codigo(
                "Código: "
            )
        )

        self.assertEqual(
            resultado,
            15,
        )

        self.assertEqual(
            mock_print.call_count,
            3,
        )

    # ========================================================
    # TESTES DA SELEÇÃO DE PAPEL
    # ========================================================

    @patch(
        "builtins.print"
    )
    @patch(
        "builtins.input",
        return_value="1",
    )
    def test_selecionar_papel_geradora(
        self,
        _mock_input,
        _mock_print,
    ):
        """
        Deve retornar o enum correspondente
        à Unidade Geradora.
        """

        resultado = (
            interface_vinculos
            ._selecionar_papel_unidade()
        )

        self.assertEqual(
            resultado,
            PapelUnidadeProjeto.GERADORA,
        )

    @patch(
        "builtins.print"
    )
    @patch(
        "builtins.input",
        return_value="2",
    )
    def test_selecionar_papel_beneficiaria(
        self,
        _mock_input,
        _mock_print,
    ):
        """
        Deve retornar o enum correspondente
        à Unidade Beneficiária.
        """

        resultado = (
            interface_vinculos
            ._selecionar_papel_unidade()
        )

        self.assertEqual(
            resultado,
            PapelUnidadeProjeto.BENEFICIARIA,
        )

    @patch(
        "builtins.print"
    )
    @patch(
        "builtins.input",
        side_effect=[
            "9",
            "1",
        ],
    )
    def test_selecionar_papel_repete_opcao_invalida(
        self,
        _mock_input,
        mock_print,
    ):
        """
        Deve repetir a pergunta quando
        o usuário escolher uma opção inválida.
        """

        resultado = (
            interface_vinculos
            ._selecionar_papel_unidade()
        )

        self.assertEqual(
            resultado,
            PapelUnidadeProjeto.GERADORA,
        )

        mock_print.assert_any_call(
            "\nOpção inválida."
        )

    # ========================================================
    # TESTES DO CADASTRO
    # ========================================================

    @patch(
        "app.interface."
        "vinculos_unidade_projeto_interface."
        "mostrar_vinculo"
    )
    @patch(
        "app.interface."
        "vinculos_unidade_projeto_interface."
        "vinculos_unidade_projeto."
        "vincular_unidade_geradora"
    )
    @patch(
        "app.interface."
        "vinculos_unidade_projeto_interface."
        "_ler_observacoes",
        return_value="Geradora principal",
    )
    @patch(
        "app.interface."
        "vinculos_unidade_projeto_interface."
        "_selecionar_papel_unidade",
        return_value=(
            PapelUnidadeProjeto.GERADORA
        ),
    )
    @patch(
        "app.interface."
        "vinculos_unidade_projeto_interface."
        "_ler_codigo",
        side_effect=[
            10,
            20,
        ],
    )
    @patch(
        "builtins.print"
    )
    def test_cadastrar_vinculo_geradora(
        self,
        _mock_print,
        _mock_ler_codigo,
        _mock_selecionar_papel,
        _mock_ler_observacoes,
        mock_vincular_geradora,
        mock_mostrar_vinculo,
    ):
        """
        Deve encaminhar corretamente os dados
        para a criação de uma Geradora.
        """

        vinculo = self.criar_vinculo_exemplo(
            observacoes="Geradora principal",
        )

        mock_vincular_geradora.return_value = (
            vinculo
        )

        resultado = (
            interface_vinculos
            .cadastrar_vinculo()
        )

        mock_vincular_geradora\
            .assert_called_once_with(
                codigo_projeto=10,
                codigo_unidade_consumidora=20,
                observacoes=(
                    "Geradora principal"
                ),
            )

        mock_mostrar_vinculo\
            .assert_called_once_with(
                vinculo
            )

        self.assertIs(
            resultado,
            vinculo,
        )

    @patch(
        "app.interface."
        "vinculos_unidade_projeto_interface."
        "mostrar_vinculo"
    )
    @patch(
        "app.interface."
        "vinculos_unidade_projeto_interface."
        "vinculos_unidade_projeto."
        "vincular_unidade_beneficiaria"
    )
    @patch(
        "app.interface."
        "vinculos_unidade_projeto_interface."
        "_ler_observacoes",
        return_value="Beneficiária residencial",
    )
    @patch(
        "app.interface."
        "vinculos_unidade_projeto_interface."
        "_selecionar_papel_unidade",
        return_value=(
            PapelUnidadeProjeto.BENEFICIARIA
        ),
    )
    @patch(
        "app.interface."
        "vinculos_unidade_projeto_interface."
        "_ler_codigo",
        side_effect=[
            10,
            21,
        ],
    )
    @patch(
        "builtins.print"
    )
    def test_cadastrar_vinculo_beneficiaria(
        self,
        _mock_print,
        _mock_ler_codigo,
        _mock_selecionar_papel,
        _mock_ler_observacoes,
        mock_vincular_beneficiaria,
        mock_mostrar_vinculo,
    ):
        """
        Deve encaminhar corretamente os dados
        para a criação de uma Beneficiária.
        """

        vinculo = self.criar_vinculo_exemplo(
            codigo_unidade=21,
            papel=(
                PapelUnidadeProjeto.BENEFICIARIA
            ),
            observacoes=(
                "Beneficiária residencial"
            ),
        )

        mock_vincular_beneficiaria.return_value = (
            vinculo
        )

        resultado = (
            interface_vinculos
            .cadastrar_vinculo()
        )

        mock_vincular_beneficiaria\
            .assert_called_once_with(
                codigo_projeto=10,
                codigo_unidade_consumidora=21,
                observacoes=(
                    "Beneficiária residencial"
                ),
            )

        mock_mostrar_vinculo\
            .assert_called_once_with(
                vinculo
            )

        self.assertIs(
            resultado,
            vinculo,
        )

    @patch(
        "app.interface."
        "vinculos_unidade_projeto_interface."
        "vinculos_unidade_projeto."
        "vincular_unidade_geradora"
    )
    @patch(
        "app.interface."
        "vinculos_unidade_projeto_interface."
        "_ler_observacoes",
        return_value="",
    )
    @patch(
        "app.interface."
        "vinculos_unidade_projeto_interface."
        "_selecionar_papel_unidade",
        return_value=(
            PapelUnidadeProjeto.GERADORA
        ),
    )
    @patch(
        "app.interface."
        "vinculos_unidade_projeto_interface."
        "_ler_codigo",
        side_effect=[
            999,
            20,
        ],
    )
    @patch(
        "builtins.print"
    )
    def test_cadastrar_vinculo_trata_value_error(
        self,
        mock_print,
        _mock_ler_codigo,
        _mock_selecionar_papel,
        _mock_ler_observacoes,
        mock_vincular_geradora,
    ):
        """
        Deve capturar erros esperados
        enviados pela fachada.
        """

        mock_vincular_geradora.side_effect = (
            ValueError(
                "O Projeto informado não existe."
            )
        )

        resultado = (
            interface_vinculos
            .cadastrar_vinculo()
        )

        self.assertIsNone(
            resultado
        )

        mock_print.assert_any_call(
            "\nNão foi possível criar "
            "o vínculo: "
            "O Projeto informado não existe."
        )

    # ========================================================
    # TESTES DA EXIBIÇÃO
    # ========================================================

    @patch(
        "builtins.print"
    )
    def test_mostrar_vinculo(
        self,
        mock_print,
    ):
        """
        Deve exibir os principais dados
        de um vínculo recebido.
        """

        vinculo = self.criar_vinculo_exemplo(
            observacoes="Geradora principal",
        )

        interface_vinculos.mostrar_vinculo(
            vinculo
        )

        mock_print.assert_any_call(
            "Código do vínculo: 1"
        )

        mock_print.assert_any_call(
            "Código do Projeto: 10"
        )

        mock_print.assert_any_call(
            "Código da Unidade Consumidora: 20"
        )

        mock_print.assert_any_call(
            "Papel no Projeto: Unidade Geradora"
        )

        mock_print.assert_any_call(
            "Situação: Ativo"
        )

        mock_print.assert_any_call(
            "Data do vínculo: "
            "27/07/2026 às 14:30"
        )

        mock_print.assert_any_call(
            "Observações: Geradora principal"
        )

    @patch(
        "builtins.print"
    )
    def test_mostrar_vinculo_none(
        self,
        mock_print,
    ):
        """
        Deve informar quando nenhum
        vínculo for recebido.
        """

        resultado = (
            interface_vinculos
            .mostrar_vinculo(
                None
            )
        )

        self.assertIsNone(
            resultado
        )

        mock_print.assert_called_once_with(
            "\nVínculo não encontrado."
        )

    # ========================================================
    # TESTES DAS CONSULTAS
    # ========================================================

    @patch(
        "app.interface."
        "vinculos_unidade_projeto_interface."
        "mostrar_vinculo"
    )
    @patch(
        "app.interface."
        "vinculos_unidade_projeto_interface."
        "vinculos_unidade_projeto."
        "listar_vinculos_do_projeto"
    )
    @patch(
        "app.interface."
        "vinculos_unidade_projeto_interface."
        "_ler_codigo",
        return_value=10,
    )
    @patch(
        "builtins.print"
    )
    def test_listar_vinculos_do_projeto(
        self,
        _mock_print,
        _mock_ler_codigo,
        mock_listar,
        mock_mostrar_vinculo,
    ):
        """
        Deve listar e exibir os vínculos
        ativos de um Projeto.
        """

        geradora = self.criar_vinculo_exemplo()

        beneficiaria = self.criar_vinculo_exemplo(
            codigo=2,
            codigo_unidade=21,
            papel=(
                PapelUnidadeProjeto.BENEFICIARIA
            ),
        )

        mock_listar.return_value = [
            geradora,
            beneficiaria,
        ]

        resultado = (
            interface_vinculos
            .listar_vinculos_do_projeto()
        )

        mock_listar.assert_called_once_with(
            codigo_projeto=10,
            somente_ativos=True,
        )

        self.assertEqual(
            resultado,
            [
                geradora,
                beneficiaria,
            ],
        )

        self.assertEqual(
            mock_mostrar_vinculo.call_count,
            2,
        )

    @patch(
        "app.interface."
        "vinculos_unidade_projeto_interface."
        "vinculos_unidade_projeto."
        "listar_vinculos_do_projeto"
    )
    @patch(
        "app.interface."
        "vinculos_unidade_projeto_interface."
        "_ler_codigo",
        return_value=10,
    )
    @patch(
        "builtins.print"
    )
    def test_listar_vinculos_projeto_sem_resultados(
        self,
        mock_print,
        _mock_ler_codigo,
        mock_listar,
    ):
        """
        Deve informar quando o Projeto
        não possuir vínculos ativos.
        """

        mock_listar.return_value = []

        resultado = (
            interface_vinculos
            .listar_vinculos_do_projeto()
        )

        self.assertEqual(
            resultado,
            [],
        )

        mock_print.assert_any_call(
            "\nNenhum vínculo ativo "
            "foi encontrado para o Projeto."
        )

    @patch(
        "app.interface."
        "vinculos_unidade_projeto_interface."
        "mostrar_vinculo"
    )
    @patch(
        "app.interface."
        "vinculos_unidade_projeto_interface."
        "vinculos_unidade_projeto."
        "obter_unidade_geradora_do_projeto"
    )
    @patch(
        "app.interface."
        "vinculos_unidade_projeto_interface."
        "_ler_codigo",
        return_value=10,
    )
    @patch(
        "builtins.print"
    )
    def test_mostrar_unidade_geradora_do_projeto(
        self,
        _mock_print,
        _mock_ler_codigo,
        mock_obter_geradora,
        mock_mostrar_vinculo,
    ):
        """
        Deve buscar e exibir a Geradora
        ativa do Projeto.
        """

        geradora = self.criar_vinculo_exemplo()

        mock_obter_geradora.return_value = (
            geradora
        )

        resultado = (
            interface_vinculos
            .mostrar_unidade_geradora_do_projeto()
        )

        mock_obter_geradora\
            .assert_called_once_with(
                10
            )

        mock_mostrar_vinculo\
            .assert_called_once_with(
                geradora
            )

        self.assertIs(
            resultado,
            geradora,
        )

    @patch(
        "app.interface."
        "vinculos_unidade_projeto_interface."
        "mostrar_vinculo"
    )
    @patch(
        "app.interface."
        "vinculos_unidade_projeto_interface."
        "vinculos_unidade_projeto."
        "listar_unidades_beneficiarias_do_projeto"
    )
    @patch(
        "app.interface."
        "vinculos_unidade_projeto_interface."
        "_ler_codigo",
        return_value=10,
    )
    @patch(
        "builtins.print"
    )
    def test_listar_unidades_beneficiarias(
        self,
        _mock_print,
        _mock_ler_codigo,
        mock_listar_beneficiarias,
        mock_mostrar_vinculo,
    ):
        """
        Deve buscar e exibir as Beneficiárias
        ativas do Projeto.
        """

        beneficiaria = self.criar_vinculo_exemplo(
            codigo=2,
            codigo_unidade=21,
            papel=(
                PapelUnidadeProjeto.BENEFICIARIA
            ),
        )

        mock_listar_beneficiarias.return_value = [
            beneficiaria,
        ]

        resultado = (
            interface_vinculos
            .listar_unidades_beneficiarias_do_projeto()
        )

        mock_listar_beneficiarias\
            .assert_called_once_with(
                10
            )

        mock_mostrar_vinculo\
            .assert_called_once_with(
                beneficiaria
            )

        self.assertEqual(
            resultado,
            [
                beneficiaria,
            ],
        )

    # ========================================================
    # TESTES DE ATIVAÇÃO E INATIVAÇÃO
    # ========================================================

    @patch(
        "app.interface."
        "vinculos_unidade_projeto_interface."
        "mostrar_vinculo"
    )
    @patch(
        "app.interface."
        "vinculos_unidade_projeto_interface."
        "vinculos_unidade_projeto."
        "inativar_vinculo"
    )
    @patch(
        "app.interface."
        "vinculos_unidade_projeto_interface."
        "_ler_codigo",
        return_value=1,
    )
    @patch(
        "builtins.print"
    )
    def test_inativar_vinculo(
        self,
        _mock_print,
        _mock_ler_codigo,
        mock_inativar,
        mock_mostrar_vinculo,
    ):
        """
        Deve solicitar o código e encaminhar
        a inativação para a fachada.
        """

        vinculo = self.criar_vinculo_exemplo(
            situacao=(
                SituacaoVinculoUnidadeProjeto
                .INATIVO
            ),
        )

        mock_inativar.return_value = vinculo

        resultado = (
            interface_vinculos
            .inativar_vinculo()
        )

        mock_inativar.assert_called_once_with(
            1
        )

        mock_mostrar_vinculo\
            .assert_called_once_with(
                vinculo
            )

        self.assertIs(
            resultado,
            vinculo,
        )

    @patch(
        "app.interface."
        "vinculos_unidade_projeto_interface."
        "mostrar_vinculo"
    )
    @patch(
        "app.interface."
        "vinculos_unidade_projeto_interface."
        "vinculos_unidade_projeto."
        "ativar_vinculo"
    )
    @patch(
        "app.interface."
        "vinculos_unidade_projeto_interface."
        "_ler_codigo",
        return_value=1,
    )
    @patch(
        "builtins.print"
    )
    def test_ativar_vinculo(
        self,
        _mock_print,
        _mock_ler_codigo,
        mock_ativar,
        mock_mostrar_vinculo,
    ):
        """
        Deve solicitar o código e encaminhar
        a ativação para a fachada.
        """

        vinculo = self.criar_vinculo_exemplo()

        mock_ativar.return_value = vinculo

        resultado = (
            interface_vinculos
            .ativar_vinculo()
        )

        mock_ativar.assert_called_once_with(
            1
        )

        mock_mostrar_vinculo\
            .assert_called_once_with(
                vinculo
            )

        self.assertIs(
            resultado,
            vinculo,
        )

    @patch(
        "app.interface."
        "vinculos_unidade_projeto_interface."
        "vinculos_unidade_projeto."
        "ativar_vinculo"
    )
    @patch(
        "app.interface."
        "vinculos_unidade_projeto_interface."
        "_ler_codigo",
        return_value=1,
    )
    @patch(
        "builtins.print"
    )
    def test_ativar_vinculo_trata_value_error(
        self,
        mock_print,
        _mock_ler_codigo,
        mock_ativar,
    ):
        """
        Deve tratar uma tentativa inválida
        de ativação.
        """

        mock_ativar.side_effect = ValueError(
            "O Projeto já possui uma "
            "Unidade Geradora ativa."
        )

        resultado = (
            interface_vinculos
            .ativar_vinculo()
        )

        self.assertIsNone(
            resultado
        )

        mock_print.assert_any_call(
            "\nNão foi possível ativar "
            "o vínculo: "
            "O Projeto já possui uma "
            "Unidade Geradora ativa."
        )


if __name__ == "__main__":
    unittest.main()