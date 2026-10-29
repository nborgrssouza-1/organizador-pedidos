"""Junta as planilhas de pedidos dos restaurantes, limpa os dados e gera o relatório do dia.

Uso:
    python3 main.py
    python3 main.py --entrada outra_pasta --saida resultados
"""

import argparse
import time
from pathlib import Path

from pedidos import leitura, metricas, relatorio
from pedidos.economia import Economia, formatar_tempo

PASTA = Path(__file__).parent


def main():
    parser = argparse.ArgumentParser(description="Organiza planilhas de pedidos de delivery.")
    parser.add_argument("--entrada", type=Path, default=PASTA / "entrada", help="pasta com os CSVs")
    parser.add_argument("--saida", type=Path, default=PASTA / "saida", help="pasta dos resultados")
    args = parser.parse_args()

    if not any(args.entrada.glob("*.csv")):
        parser.exit(1, f"Nenhum CSV em {args.entrada}. Rode antes: python3 gerar_exemplos.py\n")

    inicio = time.perf_counter()

    pedidos, problemas = leitura.ler_pasta(args.entrada)
    unicos = leitura.remover_duplicados(pedidos)
    geral, por_restaurante, top_pratos = metricas.calcular(unicos)

    linhas_lidas = len(pedidos) + len(problemas)
    args.saida.mkdir(parents=True, exist_ok=True)
    relatorio.salvar_csv(unicos, args.saida / "pedidos_organizados.csv")
    economia = Economia(linhas_lidas, time.perf_counter() - inicio)
    markdown = relatorio.montar_markdown(
        linhas_lidas, len(pedidos) - len(unicos), problemas, geral, por_restaurante, top_pratos, economia
    )
    (args.saida / "relatorio.md").write_text(markdown, encoding="utf-8")

    print(f"Linhas lidas: {linhas_lidas} | pedidos únicos: {len(unicos)} | com problema: {len(problemas)}")
    print(f"Faturamento: {relatorio.reais(geral.faturamento)} | ticket médio: {relatorio.reais(geral.ticket_medio)}")
    print(f"Tempo manual estimado: {formatar_tempo(economia.segundos_manual)}")
    print(f"Tempo do script:       {formatar_tempo(economia.segundos_script)}")
    print(f"Economia por mês:      {economia.horas_por_mes:.1f} horas")
    print(f"Resultados em: {args.saida}")


if __name__ == "__main__":
    main()
