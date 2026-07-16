"""
Módulo responsável pelo gerenciamento dos orçamentos.

Este módulo contém as operações de cadastro, busca,
listagem e alteração de status dos orçamentos.
"""

from . import clientes
from . import dados
from . import projetos
from . import status_orcamento
from . import utils


orcamentos = dados.carregar_dados("orcamentos.json")

def _coletar_dimensionamento():
    """
    Solicita e retorna os dados de dimensionamento
    do sistema fotovoltaico.
    """

    consumo_medio_kwh = utils.ler_float(
        "Consumo médio mensal do cliente (kWh): "
    )

    potencia_prevista_kwp = utils.ler_float(
        "Potência prevista do sistema (kWp): "
    )

    return {
        "consumo_medio_kwh": consumo_medio_kwh,
        "potencia_prevista_kwp": potencia_prevista_kwp
    }

def _coletar_modulos():
    """
    Solicita e retorna os dados dos módulos fotovoltaicos.
    """

    quantidade = utils.ler_int(
        "Quantidade de módulos fotovoltaicos: "
    )

    fabricante = input(
        "Fabricante dos módulos fotovoltaicos: "
    ).strip()

    return {
        "quantidade": quantidade,
        "fabricante": fabricante
    }

def _coletar_inversores():
    """
    Solicita e retorna os dados dos inversores.
    """

    quantidade = utils.ler_int(
        "Quantidade de inversores: "
    )

    fabricante = input(
        "Fabricante dos inversores: "
    ).strip()

    tensao = input(
        "Tensão dos inversores: "
    ).strip()

    return {
        "quantidade": quantidade,
        "fabricante": fabricante,
        "tensao": tensao
    }

def _coletar_local_instalacao():
    """
    Solicita e retorna os dados do local de instalação.
    """

    codigo_uc = input(
        "Código da unidade consumidora (UC): "
    ).strip()

    distribuidora = input(
        "Distribuidora de energia: "
    ).strip()

    tipo_telhado = input(
        "Tipo de telhado: "
    ).strip()

    return {
        "codigo_uc": codigo_uc,
        "distribuidora": distribuidora,
        "tipo_telhado": tipo_telhado
    }

def _coletar_dados_comerciais():
    """
    Solicita e retorna os dados comerciais do orçamento.
    """

    valor_total = utils.ler_float(
        "Valor total do orçamento (R$): "
    )

    validade_dias = utils.ler_int(
        "Validade do orçamento em dias: "
    )

    prazo_instalacao_dias = utils.ler_int(
        "Prazo estimado para instalação em dias: "
    )

    return {
        "valor_total": valor_total,
        "validade_dias": validade_dias,
        "prazo_instalacao_dias": prazo_instalacao_dias
    }

def _criar_objeto_orcamento(
    codigo,
    cliente,
    dimensionamento,
    modulos,
    inversores,
    local_instalacao,
    comercial
):
    """
    Monta e retorna o dicionário de um novo orçamento.

    Esta função não solicita dados, não imprime mensagens
    e não salva arquivos.
    """

    return {
        "codigo": codigo,
        "cliente": cliente["codigo"],
        "dimensionamento": dimensionamento,
        "modulos": modulos,
        "inversores": inversores,
        "local_instalacao": local_instalacao,
        "comercial": comercial,
        "status": status_orcamento.STATUS_INICIAL
    }

def cadastrar_orcamento():
    """
    Cadastra um novo orçamento vinculado a um cliente.
    """

    print("\n=== Cadastro de Orçamento ===")

    cliente = clientes.selecionar_cliente()

    if cliente is None:
        print(
            "\nNão foi possível criar o orçamento "
            "sem um cliente válido."
        )
        return

    codigo = utils.gerar_proximo_codigo(orcamentos)

    dimensionamento = _coletar_dimensionamento()
    modulos = _coletar_modulos()
    inversores = _coletar_inversores()
    local_instalacao = _coletar_local_instalacao()
    comercial = _coletar_dados_comerciais()

    orcamento = _criar_objeto_orcamento(
    codigo=codigo,
    cliente=cliente,
    dimensionamento=dimensionamento,
    modulos=modulos,
    inversores=inversores,
    local_instalacao=local_instalacao,
    comercial=comercial
)

    orcamentos.append(orcamento)

    dados.salvar_dados(
        "orcamentos.json",
        orcamentos
    )

    print("\nOrçamento cadastrado com sucesso!")
    print(f"Código do orçamento: {codigo}")

def buscar_orcamento(codigo):
    """
    Busca um orçamento pelo código.

    Retorna o orçamento encontrado ou None.
    """

    for orcamento in orcamentos:

        if orcamento["codigo"] == codigo:
            return orcamento

    return None

def mostrar_orcamento(orcamento):
    """
    Exibe todas as informações de um orçamento.
    """

    print("\n==============================")
    print(f"Código: {orcamento['codigo']}")
    print(f"Cliente: {orcamento['cliente']}")

    print("\n--- Dimensionamento ---")

    print(
        f"Consumo médio: "
        f"{orcamento['dimensionamento']['consumo_medio_kwh']} kWh"
    )

    print(
        f"Potência prevista: "
        f"{orcamento['dimensionamento']['potencia_prevista_kwp']} kWp"
    )

    print("\n--- Módulos ---")

    print(
        f"Quantidade: "
        f"{orcamento['modulos']['quantidade']}"
    )

    print(
        f"Fabricante: "
        f"{orcamento['modulos']['fabricante']}"
    )

    print("\n--- Inversores ---")

    print(
        f"Quantidade: "
        f"{orcamento['inversores']['quantidade']}"
    )

    print(
        f"Fabricante: "
        f"{orcamento['inversores']['fabricante']}"
    )

    print(
        f"Tensão: "
        f"{orcamento['inversores']['tensao']}"
    )

    print("\n--- Local da Instalação ---")

    print(
        f"UC: "
        f"{orcamento['local_instalacao']['codigo_uc']}"
    )

    print(
        f"Distribuidora: "
        f"{orcamento['local_instalacao']['distribuidora']}"
    )

    print(
        f"Tipo de telhado: "
        f"{orcamento['local_instalacao']['tipo_telhado']}"
    )

    print("\n--- Comercial ---")

    print(
        f"Valor: R$ "
        f"{orcamento['comercial']['valor_total']:.2f}"
    )

    print(
        f"Validade: "
        f"{orcamento['comercial']['validade_dias']} dias"
    )

    print(
        f"Prazo estimado: "
        f"{orcamento['comercial']['prazo_instalacao_dias']} dias"
    )

    print(
        f"\nStatus: "
        f"{orcamento['status']}"
    )

    print("==============================")

def listar_orcamentos():
    """
    Lista todos os orçamentos cadastrados.
    """

    print("\n=== Orçamentos Cadastrados ===")

    if not orcamentos:
        print("Nenhum orçamento cadastrado.")
        return

    for orcamento in orcamentos:
        mostrar_orcamento(orcamento)

def selecionar_orcamento():
    """
    Solicita o código de um orçamento e retorna
    o orçamento encontrado.
    """

    codigo = utils.ler_int(
        "Digite o código do orçamento: "
    )

    orcamento = buscar_orcamento(codigo)

    if orcamento is None:
        print("\nOrçamento não encontrado.")
        return None

    return orcamento

def alterar_status():
    """
    Altera o status de um orçamento existente,
    respeitando as transições comerciais permitidas.
    """

    print("\n=== Alterar Status do Orçamento ===")

    orcamento = selecionar_orcamento()

    if orcamento is None:
        return

    print("\nOrçamento selecionado:")
    mostrar_orcamento(orcamento)

    status_orcamento.exibir_status()

    codigo_status = utils.ler_int(
        "\nDigite o código do novo status: "
    )

    novo_status = status_orcamento.obter_status(
        codigo_status
    )

    if novo_status is None:
        print("\nStatus de orçamento inválido.")
        return

    status_atual = orcamento["status"]

    if not status_orcamento.transicao_permitida(
        status_atual,
        novo_status
    ):
        print("\nTransição de status não permitida.")
        print(f"Status atual: {status_atual}")
        print(f"Status solicitado: {novo_status}")
        return

    orcamento["status"] = novo_status

    dados.salvar_dados(
        "orcamentos.json",
        orcamentos
    )

    print("\nStatus do orçamento alterado com sucesso!")
    print(f"Novo status: {novo_status}")

def converter_para_projeto():
    """
    Converte um orçamento aprovado em um projeto
    de homologação.

    O projeto é criado primeiro. Somente após a
    criação bem-sucedida o orçamento recebe o status
    "Convertido em projeto".
    """

    print("\n=== Converter Orçamento em Projeto ===")

    orcamento = selecionar_orcamento()

    if orcamento is None:
        return

    print("\nOrçamento selecionado:")
    mostrar_orcamento(orcamento)

    if orcamento["status"] != "Aprovado":
        print(
            "\nSomente orçamentos aprovados "
            "podem ser convertidos em projeto."
        )
        print(f"Status atual: {orcamento['status']}")
        return

    projeto_criado = (
        projetos.criar_projeto_a_partir_do_orcamento(
            orcamento
        )
    )

    if projeto_criado is None:
        print(
            "\nNão foi possível criar o projeto."
        )
        return

    orcamento["status"] = "Convertido em projeto"

    dados.salvar_dados(
        "orcamentos.json",
        orcamentos
    )

    print("\nOrçamento convertido com sucesso!")
    print(
        f"Projeto criado com o código: "
        f"{projeto_criado['codigo']}"
    )

