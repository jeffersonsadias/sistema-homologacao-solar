"""
Interface de terminal dos vínculos entre
Projetos e Unidades Consumidoras.

Esta camada é responsável por:

- receber dados digitados pelo usuário;
- chamar a fachada pública;
- exibir resultados e mensagens;
- tratar erros esperados de domínio.
"""

from app import vinculos_unidade_projeto
from app.dominio.status import (
    PapelUnidadeProjeto,
)


def _ler_codigo(
    mensagem,
):
    """
    Solicita um código inteiro positivo.

    Continua pedindo enquanto o usuário
    informar um valor inválido.
    """

    while True:
        valor_digitado = input(
            mensagem
        ).strip()

        try:
            codigo = int(
                valor_digitado
            )

            if codigo <= 0:
                print(
                    "\nO código deve ser "
                    "maior que zero."
                )
                continue

            return codigo

        except ValueError:
            print(
                "\nDigite um número inteiro "
                "válido."
            )


def _ler_observacoes():
    """
    Solicita observações opcionais.

    O usuário pode pressionar Enter
    para deixar o campo vazio.
    """

    return input(
        "Observações, se houver: "
    ).strip()


def _selecionar_papel_unidade():
    """
    Exibe as opções de papel da Unidade
    Consumidora dentro do Projeto.

    Retorna um membro do enum
    PapelUnidadeProjeto.
    """

    while True:
        print(
            "\nPapel da Unidade no Projeto"
        )

        print(
            "1 - Unidade Geradora"
        )

        print(
            "2 - Unidade Beneficiária"
        )

        opcao = input(
            "Escolha uma opção: "
        ).strip()

        if opcao == "1":
            return (
                PapelUnidadeProjeto.GERADORA
            )

        if opcao == "2":
            return (
                PapelUnidadeProjeto.BENEFICIARIA
            )

        print(
            "\nOpção inválida."
        )


def cadastrar_vinculo():
    """
    Fluxo de terminal para vincular
    uma Unidade Consumidora a um Projeto.
    """

    print(
        "\n=== VINCULAR UNIDADE "
        "CONSUMIDORA AO PROJETO ==="
    )

    codigo_projeto = _ler_codigo(
        "Código do Projeto: "
    )

    codigo_unidade = _ler_codigo(
        "Código da Unidade Consumidora: "
    )

    papel = _selecionar_papel_unidade()

    observacoes = _ler_observacoes()

    try:
        if (
            papel
            == PapelUnidadeProjeto.GERADORA
        ):
            vinculo = (
                vinculos_unidade_projeto
                .vincular_unidade_geradora(
                    codigo_projeto=(
                        codigo_projeto
                    ),
                    codigo_unidade_consumidora=(
                        codigo_unidade
                    ),
                    observacoes=observacoes,
                )
            )

        else:
            vinculo = (
                vinculos_unidade_projeto
                .vincular_unidade_beneficiaria(
                    codigo_projeto=(
                        codigo_projeto
                    ),
                    codigo_unidade_consumidora=(
                        codigo_unidade
                    ),
                    observacoes=observacoes,
                )
            )

        print(
            "\nVínculo cadastrado "
            "com sucesso."
        )

        mostrar_vinculo(
            vinculo
        )

        return vinculo

    except ValueError as erro:
        print(
            f"\nNão foi possível criar "
            f"o vínculo: {erro}"
        )

        return None


def mostrar_vinculo(
    vinculo,
):
    """
    Exibe os dados de um único vínculo
    de forma organizada no terminal.

    A função recebe o objeto já localizado
    e não realiza novas buscas.
    """

    if vinculo is None:
        print(
            "\nVínculo não encontrado."
        )
        return

    nomes_papeis = {
        PapelUnidadeProjeto.GERADORA: (
            "Unidade Geradora"
        ),
        PapelUnidadeProjeto.BENEFICIARIA: (
            "Unidade Beneficiária"
        ),
    }

    nome_papel = nomes_papeis.get(
        vinculo.papel,
        vinculo.papel.value,
    )

    data_vinculo_formatada = (
        vinculo.data_vinculo.strftime(
            "%d/%m/%Y às %H:%M"
        )
    )

    data_atualizacao_formatada = (
        vinculo.data_atualizacao.strftime(
            "%d/%m/%Y às %H:%M"
        )
    )

    observacoes = (
        vinculo.observacoes
        if vinculo.observacoes
        else "Nenhuma"
    )

    print(
        "\n----------------------------"
    )

    print(
        f"Código do vínculo: "
        f"{vinculo.codigo}"
    )

    print(
        f"Código do Projeto: "
        f"{vinculo.codigo_projeto}"
    )

    print(
        f"Código da Unidade Consumidora: "
        f"{vinculo.codigo_unidade_consumidora}"
    )

    print(
        f"Papel no Projeto: "
        f"{nome_papel}"
    )

    print(
        f"Situação: "
        f"{vinculo.situacao.value}"
    )

    print(
        f"Data do vínculo: "
        f"{data_vinculo_formatada}"
    )

    print(
        f"Última atualização: "
        f"{data_atualizacao_formatada}"
    )

    print(
        f"Observações: "
        f"{observacoes}"
    )

    print(
        "----------------------------"
    )


def listar_vinculos_do_projeto():
    """
    Solicita o código de um Projeto
    e exibe todos os vínculos ativos.
    """

    print(
        "\n=== VÍNCULOS DO PROJETO ==="
    )

    codigo_projeto = _ler_codigo(
        "Código do Projeto: "
    )

    vinculos = (
        vinculos_unidade_projeto
        .listar_vinculos_do_projeto(
            codigo_projeto=codigo_projeto,
            somente_ativos=True,
        )
    )

    if not vinculos:
        print(
            "\nNenhum vínculo ativo "
            "foi encontrado para o Projeto."
        )
        return []

    print(
        f"\nTotal de vínculos ativos: "
        f"{len(vinculos)}"
    )

    for vinculo in vinculos:
        mostrar_vinculo(
            vinculo
        )

    return vinculos


def mostrar_unidade_geradora_do_projeto():
    """
    Solicita o código de um Projeto
    e exibe sua Unidade Geradora ativa.
    """

    print(
        "\n=== UNIDADE GERADORA "
        "DO PROJETO ==="
    )

    codigo_projeto = _ler_codigo(
        "Código do Projeto: "
    )

    vinculo = (
        vinculos_unidade_projeto
        .obter_unidade_geradora_do_projeto(
            codigo_projeto
        )
    )

    if vinculo is None:
        print(
            "\nO Projeto não possui "
            "Unidade Geradora ativa."
        )
        return None

    mostrar_vinculo(
        vinculo
    )

    return vinculo


def listar_unidades_beneficiarias_do_projeto():
    """
    Solicita o código de um Projeto
    e exibe suas Unidades Beneficiárias.
    """

    print(
        "\n=== UNIDADES BENEFICIÁRIAS "
        "DO PROJETO ==="
    )

    codigo_projeto = _ler_codigo(
        "Código do Projeto: "
    )

    vinculos = (
        vinculos_unidade_projeto
        .listar_unidades_beneficiarias_do_projeto(
            codigo_projeto
        )
    )

    if not vinculos:
        print(
            "\nO Projeto não possui "
            "Unidades Beneficiárias ativas."
        )
        return []

    print(
        f"\nTotal de beneficiárias: "
        f"{len(vinculos)}"
    )

    for vinculo in vinculos:
        mostrar_vinculo(
            vinculo
        )

    return vinculos


def inativar_vinculo():
    """
    Solicita o código de um vínculo
    e realiza sua inativação.
    """

    print(
        "\n=== INATIVAR VÍNCULO ==="
    )

    codigo = _ler_codigo(
        "Código do vínculo: "
    )

    vinculo = (
        vinculos_unidade_projeto
        .inativar_vinculo(
            codigo
        )
    )

    if vinculo is None:
        print(
            "\nVínculo não encontrado."
        )
        return None

    print(
        "\nVínculo inativado "
        "com sucesso."
    )

    mostrar_vinculo(
        vinculo
    )

    return vinculo


def ativar_vinculo():
    """
    Solicita o código de um vínculo
    e tenta realizar sua ativação.
    """

    print(
        "\n=== ATIVAR VÍNCULO ==="
    )

    codigo = _ler_codigo(
        "Código do vínculo: "
    )

    try:
        vinculo = (
            vinculos_unidade_projeto
            .ativar_vinculo(
                codigo
            )
        )

        if vinculo is None:
            print(
                "\nVínculo não encontrado."
            )
            return None

        print(
            "\nVínculo ativado "
            "com sucesso."
        )

        mostrar_vinculo(
            vinculo
        )

        return vinculo

    except ValueError as erro:
        print(
            f"\nNão foi possível ativar "
            f"o vínculo: {erro}"
        )

        return None


def alterar_observacoes():
    """
    Solicita o código de um vínculo
    e altera suas observações.
    """

    print(
        "\n=== ALTERAR OBSERVAÇÕES "
        "DO VÍNCULO ==="
    )

    codigo = _ler_codigo(
        "Código do vínculo: "
    )

    novas_observacoes = input(
        "Novas observações: "
    ).strip()

    vinculo = (
        vinculos_unidade_projeto
        .alterar_observacoes(
            codigo,
            novas_observacoes,
        )
    )

    if vinculo is None:
        print(
            "\nVínculo não encontrado."
        )
        return None

    print(
        "\nObservações alteradas "
        "com sucesso."
    )

    mostrar_vinculo(
        vinculo
    )

    return vinculo


def menu_vinculos_unidade_projeto():
    """
    Menu específico do módulo de vínculos.

    Mantém o usuário no submenu até que
    ele escolha a opção de retorno.
    """

    while True:
        print(
            "\n=== VÍNCULOS ENTRE PROJETOS "
            "E UNIDADES CONSUMIDORAS ==="
        )

        print(
            "1 - Cadastrar vínculo"
        )

        print(
            "2 - Listar vínculos de um Projeto"
        )

        print(
            "3 - Mostrar Unidade Geradora"
        )

        print(
            "4 - Listar Unidades Beneficiárias"
        )

        print(
            "5 - Inativar vínculo"
        )

        print(
            "6 - Ativar vínculo"
        )

        print(
            "7 - Alterar observações"
        )

        print(
            "0 - Voltar"
        )

        opcao = input(
            "Escolha uma opção: "
        ).strip()

        if opcao == "1":
            cadastrar_vinculo()

        elif opcao == "2":
            listar_vinculos_do_projeto()

        elif opcao == "3":
            mostrar_unidade_geradora_do_projeto()

        elif opcao == "4":
            (
                listar_unidades_beneficiarias_do_projeto()
            )

        elif opcao == "5":
            inativar_vinculo()

        elif opcao == "6":
            ativar_vinculo()

        elif opcao == "7":
            alterar_observacoes()

        elif opcao == "0":
            return

        else:
            print(
                "\nOpção inválida."
            )