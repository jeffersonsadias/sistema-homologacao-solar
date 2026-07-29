"""
Repositório JSON das Unidades Consumidoras.

Este módulo é responsável pela persistência
das entidades UnidadeConsumidora.

Responsabilidades:

- carregar dados do arquivo JSON;
- reconstruir objetos do domínio;
- converter objetos para dicionários;
- salvar os dados no arquivo JSON.

Este módulo não contém regras de negócio
nem interação direta com o usuário.
"""

import json
from pathlib import Path
from datetime import datetime

from app.dominio.unidades_consumidoras import (
    EnderecoUnidade,
    RegistroAlteracaoUnidade,
    SituacaoUnidadeConsumidora,
    TipoAlteracaoUnidade,
    TipoLigacao,
    TipoTitular,
    TitularConta,
    UnidadeConsumidora,
)


CAMINHO_ARQUIVO = (
    Path(__file__).resolve().parents[2]
    / "data"
    / "unidades_consumidoras.json"
)


def converter_titular_para_dicionario(titular):
    """
    Converte um objeto TitularConta
    para um dicionário serializável em JSON.
    """

    return {
        "nome": titular.nome,
        "documento": titular.documento,
        "tipo": titular.tipo.value,
    }


def reconstruir_titular(dados):
    """
    Reconstrói um objeto TitularConta
    a partir de um dicionário.
    """

    return TitularConta(
        nome=dados["nome"],
        documento=dados["documento"],
        tipo=TipoTitular(
            dados["tipo"]
        ),
    )


def converter_endereco_para_dicionario(
    endereco,
):
    """
    Converte um objeto EnderecoUnidade
    para um dicionário serializável.
    """

    return {
        "logradouro": endereco.logradouro,
        "numero": endereco.numero,
        "bairro": endereco.bairro,
        "cidade": endereco.cidade,
        "estado": endereco.estado,
        "cep": endereco.cep,
        "complemento": endereco.complemento,
    }


def reconstruir_endereco(dados):
    """
    Reconstrói um objeto EnderecoUnidade
    a partir de um dicionário.
    """

    return EnderecoUnidade(
        logradouro=dados["logradouro"],
        numero=dados["numero"],
        bairro=dados["bairro"],
        cidade=dados["cidade"],
        estado=dados["estado"],
        cep=dados["cep"],
        complemento=dados.get(
            "complemento",
            "",
        ),
    )


def converter_registro_para_dicionario(
    registro,
):
    """
    Converte um RegistroAlteracaoUnidade
    para um dicionário serializável.
    """

    return {
        "tipo": registro.tipo.value,
        "valor_anterior": (
            registro.valor_anterior
        ),
        "valor_novo": registro.valor_novo,
        "data_alteracao": (
            registro.data_alteracao.isoformat()
        ),
        "motivo": registro.motivo,
    }


def reconstruir_registro(dados):
    """
    Reconstrói um RegistroAlteracaoUnidade
    a partir de um dicionário.
    """

    return RegistroAlteracaoUnidade(
        tipo=TipoAlteracaoUnidade(
            dados["tipo"]
        ),
        valor_anterior=dados[
            "valor_anterior"
        ],
        valor_novo=dados["valor_novo"],
        data_alteracao=datetime.fromisoformat(
            dados["data_alteracao"]
        ),
        motivo=dados.get(
            "motivo",
            "",
        ),
    )


def converter_unidade_para_dicionario(
    unidade,
):
    """
    Converte uma UnidadeConsumidora
    para um dicionário serializável em JSON.
    """

    return {
        "codigo": unidade.codigo,
        "numero_uc": unidade.numero_uc,
        "codigo_cliente": (
            unidade.codigo_cliente
        ),
        "codigo_concessionaria": (
            unidade.codigo_concessionaria
        ),
        "titular": (
            converter_titular_para_dicionario(
                unidade.titular
            )
        ),
        "endereco": (
            converter_endereco_para_dicionario(
                unidade.endereco
            )
        ),
        "tipo_ligacao": (
            unidade.tipo_ligacao.value
        ),
        "carga_instalada_kw": (
            unidade.carga_instalada_kw
        ),
        "situacao": unidade.situacao.value,
        "data_cadastro": (
            unidade.data_cadastro.isoformat()
        ),
        "data_atualizacao": (
            unidade.data_atualizacao.isoformat()
        ),
        "historico_alteracoes": [
            converter_registro_para_dicionario(
                registro
            )
            for registro
            in unidade.historico_alteracoes
        ],
    }


def reconstruir_unidade_consumidora(
    dados,
):
    """
    Reconstrói uma UnidadeConsumidora
    a partir de um dicionário.
    """

    titular = reconstruir_titular(
        dados["titular"]
    )

    endereco = reconstruir_endereco(
        dados["endereco"]
    )

    historico = [
        reconstruir_registro(registro)
        for registro
        in dados.get(
            "historico_alteracoes",
            [],
        )
    ]

    return UnidadeConsumidora(
        codigo=dados["codigo"],
        numero_uc=dados["numero_uc"],
        codigo_cliente=dados[
            "codigo_cliente"
        ],
        codigo_concessionaria=dados[
            "codigo_concessionaria"
        ],
        titular=titular,
        endereco=endereco,
        tipo_ligacao=TipoLigacao(
            dados["tipo_ligacao"]
        ),
        carga_instalada_kw=dados.get(
            "carga_instalada_kw",
            0.0,
        ),
        situacao=(
            SituacaoUnidadeConsumidora(
                dados.get(
                    "situacao",
                    (
                        SituacaoUnidadeConsumidora
                        .ATIVA
                        .value
                    ),
                )
            )
        ),
        data_cadastro=datetime.fromisoformat(
            dados["data_cadastro"]
        ),
        data_atualizacao=(
            datetime.fromisoformat(
                dados["data_atualizacao"]
            )
        ),
        historico_alteracoes=historico,
    )


def carregar_unidades_consumidoras():
    """
    Carrega as Unidades Consumidoras
    armazenadas no arquivo JSON.

    Retorna uma lista de objetos
    UnidadeConsumidora.

    Quando o arquivo não existe,
    está vazio ou contém uma lista vazia,
    retorna uma lista vazia.
    """

    if not CAMINHO_ARQUIVO.exists():
        return []

    try:
        with open(
            CAMINHO_ARQUIVO,
            "r",
            encoding="utf-8",
        ) as arquivo:
            dados = json.load(arquivo)

    except (
        json.JSONDecodeError,
        OSError,
    ):
        return []

    if not isinstance(dados, list):
        return []

    return [
        reconstruir_unidade_consumidora(
            item
        )
        for item in dados
    ]


def salvar_unidades_consumidoras(
    unidades_consumidoras,
):
    """
    Salva uma lista de Unidades Consumidoras
    no arquivo JSON.
    """

    CAMINHO_ARQUIVO.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    dados = [
        converter_unidade_para_dicionario(
            unidade
        )
        for unidade
        in unidades_consumidoras
    ]

    with open(
        CAMINHO_ARQUIVO,
        "w",
        encoding="utf-8",
    ) as arquivo:
        json.dump(
            dados,
            arquivo,
            ensure_ascii=False,
            indent=4,
        )