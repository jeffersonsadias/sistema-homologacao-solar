import unittest

from app.dominio.painel_gerencial import (
    calcular_taxa_conclusao,
    calcular_tempo_medio_conclusao,
    calcular_visao_geral,
    contar_exigencias_abertas,
    contar_instalacoes_aguardando_execucao,
    contar_ligacoes_aguardando_conclusao,
    contar_projetos_por_concessionaria,
    contar_projetos_por_empresa,
    contar_vistorias_aguardando_resultado,
    gerar_indicadores_painel_gerencial,
)

from app.dominio.status_homologacao import (
    StatusHomologacao,
)


class TestPainelGerencialDominio(
    unittest.TestCase
):
    """
    Testes das regras de domínio
    do Painel Gerencial.
    """

    def test_visao_geral_sem_dados(
        self,
    ):
        """
        Coleções vazias devem produzir
        todos os indicadores zerados.
        """

        resultado = calcular_visao_geral(
            projetos=[],
            homologacoes=[],
        )

        esperado = {
            "total_projetos": 0,
            "total_homologacoes": 0,
            "homologacoes_em_andamento": 0,
            "homologacoes_concluidas": 0,
            "homologacoes_encerradas_sem_conclusao": 0,
        }

        self.assertEqual(
            resultado,
            esperado,
        )

    def test_deve_calcular_visao_geral(
        self,
    ):
        """
        Deve contabilizar Projetos e classificar
        as Homologações conforme seu estado.
        """

        projetos = [
            {"codigo": 1},
            {"codigo": 2},
            {"codigo": 3},
            {"codigo": 4},
        ]

        homologacoes = [
            {
                "codigo": 1,
                "status": (
                    StatusHomologacao
                    .EM_ANALISE
                    .value
                ),
            },
            {
                "codigo": 2,
                "status": (
                    StatusHomologacao
                    .AGUARDANDO_INSTALACAO
                    .value
                ),
            },
            {
                "codigo": 3,
                "status": (
                    StatusHomologacao
                    .CONCLUIDA
                    .value
                ),
            },
            {
                "codigo": 4,
                "status": (
                    StatusHomologacao
                    .CONCLUIDA
                    .value
                ),
            },
            {
                "codigo": 5,
                "status": (
                    StatusHomologacao
                    .REJEITADA
                    .value
                ),
            },
            {
                "codigo": 6,
                "status": (
                    StatusHomologacao
                    .CANCELADA
                    .value
                ),
            },
        ]

        resultado = calcular_visao_geral(
            projetos=projetos,
            homologacoes=homologacoes,
        )

        self.assertEqual(
            resultado["total_projetos"],
            4,
        )

        self.assertEqual(
            resultado["total_homologacoes"],
            6,
        )

        self.assertEqual(
            resultado[
                "homologacoes_em_andamento"
            ],
            2,
        )

        self.assertEqual(
            resultado[
                "homologacoes_concluidas"
            ],
            2,
        )

        self.assertEqual(
            resultado[
                "homologacoes_encerradas_sem_conclusao"
            ],
            2,
        )

    def test_classificacao_deve_corresponder_ao_total(
        self,
    ):
        """
        A soma das categorias deve corresponder
        ao total de Homologações.
        """

        homologacoes = [
            {
                "status": (
                    StatusHomologacao
                    .EM_ANALISE
                    .value
                ),
            },
            {
                "status": (
                    StatusHomologacao
                    .CONCLUIDA
                    .value
                ),
            },
            {
                "status": (
                    StatusHomologacao
                    .REJEITADA
                    .value
                ),
            },
        ]

        resultado = calcular_visao_geral(
            projetos=[],
            homologacoes=homologacoes,
        )

        total_classificado = (
            resultado[
                "homologacoes_em_andamento"
            ]
            + resultado[
                "homologacoes_concluidas"
            ]
            + resultado[
                "homologacoes_encerradas_sem_conclusao"
            ]
        )

        self.assertEqual(
            total_classificado,
            resultado["total_homologacoes"],
        )

    def test_taxa_conclusao_sem_homologacoes(
        self,
    ):
        """
        Sem Homologações, a taxa de
        conclusão deve ser zero.
        """

        resultado = calcular_taxa_conclusao(
            []
        )

        self.assertEqual(
            resultado,
            0.0,
        )

    def test_deve_calcular_taxa_conclusao(
        self,
    ):
        """
        Deve calcular o percentual de
        Homologações concluídas.
        """

        homologacoes = [
            {
                "status": (
                    StatusHomologacao
                    .CONCLUIDA
                    .value
                ),
            },
            {
                "status": (
                    StatusHomologacao
                    .CONCLUIDA
                    .value
                ),
            },
            {
                "status": (
                    StatusHomologacao
                    .EM_ANALISE
                    .value
                ),
            },
            {
                "status": (
                    StatusHomologacao
                    .CANCELADA
                    .value
                ),
            },
        ]

        resultado = calcular_taxa_conclusao(
            homologacoes
        )

        self.assertEqual(
            resultado,
            50.0,
        )

    def test_tempo_medio_sem_homologacoes_concluidas(
        self,
    ):
        """
        Sem Homologações concluídas,
        o tempo médio deve ser zero.
        """

        homologacoes = [
            {
                "status": (
                    StatusHomologacao
                    .EM_ANALISE
                    .value
                ),
                "data_abertura": "2026-08-01",
                "data_conclusao_real": None,
            },
        ]

        resultado = (
            calcular_tempo_medio_conclusao(
                homologacoes
            )
        )

        self.assertEqual(
            resultado,
            0.0,
        )

    def test_deve_calcular_tempo_medio_conclusao(
        self,
    ):
        """
        Deve calcular a média de dias
        entre abertura e conclusão.
        """

        homologacoes = [
            {
                "status": (
                    StatusHomologacao
                    .CONCLUIDA
                    .value
                ),
                "data_abertura": "2026-07-01",
                "data_conclusao_real": (
                    "2026-07-11"
                ),
            },
            {
                "status": (
                    StatusHomologacao
                    .CONCLUIDA
                    .value
                ),
                "data_abertura": "2026-07-01",
                "data_conclusao_real": (
                    "2026-07-21"
                ),
            },
        ]

        resultado = (
            calcular_tempo_medio_conclusao(
                homologacoes
            )
        )

        self.assertEqual(
            resultado,
            15.0,
        )

    def test_tempo_medio_deve_ignorar_homologacoes_em_andamento(
        self,
    ):
        """
        Homologações ainda em andamento
        não devem participar do cálculo.
        """

        homologacoes = [
            {
                "status": (
                    StatusHomologacao
                    .CONCLUIDA
                    .value
                ),
                "data_abertura": "2026-07-01",
                "data_conclusao_real": (
                    "2026-07-11"
                ),
            },
            {
                "status": (
                    StatusHomologacao
                    .EM_ANALISE
                    .value
                ),
                "data_abertura": "2026-01-01",
                "data_conclusao_real": None,
            },
        ]

        resultado = (
            calcular_tempo_medio_conclusao(
                homologacoes
            )
        )

        self.assertEqual(
            resultado,
            10.0,
        )

    def test_deve_contar_projetos_por_empresa(
        self,
    ):
        """
        Deve agrupar os Projetos
        pelo código da Empresa.
        """

        projetos = [
            {
                "codigo": 1,
                "codigo_empresa": 10,
            },
            {
                "codigo": 2,
                "codigo_empresa": 10,
            },
            {
                "codigo": 3,
                "codigo_empresa": 20,
            },
            {
                "codigo": 4,
                "codigo_empresa": 10,
            },
        ]

        resultado = contar_projetos_por_empresa(
            projetos
        )

        self.assertEqual(
            resultado,
            {
                10: 3,
                20: 1,
            },
        )

    def test_distribuicao_empresa_deve_ignorar_codigo_ausente(
        self,
    ):
        """
        Projetos sem código de Empresa
        não devem criar uma categoria inválida.
        """

        projetos = [
            {
                "codigo": 1,
                "codigo_empresa": 10,
            },
            {
                "codigo": 2,
            },
        ]

        resultado = contar_projetos_por_empresa(
            projetos
        )

        self.assertEqual(
            resultado,
            {
                10: 1,
            },
        )

    def test_deve_contar_projetos_por_concessionaria(
        self,
    ):
        """
        Deve agrupar os Projetos pelo
        código da Concessionária.
        """

        projetos = [
            {
                "codigo": 1,
                "codigo_concessionaria": 100,
            },
            {
                "codigo": 2,
                "codigo_concessionaria": 100,
            },
            {
                "codigo": 3,
                "codigo_concessionaria": 200,
            },
        ]

        resultado = (
            contar_projetos_por_concessionaria(
                projetos
            )
        )

        self.assertEqual(
            resultado,
            {
                100: 2,
                200: 1,
            },
        )

    def test_distribuicao_concessionaria_deve_ignorar_codigo_ausente(
        self,
    ):
        """
        Projetos sem código de Concessionária
        não devem criar categoria inválida.
        """

        projetos = [
            {
                "codigo": 1,
                "codigo_concessionaria": 100,
            },
            {
                "codigo": 2,
                "codigo_concessionaria": None,
            },
        ]

        resultado = (
            contar_projetos_por_concessionaria(
                projetos
            )
        )

        self.assertEqual(
            resultado,
            {
                100: 1,
            },
        )

    def test_distribuicoes_sem_projetos(
        self,
    ):
        """
        Sem Projetos, as distribuições
        devem ser vazias.
        """

        self.assertEqual(
            contar_projetos_por_empresa([]),
            {},
        )

        self.assertEqual(
            contar_projetos_por_concessionaria(
                []
            ),
            {},
        )

    def test_deve_contar_instalacoes_aguardando_execucao(
        self,
    ):
        homologacoes = [
            {
                "operacoes_campo": {
                    "instalacao": {
                        "status": "PLANEJADA",
                    }
                }
            },
            {
                "operacoes_campo": {
                    "instalacao": {
                        "status": "EM_EXECUCAO",
                    }
                }
            },
            {
                "operacoes_campo": {
                    "instalacao": {
                        "status": "PLANEJADA",
                    }
                }
            },
        ]

        resultado = (
            contar_instalacoes_aguardando_execucao(
                homologacoes
            )
        )

        self.assertEqual(
            resultado,
            2,
        )

    def test_deve_contar_vistorias_aguardando_resultado(
        self,
    ):
        homologacoes = [
            {
                "operacoes_campo": {
                    "vistorias": [
                        {
                            "status": "REALIZADA",
                        }
                    ]
                }
            },
            {
                "operacoes_campo": {
                    "vistorias": [
                        {
                            "status": "APROVADA",
                        }
                    ]
                }
            },
            {
                "operacoes_campo": {
                    "vistorias": [
                        {
                            "status": "REALIZADA",
                        },
                        {
                            "status": "REPROVADA",
                        },
                    ]
                }
            },
        ]

        resultado = (
            contar_vistorias_aguardando_resultado(
                homologacoes
            )
        )

        self.assertEqual(
            resultado,
            2,
        )

    def test_deve_contar_ligacoes_aguardando_conclusao(
        self,
    ):
        homologacoes = [
            {
                "operacoes_campo": {
                    "ligacao": {
                        "status": "SOLICITADA",
                    }
                }
            },
            {
                "operacoes_campo": {
                    "ligacao": {
                        "status": "AGENDADA",
                    }
                }
            },
            {
                "operacoes_campo": {
                    "ligacao": {
                        "status": "CONCLUIDA",
                    }
                }
            },
        ]

        resultado = (
            contar_ligacoes_aguardando_conclusao(
                homologacoes
            )
        )

        self.assertEqual(
            resultado,
            2,
        )

    def test_deve_contar_homologacoes_com_exigencias_abertas(
        self,
    ):
        homologacoes = [
            {
                "submissoes": [
                    {
                        "respostas": [
                            {
                                "exigencias": [
                                    {
                                        "status_atendimento": (
                                            "PENDENTE"
                                        )
                                    }
                                ]
                            }
                        ]
                    }
                ]
            },
            {
                "submissoes": [
                    {
                        "respostas": [
                            {
                                "exigencias": [
                                    {
                                        "status_atendimento": (
                                            "ATENDIDA"
                                        )
                                    }
                                ]
                            }
                        ]
                    }
                ]
            },
            {
                "submissoes": [
                    {
                        "respostas": [
                            {
                                "exigencias": [
                                    {
                                        "status_atendimento": (
                                            "PENDENTE"
                                        )
                                    },
                                    {
                                        "status_atendimento": (
                                            "PENDENTE"
                                        )
                                    },
                                ]
                            }
                        ]
                    }
                ]
            },
        ]

        resultado = contar_exigencias_abertas(
            homologacoes
        )

        self.assertEqual(
            resultado,
            2,
        )

    def test_indicadores_operacionais_devem_aceitar_dados_ausentes(
        self,
    ):
        homologacoes = [
            {},
            {
                "operacoes_campo": None,
            },
            {
                "operacoes_campo": {},
            },
        ]

        self.assertEqual(
            contar_instalacoes_aguardando_execucao(
                homologacoes
            ),
            0,
        )

        self.assertEqual(
            contar_vistorias_aguardando_resultado(
                homologacoes
            ),
            0,
        )

        self.assertEqual(
            contar_ligacoes_aguardando_conclusao(
                homologacoes
            ),
            0,
        )

    def test_deve_gerar_indicadores_consolidados(
        self,
    ):
        """
        Deve consolidar todos os grupos
        do Painel Gerencial.
        """

        projetos = [
            {
                "codigo": 1,
                "codigo_empresa": 10,
                "codigo_concessionaria": 100,
            },
            {
                "codigo": 2,
                "codigo_empresa": 10,
                "codigo_concessionaria": 200,
            },
            {
                "codigo": 3,
                "codigo_empresa": 20,
                "codigo_concessionaria": 100,
            },
        ]

        homologacoes = [
            {
                "status": (
                    StatusHomologacao
                    .CONCLUIDA
                    .value
                ),
                "data_abertura": "2026-07-01",
                "data_conclusao_real": (
                    "2026-07-11"
                ),
                "submissoes": [],
                "operacoes_campo": {
                    "instalacao": {
                        "status": "CONCLUIDA",
                    },
                    "vistorias": [
                        {
                            "status": "APROVADA",
                        }
                    ],
                    "ligacao": {
                        "status": "CONCLUIDA",
                    },
                },
            },
            {
                "status": (
                    StatusHomologacao
                    .AGUARDANDO_INSTALACAO
                    .value
                ),
                "data_abertura": "2026-08-01",
                "data_conclusao_real": None,
                "submissoes": [],
                "operacoes_campo": {
                    "instalacao": {
                        "status": "PLANEJADA",
                    },
                    "vistorias": [],
                    "ligacao": None,
                },
            },
            {
                "status": (
                    StatusHomologacao
                    .AGUARDANDO_LIGACAO
                    .value
                ),
                "data_abertura": "2026-08-01",
                "data_conclusao_real": None,
                "submissoes": [],
                "operacoes_campo": {
                    "instalacao": {
                        "status": "CONCLUIDA",
                    },
                    "vistorias": [
                        {
                            "status": "REALIZADA",
                        }
                    ],
                    "ligacao": {
                        "status": "AGENDADA",
                    },
                },
            },
        ]

        resultado = (
            gerar_indicadores_painel_gerencial(
                projetos=projetos,
                homologacoes=homologacoes,
            )
        )

        self.assertEqual(
            resultado["visao_geral"][
                "total_projetos"
            ],
            3,
        )

        self.assertEqual(
            resultado["visao_geral"][
                "total_homologacoes"
            ],
            3,
        )

        self.assertEqual(
            resultado["visao_geral"][
                "homologacoes_concluidas"
            ],
            1,
        )

        self.assertAlmostEqual(
            resultado["desempenho"][
                "taxa_conclusao"
            ],
            33.33333333333333,
        )

        self.assertEqual(
            resultado["desempenho"][
                "tempo_medio_conclusao_dias"
            ],
            10.0,
        )

        self.assertEqual(
            resultado["distribuicao"][
                "projetos_por_empresa"
            ],
            {
                10: 2,
                20: 1,
            },
        )

        self.assertEqual(
            resultado["distribuicao"][
                "projetos_por_concessionaria"
            ],
            {
                100: 2,
                200: 1,
            },
        )

        self.assertEqual(
            resultado["operacoes_campo"][
                "instalacoes_aguardando_execucao"
            ],
            1,
        )

        self.assertEqual(
            resultado["operacoes_campo"][
                "vistorias_aguardando_resultado"
            ],
            1,
        )

        self.assertEqual(
            resultado["operacoes_campo"][
                "ligacoes_aguardando_conclusao"
            ],
            1,
        )

    def test_indicadores_consolidados_sem_dados(
        self,
    ):
        """
        O Painel Gerencial deve possuir
        estrutura válida mesmo sem dados.
        """

        resultado = (
            gerar_indicadores_painel_gerencial(
                projetos=[],
                homologacoes=[],
            )
        )

        self.assertEqual(
            resultado["visao_geral"][
                "total_projetos"
            ],
            0,
        )

        self.assertEqual(
            resultado["desempenho"][
                "taxa_conclusao"
            ],
            0.0,
        )

        self.assertEqual(
            resultado["desempenho"][
                "tempo_medio_conclusao_dias"
            ],
            0.0,
        )

        self.assertEqual(
            resultado["distribuicao"][
                "projetos_por_empresa"
            ],
            {},
        )

        self.assertEqual(
            resultado["distribuicao"][
                "projetos_por_concessionaria"
            ],
            {},
        )

        self.assertEqual(
            resultado["operacoes_campo"][
                "instalacoes_aguardando_execucao"
            ],
            0,
        )


