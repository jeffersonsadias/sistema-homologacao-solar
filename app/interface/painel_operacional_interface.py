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

    print(
        "Consulta realizada em: "
        f"{momento_consulta.strftime('%d/%m/%Y %H:%M:%S')}"
    )

    print()
    print("=" * 60)

    input(
        "\nPressione Enter para voltar..."
    )