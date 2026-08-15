import unittest

from app.dominio.erros_dominio import (
    DadosObrigatoriosAusentes,
    TransicaoEstadoInvalida,
    ValorInvalido,
)

from app.dominio.servicos_empresa import (
    criar_servico_ofertado_empresa,
)

from app.dominio.solicitacoes_servico import (
    ModalidadeSolicitacaoServico,
    OrigemSolicitacaoServico,
    SolicitacaoServico,
    alterar_status_solicitacao_servico,
    buscar_solicitacao_servico_por_codigo,
    converter_solicitacao_servico_para_dicionario,
    criar_solicitacao_servico,
    listar_solicitacoes_diretas_por_empresa,
    listar_solicitacoes_por_cliente,
    listar_solicitacoes_por_modalidade,
    listar_solicitacoes_por_status,
    listar_solicitacoes_por_tipo_servico,
)

from app.dominio.tipos_servico import (
    criar_tipo_servico,
)

class TestSolicitacoesServicoDominio(
    unittest.TestCase
):
    """
    Testes do domínio de Solicitações de Serviço.
    """

    def setUp(
        self,
    ):
        self.cliente = {
            "codigo": 1,
            "nome": "Cliente Teste",
        }

        self.tipo_servico = criar_tipo_servico(
            codigo=1,
            nome="Limpeza de Módulos",
            categoria="LIMPEZA_E_CONSERVACAO",
            origem="PADRAO_PLATAFORMA",
            fluxo_operacional=(
                "ORDEM_SERVICO_POS_VENDA"
            ),
        )

        self.empresa = {
            "codigo": 1,
            "razao_social": (
                "Empresa Solar Teste Ltda"
            ),
            "nome_fantasia": "Solar Teste",
            "cnpj": "12.345.678/0001-95",
            "email": "empresa@teste.com",
            "telefone": "(77) 99999-9999",
            "situacao": "ATIVA",
        }

        self.servico_ofertado = (
            criar_servico_ofertado_empresa(
                codigo=1,
                empresa=self.empresa,
                tipo_servico=self.tipo_servico,
                modelo_precificacao=(
                    "SOB_CONSULTA"
                ),
                aceita_solicitacao_direta=True,
            )
        )

    def test_criar_solicitacao_aberta(
        self,
    ):
        """
        Deve criar Solicitação ABERTA
        sem Empresa ou oferta vinculada.
        """

        solicitacao = criar_solicitacao_servico(
            codigo=1,
            cliente=self.cliente,
            tipo_servico=self.tipo_servico,
            modalidade="ABERTA",
            origem="CLIENTE",
            municipio="Caetité",
            uf="BA",
            dados_tecnicos={
                "quantidade_modulos": 20,
            },
        )

        self.assertIsInstance(
            solicitacao,
            SolicitacaoServico,
        )

        self.assertEqual(
            solicitacao.codigo,
            1,
        )

        self.assertEqual(
            solicitacao.codigo_cliente,
            1,
        )

        self.assertEqual(
            solicitacao.codigo_tipo_servico,
            1,
        )

        self.assertEqual(
            solicitacao.modalidade,
            ModalidadeSolicitacaoServico.ABERTA,
        )

        self.assertEqual(
            solicitacao.origem,
            OrigemSolicitacaoServico.CLIENTE,
        )

        self.assertIsNone(
            solicitacao.codigo_empresa_destinataria
        )

        self.assertIsNone(
            solicitacao.codigo_servico_ofertado_empresa
        )

    def test_nova_solicitacao_inicia_em_elaboracao(
        self,
    ):
        """
        Toda nova Solicitação deve iniciar
        em EM_ELABORACAO.
        """

        solicitacao = criar_solicitacao_servico(
            codigo=1,
            cliente=self.cliente,
            tipo_servico=self.tipo_servico,
            modalidade="ABERTA",
            origem="CLIENTE",
            municipio="Caetité",
            uf="BA",
            dados_tecnicos={},
        )

        self.assertEqual(
            solicitacao.status,
            "EM_ELABORACAO",
        )

    def test_modalidade_deve_ser_normalizada(
        self,
    ):
        """
        Texto válido deve ser convertido
        para ModalidadeSolicitacaoServico.
        """

        solicitacao = criar_solicitacao_servico(
            codigo=1,
            cliente=self.cliente,
            tipo_servico=self.tipo_servico,
            modalidade="ABERTA",
            origem="CLIENTE",
            municipio="Caetité",
            uf="BA",
            dados_tecnicos={},
        )

        self.assertEqual(
            solicitacao.modalidade,
            ModalidadeSolicitacaoServico.ABERTA,
        )

    def test_modalidade_invalida_deve_ser_rejeitada(
        self,
    ):
        """
        Modalidade desconhecida deve
        ser rejeitada.
        """

        with self.assertRaises(
            ValorInvalido
        ):
            criar_solicitacao_servico(
                codigo=1,
                cliente=self.cliente,
                tipo_servico=self.tipo_servico,
                modalidade="QUALQUER",
                origem="CLIENTE",
                municipio="Caetité",
                uf="BA",
                dados_tecnicos={},
            )

    def test_origem_deve_ser_normalizada(
        self,
    ):
        """
        Origem textual válida deve virar Enum.
        """

        solicitacao = criar_solicitacao_servico(
            codigo=1,
            cliente=self.cliente,
            tipo_servico=self.tipo_servico,
            modalidade="ABERTA",
            origem="EMPRESA",
            municipio="Caetité",
            uf="BA",
            dados_tecnicos={},
        )

        self.assertEqual(
            solicitacao.origem,
            OrigemSolicitacaoServico.EMPRESA,
        )

    def test_origem_invalida_deve_ser_rejeitada(
        self,
    ):
        """
        Origem desconhecida deve
        ser rejeitada.
        """

        with self.assertRaises(
            ValorInvalido
        ):
            criar_solicitacao_servico(
                codigo=1,
                cliente=self.cliente,
                tipo_servico=self.tipo_servico,
                modalidade="ABERTA",
                origem="OUTRA",
                municipio="Caetité",
                uf="BA",
                dados_tecnicos={},
            )

    def test_codigo_solicitacao_deve_ser_positivo(
        self,
    ):
        """
        Código deve ser inteiro positivo.
        """

        for codigo in (
            0,
            -1,
            1.5,
            "1",
            True,
        ):
            with self.subTest(
                codigo=codigo
            ):
                with self.assertRaises(
                    ValorInvalido
                ):
                    criar_solicitacao_servico(
                        codigo=codigo,
                        cliente=self.cliente,
                        tipo_servico=self.tipo_servico,
                        modalidade="ABERTA",
                        origem="CLIENTE",
                        municipio="Caetité",
                        uf="BA",
                        dados_tecnicos={},
                    )

    def test_cliente_deve_ser_dicionario(
        self,
    ):
        """
        Cliente inválido deve ser rejeitado.
        """

        with self.assertRaises(
            TypeError
        ):
            criar_solicitacao_servico(
                codigo=1,
                cliente="Cliente",
                tipo_servico=self.tipo_servico,
                modalidade="ABERTA",
                origem="CLIENTE",
                municipio="Caetité",
                uf="BA",
                dados_tecnicos={},
            )

    def test_cliente_sem_codigo_deve_ser_rejeitado(
        self,
    ):
        """
        Cliente precisa possuir código.
        """

        with self.assertRaises(
            DadosObrigatoriosAusentes
        ):
            criar_solicitacao_servico(
                codigo=1,
                cliente={
                    "nome": "Cliente Teste",
                },
                tipo_servico=self.tipo_servico,
                modalidade="ABERTA",
                origem="CLIENTE",
                municipio="Caetité",
                uf="BA",
                dados_tecnicos={},
            )

    def test_tipo_servico_deve_ser_instancia_valida(
        self,
    ):
        """
        Tipo solicitado deve ser TipoServico.
        """

        with self.assertRaises(
            TypeError
        ):
            criar_solicitacao_servico(
                codigo=1,
                cliente=self.cliente,
                tipo_servico={
                    "codigo": 1,
                },
                modalidade="ABERTA",
                origem="CLIENTE",
                municipio="Caetité",
                uf="BA",
                dados_tecnicos={},
            )

    def test_tipo_servico_inativo_nao_pode_ser_solicitado(
        self,
    ):
        """
        Não deve criar nova Solicitação
        para Tipo de Serviço inativo.
        """

        self.tipo_servico.inativar()

        with self.assertRaises(
            ValorInvalido
        ):
            criar_solicitacao_servico(
                codigo=1,
                cliente=self.cliente,
                tipo_servico=self.tipo_servico,
                modalidade="ABERTA",
                origem="CLIENTE",
                municipio="Caetité",
                uf="BA",
                dados_tecnicos={},
            )

    def test_municipio_deve_ser_normalizado(
        self,
    ):
        """
        Espaços excedentes devem ser removidos.
        """

        solicitacao = criar_solicitacao_servico(
            codigo=1,
            cliente=self.cliente,
            tipo_servico=self.tipo_servico,
            modalidade="ABERTA",
            origem="CLIENTE",
            municipio="  Vitória   da Conquista  ",
            uf="BA",
            dados_tecnicos={},
        )

        self.assertEqual(
            solicitacao.municipio,
            "Vitória da Conquista",
        )

    def test_municipio_e_obrigatorio(
        self,
    ):
        """
        Município vazio deve ser rejeitado.
        """

        for municipio in (
            None,
            "",
            "   ",
        ):
            with self.subTest(
                municipio=municipio
            ):
                with self.assertRaises(
                    DadosObrigatoriosAusentes
                ):
                    criar_solicitacao_servico(
                        codigo=1,
                        cliente=self.cliente,
                        tipo_servico=self.tipo_servico,
                        modalidade="ABERTA",
                        origem="CLIENTE",
                        municipio=municipio,
                        uf="BA",
                        dados_tecnicos={},
                    )

    def test_uf_deve_ser_normalizada(
        self,
    ):
        """
        UF deve ser armazenada em maiúsculas.
        """

        solicitacao = criar_solicitacao_servico(
            codigo=1,
            cliente=self.cliente,
            tipo_servico=self.tipo_servico,
            modalidade="ABERTA",
            origem="CLIENTE",
            municipio="Caetité",
            uf="ba",
            dados_tecnicos={},
        )

        self.assertEqual(
            solicitacao.uf,
            "BA",
        )

    def test_uf_invalida_deve_ser_rejeitada(
        self,
    ):
        """
        UF deve possuir duas letras.
        """

        for uf in (
            "B",
            "BAH",
            "B1",
            "",
        ):
            with self.subTest(
                uf=uf
            ):
                with self.assertRaises(
                    ValorInvalido
                ):
                    criar_solicitacao_servico(
                        codigo=1,
                        cliente=self.cliente,
                        tipo_servico=self.tipo_servico,
                        modalidade="ABERTA",
                        origem="CLIENTE",
                        municipio="Caetité",
                        uf=uf,
                        dados_tecnicos={},
                    )

    def test_uf_e_obrigatoria(
        self,
    ):
        """
        Ausência de UF deve ser rejeitada.
        """

        with self.assertRaises(
            DadosObrigatoriosAusentes
        ):
            criar_solicitacao_servico(
                codigo=1,
                cliente=self.cliente,
                tipo_servico=self.tipo_servico,
                modalidade="ABERTA",
                origem="CLIENTE",
                municipio="Caetité",
                uf=None,
                dados_tecnicos={},
            )

    def test_dados_tecnicos_devem_ser_dicionario(
        self,
    ):
        """
        Estrutura técnica inválida
        deve ser rejeitada.
        """

        with self.assertRaises(
            ValorInvalido
        ):
            criar_solicitacao_servico(
                codigo=1,
                cliente=self.cliente,
                tipo_servico=self.tipo_servico,
                modalidade="ABERTA",
                origem="CLIENTE",
                municipio="Caetité",
                uf="BA",
                dados_tecnicos=[
                    "item",
                ],
            )

    def test_dados_tecnicos_sao_obrigatorios(
        self,
    ):
        """
        None não representa estrutura
        técnica válida.
        """

        with self.assertRaises(
            DadosObrigatoriosAusentes
        ):
            criar_solicitacao_servico(
                codigo=1,
                cliente=self.cliente,
                tipo_servico=self.tipo_servico,
                modalidade="ABERTA",
                origem="CLIENTE",
                municipio="Caetité",
                uf="BA",
                dados_tecnicos=None,
            )

    def test_dados_tecnicos_podem_ser_vazios(
        self,
    ):
        """
        Nesta etapa ainda não há schema técnico
        obrigatório por Tipo de Serviço.
        """

        solicitacao = criar_solicitacao_servico(
            codigo=1,
            cliente=self.cliente,
            tipo_servico=self.tipo_servico,
            modalidade="ABERTA",
            origem="CLIENTE",
            municipio="Caetité",
            uf="BA",
            dados_tecnicos={},
        )

        self.assertEqual(
            solicitacao.dados_tecnicos,
            {},
        )

    def test_dados_tecnicos_devem_ser_copiados(
        self,
    ):
        """
        Alteração posterior no dicionário recebido
        não deve alterar a Solicitação.
        """

        dados_originais = {
            "quantidade_modulos": 20,
        }

        solicitacao = criar_solicitacao_servico(
            codigo=1,
            cliente=self.cliente,
            tipo_servico=self.tipo_servico,
            modalidade="ABERTA",
            origem="CLIENTE",
            municipio="Caetité",
            uf="BA",
            dados_tecnicos=dados_originais,
        )

        dados_originais[
            "quantidade_modulos"
        ] = 999

        self.assertEqual(
            solicitacao.dados_tecnicos[
                "quantidade_modulos"
            ],
            20,
        )

    def test_converter_solicitacao_para_dicionario(
        self,
    ):
        """
        Conversão deve preparar Enums
        para persistência.
        """

        solicitacao = criar_solicitacao_servico(
            codigo=1,
            cliente=self.cliente,
            tipo_servico=self.tipo_servico,
            modalidade="ABERTA",
            origem="CLIENTE",
            municipio="Caetité",
            uf="BA",
            dados_tecnicos={
                "quantidade_modulos": 20,
            },
        )

        dados = (
            converter_solicitacao_servico_para_dicionario(
                solicitacao
            )
        )

        self.assertEqual(
            dados,
            {
                "codigo": 1,
                "codigo_cliente": 1,
                "codigo_tipo_servico": 1,
                "modalidade": "ABERTA",
                "origem": "CLIENTE",
                "municipio": "Caetité",
                "uf": "BA",
                "dados_tecnicos": {
                    "quantidade_modulos": 20,
                },
                "codigo_empresa_destinataria": None,
                "codigo_servico_ofertado_empresa": None,
                "status": "EM_ELABORACAO",
            },
        )

    def test_converter_exige_solicitacao_valida(
        self,
    ):
        """
        Conversor deve receber uma entidade
        SolicitacaoServico.
        """

        with self.assertRaises(
            TypeError
        ):
            converter_solicitacao_servico_para_dicionario(
                {
                    "codigo": 1,
                }
            )

    def test_criar_solicitacao_direta(
        self,
    ):
        """
        Solicitação DIRETA deve ser vinculada
        à oferta e à Empresa destinatária.
        """

        solicitacao = criar_solicitacao_servico(
            codigo=1,
            cliente=self.cliente,
            tipo_servico=self.tipo_servico,
            modalidade="DIRETA",
            origem="CLIENTE",
            municipio="Caetité",
            uf="BA",
            dados_tecnicos={},
            servico_ofertado=self.servico_ofertado,
        )

        self.assertEqual(
            solicitacao.modalidade,
            ModalidadeSolicitacaoServico.DIRETA,
        )

        self.assertEqual(
            solicitacao.codigo_empresa_destinataria,
            self.servico_ofertado.codigo_empresa,
        )

        self.assertEqual(
            solicitacao.codigo_servico_ofertado_empresa,
            self.servico_ofertado.codigo,
        )

    def test_solicitacao_direta_exige_oferta(
        self,
    ):
        """
        Solicitação DIRETA não pode existir
        sem Serviço oferecido.
        """

        with self.assertRaises(
            TypeError
        ):
            criar_solicitacao_servico(
                codigo=1,
                cliente=self.cliente,
                tipo_servico=self.tipo_servico,
                modalidade="DIRETA",
                origem="CLIENTE",
                municipio="Caetité",
                uf="BA",
                dados_tecnicos={},
            )

    def test_solicitacao_direta_exige_oferta_valida(
        self,
    ):
        """
        Oferta da Solicitação DIRETA deve ser
        ServicoOfertadoEmpresa.
        """

        with self.assertRaises(
            TypeError
        ):
            criar_solicitacao_servico(
                codigo=1,
                cliente=self.cliente,
                tipo_servico=self.tipo_servico,
                modalidade="DIRETA",
                origem="CLIENTE",
                municipio="Caetité",
                uf="BA",
                dados_tecnicos={},
                servico_ofertado={
                    "codigo": 1,
                },
            )

    def test_solicitacao_direta_rejeita_oferta_inativa(
        self,
    ):
        """
        Oferta inativa não pode receber
        nova Solicitação DIRETA.
        """

        self.servico_ofertado.inativar()

        with self.assertRaises(
            ValorInvalido
        ):
            criar_solicitacao_servico(
                codigo=1,
                cliente=self.cliente,
                tipo_servico=self.tipo_servico,
                modalidade="DIRETA",
                origem="CLIENTE",
                municipio="Caetité",
                uf="BA",
                dados_tecnicos={},
                servico_ofertado=(
                    self.servico_ofertado
                ),
            )

    def test_solicitacao_direta_exige_permissao_da_oferta(
        self,
    ):
        """
        A oferta precisa aceitar
        Solicitações DIRETAS.
        """

        oferta = criar_servico_ofertado_empresa(
            codigo=2,
            empresa=self.empresa,
            tipo_servico=self.tipo_servico,
            modelo_precificacao="SOB_CONSULTA",
            aceita_solicitacao_direta=False,
        )

        with self.assertRaises(
            ValorInvalido
        ):
            criar_solicitacao_servico(
                codigo=1,
                cliente=self.cliente,
                tipo_servico=self.tipo_servico,
                modalidade="DIRETA",
                origem="CLIENTE",
                municipio="Caetité",
                uf="BA",
                dados_tecnicos={},
                servico_ofertado=oferta,
            )

    def test_solicitacao_direta_rejeita_oferta_de_outro_tipo(
        self,
    ):
        """
        Oferta deve corresponder exatamente
        ao Tipo de Serviço solicitado.
        """

        outro_tipo = criar_tipo_servico(
            codigo=2,
            nome="Manutenção Elétrica",
            categoria="MANUTENCAO_CORRETIVA",
            origem="PADRAO_PLATAFORMA",
            fluxo_operacional=(
                "ORDEM_SERVICO_POS_VENDA"
            ),
        )

        oferta_outro_tipo = (
            criar_servico_ofertado_empresa(
                codigo=2,
                empresa=self.empresa,
                tipo_servico=outro_tipo,
                modelo_precificacao=(
                    "SOB_CONSULTA"
                ),
                aceita_solicitacao_direta=True,
            )
        )

        with self.assertRaises(
            ValorInvalido
        ):
            criar_solicitacao_servico(
                codigo=1,
                cliente=self.cliente,
                tipo_servico=self.tipo_servico,
                modalidade="DIRETA",
                origem="CLIENTE",
                municipio="Caetité",
                uf="BA",
                dados_tecnicos={},
                servico_ofertado=oferta_outro_tipo,
            )

    def test_solicitacao_aberta_rejeita_oferta_vinculada(
        self,
    ):
        """
        Solicitação ABERTA não deve nascer
        vinculada previamente a uma oferta.
        """

        with self.assertRaises(
            ValorInvalido
        ):
            criar_solicitacao_servico(
                codigo=1,
                cliente=self.cliente,
                tipo_servico=self.tipo_servico,
                modalidade="ABERTA",
                origem="CLIENTE",
                municipio="Caetité",
                uf="BA",
                dados_tecnicos={},
                servico_ofertado=(
                    self.servico_ofertado
                ),
            )

    def test_alterar_status_de_elaboracao_para_publicada(
        self,
    ):
        """
        Solicitação em elaboração pode
        ser publicada.
        """

        solicitacao = criar_solicitacao_servico(
            codigo=1,
            cliente=self.cliente,
            tipo_servico=self.tipo_servico,
            modalidade="ABERTA",
            origem="CLIENTE",
            municipio="Caetité",
            uf="BA",
            dados_tecnicos={},
        )

        resultado = alterar_status_solicitacao_servico(
            solicitacao,
            "PUBLICADA",
        )

        self.assertIs(
            resultado,
            solicitacao,
        )

        self.assertEqual(
            solicitacao.status,
            "PUBLICADA",
        )

    def test_novo_status_deve_ser_normalizado(
        self,
    ):
        """
        Espaços externos e caixa devem
        ser normalizados.
        """

        solicitacao = criar_solicitacao_servico(
            codigo=1,
            cliente=self.cliente,
            tipo_servico=self.tipo_servico,
            modalidade="ABERTA",
            origem="CLIENTE",
            municipio="Caetité",
            uf="BA",
            dados_tecnicos={},
        )

        alterar_status_solicitacao_servico(
            solicitacao,
            "  publicada  ",
        )

        self.assertEqual(
            solicitacao.status,
            "PUBLICADA",
        )

    def test_fluxo_valido_ate_analise_cliente(
        self,
    ):
        """
        Deve permitir o fluxo principal
        até análise das propostas.
        """

        solicitacao = criar_solicitacao_servico(
            codigo=1,
            cliente=self.cliente,
            tipo_servico=self.tipo_servico,
            modalidade="ABERTA",
            origem="CLIENTE",
            municipio="Caetité",
            uf="BA",
            dados_tecnicos={},
        )

        alterar_status_solicitacao_servico(
            solicitacao,
            "PUBLICADA",
        )

        alterar_status_solicitacao_servico(
            solicitacao,
            "RECEBENDO_PROPOSTAS",
        )

        alterar_status_solicitacao_servico(
            solicitacao,
            "EM_ANALISE_PELO_CLIENTE",
        )

        self.assertEqual(
            solicitacao.status,
            "EM_ANALISE_PELO_CLIENTE",
        )

    def test_analise_pode_retornar_para_recebimento(
        self,
    ):
        """
        Enquanto não estiver encerrada,
        a Solicitação pode voltar a receber propostas.
        """

        solicitacao = criar_solicitacao_servico(
            codigo=1,
            cliente=self.cliente,
            tipo_servico=self.tipo_servico,
            modalidade="ABERTA",
            origem="CLIENTE",
            municipio="Caetité",
            uf="BA",
            dados_tecnicos={},
        )

        alterar_status_solicitacao_servico(
            solicitacao,
            "PUBLICADA",
        )
        alterar_status_solicitacao_servico(
            solicitacao,
            "RECEBENDO_PROPOSTAS",
        )
        alterar_status_solicitacao_servico(
            solicitacao,
            "EM_ANALISE_PELO_CLIENTE",
        )
        alterar_status_solicitacao_servico(
            solicitacao,
            "RECEBENDO_PROPOSTAS",
        )

        self.assertEqual(
            solicitacao.status,
            "RECEBENDO_PROPOSTAS",
        )

    def test_analise_pode_encerrar_com_contratacao(
        self,
    ):
        """
        Solicitação em análise pode ser encerrada
        após aceite de proposta.
        """

        solicitacao = criar_solicitacao_servico(
            codigo=1,
            cliente=self.cliente,
            tipo_servico=self.tipo_servico,
            modalidade="ABERTA",
            origem="CLIENTE",
            municipio="Caetité",
            uf="BA",
            dados_tecnicos={},
        )

        alterar_status_solicitacao_servico(
            solicitacao,
            "PUBLICADA",
        )
        alterar_status_solicitacao_servico(
            solicitacao,
            "RECEBENDO_PROPOSTAS",
        )
        alterar_status_solicitacao_servico(
            solicitacao,
            "EM_ANALISE_PELO_CLIENTE",
        )
        alterar_status_solicitacao_servico(
            solicitacao,
            "ENCERRADA_COM_CONTRATACAO",
        )

        self.assertEqual(
            solicitacao.status,
            "ENCERRADA_COM_CONTRATACAO",
        )

    def test_solicitacao_em_elaboracao_pode_ser_cancelada(
        self,
    ):
        """
        Solicitação em elaboração pode
        ser cancelada.
        """

        solicitacao = criar_solicitacao_servico(
            codigo=1,
            cliente=self.cliente,
            tipo_servico=self.tipo_servico,
            modalidade="ABERTA",
            origem="CLIENTE",
            municipio="Caetité",
            uf="BA",
            dados_tecnicos={},
        )

        alterar_status_solicitacao_servico(
            solicitacao,
            "CANCELADA",
        )

        self.assertEqual(
            solicitacao.status,
            "CANCELADA",
        )

    def test_transicao_invalida_deve_ser_bloqueada(
        self,
    ):
        """
        Não deve permitir salto direto
        de elaboração para contratação.
        """

        solicitacao = criar_solicitacao_servico(
            codigo=1,
            cliente=self.cliente,
            tipo_servico=self.tipo_servico,
            modalidade="ABERTA",
            origem="CLIENTE",
            municipio="Caetité",
            uf="BA",
            dados_tecnicos={},
        )

        with self.assertRaises(
            TransicaoEstadoInvalida
        ):
            alterar_status_solicitacao_servico(
                solicitacao,
                "ENCERRADA_COM_CONTRATACAO",
            )

    def test_transicao_invalida_nao_altera_estado_atual(
        self,
    ):
        """
        Falha de transição não pode deixar
        a entidade parcialmente alterada.
        """

        solicitacao = criar_solicitacao_servico(
            codigo=1,
            cliente=self.cliente,
            tipo_servico=self.tipo_servico,
            modalidade="ABERTA",
            origem="CLIENTE",
            municipio="Caetité",
            uf="BA",
            dados_tecnicos={},
        )

        with self.assertRaises(
            TransicaoEstadoInvalida
        ):
            alterar_status_solicitacao_servico(
                solicitacao,
                "EM_ANALISE_PELO_CLIENTE",
            )

        self.assertEqual(
            solicitacao.status,
            "EM_ELABORACAO",
        )

    def test_status_inexistente_deve_ser_rejeitado(
        self,
    ):
        """
        Estado fora do catálogo oficial
        deve ser rejeitado.
        """

        solicitacao = criar_solicitacao_servico(
            codigo=1,
            cliente=self.cliente,
            tipo_servico=self.tipo_servico,
            modalidade="ABERTA",
            origem="CLIENTE",
            municipio="Caetité",
            uf="BA",
            dados_tecnicos={},
        )

        with self.assertRaises(
            ValorInvalido
        ):
            alterar_status_solicitacao_servico(
                solicitacao,
                "STATUS_INVENTADO",
            )

    def test_novo_status_e_obrigatorio(
        self,
    ):
        """
        Ausência de novo status deve
        ser rejeitada.
        """

        solicitacao = criar_solicitacao_servico(
            codigo=1,
            cliente=self.cliente,
            tipo_servico=self.tipo_servico,
            modalidade="ABERTA",
            origem="CLIENTE",
            municipio="Caetité",
            uf="BA",
            dados_tecnicos={},
        )

        with self.assertRaises(
            DadosObrigatoriosAusentes
        ):
            alterar_status_solicitacao_servico(
                solicitacao,
                None,
            )

    def test_estado_terminal_nao_pode_ser_reaberto(
        self,
    ):
        """
        Solicitação cancelada não pode
        retornar ao fluxo ativo.
        """

        solicitacao = criar_solicitacao_servico(
            codigo=1,
            cliente=self.cliente,
            tipo_servico=self.tipo_servico,
            modalidade="ABERTA",
            origem="CLIENTE",
            municipio="Caetité",
            uf="BA",
            dados_tecnicos={},
        )

        alterar_status_solicitacao_servico(
            solicitacao,
            "CANCELADA",
        )

        with self.assertRaises(
            TransicaoEstadoInvalida
        ):
            alterar_status_solicitacao_servico(
                solicitacao,
                "PUBLICADA",
            )

        self.assertEqual(
            solicitacao.status,
            "CANCELADA",
        )

    def test_alterar_status_exige_solicitacao_valida(
        self,
    ):
        """
        Operação deve receber
        SolicitacaoServico válida.
        """

        with self.assertRaises(
            TypeError
        ):
            alterar_status_solicitacao_servico(
                {
                    "codigo": 1,
                },
                "PUBLICADA",
            )

    def test_buscar_solicitacao_por_codigo(
        self,
    ):
        """
        Busca deve retornar a Solicitação
        correspondente ao código informado.
        """

        solicitacao_1 = criar_solicitacao_servico(
            codigo=1,
            cliente=self.cliente,
            tipo_servico=self.tipo_servico,
            modalidade="ABERTA",
            origem="CLIENTE",
            municipio="Caetité",
            uf="BA",
            dados_tecnicos={},
        )

        solicitacao_2 = criar_solicitacao_servico(
            codigo=2,
            cliente=self.cliente,
            tipo_servico=self.tipo_servico,
            modalidade="ABERTA",
            origem="CLIENTE",
            municipio="Caetité",
            uf="BA",
            dados_tecnicos={},
        )

        solicitacoes = [
            solicitacao_1,
            solicitacao_2,
        ]

        resultado = (
            buscar_solicitacao_servico_por_codigo(
                solicitacoes,
                2,
            )
        )

        self.assertIs(
            resultado,
            solicitacao_2,
        )

    def test_buscar_solicitacao_inexistente_retorna_none(
        self,
    ):
        """
        Código não encontrado deve
        retornar None.
        """

        solicitacao = criar_solicitacao_servico(
            codigo=1,
            cliente=self.cliente,
            tipo_servico=self.tipo_servico,
            modalidade="ABERTA",
            origem="CLIENTE",
            municipio="Caetité",
            uf="BA",
            dados_tecnicos={},
        )

        resultado = (
            buscar_solicitacao_servico_por_codigo(
                [solicitacao],
                999,
            )
        )

        self.assertIsNone(
            resultado
        )

    def test_buscar_solicitacao_em_lista_vazia_retorna_none(
        self,
    ):
        """
        Busca em coleção vazia deve
        retornar None.
        """

        resultado = (
            buscar_solicitacao_servico_por_codigo(
                [],
                1,
            )
        )

        self.assertIsNone(
            resultado
        )

    def test_buscar_solicitacao_exige_codigo_valido(
        self,
    ):
        """
        Código utilizado na busca deve
        ser inteiro positivo.
        """

        for codigo in (
            0,
            -1,
            1.5,
            "1",
            True,
        ):
            with self.subTest(
                codigo=codigo
            ):
                with self.assertRaises(
                    ValorInvalido
                ):
                    buscar_solicitacao_servico_por_codigo(
                        [],
                        codigo,
                    )

    def test_listar_solicitacoes_por_cliente(
        self,
    ):
        """
        Deve retornar apenas Solicitações
        do Cliente informado.
        """

        cliente_2 = {
            "codigo": 2,
            "nome": "Outro Cliente",
        }

        solicitacao_1 = criar_solicitacao_servico(
            codigo=1,
            cliente=self.cliente,
            tipo_servico=self.tipo_servico,
            modalidade="ABERTA",
            origem="CLIENTE",
            municipio="Caetité",
            uf="BA",
            dados_tecnicos={},
        )

        solicitacao_2 = criar_solicitacao_servico(
            codigo=2,
            cliente=cliente_2,
            tipo_servico=self.tipo_servico,
            modalidade="ABERTA",
            origem="CLIENTE",
            municipio="Caetité",
            uf="BA",
            dados_tecnicos={},
        )

        resultado = listar_solicitacoes_por_cliente(
            [
                solicitacao_1,
                solicitacao_2,
            ],
            1,
        )

        self.assertEqual(
            resultado,
            [
                solicitacao_1,
            ],
        )

    def test_listar_solicitacoes_por_cliente_sem_resultado(
        self,
    ):
        """
        Consulta sem correspondências
        deve retornar lista vazia.
        """

        resultado = listar_solicitacoes_por_cliente(
            [],
            1,
        )

        self.assertEqual(
            resultado,
            [],
        )

    def test_listar_solicitacoes_por_tipo_servico(
        self,
    ):
        """
        Deve filtrar pelo Tipo de Serviço.
        """

        outro_tipo = criar_tipo_servico(
            codigo=2,
            nome="Manutenção Corretiva",
            categoria="MANUTENCAO_CORRETIVA",
            origem="PADRAO_PLATAFORMA",
            fluxo_operacional=(
                "ORDEM_SERVICO_POS_VENDA"
            ),
        )

        solicitacao_1 = criar_solicitacao_servico(
            codigo=1,
            cliente=self.cliente,
            tipo_servico=self.tipo_servico,
            modalidade="ABERTA",
            origem="CLIENTE",
            municipio="Caetité",
            uf="BA",
            dados_tecnicos={},
        )

        solicitacao_2 = criar_solicitacao_servico(
            codigo=2,
            cliente=self.cliente,
            tipo_servico=outro_tipo,
            modalidade="ABERTA",
            origem="CLIENTE",
            municipio="Caetité",
            uf="BA",
            dados_tecnicos={},
        )

        resultado = (
            listar_solicitacoes_por_tipo_servico(
                [
                    solicitacao_1,
                    solicitacao_2,
                ],
                2,
            )
        )

        self.assertEqual(
            resultado,
            [
                solicitacao_2,
            ],
        )

    def test_listar_solicitacoes_diretas_por_empresa(
        self,
    ):
        """
        Deve retornar somente Solicitações DIRETAS
        destinadas à Empresa informada.
        """

        solicitacao_direta = criar_solicitacao_servico(
            codigo=1,
            cliente=self.cliente,
            tipo_servico=self.tipo_servico,
            modalidade="DIRETA",
            origem="CLIENTE",
            municipio="Caetité",
            uf="BA",
            dados_tecnicos={},
            servico_ofertado=(
                self.servico_ofertado
            ),
        )

        solicitacao_aberta = criar_solicitacao_servico(
            codigo=2,
            cliente=self.cliente,
            tipo_servico=self.tipo_servico,
            modalidade="ABERTA",
            origem="CLIENTE",
            municipio="Caetité",
            uf="BA",
            dados_tecnicos={},
        )

        resultado = (
            listar_solicitacoes_diretas_por_empresa(
                [
                    solicitacao_direta,
                    solicitacao_aberta,
                ],
                self.empresa["codigo"],
            )
        )

        self.assertEqual(
            resultado,
            [
                solicitacao_direta,
            ],
        )

    def test_consultas_relacionais_exigem_codigo_valido(
        self,
    ):
        """
        Filtros relacionais devem exigir
        identificadores inteiros positivos.
        """

        funcoes = (
            listar_solicitacoes_por_cliente,
            listar_solicitacoes_por_tipo_servico,
            listar_solicitacoes_diretas_por_empresa,
        )

        for funcao in funcoes:
            for codigo in (
                0,
                -1,
                "1",
                1.5,
                True,
            ):
                with self.subTest(
                    funcao=funcao.__name__,
                    codigo=codigo,
                ):
                    with self.assertRaises(
                        ValorInvalido
                    ):
                        funcao(
                            [],
                            codigo,
                        )

    def test_listar_solicitacoes_por_modalidade(
        self,
    ):
        """
        Deve retornar somente Solicitações
        da modalidade informada.
        """

        solicitacao_aberta = criar_solicitacao_servico(
            codigo=1,
            cliente=self.cliente,
            tipo_servico=self.tipo_servico,
            modalidade="ABERTA",
            origem="CLIENTE",
            municipio="Caetité",
            uf="BA",
            dados_tecnicos={},
        )

        solicitacao_direta = criar_solicitacao_servico(
            codigo=2,
            cliente=self.cliente,
            tipo_servico=self.tipo_servico,
            modalidade="DIRETA",
            origem="CLIENTE",
            municipio="Caetité",
            uf="BA",
            dados_tecnicos={},
            servico_ofertado=(
                self.servico_ofertado
            ),
        )

        resultado = listar_solicitacoes_por_modalidade(
            [
                solicitacao_aberta,
                solicitacao_direta,
            ],
            "ABERTA",
        )

        self.assertEqual(
            resultado,
            [
                solicitacao_aberta,
            ],
        )

    def test_listar_por_modalidade_aceita_enum(
        self,
    ):
        """
        Consulta deve aceitar diretamente
        ModalidadeSolicitacaoServico.
        """

        solicitacao = criar_solicitacao_servico(
            codigo=1,
            cliente=self.cliente,
            tipo_servico=self.tipo_servico,
            modalidade="ABERTA",
            origem="CLIENTE",
            municipio="Caetité",
            uf="BA",
            dados_tecnicos={},
        )

        resultado = listar_solicitacoes_por_modalidade(
            [
                solicitacao,
            ],
            ModalidadeSolicitacaoServico.ABERTA,
        )

        self.assertEqual(
            resultado,
            [
                solicitacao,
            ],
        )

    def test_listar_por_modalidade_invalida_deve_ser_rejeitada(
        self,
    ):
        """
        Consulta deve rejeitar modalidade
        inexistente no domínio.
        """

        with self.assertRaises(
            ValorInvalido
        ):
            listar_solicitacoes_por_modalidade(
                [],
                "QUALQUER",
            )

    def test_listar_solicitacoes_por_status(
        self,
    ):
        """
        Deve retornar somente Solicitações
        que estejam no status informado.
        """

        em_elaboracao = criar_solicitacao_servico(
            codigo=1,
            cliente=self.cliente,
            tipo_servico=self.tipo_servico,
            modalidade="ABERTA",
            origem="CLIENTE",
            municipio="Caetité",
            uf="BA",
            dados_tecnicos={},
        )

        publicada = criar_solicitacao_servico(
            codigo=2,
            cliente=self.cliente,
            tipo_servico=self.tipo_servico,
            modalidade="ABERTA",
            origem="CLIENTE",
            municipio="Caetité",
            uf="BA",
            dados_tecnicos={},
        )

        alterar_status_solicitacao_servico(
            publicada,
            "PUBLICADA",
        )

        resultado = listar_solicitacoes_por_status(
            [
                em_elaboracao,
                publicada,
            ],
            "PUBLICADA",
        )

        self.assertEqual(
            resultado,
            [
                publicada,
            ],
        )

    def test_listar_por_status_normaliza_valor(
        self,
    ):
        """
        Consulta por status deve normalizar
        espaços externos e caixa.
        """

        solicitacao = criar_solicitacao_servico(
            codigo=1,
            cliente=self.cliente,
            tipo_servico=self.tipo_servico,
            modalidade="ABERTA",
            origem="CLIENTE",
            municipio="Caetité",
            uf="BA",
            dados_tecnicos={},
        )

        alterar_status_solicitacao_servico(
            solicitacao,
            "PUBLICADA",
        )

        resultado = listar_solicitacoes_por_status(
            [
                solicitacao,
            ],
            "  publicada  ",
        )

        self.assertEqual(
            resultado,
            [
                solicitacao,
            ],
        )

    def test_listar_por_status_invalido_deve_ser_rejeitado(
        self,
    ):
        """
        Consulta deve rejeitar status
        inexistente no catálogo oficial.
        """

        with self.assertRaises(
            ValorInvalido
        ):
            listar_solicitacoes_por_status(
                [],
                "STATUS_INVENTADO",
            )

    def test_consultas_por_classificacao_sem_resultado(
        self,
    ):
        """
        Consultas válidas sem correspondências
        devem retornar lista vazia.
        """

        resultado_modalidade = (
            listar_solicitacoes_por_modalidade(
                [],
                "ABERTA",
            )
        )

        resultado_status = (
            listar_solicitacoes_por_status(
                [],
                "PUBLICADA",
            )
        )

        self.assertEqual(
            resultado_modalidade,
            [],
        )

        self.assertEqual(
            resultado_status,
            [],
        )

    def test_consultas_multiplas_retornam_nova_lista(
        self,
    ):
        """
        Consultas múltiplas devem retornar
        nova coleção, sem reutilizar a recebida.
        """

        solicitacao = criar_solicitacao_servico(
            codigo=1,
            cliente=self.cliente,
            tipo_servico=self.tipo_servico,
            modalidade="ABERTA",
            origem="CLIENTE",
            municipio="Caetité",
            uf="BA",
            dados_tecnicos={},
        )

        solicitacoes = [
            solicitacao,
        ]

        consultas = (
            (
                listar_solicitacoes_por_cliente,
                self.cliente["codigo"],
            ),
            (
                listar_solicitacoes_por_tipo_servico,
                self.tipo_servico.codigo,
            ),
            (
                listar_solicitacoes_por_modalidade,
                "ABERTA",
            ),
            (
                listar_solicitacoes_por_status,
                "EM_ELABORACAO",
            ),
        )

        for funcao, criterio in consultas:
            with self.subTest(
                funcao=funcao.__name__,
            ):
                resultado = funcao(
                    solicitacoes,
                    criterio,
                )

                self.assertIsNot(
                    resultado,
                    solicitacoes,
                )

                self.assertEqual(
                    resultado,
                    solicitacoes,
                )

    def test_consulta_direta_por_empresa_retorna_nova_lista(
        self,
    ):
        """
        Consulta DIRETA por Empresa deve
        construir nova coleção.
        """

        solicitacao = criar_solicitacao_servico(
            codigo=1,
            cliente=self.cliente,
            tipo_servico=self.tipo_servico,
            modalidade="DIRETA",
            origem="CLIENTE",
            municipio="Caetité",
            uf="BA",
            dados_tecnicos={},
            servico_ofertado=(
                self.servico_ofertado
            ),
        )

        solicitacoes = [
            solicitacao,
        ]

        resultado = (
            listar_solicitacoes_diretas_por_empresa(
                solicitacoes,
                self.empresa["codigo"],
            )
        )

        self.assertIsNot(
            resultado,
            solicitacoes,
        )

        self.assertEqual(
            resultado,
            solicitacoes,
        )

    def test_consultas_nao_alteram_ordem_original(
        self,
    ):
        """
        Consultas não devem reordenar
        a coleção recebida.
        """

        solicitacao_1 = criar_solicitacao_servico(
            codigo=3,
            cliente=self.cliente,
            tipo_servico=self.tipo_servico,
            modalidade="ABERTA",
            origem="CLIENTE",
            municipio="Caetité",
            uf="BA",
            dados_tecnicos={},
        )

        solicitacao_2 = criar_solicitacao_servico(
            codigo=1,
            cliente=self.cliente,
            tipo_servico=self.tipo_servico,
            modalidade="ABERTA",
            origem="CLIENTE",
            municipio="Caetité",
            uf="BA",
            dados_tecnicos={},
        )

        solicitacao_3 = criar_solicitacao_servico(
            codigo=2,
            cliente=self.cliente,
            tipo_servico=self.tipo_servico,
            modalidade="ABERTA",
            origem="CLIENTE",
            municipio="Caetité",
            uf="BA",
            dados_tecnicos={},
        )

        solicitacoes = [
            solicitacao_1,
            solicitacao_2,
            solicitacao_3,
        ]

        ordem_original = [
            solicitacao.codigo
            for solicitacao in solicitacoes
        ]

        listar_solicitacoes_por_cliente(
            solicitacoes,
            self.cliente["codigo"],
        )

        listar_solicitacoes_por_tipo_servico(
            solicitacoes,
            self.tipo_servico.codigo,
        )

        listar_solicitacoes_por_modalidade(
            solicitacoes,
            "ABERTA",
        )

        listar_solicitacoes_por_status(
            solicitacoes,
            "EM_ELABORACAO",
        )

        ordem_posterior = [
            solicitacao.codigo
            for solicitacao in solicitacoes
        ]

        self.assertEqual(
            ordem_posterior,
            ordem_original,
        )

    def test_consultas_nao_alteram_entidades(
        self,
    ):
        """
        Operações de consulta não devem
        modificar as Solicitações consultadas.
        """

        solicitacao = criar_solicitacao_servico(
            codigo=1,
            cliente=self.cliente,
            tipo_servico=self.tipo_servico,
            modalidade="ABERTA",
            origem="CLIENTE",
            municipio="Caetité",
            uf="BA",
            dados_tecnicos={
                "quantidade_modulos": 20,
            },
        )

        estado_antes = (
            converter_solicitacao_servico_para_dicionario(
                solicitacao
            )
        )

        solicitacoes = [
            solicitacao,
        ]

        buscar_solicitacao_servico_por_codigo(
            solicitacoes,
            1,
        )

        listar_solicitacoes_por_cliente(
            solicitacoes,
            self.cliente["codigo"],
        )

        listar_solicitacoes_por_tipo_servico(
            solicitacoes,
            self.tipo_servico.codigo,
        )

        listar_solicitacoes_por_modalidade(
            solicitacoes,
            "ABERTA",
        )

        listar_solicitacoes_por_status(
            solicitacoes,
            "EM_ELABORACAO",
        )

        estado_depois = (
            converter_solicitacao_servico_para_dicionario(
                solicitacao
            )
        )

        self.assertEqual(
            estado_depois,
            estado_antes,
        )

    def test_consulta_preserva_identidade_das_entidades(
        self,
    ):
        """
        A coleção retornada deve ser nova,
        mas suas entidades não devem ser copiadas.
        """

        solicitacao = criar_solicitacao_servico(
            codigo=1,
            cliente=self.cliente,
            tipo_servico=self.tipo_servico,
            modalidade="ABERTA",
            origem="CLIENTE",
            municipio="Caetité",
            uf="BA",
            dados_tecnicos={},
        )

        solicitacoes = [
            solicitacao,
        ]

        resultado = listar_solicitacoes_por_cliente(
            solicitacoes,
            self.cliente["codigo"],
        )

        self.assertIsNot(
            resultado,
            solicitacoes,
        )

        self.assertIs(
            resultado[0],
            solicitacao,
        )

    def test_consultas_sucessivas_sao_consistentes(
        self,
    ):
        """
        Repetir a mesma consulta sem alteração
        do domínio deve produzir o mesmo resultado.
        """

        solicitacao = criar_solicitacao_servico(
            codigo=1,
            cliente=self.cliente,
            tipo_servico=self.tipo_servico,
            modalidade="ABERTA",
            origem="CLIENTE",
            municipio="Caetité",
            uf="BA",
            dados_tecnicos={},
        )

        solicitacoes = [
            solicitacao,
        ]

        resultado_1 = listar_solicitacoes_por_cliente(
            solicitacoes,
            self.cliente["codigo"],
        )

        resultado_2 = listar_solicitacoes_por_cliente(
            solicitacoes,
            self.cliente["codigo"],
        )

        self.assertEqual(
            resultado_1,
            resultado_2,
        )

        self.assertIsNot(
            resultado_1,
            resultado_2,
        )

    def test_alterar_lista_resultado_nao_altera_colecao_original(
        self,
    ):
        """
        Alterar estruturalmente a lista retornada
        não deve modificar a coleção consultada.
        """

        solicitacao = criar_solicitacao_servico(
            codigo=1,
            cliente=self.cliente,
            tipo_servico=self.tipo_servico,
            modalidade="ABERTA",
            origem="CLIENTE",
            municipio="Caetité",
            uf="BA",
            dados_tecnicos={},
        )

        solicitacoes = [
            solicitacao,
        ]

        resultado = listar_solicitacoes_por_cliente(
            solicitacoes,
            self.cliente["codigo"],
        )

        resultado.clear()

        self.assertEqual(
            resultado,
            [],
        )

        self.assertEqual(
            solicitacoes,
            [
                solicitacao,
            ],
        )



if __name__ == "__main__":
    unittest.main()