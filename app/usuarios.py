"""
Fachada de Usuários.

Este módulo coordena:

- regras de domínio de Usuários;
- consultas públicas de Empresas;
- persistência JSON de Usuários;
- geração de códigos;
- validações entre módulos.

A fachada não deve realizar entradas ou saídas
diretas pelo terminal.

A interface de terminal será implementada em:

    app.interface.usuarios_interface
"""

from typing import Any

from app import empresas
from app.dominio import usuarios as usuarios_dominio
from app.infraestrutura.repositorio_usuarios_json import (
    carregar_usuarios,
    salvar_usuarios,
)


# ============================================================
# COLEÇÃO EM MEMÓRIA
# ============================================================

usuarios = carregar_usuarios()


# ============================================================
# FUNÇÕES AUXILIARES INTERNAS
# ============================================================

def _gerar_proximo_codigo() -> int:
    """
    Gera o próximo código disponível
    para um Usuário.

    O código é único em toda a plataforma,
    independentemente da Empresa.
    """

    if not usuarios:
        return 1

    codigos_validos = [
        usuario.get("codigo")
        for usuario in usuarios
        if (
            isinstance(usuario, dict)
            and isinstance(
                usuario.get("codigo"),
                int,
            )
            and not isinstance(
                usuario.get("codigo"),
                bool,
            )
            and usuario.get("codigo") > 0
        )
    ]

    if not codigos_validos:
        return 1

    return max(
        codigos_validos
    ) + 1


def _obter_empresa_valida(
    codigo_empresa: int,
) -> dict[str, Any]:
    """
    Obtém obrigatoriamente uma Empresa
    pela função pública da fachada de Empresas.

    A própria fachada de Empresas levanta
    ValueError quando o código não existe.
    """

    return empresas.obter_empresa(
        codigo_empresa
    )

def _obter_usuario_da_empresa(
    codigo_usuario: int,
    codigo_empresa: int,
) -> dict:
    """
    Localiza um Usuário dentro do contexto
    de uma Empresa específica.

    Mesmo que o código do Usuário exista em outra
    Empresa, ele será tratado como não encontrado.

    Essa regra protege o isolamento entre Empresas.
    """

    for usuario in usuarios:
        if (
            usuario.get("codigo") == codigo_usuario
            and usuario.get("codigo_empresa")
            == codigo_empresa
        ):
            return usuario

    raise ValueError(
        f"Usuário com código {codigo_usuario} "
        "não encontrado."
    )

def _validar_empresa_para_novo_usuario(
    codigo_empresa: int,
) -> dict[str, Any]:
    """
    Verifica se a Empresa existe e se está ativa.

    Novos usuários somente podem ser vinculados
    a Empresas ativas.
    """

    empresa = _obter_empresa_valida(
        codigo_empresa
    )

    if not empresas.empresa_esta_ativa(
        codigo_empresa
    ):
        raise ValueError(
            "Não é possível cadastrar usuário "
            "para uma Empresa que não esteja ativa."
        )

    return empresa


# ============================================================
# CADASTRO
# ============================================================

def cadastrar_usuario(
    codigo_empresa: int,
    nome: str,
    email: str,
    perfil: str,
) -> dict[str, Any]:
    """
    Cadastra um novo Usuário.

    Fluxo:

        validar Empresa
        verificar e-mail
        gerar código
        criar dados no domínio
        adicionar à coleção
        salvar no repositório
        retornar Usuário criado

    O e-mail é único em toda a plataforma.
    """

    _validar_empresa_para_novo_usuario(
        codigo_empresa
    )

    if usuarios_dominio.email_usuario_existe(
        usuarios,
        email,
    ):
        raise ValueError(
            "Já existe um usuário cadastrado "
            "com este e-mail."
        )

    codigo_usuario = _gerar_proximo_codigo()

    novo_usuario = (
        usuarios_dominio.criar_dados_usuario(
            codigo=codigo_usuario,
            codigo_empresa=codigo_empresa,
            nome=nome,
            email=email,
            perfil=perfil,
        )
    )

    usuarios.append(
        novo_usuario
    )

    salvar_usuarios(
        usuarios
    )

    return novo_usuario

def alterar_situacao_usuario(
    codigo_empresa: int,
    codigo_usuario: int,
    nova_situacao: str,
) -> dict:
    """
    Altera a situação de um Usuário.

    A fachada coordena o processo:

    1. verifica se a Empresa existe;
    2. verifica se a Empresa está ativa;
    3. localiza o Usuário dentro da Empresa;
    4. delega a transição ao domínio;
    5. salva a coleção atualizada;
    6. retorna o Usuário atualizado.
    """

    empresas.obter_empresa(
        codigo_empresa
    )

    if not empresas.empresa_esta_ativa(
        codigo_empresa
    ):
        raise ValueError(
            "Empresa deve estar ativa para "
            "alterar a situação de um Usuário."
        )

    usuario_encontrado = (
        _obter_usuario_da_empresa(
            codigo_usuario=codigo_usuario,
            codigo_empresa=codigo_empresa,
        )
    )

    usuario_atualizado = (
        usuarios_dominio
        .alterar_situacao_usuario(
            usuario=usuario_encontrado,
            nova_situacao=nova_situacao,
        )
    )

    salvar_usuarios(
        usuarios
    )

    return usuario_atualizado

def ativar_usuario(
    codigo_empresa: int,
    codigo_usuario: int,
) -> dict:
    """
    Altera a situação do Usuário para ATIVO.

    Todas as validações e a persistência
    são realizadas por alterar_situacao_usuario().
    """

    return alterar_situacao_usuario(
        codigo_empresa=codigo_empresa,
        codigo_usuario=codigo_usuario,
        nova_situacao="ATIVO",
    )

def inativar_usuario(
    codigo_empresa: int,
    codigo_usuario: int,
) -> dict:
    """
    Altera a situação do Usuário para INATIVO.
    """

    return alterar_situacao_usuario(
        codigo_empresa=codigo_empresa,
        codigo_usuario=codigo_usuario,
        nova_situacao="INATIVO",
    )

def bloquear_usuario(
    codigo_empresa: int,
    codigo_usuario: int,
) -> dict:
    """
    Altera a situação do Usuário para BLOQUEADO.
    """

    return alterar_situacao_usuario(
        codigo_empresa=codigo_empresa,
        codigo_usuario=codigo_usuario,
        nova_situacao="BLOQUEADO",
    )

def cancelar_usuario(
    codigo_empresa: int,
    codigo_usuario: int,
) -> dict:
    """
    Altera a situação do Usuário para CANCELADO.

    CANCELADO é um estado terminal.
    Depois do cancelamento, o domínio impedirá
    qualquer nova alteração de situação.
    """

    return alterar_situacao_usuario(
        codigo_empresa=codigo_empresa,
        codigo_usuario=codigo_usuario,
        nova_situacao="CANCELADO",
    )

# ============================================================
# CONSULTAS
# ============================================================

def obter_usuario(
    codigo_usuario: int,
    codigo_empresa: int,
) -> dict[str, Any] | None:
    """
    Retorna um Usuário pelo código,
    respeitando o limite da Empresa.

    Um usuário de outra Empresa não será retornado.
    """

    return (
        usuarios_dominio
        .buscar_usuario_por_codigo(
            usuarios=usuarios,
            codigo_usuario=codigo_usuario,
            codigo_empresa=codigo_empresa,
        )
    )


def buscar_usuario(
    codigo_usuario: int,
    codigo_empresa: int,
) -> dict[str, Any] | None:
    """
    Alias público para obter_usuario().
    """

    return obter_usuario(
        codigo_usuario,
        codigo_empresa,
    )


def buscar_usuario_por_email(
    email: str,
) -> dict[str, Any] | None:
    """
    Busca um Usuário pelo e-mail.

    O e-mail é globalmente único.
    """

    return (
        usuarios_dominio
        .buscar_usuario_por_email(
            usuarios,
            email,
        )
    )


def listar_usuarios(
    codigo_empresa: int,
) -> list[dict[str, Any]]:
    """
    Lista somente os Usuários
    pertencentes à Empresa informada.
    """

    _obter_empresa_valida(
        codigo_empresa
    )

    return (
        usuarios_dominio
        .listar_usuarios_da_empresa(
            usuarios,
            codigo_empresa,
        )
    )


def listar_usuarios_ativos(
    codigo_empresa: int,
) -> list[dict[str, Any]]:
    """
    Lista os Usuários ativos
    pertencentes à Empresa informada.
    """

    usuarios_da_empresa = listar_usuarios(
        codigo_empresa
    )

    return [
        usuario
        for usuario in usuarios_da_empresa
        if usuarios_dominio.usuario_esta_ativo(
            usuario
        )
    ]


def listar_usuarios_por_perfil(
    codigo_empresa: int,
    perfil: str,
) -> list[dict[str, Any]]:
    """
    Lista os Usuários da Empresa
    que possuem determinado perfil.
    """

    usuarios_da_empresa = listar_usuarios(
        codigo_empresa
    )

    return [
        usuario
        for usuario in usuarios_da_empresa
        if usuarios_dominio.usuario_possui_perfil(
            usuario,
            perfil,
        )
    ]


def quantidade_usuarios(
    codigo_empresa: int,
) -> int:
    """
    Retorna a quantidade de Usuários
    vinculados à Empresa.
    """

    return len(
        listar_usuarios(
            codigo_empresa
        )
    )


def usuario_existe(
    codigo_usuario: int,
    codigo_empresa: int,
) -> bool:
    """
    Verifica se o Usuário existe
    dentro da Empresa informada.
    """

    return obter_usuario(
        codigo_usuario,
        codigo_empresa,
    ) is not None


def email_usuario_existe(
    email: str,
) -> bool:
    """
    Verifica se o e-mail já está cadastrado
    em qualquer Empresa da plataforma.
    """

    return (
        usuarios_dominio
        .email_usuario_existe(
            usuarios,
            email,
        )
    )


# ============================================================
# CONSULTAS DE PERFIL E SITUAÇÃO
# ============================================================

def usuario_esta_ativo(
    codigo_usuario: int,
    codigo_empresa: int,
) -> bool:
    """
    Verifica se o Usuário está ativo.

    Levanta ValueError caso o Usuário
    não exista dentro da Empresa.
    """

    usuario = obter_usuario(
        codigo_usuario,
        codigo_empresa,
    )

    if usuario is None:
        raise ValueError(
            "Usuário não encontrado."
        )

    return usuarios_dominio.usuario_esta_ativo(
        usuario
    )


def usuario_esta_cancelado(
    codigo_usuario: int,
    codigo_empresa: int,
) -> bool:
    """
    Verifica se o Usuário está cancelado.

    Levanta ValueError caso o Usuário
    não exista dentro da Empresa.
    """

    usuario = obter_usuario(
        codigo_usuario,
        codigo_empresa,
    )

    if usuario is None:
        raise ValueError(
            "Usuário não encontrado."
        )

    return (
        usuarios_dominio
        .usuario_esta_cancelado(
            usuario
        )
    )


def usuario_possui_perfil(
    codigo_usuario: int,
    codigo_empresa: int,
    perfil: str,
) -> bool:
    """
    Verifica se o Usuário possui
    determinado perfil.

    A consulta respeita a Empresa.
    """

    usuario = obter_usuario(
        codigo_usuario,
        codigo_empresa,
    )

    if usuario is None:
        raise ValueError(
            "Usuário não encontrado."
        )

    return (
        usuarios_dominio
        .usuario_possui_perfil(
            usuario,
            perfil,
        )
    )


# ============================================================
# FUNÇÕES DE APOIO PARA INTERFACE
# ============================================================

def obter_perfis_usuario() -> tuple[str, ...]:
    """
    Retorna os perfis oficiais disponíveis.

    A interface pode usar esta função
    sem importar diretamente o domínio.
    """

    return usuarios_dominio.PERFIS_USUARIO


def obter_situacoes_usuario() -> tuple[str, ...]:
    """
    Retorna as situações oficiais disponíveis.

    A interface pode usar esta função
    sem importar diretamente o domínio.
    """

    return usuarios_dominio.SITUACOES_USUARIO