"""
Regras de domínio relacionadas às empresas da plataforma.

A Empresa representa uma organização de energia solar que utiliza
o ambiente corporativo do sistema.

Este módulo não realiza:
- entrada de dados pelo terminal;
- leitura ou gravação de arquivos JSON;
- exibição de mensagens;
- autenticação de usuários.

Essas responsabilidades pertencem a outras camadas da aplicação.
"""

from datetime import datetime
from typing import Any


# ============================================================
# SITUAÇÕES POSSÍVEIS DA EMPRESA
# ============================================================

SITUACAO_EMPRESA_ATIVA = "ATIVA"
SITUACAO_EMPRESA_INATIVA = "INATIVA"
SITUACAO_EMPRESA_SUSPENSA = "SUSPENSA"
SITUACAO_EMPRESA_CANCELADA = "CANCELADA"


SITUACOES_EMPRESA = (
    SITUACAO_EMPRESA_ATIVA,
    SITUACAO_EMPRESA_INATIVA,
    SITUACAO_EMPRESA_SUSPENSA,
    SITUACAO_EMPRESA_CANCELADA,
)


SITUACAO_INICIAL_EMPRESA = SITUACAO_EMPRESA_ATIVA

# ============================================================
# TRANSIÇÕES PERMITIDAS
# ============================================================

TRANSICOES_SITUACAO_EMPRESA = {
    SITUACAO_EMPRESA_ATIVA: (
        SITUACAO_EMPRESA_INATIVA,
        SITUACAO_EMPRESA_SUSPENSA,
        SITUACAO_EMPRESA_CANCELADA,
    ),
    SITUACAO_EMPRESA_INATIVA: (
        SITUACAO_EMPRESA_ATIVA,
        SITUACAO_EMPRESA_CANCELADA,
    ),
    SITUACAO_EMPRESA_SUSPENSA: (
        SITUACAO_EMPRESA_ATIVA,
        SITUACAO_EMPRESA_INATIVA,
        SITUACAO_EMPRESA_CANCELADA,
    ),
    SITUACAO_EMPRESA_CANCELADA: (),
}

# ============================================================
# FUNÇÕES AUXILIARES INTERNAS
# ============================================================

def _normalizar_texto(valor: str) -> str:
    """
    Remove espaços desnecessários do início e do fim de um texto.

    Também reduz sequências de vários espaços internos para apenas
    um espaço.

    Exemplo:
        "  Solar   Energia Bahia  "
        torna-se:
        "Solar Energia Bahia"
    """

    if not isinstance(valor, str):
        raise TypeError("O valor informado deve ser um texto.")

    return " ".join(valor.strip().split())


def _normalizar_email(email: str) -> str:
    """
    Normaliza o e-mail para facilitar comparações.

    O e-mail será:
    - limpo;
    - convertido para letras minúsculas.
    """

    email_normalizado = _normalizar_texto(email).lower()

    if not email_normalizado:
        raise ValueError("O e-mail da empresa é obrigatório.")

    if "@" not in email_normalizado:
        raise ValueError("O e-mail da empresa é inválido.")

    parte_local, separador, dominio = email_normalizado.partition("@")

    if (
        not separador
        or not parte_local
        or not dominio
        or "." not in dominio
    ):
        raise ValueError("O e-mail da empresa é inválido.")

    return email_normalizado


def _manter_apenas_numeros(valor: str) -> str:
    """
    Remove pontos, barras, traços, espaços e outros caracteres,
    mantendo somente os números.
    """

    if not isinstance(valor, str):
        raise TypeError("O valor informado deve ser um texto.")

    return "".join(
        caractere
        for caractere in valor
        if caractere.isdigit()
    )


def _validar_codigo(codigo: int) -> None:
    """
    Valida o código interno da empresa.
    """

    if not isinstance(codigo, int):
        raise TypeError("O código da empresa deve ser um número inteiro.")

    if codigo <= 0:
        raise ValueError("O código da empresa deve ser maior que zero.")


def _validar_texto_obrigatorio(
    valor: str,
    nome_campo: str,
) -> str:
    """
    Normaliza e valida campos textuais obrigatórios.
    """

    texto_normalizado = _normalizar_texto(valor)

    if not texto_normalizado:
        raise ValueError(f"{nome_campo} é obrigatório.")

    return texto_normalizado


def _validar_cnpj(cnpj: str) -> str:
    """
    Normaliza e valida estruturalmente o CNPJ.

    Nesta primeira implementação, são verificadas:
    - presença de 14 números;
    - ausência de todos os dígitos repetidos;
    - validade dos dois dígitos verificadores.
    """

    cnpj_normalizado = _manter_apenas_numeros(cnpj)

    if len(cnpj_normalizado) != 14:
        raise ValueError("O CNPJ deve possuir 14 números.")

    if len(set(cnpj_normalizado)) == 1:
        raise ValueError("O CNPJ informado é inválido.")

    primeiros_doze_digitos = cnpj_normalizado[:12]

    primeiro_digito = _calcular_digito_cnpj(
        primeiros_doze_digitos,
        pesos=(5, 4, 3, 2, 9, 8, 7, 6, 5, 4, 3, 2),
    )

    primeiros_treze_digitos = (
        primeiros_doze_digitos
        + str(primeiro_digito)
    )

    segundo_digito = _calcular_digito_cnpj(
        primeiros_treze_digitos,
        pesos=(6, 5, 4, 3, 2, 9, 8, 7, 6, 5, 4, 3, 2),
    )

    digitos_calculados = f"{primeiro_digito}{segundo_digito}"
    digitos_informados = cnpj_normalizado[-2:]

    if digitos_calculados != digitos_informados:
        raise ValueError("O CNPJ informado é inválido.")

    return cnpj_normalizado


def _calcular_digito_cnpj(
    numeros: str,
    pesos: tuple[int, ...],
) -> int:
    """
    Calcula um dos dígitos verificadores do CNPJ.
    """

    soma = sum(
        int(numero) * peso
        for numero, peso in zip(numeros, pesos)
    )

    resto = soma % 11

    if resto < 2:
        return 0

    return 11 - resto


def _validar_situacao(situacao: str) -> str:
    """
    Verifica se a situação informada é reconhecida pelo domínio.
    """

    situacao_normalizada = _normalizar_texto(situacao).upper()

    if situacao_normalizada not in SITUACOES_EMPRESA:
        raise ValueError(
            "Situação da empresa inválida. "
            f"Situações permitidas: {', '.join(SITUACOES_EMPRESA)}."
        )

    return situacao_normalizada


def _gerar_data_hora_atual() -> str:
    """
    Gera a data e hora atual no formato ISO 8601.

    Exemplo:
        2026-07-28T09:30:00
    """

    return datetime.now().isoformat(timespec="seconds")


# ============================================================
# CONSULTAS DE DOMÍNIO
# ============================================================

def buscar_empresa_por_codigo(
    empresas: list[dict[str, Any]],
    codigo: int,
) -> dict[str, Any] | None:
    """
    Busca uma empresa pelo seu código interno.

    Retorna:
    - o dicionário da empresa encontrada;
    - None quando a empresa não existe.
    """

    _validar_codigo(codigo)

    for empresa in empresas:
        if empresa.get("codigo") == codigo:
            return empresa

    return None


def codigo_empresa_existe(
    empresas: list[dict[str, Any]],
    codigo: int,
) -> bool:
    """
    Verifica se determinado código de empresa já está cadastrado.
    """

    return buscar_empresa_por_codigo(
        empresas,
        codigo,
    ) is not None


def buscar_empresa_por_cnpj(
    empresas: list[dict[str, Any]],
    cnpj: str,
) -> dict[str, Any] | None:
    """
    Busca uma empresa pelo CNPJ.
    """

    cnpj_normalizado = _validar_cnpj(cnpj)

    for empresa in empresas:
        if empresa.get("cnpj") == cnpj_normalizado:
            return empresa

    return None


def cnpj_empresa_existe(
    empresas: list[dict[str, Any]],
    cnpj: str,
) -> bool:
    """
    Verifica se o CNPJ já está associado a alguma empresa.
    """

    return buscar_empresa_por_cnpj(
        empresas,
        cnpj,
    ) is not None


def ordenar_empresas_por_nome(
    empresas: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    """
    Retorna uma nova lista ordenada pelo nome fantasia.

    A lista original não é alterada.
    """

    return sorted(
        empresas,
        key=lambda empresa: empresa.get(
            "nome_fantasia",
            "",
        ).casefold(),
    )


def empresa_esta_ativa(
    empresa: dict[str, Any],
) -> bool:
    """
    Verifica se a empresa está ativa.
    """

    return (
        empresa.get("situacao")
        == SITUACAO_EMPRESA_ATIVA
    )


# ============================================================
# CRIAÇÃO DOS DADOS DA EMPRESA
# ============================================================

def criar_dados_empresa(
    codigo: int,
    razao_social: str,
    nome_fantasia: str,
    cnpj: str,
    email: str,
    telefone: str,
) -> dict[str, Any]:
    """
    Cria e retorna os dados de uma nova empresa.

    Esta função não salva os dados em arquivo. Ela apenas:
    - valida os valores;
    - normaliza os campos;
    - monta o dicionário da empresa.

    A persistência será responsabilidade da infraestrutura.
    """

    _validar_codigo(codigo)

    razao_social_normalizada = _validar_texto_obrigatorio(
        razao_social,
        "A razão social",
    )

    nome_fantasia_normalizado = _validar_texto_obrigatorio(
        nome_fantasia,
        "O nome fantasia",
    )

    cnpj_normalizado = _validar_cnpj(cnpj)
    email_normalizado = _normalizar_email(email)

    telefone_normalizado = _manter_apenas_numeros(
        telefone,
    )

    if not telefone_normalizado:
        raise ValueError(
            "O telefone da empresa é obrigatório."
        )

    data_hora_atual = _gerar_data_hora_atual()

    return {
        "codigo": codigo,
        "razao_social": razao_social_normalizada,
        "nome_fantasia": nome_fantasia_normalizado,
        "cnpj": cnpj_normalizado,
        "email": email_normalizado,
        "telefone": telefone_normalizado,
        "situacao": SITUACAO_INICIAL_EMPRESA,
        "data_cadastro": data_hora_atual,
        "data_atualizacao": data_hora_atual,
    }

def obter_transicoes_permitidas_empresa(
    situacao_atual: str,
) -> tuple[str, ...]:
    """
    Retorna as situações para as quais uma empresa pode avançar.

    Exemplo:

        ATIVA
            ↓
        INATIVA, SUSPENSA ou CANCELADA

    A função retorna uma tupla vazia para estados terminais.
    """

    situacao_validada = _validar_situacao(
        situacao_atual,
    )

    return TRANSICOES_SITUACAO_EMPRESA[
        situacao_validada
    ]


def transicao_situacao_empresa_permitida(
    situacao_atual: str,
    nova_situacao: str,
) -> bool:
    """
    Verifica se uma transição entre situações é permitida.
    """

    situacao_atual_validada = _validar_situacao(
        situacao_atual,
    )

    nova_situacao_validada = _validar_situacao(
        nova_situacao,
    )

    transicoes_permitidas = (
        obter_transicoes_permitidas_empresa(
            situacao_atual_validada,
        )
    )

    return (
        nova_situacao_validada
        in transicoes_permitidas
    )


def empresa_esta_cancelada(
    empresa: dict[str, Any],
) -> bool:
    """
    Verifica se a empresa está cancelada.
    """

    return (
        empresa.get("situacao")
        == SITUACAO_EMPRESA_CANCELADA
    )

# ============================================================
# ATUALIZAÇÃO DOS DADOS CADASTRAIS
# ============================================================

def atualizar_dados_empresa(
    empresa: dict[str, Any],
    razao_social: str | None = None,
    nome_fantasia: str | None = None,
    email: str | None = None,
    telefone: str | None = None,
) -> dict[str, Any]:
    """
    Atualiza os dados cadastrais permitidos de uma empresa.

    Campos que podem ser alterados:
    - razão social;
    - nome fantasia;
    - e-mail;
    - telefone.

    O CNPJ não pode ser alterado por esta função.

    Quando um argumento recebe None, o valor atual é preservado.
    """

    if not isinstance(empresa, dict):
        raise TypeError(
            "A empresa deve ser representada por um dicionário."
        )

    campos_obrigatorios = (
        "codigo",
        "razao_social",
        "nome_fantasia",
        "cnpj",
        "email",
        "telefone",
        "situacao",
    )

    for campo in campos_obrigatorios:
        if campo not in empresa:
            raise ValueError(
                f"A empresa não possui o campo obrigatório: {campo}."
            )

    nenhuma_alteracao_informada = all(
        valor is None
        for valor in (
            razao_social,
            nome_fantasia,
            email,
            telefone,
        )
    )

    if nenhuma_alteracao_informada:
        raise ValueError(
            "Nenhum dado foi informado para atualização."
        )

    if razao_social is not None:
        empresa["razao_social"] = (
            _validar_texto_obrigatorio(
                razao_social,
                "A razão social",
            )
        )

    if nome_fantasia is not None:
        empresa["nome_fantasia"] = (
            _validar_texto_obrigatorio(
                nome_fantasia,
                "O nome fantasia",
            )
        )

    if email is not None:
        empresa["email"] = _normalizar_email(
            email,
        )

    if telefone is not None:
        telefone_normalizado = _manter_apenas_numeros(
            telefone,
        )

        if not telefone_normalizado:
            raise ValueError(
                "O telefone da empresa é obrigatório."
            )

        empresa["telefone"] = telefone_normalizado

    empresa["data_atualizacao"] = (
        _gerar_data_hora_atual()
    )

    return empresa

# ============================================================
# ALTERAÇÕES DE SITUAÇÃO
# ============================================================

def alterar_situacao_empresa(
    empresa: dict[str, Any],
    nova_situacao: str,
) -> dict[str, Any]:
    """
    Altera a situação da empresa quando a transição for permitida.

    Regras principais:
    - a situação atual deve ser válida;
    - a nova situação deve ser válida;
    - não são permitidas alterações redundantes;
    - empresas canceladas não podem sair do estado terminal.
    """

    if not isinstance(empresa, dict):
        raise TypeError(
            "A empresa deve ser representada por um dicionário."
        )

    if "situacao" not in empresa:
        raise ValueError(
            "A empresa não possui uma situação cadastrada."
        )

    situacao_atual = _validar_situacao(
        empresa["situacao"],
    )

    nova_situacao_validada = _validar_situacao(
        nova_situacao,
    )

    if situacao_atual == nova_situacao_validada:
        raise ValueError(
            "A empresa já se encontra na situação "
            f"{situacao_atual}."
        )

    if not transicao_situacao_empresa_permitida(
        situacao_atual,
        nova_situacao_validada,
    ):
        raise ValueError(
            "Transição de situação não permitida: "
            f"{situacao_atual} → {nova_situacao_validada}."
        )

    empresa["situacao"] = nova_situacao_validada
    empresa["data_atualizacao"] = (
        _gerar_data_hora_atual()
    )

    return empresa


def ativar_empresa(
    empresa: dict[str, Any],
) -> dict[str, Any]:
    """
    Ativa uma empresa.
    """

    return alterar_situacao_empresa(
        empresa,
        SITUACAO_EMPRESA_ATIVA,
    )


def inativar_empresa(
    empresa: dict[str, Any],
) -> dict[str, Any]:
    """
    Inativa uma empresa sem apagar seu histórico.
    """

    return alterar_situacao_empresa(
        empresa,
        SITUACAO_EMPRESA_INATIVA,
    )


def suspender_empresa(
    empresa: dict[str, Any],
) -> dict[str, Any]:
    """
    Suspende temporariamente uma empresa.
    """

    return alterar_situacao_empresa(
        empresa,
        SITUACAO_EMPRESA_SUSPENSA,
    )


def cancelar_empresa(
    empresa: dict[str, Any],
) -> dict[str, Any]:
    """
    Cancela uma empresa preservando seus dados históricos.
    """

    return alterar_situacao_empresa(
        empresa,
        SITUACAO_EMPRESA_CANCELADA,
    )