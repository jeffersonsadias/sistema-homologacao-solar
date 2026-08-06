"""
Testes da interface de Consultas Rápidas.

As fachadas, entradas e funções de exibição são simuladas
para impedir interação real com o terminal e com os dados
persistidos.
"""

import unittest
from unittest.mock import patch

from app.dominio.status_homologacao import (
    StatusHomologacao,
)

from app.interface import consultas_rapidas_interface


class TestConsultasRapidasInterface(
    unittest.TestCase
):
    """
    Testes das consultas e do submenu operacional.
    """

    # ========================================================
    # EXIBIÇÃO DE PROJETOS
    # ========================================================

    @patch(
        "app.interface.consultas_rapidas_interface."
        "projetos.mostrar_projeto"
    )
    def test_exibir_projetos(
        self,
        mock_mostrar_projeto,
    ):
        """
        Deve solicitar a exibição de cada Projeto
        recebido e apresentar o total.
        """

        lista_projetos = [
            {
                "codigo": 1,
            },
            {
                "codigo": 2,
            },
        ]

        with patch(
            "builtins.print"
        ) as mock_print:
            (
                consultas_rapidas_interface
                ._exibir_projetos(
                    lista_projetos
                )
            )

        self.assertEqual(
            mock_mostrar_projeto.call_count,
            2,
        )

        mock_mostrar_projeto.assert_any_call(
            lista_projetos[0]
        )

        mock_mostrar_projeto.assert_any_call(
            lista_projetos[1]
        )

        mock_print.assert_any_call(
            "\nTotal de Projetos encontrados: 2"
        )

    @patch(
        "builtins.print"
    )
    @patch(
        "app.interface.consultas_rapidas_interface."
        "projetos.mostrar_projeto"
    )
    def test_exibir_projetos_sem_resultados(
        self,
        mock_mostrar_projeto,
        mock_print,
    ):
        """
        Deve informar quando nenhum Projeto
        for encontrado.
        """

        (
            consultas_rapidas_interface
            ._exibir_projetos(
                []
            )
        )

        mock_mostrar_projeto.assert_not_called()

        mock_print.assert_any_call(
            "\nNenhum Projeto encontrado."
        )

    # ========================================================
    # EXIBIÇÃO DE HOMOLOGAÇÕES
    # ========================================================

    @patch(
        "app.interface.consultas_rapidas_interface."
        "_exibir_homologacao_resumida"
    )
    def test_exibir_homologacoes(
        self,
        mock_exibir_homologacao,
    ):
        """
        Deve exibir todas as Homologações
        recebidas e apresentar o total.
        """

        lista_homologacoes = [
            {
                "codigo": 1,
            },
            {
                "codigo": 2,
            },
        ]

        with patch(
            "builtins.print"
        ) as mock_print:
            (
                consultas_rapidas_interface
                ._exibir_homologacoes(
                    lista_homologacoes
                )
            )

        self.assertEqual(
            mock_exibir_homologacao.call_count,
            2,
        )

        mock_exibir_homologacao.assert_any_call(
            lista_homologacoes[0]
        )

        mock_exibir_homologacao.assert_any_call(
            lista_homologacoes[1]
        )

        mock_print.assert_any_call(
            "\nTotal de Homologações encontradas: 2"
        )

    @patch(
        "builtins.print"
    )
    @patch(
        "app.interface.consultas_rapidas_interface."
        "_exibir_homologacao_resumida"
    )
    def test_exibir_homologacoes_sem_resultados(
        self,
        mock_exibir_homologacao,
        mock_print,
    ):
        """
        Deve informar quando nenhuma Homologação
        for encontrada.
        """

        (
            consultas_rapidas_interface
            ._exibir_homologacoes(
                []
            )
        )

        mock_exibir_homologacao.assert_not_called()

        mock_print.assert_any_call(
            "\nNenhuma Homologação encontrada."
        )

    # ========================================================
    # SELEÇÃO DE STATUS
    # ========================================================

    @patch(
        "app.interface.consultas_rapidas_interface."
        "status.obter_status",
        return_value="Aprovado",
    )
    @patch(
        "app.interface.consultas_rapidas_interface."
        "status.exibir_status"
    )
    @patch(
        "app.interface.consultas_rapidas_interface."
        "ler_int",
        return_value=5,
    )
    def test_selecionar_status_projeto(
        self,
        mock_ler_int,
        mock_exibir_status,
        mock_obter_status,
    ):
        """
        Deve retornar o status de Projeto
        correspondente ao código informado.
        """

        resultado = (
            consultas_rapidas_interface
            ._selecionar_status_projeto()
        )

        mock_exibir_status.assert_called_once_with()

        mock_ler_int.assert_called_once_with(
            "\nDigite o código do status: "
        )

        mock_obter_status.assert_called_once_with(
            5
        )

        self.assertEqual(
            resultado,
            "Aprovado",
        )

    @patch(
        "builtins.print"
    )
    @patch(
        "app.interface.consultas_rapidas_interface."
        "status.obter_status",
        return_value=None,
    )
    @patch(
        "app.interface.consultas_rapidas_interface."
        "status.exibir_status"
    )
    @patch(
        "app.interface.consultas_rapidas_interface."
        "ler_int",
        return_value=999,
    )
    def test_selecionar_status_projeto_invalido(
        self,
        mock_ler_int,
        mock_exibir_status,
        mock_obter_status,
        mock_print,
    ):
        """
        Deve retornar None quando o código
        do status de Projeto for inválido.
        """

        resultado = (
            consultas_rapidas_interface
            ._selecionar_status_projeto()
        )

        self.assertIsNone(
            resultado
        )

        mock_print.assert_any_call(
            "\nStatus de Projeto inválido."
        )

    @patch(
        "app.interface.consultas_rapidas_interface."
        "ler_int",
        return_value=1,
    )
    def test_selecionar_status_homologacao(
        self,
        mock_ler_int,
    ):
        """
        A primeira opção deve retornar
        o primeiro StatusHomologacao.
        """

        resultado = (
            consultas_rapidas_interface
            ._selecionar_status_homologacao()
        )

        self.assertEqual(
            resultado,
            StatusHomologacao.EM_PREPARACAO,
        )

    @patch(
        "builtins.print"
    )
    @patch(
        "app.interface.consultas_rapidas_interface."
        "ler_int",
        return_value=999,
    )
    def test_selecionar_status_homologacao_invalido(
        self,
        mock_ler_int,
        mock_print,
    ):
        """
        Deve rejeitar uma opção fora do intervalo
        dos status oficiais da Homologação.
        """

        resultado = (
            consultas_rapidas_interface
            ._selecionar_status_homologacao()
        )

        self.assertIsNone(
            resultado
        )

        mock_print.assert_any_call(
            "\nStatus de Homologação inválido."
        )

    # ========================================================
    # CONSULTAS DE PROJETOS
    # ========================================================

    @patch(
        "app.interface.consultas_rapidas_interface."
        "_exibir_projetos"
    )
    @patch(
        "app.interface.consultas_rapidas_interface."
        "projetos.buscar_projetos_do_cliente"
    )
    @patch(
        "app.interface.consultas_rapidas_interface."
        "ler_int",
        return_value=10,
    )
    def test_consultar_projetos_por_cliente(
        self,
        mock_ler_int,
        mock_buscar,
        mock_exibir,
    ):
        """
        Deve buscar e exibir os Projetos
        vinculados ao Cliente informado.
        """

        projetos_encontrados = [
            {
                "codigo": 1,
                "cliente": 10,
            }
        ]

        mock_buscar.return_value = (
            projetos_encontrados
        )

        (
            consultas_rapidas_interface
            .consultar_projetos_por_cliente()
        )

        mock_buscar.assert_called_once_with(
            10
        )

        mock_exibir.assert_called_once_with(
            projetos_encontrados
        )

    @patch(
        "app.interface.consultas_rapidas_interface."
        "_exibir_projetos"
    )
    @patch(
        "app.interface.consultas_rapidas_interface."
        "projetos.buscar_projetos_com_status"
    )
    @patch(
        "app.interface.consultas_rapidas_interface."
        "_selecionar_status_projeto",
        return_value="Aprovado",
    )
    def test_consultar_projetos_por_status(
        self,
        mock_selecionar_status,
        mock_buscar,
        mock_exibir,
    ):
        """
        Deve buscar e exibir Projetos
        com o status selecionado.
        """

        projetos_encontrados = [
            {
                "codigo": 1,
                "status": "Aprovado",
            }
        ]

        mock_buscar.return_value = (
            projetos_encontrados
        )

        (
            consultas_rapidas_interface
            .consultar_projetos_por_status()
        )

        mock_buscar.assert_called_once_with(
            "Aprovado"
        )

        mock_exibir.assert_called_once_with(
            projetos_encontrados
        )

    @patch(
        "app.interface.consultas_rapidas_interface."
        "_exibir_projetos"
    )
    @patch(
        "app.interface.consultas_rapidas_interface."
        "projetos.buscar_projetos_com_status"
    )
    @patch(
        "app.interface.consultas_rapidas_interface."
        "_selecionar_status_projeto",
        return_value=None,
    )
    def test_consultar_projetos_por_status_invalido(
        self,
        mock_selecionar_status,
        mock_buscar,
        mock_exibir,
    ):
        """
        Um status inválido deve encerrar a consulta
        sem chamar a fachada.
        """

        (
            consultas_rapidas_interface
            .consultar_projetos_por_status()
        )

        mock_buscar.assert_not_called()
        mock_exibir.assert_not_called()

    # ========================================================
    # CONSULTAS DE HOMOLOGAÇÕES
    # ========================================================

    @patch(
        "app.interface.consultas_rapidas_interface."
        "_exibir_homologacao_resumida"
    )
    @patch(
        "app.interface.consultas_rapidas_interface."
        "homologacoes.buscar_homologacao_por_projeto"
    )
    @patch(
        "app.interface.consultas_rapidas_interface."
        "ler_int",
        side_effect=[
            10,
            20,
        ],
    )
    def test_consultar_homologacao_por_projeto(
        self,
        mock_ler_int,
        mock_buscar,
        mock_exibir,
    ):
        """
        Deve consultar a Homologação ativa
        do Projeto dentro da Empresa.
        """

        homologacao_encontrada = {
            "codigo": 1,
        }

        mock_buscar.return_value = (
            homologacao_encontrada
        )

        (
            consultas_rapidas_interface
            .consultar_homologacao_por_projeto()
        )

        mock_buscar.assert_called_once_with(
            codigo_projeto=20,
            codigo_empresa=10,
        )

        mock_exibir.assert_called_once_with(
            homologacao_encontrada
        )

    @patch(
        "builtins.print"
    )
    @patch(
        "app.interface.consultas_rapidas_interface."
        "_exibir_homologacao_resumida"
    )
    @patch(
        "app.interface.consultas_rapidas_interface."
        "homologacoes.buscar_homologacao_por_projeto",
        return_value=None,
    )
    @patch(
        "app.interface.consultas_rapidas_interface."
        "ler_int",
        side_effect=[
            10,
            999,
        ],
    )
    def test_consultar_homologacao_por_projeto_sem_resultado(
        self,
        mock_ler_int,
        mock_buscar,
        mock_exibir,
        mock_print,
    ):
        """
        Deve informar quando não existir
        Homologação ativa para o Projeto.
        """

        (
            consultas_rapidas_interface
            .consultar_homologacao_por_projeto()
        )

        mock_exibir.assert_not_called()

        mock_print.assert_any_call(
            "\nNenhuma Homologação ativa encontrada "
            "para o Projeto."
        )

    @patch(
        "app.interface.consultas_rapidas_interface."
        "_exibir_homologacoes"
    )
    @patch(
        "app.interface.consultas_rapidas_interface."
        "homologacoes.listar_homologacoes"
    )
    @patch(
        "app.interface.consultas_rapidas_interface."
        "ler_int",
        return_value=10,
    )
    def test_consultar_homologacoes_por_empresa(
        self,
        mock_ler_int,
        mock_listar,
        mock_exibir,
    ):
        """
        Deve listar as Homologações
        pertencentes à Empresa.
        """

        homologacoes_encontradas = [
            {
                "codigo": 1,
            }
        ]

        mock_listar.return_value = (
            homologacoes_encontradas
        )

        (
            consultas_rapidas_interface
            .consultar_homologacoes_por_empresa()
        )

        mock_listar.assert_called_once_with(
            codigo_empresa=10,
        )

        mock_exibir.assert_called_once_with(
            homologacoes_encontradas
        )

    @patch(
        "app.interface.consultas_rapidas_interface."
        "_exibir_homologacoes"
    )
    @patch(
        "app.interface.consultas_rapidas_interface."
        "homologacoes."
        "listar_homologacoes_por_concessionaria"
    )
    @patch(
        "app.interface.consultas_rapidas_interface."
        "ler_int",
        side_effect=[
            10,
            30,
        ],
    )
    def test_consultar_homologacoes_por_concessionaria(
        self,
        mock_ler_int,
        mock_listar,
        mock_exibir,
    ):
        """
        Deve buscar Homologações por
        Concessionária e Empresa.
        """

        homologacoes_encontradas = [
            {
                "codigo": 1,
            }
        ]

        mock_listar.return_value = (
            homologacoes_encontradas
        )

        (
            consultas_rapidas_interface
            .consultar_homologacoes_por_concessionaria()
        )

        mock_listar.assert_called_once_with(
            codigo_concessionaria=30,
            codigo_empresa=10,
        )

        mock_exibir.assert_called_once_with(
            homologacoes_encontradas
        )

    @patch(
        "app.interface.consultas_rapidas_interface."
        "_exibir_homologacoes"
    )
    @patch(
        "app.interface.consultas_rapidas_interface."
        "homologacoes.listar_homologacoes_por_status"
    )
    @patch(
        "app.interface.consultas_rapidas_interface."
        "_selecionar_status_homologacao",
        return_value=StatusHomologacao.EM_ANALISE,
    )
    @patch(
        "app.interface.consultas_rapidas_interface."
        "ler_int",
        return_value=10,
    )
    def test_consultar_homologacoes_por_status(
        self,
        mock_ler_int,
        mock_selecionar_status,
        mock_listar,
        mock_exibir,
    ):
        """
        Deve buscar as Homologações da Empresa
        com o status selecionado.
        """

        homologacoes_encontradas = [
            {
                "codigo": 1,
                "status": "EM_ANALISE",
            }
        ]

        mock_listar.return_value = (
            homologacoes_encontradas
        )

        (
            consultas_rapidas_interface
            .consultar_homologacoes_por_status()
        )

        mock_listar.assert_called_once_with(
            status=StatusHomologacao.EM_ANALISE,
            codigo_empresa=10,
        )

        mock_exibir.assert_called_once_with(
            homologacoes_encontradas
        )

    @patch(
        "app.interface.consultas_rapidas_interface."
        "_exibir_homologacoes"
    )
    @patch(
        "app.interface.consultas_rapidas_interface."
        "homologacoes.listar_homologacoes_por_status"
    )
    @patch(
        "app.interface.consultas_rapidas_interface."
        "_selecionar_status_homologacao",
        return_value=None,
    )
    @patch(
        "app.interface.consultas_rapidas_interface."
        "ler_int",
        return_value=10,
    )
    def test_consultar_homologacoes_por_status_invalido(
        self,
        mock_ler_int,
        mock_selecionar_status,
        mock_listar,
        mock_exibir,
    ):
        """
        Um status inválido deve encerrar a consulta
        sem acessar a fachada.
        """

        (
            consultas_rapidas_interface
            .consultar_homologacoes_por_status()
        )

        mock_listar.assert_not_called()
        mock_exibir.assert_not_called()

    # ========================================================
    # MENU
    # ========================================================

    @patch(
        "app.interface.consultas_rapidas_interface."
        "_pausar"
    )
    @patch(
        "app.interface.consultas_rapidas_interface."
        "consultar_projetos_por_cliente"
    )
    @patch(
        "builtins.input",
        side_effect=[
            "1",
            "0",
        ],
    )
    def test_menu_deve_abrir_projetos_por_cliente(
        self,
        mock_input,
        mock_consultar,
        mock_pausar,
    ):
        """
        A opção 1 deve abrir
        Projetos por Cliente.
        """

        (
            consultas_rapidas_interface
            .menu_consultas_rapidas()
        )

        mock_consultar.assert_called_once_with()
        mock_pausar.assert_called_once_with()

    @patch(
        "app.interface.consultas_rapidas_interface."
        "_pausar"
    )
    @patch(
        "app.interface.consultas_rapidas_interface."
        "consultar_homologacao_por_projeto"
    )
    @patch(
        "builtins.input",
        side_effect=[
            "2",
            "0",
        ],
    )
    def test_menu_deve_abrir_homologacao_por_projeto(
        self,
        mock_input,
        mock_consultar,
        mock_pausar,
    ):
        """
        A opção 2 deve abrir a consulta
        de Homologação por Projeto.
        """

        (
            consultas_rapidas_interface
            .menu_consultas_rapidas()
        )

        mock_consultar.assert_called_once_with()
        mock_pausar.assert_called_once_with()

    @patch(
        "app.interface.consultas_rapidas_interface."
        "_pausar"
    )
    @patch(
        "app.interface.consultas_rapidas_interface."
        "consultar_homologacoes_por_empresa"
    )
    @patch(
        "builtins.input",
        side_effect=[
            "3",
            "0",
        ],
    )
    def test_menu_deve_abrir_homologacoes_por_empresa(
        self,
        mock_input,
        mock_consultar,
        mock_pausar,
    ):
        """
        A opção 3 deve abrir
        Homologações por Empresa.
        """

        (
            consultas_rapidas_interface
            .menu_consultas_rapidas()
        )

        mock_consultar.assert_called_once_with()
        mock_pausar.assert_called_once_with()

    @patch(
        "app.interface.consultas_rapidas_interface."
        "_pausar"
    )
    @patch(
        "app.interface.consultas_rapidas_interface."
        "consultar_homologacoes_por_concessionaria"
    )
    @patch(
        "builtins.input",
        side_effect=[
            "4",
            "0",
        ],
    )
    def test_menu_deve_abrir_homologacoes_por_concessionaria(
        self,
        mock_input,
        mock_consultar,
        mock_pausar,
    ):
        """
        A opção 4 deve abrir a consulta
        por Concessionária.
        """

        (
            consultas_rapidas_interface
            .menu_consultas_rapidas()
        )

        mock_consultar.assert_called_once_with()
        mock_pausar.assert_called_once_with()

    @patch(
        "app.interface.consultas_rapidas_interface."
        "_pausar"
    )
    @patch(
        "app.interface.consultas_rapidas_interface."
        "consultar_projetos_por_status"
    )
    @patch(
        "builtins.input",
        side_effect=[
            "5",
            "0",
        ],
    )
    def test_menu_deve_abrir_projetos_por_status(
        self,
        mock_input,
        mock_consultar,
        mock_pausar,
    ):
        """
        A opção 5 deve abrir
        Projetos por Status.
        """

        (
            consultas_rapidas_interface
            .menu_consultas_rapidas()
        )

        mock_consultar.assert_called_once_with()
        mock_pausar.assert_called_once_with()

    @patch(
        "app.interface.consultas_rapidas_interface."
        "_pausar"
    )
    @patch(
        "app.interface.consultas_rapidas_interface."
        "consultar_homologacoes_por_status"
    )
    @patch(
        "builtins.input",
        side_effect=[
            "6",
            "0",
        ],
    )
    def test_menu_deve_abrir_homologacoes_por_status(
        self,
        mock_input,
        mock_consultar,
        mock_pausar,
    ):
        """
        A opção 6 deve abrir
        Homologações por Status.
        """

        (
            consultas_rapidas_interface
            .menu_consultas_rapidas()
        )

        mock_consultar.assert_called_once_with()
        mock_pausar.assert_called_once_with()

    @patch(
        "app.interface.consultas_rapidas_interface."
        "_pausar"
    )
    @patch(
        "builtins.print"
    )
    @patch(
        "builtins.input",
        side_effect=[
            "99",
            "0",
        ],
    )
    def test_menu_deve_tratar_opcao_invalida(
        self,
        mock_input,
        mock_print,
        mock_pausar,
    ):
        """
        Uma opção desconhecida deve exibir erro
        e manter o submenu em execução.
        """

        (
            consultas_rapidas_interface
            .menu_consultas_rapidas()
        )

        mock_print.assert_any_call(
            "\nOpção inválida."
        )

        mock_pausar.assert_called_once_with()


if __name__ == "__main__":
    unittest.main()