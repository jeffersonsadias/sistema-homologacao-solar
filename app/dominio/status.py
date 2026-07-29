from enum import Enum


STATUS_PROJETO = {
    1: "Aguardando documentação",
    2: "Documentação recebida",
    3: "Em análise pela distribuidora",
    4: "Correção solicitada",
    5: "Aprovado",
    6: "Instalação concluída",
    7: "Vistoria solicitada",
    8: "Vistoria aprovada",
    9: "Homologado",
    10: "Cancelado",
}


STATUS_INICIAL = STATUS_PROJETO[1]


TRANSICOES_PERMITIDAS = {
    "Aguardando documentação": [
        "Documentação recebida",
        "Cancelado",
    ],

    "Documentação recebida": [
        "Em análise pela distribuidora",
        "Cancelado",
    ],

    "Em análise pela distribuidora": [
        "Correção solicitada",
        "Aprovado",
        "Cancelado",
    ],

    "Correção solicitada": [
        "Documentação recebida",
        "Cancelado",
    ],

    "Aprovado": [
        "Instalação concluída",
        "Cancelado",
    ],

    "Instalação concluída": [
        "Vistoria solicitada",
        "Cancelado",
    ],

    "Vistoria solicitada": [
        "Vistoria aprovada",
        "Correção solicitada",
        "Cancelado",
    ],

    "Vistoria aprovada": [
        "Homologado",
        "Cancelado",
    ],

    "Homologado": [],
    "Cancelado": [],
}


def obter_status(codigo):
    """
    Retorna a descrição correspondente ao código.

    Retorna None quando o código não existe.
    """

    return STATUS_PROJETO.get(codigo)


def status_valido(codigo):
    """
    Verifica se o código informado representa
    um status válido.
    """

    return codigo in STATUS_PROJETO


def transicao_permitida(
    status_atual,
    novo_status,
):
    """
    Verifica se uma transição entre dois status
    é permitida.
    """

    proximos_status = TRANSICOES_PERMITIDAS.get(
        status_atual,
        [],
    )

    return novo_status in proximos_status

# ============================================================
# SPRINT 2 — ESTADOS DO NOVO DOMÍNIO
# ============================================================


class SituacaoProcesso(str, Enum):
    """
    Representa a situação administrativa geral de um
    Processo de Homologação.

    A situação informa a condição global do Processo,
    enquanto a fase informa em qual etapa do fluxo ele está.
    """

    RASCUNHO = "RASCUNHO"
    EM_PREPARACAO = "EM_PREPARACAO"
    ATIVO = "ATIVO"
    SUSPENSO = "SUSPENSO"
    CONCLUIDO = "CONCLUIDO"
    REJEITADO = "REJEITADO"
    CANCELADO = "CANCELADO"
    ARQUIVADO = "ARQUIVADO"


class FaseProcesso(str, Enum):
    """
    Representa a etapa atual do Processo de Homologação.

    Nesta primeira implementação, são incluídas apenas as fases
    necessárias para o primeiro fluxo funcional da Sprint 2.
    """

    CADASTRO_INICIAL = "CADASTRO_INICIAL"
    LEVANTAMENTO = "LEVANTAMENTO"
    VALIDACAO_INTERNA = "VALIDACAO_INTERNA"
    PREPARACAO_TECNICA = "PREPARACAO_TECNICA"
    PREPARACAO_DOCUMENTAL = "PREPARACAO_DOCUMENTAL"
    PRONTO_PARA_SUBMISSAO = "PRONTO_PARA_SUBMISSAO"


class SituacaoConcessionaria(str, Enum):
    """
    Representa a situação cadastral de uma Concessionária
    dentro da plataforma.
    """

    ATIVA = "ATIVA"
    INATIVA = "INATIVA"
    SUSPENSA = "SUSPENSA"


class SituacaoUnidadeConsumidora(str, Enum):
    """
    Representa a situação cadastral de uma Unidade Consumidora.

    Essa situação não representa o papel da Unidade no Projeto.
    Os papéis Geradora e Beneficiária serão definidos no
    contexto de cada Projeto.
    """

    ATIVA = "ATIVA"
    INATIVA = "INATIVA"
    SUSPENSA = "SUSPENSA"


class PapelUnidadeProjeto(str, Enum):
    """
    Representa o papel desempenhado por uma Unidade Consumidora
    dentro de um Projeto específico.
    """

    GERADORA = "GERADORA"
    BENEFICIARIA = "BENEFICIARIA"