"""
Construção das Movimentações do Contexto de Homologação.

Uma Movimentação representa um registro histórico imutável de um
acontecimento relevante durante o processo.

Este módulo é responsável por:

- gerar o próximo código interno de uma Movimentação;
- construir Movimentações da Homologação;
- construir Movimentações de Documentos;
- construir Movimentações de Submissões;
- construir Movimentações de Respostas;
- construir Movimentações de Exigências;
- construir registros das mudanças de estado produzidas por
  eventos internos do domínio.

Este módulo não é responsável por:

- adicionar Movimentações à Homologação;
- alterar o estado da Homologação;
- alterar Documentos;
- alterar Submissões;
- alterar Exigências;
- validar transições;
- buscar entidades no agregado;
- decidir quando um evento deve ser registrado.

A decisão de quando criar e registrar cada Movimentação continua
pertencendo ao Aggregate Root:

    app/dominio/homologacoes.py
"""

from app.dominio.documentos_homologacao import (
    StatusDocumentoHomologacao,
)

from app.dominio.status_homologacao import (
    STATUS_INICIAL_HOMOLOGACAO,
    StatusHomologacao,
)

from app.dominio.status_submissao import (
    StatusAnaliseSubmissao,
    StatusOperacionalSubmissao,
)

from app.dominio.submissoes_homologacao import (
    CanalEnvioSubmissao,
)


def gerar_proximo_codigo_movimentacao(
    movimentacoes: list[dict],
) -> int:
    """
    Gera o próximo código interno das Movimentações.

    O código é calculado dentro da própria Homologação.

    Exemplo:

        Movimentações existentes:
            1, 2, 3

        Próximo código:
            4

    Caso a lista esteja vazia, o primeiro código será 1.
    """

    if not movimentacoes:
        return 1

    maior_codigo = max(
        movimentacao.get("codigo", 0)
        for movimentacao in movimentacoes
    )

    return maior_codigo + 1

def criar_movimentacao_de_abertura(
    data_abertura: str,
    responsavel_abertura: str,
) -> dict:
    """
    Cria a primeira Movimentação da Homologação.

    Toda Homologação deve nascer com um registro histórico
    informando que o processo foi aberto.
    """

    return {
        "codigo": 1,
        "tipo_evento": "HOMOLOGACAO_ABERTA",
        "data": data_abertura,
        "responsavel": responsavel_abertura,
        "status_anterior": None,
        "novo_status": STATUS_INICIAL_HOMOLOGACAO.value,
        "descricao": "Homologação aberta.",
        "motivo": None,
    }

def criar_movimentacao_de_status(
    movimentacoes: list[dict],
    status_anterior: StatusHomologacao,
    novo_status: StatusHomologacao,
    data_movimentacao: str,
    responsavel: str,
    descricao: str,
    motivo: str | None,
) -> dict:
    """
    Cria uma Movimentação correspondente à mudança
    de status da Homologação.
    """

    return {
        "codigo": gerar_proximo_codigo_movimentacao(
            movimentacoes
        ),
        "tipo_evento": "STATUS_HOMOLOGACAO_ALTERADO",
        "data": data_movimentacao,
        "responsavel": responsavel,
        "status_anterior": status_anterior.value,
        "novo_status": novo_status.value,
        "descricao": descricao,
        "motivo": motivo,
    }

def criar_movimentacao_instalacao_planejada(
    movimentacoes: list[dict],
    instalacao: dict,
    status_anterior: StatusHomologacao,
    novo_status: StatusHomologacao,
    data_movimentacao: str,
    responsavel: str,
) -> dict:
    """
    Cria uma Movimentação correspondente
    ao planejamento da Instalação.
    """

    return {
        "codigo": gerar_proximo_codigo_movimentacao(
            movimentacoes
        ),
        "tipo_evento": "INSTALACAO_PLANEJADA",
        "data": data_movimentacao,
        "responsavel": responsavel,
        "status_anterior": status_anterior.value,
        "novo_status": novo_status.value,
        "descricao": (
            "Instalação planejada para "
            f"{instalacao['data_prevista']}."
        ),
        "motivo": None,
        "data_prevista_instalacao": (
            instalacao["data_prevista"]
        ),
        "equipe_responsavel": (
            instalacao["equipe_responsavel"]
        ),
    }

def criar_movimentacao_instalacao_iniciada(
    movimentacoes: list[dict],
    instalacao: dict,
    data_movimentacao: str,
    responsavel: str,
) -> dict:
    """
    Cria uma Movimentação correspondente
    ao início da execução da Instalação.
    """

    return {
        "codigo": gerar_proximo_codigo_movimentacao(
            movimentacoes
        ),
        "tipo_evento": "INSTALACAO_INICIADA",
        "data": data_movimentacao,
        "responsavel": responsavel,
        "status_anterior": None,
        "novo_status": None,
        "descricao": (
            "Execução da Instalação iniciada em "
            f"{instalacao['data_inicio']}."
        ),
        "motivo": None,
        "status_instalacao": (
            instalacao["status"]
        ),
        "data_inicio_instalacao": (
            instalacao["data_inicio"]
        ),
        "equipe_responsavel": (
            instalacao["equipe_responsavel"]
        ),
    }

def criar_movimentacao_instalacao_concluida(
    movimentacoes: list[dict],
    instalacao: dict,
    status_anterior: StatusHomologacao,
    novo_status: StatusHomologacao,
    data_movimentacao: str,
    responsavel: str,
) -> dict:
    """
    Cria uma Movimentação correspondente
    à conclusão da Instalação.
    """

    return {
        "codigo": gerar_proximo_codigo_movimentacao(
            movimentacoes
        ),
        "tipo_evento": "INSTALACAO_CONCLUIDA",
        "data": data_movimentacao,
        "responsavel": responsavel,
        "status_anterior": status_anterior.value,
        "novo_status": novo_status.value,
        "descricao": (
            "Instalação concluída em "
            f"{instalacao['data_conclusao']}."
        ),
        "motivo": None,
        "status_instalacao": instalacao["status"],
        "data_inicio_instalacao": (
            instalacao["data_inicio"]
        ),
        "data_conclusao_instalacao": (
            instalacao["data_conclusao"]
        ),
        "equipe_responsavel": (
            instalacao["equipe_responsavel"]
        ),
    }

def criar_movimentacao_vistoria_solicitada(
    movimentacoes: list[dict],
    vistoria: dict,
    status_anterior: StatusHomologacao,
    novo_status: StatusHomologacao,
    data_movimentacao: str,
    responsavel: str,
) -> dict:
    """
    Cria uma Movimentação correspondente
    à solicitação de uma Vistoria.
    """

    return {
        "codigo": gerar_proximo_codigo_movimentacao(
            movimentacoes
        ),
        "tipo_evento": "VISTORIA_SOLICITADA",
        "data": data_movimentacao,
        "responsavel": responsavel,
        "status_anterior": status_anterior.value,
        "novo_status": novo_status.value,
        "descricao": (
            "Vistoria "
            f"{vistoria['numero_sequencial']} "
            "solicitada sob o protocolo "
            f"{vistoria['protocolo']}."
        ),
        "motivo": None,
        "codigo_vistoria": vistoria["codigo"],
        "numero_sequencial_vistoria": (
            vistoria["numero_sequencial"]
        ),
        "protocolo_vistoria": (
            vistoria["protocolo"]
        ),
        "data_solicitacao_vistoria": (
            vistoria["data_solicitacao"]
        ),
    }

def criar_movimentacao_vistoria_agendada(
    movimentacoes: list[dict],
    vistoria: dict,
    status_anterior: StatusHomologacao,
    novo_status: StatusHomologacao,
    data_movimentacao: str,
    responsavel: str,
) -> dict:
    """
    Cria uma Movimentação correspondente
    ao agendamento da Vistoria.
    """

    return {
        "codigo": gerar_proximo_codigo_movimentacao(
            movimentacoes
        ),
        "tipo_evento": "VISTORIA_AGENDADA",
        "data": data_movimentacao,
        "responsavel": responsavel,
        "status_anterior": status_anterior.value,
        "novo_status": novo_status.value,
        "descricao": (
            "Vistoria "
            f"{vistoria['numero_sequencial']} "
            "agendada para "
            f"{vistoria['data_agendamento']}."
        ),
        "motivo": None,
        "codigo_vistoria": vistoria["codigo"],
        "numero_sequencial_vistoria": (
            vistoria["numero_sequencial"]
        ),
        "protocolo_vistoria": (
            vistoria["protocolo"]
        ),
        "data_agendamento_vistoria": (
            vistoria["data_agendamento"]
        ),
    }

def criar_movimentacao_vistoria_realizada(
    movimentacoes: list[dict],
    vistoria: dict,
    data_movimentacao: str,
    responsavel: str,
) -> dict:
    """
    Cria uma Movimentação correspondente
    à realização da Vistoria.

    O estado geral da Homologação permanece
    AGUARDANDO_VISTORIA.
    """

    return {
        "codigo": gerar_proximo_codigo_movimentacao(
            movimentacoes
        ),
        "tipo_evento": "VISTORIA_REALIZADA",
        "data": data_movimentacao,
        "responsavel": responsavel,
        "status_anterior": None,
        "novo_status": None,
        "descricao": (
            "Vistoria "
            f"{vistoria['numero_sequencial']} "
            "realizada em "
            f"{vistoria['data_realizacao']}."
        ),
        "motivo": None,
        "codigo_vistoria": vistoria["codigo"],
        "numero_sequencial_vistoria": (
            vistoria["numero_sequencial"]
        ),
        "protocolo_vistoria": (
            vistoria["protocolo"]
        ),
        "data_realizacao_vistoria": (
            vistoria["data_realizacao"]
        ),
        "status_vistoria": vistoria["status"],
    }

def criar_movimentacao_vistoria_aprovada(
    movimentacoes: list[dict],
    vistoria: dict,
    status_anterior: StatusHomologacao,
    novo_status: StatusHomologacao,
    data_movimentacao: str,
    responsavel: str,
) -> dict:
    """
    Cria uma Movimentação correspondente
    à aprovação da Vistoria.
    """

    return {
        "codigo": gerar_proximo_codigo_movimentacao(
            movimentacoes
        ),
        "tipo_evento": "VISTORIA_APROVADA",
        "data": data_movimentacao,
        "responsavel": responsavel,
        "status_anterior": status_anterior.value,
        "novo_status": novo_status.value,
        "descricao": (
            "Vistoria "
            f"{vistoria['numero_sequencial']} "
            "aprovada."
        ),
        "motivo": None,
        "codigo_vistoria": vistoria["codigo"],
        "numero_sequencial_vistoria": (
            vistoria["numero_sequencial"]
        ),
        "protocolo_vistoria": (
            vistoria["protocolo"]
        ),
        "data_resultado_vistoria": (
            vistoria["data_resultado"]
        ),
        "resultado_vistoria": (
            vistoria["resultado"]
        ),
    }

def criar_movimentacao_vistoria_reprovada(
    movimentacoes: list[dict],
    vistoria: dict,
    status_anterior: StatusHomologacao,
    novo_status: StatusHomologacao,
    data_movimentacao: str,
    responsavel: str,
) -> dict:
    """
    Cria uma Movimentação correspondente
    à reprovação da Vistoria.
    """

    return {
        "codigo": gerar_proximo_codigo_movimentacao(
            movimentacoes
        ),
        "tipo_evento": "VISTORIA_REPROVADA",
        "data": data_movimentacao,
        "responsavel": responsavel,
        "status_anterior": status_anterior.value,
        "novo_status": novo_status.value,
        "descricao": (
            "Vistoria "
            f"{vistoria['numero_sequencial']} "
            "reprovada."
        ),
        "motivo": vistoria["motivo_reprovacao"],
        "codigo_vistoria": vistoria["codigo"],
        "numero_sequencial_vistoria": (
            vistoria["numero_sequencial"]
        ),
        "protocolo_vistoria": (
            vistoria["protocolo"]
        ),
        "data_resultado_vistoria": (
            vistoria["data_resultado"]
        ),
        "resultado_vistoria": (
            vistoria["resultado"]
        ),
    }

def criar_movimentacao_correcao_pos_vistoria(
    movimentacoes: list[dict],
    vistoria: dict,
    status_anterior: StatusHomologacao,
    novo_status: StatusHomologacao,
    data_movimentacao: str,
    responsavel: str,
    descricao_correcao: str,
) -> dict:
    """
    Cria uma Movimentação correspondente
    ao registro da correção pós-vistoria.
    """

    return {
        "codigo": gerar_proximo_codigo_movimentacao(
            movimentacoes
        ),
        "tipo_evento": "CORRECAO_POS_VISTORIA",
        "data": data_movimentacao,
        "responsavel": responsavel,
        "status_anterior": status_anterior.value,
        "novo_status": novo_status.value,
        "descricao": (
            "Correção pós-vistoria registrada para "
            f"a Vistoria {vistoria['numero_sequencial']}."
        ),
        "motivo": vistoria["motivo_reprovacao"],
        "codigo_vistoria": vistoria["codigo"],
        "numero_sequencial_vistoria": (
            vistoria["numero_sequencial"]
        ),
        "descricao_correcao": descricao_correcao,
    }

def criar_movimentacao_documento_adicionado(
    movimentacoes: list[dict],
    documento: dict,
    data_movimentacao: str,
    responsavel: str,
) -> dict:
    """
    Cria uma Movimentação informando a inclusão
    de um Documento.
    """

    return {
        "codigo": gerar_proximo_codigo_movimentacao(
            movimentacoes
        ),
        "tipo_evento": "DOCUMENTO_ADICIONADO",
        "data": data_movimentacao,
        "responsavel": responsavel,
        "status_anterior": None,
        "novo_status": None,
        "descricao": (
            "Documento adicionado à Homologação: "
            f"{documento['nome']}."
        ),
        "motivo": None,
        "codigo_documento": documento["codigo"],
    }

def criar_movimentacao_status_documento(
    movimentacoes: list[dict],
    documento: dict,
    status_anterior: StatusDocumentoHomologacao,
    novo_status: StatusDocumentoHomologacao,
    data_movimentacao: str,
    responsavel: str,
    motivo: str | None,
) -> dict:
    """
    Cria uma Movimentação de mudança de status documental.
    """

    return {
        "codigo": gerar_proximo_codigo_movimentacao(
            movimentacoes
        ),
        "tipo_evento": "STATUS_DOCUMENTO_ALTERADO",
        "data": data_movimentacao,
        "responsavel": responsavel,
        "status_anterior": status_anterior.value,
        "novo_status": novo_status.value,
        "descricao": (
            f"Status do documento '{documento['nome']}' "
            f"alterado de {status_anterior.value} "
            f"para {novo_status.value}."
        ),
        "motivo": motivo,
        "codigo_documento": documento["codigo"],
    }

def criar_movimentacao_submissao_adicionada(
    movimentacoes: list[dict],
    submissao: dict,
    data_movimentacao: str,
    responsavel: str,
) -> dict:
    """
    Cria a Movimentação referente à inclusão de uma Submissão.
    """

    return {
        "codigo": gerar_proximo_codigo_movimentacao(
            movimentacoes
        ),
        "tipo_evento": "SUBMISSAO_ADICIONADA",
        "data": data_movimentacao,
        "responsavel": responsavel,
        "status_anterior": None,
        "novo_status": None,
        "descricao": (
            "Submissão adicionada à Homologação: "
            f"{submissao['tipo']} "
            f"nº {submissao['numero_sequencial']}."
        ),
        "motivo": None,
        "codigo_submissao": submissao["codigo"],
        "numero_sequencial_submissao": (
            submissao["numero_sequencial"]
        ),
        "tipo_submissao": submissao["tipo"],
    }

def criar_movimentacao_status_operacional_submissao(
    movimentacoes: list[dict],
    submissao: dict,
    status_anterior: StatusOperacionalSubmissao,
    novo_status: StatusOperacionalSubmissao,
    data_movimentacao: str,
    responsavel: str,
    motivo: str | None,
) -> dict:
    """
    Cria uma Movimentação de alteração do status operacional
    de uma Submissão.
    """

    return {
        "codigo": gerar_proximo_codigo_movimentacao(
            movimentacoes
        ),
        "tipo_evento": (
            "STATUS_OPERACIONAL_SUBMISSAO_ALTERADO"
        ),
        "data": data_movimentacao,
        "responsavel": responsavel,
        "status_anterior": status_anterior.value,
        "novo_status": novo_status.value,
        "descricao": (
            "Status operacional da Submissão "
            f"nº {submissao['numero_sequencial']} "
            f"alterado de {status_anterior.value} "
            f"para {novo_status.value}."
        ),
        "motivo": motivo,
        "codigo_submissao": submissao["codigo"],
        "numero_sequencial_submissao": (
            submissao["numero_sequencial"]
        ),
    }

def criar_movimentacao_submissao_enviada(
    movimentacoes: list[dict],
    submissao: dict,
    canal_envio: CanalEnvioSubmissao,
    data_envio: str,
    responsavel_envio: str,
) -> dict:
    """
    Cria a Movimentação referente ao envio formal
    da Submissão.
    """

    return {
        "codigo": gerar_proximo_codigo_movimentacao(
            movimentacoes
        ),
        "tipo_evento": "SUBMISSAO_ENVIADA",
        "data": data_envio,
        "responsavel": responsavel_envio,
        "status_anterior": (
            StatusOperacionalSubmissao
            .PRONTA_PARA_ENVIO
            .value
        ),
        "novo_status": (
            StatusOperacionalSubmissao
            .ENVIADA
            .value
        ),
        "descricao": (
            "Submissão "
            f"nº {submissao['numero_sequencial']} "
            "enviada à concessionária pelo canal "
            f"{canal_envio.value}."
        ),
        "motivo": None,
        "codigo_submissao": submissao["codigo"],
        "numero_sequencial_submissao": (
            submissao["numero_sequencial"]
        ),
        "tipo_submissao": submissao["tipo"],
        "canal_envio": canal_envio.value,
    }

def criar_movimentacao_submissao_protocolada(
    movimentacoes: list[dict],
    submissao: dict,
    protocolo: str,
    data_protocolo: str,
    responsavel: str,
) -> dict:
    """
    Cria a Movimentação referente à protocolação
    de uma Submissão.
    """

    return {
        "codigo": gerar_proximo_codigo_movimentacao(
            movimentacoes
        ),
        "tipo_evento": "SUBMISSAO_PROTOCOLADA",
        "data": data_protocolo,
        "responsavel": responsavel,
        "status_anterior": (
            StatusOperacionalSubmissao
            .ENVIADA
            .value
        ),
        "novo_status": (
            StatusOperacionalSubmissao
            .PROTOCOLADA
            .value
        ),
        "descricao": (
            "Submissão "
            f"nº {submissao['numero_sequencial']} "
            "protocolada na concessionária sob o número "
            f"{protocolo}."
        ),
        "motivo": None,
        "codigo_submissao": submissao["codigo"],
        "numero_sequencial_submissao": (
            submissao["numero_sequencial"]
        ),
        "tipo_submissao": submissao["tipo"],
        "protocolo": protocolo,
    }

def criar_movimentacao_resposta_concessionaria(
    movimentacoes: list[dict],
    submissao: dict,
    resposta: dict,
    status_anterior: StatusAnaliseSubmissao,
    novo_status: StatusAnaliseSubmissao,
) -> dict:
    """
    Cria a Movimentação referente ao registro de uma
    Resposta da concessionária.
    """

    return {
        "codigo": gerar_proximo_codigo_movimentacao(
            movimentacoes
        ),
        "tipo_evento": (
            "RESPOSTA_CONCESSIONARIA_REGISTRADA"
        ),
        "data": resposta["data_registro"],
        "responsavel": resposta["responsavel_registro"],
        "status_anterior": status_anterior.value,
        "novo_status": novo_status.value,
        "descricao": (
            "Resposta da concessionária registrada para a "
            f"Submissão nº {submissao['numero_sequencial']}: "
            f"{resposta['tipo']}."
        ),
        "motivo": None,
        "codigo_submissao": submissao["codigo"],
        "numero_sequencial_submissao": (
            submissao["numero_sequencial"]
        ),
        "codigo_resposta": resposta["codigo"],
        "numero_sequencial_resposta": (
            resposta["numero_sequencial"]
        ),
        "tipo_resposta": resposta["tipo"],
    }

def criar_movimentacao_resposta_exigencia(
    movimentacoes: list[dict],
    submissao: dict,
    resposta: dict,
    status_anterior: StatusAnaliseSubmissao,
) -> dict:
    """
    Cria a Movimentação referente ao recebimento de uma
    Resposta contendo Exigências.
    """

    codigos_exigencias = [
        exigencia["codigo"]
        for exigencia in resposta["exigencias"]
    ]

    return {
        "codigo": gerar_proximo_codigo_movimentacao(
            movimentacoes
        ),
        "tipo_evento": (
            "EXIGENCIAS_CONCESSIONARIA_REGISTRADAS"
        ),
        "data": resposta["data_registro"],
        "responsavel": resposta["responsavel_registro"],
        "status_anterior": status_anterior.value,
        "novo_status": (
            StatusAnaliseSubmissao.COM_EXIGENCIA.value
        ),
        "descricao": (
            "Resposta de Exigência registrada para a "
            f"Submissão nº {submissao['numero_sequencial']}, "
            f"contendo {len(codigos_exigencias)} "
            "Exigência(s)."
        ),
        "motivo": None,
        "codigo_submissao": submissao["codigo"],
        "numero_sequencial_submissao": (
            submissao["numero_sequencial"]
        ),
        "codigo_resposta": resposta["codigo"],
        "numero_sequencial_resposta": (
            resposta["numero_sequencial"]
        ),
        "tipo_resposta": resposta["tipo"],
        "codigos_exigencias": codigos_exigencias,
    }