"""
Interface de Concessionárias.

Este módulo é responsável pela interação com o usuário.

Responsabilidades:

- solicitar dados pelo terminal;
- exibir Concessionárias;
- cadastrar Concessionárias;
- buscar Concessionárias;
- adicionar Áreas de Atuação;
- alterar a situação cadastral;
- solicitar a persistência dos dados.

As regras de negócio permanecem no domínio.
A leitura e gravação do JSON permanecem na infraestrutura.
"""

from app.dominio.concessionarias import (
    buscar_concessionaria_por_codigo,
    buscar_concessionarias_por_nome,
    criar_concessionaria,
    validar_duplicidade_concessionaria,
)
from app.dominio.erros_dominio import (
    DadosObrigatoriosAusentes,
    RegistroDuplicado,
    ValorInvalido,
)
from app.infraestrutura.repositorio_concessionarias_json import (
    salvar_concessionarias,
)
from app import utils


def exibir_concessionaria(concessionaria):
    """
    Exibe os dados de uma Concessionária.
    """

    print("\n--- CONCESSIONÁRIA ---")
    print(f"Código: {concessionaria.codigo}")
    print(f"Nome: {concessionaria.nome}")
    print(
        "Nome abreviado: "
        f"{concessionaria.nome_abreviado}"
    )

    cnpj = concessionaria.cnpj or "Não informado"

    print(f"CNPJ: {cnpj}")
    print(
        "Situação: "
        f"{concessionaria.situacao.value}"
    )
    print(
        "Data de cadastro: "
        f"{concessionaria.data_cadastro}"
    )
    print(
        "Última atualização: "
        f"{concessionaria.data_atualizacao}"
    )

    if not concessionaria.areas_atuacao:
        print("Áreas de atuação: nenhuma cadastrada")
        return

    print("Áreas de atuação:")

    for indice, area in enumerate(
        concessionaria.areas_atuacao,
        start=1,
    ):
        situacao_area = (
            "ATIVA"
            if area.ativa
            else "INATIVA"
        )

        print(
            f"  {indice}. "
            f"{area.estado} / "
            f"{area.municipio} "
            f"({situacao_area})"
        )


def listar_concessionarias(lista_concessionarias):
    """
    Exibe todas as Concessionárias cadastradas.
    """

    if not lista_concessionarias:
        print("\nNenhuma Concessionária cadastrada.")
        return

    print("\n=== CONCESSIONÁRIAS CADASTRADAS ===")

    for concessionaria in lista_concessionarias:
        print(
            f"{concessionaria.codigo} - "
            f"{concessionaria.nome_abreviado} - "
            f"{concessionaria.situacao.value}"
        )


def cadastrar_concessionaria(
    lista_concessionarias,
):
    """
    Solicita os dados e cadastra uma nova Concessionária.

    Após o cadastro, salva a lista no repositório JSON.

    Retorna a Concessionária criada quando o cadastro
    for concluído.

    Retorna None quando ocorrer erro de validação.
    """

    print("\n=== CADASTRAR CONCESSIONÁRIA ===")

    try:
        codigo = utils.gerar_proximo_codigo(
            lista_concessionarias
        )

        nome = input(
            "Nome completo da Concessionária: "
        )

        nome_abreviado = input(
            "Nome abreviado da Concessionária: "
        )

        cnpj = input(
            "CNPJ, apenas se disponível: "
        )

        validar_duplicidade_concessionaria(
            lista_concessionarias,
            codigo=codigo,
            cnpj=cnpj,
        )

        concessionaria = criar_concessionaria(
            codigo=codigo,
            nome=nome,
            nome_abreviado=nome_abreviado,
            cnpj=cnpj,
        )

        lista_concessionarias.append(
            concessionaria
        )

        salvar_concessionarias(
            lista_concessionarias
        )

        print(
            "\nConcessionária cadastrada "
            "com sucesso."
        )

        return concessionaria

    except (
        DadosObrigatoriosAusentes,
        RegistroDuplicado,
        ValorInvalido,
    ) as erro:
        print(f"\nErro: {erro}")
        return None


def selecionar_concessionaria_por_codigo(
    lista_concessionarias,
):
    """
    Solicita um código e retorna a Concessionária
    correspondente.

    Retorna None quando a Concessionária não existir.
    """

    codigo = utils.ler_int(
        "Informe o código da Concessionária: "
    )

    concessionaria = (
        buscar_concessionaria_por_codigo(
            lista_concessionarias,
            codigo,
        )
    )

    if concessionaria is None:
        print(
            "\nConcessionária não encontrada."
        )
        return None

    return concessionaria


def buscar_concessionaria(
    lista_concessionarias,
):
    """
    Permite buscar Concessionárias por código ou nome.
    """

    print("\n=== BUSCAR CONCESSIONÁRIA ===")
    print("1 - Buscar por código")
    print("2 - Buscar por nome")
    print("0 - Voltar")

    opcao = input("Escolha uma opção: ").strip()

    if opcao == "0":
        return None

    if opcao == "1":
        concessionaria = (
            selecionar_concessionaria_por_codigo(
                lista_concessionarias
            )
        )

        if concessionaria is not None:
            exibir_concessionaria(
                concessionaria
            )

        return concessionaria

    if opcao == "2":
        nome = input(
            "Informe o nome ou parte do nome: "
        )

        try:
            resultados = (
                buscar_concessionarias_por_nome(
                    lista_concessionarias,
                    nome,
                )
            )

        except DadosObrigatoriosAusentes as erro:
            print(f"\nErro: {erro}")
            return []

        if not resultados:
            print(
                "\nNenhuma Concessionária encontrada."
            )
            return []

        for concessionaria in resultados:
            exibir_concessionaria(
                concessionaria
            )

        return resultados

    print("\nOpção inválida.")
    return None


def adicionar_area_atuacao(
    lista_concessionarias,
):
    """
    Adiciona uma Área de Atuação a uma Concessionária.
    """

    print("\n=== ADICIONAR ÁREA DE ATUAÇÃO ===")

    concessionaria = (
        selecionar_concessionaria_por_codigo(
            lista_concessionarias
        )
    )

    if concessionaria is None:
        return None

    estado = input("Estado: ")
    municipio = input("Município: ")

    try:
        area = concessionaria.adicionar_area_atuacao(
            estado=estado,
            municipio=municipio,
        )

        salvar_concessionarias(
            lista_concessionarias
        )

        print(
            "\nÁrea de Atuação adicionada "
            "com sucesso."
        )

        return area

    except (
        DadosObrigatoriosAusentes,
        RegistroDuplicado,
    ) as erro:
        print(f"\nErro: {erro}")
        return None


def alterar_situacao_concessionaria(
    lista_concessionarias,
):
    """
    Permite ativar, inativar ou suspender
    uma Concessionária.
    """

    print(
        "\n=== ALTERAR SITUAÇÃO "
        "DA CONCESSIONÁRIA ==="
    )

    concessionaria = (
        selecionar_concessionaria_por_codigo(
            lista_concessionarias
        )
    )

    if concessionaria is None:
        return None

    print(
        "\nSituação atual: "
        f"{concessionaria.situacao.value}"
    )
    print("1 - Ativar")
    print("2 - Inativar")
    print("3 - Suspender")
    print("0 - Voltar")

    opcao = input("Escolha uma opção: ").strip()

    if opcao == "0":
        return None

    if opcao == "1":
        concessionaria.ativar()

    elif opcao == "2":
        concessionaria.inativar()

    elif opcao == "3":
        concessionaria.suspender()

    else:
        print("\nOpção inválida.")
        return None

    salvar_concessionarias(
        lista_concessionarias
    )

    print(
        "\nSituação alterada com sucesso."
    )

    return concessionaria


def alterar_situacao_area_atuacao(
    lista_concessionarias,
):
    """
    Permite ativar ou inativar uma Área de Atuação.
    """

    print(
        "\n=== ALTERAR SITUAÇÃO "
        "DA ÁREA DE ATUAÇÃO ==="
    )

    concessionaria = (
        selecionar_concessionaria_por_codigo(
            lista_concessionarias
        )
    )

    if concessionaria is None:
        return None

    if not concessionaria.areas_atuacao:
        print(
            "\nA Concessionária não possui "
            "Áreas de Atuação cadastradas."
        )
        return None

    exibir_concessionaria(concessionaria)

    estado = input(
        "\nInforme o estado da Área: "
    )

    municipio = input(
        "Informe o município da Área: "
    )

    area = concessionaria.buscar_area_atuacao(
        estado=estado,
        municipio=municipio,
    )

    if area is None:
        print(
            "\nÁrea de Atuação não encontrada."
        )
        return None

    print(
        "\nSituação atual da Área: "
        f"{'ATIVA' if area.ativa else 'INATIVA'}"
    )
    print("1 - Ativar")
    print("2 - Inativar")
    print("0 - Voltar")

    opcao = input("Escolha uma opção: ").strip()

    try:
        if opcao == "0":
            return None

        if opcao == "1":
            area_atualizada = (
                concessionaria.ativar_area_atuacao(
                    estado=estado,
                    municipio=municipio,
                )
            )

        elif opcao == "2":
            area_atualizada = (
                concessionaria.inativar_area_atuacao(
                    estado=estado,
                    municipio=municipio,
                )
            )

        else:
            print("\nOpção inválida.")
            return None

        salvar_concessionarias(
            lista_concessionarias
        )

        print(
            "\nSituação da Área de Atuação "
            "alterada com sucesso."
        )

        return area_atualizada

    except ValorInvalido as erro:
        print(f"\nErro: {erro}")
        return None


def menu_concessionarias(
    lista_concessionarias,
):
    """
    Exibe o menu de gerenciamento
    das Concessionárias.
    """

    while True:
        print("\n=== MENU CONCESSIONÁRIAS ===")
        print("1 - Cadastrar Concessionária")
        print("2 - Listar Concessionárias")
        print("3 - Buscar Concessionária")
        print("4 - Adicionar Área de Atuação")
        print("5 - Alterar situação da Concessionária")
        print("6 - Alterar situação de Área de Atuação")
        print("0 - Voltar")

        opcao = input(
            "Escolha uma opção: "
        ).strip()

        if opcao == "1":
            cadastrar_concessionaria(
                lista_concessionarias
            )

        elif opcao == "2":
            listar_concessionarias(
                lista_concessionarias
            )

        elif opcao == "3":
            buscar_concessionaria(
                lista_concessionarias
            )

        elif opcao == "4":
            adicionar_area_atuacao(
                lista_concessionarias
            )

        elif opcao == "5":
            alterar_situacao_concessionaria(
                lista_concessionarias
            )

        elif opcao == "6":
            alterar_situacao_area_atuacao(
                lista_concessionarias
            )

        elif opcao == "0":
            break

        else:
            print("\nOpção inválida.")