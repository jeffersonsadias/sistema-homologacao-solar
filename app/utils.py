def ler_float(mensagem):
    """
    Lê um número decimal digitado pelo usuário.
    Aceita vírgula ou ponto.
    """

    while True:

        entrada = input(mensagem)

        entrada = entrada.replace(",", ".")

        try:

            valor = float(entrada)
            return valor

        except ValueError:

            print("Valor inválido. Digite novamente.")

def gerar_proximo_codigo(registros):
    """
    Retorna o próximo código disponível de uma lista de registros.
    Cada registro deve possuir a chave 'codigo'.
    """

    if not registros:
        return 1

    maior_codigo = max(registro["codigo"] for registro in registros)

    return maior_codigo + 1

def ler_int(mensagem):
    """
    Lê um número inteiro digitado pelo usuário.
    Repete a pergunta enquanto o valor informado for inválido.
    """

    while True:
        entrada = input(mensagem)

        try:
            valor = int(entrada)
            return valor

        except ValueError:
            print("Valor inválido. Digite um número inteiro.")