"""Calcula os indicadores que um time de operações acompanha todo dia."""

from collections import Counter, defaultdict
from dataclasses import dataclass, field
from statistics import mean

LIMITE_ATRASO_MIN = 45


@dataclass
class Resumo:
    total: int = 0
    entregues: int = 0
    cancelados: int = 0
    faturamento: float = 0.0
    atrasados: int = 0
    tempos_entrega: list = field(default_factory=list)

    @property
    def ticket_medio(self):
        return self.faturamento / self.entregues if self.entregues else 0.0

    @property
    def taxa_cancelamento(self):
        return self.cancelados / self.total if self.total else 0.0

    @property
    def tempo_medio(self):
        return mean(self.tempos_entrega) if self.tempos_entrega else 0.0

    @property
    def taxa_atraso(self):
        return self.atrasados / self.entregues if self.entregues else 0.0

    def adicionar(self, pedido):
        self.total += 1
        if pedido.status == "Cancelado":
            self.cancelados += 1
            return
        self.entregues += 1
        self.faturamento += pedido.valor
        self.tempos_entrega.append(pedido.minutos_entrega)
        if pedido.minutos_entrega > LIMITE_ATRASO_MIN:
            self.atrasados += 1


def calcular(pedidos):
    """Devolve (resumo geral, resumo por restaurante, pratos mais vendidos)."""
    geral = Resumo()
    por_restaurante = defaultdict(Resumo)
    pratos = Counter()
    for pedido in pedidos:
        geral.adicionar(pedido)
        por_restaurante[pedido.restaurante].adicionar(pedido)
        if pedido.status == "Entregue":
            pratos[pedido.prato] += 1
    return geral, dict(sorted(por_restaurante.items())), pratos.most_common(5)
