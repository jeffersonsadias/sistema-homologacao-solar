"""
Registro de histórico das operações relevantes do sistema.

Este módulo será responsável por representar fatos ocorridos no domínio,
como criação de entidades, alterações de estado, vínculos e cancelamentos.

Nesta primeira versão, o módulo apenas cria e manipula registros em memória.
A persistência em JSON será adicionada posteriormente.
"""

from dataclasses import asdict, dataclass
from datetime import datetime
from typing import Optional


@dataclass(frozen=True)
class RegistroHistorico:
    """
    Representa um fato ocorrido no sistema.

    O parâmetro frozen=True torna a instância imutável depois de criada.

    Isso significa que um registro de histórico não pode ser alterado.
    Caso uma informação precise ser corrigida, deverá ser criado um novo
    registro explicando a retificação.
    """

    entidade_tipo: str
    entidade_codigo: int
    evento: str
    descricao: str
    data_hora: str
    responsavel: Optional[str] = None
    dados_anteriores: Optional[dict] = None
    dados_novos: Optional[dict] = None


def obter_data_hora_atual():
    """
    Retorna a data e a hora atuais em formato textual padronizado.

    O formato ISO facilita:

    - ordenação;
    - leitura;
    - persistência em JSON;
    - conversão futura para banco de dados;
    - integração com APIs.
    """

    return datetime.now().isoformat(timespec="seconds")


def criar_registro_historico(
    entidade_tipo,
    entidade_codigo,
    evento,
    descricao,
    responsavel=None,
    dados_anteriores=None,
    dados_novos=None,
):
    """
    Cria um novo registro de histórico.

    Esta função centraliza a criação do registro para impedir que cada módulo
    construa o histórico de maneira diferente.

    Parâmetros:

    entidade_tipo:
        Nome do tipo da entidade relacionada ao evento.

        Exemplos:
            "PROJETO"
            "PROCESSO_HOMOLOGACAO"
            "CONCESSIONARIA"
            "UNIDADE_CONSUMIDORA"

    entidade_codigo:
        Código numérico da entidade relacionada ao evento.

    evento:
        Nome técnico e padronizado do fato ocorrido.

        Exemplos:
            "PROCESSO_CRIADO"
            "FASE_ALTERADA"
            "UNIDADE_GERADORA_VINCULADA"

    descricao:
        Explicação legível do que aconteceu.

    responsavel:
        Pessoa ou usuário responsável pela operação.

    dados_anteriores:
        Estado anterior da informação, quando aplicável.

    dados_novos:
        Estado resultante da operação, quando aplicável.
    """

    return RegistroHistorico(
        entidade_tipo=entidade_tipo,
        entidade_codigo=entidade_codigo,
        evento=evento,
        descricao=descricao,
        data_hora=obter_data_hora_atual(),
        responsavel=responsavel,
        dados_anteriores=dados_anteriores,
        dados_novos=dados_novos,
    )


def converter_registro_para_dicionario(registro):
    """
    Converte um RegistroHistorico em dicionário.

    Essa conversão será utilizada futuramente para salvar o registro
    em arquivo JSON.
    """

    return asdict(registro)