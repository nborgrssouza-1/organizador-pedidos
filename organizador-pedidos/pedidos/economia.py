"""Compara o tempo do processo manual (estimado) com o tempo do script (medido)."""

from dataclasses import dataclass

# Estimativas do processo manual numa planilha. Ajuste cronometrando a tarefa de verdade.
SEGUNDOS_POR_LINHA = 15        # copiar a linha, corrigir valor/status/horário, checar duplicado
MINUTOS_RELATORIO = 20         # montar tabelas por restaurante, ranking de pratos e resumo
EXECUCOES_POR_MES = 30         # um fechamento por dia


@dataclass
class Economia:
    linhas: int
    segundos_script: float

    @property
    def segundos_manual(self):
        return self.linhas * SEGUNDOS_POR_LINHA + MINUTOS_RELATORIO * 60

    @property
    def segundos_economizados(self):
        return self.segundos_manual - self.segundos_script

    @property
    def horas_por_mes(self):
        return self.segundos_economizados * EXECUCOES_POR_MES / 3600


def formatar_tempo(segundos):
    if segundos < 1:
        return f"{segundos * 1000:.0f} ms"
    minutos, seg = divmod(round(segundos), 60)
    horas, minutos = divmod(minutos, 60)
    if horas:
        return f"{horas}h {minutos:02d}min"
    return f"{minutos}min {seg:02d}s" if minutos else f"{seg}s"
