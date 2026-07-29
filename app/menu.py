"""
Menu principal do Sistema de Homologação Solar.

Este módulo representa o ponto inicial da aplicação.

Execução:

    python -m app.menu
"""

from app import clientes
from app import concessionarias
from app import orcamentos
from app import projetos
from app import unidades_consumidoras
from app import utils

from app.interface import (
    empresas_interface,
    usuarios_interface,
    vinculos_unidade_projeto_interface,
)


def exibir_menu():
    """
    Exibe as opções principais do sistema.
    """

    print(
        "\n=== SISTEMA DE HOMOLOGAÇÃO ==="
    )

    print(
        "1 - Cadastrar cliente"
    )

    print(
        "2 - Listar clientes"
    )

    print(
        "3 - Buscar cliente"
    )

    print(
        "4 - Cadastrar projeto"
    )

    print(
        "5 - Listar projetos"
    )

    print(
        "6 - Buscar projeto"
    )

    print(
        "7 - Alterar status do projeto"
    )

    print(
        "8 - Buscar cliente por nome"
    )

    print(
        "9 - Cadastrar orçamento"
    )

    print(
        "10 - Listar orçamentos"
    )

    print(
        "11 - Alterar status do orçamento"
    )

    print(
        "12 - Converter orçamento em projeto"
    )

    print(
        "13 - Gerenciar concessionárias"
    )

    print(
        "14 - Gerenciar Unidades Consumidoras"
    )

    print(
        "15 - Gerenciar vínculos Unidade-Projeto"
    )

    print(
        "16 - Gerenciar empresas"
    )

    print(
        "17 - Gerenciar usuários"
    )

    print(
        "0 - Sair"
    )


def executar_menu():
    """
    Mantém o menu principal em execução
    até que o usuário escolha sair.
    """

    while True:
        exibir_menu()

        opcao = input(
            "Escolha uma opção: "
        ).strip()

        if opcao == "1":
            clientes.cadastrar_cliente()

        elif opcao == "2":
            clientes.listar_clientes()

        elif opcao == "3":
            codigo = utils.ler_int(
                "Digite o código do cliente: "
            )

            cliente = clientes.buscar_cliente(
                codigo
            )

            if cliente:
                print(
                    "\nCliente encontrado:"
                )

                print(
                    f"Código: {cliente['codigo']}"
                )

                print(
                    f"Nome: {cliente['nome']}"
                )

                print(
                    f"Cidade: {cliente['cidade']}"
                )

                print(
                    f"Telefone: {cliente['telefone']}"
                )

            else:
                print(
                    "\nCliente não encontrado."
                )

        elif opcao == "4":
            projetos.cadastrar_projeto()

        elif opcao == "5":
            projetos.listar_projetos()

        elif opcao == "6":
            codigo = utils.ler_int(
                "Digite o código do projeto: "
            )

            projeto = projetos.buscar_projeto(
                codigo
            )

            if projeto:
                print(
                    "\n=== Projeto Encontrado ==="
                )

                projetos.mostrar_projeto(
                    projeto
                )

            else:
                print(
                    "\nProjeto não encontrado."
                )

        elif opcao == "7":
            projetos.alterar_status()

        elif opcao == "8":
            clientes.consultar_clientes_por_nome()

        elif opcao == "9":
            orcamentos.cadastrar_orcamento()

        elif opcao == "10":
            orcamentos.listar_orcamentos()

        elif opcao == "11":
            orcamentos.alterar_status()

        elif opcao == "12":
            orcamentos.converter_para_projeto()

        elif opcao == "13":
            concessionarias.abrir_menu_concessionarias()

        elif opcao == "14":
            unidades_consumidoras.abrir_menu_unidades_consumidoras(
                concessionarias.obter_concessionarias()
            )

        elif opcao == "15":
            (
                vinculos_unidade_projeto_interface
                .menu_vinculos_unidade_projeto()
            )

        elif opcao == "16":
            empresas_interface.menu_empresas()

        elif opcao == "17":
            usuarios_interface.menu_usuarios()

        elif opcao == "0":
            print(
                "\nSaindo do sistema..."
            )

            break

        else:
            print(
                "\nOpção inválida."
            )


if __name__ == "__main__":
    executar_menu()