"""
Fachada de compatibilidade do módulo de Projetos.

Este módulo preserva a interface pública utilizada
pelos módulos antigos e pelos testes da Sprint 1.

As responsabilidades estão distribuídas entre:

- app.dominio.projetos
- app.infraestrutura.repositorio_projetos_json
- app.interface.projetos_interface
"""

from app import utils
from app import status

from app.dominio.projetos import (
    buscar_projeto_por_codigo,
    criar_dados_projeto_a_partir_do_orcamento as criar_dados_projeto_do_orcamento,
)

from app.infraestrutura.repositorio_projetos_json import (
    carregar_projetos,
    salvar_projetos,
)

from app.interface import projetos_interface


# Coleção mantida pela fachada para preservar
# compatibilidade com os módulos e testes existentes.
projetos = carregar_projetos()


def cadastrar_projeto():
    """
    Encaminha o cadastro para a camada de interface.
    """

    return projetos_interface.cadastrar_projeto(
        projetos
    )


def listar_projetos():
    """
    Encaminha a listagem para a camada de interface.
    """

    return projetos_interface.listar_projetos(
        projetos
    )


def buscar_projeto(codigo):
    """
    Busca um Projeto pelo código.

    A regra efetiva de busca pertence ao domínio.
    """

    return buscar_projeto_por_codigo(
        projetos,
        codigo,
    )


def mostrar_projeto(projeto):
    """
    Encaminha a exibição para a camada de interface.
    """

    return projetos_interface.mostrar_projeto(
        projeto
    )


def alterar_status():
    """
    Encaminha a alteração de status
    para a camada de interface.
    """

    return projetos_interface.alterar_status(
        projetos
    )


def criar_projeto_a_partir_do_orcamento(orcamento):
    """
    Cria e salva um novo Projeto com base
    nos dados de um Orçamento aprovado.

    Esta função permanece na fachada porque pode ser
    utilizada por outros módulos sem interação
    com o terminal.

    Retorna:
        O Projeto criado.
    """

    codigo = utils.gerar_proximo_codigo(
        projetos
    )

    projeto = criar_dados_projeto_do_orcamento(
        codigo=codigo,
        orcamento=orcamento,
        status_inicial=status.STATUS_INICIAL,
    )

    projetos.append(projeto)

    salvar_projetos(projetos)

    return projeto