"""Gera planilhas de pedidos de exemplo, como se cada restaurante exportasse a sua.

Os dados vêm "bagunçados" de propósito, como acontece na vida real:
- valores como "R$ 32,90", "32.90" ou "32,9"
- status com nomes diferentes ("Entregue", "finalizado", "CANCELADO ")
- horários em formatos diferentes
- nomes com maiúsculas/minúsculas e espaços misturados
- pedidos repetidos (exportados duas vezes) e algumas linhas com erro

Uso:
    python3 gerar_exemplos.py            # 4 restaurantes, 150 pedidos cada
    python3 gerar_exemplos.py 6 1000     # 6 restaurantes, 1000 pedidos cada
"""

import csv
import random
import sys
from datetime import datetime, timedelta
from pathlib import Path

PASTA_ENTRADA = Path(__file__).parent / "entrada"

CARDAPIOS = {
    "Pizzaria Bella Massa": [("Pizza Calabresa", 49.90), ("Pizza Margherita", 52.90), ("Pizza Frango Catupiry", 56.90)],
    "Burger da Esquina": [("X-Burger", 28.90), ("X-Bacon", 33.90), ("Combo Smash", 42.50)],
    "Sushi Kento": [("Combo 20 Peças", 69.90), ("Temaki Salmão", 31.90), ("Hot Roll", 26.90)],
    "Marmitaria Sabor Caseiro": [("Marmita Frango", 22.90), ("Marmita Feijoada", 29.90), ("Marmita Fit", 25.90)],
    "Açaí Tropical": [("Açaí 500ml", 21.90), ("Açaí 700ml", 27.90), ("Cupuaçu 500ml", 23.90)],
    "Pastelaria Japa": [("Pastel Carne", 12.90), ("Pastel Queijo", 11.90), ("Combo 3 Pastéis", 32.90)],
}
STATUS = {"entregue": ["Entregue", "entregue", "FINALIZADO", "concluído"],
          "cancelado": ["Cancelado", "CANCELADO ", "cancelada", "estornado"]}
FORMATOS = ["%d/%m/%Y %H:%M", "%Y-%m-%d %H:%M", "%Y-%m-%dT%H:%M:%S"]


def valor_baguncado(valor):
    return random.choice([f"R$ {valor:.2f}".replace(".", ","), f"{valor:.2f}", f"{valor:.2f}".replace(".", ",")])


def texto_baguncado(texto):
    return random.choice([texto, texto.lower(), texto.upper(), f"  {texto} "])


def gerar_linha(numero, restaurante, inicio_dia):
    prato, valor = random.choice(CARDAPIOS[restaurante])
    horario = inicio_dia + timedelta(minutes=random.randint(0, 12 * 60))
    cancelado = random.random() < 0.08
    entrega = "" if cancelado else (horario + timedelta(minutes=random.randint(18, 58))).strftime(random.choice(FORMATOS))
    return [
        f"PED-{numero:05d}",
        texto_baguncado(restaurante),
        texto_baguncado(prato),
        valor_baguncado(valor),
        random.choice(STATUS["cancelado" if cancelado else "entregue"]),
        horario.strftime(random.choice(FORMATOS)),
        entrega,
    ]


def gerar(qtd_restaurantes=4, pedidos_por_restaurante=150, semente=7):
    random.seed(semente)
    PASTA_ENTRADA.mkdir(exist_ok=True)
    for antigo in PASTA_ENTRADA.glob("*.csv"):
        antigo.unlink()

    inicio_dia = datetime(2026, 10, 28, 11, 0)
    numero = 0
    for restaurante in list(CARDAPIOS)[:qtd_restaurantes]:
        linhas = []
        for _ in range(pedidos_por_restaurante):
            numero += 1
            linhas.append(gerar_linha(numero, restaurante, inicio_dia))
        # ~5% dos pedidos exportados duas vezes
        linhas += random.sample(linhas, k=max(1, pedidos_por_restaurante // 20))
        # duas linhas com erro de digitação, para mostrar o tratamento de problemas
        linhas[random.randrange(len(linhas))][3] = "trinta reais"
        linhas[random.randrange(len(linhas))][4] = "a caminho?"
        random.shuffle(linhas)

        arquivo = PASTA_ENTRADA / f"pedidos_{restaurante.split()[0].lower()}.csv"
        with arquivo.open("w", newline="", encoding="utf-8") as f:
            escritor = csv.writer(f)
            escritor.writerow(["id_pedido", "restaurante", "prato", "valor", "status", "horario_pedido", "horario_entrega"])
            escritor.writerows(linhas)
        print(f"Criado: {arquivo.name} ({len(linhas)} linhas)")


if __name__ == "__main__":
    gerar(*[int(a) for a in sys.argv[1:3]])
