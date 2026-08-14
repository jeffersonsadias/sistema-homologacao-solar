import unittest

from app.dominio.erros_dominio import (
    DadosObrigatoriosAusentes,
    RegistroDuplicado,
    ValorInvalido,
)

from app.dominio.tipos_servico import (
    CategoriaTipoServico,
    FluxoOperacionalServico,
    OrigemTipoServico,
    TipoServico,
    buscar_tipo_servico_por_codigo,
    buscar_tipos_servico_por_nome,
    codigo_tipo_servico_existe,
    converter_tipo_servico_para_dicionario,
    criar_catalogo_padrao,
    criar_tipo_servico,
    tipo_servico_esta_ativo,
    validar_duplicidade_tipo_servico,
)


class TestTiposServicoDominio(
    unittest.TestCase
):
    """
    Testes das regras estruturais
    dos Tipos de Serviço.
    """

    def test_criar_tipo_servico_padrao(
        self,
    ):
        """
        Deve criar um Tipo de Serviço
        pertencente ao catálogo da Plataforma.
        """

        servico = criar_tipo_servico(
            codigo=1,
            nome=(
                "Instalação de Sistema "
                "Fotovoltaico"
            ),
            categoria="INSTALACAO",
            origem="PADRAO_PLATAFORMA",
            fluxo_operacional=(
                "ORCAMENTO_FOTOVOLTAICO"
            ),
            descricao=(
                "Instalação completa de "
                "sistema fotovoltaico."
            ),
        )

        self.assertIsInstance(
            servico,
            TipoServico,
        )

        self.assertEqual(
            servico.codigo,
            1,
        )

        self.assertEqual(
            servico.nome,
            (
                "Instalação de Sistema "
                "Fotovoltaico"
            ),
        )

        self.assertEqual(
            servico.categoria,
            CategoriaTipoServico.INSTALACAO,
        )

        self.assertEqual(
            servico.origem,
            OrigemTipoServico.PADRAO_PLATAFORMA,
        )

        self.assertEqual(
            servico.fluxo_operacional,
            (
                FluxoOperacionalServico
                .ORCAMENTO_FOTOVOLTAICO
            ),
        )

        self.assertIsNone(
            servico.codigo_empresa_criadora
        )

        self.assertTrue(
            servico.ativo
        )

    def test_criar_tipo_servico_personalizado(
        self,
    ):
        """
        Serviço personalizado deve registrar
        a Empresa que o criou.
        """

        servico = criar_tipo_servico(
            codigo=2,
            nome=(
                "Inspeção aérea com drone"
            ),
            categoria="INSPECAO_E_DIAGNOSTICO",
            origem="PERSONALIZADO_EMPRESA",
            fluxo_operacional=(
                "ORDEM_SERVICO_POS_VENDA"
            ),
            codigo_empresa_criadora=50,
        )

        self.assertEqual(
            servico.codigo_empresa_criadora,
            50,
        )

        self.assertEqual(
            servico.origem,
            (
                OrigemTipoServico
                .PERSONALIZADO_EMPRESA
            ),
        )

    def test_servico_padrao_nao_pode_ter_empresa_criadora(
        self,
    ):
        """
        Serviço padrão pertence à Plataforma,
        não a uma Empresa específica.
        """

        with self.assertRaises(
            ValorInvalido
        ):
            criar_tipo_servico(
                codigo=1,
                nome="Limpeza de Módulos",
                categoria=(
                    "LIMPEZA_E_CONSERVACAO"
                ),
                origem="PADRAO_PLATAFORMA",
                fluxo_operacional=(
                    "ORDEM_SERVICO_POS_VENDA"
                ),
                codigo_empresa_criadora=50,
            )

    def test_servico_personalizado_exige_empresa(
        self,
    ):
        """
        Serviço personalizado precisa identificar
        a Empresa que o criou.
        """

        with self.assertRaises(
            DadosObrigatoriosAusentes
        ):
            criar_tipo_servico(
                codigo=1,
                nome="Serviço Especial",
                categoria="OUTROS",
                origem="PERSONALIZADO_EMPRESA",
                fluxo_operacional=(
                    "ORDEM_SERVICO_POS_VENDA"
                ),
            )

    def test_codigo_deve_ser_inteiro_positivo(
        self,
    ):
        """
        Código deve ser inteiro maior que zero.
        """

        codigos_invalidos = [
            0,
            -1,
            1.5,
            "1",
            True,
        ]

        for codigo in codigos_invalidos:
            with self.subTest(
                codigo=codigo
            ):
                with self.assertRaises(
                    ValorInvalido
                ):
                    criar_tipo_servico(
                        codigo=codigo,
                        nome="Limpeza",
                        categoria=(
                            "LIMPEZA_E_CONSERVACAO"
                        ),
                        origem=(
                            "PADRAO_PLATAFORMA"
                        ),
                        fluxo_operacional=(
                            "ORDEM_SERVICO_POS_VENDA"
                        ),
                    )

    def test_nome_e_obrigatorio(
        self,
    ):
        """
        Nome vazio deve ser rejeitado.
        """

        with self.assertRaises(
            DadosObrigatoriosAusentes
        ):
            criar_tipo_servico(
                codigo=1,
                nome="   ",
                categoria="OUTROS",
                origem="PADRAO_PLATAFORMA",
                fluxo_operacional=(
                    "ORDEM_SERVICO_POS_VENDA"
                ),
            )

    def test_nome_deve_ser_normalizado(
        self,
    ):
        """
        Espaços excedentes devem ser removidos.
        """

        servico = criar_tipo_servico(
            codigo=1,
            nome="  Limpeza   de   Módulos  ",
            categoria=(
                "LIMPEZA_E_CONSERVACAO"
            ),
            origem="PADRAO_PLATAFORMA",
            fluxo_operacional=(
                "ORDEM_SERVICO_POS_VENDA"
            ),
        )

        self.assertEqual(
            servico.nome,
            "Limpeza de Módulos",
        )

    def test_categoria_invalida_deve_ser_rejeitada(
        self,
    ):
        """
        Categoria precisa ser reconhecida.
        """

        with self.assertRaises(
            ValorInvalido
        ):
            criar_tipo_servico(
                codigo=1,
                nome="Serviço",
                categoria="CATEGORIA_INEXISTENTE",
                origem="PADRAO_PLATAFORMA",
                fluxo_operacional=(
                    "ORDEM_SERVICO_POS_VENDA"
                ),
            )

    def test_origem_invalida_deve_ser_rejeitada(
        self,
    ):
        """
        Origem precisa ser reconhecida.
        """

        with self.assertRaises(
            ValorInvalido
        ):
            criar_tipo_servico(
                codigo=1,
                nome="Serviço",
                categoria="OUTROS",
                origem="ORIGEM_INEXISTENTE",
                fluxo_operacional=(
                    "ORDEM_SERVICO_POS_VENDA"
                ),
            )

    def test_fluxo_operacional_invalido(
        self,
    ):
        """
        Fluxo operacional precisa ser reconhecido.
        """

        with self.assertRaises(
            ValorInvalido
        ):
            criar_tipo_servico(
                codigo=1,
                nome="Serviço",
                categoria="OUTROS",
                origem="PADRAO_PLATAFORMA",
                fluxo_operacional=(
                    "FLUXO_INEXISTENTE"
                ),
            )

    def test_descricao_vazia_deve_virar_none(
        self,
    ):
        """
        Descrição é opcional.
        """

        servico = criar_tipo_servico(
            codigo=1,
            nome="Limpeza",
            categoria=(
                "LIMPEZA_E_CONSERVACAO"
            ),
            origem="PADRAO_PLATAFORMA",
            fluxo_operacional=(
                "ORDEM_SERVICO_POS_VENDA"
            ),
            descricao="   ",
        )

        self.assertIsNone(
            servico.descricao
        )

    def test_inativar_tipo_servico(
        self,
    ):
        """
        Deve permitir inativar sem excluir.
        """

        servico = criar_tipo_servico(
            codigo=1,
            nome="Limpeza",
            categoria=(
                "LIMPEZA_E_CONSERVACAO"
            ),
            origem="PADRAO_PLATAFORMA",
            fluxo_operacional=(
                "ORDEM_SERVICO_POS_VENDA"
            ),
        )

        resultado = servico.inativar()

        self.assertIs(
            resultado,
            servico,
        )

        self.assertFalse(
            servico.ativo
        )

    def test_reativar_tipo_servico(
        self,
    ):
        """
        Deve permitir reativar um serviço.
        """

        servico = criar_tipo_servico(
            codigo=1,
            nome="Limpeza",
            categoria=(
                "LIMPEZA_E_CONSERVACAO"
            ),
            origem="PADRAO_PLATAFORMA",
            fluxo_operacional=(
                "ORDEM_SERVICO_POS_VENDA"
            ),
        )

        servico.inativar()
        servico.ativar()

        self.assertTrue(
            servico.ativo
        )

    def test_converter_para_dicionario(
        self,
    ):
        """
        Conversão deve produzir estrutura
        preparada para persistência.
        """

        servico = criar_tipo_servico(
            codigo=1,
            nome="Limpeza de Módulos",
            categoria=(
                "LIMPEZA_E_CONSERVACAO"
            ),
            origem="PADRAO_PLATAFORMA",
            fluxo_operacional=(
                "ORDEM_SERVICO_POS_VENDA"
            ),
        )

        dados = (
            converter_tipo_servico_para_dicionario(
                servico
            )
        )

        self.assertEqual(
            dados["categoria"],
            "LIMPEZA_E_CONSERVACAO",
        )

        self.assertEqual(
            dados["origem"],
            "PADRAO_PLATAFORMA",
        )

        self.assertEqual(
            dados["fluxo_operacional"],
            "ORDEM_SERVICO_POS_VENDA",
        )

        self.assertTrue(
            dados["ativo"]
        )

    def test_catalogo_padrao_deve_possuir_16_servicos(
        self,
    ):
        """
        O catálogo inicial deve possuir os
        16 Tipos de Serviço definidos.
        """

        catalogo = criar_catalogo_padrao()

        self.assertEqual(
            len(catalogo),
            16,
        )

    def test_catalogo_padrao_deve_ter_codigos_unicos(
        self,
    ):
        """
        Cada Tipo de Serviço padrão deve possuir
        um código exclusivo.
        """

        catalogo = criar_catalogo_padrao()

        codigos = [
            servico.codigo
            for servico in catalogo
        ]

        self.assertEqual(
            len(codigos),
            len(set(codigos)),
        )

    def test_catalogo_padrao_deve_ter_nomes_unicos(
        self,
    ):
        """
        O catálogo mestre não deve possuir
        Tipos de Serviço com nomes repetidos.
        """

        catalogo = criar_catalogo_padrao()

        nomes_normalizados = [
            servico.nome.casefold()
            for servico in catalogo
        ]

        self.assertEqual(
            len(nomes_normalizados),
            len(set(nomes_normalizados)),
        )

    def test_catalogo_padrao_deve_ter_origem_plataforma(
        self,
    ):
        """
        Todos os itens do catálogo mestre devem
        pertencer à Plataforma.
        """

        catalogo = criar_catalogo_padrao()

        for servico in catalogo:
            with self.subTest(
                codigo=servico.codigo
            ):
                self.assertEqual(
                    servico.origem,
                    (
                        OrigemTipoServico
                        .PADRAO_PLATAFORMA
                    ),
                )

                self.assertIsNone(
                    servico.codigo_empresa_criadora
                )

    def test_catalogo_padrao_deve_iniciar_ativo(
        self,
    ):
        """
        Todos os serviços padrão devem ser
        disponibilizados inicialmente como ativos.
        """

        catalogo = criar_catalogo_padrao()

        for servico in catalogo:
            with self.subTest(
                codigo=servico.codigo
            ):
                self.assertTrue(
                    servico.ativo
                )

    def test_instalacao_deve_usar_fluxo_fotovoltaico(
        self,
    ):
        """
        Instalação Fotovoltaica deve utilizar
        o fluxo especializado de orçamento.
        """

        catalogo = criar_catalogo_padrao()

        instalacao = next(
            servico
            for servico in catalogo
            if servico.codigo == 1
        )

        self.assertEqual(
            instalacao.nome,
            (
                "Instalação de Sistema "
                "Fotovoltaico"
            ),
        )

        self.assertEqual(
            instalacao.fluxo_operacional,
            (
                FluxoOperacionalServico
                .ORCAMENTO_FOTOVOLTAICO
            ),
        )

    def test_demais_servicos_devem_usar_fluxo_pos_venda(
        self,
    ):
        """
        Os serviços padrão diferentes da instalação
        devem inicialmente gerar Ordem de Serviço.
        """

        catalogo = criar_catalogo_padrao()

        servicos_pos_venda = [
            servico
            for servico in catalogo
            if servico.codigo != 1
        ]

        for servico in servicos_pos_venda:
            with self.subTest(
                codigo=servico.codigo
            ):
                self.assertEqual(
                    servico.fluxo_operacional,
                    (
                        FluxoOperacionalServico
                        .ORDEM_SERVICO_POS_VENDA
                    ),
                )

    def test_catalogo_padrao_deve_retornar_novas_entidades(
        self,
    ):
        """
        Chamadas diferentes não devem compartilhar
        as mesmas entidades mutáveis.
        """

        catalogo_1 = criar_catalogo_padrao()
        catalogo_2 = criar_catalogo_padrao()

        catalogo_1[0].inativar()

        self.assertFalse(
            catalogo_1[0].ativo
        )

        self.assertTrue(
            catalogo_2[0].ativo
        )

        self.assertIsNot(
            catalogo_1[0],
            catalogo_2[0],
        )

    def test_buscar_tipo_servico_por_codigo(
        self,
    ):
        """
        Deve retornar o Tipo de Serviço
        correspondente ao código informado.
        """

        catalogo = criar_catalogo_padrao()

        resultado = buscar_tipo_servico_por_codigo(
            catalogo,
            2,
        )

        self.assertIsNotNone(
            resultado
        )

        self.assertEqual(
            resultado.nome,
            "Limpeza de Módulos",
        )

    def test_buscar_tipo_servico_por_codigo_inexistente(
        self,
    ):
        """
        Código inexistente deve retornar None.
        """

        catalogo = criar_catalogo_padrao()

        resultado = buscar_tipo_servico_por_codigo(
            catalogo,
            999,
        )

        self.assertIsNone(
            resultado
        )

    def test_codigo_tipo_servico_existe(
        self,
    ):
        """
        Deve informar corretamente se o código existe.
        """

        catalogo = criar_catalogo_padrao()

        self.assertTrue(
            codigo_tipo_servico_existe(
                catalogo,
                1,
            )
        )

        self.assertFalse(
            codigo_tipo_servico_existe(
                catalogo,
                999,
            )
        )

    def test_buscar_tipos_servico_por_parte_do_nome(
        self,
    ):
        """
        Busca deve aceitar parte do nome.
        """

        catalogo = criar_catalogo_padrao()

        resultado = buscar_tipos_servico_por_nome(
            catalogo,
            "inversor",
        )

        nomes = [
            servico.nome
            for servico in resultado
        ]

        self.assertEqual(
            nomes,
            [
                "Manutenção de Inversor",
                "Substituição de Inversor",
            ],
        )

    def test_busca_por_nome_deve_ignorar_maiusculas_e_espacos(
        self,
    ):
        """
        Busca deve ignorar caixa e espaços externos.
        """

        catalogo = criar_catalogo_padrao()

        resultado = buscar_tipos_servico_por_nome(
            catalogo,
            "   LIMPEZA   ",
        )

        self.assertEqual(
            len(resultado),
            1,
        )

        self.assertEqual(
            resultado[0].nome,
            "Limpeza de Módulos",
        )

    def test_tipo_servico_esta_ativo(
        self,
    ):
        """
        Deve refletir a situação atual
        do Tipo de Serviço.
        """

        servico = criar_tipo_servico(
            codigo=50,
            nome="Serviço Teste",
            categoria="OUTROS",
            origem="PADRAO_PLATAFORMA",
            fluxo_operacional=(
                "ORDEM_SERVICO_POS_VENDA"
            ),
        )

        self.assertTrue(
            tipo_servico_esta_ativo(
                servico
            )
        )

        servico.inativar()

        self.assertFalse(
            tipo_servico_esta_ativo(
                servico
            )
        )

    def test_nao_permitir_nome_duplicado_no_catalogo_padrao(
        self,
    ):
        """
        Catálogo padrão não deve aceitar
        dois serviços com o mesmo nome.
        """

        catalogo = criar_catalogo_padrao()

        with self.assertRaises(
            RegistroDuplicado
        ):
            validar_duplicidade_tipo_servico(
                tipos_servico=catalogo,
                nome="  limpeza DE módulos  ",
                origem="PADRAO_PLATAFORMA",
            )

    def test_nao_permitir_servico_personalizado_duplicado_na_mesma_empresa(
        self,
    ):
        """
        Uma Empresa não pode criar duas vezes
        o mesmo Tipo de Serviço personalizado.
        """

        servico = criar_tipo_servico(
            codigo=100,
            nome="Inspeção com Drone",
            categoria=(
                "INSPECAO_E_DIAGNOSTICO"
            ),
            origem="PERSONALIZADO_EMPRESA",
            fluxo_operacional=(
                "ORDEM_SERVICO_POS_VENDA"
            ),
            codigo_empresa_criadora=50,
        )

        tipos_servico = [
            servico
        ]

        with self.assertRaises(
            RegistroDuplicado
        ):
            validar_duplicidade_tipo_servico(
                tipos_servico=tipos_servico,
                nome="inspeção com drone",
                origem="PERSONALIZADO_EMPRESA",
                codigo_empresa_criadora=50,
            )

    def test_empresas_diferentes_podem_usar_mesmo_nome_personalizado(
        self,
    ):
        """
        Empresas diferentes podem cadastrar
        serviços personalizados com o mesmo nome.
        """

        servico = criar_tipo_servico(
            codigo=100,
            nome="Inspeção com Drone",
            categoria=(
                "INSPECAO_E_DIAGNOSTICO"
            ),
            origem="PERSONALIZADO_EMPRESA",
            fluxo_operacional=(
                "ORDEM_SERVICO_POS_VENDA"
            ),
            codigo_empresa_criadora=50,
        )

        tipos_servico = [
            servico
        ]

        resultado = validar_duplicidade_tipo_servico(
            tipos_servico=tipos_servico,
            nome="Inspeção com Drone",
            origem="PERSONALIZADO_EMPRESA",
            codigo_empresa_criadora=60,
        )

        self.assertIsNone(
            resultado
        )



if __name__ == "__main__":
    unittest.main()