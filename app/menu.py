from . import clientes
from . import projetos
from . import orcamentos
from . import utils

while True:
    print("\n=== SISTEMA DE HOMOLOGAÇÃO ===")
    print("1 - Cadastrar cliente")
    print("2 - Listar clientes")
    print("3 - Buscar cliente")
    print("4 - Cadastrar projeto")
    print("5 - Listar projetos")
    print("6 - Buscar projeto")
    print("7 - Alterar status do projeto")
    print("8 - Buscar cliente por nome")
    print("9 - Cadastrar orçamento")
    print("10 - Listar orçamentos")
    print("11 - Alterar status do orçamento")
    print("12 - Converter orçamento em projeto")
    print("0 - Sair")

    opcao = input("Escolha uma opção: ")

    if opcao == "1":
        clientes.cadastrar_cliente()

    elif opcao == "2":
        clientes.listar_clientes()

    elif opcao == "3":
        codigo = utils.ler_int("Digite o código do cliente: ")

        cliente = clientes.buscar_cliente(codigo)

        if cliente:
            print("\nCliente encontrado:")
            print(f"Código: {cliente['codigo']}")
            print(f"Nome: {cliente['nome']}")
            print(f"Cidade: {cliente['cidade']}")
            print(f"Telefone: {cliente['telefone']}")
        else:
            print("\nCliente não encontrado.")

    elif opcao == "4":
        projetos.cadastrar_projeto()

    elif opcao == "5":
        projetos.listar_projetos()

    elif opcao == "6":

        codigo = utils.ler_int("Digite o código do projeto: ")

        projeto = projetos.buscar_projeto(codigo)

        if projeto:
            print("\n=== Projeto Encontrado ===")
            projetos.mostrar_projeto(projeto)

        else:
            print("\nProjeto não encontrado.")

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

    elif opcao == "0":
        print("Saindo do sistema...")
        break

    else:
        print("Opção inválida.")
