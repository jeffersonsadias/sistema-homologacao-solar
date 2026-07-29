"""
Repositório JSON de Usuários.

Este módulo é responsável exclusivamente por:

- carregar usuários do arquivo JSON;
- salvar usuários no arquivo JSON;
- criar automaticamente o diretório de dados;
- criar automaticamente o arquivo quando necessário;
- validar a estrutura básica do conteúdo persistido.

As regras de negócio dos Usuários pertencem ao módulo:

    app.dominio.usuarios
"""

import json
from pathlib import Path
from typing import Any


# ============================================================
# CAMINHO DO ARQUIVO
# ============================================================

CAMINHO_ARQUIVO_USUARIOS = (
    Path(__file__).resolve().parents[2]
    / "data"
    / "usuarios.json"
)


# ============================================================
# FUNÇÕES AUXILIARES
# ============================================================

def _garantir_diretorio_dados() -> None:
    """
    Garante que o diretório onde o arquivo JSON
    será armazenado exista.

    O parâmetro parents=True permite criar
    diretórios intermediários.

    O parâmetro exist_ok=True impede erro
    caso o diretório já exista.
    """

    CAMINHO_ARQUIVO_USUARIOS.parent.mkdir(
        parents=True,
        exist_ok=True,
    )


def _criar_arquivo_vazio() -> None:
    """
    Cria o arquivo de Usuários com uma lista vazia.

    O arquivo inicial terá este conteúdo:

        []
    """

    _garantir_diretorio_dados()

    CAMINHO_ARQUIVO_USUARIOS.write_text(
        "[]",
        encoding="utf-8",
    )


def _validar_estrutura_usuarios(
    dados: Any,
) -> list[dict[str, Any]]:
    """
    Valida a estrutura geral carregada do JSON.

    A raiz do arquivo deve ser uma lista.

    Cada item da lista deve ser um dicionário.

    Esta função não valida regras detalhadas
    de domínio, como e-mail, perfil ou situação.
    """

    if not isinstance(dados, list):
        raise ValueError(
            "O arquivo de usuários deve conter "
            "uma lista."
        )

    for indice, usuario in enumerate(
        dados
    ):
        if not isinstance(usuario, dict):
            raise ValueError(
                "Cada usuário deve ser representado "
                "por um objeto JSON. "
                f"Item inválido no índice {indice}."
            )

    return dados


# ============================================================
# CARREGAMENTO
# ============================================================

def carregar_usuarios() -> list[dict[str, Any]]:
    """
    Carrega os Usuários armazenados no arquivo JSON.

    Caso o arquivo ainda não exista, ele será criado
    automaticamente com uma lista vazia.

    Retorna:

        Uma lista de dicionários representando usuários.

    Exceções:

        ValueError:
            Quando o JSON estiver inválido ou a estrutura
            principal do arquivo estiver incorreta.

        OSError:
            Quando ocorrer um problema de acesso ao arquivo.
    """

    _garantir_diretorio_dados()

    if not CAMINHO_ARQUIVO_USUARIOS.exists():
        _criar_arquivo_vazio()

    try:
        conteudo = (
            CAMINHO_ARQUIVO_USUARIOS.read_text(
                encoding="utf-8"
            )
        )

        dados = json.loads(
            conteudo
        )

    except json.JSONDecodeError as erro:
        raise ValueError(
            "O arquivo de usuários contém "
            "um JSON inválido."
        ) from erro

    return _validar_estrutura_usuarios(
        dados
    )


# ============================================================
# SALVAMENTO
# ============================================================

def salvar_usuarios(
    usuarios: list[dict[str, Any]],
) -> None:
    """
    Salva a coleção de Usuários no arquivo JSON.

    A estrutura é validada antes da gravação.

    O conteúdo é salvo com:

    - indentação de quatro espaços;
    - caracteres acentuados preservados;
    - codificação UTF-8.
    """

    usuarios_validados = (
        _validar_estrutura_usuarios(
            usuarios
        )
    )

    _garantir_diretorio_dados()

    conteudo_json = json.dumps(
        usuarios_validados,
        ensure_ascii=False,
        indent=4,
    )

    CAMINHO_ARQUIVO_USUARIOS.write_text(
        conteudo_json,
        encoding="utf-8",
    )