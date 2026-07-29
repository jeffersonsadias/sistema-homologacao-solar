"""
Repositório JSON dos vínculos entre
Projetos e Unidades Consumidoras.

Este módulo é responsável por:

- salvar os vínculos em arquivo JSON;
- carregar os vínculos do arquivo;
- converter objetos do domínio em dicionários;
- reconstruir objetos do domínio.
"""

import json
from datetime import datetime
from pathlib import Path

from app.dominio.status import (
    PapelUnidadeProjeto,
)

from app.dominio.vinculos_unidade_projeto import (
    SituacaoVinculoUnidadeProjeto,
    VinculoUnidadeProjeto,
)


CAMINHO_ARQUIVO = Path(
    "data/vinculos_unidade_projeto.json"
)


def salvar_vinculos_unidade_projeto(
    vinculos,
    caminho_arquivo=CAMINHO_ARQUIVO,
):
    """
    Salva a lista de vínculos
    em um arquivo JSON.
    """

    caminho_arquivo = Path(
        caminho_arquivo
    )

    caminho_arquivo.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    dados = []

    for vinculo in vinculos:
        dados.append(
            converter_vinculo_para_dicionario(
                vinculo
            )
        )

    with caminho_arquivo.open(
        "w",
        encoding="utf-8",
    ) as arquivo:
        json.dump(
            dados,
            arquivo,
            ensure_ascii=False,
            indent=4,
        )


def carregar_vinculos_unidade_projeto(
    caminho_arquivo=CAMINHO_ARQUIVO,
):
    """
    Carrega os vínculos armazenados
    no arquivo JSON.

    Retorna uma lista vazia quando:

    - o arquivo não existe;
    - o arquivo está vazio;
    - o conteúdo JSON é inválido.
    """

    caminho_arquivo = Path(
        caminho_arquivo
    )

    if not caminho_arquivo.exists():
        return []

    try:
        with caminho_arquivo.open(
            "r",
            encoding="utf-8",
        ) as arquivo:
            conteudo = arquivo.read()

        if not conteudo.strip():
            return []

        dados = json.loads(
            conteudo
        )

    except (
        json.JSONDecodeError,
        OSError,
    ):
        return []

    vinculos = []

    for dados_vinculo in dados:
        vinculo = (
            reconstruir_vinculo_do_dicionario(
                dados_vinculo
            )
        )

        vinculos.append(
            vinculo
        )

    return vinculos


def converter_vinculo_para_dicionario(
    vinculo,
):
    """
    Converte um objeto VinculoUnidadeProjeto
    em um dicionário compatível com JSON.
    """

    return {
        "codigo": vinculo.codigo,
        "codigo_projeto": (
            vinculo.codigo_projeto
        ),
        "codigo_unidade_consumidora": (
            vinculo.codigo_unidade_consumidora
        ),
        "papel": vinculo.papel.value,
        "situacao": vinculo.situacao.value,
        "data_vinculo": (
            vinculo.data_vinculo.isoformat()
        ),
        "data_atualizacao": (
            vinculo.data_atualizacao.isoformat()
        ),
        "observacoes": vinculo.observacoes,
    }


def reconstruir_vinculo_do_dicionario(
    dados,
):
    """
    Reconstrói um VinculoUnidadeProjeto
    a partir de um dicionário.
    """

    return VinculoUnidadeProjeto(
        codigo=dados["codigo"],
        codigo_projeto=(
            dados["codigo_projeto"]
        ),
        codigo_unidade_consumidora=(
            dados[
                "codigo_unidade_consumidora"
            ]
        ),
        papel=PapelUnidadeProjeto(
            dados["papel"]
        ),
        situacao=(
            SituacaoVinculoUnidadeProjeto(
                dados["situacao"]
            )
        ),
        data_vinculo=datetime.fromisoformat(
            dados["data_vinculo"]
        ),
        data_atualizacao=(
            datetime.fromisoformat(
                dados["data_atualizacao"]
            )
        ),
        observacoes=dados.get(
            "observacoes",
            "",
        ),
    )