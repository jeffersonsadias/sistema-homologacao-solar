"""
Experimentos sobre objetos, referências e mutabilidade em Python.

Este módulo é apenas didático e não faz parte do funcionamento
principal do Sistema de Homologação Solar.
"""


print("\n=== EXPERIMENTO 1: DUAS REFERÊNCIAS PARA O MESMO OBJETO ===")

cliente = {
    "nome": "Jefferson"
}

clientes = []

clientes.append(cliente)

print("\nObjeto acessado pela variável cliente:")
print(cliente)

print("\nObjeto acessado pela lista clientes:")
print(clientes[0])

print("\nIdentificador do objeto pela variável cliente:")
print(id(cliente))

print("\nIdentificador do objeto dentro da lista:")
print(id(clientes[0]))

print("\n=== EXPERIMENTO 2: ALTERAÇÃO DO OBJETO EXISTENTE ===")

cliente["nome"] = "Carlos"

print("\nValor acessado pela variável cliente:")
print(cliente)

print("\nValor acessado pela lista clientes:")
print(clientes[0])

print("\nIdentificadores depois da alteração:")
print("cliente:", id(cliente))
print("clientes[0]:", id(clientes[0]))

print("\n=== EXPERIMENTO 3: CRIAÇÃO DE UM NOVO OBJETO ===")

cliente = {
    "nome": "Amanda"
}

print("\nNovo objeto acessado pela variável cliente:")
print(cliente)

print("\nObjeto antigo ainda acessado pela lista:")
print(clientes[0])

print("\nIdentificador do novo objeto:")
print("cliente:", id(cliente))

print("\nIdentificador do objeto antigo:")
print("clientes[0]:", id(clientes[0]))

print("\n=== EXPERIMENTO 4: ATRIBUIÇÃO NÃO É CÓPIA ===")

cliente_original = {
    "nome": "Jefferson",
    "cidade": "Caetité"
}

cliente_apontando_mesmo_objeto = cliente_original

cliente_apontando_mesmo_objeto["cidade"] = "Salvador"

print("\ncliente_original:")
print(cliente_original)

print("\ncliente_apontando_mesmo_objeto:")
print(cliente_apontando_mesmo_objeto)

print("\nIDs:")
print("cliente_original:", id(cliente_original))
print(
    "cliente_apontando_mesmo_objeto:",
    id(cliente_apontando_mesmo_objeto)
)

print("\n=== EXPERIMENTO 5: CÓPIA RASA DE DICIONÁRIO ===")

cliente_original = {
    "nome": "Jefferson",
    "cidade": "Caetité"
}

cliente_copia = cliente_original.copy()

cliente_copia["cidade"] = "Salvador"

print("\ncliente_original:")
print(cliente_original)

print("\ncliente_copia:")
print(cliente_copia)

print("\nIDs:")
print("cliente_original:", id(cliente_original))
print("cliente_copia:", id(cliente_copia))

print("\n=== EXPERIMENTO 6: A ARMADILHA DO COPY() ===")

cliente_original = {

    "nome": "Jefferson",

    "telefones": [
        "77999999999",
        "7733333333"
    ]

}

cliente_copia = cliente_original.copy()

print("\nAntes da alteração:")

print(cliente_original)
print(cliente_copia)

cliente_copia["telefones"].append("77111111111")

print("\nDepois da alteração:")

print(cliente_original)
print(cliente_copia)

print("\nIDs dos dicionários:")

print(id(cliente_original))
print(id(cliente_copia))

print("\nIDs da lista telefones:")

print(id(cliente_original["telefones"]))
print(id(cliente_copia["telefones"]))