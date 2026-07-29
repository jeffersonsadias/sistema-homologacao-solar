"""
Repositório JSON de Concessionárias.

Este módulo pertence à camada de infraestrutura.

Responsabilidades:

- carregar Concessionárias do arquivo JSON;
- reconstruir as entidades do domínio;
- converter as entidades para dicionários;
- salvar as Concessionárias no arquivo JSON.

Este módulo não deve:

- usar input();
- usar print();
- aplicar regras de interação com o usuário;
- duplicar regras de negócio do domínio.
"""

import json
from pathlib import Path

from app.dominio.concessionarias import (
    converter_concessionaria_para_dicionario,
    reconstruir_concessionaria,
)


CAMINHO_ARQUIVO = (
    Path(__file__).resolve().parents[2]
    / "data"
    / "concessionarias.json"
)


def carregar_concessionarias(
    caminho_arquivo=CAMINHO_ARQUIVO,
):
    """
    Carrega as Concessionárias armazenadas
    em um arquivo JSON.

    O caminho padrão é:

        data/concessionarias.json

    Comportamentos:

    - se o arquivo não existir, retorna uma lista vazia;
    - se o arquivo estiver vazio, retorna uma lista vazia;
    - se o arquivo contiver uma lista válida, reconstrói
      cada Concessionária;
    - se o conteúdo principal não for uma lista,
      lança ValueError;
    - se o JSON estiver malformado, o erro JSONDecodeError
      será propagado.

    Retorna uma lista de entidades Concessionaria.
    """

    caminho = Path(caminho_arquivo)

    if not caminho.exists():
        return []

    conteudo = caminho.read_text(
        encoding="utf-8"
    )

    if not conteudo.strip():
        return []

    dados_concessionarias = json.loads(
        conteudo
    )

    if not isinstance(
        dados_concessionarias,
        list,
    ):
        raise ValueError(
            "O arquivo de Concessionárias "
            "deve conter uma lista JSON."
        )

    concessionarias = []

    for dados in dados_concessionarias:
        if not isinstance(dados, dict):
            raise ValueError(
                "Cada Concessionária armazenada "
                "deve ser representada por um objeto JSON."
            )

        concessionaria = (
            reconstruir_concessionaria(
                codigo=dados.get("codigo"),
                nome=dados.get("nome"),
                nome_abreviado=dados.get(
                    "nome_abreviado"
                ),
                cnpj=dados.get("cnpj"),
                situacao=dados.get(
                    "situacao",
                    "ATIVA",
                ),
                areas_atuacao=dados.get(
                    "areas_atuacao",
                    [],
                ),
                data_cadastro=dados.get(
                    "data_cadastro"
                ),
                data_atualizacao=dados.get(
                    "data_atualizacao"
                ),
            )
        )

        concessionarias.append(
            concessionaria
        )

    return concessionarias


def salvar_concessionarias(
    concessionarias,
    caminho_arquivo=CAMINHO_ARQUIVO,
):
    """
    Salva uma coleção de Concessionárias
    em um arquivo JSON.

    Antes da gravação, cada entidade é convertida
    para um dicionário apropriado à persistência.

    O diretório do arquivo é criado automaticamente
    quando ainda não existir.

    Retorna o caminho do arquivo salvo.
    """

    caminho = Path(caminho_arquivo)

    caminho.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    dados_concessionarias = [
        converter_concessionaria_para_dicionario(
            concessionaria
        )
        for concessionaria in concessionarias
    ]

    conteudo_json = json.dumps(
        dados_concessionarias,
        ensure_ascii=False,
        indent=4,
    )

    caminho.write_text(
        conteudo_json,
        encoding="utf-8",
    )

    return caminho