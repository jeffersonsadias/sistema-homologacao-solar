"""
Fachada de empresas.

Este módulo coordena as operações relacionadas às empresas,
conectando:

- domínio;
- infraestrutura;
- coleção de empresas carregada em memória.

A fachada não deve:
- solicitar dados com input();
- exibir menus;
- conter regras internas de validação de CNPJ;
- manipular diretamente arquivos JSON.

As regras pertencem ao domínio e a persistência pertence
à infraestrutura.
"""

from typing import Any

from app.dominio.empresas import (
    SITUACAO_EMPRESA_ATIVA,
    SITUACAO_EMPRESA_CANCELADA,
    SITUACAO_EMPRESA_INATIVA,
    SITUACAO_EMPRESA_SUSPENSA,
    ativar_empresa as ativar_empresa_dominio,
    atualizar_dados_empresa,
    buscar_empresa_por_cnpj,
    buscar_empresa_por_codigo,
    cancelar_empresa as cancelar_empresa_dominio,
    cnpj_empresa_existe,
    criar_dados_empresa,
    empresa_esta_ativa as empresa_esta_ativa_dominio,
    inativar_empresa as inativar_empresa_dominio,
    ordenar_empresas_por_nome,
    suspender_empresa as suspender_empresa_dominio,
    obter_transicoes_permitidas_empresa,
)
from app.infraestrutura.repositorio_empresas_json import (
    carregar_empresas,
    salvar_empresas,
)
from app.utils import gerar_proximo_codigo


# ============================================================
# COLEÇÃO DE EMPRESAS
# ============================================================

empresas: list[dict[str, Any]] = carregar_empresas()


# ============================================================
# FUNÇÕES AUXILIARES INTERNAS
# ============================================================

def _obter_empresa_obrigatoria(
    codigo_empresa: int,
) -> dict[str, Any]:
    """
    Busca uma empresa pelo código.

    Caso a empresa não exista, gera um erro.

    Esta função é interna porque serve como apoio para operações
    que precisam obrigatoriamente de uma empresa existente.
    """

    empresa = buscar_empresa_por_codigo(
        empresas,
        codigo_empresa,
    )

    if empresa is None:
        raise ValueError(
            f"Empresa com código {codigo_empresa} não encontrada."
        )

    return empresa


def _salvar_alteracoes() -> None:
    """
    Salva a coleção atual de empresas.

    A função centraliza a chamada ao repositório para evitar
    repetição dentro da fachada.
    """

    salvar_empresas(
        empresas,
    )


# ============================================================
# CADASTRO
# ============================================================

def cadastrar_empresa(
    razao_social: str,
    nome_fantasia: str,
    cnpj: str,
    email: str,
    telefone: str,
) -> dict[str, Any]:
    """
    Cadastra uma nova empresa.

    Fluxo:

    1. verifica se o CNPJ já está cadastrado;
    2. gera o próximo código;
    3. solicita ao domínio a criação dos dados;
    4. adiciona a empresa à coleção;
    5. salva a coleção no repositório;
    6. retorna a empresa cadastrada.
    """

    if cnpj_empresa_existe(
        empresas,
        cnpj,
    ):
        raise ValueError(
            "Já existe uma empresa cadastrada com esse CNPJ."
        )

    proximo_codigo = gerar_proximo_codigo(
        empresas,
    )

    nova_empresa = criar_dados_empresa(
        codigo=proximo_codigo,
        razao_social=razao_social,
        nome_fantasia=nome_fantasia,
        cnpj=cnpj,
        email=email,
        telefone=telefone,
    )

    empresas.append(
        nova_empresa,
    )

    _salvar_alteracoes()

    return nova_empresa


# ============================================================
# CONSULTAS
# ============================================================

def buscar_empresa(
    codigo_empresa: int,
) -> dict[str, Any] | None:
    """
    Busca uma empresa pelo código.

    Retorna:
    - a empresa encontrada;
    - None quando a empresa não existe.
    """

    return buscar_empresa_por_codigo(
        empresas,
        codigo_empresa,
    )


def obter_empresa(
    codigo_empresa: int,
) -> dict[str, Any]:
    """
    Retorna obrigatoriamente uma empresa existente.

    Diferentemente de buscar_empresa(), esta função gera
    ValueError quando o código não é encontrado.
    """

    return _obter_empresa_obrigatoria(
        codigo_empresa,
    )


def buscar_empresa_com_cnpj(
    cnpj: str,
) -> dict[str, Any] | None:
    """
    Busca uma empresa pelo CNPJ.
    """

    return buscar_empresa_por_cnpj(
        empresas,
        cnpj,
    )


def listar_empresas(
    ordenar_por_nome: bool = False,
) -> list[dict[str, Any]]:
    """
    Retorna a lista de empresas.

    Quando ordenar_por_nome for True, retorna uma nova lista
    ordenada pelo nome fantasia.

    A função sempre retorna uma nova lista para evitar que outros
    módulos alterem diretamente a coleção interna da fachada.
    """

    if ordenar_por_nome:
        return ordenar_empresas_por_nome(
            empresas,
        )

    return list(
        empresas,
    )


def listar_empresas_ativas() -> list[dict[str, Any]]:
    """
    Retorna somente as empresas ativas.
    """

    return [
        empresa
        for empresa in empresas
        if empresa_esta_ativa_dominio(
            empresa
        )
    ]


def listar_empresas_por_situacao(
    situacao: str,
) -> list[dict[str, Any]]:
    """
    Retorna as empresas que possuem a situação informada.

    Situações aceitas:

    - ATIVA
    - INATIVA
    - SUSPENSA
    - CANCELADA
    """

    situacao_normalizada = situacao.strip().upper()

    situacoes_permitidas = {
        SITUACAO_EMPRESA_ATIVA,
        SITUACAO_EMPRESA_INATIVA,
        SITUACAO_EMPRESA_SUSPENSA,
        SITUACAO_EMPRESA_CANCELADA,
    }

    if situacao_normalizada not in situacoes_permitidas:
        raise ValueError(
            "Situação de empresa inválida."
        )

    return [
        empresa
        for empresa in empresas
        if empresa.get("situacao") == situacao_normalizada
    ]


def quantidade_empresas() -> int:
    """
    Retorna a quantidade total de empresas cadastradas.
    """

    return len(
        empresas,
    )


def empresa_existe(
    codigo_empresa: int,
) -> bool:
    """
    Verifica se uma empresa existe.
    """

    return buscar_empresa(
        codigo_empresa,
    ) is not None

def empresa_esta_ativa(
    codigo_empresa: int,
) -> bool:
    """
    Verifica se uma empresa existente está ativa.

    A função recebe o código da empresa,
    localiza o registro pela fachada e solicita
    ao domínio a verificação da situação.

    Levanta:
        ValueError:
            Quando a empresa não existe.
    """

    empresa = _obter_empresa_obrigatoria(
        codigo_empresa
    )

    return empresa_esta_ativa_dominio(
        empresa
    )

def listar_transicoes_permitidas(
    codigo_empresa: int,
) -> tuple[str, ...]:
    """
    Retorna as situações disponíveis para uma empresa.

    A fachada localiza a empresa e solicita ao domínio
    as transições permitidas para a situação atual.
    """

    empresa = _obter_empresa_obrigatoria(
        codigo_empresa,
    )

    return obter_transicoes_permitidas_empresa(
        empresa["situacao"],
    )

# ============================================================
# EDIÇÃO DOS DADOS CADASTRAIS
# ============================================================

def editar_empresa(
    codigo_empresa: int,
    razao_social: str | None = None,
    nome_fantasia: str | None = None,
    email: str | None = None,
    telefone: str | None = None,
) -> dict[str, Any]:
    """
    Edita os dados cadastrais de uma empresa existente.

    O CNPJ não pode ser alterado por esta operação.
    """

    empresa = _obter_empresa_obrigatoria(
        codigo_empresa,
    )

    atualizar_dados_empresa(
        empresa=empresa,
        razao_social=razao_social,
        nome_fantasia=nome_fantasia,
        email=email,
        telefone=telefone,
    )

    _salvar_alteracoes()

    return empresa

# ============================================================
# ALTERAÇÃO DA SITUAÇÃO
# ============================================================

def ativar_empresa(
    codigo_empresa: int,
) -> dict[str, Any]:
    """
    Ativa uma empresa existente.
    """

    empresa = _obter_empresa_obrigatoria(
        codigo_empresa,
    )

    ativar_empresa_dominio(
        empresa,
    )

    _salvar_alteracoes()

    return empresa


def inativar_empresa(
    codigo_empresa: int,
) -> dict[str, Any]:
    """
    Inativa uma empresa existente.

    A empresa permanece cadastrada e seu histórico é preservado.
    """

    empresa = _obter_empresa_obrigatoria(
        codigo_empresa,
    )

    inativar_empresa_dominio(
        empresa,
    )

    _salvar_alteracoes()

    return empresa


def suspender_empresa(
    codigo_empresa: int,
) -> dict[str, Any]:
    """
    Suspende temporariamente uma empresa existente.
    """

    empresa = _obter_empresa_obrigatoria(
        codigo_empresa,
    )

    suspender_empresa_dominio(
        empresa,
    )

    _salvar_alteracoes()

    return empresa


def cancelar_empresa(
    codigo_empresa: int,
) -> dict[str, Any]:
    """
    Cancela uma empresa existente.

    A operação não remove fisicamente o registro.
    """

    empresa = _obter_empresa_obrigatoria(
        codigo_empresa,
    )

    cancelar_empresa_dominio(
        empresa,
    )

    _salvar_alteracoes()

    return empresa