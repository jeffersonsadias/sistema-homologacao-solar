"""
Regras puras do domínio de Projetos.

Este módulo não utiliza:

- input();
- print();
- arquivos JSON;
- coleções globais;
- módulos de interface.

As funções recebem os dados necessários e retornam resultados.
"""


def buscar_projeto_por_codigo(projetos, codigo):
    """
    Busca um Projeto pelo código informado.

    Parâmetros:
        projetos:
            Coleção de Projetos cadastrados.

        codigo:
            Código do Projeto procurado.

    Retorno:
        O Projeto encontrado ou None.
    """

    for projeto in projetos:
        if projeto["codigo"] == codigo:
            return projeto

    return None

def buscar_projetos_por_cliente(
    projetos,
    codigo_cliente,
):
    """
    Retorna todos os Projetos vinculados
    ao Cliente informado.

    A função retorna uma nova lista e não altera
    a coleção recebida.
    """

    return [
        projeto
        for projeto in projetos
        if projeto.get("cliente") == codigo_cliente
    ]

def codigo_projeto_existe(projetos, codigo):
    """
    Verifica se já existe um Projeto com o código informado.

    Retorna:
        True quando o código existir.
        False quando o código não existir.
    """

    return buscar_projeto_por_codigo(
        projetos,
        codigo,
    ) is not None

def quantidade_projetos_por_status(
    projetos,
    status,
):
    """
    Retorna a quantidade de Projetos que possuem
    exatamente o status informado.

    A função não altera a coleção recebida.
    """

    return sum(
        1
        for projeto in projetos
        if projeto.get("status") == status
    )

def buscar_projetos_por_status(
    projetos,
    status,
):
    """
    Retorna os Projetos que possuem
    exatamente o status informado.

    A função retorna uma nova lista e não altera
    a coleção recebida.
    """

    return [
        projeto
        for projeto in projetos
        if projeto.get("status") == status
    ]

def criar_dados_projeto(
    codigo,
    codigo_cliente,
    distribuidora,
    potencia,
    status_inicial,
):
    """
    Cria os dados básicos de um novo Projeto.

    Esta função apenas monta e retorna o dicionário.
    Ela não adiciona o Projeto a uma lista e não salva arquivos.
    """

    return {
        "codigo": codigo,
        "cliente": codigo_cliente,
        "distribuidora": distribuidora,
        "potencia": potencia,
        "status": status_inicial,
    }


def criar_dados_projeto_a_partir_do_orcamento(
    codigo,
    orcamento,
    status_inicial,
):
    """
    Cria os dados de um Projeto a partir de um Orçamento aprovado.

    Esta função não altera o Orçamento recebido,
    não adiciona o Projeto a coleções e não salva arquivos.
    """

    return {
        "codigo": codigo,
        "cliente": orcamento["cliente"],
        "orcamento_origem": orcamento["codigo"],
        "distribuidora": (
            orcamento["local_instalacao"]["distribuidora"]
        ),
        "potencia": (
            orcamento["dimensionamento"][
                "potencia_prevista_kwp"
            ]
        ),
        "codigo_uc": (
            orcamento["local_instalacao"]["codigo_uc"]
        ),
        "tipo_telhado": (
            orcamento["local_instalacao"]["tipo_telhado"]
        ),
        "modulos": orcamento["modulos"].copy(),
        "inversores": orcamento["inversores"].copy(),
        "status": status_inicial,
    }