from . import clientes
from . import status
from . import utils
from . import dados

#projetos = [] - foi substituido por função que chama os "projetos" salvos.
projetos = dados.carregar_dados("projetos.json")


def cadastrar_projeto():
    """
    Cadastra um novo projeto.
    """

    print("\n=== Cadastro de Projeto ===")

    cliente = clientes.selecionar_cliente()

    if cliente is None:
        print("\nCadastre o cliente antes de criar o projeto.")
        return

    codigo = utils.gerar_proximo_codigo(projetos)

    distribuidora = input("Distribuidora: ")
    potencia = utils.ler_float("Potência do sistema (kWp): ")

    projeto = {
        "codigo": codigo,
        "cliente": cliente["codigo"],
        "distribuidora": distribuidora,
        "potencia": potencia,
        "status": status.STATUS_INICIAL
    }

    projetos.append(projeto)

    dados.salvar_dados("projetos.json", projetos)

    print("\nProjeto cadastrado com sucesso!")

def listar_projetos():
    """
    Lista todos os projetos cadastrados.
    """

    print("\n=== Projetos Cadastrados ===")

    if not projetos:
        print("Nenhum projeto cadastrado.")
        return

    for projeto in projetos:
        mostrar_projeto(projeto)

def buscar_projeto(codigo):
    """
    Busca um projeto pelo código.
    Retorna o projeto encontrado ou None.
    """

    for projeto in projetos:

        if projeto["codigo"] == codigo:
            return projeto

def mostrar_projeto(projeto):
    """
    Exibe os dados de um projeto específico.
    """

    cliente = clientes.buscar_cliente(projeto["cliente"])

    print("----------------------------")
    print(f"Código: {projeto['codigo']}")

    if cliente:
        print(f"Cliente: {cliente['nome']}")
    else:
        print("Cliente: Não encontrado")

    print(f"Distribuidora: {projeto['distribuidora']}")
    print(f"Potência: {projeto['potencia']} kWp")
    print(f"Status: {projeto['status']}")

    return None

def alterar_status():
    """
    Altera o status de um projeto existente,
    respeitando as transições permitidas.
    """

    print("\n=== Alterar Status do Projeto ===")

    codigo = utils.ler_int("Digite o código do projeto: ")

    projeto = buscar_projeto(codigo)

    if projeto is None:
        print("\nProjeto não encontrado.")
        return

    print("\nProjeto selecionado:")
    mostrar_projeto(projeto)

    status.exibir_status()

    codigo_status = utils.ler_int(
    "\nDigite o código do novo status: "
    )

    novo_status = status.obter_status(codigo_status)

    if novo_status is None:
        print("\nStatus inválido.")
        return

    status_atual = projeto["status"]

    if not status.transicao_permitida(status_atual, novo_status):
        print("\nTransição de status não permitida.")
        print(f"Status atual: {status_atual}")
        print(f"Status solicitado: {novo_status}")
        return

    projeto["status"] = novo_status

    dados.salvar_dados("projetos.json", projetos)

    print("\nStatus alterado com sucesso!")
    print(f"Novo status: {novo_status}")

def criar_projeto_a_partir_do_orcamento(orcamento):
    """
    Cria e salva um novo projeto com base
    nos dados de um orçamento aprovado.

    Retorna o projeto criado.
    """

    codigo = utils.gerar_proximo_codigo(projetos)

    projeto = {
        "codigo": codigo,
        "cliente": orcamento["cliente"],
        "orcamento_origem": orcamento["codigo"],
        "distribuidora": (
            orcamento["local_instalacao"]["distribuidora"]
        ),
        "potencia": (
            orcamento["dimensionamento"]["potencia_prevista_kwp"]
        ),
        "codigo_uc": (
            orcamento["local_instalacao"]["codigo_uc"]
        ),
        "tipo_telhado": (
            orcamento["local_instalacao"]["tipo_telhado"]
        ),
        "modulos": orcamento["modulos"].copy(),
        "inversores": orcamento["inversores"].copy(),
        "status": status.STATUS_INICIAL
    }

    projetos.append(projeto)

    dados.salvar_dados(
        "projetos.json",
        projetos
    )

    return projeto

    
