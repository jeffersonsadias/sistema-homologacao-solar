"""
Interface de terminal do Painel Operacional.

Este módulo é responsável por:

- exibir os indicadores gerais do sistema;
- consultar as coleções públicas das fachadas;
- apresentar a data e a hora da consulta.

Este módulo não deve:

- alterar dados;
- acessar arquivos JSON;
- executar regras de negócio;
- persistir informações.
"""

from datetime import datetime

from app import clientes
from app import empresas
from app import homologacoes
from app import orcamentos
from app import projetos


def _obter_data_hora_consulta() -> datetime:
    """
    Retorna a data e a hora atuais.

    A função foi separada para permitir testes
    determinísticos sem depender do relógio real.
    """

    return datetime.now()

def _exibir_indicador(
    nome: str,
    quantidade: int,
) -> None:
    """
    Exibe um indicador em uma linha padronizada.
    """

    print(
        f"{nome:.<32}{quantidade:>6}"
    )

def exibir_painel_operacional() -> None:
    """
    Exibe o Dashboard Operacional do sistema.

    Os valores são obtidos por funções públicas
    das fachadas, sem acessar diretamente
    suas coleções internas.
    """

    momento_consulta = _obter_data_hora_consulta()

    print()
    print("=" * 60)
    print("PAINEL OPERACIONAL")
    print("=" * 60)
    print()

    _exibir_indicador(
        "Clientes",
        clientes.quantidade_clientes(),
    )

    _exibir_indicador(
        "Empresas",
        empresas.quantidade_empresas(),
    )

    _exibir_indicador(
        "Orçamentos",
        orcamentos.quantidade_orcamentos(),
    )

    _exibir_indicador(
        "Projetos",
        projetos.quantidade_projetos(),
    )

    _exibir_indicador(
        "Homologações",
        homologacoes.quantidade_homologacoes(),
    )

    print()
    print("-" * 60)
    print("INDICADORES DE PROJETOS")
    print("-" * 60)
    print()

    _exibir_indicador(
        "Aguardando documentação",
        projetos.quantidade_projetos_com_status(
            "Aguardando documentação"
        ),
    )

    _exibir_indicador(
        "Em análise",
        projetos.quantidade_projetos_com_status(
            "Em análise pela distribuidora"
        ),
    )

    _exibir_indicador(
        "Com exigência",
        projetos.quantidade_projetos_com_status(
            "Correção solicitada"
        ),
    )

    _exibir_indicador(
        "Aprovados",
        projetos.quantidade_projetos_com_status(
            "Aprovado"
        ),
    )

    _exibir_indicador(
        "Homologados",
        projetos.quantidade_projetos_com_status(
            "Homologado"
        ),
    )

    _exibir_indicador(
        "Total geral",
        projetos.quantidade_projetos(),
    )

    print()
    print("-" * 60)
    print("PENDÊNCIAS DE HOMOLOGAÇÃO")
    print("-" * 60)
    print()

    _exibir_indicador(
        "Aguardando documentação",
        (
            homologacoes
            .quantidade_homologacoes_aguardando_documentacao()
        ),
    )

    _exibir_indicador(
        "Com exigências abertas",
        (
            homologacoes
            .quantidade_homologacoes_com_exigencias_abertas()
        ),
    )

    _exibir_indicador(
        "Aguardando envio",
        (
            homologacoes
            .quantidade_homologacoes_pendentes_de_envio()
        ),
    )

    _exibir_indicador(
        "Aguardando resposta",
        (
            homologacoes
            .quantidade_homologacoes_pendentes_de_resposta()
        ),
    )

    _exibir_indicador(
        "Sem responsável",
        (
            homologacoes
            .quantidade_homologacoes_sem_responsavel_atual()
        ),
    )

    _exibir_indicador(
        "Total de pendências",
        homologacoes.quantidade_total_pendencias(),
    )

    print()

    print(
        "Consulta realizada em: "
        f"{momento_consulta.strftime('%d/%m/%Y %H:%M:%S')}"
    )

    print()
    print("=" * 60)

    input(
        "\nPressione Enter para voltar..."
    )