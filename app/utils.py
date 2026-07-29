"""
Funções utilitárias do sistema.

Este módulo reúne funções reutilizadas por diferentes partes
da aplicação.

Responsabilidades:

- leitura segura de números;
- geração de códigos sequenciais;
- pequenas rotinas auxiliares.

Este módulo não contém regras de negócio.
"""


def ler_int(mensagem):
    """
    Solicita ao usuário um número inteiro.

    Continua solicitando enquanto o valor informado
    não puder ser convertido para inteiro.

    Retorna um int.
    """

    while True:
        valor = input(mensagem).strip()

        try:
            return int(valor)

        except ValueError:
            print(
                "Valor inválido. "
                "Informe um número inteiro."
            )


def ler_float(mensagem):
    """
    Solicita ao usuário um número decimal.

    Aceita tanto vírgula quanto ponto como
    separador decimal.

    Exemplos válidos:

        10
        10.5
        10,5

    Retorna um float.
    """

    while True:
        valor = input(mensagem).strip()

        valor = valor.replace(",", ".")

        try:
            return float(valor)

        except ValueError:
            print(
                "Valor inválido. "
                "Informe um número."
            )


def gerar_proximo_codigo(lista):
    """
    Gera o próximo código numérico disponível.

    Compatível com:

    - listas de dicionários;
    - listas de objetos.

    Espera encontrar:

    dicionários:
        {"codigo": 10}

    objetos:
        objeto.codigo

    Quando a lista estiver vazia,
    retorna 1.
    """

    if not lista:
        return 1

    codigos = []

    for item in lista:

        if isinstance(item, dict):
            codigo = item["codigo"]

        else:
            codigo = item.codigo

        codigos.append(codigo)

    return max(codigos) + 1


def pausar():
    """
    Aguarda o usuário pressionar ENTER.

    Utilizada ao final de telas do menu.
    """

    input("\nPressione ENTER para continuar...")


def limpar_texto(texto):
    """
    Remove espaços excedentes do início
    e do fim de um texto.

    Retorna uma string.
    """

    return str(texto).strip()


def texto_vazio(texto):
    """
    Verifica se um texto está vazio.

    Retorna:

        True
        False
    """

    return limpar_texto(texto) == ""


def somente_digitos(texto):
    """
    Retorna apenas os caracteres numéricos
    presentes em um texto.

    Exemplos:

        "(77) 99999-9999"

    torna-se:

        "77999999999"
    """

    return "".join(
        caractere
        for caractere in str(texto)
        if caractere.isdigit()
    )