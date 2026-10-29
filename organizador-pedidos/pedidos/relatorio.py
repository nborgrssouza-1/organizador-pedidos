"""Gera os arquivos de saída: CSV limpo e relatório em Markdown."""

import csv
from datetime import datetime

from .economia import EXECUCOES_POR_MES, MINUTOS_RELATORIO, SEGUNDOS_POR_LINHA, formatar_tempo
from .metricas import LIMITE_ATRASO_MIN


def reais(valor):
    """1234.5 -> 'R$ 1.234,50'"""
    return "R$ " + f"{valor:,.2f}".replace(",", "_").replace(".", ",").replace("_", ".")


def salvar_csv(pedidos, arquivo):
    with arquivo.open("w", newline="", encoding="utf-8") as f:
        escritor = csv.writer(f)
        escritor.writerow(["id_pedido", "restaurante", "prato", "valor", "status",
                           "horario_pedido", "horario_entrega", "minutos_entrega"])
        for p in pedidos:
            escritor.writerow([
                p.id_pedido, p.restaurante, p.prato, f"{p.valor:.2f}", p.status,
                f"{p.horario_pedido:%d/%m/%Y %H:%M}",
                f"{p.horario_entrega:%d/%m/%Y %H:%M}" if p.horario_entrega else "",
                f"{p.minutos_entrega:.0f}" if p.minutos_entrega is not None else "",
            ])


def montar_markdown(linhas_lidas, duplicados, problemas, geral, por_restaurante, top_pratos, economia):
    r = ["# Relatório de pedidos", "", f"Gerado em {datetime.now():%d/%m/%Y %H:%M}.", ""]

    r += ["## Visão geral", ""]
    r += [
        f"- Linhas lidas: **{linhas_lidas}** "
        f"(duplicadas removidas: {duplicados}; com problema: {len(problemas)})",
        f"- Pedidos únicos: **{geral.total}**",
        f"- Faturamento (entregues): **{reais(geral.faturamento)}**",
        f"- Ticket médio: **{reais(geral.ticket_medio)}**",
        f"- Tempo médio de entrega: **{geral.tempo_medio:.0f} min**",
        f"- Entregas atrasadas (> {LIMITE_ATRASO_MIN} min): **{geral.taxa_atraso:.0%}**",
        f"- Taxa de cancelamento: **{geral.taxa_cancelamento:.0%}**",
        "",
    ]

    r += ["## Por restaurante", ""]
    r += ["| Restaurante | Pedidos | Faturamento | Ticket médio | Tempo médio | Atrasos | Cancelamentos |",
          "|---|---|---|---|---|---|---|"]
    for nome, s in por_restaurante.items():
        r.append(f"| {nome} | {s.total} | {reais(s.faturamento)} | {reais(s.ticket_medio)} | "
                 f"{s.tempo_medio:.0f} min | {s.taxa_atraso:.0%} | {s.taxa_cancelamento:.0%} |")
    r.append("")

    r += ["## Pratos mais vendidos", "", "| # | Prato | Pedidos |", "|---|---|---|"]
    r += [f"| {i} | {prato} | {qtd} |" for i, (prato, qtd) in enumerate(top_pratos, start=1)]
    r.append("")

    if problemas:
        r += ["## Linhas com problema (ignoradas)", ""]
        r += [f"- {p}" for p in problemas]
        r.append("")

    r += ["## Tempo economizado", "", "| | Tempo |", "|---|---|",
          f"| Manual (estimado) | {formatar_tempo(economia.segundos_manual)} |",
          f"| Com o script (medido) | {formatar_tempo(economia.segundos_script)} |",
          f"| Economia por execução | {formatar_tempo(economia.segundos_economizados)} |",
          f"| Economia por mês ({EXECUCOES_POR_MES} execuções) | {economia.horas_por_mes:.1f} horas |",
          "",
          f"Estimativa manual: {SEGUNDOS_POR_LINHA}s por linha × {linhas_lidas} linhas "
          f"+ {MINUTOS_RELATORIO} min para montar o resumo.", ""]
    return "\n".join(r)
