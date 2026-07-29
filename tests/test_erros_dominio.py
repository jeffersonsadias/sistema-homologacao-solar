import unittest

from app.dominio.erros_dominio import (
    CodigoDuplicado,
    DadosObrigatoriosAusentes,
    EntidadeImutavel,
    EntidadeNaoEncontrada,
    ErroDominio,
    EstadoInconsistente,
    OperacaoNaoPermitida,
    RegistroDuplicado,
    RelacionamentoInvalido,
    TransicaoEstadoInvalida,
    ValorInvalido,
)


class TestErrosDominio(unittest.TestCase):
    """
    Testes das exceções utilizadas pelas regras de negócio.
    """

    def test_erro_dominio_herda_de_exception(self):
        """
        ErroDominio deve ser uma exceção padrão do Python.
        """

        self.assertTrue(issubclass(ErroDominio, Exception))

    def test_excecoes_especificas_herdam_de_erro_dominio(self):
        """
        Todas as exceções específicas devem poder ser capturadas
        por meio da classe ErroDominio.
        """

        excecoes = [
            TransicaoEstadoInvalida,
            EntidadeNaoEncontrada,
            CodigoDuplicado,
            RelacionamentoInvalido,
            OperacaoNaoPermitida,
            DadosObrigatoriosAusentes,
            EntidadeImutavel,
            EstadoInconsistente,
            RegistroDuplicado,
            ValorInvalido,
        ]

        for excecao in excecoes:
            with self.subTest(excecao=excecao.__name__):
                self.assertTrue(issubclass(excecao, ErroDominio))

    def test_excecao_preserva_mensagem(self):
        """
        A mensagem informada ao criar a exceção deve ser preservada.
        """

        mensagem = "A Unidade Consumidora pertence a outra Concessionária."

        erro = RelacionamentoInvalido(mensagem)

        self.assertEqual(str(erro), mensagem)

    def test_erro_especifico_pode_ser_capturado_como_erro_dominio(self):
        """
        Uma exceção específica deve ser capturada por um bloco
        except que trate ErroDominio.
        """

        mensagem = "Transição não permitida."

        try:
            raise TransicaoEstadoInvalida(mensagem)

        except ErroDominio as erro:
            mensagem_capturada = str(erro)

        self.assertEqual(mensagem_capturada, mensagem)


if __name__ == "__main__":
    unittest.main()