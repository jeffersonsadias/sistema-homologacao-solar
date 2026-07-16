import json
import os


PASTA_APP = os.path.dirname(os.path.abspath(__file__))

PASTA_PROJETO = os.path.dirname(PASTA_APP)

PASTA_DADOS = os.path.join(PASTA_PROJETO, "data")


os.makedirs(PASTA_DADOS, exist_ok=True)

def salvar_dados(nome_arquivo, dados):
    """
    Salva uma lista ou dicionário em um arquivo JSON.
    """

    caminho_arquivo = os.path.join(PASTA_DADOS, nome_arquivo) 

    with open(caminho_arquivo, "w", encoding="utf-8") as arquivo:
        json.dump(dados, arquivo, ensure_ascii=False, indent=4)

def carregar_dados(nome_arquivo):
    """
    Carrega os dados de um arquivo JSON.
    """

    caminho_arquivo = os.path.join(PASTA_DADOS, nome_arquivo)

    if not os.path.exists(caminho_arquivo):
        return []

    with open(caminho_arquivo, "r", encoding="utf-8") as arquivo:
        return json.load(arquivo)