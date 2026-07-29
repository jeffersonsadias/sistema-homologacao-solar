import unittest
from dataclasses import FrozenInstanceError
from datetime import datetime

from app.dominio.historico import (
    RegistroHistorico,
    converter_registro_para_dicionario,
    criar_registro_historico,
    obter_data_hora_atual,
)


class TestHistorico(unittest.TestCase):
    """
    Testes do módulo responsável pelo Histórico do domínio.
    """

    def test_obter_data_hora_atual_retorna_formato_iso(self):
        """
        A função deve retornar uma data válida no formato ISO.
        """

        data_hora = obter_data_hora_atual()

        data_convertida = datetime.fromisoformat(data_hora)

        self.assertIsInstance(data_convertida, datetime)

    def test_criar_registro_historico(self):
        """
        A função deve criar um RegistroHistorico com os dados informados.
        """

        registro = criar_registro_historico(
            entidade_tipo="PROCESSO_HOMOLOGACAO",
            entidade_codigo=10,
            evento="PROCESSO_CRIADO",
            descricao="Processo criado para teste.",
            responsavel="Jefferson",
        )

        self.assertIsInstance(registro, RegistroHistorico)
        self.assertEqual(
            registro.entidade_tipo,
            "PROCESSO_HOMOLOGACAO",
        )
        self.assertEqual(registro.entidade_codigo, 10)
        self.assertEqual(registro.evento, "PROCESSO_CRIADO")
        self.assertEqual(
            registro.descricao,
            "Processo criado para teste.",
        )
        self.assertEqual(registro.responsavel, "Jefferson")

    def test_registro_historico_e_imutavel(self):
        """
        Um registro já criado não deve permitir alterações.
        """

        registro = criar_registro_historico(
            entidade_tipo="PROJETO",
            entidade_codigo=1,
            evento="PROJETO_CRIADO",
            descricao="Projeto criado.",
        )

        with self.assertRaises(FrozenInstanceError):
            registro.evento = "PROJETO_CANCELADO"

    def test_registro_pode_conter_dados_anteriores_e_novos(self):
        """
        O histórico deve registrar o estado anterior e o estado novo.
        """

        registro = criar_registro_historico(
            entidade_tipo="PROCESSO_HOMOLOGACAO",
            entidade_codigo=1,
            evento="FASE_ALTERADA",
            descricao="Fase do Processo alterada.",
            dados_anteriores={
                "fase": "CADASTRO_INICIAL"
            },
            dados_novos={
                "fase": "LEVANTAMENTO"
            },
        )

        self.assertEqual(
            registro.dados_anteriores,
            {"fase": "CADASTRO_INICIAL"},
        )

        self.assertEqual(
            registro.dados_novos,
            {"fase": "LEVANTAMENTO"},
        )

    def test_converter_registro_para_dicionario(self):
        """
        O RegistroHistorico deve poder ser convertido para um dicionário.
        """

        registro = criar_registro_historico(
            entidade_tipo="CONCESSIONARIA",
            entidade_codigo=5,
            evento="CONCESSIONARIA_CADASTRADA",
            descricao="Concessionária cadastrada.",
        )

        registro_convertido = converter_registro_para_dicionario(
            registro
        )

        self.assertIsInstance(registro_convertido, dict)
        self.assertEqual(
            registro_convertido["entidade_tipo"],
            "CONCESSIONARIA",
        )
        self.assertEqual(
            registro_convertido["entidade_codigo"],
            5,
        )
        self.assertEqual(
            registro_convertido["evento"],
            "CONCESSIONARIA_CADASTRADA",
        )


if __name__ == "__main__":
    unittest.main()