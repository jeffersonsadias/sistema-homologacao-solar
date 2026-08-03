"""
Fachada pública do módulo de Concessionárias.

Este módulo representa o ponto de entrada utilizado
pelo restante da aplicação para acessar as funcionalidades
relacionadas às Concessionárias.

Responsabilidades:

- carregar as Concessionárias armazenadas;
- manter a lista de Concessionárias em memória;
- delegar operações para a camada de interface;
- esconder os detalhes internos do domínio,
  da infraestrutura e da interface.

Outros módulos devem utilizar esta fachada em vez
de acessar diretamente as camadas internas.
"""

from app.infraestrutura.repositorio_concessionarias_json import (
    carregar_concessionarias,
)
from app.interface import concessionarias_interface

from app.dominio.concessionarias import (
    buscar_concessionaria_por_codigo,
)

# A lista é carregada uma única vez quando o módulo
# app.concessionarias é importado.
concessionarias = carregar_concessionarias()

def obter_concessionaria(
    codigo_concessionaria: int,
):
    """
    Retorna obrigatoriamente uma Concessionária existente.

    Esta consulta não utiliza input() e pode ser chamada
    pelas fachadas de outros módulos.

    Gera ValueError quando o código não for encontrado.
    """

    concessionaria = buscar_concessionaria_por_codigo(
        concessionarias,
        codigo_concessionaria,
    )

    if concessionaria is None:
        raise ValueError(
            "Concessionária com código "
            f"{codigo_concessionaria} não encontrada."
        )

    return concessionaria

def cadastrar_concessionaria():
    """
    Inicia o cadastro de uma nova Concessionária.

    A lista global de Concessionárias é enviada
    para a camada de interface.

    Retorna a Concessionária criada ou None.
    """

    return (
        concessionarias_interface
        .cadastrar_concessionaria(
            concessionarias
        )
    )


def listar_concessionarias():
    """
    Exibe todas as Concessionárias cadastradas.
    """

    return (
        concessionarias_interface
        .listar_concessionarias(
            concessionarias
        )
    )


def buscar_concessionaria():
    """
    Inicia a busca interativa por Concessionária.

    A busca pode ser realizada por código ou nome.
    """

    return (
        concessionarias_interface
        .buscar_concessionaria(
            concessionarias
        )
    )


def selecionar_concessionaria_por_codigo():
    """
    Solicita um código e retorna a Concessionária
    correspondente.

    Esta função pode ser utilizada por outros módulos
    que precisem selecionar uma Concessionária.
    """

    return (
        concessionarias_interface
        .selecionar_concessionaria_por_codigo(
            concessionarias
        )
    )


def adicionar_area_atuacao():
    """
    Inicia a inclusão de uma Área de Atuação
    em uma Concessionária.
    """

    return (
        concessionarias_interface
        .adicionar_area_atuacao(
            concessionarias
        )
    )


def alterar_situacao_concessionaria():
    """
    Permite ativar, inativar ou suspender
    uma Concessionária.
    """

    return (
        concessionarias_interface
        .alterar_situacao_concessionaria(
            concessionarias
        )
    )


def alterar_situacao_area_atuacao():
    """
    Permite ativar ou inativar uma Área de Atuação.
    """

    return (
        concessionarias_interface
        .alterar_situacao_area_atuacao(
            concessionarias
        )
    )


def abrir_menu_concessionarias():
    """
    Abre o menu de gerenciamento
    das Concessionárias.
    """

    return (
        concessionarias_interface
        .menu_concessionarias(
            concessionarias
        )
    )

def obter_concessionarias():
    """
    Retorna a lista de Concessionárias
    mantida pela fachada.

    A lista é fornecida para consultas
    e integração entre módulos.
    """

    return concessionarias