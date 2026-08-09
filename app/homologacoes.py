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
    agendar_vistoria,
    aprovar_vistoria,
    agendar_ligacao,
    buscar_homologacao_ativa_por_projeto,
    buscar_homologacao_por_codigo,
    buscar_homologacoes_por_concessionaria,
    buscar_homologacoes_por_status,
    concluir_instalacao,
    concluir_ligacao,
    criar_dados_homologacao,
    iniciar_instalacao,
    projeto_possui_homologacao_ativa,
    quantidade_homologacoes_aguardando_envio,
    quantidade_homologacoes_aguardando_resposta,
    quantidade_homologacoes_com_exigencia_aberta,
    quantidade_homologacoes_por_status,
    quantidade_homologacoes_sem_responsavel,
    quantidade_total_pendencias_homologacao,
    registrar_correcao_pos_vistoria,
    registrar_planejamento_instalacao,
    registrar_realizacao_vistoria,
    reprovar_vistoria,
    solicitar_vistoria,
    solicitar_ligacao,
)

from app.dominio.status_homologacao import (
    StatusHomologacao,
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

buscar_por_concessionaria_no_dominio = (
    buscar_homologacoes_por_concessionaria
)

buscar_por_status_no_dominio = (
    buscar_homologacoes_por_status
)

planejar_instalacao_no_dominio = (
    registrar_planejamento_instalacao
)

iniciar_instalacao_no_dominio = (
    iniciar_instalacao
)

concluir_instalacao_no_dominio = (
    concluir_instalacao
)

solicitar_vistoria_no_dominio = (
    solicitar_vistoria
)

agendar_vistoria_no_dominio = (
    agendar_vistoria
)

registrar_realizacao_vistoria_no_dominio = (
    registrar_realizacao_vistoria
)

aprovar_vistoria_no_dominio = (
    aprovar_vistoria
)

reprovar_vistoria_no_dominio = (
    reprovar_vistoria
)

registrar_correcao_pos_vistoria_no_dominio = (
    registrar_correcao_pos_vistoria
)

solicitar_ligacao_no_dominio = (
    solicitar_ligacao
)

agendar_ligacao_no_dominio = (
    agendar_ligacao
)

concluir_ligacao_no_dominio = (
    concluir_ligacao
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

def listar_homologacoes_por_concessionaria(
    codigo_concessionaria: int,
    codigo_empresa: int | None = None,
) -> list[dict[str, Any]]:
    """
    Retorna as Homologações vinculadas
    à Concessionária informada.

    Quando codigo_empresa for fornecido, a consulta
    também respeita o isolamento entre Empresas.
    """

    return buscar_por_concessionaria_no_dominio(
        homologacoes=homologacoes,
        codigo_concessionaria=codigo_concessionaria,
        codigo_empresa=codigo_empresa,
    )

def listar_homologacoes_por_status(
    status: str | StatusHomologacao,
    codigo_empresa: int | None = None,
) -> list[dict[str, Any]]:
    """
    Retorna as Homologações que possuem
    o status informado.

    Quando codigo_empresa for fornecido, a consulta
    também respeita o isolamento entre Empresas.
    """

    return buscar_por_status_no_dominio(
        homologacoes=homologacoes,
        status=status,
        codigo_empresa=codigo_empresa,
    )

def quantidade_homologacoes(
    codigo_empresa: int | None = None,
) -> int:
    """
    Retorna a quantidade de Homologações cadastradas.

    Quando codigo_empresa for informado, considera somente
    as Homologações pertencentes à Empresa indicada.
    """

    return len(
        listar_homologacoes(
            codigo_empresa=codigo_empresa,
        )
    )

def quantidade_homologacoes_aguardando_documentacao() -> int:
    """
    Retorna a quantidade de Homologações
    aguardando documentação.
    """

    return quantidade_homologacoes_por_status(
        homologacoes=homologacoes,
        status=(
            StatusHomologacao
            .AGUARDANDO_DOCUMENTACAO
        ),
    )

def quantidade_homologacoes_com_exigencias_abertas() -> int:
    """
    Retorna a quantidade de Homologações
    que possuem ao menos uma Exigência aberta.
    """

    return quantidade_homologacoes_com_exigencia_aberta(
        homologacoes
    )

def quantidade_homologacoes_pendentes_de_envio() -> int:
    """
    Retorna a quantidade de Homologações
    com Submissão pronta para envio.
    """

    return quantidade_homologacoes_aguardando_envio(
        homologacoes
    )

def quantidade_homologacoes_pendentes_de_resposta() -> int:
    """
    Retorna a quantidade de Homologações
    com Submissão enviada e ainda sem resposta.
    """

    return quantidade_homologacoes_aguardando_resposta(
        homologacoes
    )

def quantidade_homologacoes_sem_responsavel_atual() -> int:
    """
    Retorna a quantidade de Homologações ativas
    sem responsável atual definido.
    """

    return quantidade_homologacoes_sem_responsavel(
        homologacoes
    )

def quantidade_total_pendencias() -> int:
    """
    Retorna a soma das categorias de pendência
    das Homologações.

    Uma mesma Homologação pode contribuir para mais
    de uma categoria.
    """

    return quantidade_total_pendencias_homologacao(
        homologacoes
    )

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

# ============================================================
# OPERAÇÕES DE CAMPO — INSTALAÇÃO
# ============================================================

def planejar_instalacao(
    codigo_homologacao: int,
    codigo_empresa: int,
    data_prevista: str,
    responsavel_planejamento: str,
    equipe_responsavel: str,
    data_movimentacao: str,
    observacoes: str | None = None,
) -> dict[str, Any]:
    """
    Registra e persiste o planejamento
    da Instalação de uma Homologação.

    A busca aplica o isolamento por Empresa.
    """

    homologacao = _obter_homologacao_obrigatoria(
        codigo_homologacao=codigo_homologacao,
        codigo_empresa=codigo_empresa,
    )

    homologacao_atualizada = (
        planejar_instalacao_no_dominio(
            homologacao=homologacao,
            data_prevista=data_prevista,
            responsavel_planejamento=(
                responsavel_planejamento
            ),
            equipe_responsavel=(
                equipe_responsavel
            ),
            data_movimentacao=(
                data_movimentacao
            ),
            observacoes=observacoes,
        )
    )

    _salvar_alteracoes()

    return homologacao_atualizada

def iniciar_execucao_instalacao(
    codigo_homologacao: int,
    codigo_empresa: int,
    data_inicio: str,
    responsavel_inicio: str,
    data_movimentacao: str,
) -> dict[str, Any]:
    """
    Registra e persiste o início
    da execução da Instalação.

    A busca aplica o isolamento por Empresa.
    """

    homologacao = _obter_homologacao_obrigatoria(
        codigo_homologacao=codigo_homologacao,
        codigo_empresa=codigo_empresa,
    )

    homologacao_atualizada = (
        iniciar_instalacao_no_dominio(
            homologacao=homologacao,
            data_inicio=data_inicio,
            responsavel_inicio=(
                responsavel_inicio
            ),
            data_movimentacao=(
                data_movimentacao
            ),
        )
    )

    _salvar_alteracoes()

    return homologacao_atualizada

def concluir_execucao_instalacao(
    codigo_homologacao: int,
    codigo_empresa: int,
    data_conclusao: str,
    responsavel_conclusao: str,
    data_movimentacao: str,
    observacoes: str | None = None,
) -> dict[str, Any]:
    """
    Registra e persiste a conclusão
    da Instalação.

    A busca aplica o isolamento por Empresa.
    """

    homologacao = _obter_homologacao_obrigatoria(
        codigo_homologacao=codigo_homologacao,
        codigo_empresa=codigo_empresa,
    )

    homologacao_atualizada = (
        concluir_instalacao_no_dominio(
            homologacao=homologacao,
            data_conclusao=data_conclusao,
            responsavel_conclusao=(
                responsavel_conclusao
            ),
            data_movimentacao=(
                data_movimentacao
            ),
            observacoes=observacoes,
        )
    )

    _salvar_alteracoes()

    return homologacao_atualizada

# ============================================================
# OPERAÇÕES DE CAMPO — VISTORIA
# ============================================================

def solicitar_nova_vistoria(
    codigo_homologacao: int,
    codigo_empresa: int,
    data_solicitacao: str,
    responsavel_solicitacao: str,
    protocolo: str,
    data_movimentacao: str,
    observacoes: str | None = None,
) -> dict[str, Any]:
    """
    Solicita e persiste uma nova tentativa
    de Vistoria da Homologação.

    A busca aplica o isolamento por Empresa.
    """

    homologacao = _obter_homologacao_obrigatoria(
        codigo_homologacao=codigo_homologacao,
        codigo_empresa=codigo_empresa,
    )

    homologacao_atualizada = (
        solicitar_vistoria_no_dominio(
            homologacao=homologacao,
            data_solicitacao=data_solicitacao,
            responsavel_solicitacao=(
                responsavel_solicitacao
            ),
            protocolo=protocolo,
            data_movimentacao=data_movimentacao,
            observacoes=observacoes,
        )
    )

    _salvar_alteracoes()

    return homologacao_atualizada

def agendar_vistoria_homologacao(
    codigo_homologacao: int,
    codigo_empresa: int,
    codigo_vistoria: int,
    data_agendamento: str,
    responsavel_agendamento: str,
    data_movimentacao: str,
    observacoes: str | None = None,
) -> dict[str, Any]:
    """
    Agenda e persiste uma Vistoria
    existente da Homologação.
    """

    homologacao = _obter_homologacao_obrigatoria(
        codigo_homologacao=codigo_homologacao,
        codigo_empresa=codigo_empresa,
    )

    homologacao_atualizada = (
        agendar_vistoria_no_dominio(
            homologacao=homologacao,
            codigo_vistoria=codigo_vistoria,
            data_agendamento=data_agendamento,
            responsavel_agendamento=(
                responsavel_agendamento
            ),
            data_movimentacao=data_movimentacao,
            observacoes=observacoes,
        )
    )

    _salvar_alteracoes()

    return homologacao_atualizada

def registrar_realizacao_vistoria_homologacao(
    codigo_homologacao: int,
    codigo_empresa: int,
    codigo_vistoria: int,
    data_realizacao: str,
    responsavel_realizacao: str,
    data_movimentacao: str,
    observacoes: str | None = None,
) -> dict[str, Any]:
    """
    Registra e persiste a realização
    de uma Vistoria.
    """

    homologacao = _obter_homologacao_obrigatoria(
        codigo_homologacao=codigo_homologacao,
        codigo_empresa=codigo_empresa,
    )

    homologacao_atualizada = (
        registrar_realizacao_vistoria_no_dominio(
            homologacao=homologacao,
            codigo_vistoria=codigo_vistoria,
            data_realizacao=data_realizacao,
            responsavel_realizacao=(
                responsavel_realizacao
            ),
            data_movimentacao=data_movimentacao,
            observacoes=observacoes,
        )
    )

    _salvar_alteracoes()

    return homologacao_atualizada

def aprovar_vistoria_homologacao(
    codigo_homologacao: int,
    codigo_empresa: int,
    codigo_vistoria: int,
    data_resultado: str,
    responsavel_resultado: str,
    data_movimentacao: str,
    observacoes: str | None = None,
) -> dict[str, Any]:
    """
    Registra e persiste a aprovação
    formal de uma Vistoria.
    """

    homologacao = _obter_homologacao_obrigatoria(
        codigo_homologacao=codigo_homologacao,
        codigo_empresa=codigo_empresa,
    )

    homologacao_atualizada = (
        aprovar_vistoria_no_dominio(
            homologacao=homologacao,
            codigo_vistoria=codigo_vistoria,
            data_resultado=data_resultado,
            responsavel_resultado=(
                responsavel_resultado
            ),
            data_movimentacao=data_movimentacao,
            observacoes=observacoes,
        )
    )

    _salvar_alteracoes()

    return homologacao_atualizada

def reprovar_vistoria_homologacao(
    codigo_homologacao: int,
    codigo_empresa: int,
    codigo_vistoria: int,
    data_resultado: str,
    responsavel_resultado: str,
    motivo_reprovacao: str,
    data_movimentacao: str,
    observacoes: str | None = None,
) -> dict[str, Any]:
    """
    Registra e persiste a reprovação
    formal de uma Vistoria.
    """

    homologacao = _obter_homologacao_obrigatoria(
        codigo_homologacao=codigo_homologacao,
        codigo_empresa=codigo_empresa,
    )

    homologacao_atualizada = (
        reprovar_vistoria_no_dominio(
            homologacao=homologacao,
            codigo_vistoria=codigo_vistoria,
            data_resultado=data_resultado,
            responsavel_resultado=(
                responsavel_resultado
            ),
            motivo_reprovacao=motivo_reprovacao,
            data_movimentacao=data_movimentacao,
            observacoes=observacoes,
        )
    )

    _salvar_alteracoes()

    return homologacao_atualizada

def registrar_correcao_pos_vistoria_homologacao(
    codigo_homologacao: int,
    codigo_empresa: int,
    codigo_vistoria: int,
    descricao_correcao: str,
    responsavel_correcao: str,
    data_movimentacao: str,
) -> dict[str, Any]:
    """
    Registra e persiste a correção realizada
    após uma Vistoria reprovada.
    """

    homologacao = _obter_homologacao_obrigatoria(
        codigo_homologacao=codigo_homologacao,
        codigo_empresa=codigo_empresa,
    )

    homologacao_atualizada = (
        registrar_correcao_pos_vistoria_no_dominio(
            homologacao=homologacao,
            codigo_vistoria=codigo_vistoria,
            descricao_correcao=descricao_correcao,
            responsavel_correcao=(
                responsavel_correcao
            ),
            data_movimentacao=data_movimentacao,
        )
    )

    _salvar_alteracoes()

    return homologacao_atualizada

# ============================================================
# OPERAÇÕES DE CAMPO — LIGAÇÃO E ENERGIZAÇÃO
# ============================================================

def solicitar_ligacao_homologacao(
    codigo_homologacao: int,
    codigo_empresa: int,
    data_solicitacao: str,
    responsavel_solicitacao: str,
    protocolo: str,
    data_movimentacao: str,
    observacoes: str | None = None,
) -> dict[str, Any]:
    """
    Solicita e persiste a Ligação
    e Energização da Homologação.

    A busca aplica o isolamento por Empresa.
    """

    homologacao = _obter_homologacao_obrigatoria(
        codigo_homologacao=codigo_homologacao,
        codigo_empresa=codigo_empresa,
    )

    homologacao_atualizada = (
        solicitar_ligacao_no_dominio(
            homologacao=homologacao,
            data_solicitacao=data_solicitacao,
            responsavel_solicitacao=(
                responsavel_solicitacao
            ),
            protocolo=protocolo,
            data_movimentacao=data_movimentacao,
            observacoes=observacoes,
        )
    )

    _salvar_alteracoes()

    return homologacao_atualizada

def agendar_ligacao_homologacao(
    codigo_homologacao: int,
    codigo_empresa: int,
    data_agendamento: str,
    responsavel_agendamento: str,
    data_movimentacao: str,
    observacoes: str | None = None,
) -> dict[str, Any]:
    """
    Agenda e persiste a Ligação
    da Homologação.
    """

    homologacao = _obter_homologacao_obrigatoria(
        codigo_homologacao=codigo_homologacao,
        codigo_empresa=codigo_empresa,
    )

    homologacao_atualizada = (
        agendar_ligacao_no_dominio(
            homologacao=homologacao,
            data_agendamento=data_agendamento,
            responsavel_agendamento=(
                responsavel_agendamento
            ),
            data_movimentacao=data_movimentacao,
            observacoes=observacoes,
        )
    )

    _salvar_alteracoes()

    return homologacao_atualizada

def concluir_ligacao_homologacao(
    codigo_homologacao: int,
    codigo_empresa: int,
    data_ligacao: str,
    responsavel_ligacao: str,
    data_movimentacao: str,
    observacoes: str | None = None,
) -> dict[str, Any]:
    """
    Registra e persiste a conclusão
    da Ligação e Energização.
    """

    homologacao = _obter_homologacao_obrigatoria(
        codigo_homologacao=codigo_homologacao,
        codigo_empresa=codigo_empresa,
    )

    homologacao_atualizada = (
        concluir_ligacao_no_dominio(
            homologacao=homologacao,
            data_ligacao=data_ligacao,
            responsavel_ligacao=(
                responsavel_ligacao
            ),
            data_movimentacao=data_movimentacao,
            observacoes=observacoes,
        )
    )

    _salvar_alteracoes()

    return homologacao_atualizada
