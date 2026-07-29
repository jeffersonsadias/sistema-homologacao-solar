"""
Exceções relacionadas às regras de negócio do sistema.

Este módulo concentra os erros de domínio utilizados pelos diferentes
módulos da aplicação.

As exceções aqui definidas representam violações de regras de negócio,
e não erros técnicos como falha de leitura de arquivo ou conexão com
banco de dados.
"""


class ErroDominio(Exception):
    """
    Classe base para todas as exceções de domínio do sistema.

    Todas as exceções relacionadas às regras de negócio devem herdar
    desta classe.

    Isso permite capturar qualquer erro de domínio usando:

        except ErroDominio as erro:
            print(erro)
    """

    pass


class TransicaoEstadoInvalida(ErroDominio):
    """
    Indica que uma entidade tentou realizar uma transição de estado
    que não é permitida pela sua máquina de estados.

    Exemplo:

        Processo em CADASTRO_INICIAL tentando avançar diretamente
        para PREPARACAO_TECNICA.
    """

    pass


class EntidadeNaoEncontrada(ErroDominio):
    """
    Indica que uma entidade solicitada não foi encontrada.

    Exemplos:

        - Cliente inexistente;
        - Projeto inexistente;
        - Concessionária inexistente;
        - Unidade Consumidora inexistente.
    """

    pass


class CodigoDuplicado(ErroDominio):
    """
    Indica que houve tentativa de cadastrar uma entidade com um
    código que já está sendo utilizado.
    """

    pass


class RelacionamentoInvalido(ErroDominio):
    """
    Indica que duas ou mais entidades não podem ser relacionadas
    por violarem uma regra de negócio.

    Exemplos:

        - Unidade Beneficiária de outra Concessionária;
        - Processo associado a uma Concessionária diferente daquela
          registrada no Projeto;
        - Unidade Consumidora incompatível com o Projeto.
    """

    pass


class OperacaoNaoPermitida(ErroDominio):
    """
    Indica que uma operação não pode ser realizada nas condições
    atuais da entidade.

    É utilizada quando o problema não é necessariamente uma simples
    transição de estado.

    Exemplos:

        - Arquivar um Processo ainda ativo;
        - Alterar um Pacote já enviado;
        - Remover uma Unidade Geradora de um Projeto em tramitação.
    """

    pass


class DadosObrigatoriosAusentes(ErroDominio):
    """
    Indica que uma operação ou cadastro não possui todos os dados
    obrigatórios exigidos pelo domínio.

    Exemplos:

        - Concessionária sem nome;
        - Unidade Consumidora sem titular;
        - Processo sem Projeto;
        - Encerramento sem resultado final.
    """

    pass


class EntidadeImutavel(ErroDominio):
    """
    Indica que houve tentativa de alterar uma entidade ou versão
    que já se tornou imutável.

    Exemplos:

        - Pacote enviado;
        - Versão Técnica utilizada em Submissão;
        - Configuração de Compensação ativada;
        - Evento de Conexão já registrado.
    """

    pass


class EstadoInconsistente(ErroDominio):
    """
    Indica que os dados ou eventos registrados produzem uma condição
    incompatível ou contraditória.

    Exemplos:

        - Compensação ativa sem geração liberada;
        - Reativação sem suspensão anterior;
        - Processo aprovado com Exigência impeditiva aberta.
    """

    pass


class RegistroDuplicado(ErroDominio):
    """
    Indica que um registro equivalente já existe dentro do contexto
    analisado.

    Exemplos:

        - Mesma Unidade Beneficiária adicionada duas vezes;
        - Mesmo documento incluído duas vezes no Pacote;
        - Mesmo participante cadastrado repetidamente.
    """

    pass


class ValorInvalido(ErroDominio):
    """
    Indica que um valor informado não respeita os limites ou regras
    estabelecidos pelo domínio.

    Exemplos:

        - Potência negativa;
        - Percentual de compensação superior a 100%;
        - Data final anterior à data inicial;
        - Quantidade igual a zero quando deve ser positiva.
    """

    pass