"""
Regras de domínio relacionadas aos Orçamentos.

Este módulo não utiliza:

- input();
- print();
- arquivos JSON;
- funções de interface.

As funções recebem dados e retornam resultados.
"""


def buscar_orcamento_por_codigo(orcamentos, codigo):
    """
    Busca um Orçamento pelo código.

    Parâmetros:
        orcamentos:
            Coleção de Orçamentos cadastrados.

        codigo:
            Código do Orçamento procurado.

    Retorna:
        O Orçamento encontrado ou None.
    """

    for orcamento in orcamentos:

        if orcamento["codigo"] == codigo:
            return orcamento

    return None


def codigo_orcamento_existe(orcamentos, codigo):
    """
    Verifica se já existe um Orçamento
    com o código informado.
    """

    return (
        buscar_orcamento_por_codigo(
            orcamentos,
            codigo,
        )
        is not None
    )


def criar_dados_orcamento(
    codigo,
    codigo_cliente,
    dimensionamento,
    modulos,
    inversores,
    local_instalacao,
    comercial,
    status_inicial,
):
    """
    Cria e retorna os dados de um novo Orçamento.

    Esta função não altera a coleção recebida,
    não salva arquivos e não interage com o terminal.
    """

    return {
        "codigo": codigo,
        "cliente": codigo_cliente,
        "dimensionamento": dimensionamento.copy(),
        "modulos": modulos.copy(),
        "inversores": inversores.copy(),
        "local_instalacao": local_instalacao.copy(),
        "comercial": comercial.copy(),
        "status": status_inicial,
    }


def orcamento_pode_ser_convertido(orcamento):
    """
    Verifica se um Orçamento pode ser convertido
    em Projeto.

    Neste estágio, apenas Orçamentos aprovados
    podem ser convertidos.
    """

    return orcamento["status"] == "Aprovado"