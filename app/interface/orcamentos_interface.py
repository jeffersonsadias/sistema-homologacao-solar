"""
Interface de terminal para Orçamentos.

Este módulo concentra:
- entradas do usuário;
- exibição de mensagens;
- fluxos interativos.

Não mantém uma lista própria de Orçamentos.
A coleção é sempre recebida por parâmetro.
"""

from app import clientes
from app import homologacoes
from app import projetos
from app import status_orcamento
from app import utils

from app.dominio.orcamentos import (
    buscar_orcamento_por_codigo,
    criar_dados_orcamento,
    orcamento_pode_ser_convertido,
)

from app.infraestrutura.repositorio_orcamentos_json import (
    salvar_orcamentos,
)

# ============================================================
# INTEGRAÇÃO PROJETO → HOMOLOGAÇÃO
# ============================================================

def _confirmar_inicio_homologacao():
    """
    Pergunta se o operador deseja iniciar a Homologação.

    Retorna:
        True:
            Quando a opção escolhida for 1.

        False:
            Quando a opção escolhida for 2.

    A função permanece solicitando uma opção enquanto
    o valor informado não for reconhecido.
    """

    while True:
        print(
            "\nDeseja iniciar agora o processo "
            "de Homologação?"
        )

        print(
            "1 - Sim"
        )

        print(
            "2 - Não"
        )

        opcao = input(
            "Escolha uma opção: "
        ).strip()

        if opcao == "1":
            return True

        if opcao == "2":
            return False

        print(
            "\nOpção inválida. Informe 1 ou 2."
        )

def _iniciar_homologacao_do_projeto(
    projeto_criado,
):
    """
    Oferece a abertura de uma Homologação para o Projeto criado.

    Quando o operador não desejar iniciar o processo, nenhuma
    Homologação será criada e o Projeto será preservado.

    Quando houver falha durante a abertura da Homologação,
    o Projeto e o Orçamento já convertidos também serão
    preservados.

    Retorna:
        A Homologação criada ou None.
    """

    iniciar_agora = _confirmar_inicio_homologacao()

    if not iniciar_agora:
        print(
            "\nO Projeto foi criado normalmente."
        )

        print(
            "A Homologação poderá ser iniciada "
            "posteriormente pelo menu de Homologações."
        )

        return None

    print(
        "\n=== Iniciar Homologação do Projeto ==="
    )

    codigo_empresa = utils.ler_int(
        "Código da Empresa responsável: "
    )

    codigo_concessionaria = utils.ler_int(
        "Código da Concessionária: "
    )

    data_abertura = input(
        "Data de abertura (AAAA-MM-DD): "
    ).strip()

    responsavel_abertura = input(
        "Responsável pela abertura: "
    ).strip()

    observacoes = input(
        "Observações, se houver: "
    ).strip()

    try:
        homologacao_criada = (
            homologacoes.criar_homologacao(
                codigo_empresa=codigo_empresa,
                codigo_projeto=projeto_criado["codigo"],
                codigo_concessionaria=(
                    codigo_concessionaria
                ),
                data_abertura=data_abertura,
                responsavel_abertura=(
                    responsavel_abertura
                ),
                observacoes=observacoes,
            )
        )

    except (TypeError, ValueError) as erro:
        print(
            "\nO Projeto foi criado, mas não foi possível "
            "iniciar a Homologação:"
        )

        print(
            str(erro)
        )

        print(
            "\nA Homologação poderá ser iniciada "
            "posteriormente pelo menu."
        )

        return None

    print(
        "\nHomologação iniciada com sucesso!"
    )

    print(
        f"Código da Homologação: "
        f"{homologacao_criada['codigo']}"
    )

    print(
        f"Status inicial: "
        f"{homologacao_criada['status']}"
    )

    return homologacao_criada

def _coletar_dimensionamento():
    """
    Solicita os dados de dimensionamento.
    """

    consumo_medio_kwh = utils.ler_float(
        "Consumo médio mensal do cliente (kWh): "
    )

    potencia_prevista_kwp = utils.ler_float(
        "Potência prevista do sistema (kWp): "
    )

    return {
        "consumo_medio_kwh": consumo_medio_kwh,
        "potencia_prevista_kwp": potencia_prevista_kwp,
    }


def _coletar_modulos():
    """
    Solicita os dados dos módulos fotovoltaicos.
    """

    quantidade = utils.ler_int(
        "Quantidade de módulos fotovoltaicos: "
    )

    fabricante = input(
        "Fabricante dos módulos fotovoltaicos: "
    ).strip()

    return {
        "quantidade": quantidade,
        "fabricante": fabricante,
    }


def _coletar_inversores():
    """
    Solicita os dados dos inversores.
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
        "tensao": tensao,
    }


def _coletar_local_instalacao():
    """
    Solicita os dados do local de instalação.
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
        "tipo_telhado": tipo_telhado,
    }


def _coletar_dados_comerciais():
    """
    Solicita os dados comerciais do Orçamento.
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
        "prazo_instalacao_dias": prazo_instalacao_dias,
    }


def cadastrar_orcamento(lista_orcamentos):
    """
    Cadastra um novo Orçamento.
    """

    print("\n=== Cadastro de Orçamento ===")

    cliente = clientes.selecionar_cliente()

    if cliente is None:
        print(
            "\nNão foi possível criar o orçamento "
            "sem um cliente válido."
        )
        return None

    codigo = utils.gerar_proximo_codigo(
        lista_orcamentos
    )

    dimensionamento = _coletar_dimensionamento()
    modulos = _coletar_modulos()
    inversores = _coletar_inversores()
    local_instalacao = _coletar_local_instalacao()
    comercial = _coletar_dados_comerciais()

    orcamento = criar_dados_orcamento(
        codigo=codigo,
        codigo_cliente=cliente["codigo"],
        dimensionamento=dimensionamento,
        modulos=modulos,
        inversores=inversores,
        local_instalacao=local_instalacao,
        comercial=comercial,
        status_inicial=status_orcamento.STATUS_INICIAL,
    )

    lista_orcamentos.append(
        orcamento
    )

    salvar_orcamentos(
        lista_orcamentos
    )

    print("\nOrçamento cadastrado com sucesso!")
    print(f"Código do orçamento: {codigo}")

    return orcamento


def mostrar_orcamento(orcamento):
    """
    Exibe todas as informações de um Orçamento.
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


def listar_orcamentos(lista_orcamentos):
    """
    Lista todos os Orçamentos cadastrados.
    """

    print("\n=== Orçamentos Cadastrados ===")

    if not lista_orcamentos:
        print("Nenhum orçamento cadastrado.")
        return

    for orcamento in lista_orcamentos:
        mostrar_orcamento(
            orcamento
        )


def selecionar_orcamento(lista_orcamentos):
    """
    Solicita o código e retorna o Orçamento encontrado.
    """

    codigo = utils.ler_int(
        "Digite o código do orçamento: "
    )

    orcamento = buscar_orcamento_por_codigo(
        lista_orcamentos,
        codigo,
    )

    if orcamento is None:
        print("\nOrçamento não encontrado.")
        return None

    return orcamento


def alterar_status(lista_orcamentos):
    """
    Altera o status de um Orçamento.
    """

    print("\n=== Alterar Status do Orçamento ===")

    orcamento = selecionar_orcamento(
        lista_orcamentos
    )

    if orcamento is None:
        return None

    print("\nOrçamento selecionado:")

    mostrar_orcamento(
        orcamento
    )

    status_orcamento.exibir_status()

    codigo_status = utils.ler_int(
        "\nDigite o código do novo status: "
    )

    novo_status = status_orcamento.obter_status(
        codigo_status
    )

    if novo_status is None:
        print("\nStatus de orçamento inválido.")
        return None

    status_atual = orcamento["status"]

    if not status_orcamento.transicao_permitida(
        status_atual,
        novo_status,
    ):
        print("\nTransição de status não permitida.")
        print(f"Status atual: {status_atual}")
        print(f"Status solicitado: {novo_status}")
        return None

    orcamento["status"] = novo_status

    salvar_orcamentos(
        lista_orcamentos
    )

    print("\nStatus do orçamento alterado com sucesso!")
    print(f"Novo status: {novo_status}")

    return orcamento


def converter_para_projeto(lista_orcamentos):
    """
    Converte um Orçamento aprovado em Projeto.
    """

    print("\n=== Converter Orçamento em Projeto ===")

    orcamento = selecionar_orcamento(
        lista_orcamentos
    )

    if orcamento is None:
        return None

    print("\nOrçamento selecionado:")

    mostrar_orcamento(
        orcamento
    )

    if not orcamento_pode_ser_convertido(
        orcamento
    ):
        print(
            "\nSomente orçamentos aprovados "
            "podem ser convertidos em projeto."
        )

        print(
            f"Status atual: "
            f"{orcamento['status']}"
        )

        return None

    projeto_criado = (
        projetos.criar_projeto_a_partir_do_orcamento(
            orcamento
        )
    )

    if projeto_criado is None:
        print(
            "\nNão foi possível criar o projeto."
        )
        return None

    orcamento["status"] = "Convertido em projeto"

    salvar_orcamentos(
        lista_orcamentos
    )

    print("\nOrçamento convertido com sucesso!")

    print(
        f"Projeto criado com o código: "
        f"{projeto_criado['codigo']}"
    )

    _iniciar_homologacao_do_projeto(
        projeto_criado
    )

    return projeto_criado