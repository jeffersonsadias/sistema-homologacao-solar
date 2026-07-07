# ============================================================
# SISTEMA DE HOMOLOGAÇÃO SOLAR - VERSÃO 1
# Desenvolvido em Python
# Objetivo: controlar clientes e projetos de homologação solar
# ============================================================


# Lista onde os clientes serão armazenados
clientes = []

# Lista onde os projetos serão armazenados
projetos = []


# ------------------------------------------------------------
# Função para cadastrar um cliente
# ------------------------------------------------------------
def cadastrar_cliente():
    print("\n--- CADASTRO DE CLIENTE ---")

    nome = input("Nome do cliente: ")
    cpf_cnpj = input("CPF ou CNPJ: ")
    telefone = input("Telefone: ")
    cidade = input("Cidade: ")

    cliente = {
        "id": len(clientes) + 1,
        "nome": nome,
        "cpf_cnpj": cpf_cnpj,
        "telefone": telefone,
        "cidade": cidade
    }

    clientes.append(cliente)

    print("\nCliente cadastrado com sucesso!")


# ------------------------------------------------------------
# Função para listar clientes
# ------------------------------------------------------------
def listar_clientes():
    print("\n--- CLIENTES CADASTRADOS ---")

    if len(clientes) == 0:
        print("Nenhum cliente cadastrado.")
        return

    for cliente in clientes:
        print(f"""
ID: {cliente['id']}
Nome: {cliente['nome']}
CPF/CNPJ: {cliente['cpf_cnpj']}
Telefone: {cliente['telefone']}
Cidade: {cliente['cidade']}
""")


# ------------------------------------------------------------
# Função para cadastrar um projeto solar
# ------------------------------------------------------------
def cadastrar_projeto():
    print("\n--- CADASTRO DE PROJETO SOLAR ---")

    if len(clientes) == 0:
        print("Antes de cadastrar um projeto, cadastre um cliente.")
        return

    listar_clientes()

    id_cliente = int(input("Digite o ID do cliente: "))

    cliente_encontrado = None

    for cliente in clientes:
        if cliente["id"] == id_cliente:
            cliente_encontrado = cliente
            break

    if cliente_encontrado is None:
        print("Cliente não encontrado.")
        return

    potencia = float(input("Potência do sistema em kWp: "))
    concessionaria = input("Concessionária: ")
    unidade_consumidora = input("Número da unidade consumidora: ")

    projeto = {
        "id": len(projetos) + 1,
        "cliente": cliente_encontrado["nome"],
        "potencia": potencia,
        "concessionaria": concessionaria,
        "unidade_consumidora": unidade_consumidora,
        "status": "Documentação pendente"
    }

    projetos.append(projeto)

    print("\nProjeto cadastrado com sucesso!")


# ------------------------------------------------------------
# Função para listar projetos
# ------------------------------------------------------------
def listar_projetos():
    print("\n--- PROJETOS CADASTRADOS ---")

    if len(projetos) == 0:
        print("Nenhum projeto cadastrado.")
        return

    for projeto in projetos:
        print(f"""
ID: {projeto['id']}
Cliente: {projeto['cliente']}
Potência: {projeto['potencia']} kWp
Concessionária: {projeto['concessionaria']}
Unidade Consumidora: {projeto['unidade_consumidora']}
Status: {projeto['status']}
""")


# ------------------------------------------------------------
# Função para atualizar o status de um projeto
# ------------------------------------------------------------
def atualizar_status():
    print("\n--- ATUALIZAR STATUS DO PROJETO ---")

    if len(projetos) == 0:
        print("Nenhum projeto cadastrado.")
        return

    listar_projetos()

    id_projeto = int(input("Digite o ID do projeto: "))

    projeto_encontrado = None

    for projeto in projetos:
        if projeto["id"] == id_projeto:
            projeto_encontrado = projeto
            break

    if projeto_encontrado is None:
        print("Projeto não encontrado.")
        return

    print("""
Escolha o novo status:

1 - Documentação pendente
2 - Documentação em preparação
3 - Enviado para concessionária
4 - Em análise
5 - Ajustes solicitados
6 - Aprovado
7 - Vistoria solicitada
8 - Vistoria realizada
9 - Medidor substituído
10 - Concluído
11 - Cancelado
""")

    opcao = input("Digite a opção: ")

    status_opcoes = {
        "1": "Documentação pendente",
        "2": "Documentação em preparação",
        "3": "Enviado para concessionária",
        "4": "Em análise",
        "5": "Ajustes solicitados",
        "6": "Aprovado",
        "7": "Vistoria solicitada",
        "8": "Vistoria realizada",
        "9": "Medidor substituído",
        "10": "Concluído",
        "11": "Cancelado"
    }

    if opcao in status_opcoes:
        projeto_encontrado["status"] = status_opcoes[opcao]
        print("\nStatus atualizado com sucesso!")
    else:
        print("Opção inválida.")


# ------------------------------------------------------------
# Função para exibir resumo geral
# ------------------------------------------------------------
def resumo_geral():
    print("\n--- RESUMO GERAL ---")

    total_clientes = len(clientes)
    total_projetos = len(projetos)

    potencia_total = 0

    for projeto in projetos:
        potencia_total += projeto["potencia"]

    print(f"Total de clientes cadastrados: {total_clientes}")
    print(f"Total de projetos cadastrados: {total_projetos}")
    print(f"Potência total cadastrada: {potencia_total} kWp")


# ------------------------------------------------------------
# Função do menu principal
# ------------------------------------------------------------
def menu():
    while True:
        print("""
========================================
 SISTEMA DE HOMOLOGAÇÃO SOLAR - VERSÃO 1
========================================

1 - Cadastrar cliente
2 - Listar clientes
3 - Cadastrar projeto
4 - Listar projetos
5 - Atualizar status do projeto
6 - Resumo geral
0 - Sair
""")

        opcao = input("Escolha uma opção: ")

        if opcao == "1":
            cadastrar_cliente()

        elif opcao == "2":
            listar_clientes()

        elif opcao == "3":
            cadastrar_projeto()

        elif opcao == "4":
            listar_projetos()

        elif opcao == "5":
            atualizar_status()

        elif opcao == "6":
            resumo_geral()

        elif opcao == "0":
            print("Encerrando o sistema...")
            break

        else:
            print("Opção inválida. Tente novamente.")


# ------------------------------------------------------------
# Início do programa
# ------------------------------------------------------------
menu()