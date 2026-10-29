"""Testes automatizados. Rodar a partir da pasta do projeto:

    python3 -m unittest discover -v
"""

import unittest
from datetime import datetime, timedelta

from pedidos.economia import Economia, formatar_tempo
from pedidos.leitura import (
    Pedido,
    linha_para_pedido,
    padronizar_horario,
    padronizar_status,
    padronizar_texto,
    padronizar_valor,
    remover_duplicados,
)
from pedidos.metricas import calcular
from pedidos.relatorio import reais


def pedido(id_pedido="PED-1", restaurante="A", prato="X", valor=10.0, status="Entregue", minutos=30):
    inicio = datetime(2026, 10, 28, 12, 0)
    entrega = inicio + timedelta(minutes=minutos) if status == "Entregue" else None
    return Pedido(id_pedido, restaurante, prato, valor, status, inicio, entrega)


class TestPadronizacao(unittest.TestCase):
    def test_valor_em_varios_formatos(self):
        self.assertEqual(padronizar_valor("R$ 32,90"), 32.90)
        self.assertEqual(padronizar_valor("32.90"), 32.90)
        self.assertEqual(padronizar_valor("1.234,50"), 1234.50)

    def test_valor_invalido_gera_erro(self):
        with self.assertRaises(ValueError):
            padronizar_valor("trinta reais")
        with self.assertRaises(ValueError):
            padronizar_valor("-5,00")

    def test_status_sinonimos(self):
        self.assertEqual(padronizar_status(" FINALIZADO "), "Entregue")
        self.assertEqual(padronizar_status("estornado"), "Cancelado")
        with self.assertRaises(ValueError):
            padronizar_status("a caminho?")

    def test_texto(self):
        self.assertEqual(padronizar_texto("  burger   DA esquina "), "Burger da Esquina")
        self.assertEqual(padronizar_texto("pizza FRANGO catupiry"), "Pizza Frango Catupiry")

    def test_horario_nos_tres_formatos(self):
        esperado = datetime(2026, 10, 28, 12, 30)
        for texto in ["28/10/2026 12:30", "2026-10-28 12:30", "2026-10-28T12:30:00"]:
            self.assertEqual(padronizar_horario(texto), esperado)
        self.assertIsNone(padronizar_horario(""))

    def test_entregue_sem_horario_de_entrega_e_rejeitado(self):
        linha = {"id_pedido": "p1", "restaurante": "A", "prato": "X", "valor": "10",
                 "status": "Entregue", "horario_pedido": "28/10/2026 12:00", "horario_entrega": ""}
        with self.assertRaises(ValueError):
            linha_para_pedido(linha)


class TestDuplicados(unittest.TestCase):
    def test_remove_pedido_repetido(self):
        unicos = remover_duplicados([pedido("PED-1"), pedido("PED-2"), pedido("PED-1")])
        self.assertEqual([p.id_pedido for p in unicos].count("PED-1"), 1)
        self.assertEqual(len(unicos), 2)


class TestMetricas(unittest.TestCase):
    def test_resumo_geral(self):
        pedidos = [
            pedido("1", valor=20.0, minutos=30),
            pedido("2", valor=40.0, minutos=60),   # atrasado
            pedido("3", valor=99.0, status="Cancelado"),
        ]
        geral, por_restaurante, top = calcular(pedidos)
        self.assertEqual(geral.faturamento, 60.0)       # cancelado não entra
        self.assertEqual(geral.ticket_medio, 30.0)
        self.assertEqual(geral.tempo_medio, 45.0)
        self.assertAlmostEqual(geral.taxa_atraso, 0.5)
        self.assertAlmostEqual(geral.taxa_cancelamento, 1 / 3)
        self.assertEqual(top, [("X", 2)])


class TestEconomiaEFormatacao(unittest.TestCase):
    def test_tempo_manual(self):
        # 100 linhas × 15s + 20 min = 1500s + 1200s
        self.assertEqual(Economia(100, 0.5).segundos_manual, 2700)

    def test_formatar_tempo(self):
        self.assertEqual(formatar_tempo(0.042), "42 ms")
        self.assertEqual(formatar_tempo(95), "1min 35s")
        self.assertEqual(formatar_tempo(5400), "1h 30min")

    def test_reais(self):
        self.assertEqual(reais(1234.5), "R$ 1.234,50")


if __name__ == "__main__":
    unittest.main()
