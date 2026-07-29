"""
Repositório JSON de empresas.

Este módulo pertence à camada de infraestrutura.

Responsabilidades:
- carregar empresas do arquivo JSON;
- salvar empresas no arquivo JSON;
- garantir que o arquivo e a pasta existam;
- validar minimamente a estrutura carregada.

Este módulo não contém regras de negócio da entidade Empresa.
"""

import json
from pathlib import Path
from typing import Any


# ============================================================
# CAMINHO PADRÃO DO ARQUIVO
# ============================================================

CAMINHO_PADRAO_EMPRESAS = (
    Path(__file__).resolve().parents[2]
    / "data"
    / "empresas.json"
)


# ============================================================
# FUNÇÕES AUXILIARES INTERNAS
# ============================================================

def _garantir_diretorio(
    caminho_arquivo: Path,
) -> None:
    """
    Garante que a pasta onde o arquivo será salvo exista.

    Exemplo:

        data/empresas.json

    Caso a pasta data ainda não exista, ela será criada.
    """

    caminho_arquivo.parent.mkdir(
        parents=True,
        exist_ok=True,
    )


def _criar_arquivo_vazio(
    caminho_arquivo: Path,
) -> None:
    """
    Cria um arquivo JSON contendo uma lista vazia.
    """

    _garantir_diretorio(
        caminho_arquivo,
    )

    with caminho_arquivo.open(
        mode="w",
        encoding="utf-8",
    ) as arquivo:
        json.dump(
            [],
            arquivo,
            ensure_ascii=False,
            indent=4,
        )


def _validar_dados_carregados(
    dados: Any,
) -> list[dict[str, Any]]:
    """
    Valida minimamente os dados obtidos do arquivo JSON.

    O arquivo de empresas deve possuir, em sua raiz, uma lista.

    Cada item dessa lista deve ser um dicionário.

    Esta validação pertence à infraestrutura porque verifica
    o formato do arquivo, não as regras completas da Empresa.
    """

    if not isinstance(dados, list):
        raise ValueError(
            "O arquivo de empresas deve conter uma lista."
        )

    for indice, empresa in enumerate(
        dados,
        start=1,
    ):
        if not isinstance(empresa, dict):
            raise ValueError(
                "Cada empresa do arquivo deve ser um objeto. "
                f"Item inválido na posição {indice}."
            )

    return dados


# ============================================================
# FUNÇÕES PÚBLICAS DO REPOSITÓRIO
# ============================================================

def carregar_empresas(
    caminho_arquivo: str | Path | None = None,
) -> list[dict[str, Any]]:
    """
    Carrega e retorna as empresas armazenadas em JSON.

    Quando nenhum caminho é informado, utiliza:

        data/empresas.json

    Caso o arquivo ainda não exista:
    - cria o arquivo;
    - grava uma lista vazia;
    - retorna uma lista vazia.
    """

    caminho = Path(
        caminho_arquivo
        if caminho_arquivo is not None
        else CAMINHO_PADRAO_EMPRESAS
    )

    if not caminho.exists():
        _criar_arquivo_vazio(
            caminho,
        )

        return []

    try:
        with caminho.open(
            mode="r",
            encoding="utf-8",
        ) as arquivo:
            dados = json.load(
                arquivo,
            )

    except json.JSONDecodeError as erro:
        raise ValueError(
            "O arquivo de empresas contém JSON inválido."
        ) from erro

    return _validar_dados_carregados(
        dados,
    )


def salvar_empresas(
    empresas: list[dict[str, Any]],
    caminho_arquivo: str | Path | None = None,
) -> None:
    """
    Salva a lista de empresas em um arquivo JSON.

    Quando nenhum caminho é informado, utiliza:

        data/empresas.json
    """

    if not isinstance(empresas, list):
        raise TypeError(
            "As empresas devem ser fornecidas em uma lista."
        )

    for indice, empresa in enumerate(
        empresas,
        start=1,
    ):
        if not isinstance(empresa, dict):
            raise TypeError(
                "Cada empresa deve ser representada "
                "por um dicionário. "
                f"Item inválido na posição {indice}."
            )

    caminho = Path(
        caminho_arquivo
        if caminho_arquivo is not None
        else CAMINHO_PADRAO_EMPRESAS
    )

    _garantir_diretorio(
        caminho,
    )

    with caminho.open(
        mode="w",
        encoding="utf-8",
    ) as arquivo:
        json.dump(
            empresas,
            arquivo,
            ensure_ascii=False,
            indent=4,
        )