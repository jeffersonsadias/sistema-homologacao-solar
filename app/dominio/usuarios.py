"""
Regras de domínio relacionadas aos Usuários.

Um Usuário representa uma pessoa autorizada a acessar
a plataforma em nome de uma Empresa.

Todo usuário pertence obrigatoriamente a uma Empresa.
A Empresa funciona como limite de acesso aos dados.
"""

from datetime import datetime
from typing import Any


# ============================================================
# PERFIS DE USUÁRIO
# ============================================================

PERFIL_USUARIO_ADMINISTRADOR = "ADMINISTRADOR"
PERFIL_USUARIO_GESTOR = "GESTOR"
PERFIL_USUARIO_OPERACIONAL = "OPERACIONAL"
PERFIL_USUARIO_CONSULTA = "CONSULTA"


PERFIS_USUARIO = (
    PERFIL_USUARIO_ADMINISTRADOR,
    PERFIL_USUARIO_GESTOR,
    PERFIL_USUARIO_OPERACIONAL,
    PERFIL_USUARIO_CONSULTA,
)


# ============================================================
# SITUAÇÕES DE USUÁRIO
# ============================================================

SITUACAO_USUARIO_ATIVO = "ATIVO"
SITUACAO_USUARIO_INATIVO = "INATIVO"
SITUACAO_USUARIO_BLOQUEADO = "BLOQUEADO"
SITUACAO_USUARIO_CANCELADO = "CANCELADO"


SITUACOES_USUARIO = (
    SITUACAO_USUARIO_ATIVO,
    SITUACAO_USUARIO_INATIVO,
    SITUACAO_USUARIO_BLOQUEADO,
    SITUACAO_USUARIO_CANCELADO,
)


SITUACAO_INICIAL_USUARIO = SITUACAO_USUARIO_ATIVO

TRANSICOES_SITUACAO_USUARIO = {
    SITUACAO_USUARIO_ATIVO: (
        SITUACAO_USUARIO_INATIVO,
        SITUACAO_USUARIO_BLOQUEADO,
        SITUACAO_USUARIO_CANCELADO,
    ),
    SITUACAO_USUARIO_INATIVO: (
        SITUACAO_USUARIO_ATIVO,
        SITUACAO_USUARIO_BLOQUEADO,
        SITUACAO_USUARIO_CANCELADO,
    ),
    SITUACAO_USUARIO_BLOQUEADO: (
        SITUACAO_USUARIO_ATIVO,
        SITUACAO_USUARIO_INATIVO,
        SITUACAO_USUARIO_CANCELADO,
    ),
    SITUACAO_USUARIO_CANCELADO: (),
}

# ============================================================
# FUNÇÕES AUXILIARES
# ============================================================

def _gerar_data_hora_atual() -> str:
    """
    Retorna a data e hora atuais no formato ISO.

    Exemplo:

        2026-07-28T14:30:00
    """

    return datetime.now().isoformat(
        timespec="seconds"
    )


def _validar_codigo(
    codigo: int,
    nome_campo: str,
) -> int:
    """
    Valida códigos numéricos utilizados pelo domínio.
    """

    if isinstance(codigo, bool):
        raise TypeError(
            f"{nome_campo} deve ser um número inteiro."
        )

    if not isinstance(codigo, int):
        raise TypeError(
            f"{nome_campo} deve ser um número inteiro."
        )

    if codigo <= 0:
        raise ValueError(
            f"{nome_campo} deve ser maior que zero."
        )

    return codigo


def _normalizar_texto_obrigatorio(
    valor: str,
    nome_campo: str,
) -> str:
    """
    Valida e normaliza um texto obrigatório.

    Espaços duplicados e espaços externos são removidos.
    """

    if not isinstance(valor, str):
        raise TypeError(
            f"{nome_campo} deve ser um texto."
        )

    valor_normalizado = " ".join(
        valor.split()
    )

    if not valor_normalizado:
        raise ValueError(
            f"{nome_campo} é obrigatório."
        )

    return valor_normalizado


def _normalizar_email(
    email: str,
) -> str:
    """
    Normaliza e valida inicialmente um endereço de e-mail.
    """

    if not isinstance(email, str):
        raise TypeError(
            "O e-mail do usuário deve ser um texto."
        )

    email_normalizado = email.strip().lower()

    if not email_normalizado:
        raise ValueError(
            "O e-mail do usuário é obrigatório."
        )

    if "@" not in email_normalizado:
        raise ValueError(
            "O e-mail do usuário é inválido."
        )

    parte_local, separador, dominio = (
        email_normalizado.partition("@")
    )

    if not separador:
        raise ValueError(
            "O e-mail do usuário é inválido."
        )

    if not parte_local or not dominio:
        raise ValueError(
            "O e-mail do usuário é inválido."
        )

    if "." not in dominio:
        raise ValueError(
            "O e-mail do usuário é inválido."
        )

    return email_normalizado


def _validar_perfil(
    perfil: str,
) -> str:
    """
    Valida o perfil atribuído ao usuário.
    """

    if not isinstance(perfil, str):
        raise TypeError(
            "O perfil do usuário deve ser um texto."
        )

    perfil_normalizado = perfil.strip().upper()

    if perfil_normalizado not in PERFIS_USUARIO:
        raise ValueError(
            "O perfil do usuário é inválido."
        )

    return perfil_normalizado


def _validar_situacao(
    situacao: str,
) -> str:
    """
    Valida a situação do usuário.
    """

    if not isinstance(situacao, str):
        raise TypeError(
            "A situação do usuário deve ser um texto."
        )

    situacao_normalizada = situacao.strip().upper()

    if situacao_normalizada not in SITUACOES_USUARIO:
        raise ValueError(
            "A situação do usuário é inválida."
        )

    return situacao_normalizada


def _validar_colecao_usuarios(
    usuarios: list[dict[str, Any]],
) -> None:
    """
    Verifica se a coleção de usuários é uma lista.
    """

    if not isinstance(usuarios, list):
        raise TypeError(
            "A coleção de usuários deve ser uma lista."
        )


# ============================================================
# CRIAÇÃO
# ============================================================

def criar_dados_usuario(
    codigo: int,
    codigo_empresa: int,
    nome: str,
    email: str,
    perfil: str,
    situacao: str = SITUACAO_INICIAL_USUARIO,
) -> dict[str, Any]:
    """
    Cria os dados válidos de um novo usuário.

    Esta função não salva o usuário e não gera o código.
    Essas responsabilidades pertencem à fachada e à
    infraestrutura.
    """

    codigo_validado = _validar_codigo(
        codigo,
        "O código do usuário",
    )

    codigo_empresa_validado = _validar_codigo(
        codigo_empresa,
        "O código da empresa",
    )

    nome_normalizado = (
        _normalizar_texto_obrigatorio(
            nome,
            "O nome do usuário",
        )
    )

    email_normalizado = _normalizar_email(
        email
    )

    perfil_validado = _validar_perfil(
        perfil
    )

    situacao_validada = _validar_situacao(
        situacao
    )

    data_hora_atual = _gerar_data_hora_atual()

    return {
        "codigo": codigo_validado,
        "codigo_empresa": codigo_empresa_validado,
        "nome": nome_normalizado,
        "email": email_normalizado,
        "perfil": perfil_validado,
        "situacao": situacao_validada,
        "data_cadastro": data_hora_atual,
        "data_atualizacao": data_hora_atual,
    }

# ============================================================
# CONSULTAS
# ============================================================

def buscar_usuario_por_codigo(
    usuarios: list[dict[str, Any]],
    codigo_usuario: int,
    codigo_empresa: int,
) -> dict[str, Any] | None:
    """
    Busca um usuário pelo código dentro de uma Empresa.

    Mesmo que o código do usuário exista, ele somente será
    retornado quando pertencer à empresa informada.
    """

    _validar_colecao_usuarios(
        usuarios
    )

    codigo_usuario_validado = _validar_codigo(
        codigo_usuario,
        "O código do usuário",
    )

    codigo_empresa_validado = _validar_codigo(
        codigo_empresa,
        "O código da empresa",
    )

    for usuario in usuarios:
        if not isinstance(usuario, dict):
            continue

        if (
            usuario.get("codigo")
            == codigo_usuario_validado
            and usuario.get("codigo_empresa")
            == codigo_empresa_validado
        ):
            return usuario

    return None


def buscar_usuario_por_email(
    usuarios: list[dict[str, Any]],
    email: str,
) -> dict[str, Any] | None:
    """
    Busca um usuário pelo e-mail normalizado.

    Inicialmente, o e-mail será considerado único em toda
    a plataforma, pois será usado futuramente no login.
    """

    _validar_colecao_usuarios(
        usuarios
    )

    email_normalizado = _normalizar_email(
        email
    )

    for usuario in usuarios:
        if not isinstance(usuario, dict):
            continue

        email_usuario = usuario.get(
            "email"
        )

        if not isinstance(email_usuario, str):
            continue

        if email_usuario.strip().lower() == email_normalizado:
            return usuario

    return None


def codigo_usuario_existe(
    usuarios: list[dict[str, Any]],
    codigo_usuario: int,
) -> bool:
    """
    Verifica se o código do usuário já existe na plataforma.

    O código interno será inicialmente único em toda
    a coleção de usuários.
    """

    _validar_colecao_usuarios(
        usuarios
    )

    codigo_validado = _validar_codigo(
        codigo_usuario,
        "O código do usuário",
    )

    return any(
        isinstance(usuario, dict)
        and usuario.get("codigo") == codigo_validado
        for usuario in usuarios
    )


def email_usuario_existe(
    usuarios: list[dict[str, Any]],
    email: str,
) -> bool:
    """
    Verifica se o e-mail já pertence a outro usuário.
    """

    return buscar_usuario_por_email(
        usuarios,
        email,
    ) is not None


def listar_usuarios_da_empresa(
    usuarios: list[dict[str, Any]],
    codigo_empresa: int,
) -> list[dict[str, Any]]:
    """
    Retorna somente os usuários pertencentes à empresa.

    A nova lista é ordenada pelo nome do usuário.
    """

    _validar_colecao_usuarios(
        usuarios
    )

    codigo_empresa_validado = _validar_codigo(
        codigo_empresa,
        "O código da empresa",
    )

    usuarios_da_empresa = [
        usuario
        for usuario in usuarios
        if (
            isinstance(usuario, dict)
            and usuario.get("codigo_empresa")
            == codigo_empresa_validado
        )
    ]

    return sorted(
        usuarios_da_empresa,
        key=lambda usuario: (
            usuario.get(
                "nome",
                "",
            ).casefold()
        ),
    )

# ============================================================
# CONSULTAS DE PERFIL E SITUAÇÃO
# ============================================================

def usuario_esta_ativo(
    usuario: dict[str, Any],
) -> bool:
    """
    Verifica se o usuário está ativo.
    """

    if not isinstance(usuario, dict):
        raise TypeError(
            "O usuário deve ser representado "
            "por um dicionário."
        )

    return (
        usuario.get("situacao")
        == SITUACAO_USUARIO_ATIVO
    )


def usuario_esta_cancelado(
    usuario: dict[str, Any],
) -> bool:
    """
    Verifica se o usuário está cancelado.
    """

    if not isinstance(usuario, dict):
        raise TypeError(
            "O usuário deve ser representado "
            "por um dicionário."
        )

    return (
        usuario.get("situacao")
        == SITUACAO_USUARIO_CANCELADO
    )


def usuario_possui_perfil(
    usuario: dict[str, Any],
    perfil: str,
) -> bool:
    """
    Verifica se o usuário possui determinado perfil.
    """

    if not isinstance(usuario, dict):
        raise TypeError(
            "O usuário deve ser representado "
            "por um dicionário."
        )

    perfil_validado = _validar_perfil(
        perfil
    )

    return (
        usuario.get("perfil")
        == perfil_validado
    )

def transicao_situacao_usuario_permitida(
    situacao_atual: str,
    nova_situacao: str,
) -> bool:
    """
    Verifica se uma transição de situação
    de Usuário é permitida.

    A função:

    - normaliza as duas situações;
    - valida a situação atual;
    - valida a nova situação;
    - consulta a matriz de transições;
    - retorna True ou False.
    """

    if not isinstance(
        situacao_atual,
        str,
    ):
        raise ValueError(
            "Situação atual inválida."
        )

    if not isinstance(
        nova_situacao,
        str,
    ):
        raise ValueError(
            "Nova situação inválida."
        )

    situacao_atual_normalizada = (
        situacao_atual
        .strip()
        .upper()
    )

    nova_situacao_normalizada = (
        nova_situacao
        .strip()
        .upper()
    )

    if (
        situacao_atual_normalizada
        not in SITUACOES_USUARIO
    ):
        raise ValueError(
            "Situação atual inválida."
        )

    if (
        nova_situacao_normalizada
        not in SITUACOES_USUARIO
    ):
        raise ValueError(
            "Nova situação inválida."
        )

    situacoes_permitidas = (
        TRANSICOES_SITUACAO_USUARIO[
            situacao_atual_normalizada
        ]
    )

    return (
        nova_situacao_normalizada
        in situacoes_permitidas
    )

def alterar_situacao_usuario(
    usuario: dict,
    nova_situacao: str,
) -> dict:
    """
    Altera a situação de um Usuário.

    A alteração somente ocorre quando
    a transição estiver permitida.

    O mesmo dicionário recebido é atualizado
    e devolvido.
    """

    if not isinstance(
        usuario,
        dict,
    ):
        raise TypeError(
            "Usuário deve ser um dicionário."
        )

    situacao_atual = usuario.get(
        "situacao"
    )

    if (
        not isinstance(
            situacao_atual,
            str,
        )
        or situacao_atual.strip().upper()
        not in SITUACOES_USUARIO
    ):
        raise ValueError(
            "Situação atual do Usuário inválida."
        )

    if not isinstance(
        nova_situacao,
        str,
    ):
        raise ValueError(
            "Nova situação inválida."
        )

    nova_situacao_normalizada = (
        nova_situacao
        .strip()
        .upper()
    )

    transicao_permitida = (
        transicao_situacao_usuario_permitida(
            situacao_atual=situacao_atual,
            nova_situacao=nova_situacao_normalizada,
        )
    )

    if not transicao_permitida:
        raise ValueError(
            "Transição de situação não permitida: "
            f"{situacao_atual.strip().upper()} "
            f"→ {nova_situacao_normalizada}."
        )

    usuario["situacao"] = (
        nova_situacao_normalizada
    )

    usuario["data_atualizacao"] = (
        datetime.now().isoformat(
            timespec="seconds"
        )
    )

    return usuario