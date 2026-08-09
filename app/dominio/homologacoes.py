"""
Aggregate Root do Contexto de Homologação.

A Homologação representa o processo completo conduzido entre a
empresa de energia solar e a concessionária.

Estrutura coordenada pelo agregado:

    Homologação
    ├── Documentos
    ├── Submissões
    │   └── Respostas
    │       └── Exigências
    └── Movimentações

Este módulo é responsável por:

- criar a estrutura inicial da Homologação;
- buscar Homologações;
- proteger a regra de uma Homologação ativa por Projeto;
- alterar o estado geral do processo;
- aplicar eventos internos de negócio;
- adicionar e versionar Documentos;
- adicionar, preparar, enviar e protocolar Submissões;
- validar Submissões derivadas e suas origens;
- registrar Respostas da concessionária;
- registrar e atender Exigências;
- coordenar os efeitos entre as entidades internas;
- preservar a atomicidade das operações;
- registrar toda alteração relevante em Movimentações.

Este módulo atua como a única porta de entrada para alterações que
envolvem mais de uma entidade do contexto.

Os módulos especializados permanecem responsáveis por suas regras
locais:

- documentos_homologacao.py;
- submissoes_homologacao.py;
- respostas_concessionaria.py;
- exigencias_concessionaria.py;
- status_homologacao.py;
- status_submissao.py;
- movimentacoes_homologacao.py.

Este módulo não é responsável por:

- interagir diretamente com o usuário;
- controlar menus ou interfaces;
- persistir dados em JSON;
- acessar bancos de dados;
- alterar diretamente Projetos ou Clientes;
- enviar dados reais para portais de concessionárias.
"""

from datetime import date, timedelta

from app.dominio.documentos_homologacao import (
    StatusDocumentoHomologacao,
    buscar_documento_por_codigo,
    converter_status_documento,
    transicao_status_documento_e_valida,
)

from app.dominio.exigencias_concessionaria import (
    StatusAtendimentoExigencia,
    validar_compatibilidade_exigencia_submissao,
    validar_exigencia,
    validar_transicao_status_exigencia,
)

from app.dominio.respostas_concessionaria import (
    TipoRespostaConcessionaria,
    obter_status_resultante_resposta,
    validar_resposta_concessionaria,
)

from app.dominio.submissoes_homologacao import (
    CanalEnvioSubmissao,
    TipoSubmissao,
    validar_submissao,
)

from app.dominio.status_submissao import (
    StatusAnaliseSubmissao,
    StatusOperacionalSubmissao,
    validar_transicao_analise_submissao,
    validar_transicao_operacional_submissao,
)

from app.dominio.status_homologacao import (
    STATUS_INICIAL_HOMOLOGACAO,
    EventoHomologacao,
    StatusHomologacao,
    status_homologacao_e_terminal,
    transicao_status_homologacao_e_valida,
    validar_evento_no_estado_homologacao,
)

from app.dominio.movimentacoes_homologacao import (
    criar_movimentacao_de_abertura,
    criar_movimentacao_de_status,
    criar_movimentacao_documento_adicionado,
    criar_movimentacao_instalacao_concluida,
    criar_movimentacao_instalacao_iniciada,
    criar_movimentacao_instalacao_planejada,
    criar_movimentacao_vistoria_solicitada,
    criar_movimentacao_vistoria_agendada,
    criar_movimentacao_vistoria_realizada,
    criar_movimentacao_vistoria_aprovada,
    criar_movimentacao_vistoria_reprovada,
    criar_movimentacao_correcao_pos_vistoria,
    criar_movimentacao_resposta_concessionaria,
    criar_movimentacao_resposta_exigencia,
    criar_movimentacao_status_documento,
    criar_movimentacao_status_operacional_submissao,
    criar_movimentacao_submissao_adicionada,
    criar_movimentacao_submissao_enviada,
    criar_movimentacao_submissao_protocolada,
    criar_movimentacao_ligacao_agendada,
    criar_movimentacao_ligacao_concluida,
    criar_movimentacao_ligacao_solicitada,
)

from app.dominio.operacoes_campo import (
    StatusVistoria,
    StatusLigacao,
    buscar_ultima_vistoria,
    buscar_vistoria_por_codigo,
    criar_dados_operacoes_campo,
    criar_dados_planejamento_instalacao,
    criar_dados_vistoria_solicitada,
    criar_dados_ligacao_solicitada,
    gerar_proximo_codigo_vistoria,
    gerar_proximo_numero_sequencial_vistoria,
    preparar_agendamento_vistoria,
    preparar_conclusao_instalacao,
    preparar_inicio_instalacao,
    preparar_realizacao_vistoria,
    preparar_aprovacao_vistoria,
    preparar_reprovacao_vistoria,
    preparar_agendamento_ligacao,
    preparar_conclusao_ligacao,
    validar_instalacao,
    validar_operacoes_campo,
    validar_vistoria,
    validar_ligacao,
)

# ============================================================
# MAPA INTERNO DO MÓDULO
# ============================================================
#
# 01. Validadores e normalizadores gerais
# 02. Regras privadas de Respostas e Exigências
# 03. Conversores e validadores de estados
# 04. Regras privadas de Documentos
# 05. Auxiliares do estado geral da Homologação
# 06. Criação da Homologação
# 07. Consultas da Homologação
# 08. Estado e eventos da Homologação
# 09. Preparação atômica do agregado
# 10. Operações de Documentos
# 11. Consultas de Submissões
# 12. Regras relacionais privadas de Submissões
# 13. Operações de Submissões
# 14. Operações de Respostas da concessionária
# 15. Operações de Campo
#
# As funções privadas aparecem antes das operações públicas que
# dependem delas. Essa organização facilita a navegação sem dividir
# artificialmente o Aggregate Root em vários módulos.

# ============================================================
# VALIDADORES E NORMALIZADORES GERAIS
# ============================================================

def _validar_estrutura_homologacao(
    homologacao: dict,
) -> None:
    """
    Valida a estrutura mínima de uma Homologação.

    Esta função não valida todos os dados da entidade.

    Ela verifica somente os elementos indispensáveis para que uma
    operação de domínio possa ser executada com segurança.
    """

    if not isinstance(homologacao, dict):
        raise TypeError(
            "Homologação deve ser representada por um dicionário."
        )

    campos_obrigatorios = (
        "codigo",
        "status",
        "documentos",
        "submissoes",
        "movimentacoes",
    )

    for campo in campos_obrigatorios:
        if campo not in homologacao:
            raise ValueError(
                "Estrutura de Homologação inválida: "
                f"campo ausente: {campo}."
            )

    if not isinstance(
        homologacao["documentos"],
        list,
    ):
        raise TypeError(
            "Documentos da Homologação devem formar uma lista."
        )

    if not isinstance(
        homologacao["movimentacoes"],
        list,
    ):
        raise TypeError(
            "Movimentações da Homologação devem formar uma lista."
        )

    if not isinstance(
        homologacao["submissoes"],
        list,
    ):
        raise TypeError(
            "Submissões da Homologação devem formar uma lista."
        )

def _validar_codigo_inteiro_positivo(
    valor: int,
    nome_campo: str,
) -> None:
    """
    Valida se um código é um número inteiro positivo.

    Valores booleanos são rejeitados explicitamente porque,
    internamente, Python considera bool uma especialização de int.
    """

    if isinstance(valor, bool) or not isinstance(valor, int):
        raise TypeError(
            f"{nome_campo} deve ser um número inteiro."
        )

    if valor <= 0:
        raise ValueError(
            f"{nome_campo} deve ser maior que zero."
        )

def _validar_texto_obrigatorio(
    valor: str,
    nome_campo: str,
) -> str:
    """
    Valida e normaliza um texto obrigatório.

    O método strip() remove espaços externos.

    Exemplo:

        "  João Silva  "

    torna-se:

        "João Silva"
    """

    if not isinstance(valor, str):
        raise TypeError(
            f"{nome_campo} deve ser um texto."
        )

    valor_normalizado = valor.strip()

    if not valor_normalizado:
        raise ValueError(
            f"{nome_campo} é obrigatório."
        )

    return valor_normalizado

def _validar_data_iso(
    valor: str,
    nome_campo: str,
) -> date:
    """
    Valida uma data no formato ISO:

        AAAA-MM-DD

    Exemplo:

        2026-07-29

    Retorna um objeto date, utilizado internamente para cálculos.
    """

    if not isinstance(valor, str):
        raise TypeError(
            f"{nome_campo} deve ser um texto no formato AAAA-MM-DD."
        )

    try:
        return date.fromisoformat(valor)

    except ValueError as erro:
        raise ValueError(
            f"{nome_campo} deve estar no formato AAAA-MM-DD."
        ) from erro

# ============================================================
# REGRAS PRIVADAS DE RESPOSTAS E EXIGÊNCIAS
# ============================================================

def _buscar_exigencia_por_codigo(
    submissoes: list[dict],
    codigo_exigencia: int,
) -> dict | None:
    """
    Busca uma Exigência dentro das Respostas das Submissões.

    Estrutura percorrida:

        Homologação
        └── Submissões
            └── Respostas
                └── Exigências

    A função não utiliza homologacao["exigencias"] porque,
    nesta etapa, a fonte canônica da Exigência permanece sendo
    a Resposta emitida pela concessionária.
    """

    for submissao in submissoes:
        respostas = submissao.get("respostas", [])

        if not isinstance(respostas, list):
            continue

        for resposta in respostas:
            exigencias = resposta.get("exigencias", [])

            if not isinstance(exigencias, list):
                continue

            for exigencia in exigencias:
                if (
                    exigencia.get("codigo")
                    == codigo_exigencia
                ):
                    return exigencia

    return None

def _buscar_resposta_por_codigo_na_submissao(
    submissao: dict,
    codigo_resposta: int,
) -> dict | None:
    """
    Busca uma Resposta pelo código dentro de uma Submissão.

    A função realiza uma busca local na coleção:

        submissao["respostas"]

    Retorna:
        dict:
            Quando encontra a Resposta.

        None:
            Quando a Resposta não existe na Submissão informada.
    """

    respostas = submissao.get(
        "respostas",
        [],
    )

    if not isinstance(respostas, list):
        return None

    for resposta in respostas:
        if not isinstance(resposta, dict):
            continue

        if resposta.get("codigo") == codigo_resposta:
            return resposta

    return None

def _validar_sequencia_resposta_concessionaria(
    submissao: dict,
    resposta: dict,
) -> None:
    """
    Valida código e posição histórica da nova Resposta.

    Regras:

    - o código não pode se repetir dentro da Submissão;
    - o número sequencial não pode se repetir;
    - a primeira Resposta deve possuir sequência 1;
    - as próximas Respostas devem seguir a ordem contínua.
    """

    respostas = submissao["respostas"]

    codigo_resposta = resposta["codigo"]
    numero_sequencial = resposta["numero_sequencial"]

    for resposta_existente in respostas:
        if resposta_existente["codigo"] == codigo_resposta:
            raise ValueError(
                "Já existe uma Resposta com o código informado "
                "nesta Submissão."
            )

        if (
            resposta_existente["numero_sequencial"]
            == numero_sequencial
        ):
            raise ValueError(
                "Já existe uma Resposta com o número sequencial "
                "informado nesta Submissão."
            )

    if not respostas:
        numero_esperado = 1

    else:
        maior_numero = max(
            resposta_existente["numero_sequencial"]
            for resposta_existente in respostas
        )

        numero_esperado = maior_numero + 1

    if numero_sequencial != numero_esperado:
        raise ValueError(
            "O número sequencial da nova Resposta deve ser "
            f"{numero_esperado}."
        )

def _validar_data_resposta_submissao(
    submissao: dict,
    resposta: dict,
) -> None:
    """
    Impede que uma Resposta seja anterior ao envio da Submissão.

    A validação local da Resposta compara:

        data_resposta
        data_registro

    A raiz do agregado acrescenta a comparação com:

        data_envio da Submissão
    """

    data_envio = _validar_data_iso(
        submissao["data_envio"],
        "Data de envio da Submissão",
    )

    data_resposta = _validar_data_iso(
        resposta["data_resposta"],
        "Data da Resposta",
    )

    if data_resposta < data_envio:
        raise ValueError(
            "A data da Resposta não pode ser anterior "
            "à data de envio da Submissão."
        )

def _validar_sequencia_exigencias_resposta(
    resposta: dict,
) -> None:
    """
    Valida a ordem interna das Exigências de uma Resposta.

    A primeira Exigência deve possuir número sequencial 1.

    As demais devem formar uma sequência contínua:

        1, 2, 3, ...
    """

    exigencias = resposta["exigencias"]

    numeros_encontrados = sorted(
        exigencia["numero_sequencial"]
        for exigencia in exigencias
    )

    numeros_esperados = list(
        range(1, len(exigencias) + 1)
    )

    if numeros_encontrados != numeros_esperados:
        raise ValueError(
            "Os números sequenciais das Exigências devem "
            "formar uma sequência contínua iniciada em 1."
        )

def _validar_codigos_exigencias_unicos(
    homologacao: dict,
    resposta: dict,
) -> None:
    """
    Impede a reutilização de códigos de Exigência dentro da
    Homologação.

    O código da Exigência é único no agregado completo, mesmo que
    as Exigências pertençam a Respostas diferentes.
    """

    for exigencia in resposta["exigencias"]:
        exigencia_existente = _buscar_exigencia_por_codigo(
            submissoes=homologacao["submissoes"],
            codigo_exigencia=exigencia["codigo"],
        )

        if exigencia_existente is not None:
            raise ValueError(
                "Já existe uma Exigência com o código informado "
                "nesta Homologação: "
                f"{exigencia['codigo']}."
            )

def _validar_documentos_afetados_exigencias(
    homologacao: dict,
    resposta: dict,
) -> None:
    """
    Verifica se todos os Documentos indicados pelas Exigências
    existem na Homologação.

    Uma Exigência pode não indicar Documento específico.

    Porém, quando indicar um código, esse Documento precisa
    pertencer ao mesmo agregado.
    """

    for exigencia in resposta["exigencias"]:
        for codigo_documento in (
            exigencia["codigos_documentos_afetados"]
        ):
            documento = buscar_documento_por_codigo(
                documentos=homologacao["documentos"],
                codigo=codigo_documento,
            )

            if documento is None:
                raise ValueError(
                    "Documento afetado pela Exigência não "
                    "encontrado na Homologação: "
                    f"código {codigo_documento}."
                )

def _copiar_resposta_concessionaria(
    resposta: dict,
) -> dict:
    """
    Cria uma cópia defensiva de uma Resposta já validada.

    A operação chamadora deve validar previamente a Resposta por:

        validar_resposta_concessionaria()

    A função copia:

    - o dicionário principal da Resposta;
    - a lista de Exigências;
    - cada Exigência por meio de _copiar_exigencia();
    - as listas internas de Documentos afetados.

    Sua única responsabilidade é criar uma estrutura independente
    para inclusão segura no agregado.
    """

    resposta_copiada = resposta.copy()

    resposta_copiada["exigencias"] = [
        _copiar_exigencia(
            exigencia
        )
        for exigencia in resposta["exigencias"]
    ]

    return resposta_copiada

# ============================================================
# CONVERSORES E VALIDADORES DE ESTADOS
# ============================================================

def _converter_status_homologacao(
    status: str | StatusHomologacao,
) -> StatusHomologacao:
    """
    Converte um texto armazenado em JSON para StatusHomologacao.

    Também aceita um StatusHomologacao já convertido.
    """

    if isinstance(status, StatusHomologacao):
        return status

    try:
        return StatusHomologacao(status)

    except ValueError as erro:
        raise ValueError(
            f"Status de Homologação inválido: {status}"
        ) from erro

def _converter_status_operacional_submissao(
    status: str | StatusOperacionalSubmissao,
) -> StatusOperacionalSubmissao:
    """
    Converte texto ou Enum para StatusOperacionalSubmissao.

    A função privada é necessária porque o módulo
    status_submissao.py expõe publicamente as validações,
    mas mantém sua função de conversão como detalhe interno.
    """

    if isinstance(
        status,
        StatusOperacionalSubmissao,
    ):
        return status

    try:
        return StatusOperacionalSubmissao(status)

    except (ValueError, TypeError) as erro:
        raise ValueError(
            "Status operacional de Submissão inválido: "
            f"{status!r}."
        ) from erro

def _converter_canal_envio_submissao(
    canal_envio: str | CanalEnvioSubmissao,
) -> CanalEnvioSubmissao:
    """
    Converte texto ou Enum para CanalEnvioSubmissao.

    O módulo submissoes_homologacao.py possui sua própria conversão
    privada. A raiz do agregado utiliza diretamente o Enum público
    para não depender de detalhes internos de outro módulo.
    """

    if isinstance(
        canal_envio,
        CanalEnvioSubmissao,
    ):
        return canal_envio

    try:
        return CanalEnvioSubmissao(canal_envio)

    except (ValueError, TypeError) as erro:
        raise ValueError(
            "Canal de envio da Submissão inválido: "
            f"{canal_envio!r}."
        ) from erro

def _validar_motivo_status_operacional_submissao(
    novo_status: StatusOperacionalSubmissao,
    motivo: str | None,
) -> str | None:
    """
    Valida o motivo de uma alteração operacional.

    O motivo será obrigatório quando a Submissão for cancelada.

    Para os demais estados, o motivo é opcional.
    """

    if motivo is None:
        motivo_normalizado = None

    elif not isinstance(motivo, str):
        raise TypeError(
            "Motivo da alteração operacional deve ser um texto."
        )

    else:
        motivo_normalizado = motivo.strip() or None

    if (
        novo_status
        == StatusOperacionalSubmissao.CANCELADA
        and motivo_normalizado is None
    ):
        raise ValueError(
            "O cancelamento de uma Submissão exige "
            "uma justificativa."
        )

    return motivo_normalizado

# ============================================================
# REGRAS PRIVADAS DE DOCUMENTOS
# ============================================================

def _validar_estrutura_documento_homologacao(
    documento: dict,
) -> None:
    """
    Valida a estrutura mínima de um Documento da Homologação.

    O documento completo deve ser criado pela função:

        criar_dados_documento_homologacao()

    Esta validação protege a Homologação contra a inclusão de
    dicionários incompletos ou criados manualmente.
    """

    if not isinstance(documento, dict):
        raise TypeError(
            "Documento deve ser representado por um dicionário."
        )

    campos_obrigatorios = (
        "codigo",
        "nome",
        "categoria",
        "data_registro",
        "responsavel_registro",
        "origem",
        "visibilidade",
        "status",
        "obrigatorio",
        "referencia_arquivo",
        "versao",
        "codigo_documento_anterior",
        "codigo_submissao",
        "descricao",
    )

    for campo in campos_obrigatorios:
        if campo not in documento:
            raise ValueError(
                "Estrutura de Documento da Homologação inválida: "
                f"campo ausente: {campo}."
            )

def _validar_motivo_status_documento(
    novo_status: StatusDocumentoHomologacao,
    motivo: str | None,
) -> str | None:
    """
    Valida a justificativa de uma mudança documental.

    O motivo será obrigatório para o estado REJEITADO.
    """

    if motivo is None:
        motivo_normalizado = None

    elif not isinstance(motivo, str):
        raise TypeError(
            "Motivo da alteração documental deve ser um texto."
        )

    else:
        motivo_normalizado = motivo.strip() or None

    if (
        novo_status
        == StatusDocumentoHomologacao.REJEITADO
        and motivo_normalizado is None
    ):
        raise ValueError(
            "A rejeição de um documento exige uma justificativa."
        )

    return motivo_normalizado

def _validar_versionamento_documento(
    documentos: list[dict],
    novo_documento: dict,
) -> dict | None:
    """
    Valida o encadeamento de versões de um documento.

    Retorna:
        None:
            quando o documento é a primeira versão;

        documento anterior:
            quando o novo documento substitui uma versão existente.
    """

    versao = novo_documento["versao"]

    codigo_documento_anterior = novo_documento[
        "codigo_documento_anterior"
    ]

    if versao == 1:
        return None

    documento_anterior = buscar_documento_por_codigo(
        documentos=documentos,
        codigo=codigo_documento_anterior,
    )

    if documento_anterior is None:
        raise ValueError(
            "Documento anterior não encontrado na Homologação."
        )

    versao_anterior = documento_anterior.get("versao")

    if versao != versao_anterior + 1:
        raise ValueError(
            "A versão do novo documento deve ser exatamente "
            "uma unidade superior à versão anterior."
        )

    if (
        novo_documento["nome"]
        != documento_anterior.get("nome")
    ):
        raise ValueError(
            "Uma nova versão deve manter o mesmo nome "
            "do documento anterior."
        )

    if (
        novo_documento["categoria"]
        != documento_anterior.get("categoria")
    ):
        raise ValueError(
            "Uma nova versão deve manter a mesma categoria "
            "do documento anterior."
        )

    if (
        documento_anterior.get("status")
        == StatusDocumentoHomologacao.SUBSTITUIDO.value
    ):
        raise ValueError(
            "O documento anterior já foi substituído."
        )

    status_documento_anterior = (
        converter_status_documento(
            documento_anterior["status"]
        )
    )

    status_permitidos_para_substituicao = {
        StatusDocumentoHomologacao.VALIDADO,
        StatusDocumentoHomologacao.REJEITADO,
    }

    if (
        status_documento_anterior
        not in status_permitidos_para_substituicao
    ):
        raise ValueError(
            "Somente documentos validados ou rejeitados "
            "podem ser substituídos por uma nova versão."
        )

    return documento_anterior

# ============================================================
# AUXILIARES DO ESTADO GERAL DA HOMOLOGAÇÃO
# ============================================================

def _validar_homologacao_nao_terminal(
    homologacao: dict,
    mensagem_erro: str,
) -> StatusHomologacao:
    """
    Impede uma operação quando a Homologação está em estado
    terminal.

    A estrutura mínima da Homologação deve ter sido validada
    anteriormente pela operação chamadora.

    Parâmetros:
        homologacao:
            Homologação cuja situação será verificada.

        mensagem_erro:
            Mensagem específica da operação que será apresentada
            quando a Homologação estiver em estado terminal.

    Retorno:
        O StatusHomologacao convertido e validado.

    Exceções:
        ValueError:
            quando a Homologação está em estado terminal.

    Estados terminais atuais:

        CONCLUIDA
        REJEITADA
        CANCELADA
    """

    status_homologacao = _converter_status_homologacao(
        homologacao["status"]
    )

    if status_homologacao_e_terminal(
        status_homologacao
    ):
        raise ValueError(
            mensagem_erro
        )

    return status_homologacao

def _preparar_operacoes_campo_candidatas(
    homologacao: dict,
) -> dict:
    """
    Cria uma estrutura candidata das Operações de Campo.

    Quando a Homologação for um registro antigo e ainda não
    possuir operacoes_campo, uma nova estrutura é preparada.

    A estrutura real da Homologação não é modificada.
    """

    operacoes_atuais = homologacao.get(
        "operacoes_campo"
    )

    if operacoes_atuais is None:
        return criar_dados_operacoes_campo()

    validar_operacoes_campo(
        operacoes_atuais
    )

    instalacao_atual = operacoes_atuais[
        "instalacao"
    ]

    ligacao_atual = operacoes_atuais[
        "ligacao"
    ]

    return {
        "instalacao": (
            instalacao_atual.copy()
            if isinstance(
                instalacao_atual,
                dict,
            )
            else None
        ),
        "vistorias": list(
            operacoes_atuais["vistorias"]
        ),
        "ligacao": (
            ligacao_atual.copy()
            if isinstance(
                ligacao_atual,
                dict,
            )
            else None
        ),
    }

def _criar_descricao_transicao(
    status_anterior: StatusHomologacao,
    novo_status: StatusHomologacao,
) -> str:
    """
    Cria uma descrição técnica e legível para o histórico.

    Os identificadores internos são utilizados nesta primeira versão.

    Futuramente, os rótulos amigáveis poderão ser aplicados na
    apresentação da linha do tempo.
    """

    return (
        "Status da Homologação alterado de "
        f"{status_anterior.value} para {novo_status.value}."
    )

def _validar_motivo_transicao(
    novo_status: StatusHomologacao,
    motivo: str | None,
) -> str | None:
    """
    Valida o motivo associado à mudança de estado.

    Nesta primeira implementação, o motivo será obrigatório para:

    - CANCELADA;
    - REJEITADA.

    Para os demais estados, ele será opcional.
    """

    estados_com_motivo_obrigatorio = {
        StatusHomologacao.CANCELADA,
        StatusHomologacao.REJEITADA,
    }

    if motivo is None:
        motivo_normalizado = None

    elif not isinstance(motivo, str):
        raise TypeError(
            "Motivo da transição deve ser um texto."
        )

    else:
        motivo_normalizado = motivo.strip() or None

    if (
        novo_status in estados_com_motivo_obrigatorio
        and motivo_normalizado is None
    ):
        raise ValueError(
            "A transição para "
            f"{novo_status.value} exige uma justificativa."
        )

    return motivo_normalizado

# ============================================================
# CRIAÇÃO DA HOMOLOGAÇÃO
# ============================================================

def _calcular_data_prevista_conclusao(
    data_abertura: date,
    prazo_estimado_dias: int,
) -> date:
    """
    Calcula a previsão inicial de conclusão da Homologação.

    Nesta primeira versão, o cálculo utiliza dias corridos.

    Futuramente, o domínio poderá evoluir para considerar:

    - dias úteis;
    - feriados;
    - regras da concessionária;
    - suspensão de prazos;
    - períodos de responsabilidade do cliente;
    - pausas causadas por exigências.
    """

    return data_abertura + timedelta(
        days=prazo_estimado_dias
    )

def criar_dados_homologacao(
    codigo: int,
    codigo_empresa: int,
    codigo_projeto: int,
    codigo_concessionaria: int,
    data_abertura: str,
    responsavel_abertura: str,
    prazo_estimado_dias: int = 45,
    observacoes: str = "",
) -> dict:
    """
    Cria a estrutura inicial de uma Homologação.

    Parâmetros:
        codigo:
            Código interno da Homologação.

        codigo_empresa:
            Empresa proprietária do processo.

        codigo_projeto:
            Projeto ao qual a Homologação pertence.

        codigo_concessionaria:
            Concessionária responsável pela análise.

        data_abertura:
            Data no formato AAAA-MM-DD.

        responsavel_abertura:
            Usuário ou funcionário que iniciou o processo.

        prazo_estimado_dias:
            Estimativa inicial do ciclo completo.

            O valor padrão será 45 dias, mas ele não representa uma
            regra universal.

        observacoes:
            Informações adicionais sobre a abertura.

    Retorno:
        Dicionário contendo a estrutura inicial da Homologação.
    """

    _validar_codigo_inteiro_positivo(
        codigo,
        "Código da Homologação",
    )

    _validar_codigo_inteiro_positivo(
        codigo_empresa,
        "Código da Empresa",
    )

    _validar_codigo_inteiro_positivo(
        codigo_projeto,
        "Código do Projeto",
    )

    _validar_codigo_inteiro_positivo(
        codigo_concessionaria,
        "Código da Concessionária",
    )

    data_abertura_convertida = _validar_data_iso(
        data_abertura,
        "Data de abertura",
    )

    responsavel_normalizado = _validar_texto_obrigatorio(
        responsavel_abertura,
        "Responsável pela abertura",
    )

    if not isinstance(prazo_estimado_dias, int):
        raise TypeError(
            "Prazo estimado deve ser um número inteiro."
        )

    if prazo_estimado_dias <= 0:
        raise ValueError(
            "Prazo estimado deve ser maior que zero."
        )

    if not isinstance(observacoes, str):
        raise TypeError(
            "Observações devem ser um texto."
        )

    data_prevista = _calcular_data_prevista_conclusao(
        data_abertura_convertida,
        prazo_estimado_dias,
    )

    movimentacao_inicial = criar_movimentacao_de_abertura(
        data_abertura=data_abertura,
        responsavel_abertura=responsavel_normalizado,
    )

    operacoes_campo = (
        criar_dados_operacoes_campo()
    )

    validar_operacoes_campo(
        operacoes_campo
    )

    return {
        "codigo": codigo,
        "codigo_empresa": codigo_empresa,
        "codigo_projeto": codigo_projeto,
        "codigo_concessionaria": codigo_concessionaria,
        "status": STATUS_INICIAL_HOMOLOGACAO.value,
        "data_abertura": data_abertura,
        "data_prevista_conclusao": data_prevista.isoformat(),
        "prazo_estimado_dias": prazo_estimado_dias,
        "data_conclusao_real": None,
        "responsavel_abertura": responsavel_normalizado,
        "responsavel_atual": responsavel_normalizado,
        "documentos": [],
        "submissoes": [],
        "protocolos": [],
        "exigencias": [],
        "pendencias": [],
        "prazos": [],
        "operacoes_campo": operacoes_campo,
        "movimentacoes": [
            movimentacao_inicial
        ],
        "observacoes": observacoes.strip(),
    }

# ============================================================
# CONSULTAS DA HOMOLOGAÇÃO
# ============================================================

def buscar_homologacao_por_codigo(
    homologacoes: list[dict],
    codigo: int,
    codigo_empresa: int | None = None,
) -> dict | None:
    """
    Busca uma Homologação por seu código interno.

    Quando codigo_empresa for informado, a busca também aplicará
    o isolamento entre empresas.

    Retorna:
        dicionário da Homologação encontrada;

        None, quando não existir correspondência.
    """

    for homologacao in homologacoes:
        codigo_corresponde = (
            homologacao.get("codigo") == codigo
        )

        empresa_corresponde = (
            codigo_empresa is None
            or homologacao.get("codigo_empresa") == codigo_empresa
        )

        if codigo_corresponde and empresa_corresponde:
            return homologacao

    return None

def buscar_homologacoes_por_concessionaria(
    homologacoes: list[dict],
    codigo_concessionaria: int,
    codigo_empresa: int | None = None,
) -> list[dict]:
    """
    Retorna as Homologações vinculadas
    à Concessionária informada.

    Quando codigo_empresa for fornecido, a consulta
    também respeita o isolamento entre Empresas.

    A função retorna uma nova lista e não altera
    a coleção recebida.
    """

    return [
        homologacao
        for homologacao in homologacoes
        if (
            homologacao.get("codigo_concessionaria")
            == codigo_concessionaria
            and (
                codigo_empresa is None
                or homologacao.get("codigo_empresa")
                == codigo_empresa
            )
        )
    ]

def codigo_homologacao_existe(
    homologacoes: list[dict],
    codigo: int,
    codigo_empresa: int | None = None,
) -> bool:
    """
    Verifica se um código de Homologação já existe.

    A função reutiliza a busca para evitar duplicação de lógica.
    """

    return buscar_homologacao_por_codigo(
        homologacoes=homologacoes,
        codigo=codigo,
        codigo_empresa=codigo_empresa,
    ) is not None

def quantidade_homologacoes_por_status(
    homologacoes: list[dict],
    status: str | StatusHomologacao,
) -> int:
    """
    Conta as Homologações que possuem o status informado.

    Aceita o Enum StatusHomologacao ou seu valor textual.
    """

    status_convertido = _converter_status_homologacao(
        status
    )

    return sum(
        1
        for homologacao in homologacoes
        if homologacao.get("status")
        == status_convertido.value
    )

def buscar_homologacoes_por_status(
    homologacoes: list[dict],
    status: str | StatusHomologacao,
    codigo_empresa: int | None = None,
) -> list[dict]:
    """
    Retorna as Homologações que possuem
    o status informado.

    Aceita o Enum StatusHomologacao ou seu valor textual.

    Quando codigo_empresa for informado, a consulta
    também respeita o isolamento entre Empresas.

    A função retorna uma nova lista e não altera
    a coleção recebida.
    """

    status_convertido = _converter_status_homologacao(
        status
    )

    return [
        homologacao
        for homologacao in homologacoes
        if (
            homologacao.get("status")
            == status_convertido.value
            and (
                codigo_empresa is None
                or homologacao.get("codigo_empresa")
                == codigo_empresa
            )
        )
    ]

def _iterar_exigencias_homologacao(
    homologacao: dict,
):
    """
    Percorre as Exigências armazenadas nas Respostas
    das Submissões da Homologação.

    A função não utiliza homologacao["exigencias"],
    pois essa lista não é a fonte canônica.
    """

    for submissao in homologacao.get(
        "submissoes",
        [],
    ):
        for resposta in submissao.get(
            "respostas",
            [],
        ):
            for exigencia in resposta.get(
                "exigencias",
                [],
            ):
                yield exigencia

def homologacao_possui_exigencia_aberta(
    homologacao: dict,
) -> bool:
    """
    Informa se a Homologação possui ao menos
    uma Exigência pendente de atendimento.
    """

    return any(
        exigencia.get("status_atendimento")
        == "PENDENTE"
        for exigencia in (
            _iterar_exigencias_homologacao(
                homologacao
            )
        )
    )

def quantidade_homologacoes_com_exigencia_aberta(
    homologacoes: list[dict],
) -> int:
    """
    Conta quantas Homologações possuem ao menos
    uma Exigência aberta.
    """

    return sum(
        1
        for homologacao in homologacoes
        if homologacao_possui_exigencia_aberta(
            homologacao
        )
    )

def homologacao_possui_submissao_aguardando_envio(
    homologacao: dict,
) -> bool:
    """
    Informa se existe uma Submissão pronta para envio.
    """

    return any(
        submissao.get("status_operacional")
        == StatusOperacionalSubmissao.PRONTA_PARA_ENVIO.value
        for submissao in homologacao.get(
            "submissoes",
            [],
        )
    )

def quantidade_homologacoes_aguardando_envio(
    homologacoes: list[dict],
) -> int:
    """
    Conta Homologações com ao menos uma Submissão
    pronta para envio.
    """

    return sum(
        1
        for homologacao in homologacoes
        if (
            homologacao
            .get("status")
            not in {
                StatusHomologacao.CONCLUIDA.value,
                StatusHomologacao.REJEITADA.value,
                StatusHomologacao.CANCELADA.value,
            }
            and homologacao_possui_submissao_aguardando_envio(
                homologacao
            )
        )
    )

def homologacao_possui_submissao_aguardando_resposta(
    homologacao: dict,
) -> bool:
    """
    Informa se existe uma Submissão já enviada
    ou protocolada que ainda não recebeu resposta.
    """

    estados_enviados = {
        StatusOperacionalSubmissao.ENVIADA.value,
        StatusOperacionalSubmissao.PROTOCOLADA.value,
    }

    return any(
        (
            submissao.get("status_operacional")
            in estados_enviados
            and submissao.get("status_analise")
            == StatusAnaliseSubmissao.SEM_RESPOSTA.value
        )
        for submissao in homologacao.get(
            "submissoes",
            [],
        )
    )

def quantidade_homologacoes_aguardando_resposta(
    homologacoes: list[dict],
) -> int:
    """
    Conta Homologações com ao menos uma Submissão
    enviada que permanece sem resposta.
    """

    return sum(
        1
        for homologacao in homologacoes
        if (
            homologacao
            .get("status")
            not in {
                StatusHomologacao.CONCLUIDA.value,
                StatusHomologacao.REJEITADA.value,
                StatusHomologacao.CANCELADA.value,
            }
            and homologacao_possui_submissao_aguardando_resposta(
                homologacao
            )
        )
    )

def homologacao_esta_sem_responsavel(
    homologacao: dict,
) -> bool:
    """
    Informa se a Homologação não possui responsável atual.
    """

    responsavel = homologacao.get(
        "responsavel_atual"
    )

    return (
        responsavel is None
        or (
            isinstance(responsavel, str)
            and not responsavel.strip()
        )
    )

def quantidade_homologacoes_sem_responsavel(
    homologacoes: list[dict],
) -> int:
    """
    Conta Homologações sem responsável atual definido.
    """

    return sum(
        1
        for homologacao in homologacoes
        if (
            homologacao
            .get("status")
            not in {
                StatusHomologacao.CONCLUIDA.value,
                StatusHomologacao.REJEITADA.value,
                StatusHomologacao.CANCELADA.value,
            }
            and homologacao_esta_sem_responsavel(
                homologacao
            )
        )
    )

def quantidade_total_pendencias_homologacao(
    homologacoes: list[dict],
) -> int:
    """
    Retorna a soma dos indicadores de pendência.

    Uma mesma Homologação pode contribuir para mais de uma
    categoria quando possuir pendências diferentes.
    """

    aguardando_documentacao = (
        quantidade_homologacoes_por_status(
            homologacoes,
            StatusHomologacao.AGUARDANDO_DOCUMENTACAO,
        )
    )

    com_exigencia = (
        quantidade_homologacoes_com_exigencia_aberta(
            homologacoes
        )
    )

    aguardando_envio = (
        quantidade_homologacoes_aguardando_envio(
            homologacoes
        )
    )

    aguardando_resposta = (
        quantidade_homologacoes_aguardando_resposta(
            homologacoes
        )
    )

    sem_responsavel = (
        quantidade_homologacoes_sem_responsavel(
            homologacoes
        )
    )

    return (
        aguardando_documentacao
        + com_exigencia
        + aguardando_envio
        + aguardando_resposta
        + sem_responsavel
    )

def buscar_homologacao_ativa_por_projeto(
    homologacoes: list[dict],
    codigo_projeto: int,
    codigo_empresa: int,
) -> dict | None:
    """
    Localiza a Homologação ativa de determinado Projeto.

    Uma Homologação é considerada ativa quando seu estado não é:

    - CONCLUIDA;
    - REJEITADA;
    - CANCELADA.
    """

    for homologacao in homologacoes:
        pertence_ao_projeto = (
            homologacao.get("codigo_projeto")
            == codigo_projeto
        )

        pertence_a_empresa = (
            homologacao.get("codigo_empresa")
            == codigo_empresa
        )

        if not (
            pertence_ao_projeto
            and pertence_a_empresa
        ):
            continue

        status = _converter_status_homologacao(
            homologacao.get("status")
        )

        if not status_homologacao_e_terminal(status):
            return homologacao

    return None

def projeto_possui_homologacao_ativa(
    homologacoes: list[dict],
    codigo_projeto: int,
    codigo_empresa: int,
) -> bool:
    """
    Verifica a regra:

        um Projeto não pode possuir mais de uma
        Homologação ativa ao mesmo tempo.
    """

    return buscar_homologacao_ativa_por_projeto(
        homologacoes=homologacoes,
        codigo_projeto=codigo_projeto,
        codigo_empresa=codigo_empresa,
    ) is not None

# ============================================================
# ESTADO E EVENTOS DA HOMOLOGAÇÃO
# ============================================================

def alterar_status_homologacao(
    homologacao: dict,
    novo_status: str | StatusHomologacao,
    data_movimentacao: str,
    responsavel: str,
    motivo: str | None = None,
    descricao: str | None = None,
) -> dict:
    """
    Altera o status de uma Homologação com segurança.

    A função:

    1. valida a estrutura recebida;
    2. converte o status atual;
    3. converte o novo status;
    4. impede transições inválidas;
    5. valida data, responsável e motivo;
    6. atualiza o status;
    7. atualiza o responsável atual;
    8. registra a conclusão, quando aplicável;
    9. adiciona uma Movimentação ao histórico.

    Parâmetros:
        homologacao:
            Entidade que terá seu status alterado.

        novo_status:
            Novo estado desejado.

            Pode ser informado como Enum:

                StatusHomologacao.EM_ANALISE

            ou texto:

                "EM_ANALISE"

        data_movimentacao:
            Data da alteração no formato AAAA-MM-DD.

        responsavel:
            Usuário ou funcionário responsável pela alteração.

        motivo:
            Justificativa opcional.

            Será obrigatória para cancelamento e rejeição.

        descricao:
            Descrição personalizada para o histórico.

            Caso não seja informada, o domínio criará uma descrição
            automaticamente.

    Retorno:
        O próprio dicionário da Homologação, já atualizado.
    """

    if not isinstance(homologacao, dict):
        raise TypeError(
            "Homologação deve ser representada por um dicionário."
        )

    if "status" not in homologacao:
        raise ValueError(
            "Homologação não possui um status registrado."
        )

    status_atual = _converter_status_homologacao(
        homologacao["status"]
    )

    novo_status_convertido = _converter_status_homologacao(
        novo_status
    )

    if status_atual == novo_status_convertido:
        raise ValueError(
            "O novo status deve ser diferente do status atual."
        )

    if status_homologacao_e_terminal(status_atual):
        raise ValueError(
            "Não é possível alterar uma Homologação que está "
            f"no estado terminal {status_atual.value}."
        )

    if not transicao_status_homologacao_e_valida(
        status_atual,
        novo_status_convertido,
    ):
        raise ValueError(
            "Transição de status da Homologação não permitida: "
            f"{status_atual.value} -> "
            f"{novo_status_convertido.value}."
        )

    data_validada = _validar_data_iso(
        data_movimentacao,
        "Data da movimentação",
    )

    responsavel_normalizado = _validar_texto_obrigatorio(
        responsavel,
        "Responsável pela movimentação",
    )

    motivo_normalizado = _validar_motivo_transicao(
        novo_status_convertido,
        motivo,
    )

    if descricao is None:
        descricao_normalizada = _criar_descricao_transicao(
            status_anterior=status_atual,
            novo_status=novo_status_convertido,
        )

    else:
        descricao_normalizada = _validar_texto_obrigatorio(
            descricao,
            "Descrição da movimentação",
        )

    movimentacoes = homologacao.setdefault(
        "movimentacoes",
        [],
    )

    movimentacao = criar_movimentacao_de_status(
        movimentacoes=movimentacoes,
        status_anterior=status_atual,
        novo_status=novo_status_convertido,
        data_movimentacao=data_validada.isoformat(),
        responsavel=responsavel_normalizado,
        descricao=descricao_normalizada,
        motivo=motivo_normalizado,
    )

    homologacao["status"] = novo_status_convertido.value
    homologacao["responsavel_atual"] = responsavel_normalizado

    movimentacoes.append(movimentacao)

    if novo_status_convertido == StatusHomologacao.CONCLUIDA:
        homologacao["data_conclusao_real"] = (
            data_validada.isoformat()
        )

    return homologacao

def aplicar_evento_homologacao(
    homologacao: dict,
    evento: str | EventoHomologacao,
    data_movimentacao: str,
    responsavel: str,
    motivo: str | None = None,
    descricao: str | None = None,
) -> dict:
    """
    Aplica um Evento de negócio ao estado geral da Homologação.

    A função:

    1. valida a estrutura da Homologação;
    2. converte e valida o estado atual;
    3. valida o Evento no estado atual;
    4. determina o Status resultante;
    5. delega a alteração para alterar_status_homologacao();
    6. preserva o histórico completo da transição.

    Esta operação não interpreta Documentos, Submissões ou
    Respostas. Ela recebe um Evento já determinado pela operação
    de negócio responsável.
    """

    _validar_estrutura_homologacao(
        homologacao
    )

    status_atual = _converter_status_homologacao(
        homologacao["status"]
    )

    novo_status = validar_evento_no_estado_homologacao(
        status_atual=status_atual,
        evento=evento,
    )

    if isinstance(evento, EventoHomologacao):
        evento_convertido = evento

    else:
        try:
            evento_convertido = EventoHomologacao(
                evento
            )

        except (ValueError, TypeError) as erro:
            raise ValueError(
                "Evento da Homologação inválido: "
                f"{evento!r}."
            ) from erro

    if descricao is None:
        descricao_normalizada = (
            "Evento de negócio aplicado à Homologação: "
            f"{evento_convertido.value}."
        )

    else:
        descricao_normalizada = (
            _validar_texto_obrigatorio(
                descricao,
                "Descrição do Evento",
            )
        )

    return alterar_status_homologacao(
        homologacao=homologacao,
        novo_status=novo_status,
        data_movimentacao=data_movimentacao,
        responsavel=responsavel,
        motivo=motivo,
        descricao=descricao_normalizada,
    )

# ============================================================
# PREPARAÇÃO ATÔMICA DO AGREGADO
# ============================================================

def _copiar_exigencia(
    exigencia: dict,
) -> dict:
    """
    Cria uma cópia defensiva de uma Exigência.

    A função copia:

    - o dicionário principal;
    - a lista de códigos dos Documentos afetados.

    Os demais campos atuais da Exigência são valores escalares:

    - códigos;
    - textos;
    - status;
    - datas;
    - referências opcionais.

    Retorno:
        Uma nova estrutura de Exigência que pode ser modificada
        e validada sem alterar a Exigência real pertencente ao
        agregado.
    """

    exigencia_copiada = exigencia.copy()

    exigencia_copiada[
        "codigos_documentos_afetados"
    ] = list(
        exigencia["codigos_documentos_afetados"]
    )

    return exigencia_copiada

def _copiar_submissao(
    submissao: dict,
) -> dict:
    """
    Cria uma cópia defensiva de uma Submissão já validada.

    Esta função assume que a Submissão foi obtida por uma operação
    interna do agregado, como:

        _obter_submissao_obrigatoria()

    Por isso ela não executa novamente a validação estrutural.

    Sua única responsabilidade é criar estruturas mutáveis
    independentes para permitir alterações candidatas sem modificar
    a Submissão pertencente ao agregado.
    """

    submissao_copiada = submissao.copy()

    submissao_copiada["pacote_documental"] = [
        referencia.copy()
        for referencia in submissao["pacote_documental"]
    ]

    submissao_copiada[
        "codigos_exigencias_relacionadas"
    ] = list(
        submissao["codigos_exigencias_relacionadas"]
    )

    submissao_copiada["respostas"] = list(
        submissao["respostas"]
    )

    return submissao_copiada

def _copiar_homologacao(
    homologacao: dict,
    movimentacoes_adicionais: list[dict] | None = None,
) -> dict:
    """
    Cria uma cópia candidata de uma Homologação já validada.

    Esta função assume que a estrutura mínima da Homologação foi
    validada previamente por:

        _validar_estrutura_homologacao()

    Sua única responsabilidade é criar uma estrutura candidata
    apropriada para a preparação de mudanças no estado geral.

    A função copia:

    - o dicionário principal da Homologação;
    - a lista de Movimentações;
    - as Movimentações adicionais que devem preceder a futura
      alteração de estado.

    As coleções de Documentos e Submissões permanecem
    compartilhadas intencionalmente, pois a preparação de Eventos
    apenas consulta essas estruturas.

    Esta função não deve ser utilizada para preparar alterações em:

    - Documentos;
    - Submissões;
    - Respostas;
    - Exigências.

    Para essas estruturas, devem ser utilizados os helpers
    específicos de cópia defensiva.
    """

    if movimentacoes_adicionais is None:
        movimentacoes_adicionais = []

    if not isinstance(
        movimentacoes_adicionais,
        list,
    ):
        raise TypeError(
            "Movimentações adicionais devem formar uma lista."
        )

    homologacao_copiada = homologacao.copy()

    homologacao_copiada["movimentacoes"] = [
        *homologacao["movimentacoes"],
        *movimentacoes_adicionais,
    ]

    return homologacao_copiada

def _preparar_evento_homologacao(
    homologacao: dict,
    evento: str | EventoHomologacao,
    data_movimentacao: str,
    responsavel: str,
    descricao: str,
    motivo: str | None = None,
    movimentacoes_precedentes: list[dict] | None = None,
) -> tuple[str, str, dict]:
    """
    Prepara a aplicação de um Evento sem alterar a Homologação real.

    A função:

    1. valida a estrutura mínima da Homologação;
    2. cria uma cópia candidata da raiz do agregado;
    3. acrescenta as Movimentações precedentes;
    4. aplica o Evento apenas na candidata;
    5. retorna os dados necessários para a aplicação definitiva.

    Nenhuma estrutura real do agregado é modificada por esta função.
    """

    _validar_estrutura_homologacao(
        homologacao
    )

    homologacao_candidata = _copiar_homologacao(
        homologacao=homologacao,
        movimentacoes_adicionais=movimentacoes_precedentes,
    )

    aplicar_evento_homologacao(
        homologacao=homologacao_candidata,
        evento=evento,
        data_movimentacao=data_movimentacao,
        responsavel=responsavel,
        motivo=motivo,
        descricao=descricao,
    )

    movimentacao_evento = (
        homologacao_candidata["movimentacoes"][-1]
    )

    return (
        homologacao_candidata["status"],
        homologacao_candidata["responsavel_atual"],
        movimentacao_evento,
    )

def _preparar_atendimentos_exigencias_submissao(
    homologacao: dict,
    submissao: dict,
    data_atendimento: str,
    responsavel_atendimento: str,
) -> list[tuple[dict, dict]]:
    """
    Prepara o atendimento das Exigências relacionadas à Submissão.

    A função não altera imediatamente as Exigências reais.

    Para cada Exigência relacionada:

    1. localiza a Exigência no agregado;
    2. valida sua estrutura atual;
    3. valida a transição PENDENTE -> ATENDIDA;
    4. cria uma cópia defensiva;
    5. preenche os dados do atendimento;
    6. valida integralmente a candidata.

    Retorna pares contendo:

        Exigência real
        Exigência candidata

    Assim, todas as Exigências são validadas antes de qualquer
    alteração no agregado.

    Nenhuma Exigência real é modificada por esta função.
    As alterações somente serão aplicadas pela operação pública
    depois que todas as validações do agregado forem concluídas.
    """

    atendimentos_preparados = []

    codigos_exigencias = submissao[
        "codigos_exigencias_relacionadas"
    ]

    for codigo_exigencia in codigos_exigencias:
        exigencia = _buscar_exigencia_por_codigo(
            submissoes=homologacao["submissoes"],
            codigo_exigencia=codigo_exigencia,
        )

        if exigencia is None:
            raise ValueError(
                "Exigência relacionada não encontrada "
                "na Homologação: "
                f"código {codigo_exigencia}."
            )

        validar_exigencia(
            exigencia
        )

        validar_transicao_status_exigencia(
            status_atual=exigencia["status_atendimento"],
            novo_status=(
                StatusAtendimentoExigencia.ATENDIDA
            ),
        )

        exigencia_candidata = _copiar_exigencia(
            exigencia
        )

        exigencia_candidata["status_atendimento"] = (
            StatusAtendimentoExigencia.ATENDIDA.value
        )

        exigencia_candidata[
            "codigo_submissao_atendimento"
        ] = submissao["codigo"]

        exigencia_candidata["data_atendimento"] = (
            data_atendimento
        )

        exigencia_candidata[
            "responsavel_atendimento"
        ] = responsavel_atendimento

        exigencia_candidata[
            "observacoes_atendimento"
        ] = (
            "Exigência atendida pelo envio da Submissão "
            f"nº {submissao['numero_sequencial']}."
        )

        validar_exigencia(
            exigencia_candidata
        )

        atendimentos_preparados.append(
            (
                exigencia,
                exigencia_candidata,
            )
        )

    return atendimentos_preparados

# ============================================================
# OPERAÇÕES DE DOCUMENTOS
# ============================================================

def adicionar_documento_homologacao(
    homologacao: dict,
    documento: dict,
    data_movimentacao: str,
    responsavel: str,
) -> dict:
    """
    Adiciona um Documento à Homologação com segurança.

    A função:

    1. valida a estrutura da Homologação;
    2. valida a estrutura do documento;
    3. impede códigos duplicados;
    4. valida o encadeamento de versões;
    5. marca a versão anterior como substituída;
    6. adiciona o novo documento;
    7. registra uma Movimentação no histórico.

    Parâmetros:
        homologacao:
            Homologação que receberá o documento.

        documento:
            Documento criado por:

                criar_dados_documento_homologacao()

        data_movimentacao:
            Data da inclusão no formato AAAA-MM-DD.

        responsavel:
            Usuário responsável pela operação.

    Retorno:
        O próprio dicionário da Homologação atualizado.
    """

    _validar_estrutura_homologacao(
        homologacao
    )

    _validar_estrutura_documento_homologacao(
        documento
    )

    _validar_homologacao_nao_terminal(
        homologacao=homologacao,
        mensagem_erro=(
            "Não é possível adicionar documentos a uma "
            "Homologação em estado terminal."
        ),
    )

    data_normalizada = _validar_data_iso(
        data_movimentacao,
        "Data da movimentação",
    ).isoformat()

    responsavel_normalizado = _validar_texto_obrigatorio(
        responsavel,
        "Responsável pela movimentação",
    )

    documentos = homologacao["documentos"]

    documento_existente = buscar_documento_por_codigo(
        documentos=documentos,
        codigo=documento["codigo"],
    )

    if documento_existente is not None:
        raise ValueError(
            "Já existe um documento com o código informado "
            "nesta Homologação."
        )

    documento_anterior = (
        _validar_versionamento_documento(
            documentos=documentos,
            novo_documento=documento,
        )
    )

    movimentacao = (
        criar_movimentacao_documento_adicionado(
            movimentacoes=homologacao["movimentacoes"],
            documento=documento,
            data_movimentacao=data_normalizada,
            responsavel=responsavel_normalizado,
        )
    )

    if documento_anterior is not None:
        documento_anterior["status"] = (
            StatusDocumentoHomologacao.SUBSTITUIDO.value
        )
   
    documentos.append(documento)

    homologacao["movimentacoes"].append(
        movimentacao
    )

    return homologacao

def alterar_status_documento_homologacao(
    homologacao: dict,
    codigo_documento: int,
    novo_status: str | StatusDocumentoHomologacao,
    data_movimentacao: str,
    responsavel: str,
    motivo: str | None = None,
    referencia_arquivo: str | None = None,
) -> dict:
    """
    Altera o status de um Documento pertencente à Homologação.

    A função:

    1. valida a Homologação;
    2. impede alterações em Homologações terminais;
    3. localiza o documento;
    4. converte os estados;
    5. valida a transição;
    6. valida data, responsável e motivo;
    7. registra o arquivo quando o documento é recebido;
    8. altera o status documental;
    9. registra uma Movimentação.

    Nenhuma alteração é aplicada ao Documento ou à Homologação antes
    da conclusão de todas as validações.

    Parâmetros:
        homologacao:
            Homologação proprietária do documento.

        codigo_documento:
            Código interno do documento.

        novo_status:
            Novo estado desejado.

        data_movimentacao:
            Data da operação no formato AAAA-MM-DD.

        responsavel:
            Responsável pela alteração.

        motivo:
            Justificativa da mudança.

            Obrigatória quando o documento for rejeitado.

        referencia_arquivo:
            Referência do arquivo recebido.

            Obrigatória na transição:

                SOLICITADO → RECEBIDO

    Retorno:
        O próprio dicionário da Homologação atualizado.
    """

    _validar_estrutura_homologacao(
        homologacao
    )

    _validar_codigo_inteiro_positivo(
        codigo_documento,
        "Código do Documento",
    )

    _validar_homologacao_nao_terminal(
        homologacao=homologacao,
        mensagem_erro=(
            "Não é possível alterar documentos de uma "
            "Homologação em estado terminal."
        ),
    )

    documento = buscar_documento_por_codigo(
        documentos=homologacao["documentos"],
        codigo=codigo_documento,
    )

    if documento is None:
        raise ValueError(
            "Documento não encontrado na Homologação."
        )

    status_atual = converter_status_documento(
        documento["status"]
    )

    novo_status_convertido = converter_status_documento(
        novo_status
    )

    if status_atual == novo_status_convertido:
        raise ValueError(
            "O novo status do documento deve ser diferente "
            "do status atual."
        )

    if not transicao_status_documento_e_valida(
        status_atual,
        novo_status_convertido,
    ):
        raise ValueError(
            "Transição de status do documento não permitida: "
            f"{status_atual.value} -> "
            f"{novo_status_convertido.value}."
        )

    data_normalizada = _validar_data_iso(
        data_movimentacao,
        "Data da movimentação",
    ).isoformat()

    responsavel_normalizado = _validar_texto_obrigatorio(
        responsavel,
        "Responsável pela movimentação",
    )

    motivo_normalizado = (
        _validar_motivo_status_documento(
            novo_status=novo_status_convertido,
            motivo=motivo,
        )
    )

    if referencia_arquivo is None:
        referencia_normalizada = None

    else:
        referencia_normalizada = (
            _validar_texto_obrigatorio(
                referencia_arquivo,
                "Referência do arquivo",
            )
        )

    recebendo_documento_solicitado = (
        status_atual
        == StatusDocumentoHomologacao.SOLICITADO
        and novo_status_convertido
        == StatusDocumentoHomologacao.RECEBIDO
    )

    if (
        recebendo_documento_solicitado
        and referencia_normalizada is None
    ):
        raise ValueError(
            "O recebimento do documento exige uma "
            "referência de arquivo."
        )

    if (
        not recebendo_documento_solicitado
        and referencia_normalizada is not None
    ):
        raise ValueError(
            "A referência do arquivo somente deve ser informada "
            "na transição de SOLICITADO para RECEBIDO."
        )

    movimentacao = (
        criar_movimentacao_status_documento(
            movimentacoes=homologacao["movimentacoes"],
            documento=documento,
            status_anterior=status_atual,
            novo_status=novo_status_convertido,
            data_movimentacao=data_normalizada,
            responsavel=responsavel_normalizado,
            motivo=motivo_normalizado,
        )
    )

    if recebendo_documento_solicitado:
        documento["referencia_arquivo"] = (
            referencia_normalizada
        )

    documento["status"] = novo_status_convertido.value

    homologacao["movimentacoes"].append(
        movimentacao
    )

    return homologacao

# ============================================================
# CONSULTAS DE SUBMISSÕES
# ============================================================

def buscar_submissao_por_codigo(
    submissoes: list[dict],
    codigo: int,
) -> dict | None:
    """
    Busca uma Submissão pelo código dentro de uma coleção.

    Retorna a própria Submissão encontrada.

    Retorna None quando não existir uma Submissão com o código
    informado.

    Esta função não valida a estrutura completa da Homologação.
    """

    if not isinstance(submissoes, list):
        raise TypeError(
            "Submissões devem formar uma lista."
        )

    _validar_codigo_inteiro_positivo(
        codigo,
        "Código da Submissão",
    )

    for submissao in submissoes:
        if submissao.get("codigo") == codigo:
            return submissao

    return None

def buscar_submissao_por_numero_sequencial(
    submissoes: list[dict],
    numero_sequencial: int,
) -> dict | None:
    """
    Busca uma Submissão pelo número sequencial dentro de uma coleção.

    Retorna a própria Submissão encontrada.

    Retorna None quando não existir uma Submissão com o número
    sequencial informado.

    Esta função não valida a estrutura completa da Homologação.
    """

    if not isinstance(submissoes, list):
        raise TypeError(
            "Submissões devem formar uma lista."
        )

    _validar_codigo_inteiro_positivo(
        numero_sequencial,
        "Número sequencial da Submissão",
    )

    for submissao in submissoes:
        if (
            submissao.get("numero_sequencial")
            == numero_sequencial
        ):
            return submissao

    return None

def _obter_submissao_obrigatoria(
    homologacao: dict,
    codigo_submissao: int,
) -> dict:
    """
    Obtém uma Submissão existente dentro da Homologação.

    A função:

    1. busca a Submissão pelo código;
    2. exige que ela pertença à coleção da Homologação;
    3. valida sua estrutura local completa;
    4. retorna a própria Submissão armazenada no agregado.

    A estrutura da Homologação e o código informado devem ter sido
    validados anteriormente pela operação chamadora.

    Exceções:
        ValueError:
            quando a Submissão não for encontrada ou quando sua
            estrutura local for inválida.
    """

    submissao = buscar_submissao_por_codigo(
        submissoes=homologacao["submissoes"],
        codigo=codigo_submissao,
    )

    if submissao is None:
        raise ValueError(
            "Submissão não encontrada na Homologação."
        )

    validar_submissao(
        submissao
    )

    return submissao

# ============================================================
# REGRAS RELACIONAIS PRIVADAS DE SUBMISSÕES
# ============================================================

def _validar_sequencia_submissao(
    homologacao: dict,
    submissao: dict,
) -> None:
    """
    Valida a posição histórica da nova Submissão.

    Regras:

    - a primeira Submissão deve ser INICIAL;
    - a primeira Submissão deve possuir número sequencial 1;
    - só pode existir uma Submissão Inicial;
    - as demais devem continuar a sequência sem saltos.

    A existência e a posição da Submissão de origem são validadas
    separadamente por:

        _validar_origem_da_submissao()
    """

    submissoes = homologacao["submissoes"]
    tipo = submissao["tipo"]
    numero_sequencial = submissao["numero_sequencial"]

    if not submissoes:
        if tipo != TipoSubmissao.INICIAL.value:
            raise ValueError(
                "A primeira Submissão da Homologação "
                "deve ser do tipo INICIAL."
            )

        if numero_sequencial != 1:
            raise ValueError(
                "A primeira Submissão da Homologação "
                "deve possuir número sequencial 1."
            )

        return

    if tipo == TipoSubmissao.INICIAL.value:
        raise ValueError(
            "A Homologação já possui uma Submissão Inicial."
        )

    maior_numero_sequencial = max(
        submissao_existente["numero_sequencial"]
        for submissao_existente in submissoes
    )

    numero_esperado = maior_numero_sequencial + 1

    if numero_sequencial != numero_esperado:
        raise ValueError(
            "O número sequencial da nova Submissão deve ser "
            f"{numero_esperado}."
        )

def _validar_origem_da_submissao(
    homologacao: dict,
    submissao: dict,
) -> None:
    """
    Valida a origem de uma Submissão.

    Regras:

    - uma Submissão Inicial não possui Submissão de origem;
    - uma Submissão Inicial não possui Resposta de origem;
    - uma Submissão Inicial não possui Exigências relacionadas;
    - Complementação e Reenvio devem possuir Submissão de origem;
    - Complementação e Reenvio devem possuir Resposta de origem;
    - a Submissão de origem deve existir na mesma Homologação;
    - a Submissão de origem deve ser anterior à nova Submissão;
    - a Resposta de origem deve existir dentro da Submissão
      de origem informada;
    - todas as Exigências relacionadas devem pertencer à
      Resposta de origem.
    """

    tipo_submissao = TipoSubmissao(
        submissao["tipo"]
    )

    codigo_submissao_origem = submissao[
        "codigo_submissao_origem"
    ]

    codigo_resposta_origem = submissao[
        "codigo_resposta_origem"
    ]

    codigos_exigencias_relacionadas = submissao[
        "codigos_exigencias_relacionadas"
    ]

    if tipo_submissao == TipoSubmissao.INICIAL:
        if codigo_submissao_origem is not None:
            raise ValueError(
                "Uma Submissão Inicial não pode possuir "
                "Submissão de origem."
            )

        if codigo_resposta_origem is not None:
            raise ValueError(
                "Uma Submissão Inicial não pode possuir "
                "Resposta de origem."
            )

        if codigos_exigencias_relacionadas:
            raise ValueError(
                "Uma Submissão Inicial não pode possuir "
                "Exigências relacionadas."
            )

        return

    if codigo_submissao_origem is None:
        raise ValueError(
            "Complementação e Reenvio devem possuir "
            "Submissão de origem."
        )

    if codigo_resposta_origem is None:
        raise ValueError(
            "Complementação e Reenvio devem possuir "
            "Resposta de origem."
        )

    submissao_origem = buscar_submissao_por_codigo(
        submissoes=homologacao["submissoes"],
        codigo=codigo_submissao_origem,
    )

    if submissao_origem is None:
        raise ValueError(
            "Submissão de origem não encontrada "
            "na Homologação."
        )

    if (
        submissao_origem["numero_sequencial"]
        >= submissao["numero_sequencial"]
    ):
        raise ValueError(
            "A Submissão de origem deve ser anterior "
            "à nova Submissão."
        )

    resposta_origem = (
        _buscar_resposta_por_codigo_na_submissao(
            submissao=submissao_origem,
            codigo_resposta=codigo_resposta_origem,
        )
    )

    if resposta_origem is None:
        raise ValueError(
            "Resposta de origem não encontrada dentro "
            "da Submissão de origem informada."
        )

    codigos_exigencias_da_resposta = {
        exigencia["codigo"]
        for exigencia in resposta_origem.get(
            "exigencias",
            [],
        )
        if isinstance(exigencia, dict)
        and "codigo" in exigencia
    }

    for codigo_exigencia in (
        codigos_exigencias_relacionadas
    ):
        if (
            codigo_exigencia
            not in codigos_exigencias_da_resposta
        ):
            raise ValueError(
                "A Exigência relacionada não pertence "
                "à Resposta de origem informada: "
                f"código {codigo_exigencia}."
            )

def _validar_documentos_da_submissao(
    homologacao: dict,
    submissao: dict,
) -> None:
    """
    Valida se cada referência documental da Submissão corresponde
    a um Documento existente e à versão correta.

    A Submissão registra:

        codigo_documento
        numero_versao

    A raiz confirma que essa combinação realmente existe dentro
    da Homologação.
    """

    documentos = homologacao["documentos"]

    for referencia in submissao["pacote_documental"]:
        codigo_documento = referencia[
            "codigo_documento"
        ]

        numero_versao = referencia[
            "numero_versao"
        ]

        documento = buscar_documento_por_codigo(
            documentos=documentos,
            codigo=codigo_documento,
        )

        if documento is None:
            raise ValueError(
                "Documento do pacote não encontrado "
                "na Homologação: "
                f"código {codigo_documento}."
            )

        if documento.get("versao") != numero_versao:
            raise ValueError(
                "A versão documental informada na Submissão "
                "não corresponde à versão do Documento: "
                f"documento {codigo_documento}, "
                f"versão informada {numero_versao}, "
                f"versão existente {documento.get('versao')}."
            )

def _validar_exigencias_da_submissao(
    homologacao: dict,
    submissao: dict,
) -> None:
    """
    Valida as Exigências relacionadas a uma Complementação
    ou a um Reenvio.

    Para cada código, a função verifica:

    - existência da Exigência;
    - compatibilidade com o tipo da Submissão;
    - se a Exigência ainda está pendente;
    - se não existe outra Submissão ativa tentando atender
      a mesma Exigência.

    Uma Submissão cancelada deixa de bloquear uma nova tentativa
    de atendimento.
    """

    codigos_exigencias = submissao[
        "codigos_exigencias_relacionadas"
    ]

    for codigo_exigencia in codigos_exigencias:
        exigencia = _buscar_exigencia_por_codigo(
            submissoes=homologacao["submissoes"],
            codigo_exigencia=codigo_exigencia,
        )

        if exigencia is None:
            raise ValueError(
                "Exigência relacionada não encontrada "
                "na Homologação: "
                f"código {codigo_exigencia}."
            )

        if exigencia.get("status_atendimento") != "PENDENTE":
            raise ValueError(
                "Somente Exigências pendentes podem ser "
                "relacionadas a uma nova Submissão."
            )

        validar_compatibilidade_exigencia_submissao(
            tipo_exigencia=exigencia["tipo"],
            tipo_submissao=submissao["tipo"],
        )

        for submissao_existente in homologacao["submissoes"]:
            status_operacional = submissao_existente.get(
                "status_operacional"
            )

            if (
                status_operacional
                == StatusOperacionalSubmissao.CANCELADA.value
            ):
                continue

            codigos_ja_relacionados = submissao_existente.get(
                "codigos_exigencias_relacionadas",
                [],
            )

            if codigo_exigencia in codigos_ja_relacionados:
                raise ValueError(
                    "A Exigência já está relacionada a outra "
                    "Submissão ativa: "
                    f"código {codigo_exigencia}."
                )

def _validar_submissao_pode_receber_resposta(
    submissao: dict,
    mensagem_erro: str | None = None,
) -> StatusOperacionalSubmissao:
    """
    Valida se uma Submissão pode receber um retorno
    da concessionária.

    Somente Submissões que já tenham sido formalmente enviadas
    podem receber Respostas ou Exigências.

    Estados operacionais permitidos:

        ENVIADA
        PROTOCOLADA

    Parâmetros:
        submissao:
            Submissão já pertencente ao agregado.

        mensagem_erro:
            Mensagem contextual opcional para a operação.
            Quando omitida, utiliza a mensagem padrão de Respostas.

    Retorno:
        O StatusOperacionalSubmissao convertido e validado.

    A estrutura local completa da Submissão deve ter sido validada
    anteriormente pela operação chamadora.
    """

    status_operacional = (
        _converter_status_operacional_submissao(
            submissao["status_operacional"]
        )
    )

    estados_operacionais_permitidos = {
        StatusOperacionalSubmissao.ENVIADA,
        StatusOperacionalSubmissao.PROTOCOLADA,
    }

    if (
        status_operacional
        not in estados_operacionais_permitidos
    ):
        if mensagem_erro is None:
            mensagem_erro = (
                "Somente uma Submissão enviada ou protocolada "
                "pode receber Respostas da concessionária."
            )

        raise ValueError(
            mensagem_erro
        )

    return status_operacional

# ============================================================
# OPERAÇÕES DE SUBMISSÕES
# ============================================================

def adicionar_submissao_homologacao(
    homologacao: dict,
    submissao: dict,
    data_movimentacao: str,
    responsavel: str,
) -> dict:
    """
    Adiciona uma Submissão à Homologação com segurança.

    A função:

    1. valida a estrutura da Homologação;
    2. impede alterações em Homologações terminais;
    3. valida localmente a Submissão;
    4. impede código duplicado;
    5. impede número sequencial duplicado;
    6. valida a ordem histórica;
    7. valida a Submissão e a Resposta de origem;
    8. valida Documentos e versões do pacote;
    9. valida Exigências relacionadas;
    10. cria a Movimentação da Submissão;
    11. para Complementação ou Reenvio, prepara o Evento
        SUBMISSAO_DERIVADA_CRIADA;
    12. adiciona a Submissão;
    13. registra as Movimentações;
    14. atualiza o estado geral da Homologação, quando derivada.

    Nenhuma alteração é aplicada à Submissão recebida, às coleções
    internas ou ao estado geral da Homologação antes da conclusão
    de todas as validações e da preparação do Evento correspondente.
    """

    _validar_estrutura_homologacao(
        homologacao
    )

    _validar_homologacao_nao_terminal(
        homologacao=homologacao,
        mensagem_erro=(
            "Não é possível adicionar Submissões a uma "
            "Homologação em estado terminal."
        ),
    )

    validar_submissao(
        submissao
    )

    data_normalizada = _validar_data_iso(
        data_movimentacao,
        "Data da movimentação",
    ).isoformat()

    responsavel_normalizado = _validar_texto_obrigatorio(
        responsavel,
        "Responsável pela movimentação",
    )

    submissoes = homologacao["submissoes"]

    submissao_com_mesmo_codigo = (
        buscar_submissao_por_codigo(
            submissoes=submissoes,
            codigo=submissao["codigo"],
        )
    )

    if submissao_com_mesmo_codigo is not None:
        raise ValueError(
            "Já existe uma Submissão com o código informado "
            "nesta Homologação."
        )

    submissao_com_mesma_sequencia = (
        buscar_submissao_por_numero_sequencial(
            submissoes=submissoes,
            numero_sequencial=(
                submissao["numero_sequencial"]
            ),
        )
    )

    if submissao_com_mesma_sequencia is not None:
        raise ValueError(
            "Já existe uma Submissão com o número sequencial "
            "informado nesta Homologação."
        )

    _validar_sequencia_submissao(
        homologacao=homologacao,
        submissao=submissao,
    )

    _validar_origem_da_submissao(
        homologacao=homologacao,
        submissao=submissao,
    )

    _validar_documentos_da_submissao(
        homologacao=homologacao,
        submissao=submissao,
    )

    _validar_exigencias_da_submissao(
        homologacao=homologacao,
        submissao=submissao,
    )

    movimentacao_submissao = (
        criar_movimentacao_submissao_adicionada(
            movimentacoes=homologacao["movimentacoes"],
            submissao=submissao,
            data_movimentacao=data_normalizada,
            responsavel=responsavel_normalizado,
        )
    )

    tipo_submissao = TipoSubmissao(
        submissao["tipo"]
    )

    tipos_derivados = {
        TipoSubmissao.COMPLEMENTACAO,
        TipoSubmissao.REENVIO,
    }

    movimentacao_evento = None
    novo_status_homologacao = homologacao["status"]
    novo_responsavel_homologacao = (
        responsavel_normalizado
    )

    if tipo_submissao in tipos_derivados:
        (
            novo_status_homologacao,
            novo_responsavel_homologacao,
            movimentacao_evento,
        ) = _preparar_evento_homologacao(
            homologacao=homologacao,
            evento=(
                EventoHomologacao
                .SUBMISSAO_DERIVADA_CRIADA
            ),
            data_movimentacao=data_normalizada,
            responsavel=responsavel_normalizado,
            descricao=(
                "Homologação colocada em correção após "
                "a criação de uma Submissão derivada."
            ),
            movimentacoes_precedentes=[
                movimentacao_submissao
            ],
        )

    submissoes.append(
        submissao
    )

    homologacao["movimentacoes"].append(
        movimentacao_submissao
    )

    homologacao["status"] = (
        novo_status_homologacao
    )

    homologacao["responsavel_atual"] = (
        novo_responsavel_homologacao
    )

    if movimentacao_evento is not None:
        homologacao["movimentacoes"].append(
            movimentacao_evento
        )

    return homologacao

def alterar_status_operacional_submissao(
    homologacao: dict,
    codigo_submissao: int,
    novo_status: str | StatusOperacionalSubmissao,
    data_movimentacao: str,
    responsavel: str,
    motivo: str | None = None,
) -> dict:
    """
    Altera o status operacional de uma Submissão pertencente
    à Homologação.

    Esta função é responsável somente pelas transições que não
    exigem dados de envio ou protocolo:

        EM_PREPARACAO -> PRONTA_PARA_ENVIO
        EM_PREPARACAO -> CANCELADA

        PRONTA_PARA_ENVIO -> EM_PREPARACAO
        PRONTA_PARA_ENVIO -> CANCELADA

    As transições abaixo pertencem a operações específicas:

        PRONTA_PARA_ENVIO -> ENVIADA
            enviar_submissao_homologacao()

        ENVIADA -> PROTOCOLADA
            protocolar_submissao_homologacao()

    A função:

    1. valida a estrutura da Homologação;
    2. impede operações em Homologações terminais;
    3. localiza a Submissão;
    4. valida a estrutura atual da Submissão;
    5. converte os estados;
    6. impede que esta operação realize envio ou protocolo;
    7. valida a transição na máquina de estados;
    8. exige motivo para cancelamento;
    9. cria a Movimentação;
    10. altera o estado da Submissão;
    11. registra o responsável atual da Homologação.

    Nenhuma alteração é aplicada à Submissão ou à Homologação antes
    da conclusão de todas as validações.
    """

    _validar_estrutura_homologacao(
        homologacao
    )

    _validar_codigo_inteiro_positivo(
        codigo_submissao,
        "Código da Submissão",
    )

    _validar_homologacao_nao_terminal(
        homologacao=homologacao,
        mensagem_erro=(
            "Não é possível alterar Submissões de uma "
            "Homologação em estado terminal."
        ),
    )

    submissao = _obter_submissao_obrigatoria(
        homologacao=homologacao,
        codigo_submissao=codigo_submissao,
    )

    status_atual = (
        _converter_status_operacional_submissao(
            submissao["status_operacional"]
        )
    )

    novo_status_convertido = (
        _converter_status_operacional_submissao(
            novo_status
        )
    )

    estados_exclusivos_de_operacoes_especificas = {
        StatusOperacionalSubmissao.ENVIADA,
        StatusOperacionalSubmissao.PROTOCOLADA,
    }

    if (
        novo_status_convertido
        in estados_exclusivos_de_operacoes_especificas
    ):
        raise ValueError(
            "O estado "
            f"{novo_status_convertido.value} "
            "deve ser alcançado por uma operação específica "
            "de envio ou protocolo."
        )

    validar_transicao_operacional_submissao(
        status_atual=status_atual,
        novo_status=novo_status_convertido,
    )

    data_normalizada = _validar_data_iso(
        data_movimentacao,
        "Data da movimentação",
    ).isoformat()

    responsavel_normalizado = _validar_texto_obrigatorio(
        responsavel,
        "Responsável pela movimentação",
    )

    motivo_normalizado = (
        _validar_motivo_status_operacional_submissao(
            novo_status=novo_status_convertido,
            motivo=motivo,
        )
    )

    movimentacao = (
        criar_movimentacao_status_operacional_submissao(
            movimentacoes=homologacao["movimentacoes"],
            submissao=submissao,
            status_anterior=status_atual,
            novo_status=novo_status_convertido,
            data_movimentacao=data_normalizada,
            responsavel=responsavel_normalizado,
            motivo=motivo_normalizado,
        )
    )

    submissao["status_operacional"] = (
        novo_status_convertido.value
    )

    homologacao["movimentacoes"].append(
        movimentacao
    )

    homologacao["responsavel_atual"] = (
        responsavel_normalizado
    )

    return homologacao

def enviar_submissao_homologacao(
    homologacao: dict,
    codigo_submissao: int,
    canal_envio: str | CanalEnvioSubmissao,
    data_envio: str,
    responsavel_envio: str,
) -> dict:
    """
    Registra o envio formal de uma Submissão à concessionária.

    Quando a Submissão for uma Complementação ou um Reenvio,
    as Exigências relacionadas são marcadas como ATENDIDAS.

    A função:

    1. valida a estrutura da Homologação;
    2. impede operações em Homologações terminais;
    3. valida o código da Submissão;
    4. localiza a Submissão no agregado;
    5. valida a estrutura atual da Submissão;
    6. exige o estado PRONTA_PARA_ENVIO;
    7. valida a transição para ENVIADA;
    8. valida o canal de envio;
    9. valida a data;
    10. valida e normaliza o responsável;
    11. valida novamente os Documentos do pacote;
    12. cria e valida uma Submissão candidata;
    13. prepara os atendimentos das Exigências;
    14. cria a Movimentação de envio;
    15. aplica as alterações na Submissão real;
    16. aplica os atendimentos das Exigências;
    17. registra a Movimentação;
    18. atualiza o responsável atual da Homologação.

    Nenhuma alteração é aplicada às estruturas reais antes de todas
    as validações serem concluídas.

    Nenhuma alteração é aplicada à Submissão, às Exigências ou à
    Homologação antes da conclusão de todas as validações e da
    preparação do Evento de negócio correspondente.
    """

    _validar_estrutura_homologacao(
        homologacao
    )

    _validar_codigo_inteiro_positivo(
        codigo_submissao,
        "Código da Submissão",
    )

    _validar_homologacao_nao_terminal(
        homologacao=homologacao,
        mensagem_erro=(
            "Não é possível enviar Submissões de uma "
            "Homologação em estado terminal."
        ),
    )

    submissao = _obter_submissao_obrigatoria(
        homologacao=homologacao,
        codigo_submissao=codigo_submissao,
    )

    status_atual = (
        _converter_status_operacional_submissao(
            submissao["status_operacional"]
        )
    )

    if (
        status_atual
        != StatusOperacionalSubmissao.PRONTA_PARA_ENVIO
    ):
        raise ValueError(
            "Somente uma Submissão PRONTA_PARA_ENVIO "
            "pode ser enviada à concessionária."
        )

    validar_transicao_operacional_submissao(
        status_atual=status_atual,
        novo_status=StatusOperacionalSubmissao.ENVIADA,
    )

    canal_convertido = (
        _converter_canal_envio_submissao(
            canal_envio
        )
    )

    data_normalizada = _validar_data_iso(
        data_envio,
        "Data de envio",
    ).isoformat()

    responsavel_normalizado = _validar_texto_obrigatorio(
        responsavel_envio,
        "Responsável pelo envio",
    )

    _validar_documentos_da_submissao(
        homologacao=homologacao,
        submissao=submissao,
    )

    submissao_candidata = _copiar_submissao(
        submissao
    )

    submissao_candidata["status_operacional"] = (
        StatusOperacionalSubmissao.ENVIADA.value
    )

    submissao_candidata["canal_envio"] = (
        canal_convertido.value
    )

    submissao_candidata["data_envio"] = (
        data_normalizada
    )

    submissao_candidata["responsavel_envio"] = (
        responsavel_normalizado
    )

    validar_submissao(
        submissao_candidata
    )

    atendimentos_exigencias = (
        _preparar_atendimentos_exigencias_submissao(
            homologacao=homologacao,
            submissao=submissao,
            data_atendimento=data_normalizada,
            responsavel_atendimento=(
                responsavel_normalizado
            ),
        )
    )

    movimentacao_envio = (
        criar_movimentacao_submissao_enviada(
            movimentacoes=homologacao["movimentacoes"],
            submissao=submissao,
            canal_envio=canal_convertido,
            data_envio=data_normalizada,
            responsavel_envio=responsavel_normalizado,
        )
    )

    tipo_submissao = TipoSubmissao(
        submissao["tipo"]
    )

    tipos_derivados = {
        TipoSubmissao.COMPLEMENTACAO,
        TipoSubmissao.REENVIO,
    }

    movimentacao_evento = None
    novo_status_homologacao = homologacao["status"]
    novo_responsavel_homologacao = (
        responsavel_normalizado
    )

    if tipo_submissao in tipos_derivados:
        (
            novo_status_homologacao,
            novo_responsavel_homologacao,
            movimentacao_evento,
        ) = _preparar_evento_homologacao(
            homologacao=homologacao,
            evento=(
                EventoHomologacao
                .SUBMISSAO_DERIVADA_ENVIADA
            ),
            data_movimentacao=data_normalizada,
            responsavel=responsavel_normalizado,
            descricao=(
                "Homologação reapresentada à concessionária "
                "por meio de uma Submissão derivada."
            ),
            movimentacoes_precedentes=[
                movimentacao_envio
            ],
        )

    submissao["status_operacional"] = (
        StatusOperacionalSubmissao.ENVIADA.value
    )

    submissao["canal_envio"] = (
        canal_convertido.value
    )

    submissao["data_envio"] = (
        data_normalizada
    )

    submissao["responsavel_envio"] = (
        responsavel_normalizado
    )

    for (
        exigencia,
        exigencia_candidata,
    ) in atendimentos_exigencias:
        exigencia.update(
            exigencia_candidata
        )

    homologacao["movimentacoes"].append(
        movimentacao_envio
    )

    homologacao["status"] = (
        novo_status_homologacao
    )

    homologacao["responsavel_atual"] = (
        novo_responsavel_homologacao
    )

    if movimentacao_evento is not None:
        homologacao["movimentacoes"].append(
            movimentacao_evento
        )

    return homologacao

def protocolar_submissao_homologacao(
    homologacao: dict,
    codigo_submissao: int,
    protocolo: str,
    data_protocolo: str,
    responsavel: str,
) -> dict:
    """
    Registra o protocolo de uma Submissão enviada.

    A função:

    1. valida a estrutura da Homologação;
    2. impede operações em Homologações terminais;
    3. valida o código informado;
    4. localiza a Submissão no agregado;
    5. valida a Submissão atual;
    6. exige o estado ENVIADA;
    7. valida a transição para PROTOCOLADA;
    8. valida e normaliza o número do protocolo;
    9. valida a data do protocolo;
    10. valida e normaliza o responsável;
    11. cria uma cópia candidata;
    12. valida a candidata completa;
    13. cria a Movimentação;
    14. aplica os dados na Submissão real;
    15. registra a Movimentação;
    16. atualiza o responsável atual da Homologação.

    Nenhuma alteração é aplicada à Submissão ou à Homologação antes
    da conclusão de todas as validações e da construção segura da
    Movimentação correspondente.
    """

    _validar_estrutura_homologacao(
        homologacao
    )

    _validar_codigo_inteiro_positivo(
        codigo_submissao,
        "Código da Submissão",
    )

    _validar_homologacao_nao_terminal(
        homologacao=homologacao,
        mensagem_erro=(
            "Não é possível protocolar Submissões de uma "
            "Homologação em estado terminal."
        ),
    )

    submissao = _obter_submissao_obrigatoria(
        homologacao=homologacao,
        codigo_submissao=codigo_submissao,
    )

    status_atual = (
        _converter_status_operacional_submissao(
            submissao["status_operacional"]
        )
    )

    if (
        status_atual
        != StatusOperacionalSubmissao.ENVIADA
    ):
        raise ValueError(
            "Somente uma Submissão ENVIADA pode ser "
            "protocolada."
        )

    validar_transicao_operacional_submissao(
        status_atual=status_atual,
        novo_status=(
            StatusOperacionalSubmissao.PROTOCOLADA
        ),
    )

    protocolo_normalizado = _validar_texto_obrigatorio(
        protocolo,
        "Protocolo da Submissão",
    )

    data_normalizada = _validar_data_iso(
        data_protocolo,
        "Data do protocolo",
    ).isoformat()

    responsavel_normalizado = _validar_texto_obrigatorio(
        responsavel,
        "Responsável pela protocolação",
    )

    submissao_candidata = _copiar_submissao(
        submissao
    )

    submissao_candidata["status_operacional"] = (
        StatusOperacionalSubmissao.PROTOCOLADA.value
    )

    submissao_candidata["protocolo"] = (
        protocolo_normalizado
    )

    submissao_candidata["data_protocolo"] = (
        data_normalizada
    )

    validar_submissao(
        submissao_candidata
    )

    movimentacao = (
        criar_movimentacao_submissao_protocolada(
            movimentacoes=homologacao["movimentacoes"],
            submissao=submissao,
            protocolo=protocolo_normalizado,
            data_protocolo=data_normalizada,
            responsavel=responsavel_normalizado,
        )
    )

    submissao["status_operacional"] = (
        StatusOperacionalSubmissao.PROTOCOLADA.value
    )

    submissao["protocolo"] = (
        protocolo_normalizado
    )

    submissao["data_protocolo"] = (
        data_normalizada
    )

    homologacao["movimentacoes"].append(
        movimentacao
    )

    homologacao["responsavel_atual"] = (
        responsavel_normalizado
    )

    return homologacao

# ============================================================
# OPERAÇÕES DE RESPOSTAS DA CONCESSIONÁRIA
# ============================================================

def adicionar_resposta_concessionaria(
    homologacao: dict,
    codigo_submissao: int,
    resposta: dict,
) -> dict:
    """
    Adiciona uma Resposta da concessionária a uma Submissão.

    São aceitas nesta operação:

        RECEBIMENTO_CONFIRMADO
        ANALISE_INICIADA
        APROVACAO
        REJEICAO

    Respostas do tipo EXIGENCIA pertencem à operação específica:

        adicionar_resposta_exigencia_concessionaria()

    Reflexos no estado geral da Homologação:

        RECEBIMENTO_CONFIRMADO:
            não altera o status geral;

        ANALISE_INICIADA:
            aplica o Evento ANALISE_INICIADA;

        APROVACAO:
            aplica o Evento APROVACAO_RECEBIDA;

        REJEICAO:
            aplica o Evento REJEICAO_RECEBIDA.

    Nenhuma estrutura real é alterada antes de todas as
    validações serem concluídas.

    Nenhuma alteração é aplicada à Submissão ou à Homologação antes
    da validação completa da candidata e da preparação do Evento de
    negócio correspondente.
    """

    _validar_estrutura_homologacao(
        homologacao
    )

    _validar_codigo_inteiro_positivo(
        codigo_submissao,
        "Código da Submissão",
    )

    _validar_homologacao_nao_terminal(
        homologacao=homologacao,
        mensagem_erro=(
            "Não é possível registrar Respostas em uma "
            "Homologação em estado terminal."
        ),
    )

    submissao = _obter_submissao_obrigatoria(
        homologacao=homologacao,
        codigo_submissao=codigo_submissao,
    )

    validar_resposta_concessionaria(
        resposta
    )

    tipo_resposta = TipoRespostaConcessionaria(
        resposta["tipo"]
    )

    if tipo_resposta == TipoRespostaConcessionaria.EXIGENCIA:
        raise ValueError(
            "Respostas do tipo EXIGENCIA devem ser registradas "
            "pela operação específica de Exigências."
        )

    _validar_submissao_pode_receber_resposta(
        submissao
    )

    _validar_sequencia_resposta_concessionaria(
        submissao=submissao,
        resposta=resposta,
    )

    _validar_data_resposta_submissao(
        submissao=submissao,
        resposta=resposta,
    )

    status_anterior = StatusAnaliseSubmissao(
        submissao["status_analise"]
    )

    novo_status = obter_status_resultante_resposta(
        tipo_resposta
    )

    validar_transicao_analise_submissao(
        status_atual=status_anterior,
        novo_status=novo_status,
    )

    resposta_copiada = (
        _copiar_resposta_concessionaria(
            resposta
        )
    )

    submissao_candidata = _copiar_submissao(
        submissao
    )

    submissao_candidata["respostas"] = [
        *submissao["respostas"],
        resposta_copiada,
    ]

    submissao_candidata["status_analise"] = (
        novo_status.value
    )

    validar_submissao(
        submissao_candidata
    )

    movimentacao_resposta = (
        criar_movimentacao_resposta_concessionaria(
            movimentacoes=homologacao["movimentacoes"],
            submissao=submissao,
            resposta=resposta_copiada,
            status_anterior=status_anterior,
            novo_status=novo_status,
        )
    )

    evento_homologacao = None
    descricao_evento = None
    motivo_evento = None

    if (
        tipo_resposta
        == TipoRespostaConcessionaria.ANALISE_INICIADA
    ):
        evento_homologacao = (
            EventoHomologacao.ANALISE_INICIADA
        )

        descricao_evento = (
            "Homologação colocada em análise após retorno "
            "da concessionária."
        )

    elif (
        tipo_resposta
        == TipoRespostaConcessionaria.APROVACAO
    ):
        evento_homologacao = (
            EventoHomologacao.APROVACAO_RECEBIDA
        )

        descricao_evento = (
            "Parecer de acesso emitido após aprovação "
            "da concessionária."
        )

    elif (
        tipo_resposta
        == TipoRespostaConcessionaria.REJEICAO
    ):
        evento_homologacao = (
            EventoHomologacao.REJEICAO_RECEBIDA
        )

        descricao_evento = (
            "Homologação rejeitada pela concessionária."
        )

        motivo_evento = resposta_copiada["descricao"]

    movimentacao_evento = None
    novo_status_homologacao = homologacao["status"]
    novo_responsavel_homologacao = (
        resposta_copiada["responsavel_registro"]
    )

    if evento_homologacao is not None:
        (
            novo_status_homologacao,
            novo_responsavel_homologacao,
            movimentacao_evento,
        ) = _preparar_evento_homologacao(
            homologacao=homologacao,
            evento=evento_homologacao,
            data_movimentacao=(
                resposta_copiada["data_registro"]
            ),
            responsavel=(
                resposta_copiada["responsavel_registro"]
            ),
            descricao=descricao_evento,
            motivo=motivo_evento,
            movimentacoes_precedentes=[
                movimentacao_resposta
            ],
        )

    submissao["respostas"].append(
        resposta_copiada
    )

    submissao["status_analise"] = (
        novo_status.value
    )

    homologacao["movimentacoes"].append(
        movimentacao_resposta
    )

    homologacao["status"] = (
        novo_status_homologacao
    )

    homologacao["responsavel_atual"] = (
        novo_responsavel_homologacao
    )

    if movimentacao_evento is not None:
        homologacao["movimentacoes"].append(
            movimentacao_evento
        )

    return homologacao

def adicionar_resposta_exigencia_concessionaria(
    homologacao: dict,
    codigo_submissao: int,
    resposta: dict,
) -> dict:
    """
    Adiciona uma Resposta de Exigência a uma Submissão.

    A operação valida:

    - a Homologação;
    - a Submissão;
    - a Resposta;
    - o tipo EXIGENCIA;
    - o estado operacional da Submissão;
    - a sequência das Respostas;
    - a cronologia;
    - cada Exigência;
    - a sequência interna das Exigências;
    - a unicidade global dos códigos;
    - a existência dos Documentos afetados;
    - a transição da análise para COM_EXIGENCIA;
    - a Submissão candidata completa;
    - o Evento EXIGENCIA_RECEBIDA no estado geral
      da Homologação.

    Ao final, a operação registra:

    1. a Movimentação da Resposta de Exigência;
    2. a Movimentação da mudança de estado da Homologação.

    Nenhuma estrutura real é alterada antes da conclusão
    de todas as validações.

    Nenhuma alteração é aplicada à Submissão, às Exigências ou à
    Homologação antes da validação completa da candidata e da
    preparação do Evento EXIGENCIA_RECEBIDA.
    """

    _validar_estrutura_homologacao(
        homologacao
    )

    _validar_codigo_inteiro_positivo(
        codigo_submissao,
        "Código da Submissão",
    )

    _validar_homologacao_nao_terminal(
        homologacao=homologacao,
        mensagem_erro=(
            "Não é possível registrar Exigências em uma "
            "Homologação em estado terminal."
        ),
    )

    submissao = _obter_submissao_obrigatoria(
        homologacao=homologacao,
        codigo_submissao=codigo_submissao,
    )

    validar_resposta_concessionaria(
        resposta
    )

    if (
        resposta["tipo"]
        != TipoRespostaConcessionaria.EXIGENCIA.value
    ):
        raise ValueError(
            "A operação específica de Exigências aceita somente "
            "Respostas do tipo EXIGENCIA."
        )

    _validar_submissao_pode_receber_resposta(
        submissao=submissao,
        mensagem_erro=(
            "Somente uma Submissão enviada ou protocolada "
            "pode receber Exigências da concessionária."
        ),
    )

    _validar_sequencia_resposta_concessionaria(
        submissao=submissao,
        resposta=resposta,
    )

    _validar_data_resposta_submissao(
        submissao=submissao,
        resposta=resposta,
    )

    for exigencia in resposta["exigencias"]:
        validar_exigencia(
            exigencia
        )

    _validar_sequencia_exigencias_resposta(
        resposta
    )

    _validar_codigos_exigencias_unicos(
        homologacao=homologacao,
        resposta=resposta,
    )

    _validar_documentos_afetados_exigencias(
        homologacao=homologacao,
        resposta=resposta,
    )

    status_anterior = StatusAnaliseSubmissao(
        submissao["status_analise"]
    )

    novo_status = (
        StatusAnaliseSubmissao.COM_EXIGENCIA
    )

    validar_transicao_analise_submissao(
        status_atual=status_anterior,
        novo_status=novo_status,
    )

    resposta_copiada = (
        _copiar_resposta_concessionaria(
            resposta
        )
    )

    submissao_candidata = _copiar_submissao(
        submissao
    )

    submissao_candidata["respostas"] = [
        *submissao["respostas"],
        resposta_copiada,
    ]

    submissao_candidata["status_analise"] = (
        novo_status.value
    )

    validar_submissao(
        submissao_candidata
    )

    movimentacao_resposta = (
        criar_movimentacao_resposta_exigencia(
            movimentacoes=homologacao["movimentacoes"],
            submissao=submissao,
            resposta=resposta_copiada,
            status_anterior=status_anterior,
        )
    )

    (
        novo_status_homologacao,
        novo_responsavel_homologacao,
        movimentacao_evento,
    ) = _preparar_evento_homologacao(
        homologacao=homologacao,
        evento=EventoHomologacao.EXIGENCIA_RECEBIDA,
        data_movimentacao=resposta_copiada["data_registro"],
        responsavel=(
            resposta_copiada["responsavel_registro"]
        ),
        descricao=(
            "Homologação atualizada após o recebimento "
            "de Exigências da concessionária."
        ),
        movimentacoes_precedentes=[
            movimentacao_resposta
        ],
    )

    submissao["respostas"].append(
        resposta_copiada
    )

    submissao["status_analise"] = (
        novo_status.value
    )

    homologacao["movimentacoes"].append(
        movimentacao_resposta
    )

    homologacao["status"] = (
        novo_status_homologacao
    )

    homologacao["responsavel_atual"] = (
        novo_responsavel_homologacao
    )

    homologacao["movimentacoes"].append(
        movimentacao_evento
    )

    return homologacao

# ============================================================
# OPERAÇÕES DE CAMPO
# ============================================================

def registrar_planejamento_instalacao(
    homologacao: dict,
    data_prevista: str,
    responsavel_planejamento: str,
    equipe_responsavel: str,
    data_movimentacao: str,
    observacoes: str | None = None,
) -> dict:
    """
    Registra o planejamento da Instalação.

    A operação:

    1. valida a estrutura da Homologação;
    2. impede operações em estados terminais;
    3. exige um estado compatível com a Instalação;
    4. preserva registros antigos sem operacoes_campo;
    5. impede um segundo planejamento;
    6. cria e valida a Instalação candidata;
    7. prepara a Movimentação;
    8. aplica todas as alterações de forma atômica;
    9. atualiza o responsável atual da Homologação.

    Estados compatíveis:

    - PARECER_DE_ACESSO_EMITIDO;
    - AGUARDANDO_INSTALACAO.
    """

    _validar_estrutura_homologacao(
        homologacao
    )

    status_atual = (
        _validar_homologacao_nao_terminal(
            homologacao=homologacao,
            mensagem_erro=(
                "Não é possível planejar a Instalação "
                "de uma Homologação em estado terminal."
            ),
        )
    )

    estados_permitidos = {
        StatusHomologacao
        .PARECER_DE_ACESSO_EMITIDO,

        StatusHomologacao
        .AGUARDANDO_INSTALACAO,
    }

    if status_atual not in estados_permitidos:
        raise ValueError(
            "O planejamento da Instalação somente pode "
            "ser registrado após a emissão do parecer "
            "de acesso."
        )

    operacoes_candidatas = (
        _preparar_operacoes_campo_candidatas(
            homologacao
        )
    )

    if (
        operacoes_candidatas["instalacao"]
        is not None
    ):
        raise ValueError(
            "A Homologação já possui uma "
            "Instalação planejada."
        )

    instalacao_candidata = (
        criar_dados_planejamento_instalacao(
            data_prevista=data_prevista,
            responsavel_planejamento=(
                responsavel_planejamento
            ),
            equipe_responsavel=(
                equipe_responsavel
            ),
            observacoes=observacoes,
        )
    )

    validar_instalacao(
        instalacao_candidata
    )

    data_movimentacao_normalizada = (
        _validar_data_iso(
            data_movimentacao,
            "Data da movimentação",
        ).isoformat()
    )

    responsavel_normalizado = (
        _validar_texto_obrigatorio(
            responsavel_planejamento,
            "Responsável pelo planejamento",
        )
    )

    novo_status = (
        StatusHomologacao
        .AGUARDANDO_INSTALACAO
    )

    if (
        status_atual
        == StatusHomologacao
        .PARECER_DE_ACESSO_EMITIDO
    ):
        if not transicao_status_homologacao_e_valida(
            status_atual,
            novo_status,
        ):
            raise ValueError(
                "A transição para Aguardando Instalação "
                "não é permitida."
            )

    operacoes_candidatas[
        "instalacao"
    ] = instalacao_candidata

    validar_operacoes_campo(
        operacoes_candidatas
    )

    movimentacao = (
        criar_movimentacao_instalacao_planejada(
            movimentacoes=(
                homologacao["movimentacoes"]
            ),
            instalacao=instalacao_candidata,
            status_anterior=status_atual,
            novo_status=novo_status,
            data_movimentacao=(
                data_movimentacao_normalizada
            ),
            responsavel=(
                responsavel_normalizado
            ),
        )
    )

    # ---------------------------------------------------------
    # APLICAÇÃO ATÔMICA
    # ---------------------------------------------------------

    homologacao["operacoes_campo"] = (
        operacoes_candidatas
    )

    homologacao["status"] = (
        novo_status.value
    )

    homologacao["responsavel_atual"] = (
        responsavel_normalizado
    )

    homologacao["movimentacoes"].append(
        movimentacao
    )

    return homologacao

def iniciar_instalacao(
    homologacao: dict,
    data_inicio: str,
    responsavel_inicio: str,
    data_movimentacao: str,
) -> dict:
    """
    Registra o início da execução da Instalação.

    A operação:

    1. valida a estrutura da Homologação;
    2. impede operações em estados terminais;
    3. exige o status AGUARDANDO_INSTALACAO;
    4. exige uma Instalação planejada;
    5. prepara uma Instalação candidata;
    6. valida as Operações de Campo candidatas;
    7. cria a Movimentação;
    8. aplica as alterações de forma atômica;
    9. atualiza o responsável atual.

    O status geral da Homologação permanece
    AGUARDANDO_INSTALACAO.
    """

    _validar_estrutura_homologacao(
        homologacao
    )

    status_atual = (
        _validar_homologacao_nao_terminal(
            homologacao=homologacao,
            mensagem_erro=(
                "Não é possível iniciar a Instalação "
                "de uma Homologação em estado terminal."
            ),
        )
    )

    if (
        status_atual
        != StatusHomologacao
        .AGUARDANDO_INSTALACAO
    ):
        raise ValueError(
            "A Instalação somente pode ser iniciada "
            "quando a Homologação estiver aguardando "
            "a execução da Instalação."
        )

    operacoes_candidatas = (
        _preparar_operacoes_campo_candidatas(
            homologacao
        )
    )

    instalacao_atual = operacoes_candidatas[
        "instalacao"
    ]

    if instalacao_atual is None:
        raise ValueError(
            "A Homologação não possui uma "
            "Instalação planejada."
        )

    instalacao_candidata = (
        preparar_inicio_instalacao(
            instalacao=instalacao_atual,
            data_inicio=data_inicio,
            responsavel_inicio=(
                responsavel_inicio
            ),
        )
    )

    data_movimentacao_normalizada = (
        _validar_data_iso(
            data_movimentacao,
            "Data da movimentação",
        ).isoformat()
    )

    responsavel_normalizado = (
        _validar_texto_obrigatorio(
            responsavel_inicio,
            "Responsável pelo início",
        )
    )

    operacoes_candidatas[
        "instalacao"
    ] = instalacao_candidata

    validar_operacoes_campo(
        operacoes_candidatas
    )

    movimentacao = (
        criar_movimentacao_instalacao_iniciada(
            movimentacoes=(
                homologacao["movimentacoes"]
            ),
            instalacao=instalacao_candidata,
            data_movimentacao=(
                data_movimentacao_normalizada
            ),
            responsavel=(
                responsavel_normalizado
            ),
        )
    )

    # ---------------------------------------------------------
    # APLICAÇÃO ATÔMICA
    # ---------------------------------------------------------

    homologacao["operacoes_campo"] = (
        operacoes_candidatas
    )

    homologacao["responsavel_atual"] = (
        responsavel_normalizado
    )

    homologacao["movimentacoes"].append(
        movimentacao
    )

    return homologacao

def concluir_instalacao(
    homologacao: dict,
    data_conclusao: str,
    responsavel_conclusao: str,
    data_movimentacao: str,
    observacoes: str | None = None,
) -> dict:
    """
    Registra a conclusão da Instalação.

    A operação:

    1. valida a estrutura da Homologação;
    2. impede operações em estados terminais;
    3. exige o status AGUARDANDO_INSTALACAO;
    4. exige uma Instalação em execução;
    5. prepara a Instalação candidata;
    6. valida a transição do estado geral;
    7. prepara a Movimentação;
    8. aplica as alterações de forma atômica;
    9. atualiza o responsável atual.

    O status geral será alterado para
    INSTALACAO_CONCLUIDA.
    """

    _validar_estrutura_homologacao(
        homologacao
    )

    status_atual = (
        _validar_homologacao_nao_terminal(
            homologacao=homologacao,
            mensagem_erro=(
                "Não é possível concluir a Instalação "
                "de uma Homologação em estado terminal."
            ),
        )
    )

    if (
        status_atual
        != StatusHomologacao
        .AGUARDANDO_INSTALACAO
    ):
        raise ValueError(
            "A Instalação somente pode ser concluída "
            "quando a Homologação estiver aguardando "
            "a execução da Instalação."
        )

    operacoes_candidatas = (
        _preparar_operacoes_campo_candidatas(
            homologacao
        )
    )

    instalacao_atual = operacoes_candidatas[
        "instalacao"
    ]

    if instalacao_atual is None:
        raise ValueError(
            "A Homologação não possui uma "
            "Instalação registrada."
        )

    instalacao_candidata = (
        preparar_conclusao_instalacao(
            instalacao=instalacao_atual,
            data_conclusao=data_conclusao,
            responsavel_conclusao=(
                responsavel_conclusao
            ),
            observacoes=observacoes,
        )
    )

    data_movimentacao_normalizada = (
        _validar_data_iso(
            data_movimentacao,
            "Data da movimentação",
        ).isoformat()
    )

    responsavel_normalizado = (
        _validar_texto_obrigatorio(
            responsavel_conclusao,
            "Responsável pela conclusão",
        )
    )

    novo_status = (
        StatusHomologacao
        .INSTALACAO_CONCLUIDA
    )

    if not transicao_status_homologacao_e_valida(
        status_atual,
        novo_status,
    ):
        raise ValueError(
            "A transição para Instalação Concluída "
            "não é permitida."
        )

    operacoes_candidatas[
        "instalacao"
    ] = instalacao_candidata

    validar_operacoes_campo(
        operacoes_candidatas
    )

    movimentacao = (
        criar_movimentacao_instalacao_concluida(
            movimentacoes=(
                homologacao["movimentacoes"]
            ),
            instalacao=instalacao_candidata,
            status_anterior=status_atual,
            novo_status=novo_status,
            data_movimentacao=(
                data_movimentacao_normalizada
            ),
            responsavel=(
                responsavel_normalizado
            ),
        )
    )

    # ---------------------------------------------------------
    # APLICAÇÃO ATÔMICA
    # ---------------------------------------------------------

    homologacao["operacoes_campo"] = (
        operacoes_candidatas
    )

    homologacao["status"] = (
        novo_status.value
    )

    homologacao["responsavel_atual"] = (
        responsavel_normalizado
    )

    homologacao["movimentacoes"].append(
        movimentacao
    )

    return homologacao

def solicitar_vistoria(
    homologacao: dict,
    data_solicitacao: str,
    responsavel_solicitacao: str,
    protocolo: str,
    data_movimentacao: str,
    observacoes: str | None = None,
) -> dict:
    """
    Registra uma nova solicitação de Vistoria.

    A operação:

    1. valida a estrutura da Homologação;
    2. impede operações em estados terminais;
    3. exige um estado compatível;
    4. prepara uma cópia das Operações de Campo;
    5. verifica a tentativa anterior, quando existente;
    6. gera código e número sequencial;
    7. cria e valida a nova Vistoria;
    8. valida a transição do estado geral;
    9. prepara a Movimentação;
    10. aplica todas as alterações de forma atômica;
    11. atualiza o responsável atual.

    Estados admitidos:

    - INSTALACAO_CONCLUIDA:
      primeira solicitação;

    - CORRECAO_POS_VISTORIA:
      nova tentativa após reprovação e correção.
    """

    _validar_estrutura_homologacao(
        homologacao
    )

    status_atual = (
        _validar_homologacao_nao_terminal(
            homologacao=homologacao,
            mensagem_erro=(
                "Não é possível solicitar Vistoria "
                "para uma Homologação em estado terminal."
            ),
        )
    )

    estados_permitidos = {
        StatusHomologacao
        .INSTALACAO_CONCLUIDA,

        StatusHomologacao
        .CORRECAO_POS_VISTORIA,
    }

    if status_atual not in estados_permitidos:
        raise ValueError(
            "A Vistoria somente pode ser solicitada "
            "após a conclusão da Instalação ou após "
            "uma correção pós-vistoria."
        )

    operacoes_candidatas = (
        _preparar_operacoes_campo_candidatas(
            homologacao
        )
    )

    vistorias_candidatas = (
        operacoes_candidatas["vistorias"]
    )

    ultima_vistoria = buscar_ultima_vistoria(
        vistorias_candidatas
    )

    if (
        status_atual
        == StatusHomologacao
        .INSTALACAO_CONCLUIDA
        and ultima_vistoria is not None
    ):
        raise ValueError(
            "A primeira Vistoria da Homologação "
            "já foi registrada."
        )

    if (
        status_atual
        == StatusHomologacao
        .CORRECAO_POS_VISTORIA
    ):
        if ultima_vistoria is None:
            raise ValueError(
                "Não existe Vistoria anterior "
                "para a nova solicitação."
            )

        validar_vistoria(
            ultima_vistoria
        )

        if (
            ultima_vistoria.get("status")
            != StatusVistoria.REPROVADA.value
        ):
            raise ValueError(
                "Uma nova Vistoria somente pode ser "
                "solicitada após uma tentativa reprovada."
            )

    codigo_vistoria = (
        gerar_proximo_codigo_vistoria(
            vistorias_candidatas
        )
    )

    numero_sequencial = (
        gerar_proximo_numero_sequencial_vistoria(
            vistorias_candidatas
        )
    )

    vistoria_candidata = (
        criar_dados_vistoria_solicitada(
            codigo=codigo_vistoria,
            numero_sequencial=(
                numero_sequencial
            ),
            data_solicitacao=(
                data_solicitacao
            ),
            responsavel_solicitacao=(
                responsavel_solicitacao
            ),
            protocolo=protocolo,
            observacoes=observacoes,
        )
    )

    validar_vistoria(
        vistoria_candidata
    )

    data_movimentacao_normalizada = (
        _validar_data_iso(
            data_movimentacao,
            "Data da movimentação",
        ).isoformat()
    )

    responsavel_normalizado = (
        _validar_texto_obrigatorio(
            responsavel_solicitacao,
            "Responsável pela solicitação",
        )
    )

    novo_status = (
        StatusHomologacao
        .VISTORIA_SOLICITADA
    )

    if not transicao_status_homologacao_e_valida(
        status_atual,
        novo_status,
    ):
        raise ValueError(
            "A transição para Vistoria Solicitada "
            "não é permitida."
        )

    vistorias_candidatas.append(
        vistoria_candidata
    )

    validar_operacoes_campo(
        operacoes_candidatas
    )

    movimentacao = (
        criar_movimentacao_vistoria_solicitada(
            movimentacoes=(
                homologacao["movimentacoes"]
            ),
            vistoria=vistoria_candidata,
            status_anterior=status_atual,
            novo_status=novo_status,
            data_movimentacao=(
                data_movimentacao_normalizada
            ),
            responsavel=(
                responsavel_normalizado
            ),
        )
    )

    # ---------------------------------------------------------
    # APLICAÇÃO ATÔMICA
    # ---------------------------------------------------------

    homologacao["operacoes_campo"] = (
        operacoes_candidatas
    )

    homologacao["status"] = (
        novo_status.value
    )

    homologacao["responsavel_atual"] = (
        responsavel_normalizado
    )

    homologacao["movimentacoes"].append(
        movimentacao
    )

    return homologacao

def agendar_vistoria(
    homologacao: dict,
    codigo_vistoria: int,
    data_agendamento: str,
    responsavel_agendamento: str,
    data_movimentacao: str,
    observacoes: str | None = None,
) -> dict:
    """
    Registra o agendamento de uma Vistoria.

    A operação:

    1. valida a estrutura da Homologação;
    2. impede operações em estados terminais;
    3. exige o status VISTORIA_SOLICITADA;
    4. prepara uma cópia das Operações de Campo;
    5. localiza a Vistoria pelo código;
    6. exige que ela seja a tentativa mais recente;
    7. prepara e valida a Vistoria candidata;
    8. valida a transição do estado geral;
    9. prepara a Movimentação;
    10. aplica todas as alterações de forma atômica;
    11. atualiza o responsável atual.
    """

    _validar_estrutura_homologacao(
        homologacao
    )

    status_atual = (
        _validar_homologacao_nao_terminal(
            homologacao=homologacao,
            mensagem_erro=(
                "Não é possível agendar Vistoria "
                "para uma Homologação em estado terminal."
            ),
        )
    )

    if (
        status_atual
        != StatusHomologacao
        .VISTORIA_SOLICITADA
    ):
        raise ValueError(
            "A Vistoria somente pode ser agendada "
            "quando a Homologação estiver com uma "
            "solicitação de Vistoria aberta."
        )

    operacoes_candidatas = (
        _preparar_operacoes_campo_candidatas(
            homologacao
        )
    )

    vistorias_candidatas = (
        operacoes_candidatas["vistorias"]
    )

    vistoria_atual = buscar_vistoria_por_codigo(
        vistorias_candidatas,
        codigo_vistoria,
    )

    if vistoria_atual is None:
        raise ValueError(
            "Vistoria com código "
            f"{codigo_vistoria} não encontrada."
        )

    ultima_vistoria = buscar_ultima_vistoria(
        vistorias_candidatas
    )

    if (
        ultima_vistoria is None
        or ultima_vistoria.get("codigo")
        != codigo_vistoria
    ):
        raise ValueError(
            "Somente a Vistoria mais recente "
            "pode ser agendada."
        )

    vistoria_candidata = (
        preparar_agendamento_vistoria(
            vistoria=vistoria_atual,
            data_agendamento=data_agendamento,
            responsavel_agendamento=(
                responsavel_agendamento
            ),
            observacoes=observacoes,
        )
    )

    data_movimentacao_normalizada = (
        _validar_data_iso(
            data_movimentacao,
            "Data da movimentação",
        ).isoformat()
    )

    responsavel_normalizado = (
        _validar_texto_obrigatorio(
            responsavel_agendamento,
            "Responsável pelo agendamento",
        )
    )

    novo_status = (
        StatusHomologacao
        .AGUARDANDO_VISTORIA
    )

    if not transicao_status_homologacao_e_valida(
        status_atual,
        novo_status,
    ):
        raise ValueError(
            "A transição para Aguardando Vistoria "
            "não é permitida."
        )

    indice_vistoria = next(
        indice
        for indice, vistoria in enumerate(
            vistorias_candidatas
        )
        if vistoria.get("codigo")
        == codigo_vistoria
    )

    vistorias_candidatas[
        indice_vistoria
    ] = vistoria_candidata

    validar_operacoes_campo(
        operacoes_candidatas
    )

    movimentacao = (
        criar_movimentacao_vistoria_agendada(
            movimentacoes=(
                homologacao["movimentacoes"]
            ),
            vistoria=vistoria_candidata,
            status_anterior=status_atual,
            novo_status=novo_status,
            data_movimentacao=(
                data_movimentacao_normalizada
            ),
            responsavel=(
                responsavel_normalizado
            ),
        )
    )

    # ---------------------------------------------------------
    # APLICAÇÃO ATÔMICA
    # ---------------------------------------------------------

    homologacao["operacoes_campo"] = (
        operacoes_candidatas
    )

    homologacao["status"] = (
        novo_status.value
    )

    homologacao["responsavel_atual"] = (
        responsavel_normalizado
    )

    homologacao["movimentacoes"].append(
        movimentacao
    )

    return homologacao

def registrar_realizacao_vistoria(
    homologacao: dict,
    codigo_vistoria: int,
    data_realizacao: str,
    responsavel_realizacao: str,
    data_movimentacao: str,
    observacoes: str | None = None,
) -> dict:
    """
    Registra a realização de uma Vistoria.

    A operação:

    1. valida a estrutura da Homologação;
    2. impede operações em estados terminais;
    3. exige o status AGUARDANDO_VISTORIA;
    4. prepara uma cópia das Operações de Campo;
    5. localiza a Vistoria;
    6. exige que ela seja a tentativa mais recente;
    7. prepara e valida a Vistoria candidata;
    8. prepara a Movimentação;
    9. aplica as alterações de forma atômica;
    10. atualiza o responsável atual.

    O estado geral da Homologação permanece
    AGUARDANDO_VISTORIA.
    """

    _validar_estrutura_homologacao(
        homologacao
    )

    status_atual = (
        _validar_homologacao_nao_terminal(
            homologacao=homologacao,
            mensagem_erro=(
                "Não é possível registrar a realização "
                "de uma Vistoria em Homologação terminal."
            ),
        )
    )

    if (
        status_atual
        != StatusHomologacao
        .AGUARDANDO_VISTORIA
    ):
        raise ValueError(
            "A realização somente pode ser registrada "
            "quando a Homologação estiver aguardando "
            "a Vistoria."
        )

    operacoes_candidatas = (
        _preparar_operacoes_campo_candidatas(
            homologacao
        )
    )

    vistorias_candidatas = (
        operacoes_candidatas["vistorias"]
    )

    vistoria_atual = buscar_vistoria_por_codigo(
        vistorias_candidatas,
        codigo_vistoria,
    )

    if vistoria_atual is None:
        raise ValueError(
            "Vistoria com código "
            f"{codigo_vistoria} não encontrada."
        )

    ultima_vistoria = buscar_ultima_vistoria(
        vistorias_candidatas
    )

    if (
        ultima_vistoria is None
        or ultima_vistoria.get("codigo")
        != codigo_vistoria
    ):
        raise ValueError(
            "Somente a Vistoria mais recente "
            "pode receber o registro de realização."
        )

    vistoria_candidata = (
        preparar_realizacao_vistoria(
            vistoria=vistoria_atual,
            data_realizacao=data_realizacao,
            responsavel_realizacao=(
                responsavel_realizacao
            ),
            observacoes=observacoes,
        )
    )

    data_movimentacao_normalizada = (
        _validar_data_iso(
            data_movimentacao,
            "Data da movimentação",
        ).isoformat()
    )

    responsavel_normalizado = (
        _validar_texto_obrigatorio(
            responsavel_realizacao,
            "Responsável pela realização",
        )
    )

    indice_vistoria = next(
        indice
        for indice, vistoria in enumerate(
            vistorias_candidatas
        )
        if vistoria.get("codigo")
        == codigo_vistoria
    )

    vistorias_candidatas[
        indice_vistoria
    ] = vistoria_candidata

    validar_operacoes_campo(
        operacoes_candidatas
    )

    movimentacao = (
        criar_movimentacao_vistoria_realizada(
            movimentacoes=(
                homologacao["movimentacoes"]
            ),
            vistoria=vistoria_candidata,
            data_movimentacao=(
                data_movimentacao_normalizada
            ),
            responsavel=(
                responsavel_normalizado
            ),
        )
    )

    # ---------------------------------------------------------
    # APLICAÇÃO ATÔMICA
    # ---------------------------------------------------------

    homologacao["operacoes_campo"] = (
        operacoes_candidatas
    )

    homologacao["responsavel_atual"] = (
        responsavel_normalizado
    )

    homologacao["movimentacoes"].append(
        movimentacao
    )

    return homologacao

def aprovar_vistoria(
    homologacao: dict,
    codigo_vistoria: int,
    data_resultado: str,
    responsavel_resultado: str,
    data_movimentacao: str,
    observacoes: str | None = None,
) -> dict:
    """
    Registra a aprovação formal de uma Vistoria.

    A operação exige:

    - Homologação em AGUARDANDO_VISTORIA;
    - Vistoria existente;
    - tentativa mais recente;
    - Vistoria local em estado REALIZADA.

    A Homologação avança para VISTORIA_APROVADA.
    """

    _validar_estrutura_homologacao(
        homologacao
    )

    status_atual = (
        _validar_homologacao_nao_terminal(
            homologacao=homologacao,
            mensagem_erro=(
                "Não é possível aprovar Vistoria "
                "em uma Homologação terminal."
            ),
        )
    )

    if (
        status_atual
        != StatusHomologacao
        .AGUARDANDO_VISTORIA
    ):
        raise ValueError(
            "A aprovação somente pode ser registrada "
            "quando a Homologação estiver aguardando "
            "o resultado da Vistoria."
        )

    operacoes_candidatas = (
        _preparar_operacoes_campo_candidatas(
            homologacao
        )
    )

    vistorias_candidatas = (
        operacoes_candidatas["vistorias"]
    )

    vistoria_atual = buscar_vistoria_por_codigo(
        vistorias_candidatas,
        codigo_vistoria,
    )

    if vistoria_atual is None:
        raise ValueError(
            "Vistoria com código "
            f"{codigo_vistoria} não encontrada."
        )

    ultima_vistoria = buscar_ultima_vistoria(
        vistorias_candidatas
    )

    if (
        ultima_vistoria is None
        or ultima_vistoria.get("codigo")
        != codigo_vistoria
    ):
        raise ValueError(
            "Somente a Vistoria mais recente "
            "pode receber um resultado."
        )

    vistoria_candidata = (
        preparar_aprovacao_vistoria(
            vistoria=vistoria_atual,
            data_resultado=data_resultado,
            responsavel_resultado=(
                responsavel_resultado
            ),
            observacoes=observacoes,
        )
    )

    data_movimentacao_normalizada = (
        _validar_data_iso(
            data_movimentacao,
            "Data da movimentação",
        ).isoformat()
    )

    responsavel_normalizado = (
        _validar_texto_obrigatorio(
            responsavel_resultado,
            "Responsável pelo resultado",
        )
    )

    novo_status = (
        StatusHomologacao
        .VISTORIA_APROVADA
    )

    if not transicao_status_homologacao_e_valida(
        status_atual,
        novo_status,
    ):
        raise ValueError(
            "A transição para Vistoria Aprovada "
            "não é permitida."
        )

    indice_vistoria = next(
        indice
        for indice, vistoria in enumerate(
            vistorias_candidatas
        )
        if vistoria.get("codigo")
        == codigo_vistoria
    )

    vistorias_candidatas[
        indice_vistoria
    ] = vistoria_candidata

    validar_operacoes_campo(
        operacoes_candidatas
    )

    movimentacao = (
        criar_movimentacao_vistoria_aprovada(
            movimentacoes=(
                homologacao["movimentacoes"]
            ),
            vistoria=vistoria_candidata,
            status_anterior=status_atual,
            novo_status=novo_status,
            data_movimentacao=(
                data_movimentacao_normalizada
            ),
            responsavel=(
                responsavel_normalizado
            ),
        )
    )

    # ---------------------------------------------------------
    # APLICAÇÃO ATÔMICA
    # ---------------------------------------------------------

    homologacao["operacoes_campo"] = (
        operacoes_candidatas
    )

    homologacao["status"] = (
        novo_status.value
    )

    homologacao["responsavel_atual"] = (
        responsavel_normalizado
    )

    homologacao["movimentacoes"].append(
        movimentacao
    )

    return homologacao

def reprovar_vistoria(
    homologacao: dict,
    codigo_vistoria: int,
    data_resultado: str,
    responsavel_resultado: str,
    motivo_reprovacao: str,
    data_movimentacao: str,
    observacoes: str | None = None,
) -> dict:
    """
    Registra a reprovação formal de uma Vistoria.

    A reprovação exige motivo obrigatório.

    A Homologação avança para VISTORIA_REPROVADA.
    """

    _validar_estrutura_homologacao(
        homologacao
    )

    status_atual = (
        _validar_homologacao_nao_terminal(
            homologacao=homologacao,
            mensagem_erro=(
                "Não é possível reprovar Vistoria "
                "em uma Homologação terminal."
            ),
        )
    )

    if (
        status_atual
        != StatusHomologacao
        .AGUARDANDO_VISTORIA
    ):
        raise ValueError(
            "A reprovação somente pode ser registrada "
            "quando a Homologação estiver aguardando "
            "o resultado da Vistoria."
        )

    operacoes_candidatas = (
        _preparar_operacoes_campo_candidatas(
            homologacao
        )
    )

    vistorias_candidatas = (
        operacoes_candidatas["vistorias"]
    )

    vistoria_atual = buscar_vistoria_por_codigo(
        vistorias_candidatas,
        codigo_vistoria,
    )

    if vistoria_atual is None:
        raise ValueError(
            "Vistoria com código "
            f"{codigo_vistoria} não encontrada."
        )

    ultima_vistoria = buscar_ultima_vistoria(
        vistorias_candidatas
    )

    if (
        ultima_vistoria is None
        or ultima_vistoria.get("codigo")
        != codigo_vistoria
    ):
        raise ValueError(
            "Somente a Vistoria mais recente "
            "pode receber um resultado."
        )

    vistoria_candidata = (
        preparar_reprovacao_vistoria(
            vistoria=vistoria_atual,
            data_resultado=data_resultado,
            responsavel_resultado=(
                responsavel_resultado
            ),
            motivo_reprovacao=(
                motivo_reprovacao
            ),
            observacoes=observacoes,
        )
    )

    data_movimentacao_normalizada = (
        _validar_data_iso(
            data_movimentacao,
            "Data da movimentação",
        ).isoformat()
    )

    responsavel_normalizado = (
        _validar_texto_obrigatorio(
            responsavel_resultado,
            "Responsável pelo resultado",
        )
    )

    novo_status = (
        StatusHomologacao
        .VISTORIA_REPROVADA
    )

    if not transicao_status_homologacao_e_valida(
        status_atual,
        novo_status,
    ):
        raise ValueError(
            "A transição para Vistoria Reprovada "
            "não é permitida."
        )

    indice_vistoria = next(
        indice
        for indice, vistoria in enumerate(
            vistorias_candidatas
        )
        if vistoria.get("codigo")
        == codigo_vistoria
    )

    vistorias_candidatas[
        indice_vistoria
    ] = vistoria_candidata

    validar_operacoes_campo(
        operacoes_candidatas
    )

    movimentacao = (
        criar_movimentacao_vistoria_reprovada(
            movimentacoes=(
                homologacao["movimentacoes"]
            ),
            vistoria=vistoria_candidata,
            status_anterior=status_atual,
            novo_status=novo_status,
            data_movimentacao=(
                data_movimentacao_normalizada
            ),
            responsavel=(
                responsavel_normalizado
            ),
        )
    )

    # ---------------------------------------------------------
    # APLICAÇÃO ATÔMICA
    # ---------------------------------------------------------

    homologacao["operacoes_campo"] = (
        operacoes_candidatas
    )

    homologacao["status"] = (
        novo_status.value
    )

    homologacao["responsavel_atual"] = (
        responsavel_normalizado
    )

    homologacao["movimentacoes"].append(
        movimentacao
    )

    return homologacao

def registrar_correcao_pos_vistoria(
    homologacao: dict,
    codigo_vistoria: int,
    descricao_correcao: str,
    responsavel_correcao: str,
    data_movimentacao: str,
) -> dict:
    """
    Registra a correção realizada após
    uma Vistoria reprovada.

    A Vistoria reprovada permanece intacta
    no histórico.

    A Homologação avança para
    CORRECAO_POS_VISTORIA.
    """

    _validar_estrutura_homologacao(
        homologacao
    )

    status_atual = (
        _validar_homologacao_nao_terminal(
            homologacao=homologacao,
            mensagem_erro=(
                "Não é possível registrar correção "
                "em uma Homologação terminal."
            ),
        )
    )

    if (
        status_atual
        != StatusHomologacao
        .VISTORIA_REPROVADA
    ):
        raise ValueError(
            "A correção pós-vistoria somente pode "
            "ser registrada após uma Vistoria reprovada."
        )

    operacoes_candidatas = (
        _preparar_operacoes_campo_candidatas(
            homologacao
        )
    )

    vistorias_candidatas = (
        operacoes_candidatas["vistorias"]
    )

    vistoria = buscar_vistoria_por_codigo(
        vistorias_candidatas,
        codigo_vistoria,
    )

    if vistoria is None:
        raise ValueError(
            "Vistoria com código "
            f"{codigo_vistoria} não encontrada."
        )

    ultima_vistoria = buscar_ultima_vistoria(
        vistorias_candidatas
    )

    if (
        ultima_vistoria is None
        or ultima_vistoria.get("codigo")
        != codigo_vistoria
    ):
        raise ValueError(
            "Somente a Vistoria mais recente "
            "pode receber uma correção."
        )

    validar_vistoria(
        vistoria
    )

    if (
        vistoria.get("status")
        != StatusVistoria.REPROVADA.value
    ):
        raise ValueError(
            "A correção exige uma Vistoria "
            "localmente reprovada."
        )

    descricao_normalizada = (
        _validar_texto_obrigatorio(
            descricao_correcao,
            "Descrição da correção",
        )
    )

    responsavel_normalizado = (
        _validar_texto_obrigatorio(
            responsavel_correcao,
            "Responsável pela correção",
        )
    )

    data_movimentacao_normalizada = (
        _validar_data_iso(
            data_movimentacao,
            "Data da movimentação",
        ).isoformat()
    )

    novo_status = (
        StatusHomologacao
        .CORRECAO_POS_VISTORIA
    )

    if not transicao_status_homologacao_e_valida(
        status_atual,
        novo_status,
    ):
        raise ValueError(
            "A transição para Correção Pós-Vistoria "
            "não é permitida."
        )

    movimentacao = (
        criar_movimentacao_correcao_pos_vistoria(
            movimentacoes=(
                homologacao["movimentacoes"]
            ),
            vistoria=vistoria,
            status_anterior=status_atual,
            novo_status=novo_status,
            data_movimentacao=(
                data_movimentacao_normalizada
            ),
            responsavel=(
                responsavel_normalizado
            ),
            descricao_correcao=(
                descricao_normalizada
            ),
        )
    )

    # ---------------------------------------------------------
    # APLICAÇÃO ATÔMICA
    # ---------------------------------------------------------

    homologacao["status"] = (
        novo_status.value
    )

    homologacao["responsavel_atual"] = (
        responsavel_normalizado
    )

    homologacao["movimentacoes"].append(
        movimentacao
    )

    return homologacao

# ============================================================
# LIGAÇÃO E ENERGIZAÇÃO
# ============================================================

def solicitar_ligacao(
    homologacao: dict,
    data_solicitacao: str,
    responsavel_solicitacao: str,
    protocolo: str,
    data_movimentacao: str,
    observacoes: str | None = None,
) -> dict:
    """
    Registra a solicitação da Ligação e Energização.

    A operação:

    1. valida a estrutura da Homologação;
    2. impede operações em estados terminais;
    3. exige VISTORIA_APROVADA;
    4. prepara uma cópia das Operações de Campo;
    5. impede uma segunda Ligação;
    6. cria e valida a Ligação candidata;
    7. valida a transição para AGUARDANDO_LIGACAO;
    8. prepara a Movimentação;
    9. aplica as alterações de forma atômica;
    10. atualiza o responsável atual.
    """

    _validar_estrutura_homologacao(
        homologacao
    )

    status_atual = (
        _validar_homologacao_nao_terminal(
            homologacao=homologacao,
            mensagem_erro=(
                "Não é possível solicitar Ligação "
                "em uma Homologação terminal."
            ),
        )
    )

    if (
        status_atual
        != StatusHomologacao
        .VISTORIA_APROVADA
    ):
        raise ValueError(
            "A Ligação somente pode ser solicitada "
            "após a aprovação da Vistoria."
        )

    operacoes_candidatas = (
        _preparar_operacoes_campo_candidatas(
            homologacao
        )
    )

    if (
        operacoes_candidatas.get("ligacao")
        is not None
    ):
        raise ValueError(
            "A Homologação já possui "
            "uma Ligação registrada."
        )

    ligacao_candidata = (
        criar_dados_ligacao_solicitada(
            data_solicitacao=data_solicitacao,
            responsavel_solicitacao=(
                responsavel_solicitacao
            ),
            protocolo=protocolo,
            observacoes=observacoes,
        )
    )

    validar_ligacao(
        ligacao_candidata
    )

    data_movimentacao_normalizada = (
        _validar_data_iso(
            data_movimentacao,
            "Data da movimentação",
        ).isoformat()
    )

    responsavel_normalizado = (
        _validar_texto_obrigatorio(
            responsavel_solicitacao,
            "Responsável pela solicitação",
        )
    )

    novo_status = (
        StatusHomologacao
        .AGUARDANDO_LIGACAO
    )

    if not transicao_status_homologacao_e_valida(
        status_atual,
        novo_status,
    ):
        raise ValueError(
            "A transição para Aguardando Ligação "
            "não é permitida."
        )

    operacoes_candidatas["ligacao"] = (
        ligacao_candidata
    )

    validar_operacoes_campo(
        operacoes_candidatas
    )

    movimentacao = (
        criar_movimentacao_ligacao_solicitada(
            movimentacoes=(
                homologacao["movimentacoes"]
            ),
            ligacao=ligacao_candidata,
            status_anterior=status_atual,
            novo_status=novo_status,
            data_movimentacao=(
                data_movimentacao_normalizada
            ),
            responsavel=(
                responsavel_normalizado
            ),
        )
    )

    # ---------------------------------------------------------
    # APLICAÇÃO ATÔMICA
    # ---------------------------------------------------------

    homologacao["operacoes_campo"] = (
        operacoes_candidatas
    )

    homologacao["status"] = (
        novo_status.value
    )

    homologacao["responsavel_atual"] = (
        responsavel_normalizado
    )

    homologacao["movimentacoes"].append(
        movimentacao
    )

    return homologacao

def agendar_ligacao(
    homologacao: dict,
    data_agendamento: str,
    responsavel_agendamento: str,
    data_movimentacao: str,
    observacoes: str | None = None,
) -> dict:
    """
    Registra o agendamento da Ligação.

    O estado geral da Homologação permanece
    AGUARDANDO_LIGACAO.
    """

    _validar_estrutura_homologacao(
        homologacao
    )

    status_atual = (
        _validar_homologacao_nao_terminal(
            homologacao=homologacao,
            mensagem_erro=(
                "Não é possível agendar Ligação "
                "em uma Homologação terminal."
            ),
        )
    )

    if (
        status_atual
        != StatusHomologacao
        .AGUARDANDO_LIGACAO
    ):
        raise ValueError(
            "A Ligação somente pode ser agendada "
            "quando a Homologação estiver "
            "aguardando Ligação."
        )

    operacoes_candidatas = (
        _preparar_operacoes_campo_candidatas(
            homologacao
        )
    )

    ligacao_atual = operacoes_candidatas.get(
        "ligacao"
    )

    if ligacao_atual is None:
        raise ValueError(
            "Nenhuma Ligação foi solicitada "
            "para a Homologação."
        )

    validar_ligacao(
        ligacao_atual
    )

    ligacao_candidata = (
        preparar_agendamento_ligacao(
            ligacao=ligacao_atual,
            data_agendamento=data_agendamento,
            responsavel_agendamento=(
                responsavel_agendamento
            ),
            observacoes=observacoes,
        )
    )

    data_movimentacao_normalizada = (
        _validar_data_iso(
            data_movimentacao,
            "Data da movimentação",
        ).isoformat()
    )

    responsavel_normalizado = (
        _validar_texto_obrigatorio(
            responsavel_agendamento,
            "Responsável pelo agendamento",
        )
    )

    operacoes_candidatas["ligacao"] = (
        ligacao_candidata
    )

    validar_operacoes_campo(
        operacoes_candidatas
    )

    movimentacao = (
        criar_movimentacao_ligacao_agendada(
            movimentacoes=(
                homologacao["movimentacoes"]
            ),
            ligacao=ligacao_candidata,
            data_movimentacao=(
                data_movimentacao_normalizada
            ),
            responsavel=(
                responsavel_normalizado
            ),
        )
    )

    # ---------------------------------------------------------
    # APLICAÇÃO ATÔMICA
    # ---------------------------------------------------------

    homologacao["operacoes_campo"] = (
        operacoes_candidatas
    )

    homologacao["responsavel_atual"] = (
        responsavel_normalizado
    )

    homologacao["movimentacoes"].append(
        movimentacao
    )

    return homologacao

def concluir_ligacao(
    homologacao: dict,
    data_ligacao: str,
    responsavel_ligacao: str,
    data_movimentacao: str,
    observacoes: str | None = None,
) -> dict:
    """
    Registra a conclusão da Ligação
    e a Energização do sistema.

    A Homologação avança de
    AGUARDANDO_LIGACAO para SISTEMA_LIGADO.
    """

    _validar_estrutura_homologacao(
        homologacao
    )

    status_atual = (
        _validar_homologacao_nao_terminal(
            homologacao=homologacao,
            mensagem_erro=(
                "Não é possível concluir Ligação "
                "em uma Homologação terminal."
            ),
        )
    )

    if (
        status_atual
        != StatusHomologacao
        .AGUARDANDO_LIGACAO
    ):
        raise ValueError(
            "A conclusão da Ligação somente pode "
            "ser registrada quando a Homologação "
            "estiver aguardando Ligação."
        )

    operacoes_candidatas = (
        _preparar_operacoes_campo_candidatas(
            homologacao
        )
    )

    ligacao_atual = operacoes_candidatas.get(
        "ligacao"
    )

    if ligacao_atual is None:
        raise ValueError(
            "Nenhuma Ligação foi registrada "
            "para a Homologação."
        )

    validar_ligacao(
        ligacao_atual
    )

    ligacao_candidata = (
        preparar_conclusao_ligacao(
            ligacao=ligacao_atual,
            data_ligacao=data_ligacao,
            responsavel_ligacao=(
                responsavel_ligacao
            ),
            observacoes=observacoes,
        )
    )

    data_movimentacao_normalizada = (
        _validar_data_iso(
            data_movimentacao,
            "Data da movimentação",
        ).isoformat()
    )

    responsavel_normalizado = (
        _validar_texto_obrigatorio(
            responsavel_ligacao,
            "Responsável pela Ligação",
        )
    )

    novo_status = (
        StatusHomologacao
        .SISTEMA_LIGADO
    )

    if not transicao_status_homologacao_e_valida(
        status_atual,
        novo_status,
    ):
        raise ValueError(
            "A transição para Sistema Ligado "
            "não é permitida."
        )

    operacoes_candidatas["ligacao"] = (
        ligacao_candidata
    )

    validar_operacoes_campo(
        operacoes_candidatas
    )

    movimentacao = (
        criar_movimentacao_ligacao_concluida(
            movimentacoes=(
                homologacao["movimentacoes"]
            ),
            ligacao=ligacao_candidata,
            status_anterior=status_atual,
            novo_status=novo_status,
            data_movimentacao=(
                data_movimentacao_normalizada
            ),
            responsavel=(
                responsavel_normalizado
            ),
        )
    )

    # ---------------------------------------------------------
    # APLICAÇÃO ATÔMICA
    # ---------------------------------------------------------

    homologacao["operacoes_campo"] = (
        operacoes_candidatas
    )

    homologacao["status"] = (
        novo_status.value
    )

    homologacao["responsavel_atual"] = (
        responsavel_normalizado
    )

    homologacao["movimentacoes"].append(
        movimentacao
    )

    return homologacao

# ============================================================
# ENCERRAMENTO DA HOMOLOGAÇÃO
# ============================================================

def homologacao_pode_ser_concluida(
    homologacao: dict,
) -> bool:
    """
    Informa se a Homologação atende às condições
    necessárias para seu encerramento formal.

    Para ser concluída, a Homologação deve:

    - estar em SISTEMA_LIGADO;
    - possuir Ligação registrada;
    - possuir Ligação localmente CONCLUIDA;
    - não possuir Exigências abertas.
    """

    _validar_estrutura_homologacao(
        homologacao
    )

    status_atual = _converter_status_homologacao(
        homologacao.get("status")
    )

    if (
        status_atual
        != StatusHomologacao.SISTEMA_LIGADO
    ):
        return False

    operacoes_campo = homologacao.get(
        "operacoes_campo"
    )

    if operacoes_campo is None:
        return False

    validar_operacoes_campo(
        operacoes_campo
    )

    ligacao = operacoes_campo.get(
        "ligacao"
    )

    if ligacao is None:
        return False

    validar_ligacao(
        ligacao
    )

    if (
        ligacao.get("status")
        != StatusLigacao.CONCLUIDA.value
    ):
        return False

    if homologacao_possui_exigencia_aberta(
        homologacao
    ):
        return False

    return True

def concluir_homologacao(
    homologacao: dict,
    data_conclusao: str,
    responsavel_conclusao: str,
    observacoes: str | None = None,
) -> dict:
    """
    Encerra formalmente uma Homologação.

    A operação somente é permitida quando:

    - o sistema já estiver ligado;
    - a Ligação estiver concluída;
    - não existirem Exigências abertas.

    O encerramento:

    - altera o estado para CONCLUIDA;
    - registra data_conclusao_real;
    - atualiza o responsável atual;
    - registra uma Movimentação.
    """

    _validar_estrutura_homologacao(
        homologacao
    )

    status_atual = (
        _validar_homologacao_nao_terminal(
            homologacao=homologacao,
            mensagem_erro=(
                "Não é possível concluir uma "
                "Homologação em estado terminal."
            ),
        )
    )

    if (
        status_atual
        != StatusHomologacao.SISTEMA_LIGADO
    ):
        raise ValueError(
            "A Homologação somente pode ser concluída "
            "quando o sistema estiver ligado."
        )

    operacoes_campo = homologacao.get(
        "operacoes_campo"
    )

    if operacoes_campo is None:
        raise ValueError(
            "A Homologação não possui "
            "Operações de Campo registradas."
        )

    validar_operacoes_campo(
        operacoes_campo
    )

    ligacao = operacoes_campo.get(
        "ligacao"
    )

    if ligacao is None:
        raise ValueError(
            "A Homologação não possui "
            "Ligação registrada."
        )

    validar_ligacao(
        ligacao
    )

    if (
        ligacao.get("status")
        != StatusLigacao.CONCLUIDA.value
    ):
        raise ValueError(
            "A Homologação somente pode ser concluída "
            "após a conclusão da Ligação."
        )

    if homologacao_possui_exigencia_aberta(
        homologacao
    ):
        raise ValueError(
            "A Homologação não pode ser concluída "
            "enquanto possuir Exigências abertas."
        )

    data_normalizada = (
        _validar_data_iso(
            data_conclusao,
            "Data de conclusão da Homologação",
        ).isoformat()
    )

    responsavel_normalizado = (
        _validar_texto_obrigatorio(
            responsavel_conclusao,
            "Responsável pela conclusão",
        )
    )

    if observacoes is None:
        observacoes_normalizadas = None

    elif not isinstance(
        observacoes,
        str,
    ):
        raise TypeError(
            "Observações da conclusão "
            "devem ser um texto ou None."
        )

    else:
        observacoes_normalizadas = (
            observacoes.strip() or None
        )

    return alterar_status_homologacao(
        homologacao=homologacao,
        novo_status=StatusHomologacao.CONCLUIDA,
        data_movimentacao=data_normalizada,
        responsavel=responsavel_normalizado,
        descricao=(
            observacoes_normalizadas
            or "Homologação concluída após "
            "Ligação e Energização do sistema."
        ),
    )
