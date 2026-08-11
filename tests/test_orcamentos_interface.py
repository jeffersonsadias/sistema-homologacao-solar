import unittest
from unittest.mock import Mock, patch

from app.interface import orcamentos_interface


class TestOrcamentosInterface(unittest.TestCase):
    """
    Testes da interface de terminal de Orçamentos.

    As dependências externas são substituídas por mocks
    para que os testes não utilizem arquivos reais,
    clientes reais nem entradas manuais.
    """

    def setUp(self):
        """
        Cria uma lista vazia exclusiva
        para cada teste.
        """

        self.orcamentos = []

    # ========================================================
    # CADASTRO
    # ========================================================

    @patch(
        "app.interface.orcamentos_interface."
        "salvar_orcamentos"
    )
    @patch(
        "app.interface.orcamentos_interface."
        "criar_dados_orcamento"
    )
    @patch(
        "app.interface.orcamentos_interface."
        "_coletar_dados_comerciais"
    )
    @patch(
        "app.interface.orcamentos_interface."
        "_coletar_local_instalacao"
    )
    @patch(
        "app.interface.orcamentos_interface."
        "_coletar_inversores"
    )
    @patch(
        "app.interface.orcamentos_interface."
        "_coletar_modulos"
    )
    @patch(
        "app.interface.orcamentos_interface."
        "_coletar_dimensionamento"
    )
    @patch(
        "app.interface.orcamentos_interface."
        "utils.gerar_proximo_codigo"
    )
    @patch(
        "app.interface.orcamentos_interface."
        "clientes.selecionar_cliente"
    )
    @patch(
        "app.interface.orcamentos_interface."
        "_selecionar_concessionaria_orcamento"
    )
    @patch(
        "app.interface.orcamentos_interface."
        "_selecionar_empresa_orcamento"
    )
    def test_cadastrar_orcamento(
        self,
        mock_selecionar_empresa,
        mock_selecionar_concessionaria,
        mock_selecionar_cliente,
        mock_gerar_codigo,
        mock_dimensionamento,
        mock_modulos,
        mock_inversores,
        mock_local,
        mock_comercial,
        mock_criar_dados,
        mock_salvar,
    ):
        """
        Deve criar, adicionar e salvar
        um novo Orçamento.
        """

        empresa = {
            "codigo": 50,
            "nome": "Solar Alfa",
        }

        mock_selecionar_empresa.return_value = (
            empresa
        )

        concessionaria = Mock()
        concessionaria.codigo = 20
        concessionaria.nome = "Neoenergia Coelba"

        mock_selecionar_concessionaria.return_value = (
            concessionaria
        )

        cliente = {
            "codigo": 10,
            "nome": "Cliente Teste",
        }

        dimensionamento = {
            "consumo_medio_kwh": 500.0,
            "potencia_prevista_kwp": 4.5,
        }

        modulos = {
            "quantidade": 8,
            "fabricante": "Fabricante A",
        }

        inversores = {
            "quantidade": 1,
            "fabricante": "Fabricante B",
            "tensao": "220 V",
        }

        local = {
            "codigo_uc": "123",
            "tipo_telhado": "Cerâmico",
        }

        comercial = {
            "valor_total": 20000.0,
            "validade_dias": 10,
            "prazo_instalacao_dias": 30,
        }

        orcamento_criado = {
            "codigo": 1,
            "codigo_empresa": 50,
            "codigo_concessionaria": 20,
            "cliente": 10,
            "dimensionamento": dimensionamento,
            "modulos": modulos,
            "inversores": inversores,
            "local_instalacao": local,
            "comercial": comercial,
            "status": "Em negociação",
        }

        mock_selecionar_cliente.return_value = cliente
        mock_gerar_codigo.return_value = 1
        mock_dimensionamento.return_value = dimensionamento
        mock_modulos.return_value = modulos
        mock_inversores.return_value = inversores
        mock_local.return_value = local
        mock_comercial.return_value = comercial
        mock_criar_dados.return_value = orcamento_criado

        resultado = (
            orcamentos_interface.cadastrar_orcamento(
                self.orcamentos
            )
        )

        mock_criar_dados.assert_called_once_with(
            codigo=1,
            codigo_empresa=50,
            codigo_concessionaria=20,
            codigo_cliente=10,
            dimensionamento=dimensionamento,
            modulos=modulos,
            inversores=inversores,
            local_instalacao=local,
            comercial=comercial,
            status_inicial=(
                orcamentos_interface
                .status_orcamento
                .STATUS_INICIAL
            ),
        )

        self.assertEqual(
            local["distribuidora"],
            "Neoenergia Coelba",
        )

        self.assertEqual(
            self.orcamentos,
            [orcamento_criado],
        )

        mock_salvar.assert_called_once_with(
            self.orcamentos
        )

        self.assertEqual(
            resultado,
            orcamento_criado,
        )

    @patch(
        "app.interface.orcamentos_interface."
        "clientes.selecionar_cliente"
    )
    @patch(
        "app.interface.orcamentos_interface."
        "_selecionar_empresa_orcamento",
        return_value=None,
    )
    def test_cadastrar_orcamento_sem_empresa(
        self,
        mock_selecionar_empresa,
        mock_selecionar_cliente,
    ):
        """
        Não deve continuar o cadastro
        quando não houver Empresa válida.
        """

        resultado = (
            orcamentos_interface
            .cadastrar_orcamento(
                self.orcamentos
            )
        )

        self.assertIsNone(
            resultado
        )

        self.assertEqual(
            self.orcamentos,
            [],
        )

        mock_selecionar_cliente.assert_not_called()

    @patch(
        "app.interface.orcamentos_interface."
        "clientes.selecionar_cliente"
    )
    @patch(
        "app.interface.orcamentos_interface."
        "_selecionar_empresa_orcamento",
        return_value={
            "codigo": 50,
            "nome": "Solar Alfa",
        },
    )
    def test_cadastrar_orcamento_sem_cliente(
        self,
        mock_selecionar_empresa,
        mock_selecionar_cliente,
    ):
        """
        Não deve criar Orçamento sem cliente válido.
        """

        mock_selecionar_cliente.return_value = None

        resultado = (
            orcamentos_interface.cadastrar_orcamento(
                self.orcamentos
            )
        )

        self.assertIsNone(resultado)

        self.assertEqual(
            self.orcamentos,
            [],
        )

    @patch(
        "app.interface.orcamentos_interface."
        "utils.gerar_proximo_codigo"
    )
    @patch(
        "app.interface.orcamentos_interface."
        "_selecionar_concessionaria_orcamento",
        return_value=None,
    )
    @patch(
        "app.interface.orcamentos_interface."
        "clientes.selecionar_cliente",
        return_value={
            "codigo": 10,
            "nome": "Cliente Teste",
        },
    )
    @patch(
        "app.interface.orcamentos_interface."
        "_selecionar_empresa_orcamento",
        return_value={
            "codigo": 50,
            "nome": "Solar Alfa",
        },
    )
    def test_cadastrar_orcamento_sem_concessionaria(
        self,
        mock_selecionar_empresa,
        mock_selecionar_cliente,
        mock_selecionar_concessionaria,
        mock_gerar_codigo,
    ):
        """
        Não deve continuar o cadastro quando
        não houver Concessionária válida.
        """

        resultado = (
            orcamentos_interface
            .cadastrar_orcamento(
                self.orcamentos
            )
        )

        self.assertIsNone(
            resultado
        )

        self.assertEqual(
            self.orcamentos,
            [],
        )

        mock_gerar_codigo.assert_not_called()

    @patch(
        "app.interface.orcamentos_interface."
        "empresas.empresa_esta_ativa",
        return_value=True,
    )
    @patch(
        "app.interface.orcamentos_interface."
        "empresas.obter_empresa"
    )
    @patch(
        "app.interface.orcamentos_interface."
        "utils.ler_int",
        return_value=10,
    )
    def test_selecionar_empresa_orcamento(
        self,
        mock_ler_int,
        mock_obter_empresa,
        mock_empresa_ativa,
    ):
        empresa = {
            "codigo": 10,
            "nome": "Solar Alfa",
        }

        mock_obter_empresa.return_value = (
            empresa
        )

        resultado = (
            orcamentos_interface
            ._selecionar_empresa_orcamento()
        )

        self.assertIs(
            resultado,
            empresa,
        )

        mock_obter_empresa.assert_called_once_with(
            10
        )

        mock_empresa_ativa.assert_called_once_with(
            10
        )

    @patch(
        "app.interface.orcamentos_interface."
        "empresas.empresa_esta_ativa",
        return_value=False,
    )
    @patch(
        "app.interface.orcamentos_interface."
        "empresas.obter_empresa",
        return_value={
            "codigo": 10,
        },
    )
    @patch(
        "app.interface.orcamentos_interface."
        "utils.ler_int",
        return_value=10,
    )
    def test_nao_deve_selecionar_empresa_inativa(
        self,
        mock_ler_int,
        mock_obter_empresa,
        mock_empresa_ativa,
    ):
        resultado = (
            orcamentos_interface
            ._selecionar_empresa_orcamento()
        )

        self.assertIsNone(
            resultado
        )

    @patch(
        "app.interface.orcamentos_interface."
        "concessionarias.obter_concessionaria"
    )
    @patch(
        "app.interface.orcamentos_interface."
        "utils.ler_int",
        return_value=20,
    )
    def test_selecionar_concessionaria_orcamento(
        self,
        mock_ler_int,
        mock_obter_concessionaria,
    ):
        """
        Deve retornar a Concessionária
        encontrada pela fachada.
        """

        concessionaria = Mock()
        concessionaria.codigo = 20
        concessionaria.nome = "Neoenergia Coelba"

        mock_obter_concessionaria.return_value = (
            concessionaria
        )

        resultado = (
            orcamentos_interface
            ._selecionar_concessionaria_orcamento()
        )

        self.assertIs(
            resultado,
            concessionaria,
        )

        mock_obter_concessionaria.assert_called_once_with(
            20
        )

    @patch(
        "builtins.print"
    )
    @patch(
        "app.interface.orcamentos_interface."
        "concessionarias.obter_concessionaria",
        side_effect=ValueError(
            "Concessionária não encontrada."
        ),
    )
    @patch(
        "app.interface.orcamentos_interface."
        "utils.ler_int",
        return_value=20,
    )
    def test_nao_deve_selecionar_concessionaria_inexistente(
        self,
        mock_ler_int,
        mock_obter_concessionaria,
        mock_print,
    ):
        """
        Deve retornar None quando a
        Concessionária não existir.
        """

        resultado = (
            orcamentos_interface
            ._selecionar_concessionaria_orcamento()
        )

        self.assertIsNone(
            resultado
        )

        mock_obter_concessionaria.assert_called_once_with(
            20
        )

        mock_print.assert_any_call(
            "\nNão foi possível selecionar "
            "a Concessionária: "
            "Concessionária não encontrada."
        )

    # ========================================================
    # LISTAGEM E SELEÇÃO
    # ========================================================

    @patch("builtins.print")
    def test_listar_orcamentos_vazio(
        self,
        mock_print,
    ):
        """
        Deve informar quando não existem
        Orçamentos cadastrados.
        """

        orcamentos_interface.listar_orcamentos(
            self.orcamentos
        )

        mock_print.assert_any_call(
            "Nenhum orçamento cadastrado."
        )

    @patch(
        "app.interface.orcamentos_interface."
        "mostrar_orcamento"
    )
    def test_listar_orcamentos(
        self,
        mock_mostrar,
    ):
        """
        Deve exibir cada Orçamento da coleção.
        """

        orcamento_1 = {
            "codigo": 1,
        }

        orcamento_2 = {
            "codigo": 2,
        }

        self.orcamentos.extend(
            [
                orcamento_1,
                orcamento_2,
            ]
        )

        orcamentos_interface.listar_orcamentos(
            self.orcamentos
        )

        self.assertEqual(
            mock_mostrar.call_count,
            2,
        )

        mock_mostrar.assert_any_call(
            orcamento_1
        )

        mock_mostrar.assert_any_call(
            orcamento_2
        )

    @patch(
        "app.interface.orcamentos_interface."
        "buscar_orcamento_por_codigo"
    )
    @patch(
        "app.interface.orcamentos_interface."
        "utils.ler_int"
    )
    def test_selecionar_orcamento(
        self,
        mock_ler_int,
        mock_buscar,
    ):
        """
        Deve retornar o Orçamento selecionado.
        """

        orcamento = {
            "codigo": 3,
        }

        mock_ler_int.return_value = 3
        mock_buscar.return_value = orcamento

        resultado = (
            orcamentos_interface.selecionar_orcamento(
                self.orcamentos
            )
        )

        mock_buscar.assert_called_once_with(
            self.orcamentos,
            3,
        )

        self.assertEqual(
            resultado,
            orcamento,
        )

    # ========================================================
    # ALTERAÇÃO DE STATUS
    # ========================================================

    @patch(
        "app.interface.orcamentos_interface."
        "salvar_orcamentos"
    )
    @patch(
        "app.interface.orcamentos_interface."
        "status_orcamento.transicao_permitida"
    )
    @patch(
        "app.interface.orcamentos_interface."
        "status_orcamento.obter_status"
    )
    @patch(
        "app.interface.orcamentos_interface."
        "status_orcamento.exibir_status"
    )
    @patch(
        "app.interface.orcamentos_interface."
        "utils.ler_int"
    )
    @patch(
        "app.interface.orcamentos_interface."
        "mostrar_orcamento"
    )
    @patch(
        "app.interface.orcamentos_interface."
        "selecionar_orcamento"
    )
    def test_alterar_status(
        self,
        mock_selecionar,
        mock_mostrar,
        mock_ler_int,
        mock_exibir_status,
        mock_obter_status,
        mock_transicao,
        mock_salvar,
    ):
        """
        Deve alterar e salvar um status permitido.
        """

        orcamento = {
            "codigo": 1,
            "status": "Em negociação",
        }

        mock_selecionar.return_value = orcamento
        mock_ler_int.return_value = 2
        mock_obter_status.return_value = "Aprovado"
        mock_transicao.return_value = True

        resultado = (
            orcamentos_interface.alterar_status(
                self.orcamentos
            )
        )

        mock_transicao.assert_called_once_with(
            "Em negociação",
            "Aprovado",
        )

        self.assertEqual(
            orcamento["status"],
            "Aprovado",
        )

        mock_salvar.assert_called_once_with(
            self.orcamentos
        )

        self.assertEqual(
            resultado,
            orcamento,
        )

    # ========================================================
    # INTEGRAÇÃO PROJETO → HOMOLOGAÇÃO
    # ========================================================

    @patch(
        "builtins.input",
        return_value="1",
    )
    def test_confirmar_inicio_homologacao_deve_retornar_true(
        self,
        mock_input,
    ):
        """
        A opção 1 deve confirmar o início da Homologação.
        """

        resultado = (
            orcamentos_interface
            ._confirmar_inicio_homologacao()
        )

        self.assertTrue(
            resultado
        )

        mock_input.assert_called_once_with(
            "Escolha uma opção: "
        )

    @patch(
        "builtins.input",
        return_value="2",
    )
    def test_confirmar_inicio_homologacao_deve_retornar_false(
        self,
        mock_input,
    ):
        """
        A opção 2 deve recusar o início imediato
        da Homologação.
        """

        resultado = (
            orcamentos_interface
            ._confirmar_inicio_homologacao()
        )

        self.assertFalse(
            resultado
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
    def test_confirmar_inicio_homologacao_deve_repetir_opcao_invalida(
        self,
        mock_input,
        mock_print,
    ):
        """
        Uma opção inválida deve ser rejeitada,
        mantendo a pergunta até uma resposta válida.
        """

        resultado = (
            orcamentos_interface
            ._confirmar_inicio_homologacao()
        )

        self.assertTrue(
            resultado
        )

        self.assertEqual(
            mock_input.call_count,
            2,
        )

        mock_print.assert_any_call(
            "\nOpção inválida. Informe 1 ou 2."
        )

    @patch(
        "builtins.print"
    )
    @patch(
        "app.interface.orcamentos_interface."
        "_confirmar_inicio_homologacao",
        return_value=False,
    )
    def test_nao_iniciar_homologacao_deve_preservar_projeto(
        self,
        mock_confirmar,
        mock_print,
    ):
        """
        Quando o operador escolher Não:

        - nenhuma Homologação deve ser criada;
        - o Projeto deve permanecer válido;
        - o helper deve retornar None.
        """

        projeto = {
            "codigo": 50,
        }

        resultado = (
            orcamentos_interface
            ._iniciar_homologacao_do_projeto(
                projeto
            )
        )

        self.assertIsNone(
            resultado
        )

        mock_confirmar.assert_called_once_with()

        mock_print.assert_any_call(
            "A Homologação poderá ser iniciada "
            "posteriormente pelo menu de Homologações."
        )

    @patch(
        "app.interface.orcamentos_interface."
        "homologacoes.criar_homologacao"
    )
    @patch(
        "builtins.input",
        side_effect=[
            "2026-08-04",
            "Ana Lima",
            "Abertura integrada.",
        ],
    )
    @patch(
        "app.interface.orcamentos_interface."
        "_confirmar_inicio_homologacao",
        return_value=True,
    )
    def test_iniciar_homologacao_deve_criar_processo(
        self,
        mock_confirmar,
        mock_input,
        mock_criar_homologacao,
    ):
        """
        Quando o operador confirmar, os dados devem ser
        encaminhados corretamente à fachada de Homologações.
        """

        projeto = {
            "codigo": 50,
            "codigo_empresa": 1,
            "codigo_concessionaria": 2,
        }

        homologacao_criada = {
            "codigo": 8,
            "status": "EM_PREPARACAO",
        }

        mock_criar_homologacao.return_value = (
            homologacao_criada
        )

        resultado = (
            orcamentos_interface
            ._iniciar_homologacao_do_projeto(
                projeto
            )
        )

        mock_criar_homologacao.assert_called_once_with(
            codigo_empresa=1,
            codigo_projeto=50,
            codigo_concessionaria=2,
            data_abertura="2026-08-04",
            responsavel_abertura="Ana Lima",
            observacoes="Abertura integrada.",
        )

        self.assertIs(
            resultado,
            homologacao_criada,
        )

    @patch(
        "builtins.print"
    )
    @patch(
        "app.interface.orcamentos_interface."
        "homologacoes.criar_homologacao",
        side_effect=ValueError(
            "Projeto já possui uma Homologação ativa."
        ),
    )
    @patch(
        "builtins.input",
        side_effect=[
            "2026-08-04",
            "Ana Lima",
            "",
        ],
    )
    @patch(
        "app.interface.orcamentos_interface."
        "_confirmar_inicio_homologacao",
        return_value=True,
    )
    def test_falha_na_homologacao_nao_deve_invalidar_projeto(
        self,
        mock_confirmar,
        mock_input,
        mock_criar_homologacao,
        mock_print,
    ):
        """
        Uma falha ao abrir a Homologação não deve remover,
        alterar ou invalidar o Projeto já criado.
        """

        projeto = {
            "codigo": 50,
            "codigo_empresa": 1,
            "codigo_concessionaria": 2,
            "status": "Aguardando documentação",
        }

        projeto_antes = projeto.copy()

        resultado = (
            orcamentos_interface
            ._iniciar_homologacao_do_projeto(
                projeto
            )
        )

        self.assertIsNone(
            resultado
        )

        self.assertEqual(
            projeto,
            projeto_antes,
        )

        mock_print.assert_any_call(
            "Projeto já possui uma Homologação ativa."
        )

        mock_print.assert_any_call(
            "\nA Homologação poderá ser iniciada "
            "posteriormente pelo menu."
        )

    @patch(
        "app.interface.orcamentos_interface."
        "_iniciar_homologacao_do_projeto"
    )
    @patch(
        "app.interface.orcamentos_interface."
        "salvar_orcamentos"
    )
    @patch(
        "app.interface.orcamentos_interface."
        "projetos.criar_projeto_a_partir_do_orcamento"
    )
    @patch(
        "app.interface.orcamentos_interface."
        "orcamento_pode_ser_convertido"
    )
    @patch(
        "app.interface.orcamentos_interface."
        "mostrar_orcamento"
    )
    @patch(
        "app.interface.orcamentos_interface."
        "selecionar_orcamento"
    )
    def test_converter_para_projeto(
        self,
        mock_selecionar,
        mock_mostrar,
        mock_pode_converter,
        mock_criar_projeto,
        mock_salvar,
        mock_iniciar_homologacao,
    ):
        """
        Deve criar o Projeto e atualizar
        o status do Orçamento.
        """

        orcamento = {
            "codigo": 1,
            "status": "Aprovado",
        }

        projeto = {
            "codigo": 50,
        }

        mock_selecionar.return_value = orcamento
        mock_pode_converter.return_value = True
        mock_criar_projeto.return_value = projeto

        resultado = (
            orcamentos_interface.converter_para_projeto(
                self.orcamentos
            )
        )

        mock_criar_projeto.assert_called_once_with(
            orcamento
        )

        self.assertEqual(
            orcamento["status"],
            "Convertido em projeto",
        )

        mock_salvar.assert_called_once_with(
            self.orcamentos
        )

        mock_iniciar_homologacao.assert_called_once_with(
            projeto
        )
        
        self.assertEqual(
            resultado,
            projeto,
        )


if __name__ == "__main__":
    unittest.main()