"""
Interface das Unidades Consumidoras.

Este módulo concentra a interação com o usuário
relacionada ao Cadastro Mestre de Unidades Consumidoras.

Responsabilidades:

- solicitar dados;
- cadastrar Unidades Consumidoras;
- listar Unidades Consumidoras;
- buscar Unidades Consumidoras;
- selecionar uma Unidade por código;
- alterar sua situação;
- exibir seus dados;
- delegar regras ao domínio;
- solicitar a persistência à infraestrutura.

Este módulo não deve implementar regras de negócio
que pertencem às entidades do domínio.
"""

from app import utils

from app.dominio.concessionarias import (
    buscar_concessionaria_por_codigo,
)
from app.dominio.unidades_consumidoras import (
    EnderecoUnidade,
    SituacaoUnidadeConsumidora,
    TipoLigacao,
    TipoTitular,
    TitularConta,
    buscar_unidade_por_codigo,
    buscar_unidade_por_numero_uc,
    criar_unidade_consumidora,
    numero_uc_existe,
)
from app.infraestrutura.repositorio_unidades_consumidoras_json import (
    salvar_unidades_consumidoras,
)


def exibir_menu_unidades_consumidoras():
    """
    Exibe as opções do menu
    de Unidades Consumidoras.
    """

    print(
        "\n=== MENU DE UNIDADES CONSUMIDORAS ==="
    )
    print("1 - Cadastrar Unidade Consumidora")
    print("2 - Listar Unidades Consumidoras")
    print("3 - Buscar Unidade Consumidora")
    print("4 - Alterar situação da Unidade")
    print("0 - Voltar")


def menu_unidades_consumidoras(
    unidades_consumidoras,
    concessionarias,
):
    """
    Mantém o submenu de Unidades Consumidoras
    em execução até o usuário escolher voltar.
    """

    while True:
        exibir_menu_unidades_consumidoras()

        opcao = input(
            "Escolha uma opção: "
        ).strip()

        if opcao == "1":
            cadastrar_unidade_consumidora(
                unidades_consumidoras,
                concessionarias,
            )

        elif opcao == "2":
            listar_unidades_consumidoras(
                unidades_consumidoras
            )

        elif opcao == "3":
            buscar_unidade_consumidora(
                unidades_consumidoras
            )

        elif opcao == "4":
            alterar_situacao_unidade(
                unidades_consumidoras
            )

        elif opcao == "0":
            break

        else:
            print(
                "\nOpção inválida."
            )


def gerar_proximo_codigo_unidade(
    unidades_consumidoras,
):
    """
    Gera o próximo código interno disponível
    para uma Unidade Consumidora.
    """

    return utils.gerar_proximo_codigo(
        unidades_consumidoras
    )


def selecionar_tipo_titular():
    """
    Solicita ao usuário o tipo do titular.

    Retorna um item do enum TipoTitular
    ou None quando a operação é cancelada.
    """

    while True:
        print("\n=== TIPO DO TITULAR ===")
        print("1 - Pessoa física")
        print("2 - Pessoa jurídica")
        print("0 - Cancelar")

        opcao = input(
            "Escolha o tipo do titular: "
        ).strip()

        if opcao == "1":
            return TipoTitular.PESSOA_FISICA

        if opcao == "2":
            return TipoTitular.PESSOA_JURIDICA

        if opcao == "0":
            return None

        print(
            "\nOpção inválida."
        )


def selecionar_tipo_ligacao():
    """
    Solicita ao usuário o tipo de ligação elétrica.

    Retorna um item do enum TipoLigacao
    ou None quando a operação é cancelada.
    """

    while True:
        print("\n=== TIPO DE LIGAÇÃO ===")
        print("1 - Monofásica")
        print("2 - Bifásica")
        print("3 - Trifásica")
        print("0 - Cancelar")

        opcao = input(
            "Escolha o tipo de ligação: "
        ).strip()

        if opcao == "1":
            return TipoLigacao.MONOFASICA

        if opcao == "2":
            return TipoLigacao.BIFASICA

        if opcao == "3":
            return TipoLigacao.TRIFASICA

        if opcao == "0":
            return None

        print(
            "\nOpção inválida."
        )


def selecionar_concessionaria(
    concessionarias,
):
    """
    Solicita o código de uma Concessionária
    e retorna o objeto encontrado.

    Retorna None quando não houver Concessionárias
    ou quando o código não for localizado.
    """

    if not concessionarias:
        print(
            "\nNenhuma Concessionária cadastrada."
        )
        return None

    print(
        "\n=== CONCESSIONÁRIAS DISPONÍVEIS ==="
    )

    for concessionaria in concessionarias:
        print(
            f"{concessionaria.codigo} - "
            f"{concessionaria.nome_abreviado}"
        )

    codigo = utils.ler_int(
        "\nDigite o código da Concessionária: "
    )

    concessionaria = (
        buscar_concessionaria_por_codigo(
            concessionarias,
            codigo,
        )
    )

    if concessionaria is None:
        print(
            "\nConcessionária não encontrada."
        )

    return concessionaria


def coletar_titular():
    """
    Solicita os dados do titular
    e cria um objeto TitularConta.

    Retorna o titular criado ou None
    quando a operação é cancelada.
    """

    tipo_titular = selecionar_tipo_titular()

    if tipo_titular is None:
        return None

    nome = input(
        "Nome ou razão social do titular: "
    ).strip()

    if tipo_titular == TipoTitular.PESSOA_FISICA:
        documento = input(
            "CPF do titular: "
        ).strip()

    else:
        documento = input(
            "CNPJ do titular: "
        ).strip()

    try:
        return TitularConta(
            nome=nome,
            documento=documento,
            tipo=tipo_titular,
        )

    except (
        TypeError,
        ValueError,
    ) as erro:
        print(
            f"\nNão foi possível cadastrar "
            f"o titular: {erro}"
        )

        return None


def coletar_endereco():
    """
    Solicita os dados do endereço
    e cria um objeto EnderecoUnidade.

    Retorna o endereço criado ou None
    quando os dados forem inválidos.
    """

    print("\n=== ENDEREÇO DA UNIDADE ===")

    logradouro = input(
        "Logradouro: "
    ).strip()

    numero = input(
        "Número: "
    ).strip()

    bairro = input(
        "Bairro: "
    ).strip()

    cidade = input(
        "Cidade: "
    ).strip()

    estado = input(
        "Estado (UF): "
    ).strip()

    cep = input(
        "CEP: "
    ).strip()

    complemento = input(
        "Complemento, se houver: "
    ).strip()

    try:
        return EnderecoUnidade(
            logradouro=logradouro,
            numero=numero,
            bairro=bairro,
            cidade=cidade,
            estado=estado,
            cep=cep,
            complemento=complemento,
        )

    except (
        TypeError,
        ValueError,
    ) as erro:
        print(
            f"\nNão foi possível cadastrar "
            f"o endereço: {erro}"
        )

        return None


def cadastrar_unidade_consumidora(
    unidades_consumidoras,
    concessionarias,
):
    """
    Realiza o cadastro de uma nova
    Unidade Consumidora.

    Retorna a Unidade criada ou None
    quando o cadastro não for concluído.
    """

    print(
        "\n=== CADASTRO DE UNIDADE CONSUMIDORA ==="
    )

    concessionaria = selecionar_concessionaria(
        concessionarias
    )

    if concessionaria is None:
        return None

    numero_uc = input(
        "Número da Unidade Consumidora: "
    ).strip()

    if numero_uc_existe(
        unidades_consumidoras,
        numero_uc,
        concessionaria.codigo,
    ):
        print(
            "\nJá existe uma Unidade Consumidora "
            "com esse número nessa Concessionária."
        )

        return None

    codigo_cliente = input(
        "Código do cliente na Concessionária: "
    ).strip()

    titular = coletar_titular()

    if titular is None:
        return None

    endereco = coletar_endereco()

    if endereco is None:
        return None

    tipo_ligacao = selecionar_tipo_ligacao()

    if tipo_ligacao is None:
        return None

    carga_instalada_kw = utils.ler_float(
        "Carga instalada da unidade em kW: "
    )

    codigo = gerar_proximo_codigo_unidade(
        unidades_consumidoras
    )

    try:
        unidade = criar_unidade_consumidora(
            codigo=codigo,
            numero_uc=numero_uc,
            codigo_cliente=codigo_cliente,
            codigo_concessionaria=(
                concessionaria.codigo
            ),
            titular=titular,
            endereco=endereco,
            tipo_ligacao=tipo_ligacao,
            carga_instalada_kw=(
                carga_instalada_kw
            ),
        )

    except (
        TypeError,
        ValueError,
    ) as erro:
        print(
            f"\nNão foi possível cadastrar "
            f"a Unidade Consumidora: {erro}"
        )

        return None

    unidades_consumidoras.append(
        unidade
    )

    salvar_unidades_consumidoras(
        unidades_consumidoras
    )

    print(
        "\nUnidade Consumidora cadastrada "
        "com sucesso."
    )

    exibir_unidade_consumidora(
        unidade
    )

    return unidade


def obter_nome_concessionaria(
    codigo_concessionaria,
    concessionarias,
):
    """
    Retorna o nome abreviado da Concessionária
    correspondente ao código informado.

    Quando não localizada, retorna uma descrição
    contendo apenas o código.
    """

    concessionaria = (
        buscar_concessionaria_por_codigo(
            concessionarias,
            codigo_concessionaria,
        )
    )

    if concessionaria is None:
        return (
            f"Código {codigo_concessionaria}"
        )

    return concessionaria.nome_abreviado


def exibir_unidade_consumidora(
    unidade,
    concessionarias=None,
):
    """
    Exibe os dados completos de uma
    Unidade Consumidora.
    """

    if concessionarias is None:
        nome_concessionaria = (
            f"Código "
            f"{unidade.codigo_concessionaria}"
        )

    else:
        nome_concessionaria = (
            obter_nome_concessionaria(
                unidade.codigo_concessionaria,
                concessionarias,
            )
        )

    print(
        "\n=== UNIDADE CONSUMIDORA ==="
    )
    print(
        f"Código interno: {unidade.codigo}"
    )
    print(
        f"Número da UC: {unidade.numero_uc}"
    )
    print(
        f"Código do cliente: "
        f"{unidade.codigo_cliente}"
    )
    print(
        f"Concessionária: "
        f"{nome_concessionaria}"
    )
    print(
        f"Situação: {unidade.situacao.value}"
    )
    print(
        f"Tipo de ligação: "
        f"{unidade.tipo_ligacao.value}"
    )
    print(
        f"Carga instalada: "
        f"{unidade.carga_instalada_kw:.2f} kW"
    )

    print("\n--- TITULAR ---")
    print(
        f"Nome: {unidade.titular.nome}"
    )
    print(
        f"Documento: "
        f"{unidade.titular.documento}"
    )
    print(
        f"Tipo: {unidade.titular.tipo.value}"
    )

    print("\n--- ENDEREÇO ---")
    print(
        f"Logradouro: "
        f"{unidade.endereco.logradouro}, "
        f"{unidade.endereco.numero}"
    )
    print(
        f"Bairro: {unidade.endereco.bairro}"
    )
    print(
        f"Cidade/UF: "
        f"{unidade.endereco.cidade}/"
        f"{unidade.endereco.estado}"
    )
    print(
        f"CEP: {unidade.endereco.cep}"
    )

    if unidade.endereco.complemento:
        print(
            f"Complemento: "
            f"{unidade.endereco.complemento}"
        )

    print(
        f"\nData de cadastro: "
        f"{unidade.data_cadastro.strftime('%d/%m/%Y %H:%M')}"
    )

    print(
        f"Última atualização: "
        f"{unidade.data_atualizacao.strftime('%d/%m/%Y %H:%M')}"
    )

    print(
        f"Alterações registradas: "
        f"{len(unidade.historico_alteracoes)}"
    )


def listar_unidades_consumidoras(
    unidades_consumidoras,
    concessionarias=None,
):
    """
    Exibe todas as Unidades Consumidoras
    cadastradas.

    Retorna a própria lista recebida.
    """

    if not unidades_consumidoras:
        print(
            "\nNenhuma Unidade Consumidora "
            "cadastrada."
        )

        return []

    print(
        "\n=== UNIDADES CONSUMIDORAS CADASTRADAS ==="
    )

    for unidade in unidades_consumidoras:
        exibir_unidade_consumidora(
            unidade,
            concessionarias,
        )

    return unidades_consumidoras


def selecionar_unidade_por_codigo(
    unidades_consumidoras,
):
    """
    Solicita um código e retorna a Unidade
    Consumidora correspondente.

    Retorna None quando a Unidade não for encontrada.
    """

    if not unidades_consumidoras:
        print(
            "\nNenhuma Unidade Consumidora "
            "cadastrada."
        )

        return None

    codigo = utils.ler_int(
        "Digite o código da Unidade Consumidora: "
    )

    unidade = buscar_unidade_por_codigo(
        unidades_consumidoras,
        codigo,
    )

    if unidade is None:
        print(
            "\nUnidade Consumidora não encontrada."
        )

    return unidade


def buscar_unidade_consumidora(
    unidades_consumidoras,
    concessionarias=None,
):
    """
    Permite buscar uma Unidade Consumidora
    por código interno ou pelo número da UC.

    Retorna a Unidade encontrada ou None.
    """

    if not unidades_consumidoras:
        print(
            "\nNenhuma Unidade Consumidora "
            "cadastrada."
        )

        return None

    print(
        "\n=== BUSCAR UNIDADE CONSUMIDORA ==="
    )
    print("1 - Buscar por código interno")
    print("2 - Buscar pelo número da UC")
    print("0 - Cancelar")

    opcao = input(
        "Escolha uma opção: "
    ).strip()

    if opcao == "1":
        codigo = utils.ler_int(
            "Digite o código interno: "
        )

        unidade = buscar_unidade_por_codigo(
            unidades_consumidoras,
            codigo,
        )

    elif opcao == "2":
        numero_uc = input(
            "Digite o número da UC: "
        ).strip()

        unidade = buscar_unidade_por_numero_uc(
            unidades_consumidoras,
            numero_uc,
        )

    elif opcao == "0":
        return None

    else:
        print(
            "\nOpção inválida."
        )
        return None

    if unidade is None:
        print(
            "\nUnidade Consumidora não encontrada."
        )
        return None

    exibir_unidade_consumidora(
        unidade,
        concessionarias,
    )

    return unidade


def alterar_situacao_unidade(
    unidades_consumidoras,
):
    """
    Permite ativar ou inativar uma
    Unidade Consumidora.

    Retorna a Unidade alterada ou None.
    """

    unidade = selecionar_unidade_por_codigo(
        unidades_consumidoras
    )

    if unidade is None:
        return None

    print(
        "\n=== ALTERAR SITUAÇÃO DA UNIDADE ==="
    )
    print(
        f"Situação atual: "
        f"{unidade.situacao.value}"
    )
    print("1 - Ativar")
    print("2 - Inativar")
    print("0 - Cancelar")

    opcao = input(
        "Escolha a nova situação: "
    ).strip()

    motivo = ""

    if opcao in ("1", "2"):
        motivo = input(
            "Motivo da alteração: "
        ).strip()

    if opcao == "1":
        alterou = unidade.ativar(
            motivo=motivo
        )

    elif opcao == "2":
        alterou = unidade.inativar(
            motivo=motivo
        )

    elif opcao == "0":
        return None

    else:
        print(
            "\nOpção inválida."
        )
        return None

    if not alterou:
        print(
            "\nA Unidade Consumidora já possui "
            "a situação selecionada."
        )

        return unidade

    salvar_unidades_consumidoras(
        unidades_consumidoras
    )

    print(
        "\nSituação da Unidade Consumidora "
        "alterada com sucesso."
    )

    return unidade