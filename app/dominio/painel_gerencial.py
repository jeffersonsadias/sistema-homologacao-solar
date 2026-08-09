"""
Regras de domínio relacionadas ao Painel Gerencial.

Este módulo é responsável por calcular indicadores
gerenciais a partir de dados já pertencentes aos
demais contextos do sistema.

O Painel Gerencial não é proprietário dos Projetos
nem das Homologações. Ele apenas recebe coleções
desses dados e produz informações consolidadas.
"""

from datetime import date
from typing import Any

from app.dominio.status_homologacao import (
    StatusHomologacao,
)

from app.dominio.homologacoes import (
    homologacao_possui_exigencia_aberta,
)

def calcular_visao_geral(
    projetos: list[dict[str, Any]],
    homologacoes: list[dict[str, Any]],
) -> dict[str, int]:
    """
    Calcula os indicadores gerais do
    Painel Gerencial.

    As Homologações são classificadas em:

    - concluídas;
    - encerradas sem conclusão;
    - em andamento.
    """

    total_projetos = len(
        projetos
    )

    total_homologacoes = len(
        homologacoes
    )

    total_concluidas = 0

    total_encerradas_sem_conclusao = 0

    for homologacao in homologacoes:
        status = homologacao.get(
            "status"
        )

        if (
            status
            == StatusHomologacao.CONCLUIDA.value
        ):
            total_concluidas += 1

        elif status in {
            StatusHomologacao.REJEITADA.value,
            StatusHomologacao.CANCELADA.value,
        }:
            total_encerradas_sem_conclusao += 1

    total_em_andamento = (
        total_homologacoes
        - total_concluidas
        - total_encerradas_sem_conclusao
    )

    return {
        "total_projetos": (
            total_projetos
        ),
        "total_homologacoes": (
            total_homologacoes
        ),
        "homologacoes_em_andamento": (
            total_em_andamento
        ),
        "homologacoes_concluidas": (
            total_concluidas
        ),
        "homologacoes_encerradas_sem_conclusao": (
            total_encerradas_sem_conclusao
        ),
    }

def calcular_taxa_conclusao(
    homologacoes: list[dict[str, Any]],
) -> float:
    """
    Calcula a taxa percentual de Homologações
    concluídas sobre o total de Homologações.

    Quando não existirem Homologações,
    retorna 0.0.
    """

    total_homologacoes = len(
        homologacoes
    )

    if total_homologacoes == 0:
        return 0.0

    total_concluidas = sum(
        1
        for homologacao in homologacoes
        if homologacao.get("status")
        == StatusHomologacao.CONCLUIDA.value
    )

    return (
        total_concluidas
        / total_homologacoes
        * 100
    )

def calcular_tempo_medio_conclusao(
    homologacoes: list[dict[str, Any]],
) -> float:
    """
    Calcula o tempo médio, em dias,
    entre a abertura e a conclusão real
    das Homologações concluídas.

    Homologações ainda não concluídas
    não participam do cálculo.

    Quando nenhuma Homologação concluída
    possuir datas válidas, retorna 0.0.
    """

    tempos_conclusao = []

    for homologacao in homologacoes:
        if (
            homologacao.get("status")
            != StatusHomologacao.CONCLUIDA.value
        ):
            continue

        data_abertura = homologacao.get(
            "data_abertura"
        )

        data_conclusao = homologacao.get(
            "data_conclusao_real"
        )

        if (
            not data_abertura
            or not data_conclusao
        ):
            continue

        data_abertura_convertida = (
            date.fromisoformat(
                data_abertura
            )
        )

        data_conclusao_convertida = (
            date.fromisoformat(
                data_conclusao
            )
        )

        diferenca = (
            data_conclusao_convertida
            - data_abertura_convertida
        ).days

        tempos_conclusao.append(
            diferenca
        )

    if not tempos_conclusao:
        return 0.0

    return (
        sum(tempos_conclusao)
        / len(tempos_conclusao)
    )

def contar_projetos_por_empresa(
    projetos: list[dict[str, Any]],
) -> dict[int, int]:
    """
    Conta quantos Projetos pertencem
    a cada Empresa.

    Retorna um dicionário no formato:

        {
            codigo_empresa: quantidade,
        }
    """

    distribuicao = {}

    for projeto in projetos:
        codigo_empresa = projeto.get(
            "codigo_empresa"
        )

        if codigo_empresa is None:
            continue

        distribuicao[codigo_empresa] = (
            distribuicao.get(
                codigo_empresa,
                0,
            )
            + 1
        )

    return distribuicao

def contar_projetos_por_concessionaria(
    projetos: list[dict[str, Any]],
) -> dict[int, int]:
    """
    Conta quantos Projetos pertencem
    a cada Concessionária.

    Retorna um dicionário no formato:

        {
            codigo_concessionaria: quantidade,
        }
    """

    distribuicao = {}

    for projeto in projetos:
        codigo_concessionaria = projeto.get(
            "codigo_concessionaria"
        )

        if codigo_concessionaria is None:
            continue

        distribuicao[
            codigo_concessionaria
        ] = (
            distribuicao.get(
                codigo_concessionaria,
                0,
            )
            + 1
        )

    return distribuicao

def contar_instalacoes_aguardando_execucao(
    homologacoes: list[dict[str, Any]],
) -> int:
    """
    Conta Homologações cuja Instalação
    já foi planejada, mas ainda não foi iniciada.
    """

    total = 0

    for homologacao in homologacoes:
        operacoes_campo = homologacao.get(
            "operacoes_campo"
        ) or {}

        instalacao = operacoes_campo.get(
            "instalacao"
        )

        if (
            isinstance(instalacao, dict)
            and instalacao.get("status")
            == "PLANEJADA"
        ):
            total += 1

    return total

def contar_vistorias_aguardando_resultado(
    homologacoes: list[dict[str, Any]],
) -> int:
    """
    Conta Homologações com ao menos
    uma Vistoria já realizada e ainda
    sem resultado final.
    """

    total = 0

    for homologacao in homologacoes:
        operacoes_campo = homologacao.get(
            "operacoes_campo"
        ) or {}

        vistorias = operacoes_campo.get(
            "vistorias"
        ) or []

        possui_vistoria_aguardando = any(
            vistoria.get("status")
            == "REALIZADA"
            for vistoria in vistorias
        )

        if possui_vistoria_aguardando:
            total += 1

    return total

def contar_ligacoes_aguardando_conclusao(
    homologacoes: list[dict[str, Any]],
) -> int:
    """
    Conta Homologações cuja Ligação
    foi solicitada ou agendada,
    mas ainda não foi concluída.
    """

    estados_pendentes = {
        "SOLICITADA",
        "AGENDADA",
    }

    total = 0

    for homologacao in homologacoes:
        operacoes_campo = homologacao.get(
            "operacoes_campo"
        ) or {}

        ligacao = operacoes_campo.get(
            "ligacao"
        )

        if (
            isinstance(ligacao, dict)
            and ligacao.get("status")
            in estados_pendentes
        ):
            total += 1

    return total

def contar_exigencias_abertas(
    homologacoes: list[dict[str, Any]],
) -> int:
    """
    Conta Homologações que possuem
    ao menos uma Exigência aberta.
    """

    return sum(
        1
        for homologacao in homologacoes
        if homologacao_possui_exigencia_aberta(
            homologacao
        )
    )

def gerar_indicadores_painel_gerencial(
    projetos: list[dict[str, Any]],
    homologacoes: list[dict[str, Any]],
) -> dict[str, Any]:
    """
    Consolida os indicadores do
    Painel Gerencial.

    A função reutiliza os cálculos específicos
    já definidos neste módulo e devolve uma
    estrutura única para consumo pela fachada
    e pela interface.
    """

    visao_geral = calcular_visao_geral(
        projetos=projetos,
        homologacoes=homologacoes,
    )

    desempenho = {
        "taxa_conclusao": (
            calcular_taxa_conclusao(
                homologacoes
            )
        ),
        "tempo_medio_conclusao_dias": (
            calcular_tempo_medio_conclusao(
                homologacoes
            )
        ),
        "homologacoes_com_exigencias_abertas": (
            contar_exigencias_abertas(
                homologacoes
            )
        ),
    }

    distribuicao = {
        "projetos_por_empresa": (
            contar_projetos_por_empresa(
                projetos
            )
        ),
        "projetos_por_concessionaria": (
            contar_projetos_por_concessionaria(
                projetos
            )
        ),
    }

    operacoes_campo = {
        "instalacoes_aguardando_execucao": (
            contar_instalacoes_aguardando_execucao(
                homologacoes
            )
        ),
        "vistorias_aguardando_resultado": (
            contar_vistorias_aguardando_resultado(
                homologacoes
            )
        ),
        "ligacoes_aguardando_conclusao": (
            contar_ligacoes_aguardando_conclusao(
                homologacoes
            )
        ),
    }

    return {
        "visao_geral": visao_geral,
        "desempenho": desempenho,
        "distribuicao": distribuicao,
        "operacoes_campo": operacoes_campo,
    }

