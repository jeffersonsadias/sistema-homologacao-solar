"""
Domínio das Áreas de Atendimento das Empresas.

Define a cobertura geográfica utilizada
pelas ofertas de serviço.

Este módulo não realiza cálculo de distância
geográfica. Ele apenas representa e valida
a configuração da área de atendimento.
"""

from dataclasses import dataclass
from enum import Enum

from app.dominio.erros_dominio import (
    DadosObrigatoriosAusentes,
    ValorInvalido,
)


class ModalidadeAreaAtendimento(str, Enum):
    """
    Define como a cobertura geográfica
    da oferta de serviço é configurada.
    """

    RAIO = "RAIO"
    MUNICIPIOS = "MUNICIPIOS"
    NACIONAL = "NACIONAL"


@dataclass
class AreaAtendimento:
    """
    Representa a área geográfica na qual
    determinada oferta pode ser atendida.
    """

    modalidade: ModalidadeAreaAtendimento
    municipio_base: str | None = None
    uf_base: str | None = None
    raio_km: float | None = None
    municipios: tuple[str, ...] = ()

def _normalizar_modalidade(
    modalidade,
) -> ModalidadeAreaAtendimento:
    """
    Converte o valor informado para
    ModalidadeAreaAtendimento.
    """

    if isinstance(
        modalidade,
        ModalidadeAreaAtendimento,
    ):
        return modalidade

    try:
        return ModalidadeAreaAtendimento(
            modalidade
        )

    except (ValueError, TypeError):
        raise ValorInvalido(
            "Modalidade da área de atendimento inválida."
        )

def _normalizar_texto_obrigatorio(
    valor: str,
    nome_campo: str,
) -> str:
    """
    Valida e normaliza texto obrigatório.
    """

    if valor is None:
        raise DadosObrigatoriosAusentes(
            f"{nome_campo} é obrigatório."
        )

    if not isinstance(
        valor,
        str,
    ):
        raise ValorInvalido(
            f"{nome_campo} deve ser um texto."
        )

    valor_normalizado = " ".join(
        valor.strip().split()
    )

    if not valor_normalizado:
        raise DadosObrigatoriosAusentes(
            f"{nome_campo} é obrigatório."
        )

    return valor_normalizado

def _normalizar_uf(
    uf: str,
) -> str:
    """
    Valida e normaliza uma UF brasileira.
    """

    uf_normalizada = (
        _normalizar_texto_obrigatorio(
            uf,
            "UF",
        )
        .upper()
    )

    if len(uf_normalizada) != 2:
        raise ValorInvalido(
            "UF deve possuir exatamente 2 caracteres."
        )

    if not uf_normalizada.isalpha():
        raise ValorInvalido(
            "UF deve conter apenas letras."
        )

    return uf_normalizada

def _validar_raio_km(
    raio_km,
) -> float:
    """
    Valida o raio de atendimento em quilômetros.
    """

    if raio_km is None:
        raise DadosObrigatoriosAusentes(
            "Raio de atendimento é obrigatório."
        )

    if (
        isinstance(raio_km, bool)
        or not isinstance(
            raio_km,
            (int, float),
        )
    ):
        raise ValorInvalido(
            "Raio de atendimento deve ser numérico."
        )

    raio_normalizado = float(
        raio_km
    )

    if raio_normalizado <= 0:
        raise ValorInvalido(
            "Raio de atendimento deve ser maior que zero."
        )

    return raio_normalizado

def _normalizar_municipios(
    municipios,
) -> tuple[str, ...]:
    """
    Valida e normaliza a coleção de municípios.

    A ordem informada é preservada.
    Duplicidades são removidas.
    """

    if municipios is None:
        raise DadosObrigatoriosAusentes(
            "Municípios atendidos são obrigatórios."
        )

    if not isinstance(
        municipios,
        (list, tuple),
    ):
        raise ValorInvalido(
            "Municípios devem ser informados "
            "em uma lista ou tupla."
        )

    if not municipios:
        raise DadosObrigatoriosAusentes(
            "Informe ao menos um município."
        )

    municipios_normalizados = []
    nomes_comparacao = set()

    for municipio in municipios:
        municipio_normalizado = (
            _normalizar_texto_obrigatorio(
                municipio,
                "Município",
            )
        )

        chave = municipio_normalizado.casefold()

        if chave in nomes_comparacao:
            continue

        nomes_comparacao.add(
            chave
        )

        municipios_normalizados.append(
            municipio_normalizado
        )

    return tuple(
        municipios_normalizados
    )

def criar_area_atendimento(
    modalidade,
    municipio_base: str | None = None,
    uf_base: str | None = None,
    raio_km=None,
    municipios=None,
) -> AreaAtendimento:
    """
    Cria uma Área de Atendimento.

    Regras por modalidade:

    RAIO:
        exige município-base, UF e raio.

    MUNICIPIOS:
        exige ao menos um município.

    NACIONAL:
        não utiliza município-base, UF,
        raio ou lista de municípios.
    """

    modalidade_normalizada = (
        _normalizar_modalidade(
            modalidade
        )
    )

    if (
        modalidade_normalizada
        == ModalidadeAreaAtendimento.RAIO
    ):
        municipio_base_normalizado = (
            _normalizar_texto_obrigatorio(
                municipio_base,
                "Município-base",
            )
        )

        uf_base_normalizada = (
            _normalizar_uf(
                uf_base
            )
        )

        raio_validado = _validar_raio_km(
            raio_km
        )

        if municipios is not None:
            raise ValorInvalido(
                "A modalidade RAIO não utiliza "
                "lista de municípios."
            )

        return AreaAtendimento(
            modalidade=modalidade_normalizada,
            municipio_base=(
                municipio_base_normalizado
            ),
            uf_base=uf_base_normalizada,
            raio_km=raio_validado,
            municipios=(),
        )

    if (
        modalidade_normalizada
        == ModalidadeAreaAtendimento.MUNICIPIOS
    ):
        municipios_normalizados = (
            _normalizar_municipios(
                municipios
            )
        )

        if (
            municipio_base is not None
            or uf_base is not None
            or raio_km is not None
        ):
            raise ValorInvalido(
                "A modalidade MUNICIPIOS não utiliza "
                "município-base, UF ou raio."
            )

        return AreaAtendimento(
            modalidade=modalidade_normalizada,
            municipio_base=None,
            uf_base=None,
            raio_km=None,
            municipios=(
                municipios_normalizados
            ),
        )

    if (
        modalidade_normalizada
        == ModalidadeAreaAtendimento.NACIONAL
    ):
        if (
            municipio_base is not None
            or uf_base is not None
            or raio_km is not None
            or municipios is not None
        ):
            raise ValorInvalido(
                "A modalidade NACIONAL não deve "
                "possuir configuração geográfica adicional."
            )

        return AreaAtendimento(
            modalidade=modalidade_normalizada,
            municipio_base=None,
            uf_base=None,
            raio_km=None,
            municipios=(),
        )

    raise ValorInvalido(
        "Modalidade da área de atendimento inválida."
    )

def area_atende_localidade(
    area,
    municipio: str,
    uf: str,
    distancia_km=None,
) -> bool:
    """
    Informa se uma Área de Atendimento
    cobre determinada localidade.

    Para modalidade RAIO, a distância deve
    ser previamente calculada e informada.
    """

    if not isinstance(
        area,
        AreaAtendimento,
    ):
        raise ValorInvalido(
            "Área de atendimento deve ser "
            "uma AreaAtendimento válida."
        )

    municipio_normalizado = (
        _normalizar_texto_obrigatorio(
            municipio,
            "Município",
        )
    )

    uf_normalizada = _normalizar_uf(
        uf
    )

    if (
        area.modalidade
        == ModalidadeAreaAtendimento.NACIONAL
    ):
        return True

    if (
        area.modalidade
        == ModalidadeAreaAtendimento.MUNICIPIOS
    ):
        municipio_comparacao = (
            municipio_normalizado.casefold()
        )

        return any(
            municipio_atendido.casefold()
            == municipio_comparacao
            for municipio_atendido
            in area.municipios
        )

    if (
        area.modalidade
        == ModalidadeAreaAtendimento.RAIO
    ):
        if distancia_km is None:
            raise DadosObrigatoriosAusentes(
                "Distância é obrigatória para "
                "validar Área de Atendimento "
                "por RAIO."
            )

        if (
            isinstance(distancia_km, bool)
            or not isinstance(
                distancia_km,
                (int, float),
            )
        ):
            raise ValorInvalido(
                "Distância deve ser numérica."
            )

        distancia_normalizada = float(
            distancia_km
        )

        if distancia_normalizada < 0:
            raise ValorInvalido(
                "Distância não pode ser negativa."
            )

        if (
            uf_normalizada
            != area.uf_base
        ):
            return False

        return (
            distancia_normalizada
            <= area.raio_km
        )

    raise ValorInvalido(
        "Modalidade da área de atendimento inválida."
    )





