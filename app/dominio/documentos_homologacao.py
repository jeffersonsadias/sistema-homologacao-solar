"""
Regras locais dos Documentos da Homologação.

Este módulo é responsável por:

- definir as origens possíveis de um Documento;
- definir as regras de visibilidade;
- definir os estados documentais;
- definir as transições permitidas;
- criar a estrutura local de um Documento;
- buscar Documentos;
- verificar a existência de códigos;
- listar Documentos visíveis ao cliente;
- fornecer rótulos e consultas da máquina documental.

Este módulo não é responsável por:

- salvar arquivos físicos;
- persistir dados em JSON;
- interagir com o usuário;
- adicionar diretamente Documentos à Homologação;
- coordenar o versionamento dentro do agregado;
- registrar Movimentações;
- modificar diretamente coleções pertencentes a outros módulos.

A inclusão, a alteração de status e o versionamento coordenado dos
Documentos pertencem ao Aggregate Root:

    app/dominio/homologacoes.py
"""

from datetime import date
from enum import Enum


class OrigemDocumento(str, Enum):
    """
    Identifica de onde o documento foi recebido ou produzido.
    """

    CLIENTE = "CLIENTE"
    EMPRESA = "EMPRESA"
    CONCESSIONARIA = "CONCESSIONARIA"
    RESPONSAVEL_TECNICO = "RESPONSAVEL_TECNICO"
    SISTEMA = "SISTEMA"
    OUTRA = "OUTRA"


class VisibilidadeDocumento(str, Enum):
    """
    Define quem poderá visualizar o documento.

    Nesta primeira versão, utilizaremos dois níveis:

    INTERNA:
        documento disponível apenas no ambiente corporativo;

    CLIENTE:
        documento disponível tanto para a empresa quanto para
        o cliente final.
    """

    INTERNA = "INTERNA"
    CLIENTE = "CLIENTE"


class StatusDocumentoHomologacao(str, Enum):
    """
    Representa a situação do documento dentro da Homologação.
    """

    SOLICITADO = "SOLICITADO"
    RECEBIDO = "RECEBIDO"
    EM_VALIDACAO = "EM_VALIDACAO"
    VALIDADO = "VALIDADO"
    REJEITADO = "REJEITADO"
    SUBSTITUIDO = "SUBSTITUIDO"


ROTULOS_ORIGEM_DOCUMENTO = {
    OrigemDocumento.CLIENTE:
        "Cliente",

    OrigemDocumento.EMPRESA:
        "Empresa",

    OrigemDocumento.CONCESSIONARIA:
        "Concessionária",

    OrigemDocumento.RESPONSAVEL_TECNICO:
        "Responsável técnico",

    OrigemDocumento.SISTEMA:
        "Sistema",

    OrigemDocumento.OUTRA:
        "Outra origem",
}


ROTULOS_VISIBILIDADE_DOCUMENTO = {
    VisibilidadeDocumento.INTERNA:
        "Somente equipe interna",

    VisibilidadeDocumento.CLIENTE:
        "Disponível para o cliente",
}

ROTULOS_STATUS_DOCUMENTO = {
    StatusDocumentoHomologacao.SOLICITADO:
        "Solicitado",

    StatusDocumentoHomologacao.RECEBIDO:
        "Recebido",

    StatusDocumentoHomologacao.EM_VALIDACAO:
        "Em validação",

    StatusDocumentoHomologacao.VALIDADO:
        "Validado",

    StatusDocumentoHomologacao.REJEITADO:
        "Rejeitado",

    StatusDocumentoHomologacao.SUBSTITUIDO:
        "Substituído",
}

TRANSICOES_STATUS_DOCUMENTO = {
    StatusDocumentoHomologacao.SOLICITADO: {
        StatusDocumentoHomologacao.RECEBIDO,
    },

    StatusDocumentoHomologacao.RECEBIDO: {
        StatusDocumentoHomologacao.EM_VALIDACAO,
        StatusDocumentoHomologacao.REJEITADO,
    },

    StatusDocumentoHomologacao.EM_VALIDACAO: {
        StatusDocumentoHomologacao.VALIDADO,
        StatusDocumentoHomologacao.REJEITADO,
    },

    StatusDocumentoHomologacao.VALIDADO: {
        StatusDocumentoHomologacao.SUBSTITUIDO,
    },

    StatusDocumentoHomologacao.REJEITADO: {
        StatusDocumentoHomologacao.SUBSTITUIDO,
    },

    StatusDocumentoHomologacao.SUBSTITUIDO: set(),
}

STATUS_TERMINAIS_DOCUMENTO = {
    StatusDocumentoHomologacao.SUBSTITUIDO,
}

def _validar_codigo_inteiro_positivo(
    valor: int,
    nome_campo: str,
) -> None:
    """
    Valida códigos inteiros positivos.

    O tipo bool é rejeitado explicitamente porque, em Python,
    bool é uma especialização de int.

    Dessa forma:

        True

    não será aceito como código 1.
    """

    if isinstance(valor, bool) or not isinstance(valor, int):
        raise TypeError(
            f"{nome_campo} deve ser um número inteiro."
        )

    if valor <= 0:
        raise ValueError(
            f"{nome_campo} deve ser maior que zero."
        )

def _validar_codigo_opcional(
    valor: int | None,
    nome_campo: str,
) -> None:
    """
    Valida um código que pode ser None.

    Quando informado, o código deverá ser inteiro e positivo.
    """

    if valor is None:
        return

    _validar_codigo_inteiro_positivo(
        valor,
        nome_campo,
    )

def _validar_texto_obrigatorio(
    valor: str,
    nome_campo: str,
) -> str:
    """
    Valida e normaliza um texto obrigatório.
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

def _validar_texto_opcional(
    valor: str | None,
    nome_campo: str,
) -> str | None:
    """
    Valida e normaliza um texto opcional.

    Textos vazios serão convertidos para None.
    """

    if valor is None:
        return None

    if not isinstance(valor, str):
        raise TypeError(
            f"{nome_campo} deve ser um texto."
        )

    return valor.strip() or None

def _validar_data_iso(
    valor: str,
    nome_campo: str,
) -> str:
    """
    Valida uma data no formato AAAA-MM-DD.

    O retorno permanece como texto ISO porque essa será a forma
    utilizada na futura persistência JSON.
    """

    if not isinstance(valor, str):
        raise TypeError(
            f"{nome_campo} deve ser um texto no formato AAAA-MM-DD."
        )

    try:
        data_convertida = date.fromisoformat(valor)

    except ValueError as erro:
        raise ValueError(
            f"{nome_campo} deve estar no formato AAAA-MM-DD."
        ) from erro

    return data_convertida.isoformat()

def _converter_origem_documento(
    origem: str | OrigemDocumento,
) -> OrigemDocumento:
    """
    Converte texto ou Enum para OrigemDocumento.
    """

    if isinstance(origem, OrigemDocumento):
        return origem

    try:
        return OrigemDocumento(origem)

    except ValueError as erro:
        raise ValueError(
            f"Origem de documento inválida: {origem}"
        ) from erro

def _converter_visibilidade_documento(
    visibilidade: str | VisibilidadeDocumento,
) -> VisibilidadeDocumento:
    """
    Converte texto ou Enum para VisibilidadeDocumento.
    """

    if isinstance(
        visibilidade,
        VisibilidadeDocumento,
    ):
        return visibilidade

    try:
        return VisibilidadeDocumento(visibilidade)

    except ValueError as erro:
        raise ValueError(
            "Visibilidade de documento inválida: "
            f"{visibilidade}"
        ) from erro

def _converter_status_documento(
    status: str | StatusDocumentoHomologacao,
) -> StatusDocumentoHomologacao:
    """
    Converte texto ou Enum para StatusDocumentoHomologacao.
    """

    if isinstance(
        status,
        StatusDocumentoHomologacao,
    ):
        return status

    try:
        return StatusDocumentoHomologacao(status)

    except ValueError as erro:
        raise ValueError(
            f"Status de documento inválido: {status}"
        ) from erro

def criar_dados_documento_homologacao(
    codigo: int,
    nome: str,
    categoria: str,
    data_registro: str,
    responsavel_registro: str,
    origem: str | OrigemDocumento,
    visibilidade: (
        str | VisibilidadeDocumento
    ) = VisibilidadeDocumento.INTERNA,
    status: (
        str | StatusDocumentoHomologacao
    ) = StatusDocumentoHomologacao.SOLICITADO,
    obrigatorio: bool = False,
    referencia_arquivo: str | None = None,
    versao: int = 1,
    codigo_documento_anterior: int | None = None,
    codigo_submissao: int | None = None,
    descricao: str | None = None,
) -> dict:
    """
    Cria a estrutura de um Documento da Homologação.

    Parâmetros:
        codigo:
            Código interno do documento dentro da Homologação.

        nome:
            Nome que identifica o documento.

            Exemplo:
                Fatura de energia da Unidade Geradora

        categoria:
            Grupo funcional do documento.

            A categoria é um texto flexível porque os documentos
            variam conforme a concessionária e o tipo de projeto.

            Exemplos:
                Cliente e titular
                Unidade Consumidora
                Projeto técnico
                Parecer de acesso
                Vistoria
                Documento final

        data_registro:
            Data em que o documento foi solicitado ou registrado.

        responsavel_registro:
            Usuário que realizou o registro.

        origem:
            Parte que forneceu ou produziu o documento.

        visibilidade:
            Indica se o cliente poderá visualizá-lo.

        status:
            Situação atual do documento.

        obrigatorio:
            Informa se aquele documento foi considerado obrigatório
            especificamente para essa Homologação.

            Não representa uma lista universal de documentos
            obrigatórios.

        referencia_arquivo:
            Identificador, caminho ou referência técnica do arquivo.

            Nesta fase, o domínio não salva o arquivo físico.

        versao:
            Número da versão do documento.

        codigo_documento_anterior:
            Código da versão anterior, quando existir.

        codigo_submissao:
            Submissão à qual o documento está associado.

        descricao:
            Informações complementares.

    Retorno:
        Dicionário representando o documento.
    """

    _validar_codigo_inteiro_positivo(
        codigo,
        "Código do Documento",
    )

    nome_normalizado = _validar_texto_obrigatorio(
        nome,
        "Nome do Documento",
    )

    categoria_normalizada = _validar_texto_obrigatorio(
        categoria,
        "Categoria do Documento",
    )

    data_normalizada = _validar_data_iso(
        data_registro,
        "Data de registro",
    )

    responsavel_normalizado = _validar_texto_obrigatorio(
        responsavel_registro,
        "Responsável pelo registro",
    )

    origem_convertida = _converter_origem_documento(
        origem
    )

    visibilidade_convertida = (
        _converter_visibilidade_documento(
            visibilidade
        )
    )

    status_convertido = _converter_status_documento(
        status
    )

    if not isinstance(obrigatorio, bool):
        raise TypeError(
            "Obrigatório deve ser um valor booleano."
        )

    if isinstance(versao, bool) or not isinstance(
        versao,
        int,
    ):
        raise TypeError(
            "Versão do documento deve ser um número inteiro."
        )

    if versao <= 0:
        raise ValueError(
            "Versão do documento deve ser maior que zero."
        )

    _validar_codigo_opcional(
        codigo_documento_anterior,
        "Código do Documento anterior",
    )

    _validar_codigo_opcional(
        codigo_submissao,
        "Código da Submissão",
    )

    referencia_normalizada = _validar_texto_opcional(
        referencia_arquivo,
        "Referência do arquivo",
    )

    descricao_normalizada = _validar_texto_opcional(
        descricao,
        "Descrição",
    )

    if (
        status_convertido
        != StatusDocumentoHomologacao.SOLICITADO
        and referencia_normalizada is None
    ):
        raise ValueError(
            "Documentos recebidos, em validação, validados, "
            "rejeitados ou substituídos devem possuir uma "
            "referência de arquivo."
        )

    if (
        status_convertido
        == StatusDocumentoHomologacao.SOLICITADO
        and referencia_normalizada is not None
    ):
        raise ValueError(
            "Um documento com arquivo registrado não pode "
            "permanecer com status SOLICITADO."
        )

    if (
        versao > 1
        and codigo_documento_anterior is None
    ):
        raise ValueError(
            "Documentos com versão superior a 1 devem informar "
            "o código do documento anterior."
        )

    if (
        versao == 1
        and codigo_documento_anterior is not None
    ):
        raise ValueError(
            "A primeira versão não deve possuir documento anterior."
        )

    return {
        "codigo": codigo,
        "nome": nome_normalizado,
        "categoria": categoria_normalizada,
        "data_registro": data_normalizada,
        "responsavel_registro": responsavel_normalizado,
        "origem": origem_convertida.value,
        "visibilidade": visibilidade_convertida.value,
        "status": status_convertido.value,
        "obrigatorio": obrigatorio,
        "referencia_arquivo": referencia_normalizada,
        "versao": versao,
        "codigo_documento_anterior": (
            codigo_documento_anterior
        ),
        "codigo_submissao": codigo_submissao,
        "descricao": descricao_normalizada,
    }

def buscar_documento_por_codigo(
    documentos: list[dict],
    codigo: int,
) -> dict | None:
    """
    Busca um documento pelo código interno.
    """

    for documento in documentos:
        if documento.get("codigo") == codigo:
            return documento

    return None

def codigo_documento_existe(
    documentos: list[dict],
    codigo: int,
) -> bool:
    """
    Verifica se um código de documento já existe.
    """

    return buscar_documento_por_codigo(
        documentos=documentos,
        codigo=codigo,
    ) is not None

def listar_documentos_visiveis_ao_cliente(
    documentos: list[dict],
) -> list[dict]:
    """
    Retorna somente os documentos liberados para o cliente.

    Uma nova lista é criada para proteger a coleção original.
    """

    return [
        documento
        for documento in documentos
        if documento.get("visibilidade")
        == VisibilidadeDocumento.CLIENTE.value
    ]

def obter_rotulo_origem_documento(
    origem: str | OrigemDocumento,
) -> str:
    """
    Retorna o rótulo amigável da origem.
    """

    origem_convertida = _converter_origem_documento(
        origem
    )

    return ROTULOS_ORIGEM_DOCUMENTO[
        origem_convertida
    ]

def obter_rotulo_visibilidade_documento(
    visibilidade: str | VisibilidadeDocumento,
) -> str:
    """
    Retorna o rótulo amigável da visibilidade.
    """

    visibilidade_convertida = (
        _converter_visibilidade_documento(
            visibilidade
        )
    )

    return ROTULOS_VISIBILIDADE_DOCUMENTO[
        visibilidade_convertida
    ]

def obter_rotulo_status_documento(
    status: str | StatusDocumentoHomologacao,
) -> str:
    """
    Retorna o rótulo amigável do status documental.
    """

    status_convertido = _converter_status_documento(
        status
    )

    return ROTULOS_STATUS_DOCUMENTO[
        status_convertido
    ]

def converter_status_documento(
    status: str | StatusDocumentoHomologacao,
) -> StatusDocumentoHomologacao:
    """
    Converte um texto ou Enum em StatusDocumentoHomologacao.

    Esta função pública permite que outros módulos do domínio
    interpretem o status sem acessar diretamente uma função privada.
    """

    return _converter_status_documento(status)

def transicao_status_documento_e_valida(
    status_atual: str | StatusDocumentoHomologacao,
    novo_status: str | StatusDocumentoHomologacao,
) -> bool:
    """
    Verifica se uma transição documental é permitida.
    """

    status_atual_convertido = (
        _converter_status_documento(status_atual)
    )

    novo_status_convertido = (
        _converter_status_documento(novo_status)
    )

    proximos_status = TRANSICOES_STATUS_DOCUMENTO.get(
        status_atual_convertido,
        set(),
    )

    return novo_status_convertido in proximos_status

def listar_transicoes_status_documento(
    status_atual: str | StatusDocumentoHomologacao,
) -> tuple[StatusDocumentoHomologacao, ...]:
    """
    Retorna os próximos estados permitidos.

    O resultado é uma tupla ordenada pelo valor interno.
    """

    status_atual_convertido = (
        _converter_status_documento(status_atual)
    )

    proximos_status = TRANSICOES_STATUS_DOCUMENTO.get(
        status_atual_convertido,
        set(),
    )

    return tuple(
        sorted(
            proximos_status,
            key=lambda status: status.value,
        )
    )

def status_documento_e_terminal(
    status: str | StatusDocumentoHomologacao,
) -> bool:
    """
    Verifica se o documento se encontra em estado terminal.
    """

    status_convertido = _converter_status_documento(
        status
    )

    return status_convertido in STATUS_TERMINAIS_DOCUMENTO