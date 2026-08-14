import unittest

from app.dominio.areas_atendimento import (
    AreaAtendimento,
    criar_area_atendimento,
)

from app.dominio.empresas import (
    criar_dados_empresa,
    inativar_empresa,
)

from app.dominio.erros_dominio import (
    DadosObrigatoriosAusentes,
    RegistroDuplicado,
    ValorInvalido,
)

from app.dominio.servicos_empresa import (
    ServicoOfertadoEmpresa,
    buscar_servico_ofertado_por_codigo,
    converter_servico_ofertado_para_dicionario,
    criar_servico_ofertado_empresa,
    listar_servicos_ofertados_ativos,
    listar_servicos_ofertados_por_empresa,
    listar_servicos_ofertados_por_tipo_servico,
    reativar_servico_ofertado_empresa,
    servico_elegivel_marketplace,
    servico_ofertado_duplicado,
    validar_nova_oferta_servico,
)

from app.dominio.tipos_servico import (
    criar_tipo_servico,
)


class TestServicosEmpresaDominio(
    unittest.TestCase
):
    """
    Testes das regras básicas dos
    Serviços oferecidos pelas Empresas.
    """

    def setUp(self):
        """
        Cria Empresa e Tipos de Serviço
        reutilizados pelos testes.
        """

        self.empresa = criar_dados_empresa(
            codigo=1,
            razao_social=(
                "Solar Energia Bahia Ltda"
            ),
            nome_fantasia="Solar Bahia",
            cnpj="11.222.333/0001-81",
            email=(
                "contato@solarbahia.com.br"
            ),
            telefone="(77) 99999-9999",
        )

        self.tipo_padrao = criar_tipo_servico(
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
        )

        self.tipo_personalizado = (
            criar_tipo_servico(
                codigo=100,
                nome=(
                    "Inspeção Premium com Drone"
                ),
                categoria=(
                    "INSPECAO_E_DIAGNOSTICO"
                ),
                origem=(
                    "PERSONALIZADO_EMPRESA"
                ),
                fluxo_operacional=(
                    "ORDEM_SERVICO_POS_VENDA"
                ),
                codigo_empresa_criadora=1,
            )
        )

    def test_criar_servico_ofertado_empresa(
        self,
    ):
        """
        Deve criar corretamente o vínculo
        Empresa x Tipo de Serviço.
        """

        servico = (
            criar_servico_ofertado_empresa(
                codigo=1,
                empresa=self.empresa,
                tipo_servico=self.tipo_padrao,
                modelo_precificacao="ORCAMENTO",
            )
        )

        self.assertIsInstance(
            servico,
            ServicoOfertadoEmpresa,
        )

        self.assertEqual(
            servico.codigo,
            1,
        )

        self.assertEqual(
            servico.codigo_empresa,
            1,
        )

        self.assertEqual(
            servico.codigo_tipo_servico,
            1,
        )

        self.assertEqual(
            servico.modelo_precificacao.value,
            "ORCAMENTO",
        )

        self.assertIsNone(
            servico.valor
        )

        self.assertTrue(
            servico.aceita_solicitacao_direta
        )

        self.assertTrue(
            servico.participa_marketplace
        )

        self.assertTrue(
            servico.ativo
        )

    def test_codigo_da_oferta_deve_ser_positivo(
        self,
    ):
        """
        Código da oferta deve ser inteiro
        maior que zero.
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
                    criar_servico_ofertado_empresa(
                        codigo=codigo,
                        empresa=self.empresa,
                        tipo_servico=(
                            self.tipo_padrao
                        ),
                        modelo_precificacao="ORCAMENTO",
                    )

    def test_empresa_deve_ser_dicionario(
        self,
    ):
        """
        Empresa inválida deve ser rejeitada.
        """

        with self.assertRaises(
            TypeError
        ):
            criar_servico_ofertado_empresa(
                codigo=1,
                empresa="Empresa inválida",
                tipo_servico=self.tipo_padrao,
                modelo_precificacao="ORCAMENTO",
            )

    def test_empresa_inativa_nao_pode_criar_oferta(
        self,
    ):
        """
        Empresa inativa não pode disponibilizar
        um novo serviço.
        """

        inativar_empresa(
            self.empresa
        )

        with self.assertRaises(
            ValorInvalido
        ):
            criar_servico_ofertado_empresa(
                codigo=1,
                empresa=self.empresa,
                tipo_servico=self.tipo_padrao,
                modelo_precificacao="ORCAMENTO",
            )

    def test_tipo_servico_deve_ser_instancia_valida(
        self,
    ):
        """
        Tipo de Serviço inválido deve ser rejeitado.
        """

        with self.assertRaises(
            TypeError
        ):
            criar_servico_ofertado_empresa(
                codigo=1,
                empresa=self.empresa,
                tipo_servico={
                    "codigo": 1
                },
                modelo_precificacao="ORCAMENTO",
            )

    def test_tipo_servico_inativo_nao_pode_ser_ofertado(
        self,
    ):
        """
        Tipo de Serviço inativo não pode gerar
        nova oferta para Empresa.
        """

        self.tipo_padrao.inativar()

        with self.assertRaises(
            ValorInvalido
        ):
            criar_servico_ofertado_empresa(
                codigo=1,
                empresa=self.empresa,
                tipo_servico=self.tipo_padrao,
                modelo_precificacao="ORCAMENTO",
            )

    def test_empresa_criadora_pode_ofertar_servico_personalizado(
        self,
    ):
        """
        A Empresa que criou um Tipo de Serviço
        personalizado pode oferecê-lo.
        """

        servico = (
            criar_servico_ofertado_empresa(
                codigo=1,
                empresa=self.empresa,
                tipo_servico=(
                    self.tipo_personalizado
                ),
                modelo_precificacao="SOB_CONSULTA",
            )
        )

        self.assertEqual(
            servico.codigo_empresa,
            1,
        )

        self.assertEqual(
            servico.codigo_tipo_servico,
            100,
        )

        self.assertEqual(
            servico.modelo_precificacao.value,
            "SOB_CONSULTA",
        )

        self.assertIsNone(
            servico.valor
        )

    def test_outra_empresa_nao_pode_ofertar_servico_personalizado(
        self,
    ):
        """
        Serviço personalizado não pode ser
        utilizado por outra Empresa.
        """

        outra_empresa = criar_dados_empresa(
            codigo=2,
            razao_social=(
                "Energia do Sertão Ltda"
            ),
            nome_fantasia=(
                "Energia Sertão"
            ),
            cnpj="45.723.174/0001-10",
            email=(
                "contato@energiasertao.com.br"
            ),
            telefone="(77) 98888-7777",
        )

        with self.assertRaises(
            ValorInvalido
        ):
            criar_servico_ofertado_empresa(
                codigo=1,
                empresa=outra_empresa,
                tipo_servico=(
                    self.tipo_personalizado
                ),
                modelo_precificacao="SOB_CONSULTA",
            )

    def test_inativar_servico_ofertado(
        self,
    ):
        """
        A oferta pode ser inativada
        preservando a entidade.
        """

        servico = (
            criar_servico_ofertado_empresa(
                codigo=1,
                empresa=self.empresa,
                tipo_servico=self.tipo_padrao,
                modelo_precificacao="ORCAMENTO",
            )
        )

        resultado = servico.inativar()

        self.assertIs(
            resultado,
            servico,
        )

        self.assertFalse(
            servico.ativo
        )

    def test_reativar_servico_ofertado(
        self,
    ):
        """
        A oferta pode ser reativada.
        """

        servico = (
            criar_servico_ofertado_empresa(
                codigo=1,
                empresa=self.empresa,
                tipo_servico=self.tipo_padrao,
                modelo_precificacao="ORCAMENTO",
            )
        )

        servico.inativar()

        resultado = (
            reativar_servico_ofertado_empresa(
                servico_ofertado=servico,
                empresa=self.empresa,
                tipo_servico=self.tipo_padrao,
            )
        )

        self.assertIs(
            resultado,
            servico,
        )

        self.assertTrue(
            servico.ativo
        )

    def test_nao_deve_reativar_oferta_com_empresa_inativa(
        self,
    ):
        """
        Oferta não pode ser reativada quando
        a Empresa vinculada estiver inativa.
        """

        servico = (
            criar_servico_ofertado_empresa(
                codigo=1,
                empresa=self.empresa,
                tipo_servico=self.tipo_padrao,
                modelo_precificacao="ORCAMENTO",
            )
        )

        servico.inativar()

        inativar_empresa(
            self.empresa
        )

        with self.assertRaises(
            ValorInvalido
        ):
            reativar_servico_ofertado_empresa(
                servico_ofertado=servico,
                empresa=self.empresa,
                tipo_servico=self.tipo_padrao,
            )

        self.assertFalse(
            servico.ativo
        )

    def test_nao_deve_reativar_oferta_com_tipo_servico_inativo(
        self,
    ):
        """
        Oferta não pode ser reativada quando
        o Tipo de Serviço estiver inativo.
        """

        servico = (
            criar_servico_ofertado_empresa(
                codigo=1,
                empresa=self.empresa,
                tipo_servico=self.tipo_padrao,
                modelo_precificacao="ORCAMENTO",
            )
        )

        servico.inativar()

        self.tipo_padrao.inativar()

        with self.assertRaises(
            ValorInvalido
        ):
            reativar_servico_ofertado_empresa(
                servico_ofertado=servico,
                empresa=self.empresa,
                tipo_servico=self.tipo_padrao,
            )

        self.assertFalse(
            servico.ativo
        )

    def test_nao_deve_reativar_oferta_com_outra_empresa(
        self,
    ):
        """
        Empresa ativa diferente da vinculada
        não pode reativar a oferta.
        """

        servico = (
            criar_servico_ofertado_empresa(
                codigo=1,
                empresa=self.empresa,
                tipo_servico=self.tipo_padrao,
                modelo_precificacao="ORCAMENTO",
            )
        )

        servico.inativar()

        outra_empresa = criar_dados_empresa(
            codigo=2,
            razao_social=(
                "Energia Solar Sertão Ltda"
            ),
            nome_fantasia="Solar Sertão",
            cnpj="45.723.174/0001-10",
            email=(
                "contato@solarsertao.com.br"
            ),
            telefone="(77) 98888-7777",
        )

        with self.assertRaises(
            ValorInvalido
        ):
            reativar_servico_ofertado_empresa(
                servico_ofertado=servico,
                empresa=outra_empresa,
                tipo_servico=self.tipo_padrao,
            )

        self.assertFalse(
            servico.ativo
        )

    def test_nao_deve_reativar_oferta_com_outro_tipo_servico(
        self,
    ):
        """
        Tipo de Serviço diferente do vínculo
        não pode ser usado para reativar a oferta.
        """

        servico = (
            criar_servico_ofertado_empresa(
                codigo=1,
                empresa=self.empresa,
                tipo_servico=self.tipo_padrao,
                modelo_precificacao="ORCAMENTO",
            )
        )

        servico.inativar()

        outro_tipo = criar_tipo_servico(
            codigo=2,
            nome="Limpeza de Módulos",
            categoria=(
                "LIMPEZA_E_CONSERVACAO"
            ),
            origem="PADRAO_PLATAFORMA",
            fluxo_operacional=(
                "ORDEM_SERVICO_POS_VENDA"
            ),
        )

        with self.assertRaises(
            ValorInvalido
        ):
            reativar_servico_ofertado_empresa(
                servico_ofertado=servico,
                empresa=self.empresa,
                tipo_servico=outro_tipo,
            )

        self.assertFalse(
            servico.ativo
        )

    def test_reativacao_exige_servico_ofertado_valido(
        self,
    ):
        """
        Reativação deve receber uma entidade
        ServicoOfertadoEmpresa válida.
        """

        with self.assertRaises(
            TypeError
        ):
            reativar_servico_ofertado_empresa(
                servico_ofertado={
                    "codigo": 1,
                },
                empresa=self.empresa,
                tipo_servico=self.tipo_padrao,
            )

    def test_converter_servico_ofertado_para_dicionario(
        self,
    ):
        """
        Conversão deve preservar os códigos
        e a situação atual.
        """

        servico = (
            criar_servico_ofertado_empresa(
                codigo=1,
                empresa=self.empresa,
                tipo_servico=self.tipo_padrao,
                modelo_precificacao="ORCAMENTO",
            )
        )

        dados = (
            converter_servico_ofertado_para_dicionario(
                servico
            )
        )

        self.assertEqual(
            dados,
            {
                "codigo": 1,
                "codigo_empresa": 1,
                "codigo_tipo_servico": 1,
                "modelo_precificacao": "ORCAMENTO",
                "valor": None,
                "aceita_solicitacao_direta": True,
                "participa_marketplace": True,
                "area_atendimento": None,
                "ativo": True,
            },
        )

    def test_preco_fixo_exige_valor(
        self,
    ):
        """
        PRECO_FIXO deve exigir valor.
        """

        tipo_servico = criar_tipo_servico(
            codigo=2,
            nome="Limpeza de Módulos",
            categoria=(
                "LIMPEZA_E_CONSERVACAO"
            ),
            origem="PADRAO_PLATAFORMA",
            fluxo_operacional=(
                "ORDEM_SERVICO_POS_VENDA"
            ),
        )

        with self.assertRaises(
            DadosObrigatoriosAusentes
        ):
            criar_servico_ofertado_empresa(
                codigo=2,
                empresa=self.empresa,
                tipo_servico=tipo_servico,
                modelo_precificacao="PRECO_FIXO",
            )

    def test_preco_fixo_deve_aceitar_valor_positivo(
        self,
    ):
        """
        PRECO_FIXO deve armazenar valor positivo.
        """

        tipo_servico = criar_tipo_servico(
            codigo=2,
            nome="Limpeza de Módulos",
            categoria=(
                "LIMPEZA_E_CONSERVACAO"
            ),
            origem="PADRAO_PLATAFORMA",
            fluxo_operacional=(
                "ORDEM_SERVICO_POS_VENDA"
            ),
        )

        servico = (
            criar_servico_ofertado_empresa(
                codigo=2,
                empresa=self.empresa,
                tipo_servico=tipo_servico,
                modelo_precificacao="PRECO_FIXO",
                valor=350,
            )
        )

        self.assertEqual(
            servico.valor,
            350.0,
        )

    def test_a_partir_de_exige_valor(
        self,
    ):
        """
        A_PARTIR_DE deve exigir valor.
        """

        tipo_servico = criar_tipo_servico(
            codigo=2,
            nome="Limpeza de Módulos",
            categoria=(
                "LIMPEZA_E_CONSERVACAO"
            ),
            origem="PADRAO_PLATAFORMA",
            fluxo_operacional=(
                "ORDEM_SERVICO_POS_VENDA"
            ),
        )

        with self.assertRaises(
            DadosObrigatoriosAusentes
        ):
            criar_servico_ofertado_empresa(
                codigo=2,
                empresa=self.empresa,
                tipo_servico=tipo_servico,
                modelo_precificacao="A_PARTIR_DE",
            )

    def test_orcamento_nao_deve_possuir_valor(
        self,
    ):
        """
        ORCAMENTO não deve receber valor.
        """

        with self.assertRaises(
            ValorInvalido
        ):
            criar_servico_ofertado_empresa(
                codigo=1,
                empresa=self.empresa,
                tipo_servico=self.tipo_padrao,
                modelo_precificacao="ORCAMENTO",
                valor=10000,
            )

    def test_sob_consulta_nao_deve_possuir_valor(
        self,
    ):
        """
        SOB_CONSULTA não deve receber valor.
        """

        with self.assertRaises(
            ValorInvalido
        ):
            criar_servico_ofertado_empresa(
                codigo=2,
                empresa=self.empresa,
                tipo_servico=(
                    self.tipo_personalizado
                ),
                modelo_precificacao="SOB_CONSULTA",
                valor=500,
            )

    def test_valor_deve_ser_maior_que_zero(
        self,
    ):
        """
        Valores zero ou negativos devem
        ser rejeitados.
        """

        tipo_servico = criar_tipo_servico(
            codigo=2,
            nome="Limpeza de Módulos",
            categoria=(
                "LIMPEZA_E_CONSERVACAO"
            ),
            origem="PADRAO_PLATAFORMA",
            fluxo_operacional=(
                "ORDEM_SERVICO_POS_VENDA"
            ),
        )

        for valor in (
            0,
            -1,
        ):
            with self.subTest(
                valor=valor
            ):
                with self.assertRaises(
                    ValorInvalido
                ):
                    criar_servico_ofertado_empresa(
                        codigo=2,
                        empresa=self.empresa,
                        tipo_servico=tipo_servico,
                        modelo_precificacao=(
                            "PRECO_FIXO"
                        ),
                        valor=valor,
                    )

    def test_modelo_precificacao_invalido(
        self,
    ):
        """
        Modelo desconhecido deve ser rejeitado.
        """

        with self.assertRaises(
            ValorInvalido
        ):
            criar_servico_ofertado_empresa(
                codigo=1,
                empresa=self.empresa,
                tipo_servico=self.tipo_padrao,
                modelo_precificacao=(
                    "MODELO_INEXISTENTE"
                ),
            )

    def test_instalacao_fotovoltaica_deve_usar_orcamento(
        self,
    ):
        """
        Instalação Fotovoltaica deve utilizar
        obrigatoriamente ORCAMENTO.
        """

        with self.assertRaises(
            ValorInvalido
        ):
            criar_servico_ofertado_empresa(
                codigo=1,
                empresa=self.empresa,
                tipo_servico=self.tipo_padrao,
                modelo_precificacao="PRECO_FIXO",
                valor=20000,
            )

    def test_pode_desativar_solicitacao_direta(
        self,
    ):
        """
        Deve permitir que a Empresa ofereça o serviço
        sem aceitar solicitações diretas.
        """

        servico = criar_servico_ofertado_empresa(
            codigo=1,
            empresa=self.empresa,
            tipo_servico=self.tipo_padrao,
            modelo_precificacao="ORCAMENTO",
            aceita_solicitacao_direta=False,
        )

        self.assertFalse(
            servico.aceita_solicitacao_direta
        )

        self.assertTrue(
            servico.participa_marketplace
        )

        self.assertTrue(
            servico.ativo
        )

    def test_pode_desativar_participacao_marketplace(
        self,
    ):
        """
        Deve permitir que a Empresa ofereça o serviço
        sem participar do marketplace aberto.
        """

        servico = criar_servico_ofertado_empresa(
            codigo=1,
            empresa=self.empresa,
            tipo_servico=self.tipo_padrao,
            modelo_precificacao="ORCAMENTO",
            participa_marketplace=False,
        )

        self.assertTrue(
            servico.aceita_solicitacao_direta
        )

        self.assertFalse(
            servico.participa_marketplace
        )

        self.assertTrue(
            servico.ativo
        )

    def test_pode_desativar_ambos_canais_comerciais(
        self,
    ):
        """
        A oferta pode permanecer cadastrada e ativa
        mesmo sem aceitar solicitações diretas
        e sem participar do marketplace.
        """

        servico = criar_servico_ofertado_empresa(
            codigo=1,
            empresa=self.empresa,
            tipo_servico=self.tipo_padrao,
            modelo_precificacao="ORCAMENTO",
            aceita_solicitacao_direta=False,
            participa_marketplace=False,
        )

        self.assertFalse(
            servico.aceita_solicitacao_direta
        )

        self.assertFalse(
            servico.participa_marketplace
        )

        self.assertTrue(
            servico.ativo
        )

    def test_aceita_solicitacao_direta_deve_ser_booleano(
        self,
    ):
        """
        A configuração de solicitação direta
        deve aceitar somente bool.
        """

        valores_invalidos = [
            1,
            0,
            "True",
            "False",
            None,
        ]

        for valor in valores_invalidos:
            with self.subTest(
                valor=valor
            ):
                with self.assertRaises(
                    ValorInvalido
                ):
                    criar_servico_ofertado_empresa(
                        codigo=1,
                        empresa=self.empresa,
                        tipo_servico=self.tipo_padrao,
                        modelo_precificacao="ORCAMENTO",
                        aceita_solicitacao_direta=valor,
                    )

    def test_participa_marketplace_deve_ser_booleano(
        self,
    ):
        """
        A configuração de marketplace
        deve aceitar somente bool.
        """

        valores_invalidos = [
            1,
            0,
            "True",
            "False",
            None,
        ]

        for valor in valores_invalidos:
            with self.subTest(
                valor=valor
            ):
                with self.assertRaises(
                    ValorInvalido
                ):
                    criar_servico_ofertado_empresa(
                        codigo=1,
                        empresa=self.empresa,
                        tipo_servico=self.tipo_padrao,
                        modelo_precificacao="ORCAMENTO",
                        participa_marketplace=valor,
                    )

    def test_servico_pode_receber_area_atendimento(
        self,
    ):
        """
        Oferta pode receber uma Área de Atendimento
        válida criada pelo domínio geográfico.
        """

        area = criar_area_atendimento(
            modalidade="RAIO",
            municipio_base="Caetité",
            uf_base="BA",
            raio_km=150,
        )

        servico = criar_servico_ofertado_empresa(
            codigo=1,
            empresa=self.empresa,
            tipo_servico=self.tipo_padrao,
            modelo_precificacao="ORCAMENTO",
            area_atendimento=area,
        )

        self.assertIs(
            servico.area_atendimento,
            area,
        )

        self.assertIsInstance(
            servico.area_atendimento,
            AreaAtendimento,
        )

    def test_area_atendimento_deve_ser_instancia_valida(
        self,
    ):
        """
        Oferta não deve aceitar estrutura geográfica
        que não seja AreaAtendimento.
        """

        with self.assertRaises(
            TypeError
        ):
            criar_servico_ofertado_empresa(
                codigo=1,
                empresa=self.empresa,
                tipo_servico=self.tipo_padrao,
                modelo_precificacao="ORCAMENTO",
                area_atendimento={
                    "modalidade": "RAIO",
                },
            )

    def test_converter_servico_com_area_atendimento(
        self,
    ):
        """
        Conversão deve preparar também a Área
        de Atendimento para persistência.
        """

        area = criar_area_atendimento(
            modalidade="RAIO",
            municipio_base="Caetité",
            uf_base="BA",
            raio_km=150,
        )

        servico = criar_servico_ofertado_empresa(
            codigo=1,
            empresa=self.empresa,
            tipo_servico=self.tipo_padrao,
            modelo_precificacao="ORCAMENTO",
            area_atendimento=area,
        )

        dados = (
            converter_servico_ofertado_para_dicionario(
                servico
            )
        )

        self.assertEqual(
            dados["area_atendimento"],
            {
                "modalidade": "RAIO",
                "municipio_base": "Caetité",
                "uf_base": "BA",
                "raio_km": 150.0,
                "municipios": (),
            },
        )

    def test_marketplace_sem_area_nao_e_elegivel(
        self,
    ):
        """
        Participar do marketplace não basta.

        Sem Área de Atendimento configurada,
        a oferta ainda não pode receber
        oportunidades abertas.
        """

        servico = criar_servico_ofertado_empresa(
            codigo=1,
            empresa=self.empresa,
            tipo_servico=self.tipo_padrao,
            modelo_precificacao="ORCAMENTO",
            participa_marketplace=True,
        )

        self.assertFalse(
            servico_elegivel_marketplace(
                servico
            )
        )

    def test_marketplace_com_area_valida_e_elegivel(
        self,
    ):
        """
        Oferta ativa, participante do marketplace
        e com Área de Atendimento válida deve
        estar elegível para oportunidades abertas.
        """

        area = criar_area_atendimento(
            modalidade="RAIO",
            municipio_base="Caetité",
            uf_base="BA",
            raio_km=150,
        )

        servico = criar_servico_ofertado_empresa(
            codigo=1,
            empresa=self.empresa,
            tipo_servico=self.tipo_padrao,
            modelo_precificacao="ORCAMENTO",
            participa_marketplace=True,
            area_atendimento=area,
        )

        self.assertTrue(
            servico_elegivel_marketplace(
                servico
            )
        )

    def test_area_nao_obriga_participacao_marketplace(
        self,
    ):
        """
        Possuir Área de Atendimento não deve
        habilitar automaticamente o marketplace.
        """

        area = criar_area_atendimento(
            modalidade="RAIO",
            municipio_base="Caetité",
            uf_base="BA",
            raio_km=150,
        )

        servico = criar_servico_ofertado_empresa(
            codigo=1,
            empresa=self.empresa,
            tipo_servico=self.tipo_padrao,
            modelo_precificacao="ORCAMENTO",
            participa_marketplace=False,
            area_atendimento=area,
        )

        self.assertFalse(
            servico_elegivel_marketplace(
                servico
            )
        )

    def test_servico_inativo_nao_e_elegivel_marketplace(
        self,
    ):
        """
        Oferta inativa não pode receber
        oportunidades do marketplace.
        """

        area = criar_area_atendimento(
            modalidade="RAIO",
            municipio_base="Caetité",
            uf_base="BA",
            raio_km=150,
        )

        servico = criar_servico_ofertado_empresa(
            codigo=1,
            empresa=self.empresa,
            tipo_servico=self.tipo_padrao,
            modelo_precificacao="ORCAMENTO",
            participa_marketplace=True,
            area_atendimento=area,
        )

        servico.inativar()

        self.assertFalse(
            servico_elegivel_marketplace(
                servico
            )
        )

    def test_elegibilidade_marketplace_exige_servico_valido(
        self,
    ):
        """
        Consulta de elegibilidade deve receber
        uma oferta válida.
        """

        with self.assertRaises(
            TypeError
        ):
            servico_elegivel_marketplace(
                {
                    "codigo": 1,
                }
            )

    def test_buscar_servico_ofertado_por_codigo(
        self,
    ):
        """
        Deve retornar a oferta correspondente
        ao código informado.
        """

        servico_1 = criar_servico_ofertado_empresa(
            codigo=1,
            empresa=self.empresa,
            tipo_servico=self.tipo_padrao,
            modelo_precificacao="ORCAMENTO",
        )

        servico_2 = criar_servico_ofertado_empresa(
            codigo=2,
            empresa=self.empresa,
            tipo_servico=self.tipo_personalizado,
            modelo_precificacao="SOB_CONSULTA",
        )

        servicos = [
            servico_1,
            servico_2,
        ]

        resultado = (
            buscar_servico_ofertado_por_codigo(
                servicos,
                2,
            )
        )

        self.assertIs(
            resultado,
            servico_2,
        )

    def test_buscar_servico_ofertado_inexistente(
        self,
    ):
        """
        Busca por código inexistente deve
        retornar None.
        """

        servico = criar_servico_ofertado_empresa(
            codigo=1,
            empresa=self.empresa,
            tipo_servico=self.tipo_padrao,
            modelo_precificacao="ORCAMENTO",
        )

        resultado = (
            buscar_servico_ofertado_por_codigo(
                [servico],
                999,
            )
        )

        self.assertIsNone(
            resultado
        )

    def test_buscar_servico_ofertado_exige_codigo_valido(
        self,
    ):
        """
        Código utilizado na busca deve ser
        inteiro positivo.
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
                    buscar_servico_ofertado_por_codigo(
                        [],
                        codigo,
                    )

    def test_listar_servicos_ofertados_por_empresa(
        self,
    ):
        """
        Deve retornar todas as ofertas da Empresa,
        inclusive ofertas inativas.
        """

        servico_1 = criar_servico_ofertado_empresa(
            codigo=1,
            empresa=self.empresa,
            tipo_servico=self.tipo_padrao,
            modelo_precificacao="ORCAMENTO",
        )

        servico_2 = criar_servico_ofertado_empresa(
            codigo=2,
            empresa=self.empresa,
            tipo_servico=self.tipo_personalizado,
            modelo_precificacao="SOB_CONSULTA",
        )

        servico_2.inativar()

        outra_empresa = criar_dados_empresa(
            codigo=2,
            razao_social=(
                "Energia Solar Sertão Ltda"
            ),
            nome_fantasia="Solar Sertão",
            cnpj="45.723.174/0001-10",
            email=(
                "contato@solarsertao.com.br"
            ),
            telefone="(77) 98888-7777",
        )

        outro_tipo = criar_tipo_servico(
            codigo=2,
            nome="Limpeza de Módulos",
            categoria=(
                "LIMPEZA_E_CONSERVACAO"
            ),
            origem="PADRAO_PLATAFORMA",
            fluxo_operacional=(
                "ORDEM_SERVICO_POS_VENDA"
            ),
        )

        servico_outra_empresa = (
            criar_servico_ofertado_empresa(
                codigo=3,
                empresa=outra_empresa,
                tipo_servico=outro_tipo,
                modelo_precificacao="SOB_CONSULTA",
            )
        )

        servicos = [
            servico_1,
            servico_2,
            servico_outra_empresa,
        ]

        resultado = (
            listar_servicos_ofertados_por_empresa(
                servicos,
                1,
            )
        )

        self.assertEqual(
            resultado,
            [
                servico_1,
                servico_2,
            ],
        )

        self.assertFalse(
            resultado[1].ativo
        )

    def test_listar_servicos_ofertados_ativos(
        self,
    ):
        """
        Deve retornar somente ofertas
        atualmente ativas.
        """

        servico_ativo = (
            criar_servico_ofertado_empresa(
                codigo=1,
                empresa=self.empresa,
                tipo_servico=self.tipo_padrao,
                modelo_precificacao="ORCAMENTO",
            )
        )

        servico_inativo = (
            criar_servico_ofertado_empresa(
                codigo=2,
                empresa=self.empresa,
                tipo_servico=self.tipo_personalizado,
                modelo_precificacao="SOB_CONSULTA",
            )
        )

        servico_inativo.inativar()

        servicos = [
            servico_ativo,
            servico_inativo,
        ]

        resultado = (
            listar_servicos_ofertados_ativos(
                servicos
            )
        )

        self.assertEqual(
            resultado,
            [
                servico_ativo,
            ],
        )

    def test_listar_servicos_ativos_nao_altera_lista_original(
        self,
    ):
        """
        Consulta de ofertas ativas não deve
        modificar a lista recebida.
        """

        servico_ativo = (
            criar_servico_ofertado_empresa(
                codigo=1,
                empresa=self.empresa,
                tipo_servico=self.tipo_padrao,
                modelo_precificacao="ORCAMENTO",
            )
        )

        servico_inativo = (
            criar_servico_ofertado_empresa(
                codigo=2,
                empresa=self.empresa,
                tipo_servico=self.tipo_personalizado,
                modelo_precificacao="SOB_CONSULTA",
            )
        )

        servico_inativo.inativar()

        servicos = [
            servico_ativo,
            servico_inativo,
        ]

        lista_original = list(
            servicos
        )

        listar_servicos_ofertados_ativos(
            servicos
        )

        self.assertEqual(
            servicos,
            lista_original,
        )

    def test_listar_servicos_por_tipo_servico(
        self,
    ):
        """
        Deve retornar ofertas de diferentes Empresas
        vinculadas ao mesmo Tipo de Serviço.
        """

        servico_empresa_1 = (
            criar_servico_ofertado_empresa(
                codigo=1,
                empresa=self.empresa,
                tipo_servico=self.tipo_padrao,
                modelo_precificacao="ORCAMENTO",
            )
        )

        outra_empresa = criar_dados_empresa(
            codigo=2,
            razao_social=(
                "Energia Solar Sertão Ltda"
            ),
            nome_fantasia="Solar Sertão",
            cnpj="45.723.174/0001-10",
            email=(
                "contato@solarsertao.com.br"
            ),
            telefone="(77) 98888-7777",
        )

        servico_empresa_2 = (
            criar_servico_ofertado_empresa(
                codigo=2,
                empresa=outra_empresa,
                tipo_servico=self.tipo_padrao,
                modelo_precificacao="ORCAMENTO",
            )
        )

        servico_outro_tipo = (
            criar_servico_ofertado_empresa(
                codigo=3,
                empresa=self.empresa,
                tipo_servico=self.tipo_personalizado,
                modelo_precificacao="SOB_CONSULTA",
            )
        )

        servicos = [
            servico_empresa_1,
            servico_empresa_2,
            servico_outro_tipo,
        ]

        resultado = (
            listar_servicos_ofertados_por_tipo_servico(
                servicos,
                1,
            )
        )

        self.assertEqual(
            resultado,
            [
                servico_empresa_1,
                servico_empresa_2,
            ],
        )

    def test_consultas_em_lista_vazia(
        self,
    ):
        """
        Consultas em coleção vazia devem
        retornar resultados vazios ou None.
        """

        self.assertIsNone(
            buscar_servico_ofertado_por_codigo(
                [],
                1,
            )
        )

        self.assertEqual(
            listar_servicos_ofertados_por_empresa(
                [],
                1,
            ),
            [],
        )

        self.assertEqual(
            listar_servicos_ofertados_ativos(
                []
            ),
            [],
        )

        self.assertEqual(
            listar_servicos_ofertados_por_tipo_servico(
                [],
                1,
            ),
            [],
        )

    def test_consultas_rejeitam_elemento_invalido(
        self,
    ):
        """
        Coleções de ofertas devem conter somente
        instâncias de ServicoOfertadoEmpresa.
        """

        lista_invalida = [
            {
                "codigo": 1,
            },
        ]

        with self.assertRaises(
            TypeError
        ):
            buscar_servico_ofertado_por_codigo(
                lista_invalida,
                1,
            )

        with self.assertRaises(
            TypeError
        ):
            listar_servicos_ofertados_por_empresa(
                lista_invalida,
                1,
            )

        with self.assertRaises(
            TypeError
        ):
            listar_servicos_ofertados_ativos(
                lista_invalida
            )

        with self.assertRaises(
            TypeError
        ):
            listar_servicos_ofertados_por_tipo_servico(
                lista_invalida,
                1,
            )

    def test_servico_ofertado_duplicado_ativo(
        self,
    ):
        """
        Deve identificar duplicidade quando
        Empresa e Tipo de Serviço já possuem
        uma oferta ativa.
        """

        servico = criar_servico_ofertado_empresa(
            codigo=1,
            empresa=self.empresa,
            tipo_servico=self.tipo_padrao,
            modelo_precificacao="ORCAMENTO",
        )

        resultado = servico_ofertado_duplicado(
            [servico],
            codigo_empresa=1,
            codigo_tipo_servico=1,
        )

        self.assertTrue(
            resultado
        )

    def test_servico_ofertado_inativo_tambem_e_duplicado(
        self,
    ):
        """
        Oferta inativa continua representando
        o vínculo Empresa x Tipo de Serviço.
        """

        servico = criar_servico_ofertado_empresa(
            codigo=1,
            empresa=self.empresa,
            tipo_servico=self.tipo_padrao,
            modelo_precificacao="ORCAMENTO",
        )

        servico.inativar()

        resultado = servico_ofertado_duplicado(
            [servico],
            codigo_empresa=1,
            codigo_tipo_servico=1,
        )

        self.assertTrue(
            resultado
        )

    def test_mesma_empresa_outro_tipo_nao_e_duplicado(
        self,
    ):
        """
        A mesma Empresa pode possuir ofertas
        para Tipos de Serviço diferentes.
        """

        servico = criar_servico_ofertado_empresa(
            codigo=1,
            empresa=self.empresa,
            tipo_servico=self.tipo_padrao,
            modelo_precificacao="ORCAMENTO",
        )

        resultado = servico_ofertado_duplicado(
            [servico],
            codigo_empresa=1,
            codigo_tipo_servico=100,
        )

        self.assertFalse(
            resultado
        )

    def test_outra_empresa_mesmo_tipo_nao_e_duplicado(
        self,
    ):
        """
        Empresas diferentes podem oferecer
        o mesmo Tipo de Serviço.
        """

        servico = criar_servico_ofertado_empresa(
            codigo=1,
            empresa=self.empresa,
            tipo_servico=self.tipo_padrao,
            modelo_precificacao="ORCAMENTO",
        )

        resultado = servico_ofertado_duplicado(
            [servico],
            codigo_empresa=2,
            codigo_tipo_servico=1,
        )

        self.assertFalse(
            resultado
        )

    def test_lista_vazia_nao_possui_servico_duplicado(
        self,
    ):
        """
        Coleção vazia não possui vínculo duplicado.
        """

        resultado = servico_ofertado_duplicado(
            [],
            codigo_empresa=1,
            codigo_tipo_servico=1,
        )

        self.assertFalse(
            resultado
        )

    def test_verificacao_duplicidade_rejeita_elemento_invalido(
        self,
    ):
        """
        Verificação de duplicidade deve receber
        somente ofertas válidas na coleção.
        """

        servicos_invalidos = [
            {
                "codigo": 1,
            },
        ]

        with self.assertRaises(
            TypeError
        ):
            servico_ofertado_duplicado(
                servicos_invalidos,
                codigo_empresa=1,
                codigo_tipo_servico=1,
            )

    def test_validar_nova_oferta_bloqueia_duplicidade_ativa(
        self,
    ):
        """
        Não deve permitir novo cadastro quando
        o vínculo Empresa x Tipo já estiver ativo.
        """

        servico_existente = (
            criar_servico_ofertado_empresa(
                codigo=1,
                empresa=self.empresa,
                tipo_servico=self.tipo_padrao,
                modelo_precificacao="ORCAMENTO",
            )
        )

        with self.assertRaises(
            RegistroDuplicado
        ):
            validar_nova_oferta_servico(
                servicos_ofertados=[
                    servico_existente,
                ],
                empresa=self.empresa,
                tipo_servico=self.tipo_padrao,
            )

    def test_validar_nova_oferta_bloqueia_duplicidade_inativa(
        self,
    ):
        """
        Oferta inativa não deve permitir a criação
        de uma nova entidade equivalente.

        O fluxo correto é reativar a oferta
        já existente.
        """

        servico_existente = (
            criar_servico_ofertado_empresa(
                codigo=1,
                empresa=self.empresa,
                tipo_servico=self.tipo_padrao,
                modelo_precificacao="ORCAMENTO",
            )
        )

        servico_existente.inativar()

        with self.assertRaises(
            RegistroDuplicado
        ):
            validar_nova_oferta_servico(
                servicos_ofertados=[
                    servico_existente,
                ],
                empresa=self.empresa,
                tipo_servico=self.tipo_padrao,
            )

        self.assertFalse(
            servico_existente.ativo
        )

    def test_validar_nova_oferta_permite_vinculo_inexistente(
        self,
    ):
        """
        Deve permitir validação quando ainda não
        existir a combinação Empresa x Tipo.
        """

        servico_existente = (
            criar_servico_ofertado_empresa(
                codigo=1,
                empresa=self.empresa,
                tipo_servico=self.tipo_padrao,
                modelo_precificacao="ORCAMENTO",
            )
        )

        resultado = validar_nova_oferta_servico(
            servicos_ofertados=[
                servico_existente,
            ],
            empresa=self.empresa,
            tipo_servico=self.tipo_personalizado,
        )

        self.assertIsNone(
            resultado
        )



if __name__ == "__main__":
    unittest.main()