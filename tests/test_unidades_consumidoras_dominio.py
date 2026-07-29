import unittest

from app.dominio.unidades_consumidoras import (
    EnderecoUnidade,
    SituacaoUnidadeConsumidora,
    TipoLigacao,
    TipoTitular,
    TitularConta,
    UnidadeConsumidora,
    buscar_unidade_por_codigo,
    buscar_unidade_por_numero_uc,
    codigo_unidade_existe,
    criar_unidade_consumidora,
    numero_uc_existe,
)


class TestTitularConta(unittest.TestCase):
    """
    Testes da entidade TitularConta.
    """

    def test_criar_titular_pessoa_fisica(self):
        """
        Deve criar um titular pessoa física
        com CPF normalizado.
        """

        titular = TitularConta(
            nome="João da Silva",
            documento="123.456.789-00",
            tipo=TipoTitular.PESSOA_FISICA,
        )

        self.assertEqual(
            titular.nome,
            "João da Silva",
        )

        self.assertEqual(
            titular.documento,
            "12345678900",
        )

        self.assertEqual(
            titular.tipo,
            TipoTitular.PESSOA_FISICA,
        )

    def test_criar_titular_pessoa_juridica(self):
        """
        Deve criar um titular pessoa jurídica
        com CNPJ normalizado.
        """

        titular = TitularConta(
            nome="Empresa Solar Ltda",
            documento="12.345.678/0001-90",
            tipo=TipoTitular.PESSOA_JURIDICA,
        )

        self.assertEqual(
            titular.documento,
            "12345678000190",
        )

        self.assertEqual(
            titular.tipo,
            TipoTitular.PESSOA_JURIDICA,
        )

    def test_rejeitar_cpf_com_quantidade_invalida(self):
        """
        Deve rejeitar um CPF que não possua
        exatamente 11 dígitos.
        """

        with self.assertRaises(ValueError):
            TitularConta(
                nome="João da Silva",
                documento="123456789",
                tipo=TipoTitular.PESSOA_FISICA,
            )

    def test_rejeitar_cnpj_com_quantidade_invalida(self):
        """
        Deve rejeitar um CNPJ que não possua
        exatamente 14 dígitos.
        """

        with self.assertRaises(ValueError):
            TitularConta(
                nome="Empresa Solar Ltda",
                documento="123456780001",
                tipo=TipoTitular.PESSOA_JURIDICA,
            )

    def test_rejeitar_tipo_titular_invalido(self):
        """
        Deve rejeitar um tipo de titular
        que não pertença ao enum TipoTitular.
        """

        with self.assertRaises(TypeError):
            TitularConta(
                nome="João da Silva",
                documento="12345678900",
                tipo="PESSOA_FISICA",
            )


class TestEnderecoUnidade(unittest.TestCase):
    """
    Testes da entidade EnderecoUnidade.
    """

    def test_criar_endereco_valido(self):
        """
        Deve criar um endereço válido
        e normalizar estado e CEP.
        """

        endereco = EnderecoUnidade(
            logradouro="Rua das Flores",
            numero="100",
            bairro="Centro",
            cidade="Caetité",
            estado="ba",
            cep="46.400-000",
            complemento="Casa",
        )

        self.assertEqual(
            endereco.estado,
            "BA",
        )

        self.assertEqual(
            endereco.cep,
            "46400000",
        )

        self.assertEqual(
            endereco.complemento,
            "Casa",
        )

    def test_rejeitar_estado_invalido(self):
        """
        Deve rejeitar estado que não possua
        exatamente dois caracteres.
        """

        with self.assertRaises(ValueError):
            EnderecoUnidade(
                logradouro="Rua das Flores",
                numero="100",
                bairro="Centro",
                cidade="Caetité",
                estado="Bahia",
                cep="46400000",
            )

    def test_rejeitar_cep_invalido(self):
        """
        Deve rejeitar CEP que não possua
        exatamente oito dígitos.
        """

        with self.assertRaises(ValueError):
            EnderecoUnidade(
                logradouro="Rua das Flores",
                numero="100",
                bairro="Centro",
                cidade="Caetité",
                estado="BA",
                cep="46400",
            )


class TestUnidadeConsumidora(unittest.TestCase):
    """
    Testes da entidade UnidadeConsumidora
    e das funções auxiliares do domínio.
    """

    def setUp(self):
        """
        Cria objetos reutilizados
        em vários testes.
        """

        self.titular = TitularConta(
            nome="João da Silva",
            documento="123.456.789-00",
            tipo=TipoTitular.PESSOA_FISICA,
        )

        self.endereco = EnderecoUnidade(
            logradouro="Rua das Flores",
            numero="100",
            bairro="Centro",
            cidade="Caetité",
            estado="BA",
            cep="46400000",
            complemento="Casa",
        )

        self.unidade = criar_unidade_consumidora(
            codigo=1,
            numero_uc="703456789",
            codigo_cliente="900123",
            codigo_concessionaria=1,
            titular=self.titular,
            endereco=self.endereco,
            tipo_ligacao=TipoLigacao.TRIFASICA,
            carga_instalada_kw=10.5,
        )

        self.lista_unidades = [
            self.unidade,
        ]

    def test_criar_unidade_consumidora(self):
        """
        Deve criar uma Unidade Consumidora
        com os dados informados.
        """

        self.assertIsInstance(
            self.unidade,
            UnidadeConsumidora,
        )

        self.assertEqual(
            self.unidade.codigo,
            1,
        )

        self.assertEqual(
            self.unidade.numero_uc,
            "703456789",
        )

        self.assertEqual(
            self.unidade.codigo_cliente,
            "900123",
        )

        self.assertEqual(
            self.unidade.codigo_concessionaria,
            1,
        )

        self.assertEqual(
            self.unidade.tipo_ligacao,
            TipoLigacao.TRIFASICA,
        )

        self.assertEqual(
            self.unidade.carga_instalada_kw,
            10.5,
        )

        self.assertEqual(
            self.unidade.situacao,
            SituacaoUnidadeConsumidora.ATIVA,
        )

        self.assertEqual(
            self.unidade.historico_alteracoes,
            [],
        )

    def test_buscar_unidade_por_codigo(self):
        """
        Deve localizar uma Unidade Consumidora
        pelo código interno.
        """

        resultado = buscar_unidade_por_codigo(
            self.lista_unidades,
            1,
        )

        self.assertIs(
            resultado,
            self.unidade,
        )

    def test_buscar_unidade_por_codigo_inexistente(self):
        """
        Deve retornar None quando o código
        não estiver cadastrado.
        """

        resultado = buscar_unidade_por_codigo(
            self.lista_unidades,
            99,
        )

        self.assertIsNone(resultado)

    def test_buscar_unidade_por_numero_uc(self):
        """
        Deve localizar uma Unidade Consumidora
        pelo número da UC.
        """

        resultado = buscar_unidade_por_numero_uc(
            self.lista_unidades,
            "703456789",
        )

        self.assertIs(
            resultado,
            self.unidade,
        )

    def test_codigo_unidade_existe(self):
        """
        Deve informar se um código interno
        já está cadastrado.
        """

        self.assertTrue(
            codigo_unidade_existe(
                self.lista_unidades,
                1,
            )
        )

        self.assertFalse(
            codigo_unidade_existe(
                self.lista_unidades,
                99,
            )
        )

    def test_numero_uc_existe(self):
        """
        Deve informar se o número da UC
        já está cadastrado.
        """

        self.assertTrue(
            numero_uc_existe(
                self.lista_unidades,
                "703456789",
            )
        )

        self.assertFalse(
            numero_uc_existe(
                self.lista_unidades,
                "999999999",
            )
        )

    def test_numero_uc_existe_na_mesma_concessionaria(self):
        """
        Deve considerar a combinação entre
        número da UC e Concessionária.
        """

        self.assertTrue(
            numero_uc_existe(
                self.lista_unidades,
                "703456789",
                codigo_concessionaria=1,
            )
        )

        self.assertFalse(
            numero_uc_existe(
                self.lista_unidades,
                "703456789",
                codigo_concessionaria=2,
            )
        )

    def test_alterar_carga_instalada(self):
        """
        Deve alterar a carga instalada
        e registrar a mudança no histórico.
        """

        resultado = (
            self.unidade
            .alterar_carga_instalada(
                15.0,
                motivo="Ampliação de carga.",
            )
        )

        self.assertTrue(resultado)

        self.assertEqual(
            self.unidade.carga_instalada_kw,
            15.0,
        )

        self.assertEqual(
            len(
                self.unidade
                .historico_alteracoes
            ),
            1,
        )

        registro = (
            self.unidade
            .historico_alteracoes[0]
        )

        self.assertEqual(
            registro.valor_anterior,
            "10.5",
        )

        self.assertEqual(
            registro.valor_novo,
            "15.0",
        )

        self.assertEqual(
            registro.motivo,
            "Ampliação de carga.",
        )

    def test_nao_registrar_alteracao_quando_carga_nao_mudar(
        self,
    ):
        """
        Não deve registrar alteração quando
        o novo valor for igual ao atual.
        """

        resultado = (
            self.unidade
            .alterar_carga_instalada(
                10.5
            )
        )

        self.assertFalse(resultado)

        self.assertEqual(
            len(
                self.unidade
                .historico_alteracoes
            ),
            0,
        )

    def test_alterar_titular(self):
        """
        Deve alterar o titular e registrar
        a mudança no histórico.
        """

        novo_titular = TitularConta(
            nome="Maria da Silva",
            documento="987.654.321-00",
            tipo=TipoTitular.PESSOA_FISICA,
        )

        resultado = (
            self.unidade
            .alterar_titular(
                novo_titular,
                motivo="Alteração de titularidade.",
            )
        )

        self.assertTrue(resultado)

        self.assertIs(
            self.unidade.titular,
            novo_titular,
        )

        self.assertEqual(
            len(
                self.unidade
                .historico_alteracoes
            ),
            1,
        )

    def test_alterar_codigo_cliente(self):
        """
        Deve alterar o código do cliente
        e registrar a mudança.
        """

        resultado = (
            self.unidade
            .alterar_codigo_cliente(
                "900999",
                motivo="Atualização cadastral.",
            )
        )

        self.assertTrue(resultado)

        self.assertEqual(
            self.unidade.codigo_cliente,
            "900999",
        )

        self.assertEqual(
            len(
                self.unidade
                .historico_alteracoes
            ),
            1,
        )

    def test_alterar_tipo_ligacao(self):
        """
        Deve alterar o tipo de ligação elétrica
        e registrar a mudança.
        """

        resultado = (
            self.unidade
            .alterar_tipo_ligacao(
                TipoLigacao.BIFASICA,
                motivo="Adequação elétrica.",
            )
        )

        self.assertTrue(resultado)

        self.assertEqual(
            self.unidade.tipo_ligacao,
            TipoLigacao.BIFASICA,
        )

        self.assertEqual(
            len(
                self.unidade
                .historico_alteracoes
            ),
            1,
        )

    def test_inativar_unidade(self):
        """
        Deve inativar a Unidade Consumidora
        e registrar a alteração.
        """

        resultado = self.unidade.inativar(
            motivo="Conta encerrada.",
        )

        self.assertTrue(resultado)

        self.assertEqual(
            self.unidade.situacao,
            SituacaoUnidadeConsumidora.INATIVA,
        )

        self.assertEqual(
            len(
                self.unidade
                .historico_alteracoes
            ),
            1,
        )

    def test_ativar_unidade_inativa(self):
        """
        Deve reativar uma Unidade Consumidora
        previamente inativada.
        """

        self.unidade.inativar()

        resultado = self.unidade.ativar(
            motivo="Conta reativada.",
        )

        self.assertTrue(resultado)

        self.assertEqual(
            self.unidade.situacao,
            SituacaoUnidadeConsumidora.ATIVA,
        )

        self.assertEqual(
            len(
                self.unidade
                .historico_alteracoes
            ),
            2,
        )

    def test_rejeitar_carga_negativa(self):
        """
        Deve rejeitar uma carga instalada negativa.
        """

        with self.assertRaises(ValueError):
            criar_unidade_consumidora(
                codigo=2,
                numero_uc="123456789",
                codigo_cliente="123",
                codigo_concessionaria=1,
                titular=self.titular,
                endereco=self.endereco,
                tipo_ligacao=(
                    TipoLigacao.MONOFASICA
                ),
                carga_instalada_kw=-1,
            )

    def test_rejeitar_codigo_interno_invalido(self):
        """
        Deve rejeitar código interno igual
        ou inferior a zero.
        """

        with self.assertRaises(ValueError):
            criar_unidade_consumidora(
                codigo=0,
                numero_uc="123456789",
                codigo_cliente="123",
                codigo_concessionaria=1,
                titular=self.titular,
                endereco=self.endereco,
                tipo_ligacao=(
                    TipoLigacao.MONOFASICA
                ),
            )

    def test_rejeitar_titular_invalido(self):
        """
        Deve rejeitar titular que não seja
        um objeto TitularConta.
        """

        with self.assertRaises(TypeError):
            criar_unidade_consumidora(
                codigo=2,
                numero_uc="123456789",
                codigo_cliente="123",
                codigo_concessionaria=1,
                titular="João da Silva",
                endereco=self.endereco,
                tipo_ligacao=(
                    TipoLigacao.MONOFASICA
                ),
            )

    def test_rejeitar_endereco_invalido(self):
        """
        Deve rejeitar endereço que não seja
        um objeto EnderecoUnidade.
        """

        with self.assertRaises(TypeError):
            criar_unidade_consumidora(
                codigo=2,
                numero_uc="123456789",
                codigo_cliente="123",
                codigo_concessionaria=1,
                titular=self.titular,
                endereco="Rua das Flores",
                tipo_ligacao=(
                    TipoLigacao.MONOFASICA
                ),
            )


if __name__ == "__main__":
    unittest.main()