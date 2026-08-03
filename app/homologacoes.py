"""
Fachada de Homologações.

Este módulo coordena:

- domínio de Homologações;
- consultas públicas de Empresas;
- consultas públicas de Projetos;
- consultas públicas de Concessionárias;
- persistência JSON;
- geração de códigos;
- coleção de Homologações mantida em memória.

A fachada não deve:

- utilizar input();
- utilizar print();
- acessar arquivos JSON diretamente;
- implementar regras internas do Aggregate Root;
- alterar coleções internas de outros módulos.
"""

from typing import Any

from app import concessionarias
from app import empresas
from app import projetos

from app.dominio.homologacoes import (
    buscar_homologacao_ativa_por_projeto,
    buscar_homologacao_por_codigo,
    criar_dados_homologacao,
    projeto_possui_homologacao_ativa,
)

from app.infraestrutura.repositorio_homologacoes_json import (
    carregar_homologacoes,
    salvar_homologacoes,
)

from app.utils import gerar_proximo_codigo


buscar_ativa_por_projeto_no_dominio = (
    buscar_homologacao_ativa_por_projeto
)

buscar_por_codigo_no_dominio = (
    buscar_homologacao_por_codigo
)

# ============================================================
# COLEÇÃO EM MEMÓRIA
# ============================================================

homologacoes: list[dict[str, Any]] = (
    carregar_homologacoes()
)


# ============================================================
# FUNÇÕES AUXILIARES INTERNAS
# ============================================================

def _salvar_alteracoes() -> None:
    """
    Persiste a coleção atual de Homologações.
    """

    salvar_homologacoes(
        homologacoes
    )

def _obter_homologacao_obrigatoria(
    codigo_homologacao: int,
    codigo_empresa: int | None = None,
) -> dict[str, Any]:
    """
    Obtém obrigatoriamente uma Homologação existente.

    Quando codigo_empresa for informado, a busca também
    respeita o isolamento entre Empresas.
    """

    homologacao = buscar_por_codigo_no_dominio(
        homologacoes=homologacoes,
        codigo=codigo_homologacao,
        codigo_empresa=codigo_empresa,
    )

    if homologacao is None:
        raise ValueError(
            "Homologação com código "
            f"{codigo_homologacao} não encontrada."
        )

    return homologacao

def _validar_dependencias_da_homologacao(
    codigo_empresa: int,
    codigo_projeto: int,
    codigo_concessionaria: int,
) -> None:
    """
    Confirma a existência das entidades externas necessárias.

    Também exige que a Empresa esteja ativa para iniciar
    um novo processo de Homologação.
    """

    empresas.obter_empresa(
        codigo_empresa
    )

    if not empresas.empresa_esta_ativa(
        codigo_empresa
    ):
        raise ValueError(
            "Não é possível criar uma Homologação para "
            "uma Empresa que não esteja ativa."
        )

    projeto = projetos.buscar_projeto(
        codigo_projeto
    )

    if projeto is None:
        raise ValueError(
            "Projeto com código "
            f"{codigo_projeto} não encontrado."
        )

    concessionarias.obter_concessionaria(
        codigo_concessionaria
    )

# ============================================================
# CONSULTAS
# ============================================================

def buscar_homologacao(
    codigo_homologacao: int,
    codigo_empresa: int | None = None,
) -> dict[str, Any] | None:
    """
    Busca uma Homologação pelo código.

    Quando codigo_empresa for informado, aplica o isolamento
    entre Empresas.

    Retorna None quando não houver correspondência.
    """

    return buscar_por_codigo_no_dominio(
        homologacoes=homologacoes,
        codigo=codigo_homologacao,
        codigo_empresa=codigo_empresa,
    )

def obter_homologacao(
    codigo_homologacao: int,
    codigo_empresa: int | None = None,
) -> dict[str, Any]:
    """
    Retorna obrigatoriamente uma Homologação existente.

    Gera ValueError quando o registro não for encontrado.
    """

    return _obter_homologacao_obrigatoria(
        codigo_homologacao=codigo_homologacao,
        codigo_empresa=codigo_empresa,
    )

def listar_homologacoes(
    codigo_empresa: int | None = None,
) -> list[dict[str, Any]]:
    """
    Retorna uma nova lista contendo as Homologações.

    Quando codigo_empresa for informado, retorna somente
    os registros pertencentes à Empresa indicada.

    A nova lista impede que outros módulos modifiquem
    diretamente a coleção mantida pela fachada.
    """

    if codigo_empresa is None:
        return list(
            homologacoes
        )

    return [
        homologacao
        for homologacao in homologacoes
        if homologacao.get("codigo_empresa")
        == codigo_empresa
    ]

def buscar_homologacao_por_projeto(
    codigo_projeto: int,
    codigo_empresa: int,
) -> dict[str, Any] | None:
    """
    Busca a Homologação ativa de um Projeto dentro
    do contexto de uma Empresa.
    """

    return buscar_ativa_por_projeto_no_dominio(
        homologacoes=homologacoes,
        codigo_projeto=codigo_projeto,
        codigo_empresa=codigo_empresa,
    )

# ============================================================
# CADASTRO
# ============================================================

def criar_homologacao(
    codigo_empresa: int,
    codigo_projeto: int,
    codigo_concessionaria: int,
    data_abertura: str,
    responsavel_abertura: str,
    prazo_estimado_dias: int = 45,
    observacoes: str = "",
) -> dict[str, Any]:
    """
    Cria e persiste uma nova Homologação.

    Fluxo:

    1. valida Empresa, Projeto e Concessionária;
    2. impede mais de uma Homologação ativa para o Projeto;
    3. gera o próximo código;
    4. solicita ao domínio a criação dos dados;
    5. adiciona a Homologação à coleção;
    6. persiste a coleção;
    7. retorna a Homologação criada.
    """

    _validar_dependencias_da_homologacao(
        codigo_empresa=codigo_empresa,
        codigo_projeto=codigo_projeto,
        codigo_concessionaria=codigo_concessionaria,
    )

    if projeto_possui_homologacao_ativa(
        homologacoes=homologacoes,
        codigo_projeto=codigo_projeto,
        codigo_empresa=codigo_empresa,
    ):
        raise ValueError(
            "O Projeto já possui uma Homologação ativa."
        )

    codigo_homologacao = gerar_proximo_codigo(
        homologacoes
    )

    nova_homologacao = criar_dados_homologacao(
        codigo=codigo_homologacao,
        codigo_empresa=codigo_empresa,
        codigo_projeto=codigo_projeto,
        codigo_concessionaria=codigo_concessionaria,
        data_abertura=data_abertura,
        responsavel_abertura=responsavel_abertura,
        prazo_estimado_dias=prazo_estimado_dias,
        observacoes=observacoes,
    )

    homologacoes.append(
        nova_homologacao
    )

    _salvar_alteracoes()

    return nova_homologacao