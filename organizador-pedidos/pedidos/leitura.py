"""Lê as planilhas exportadas pelos restaurantes e transforma cada linha em um Pedido padronizado."""

import csv
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path

STATUS_PADRAO = {
    "entregue": "Entregue", "finalizado": "Entregue", "concluido": "Entregue", "concluído": "Entregue",
    "cancelado": "Cancelado", "cancelada": "Cancelado", "estornado": "Cancelado",
}
PALAVRAS_MINUSCULAS = {"da", "de", "do", "das", "dos", "e"}
FORMATOS_HORARIO =("%d/%m/%Y %H:%M", "%Y-%m-%d %H:%M", "%Y-%m-%dT%H:%M:%S")


@dataclass
class Pedido:
    id_pedido: str
    restaurante: str
    prato: str
    valor: float
    status: str
    horario_pedido: datetime
    horario_entrega: datetime | None

    @property
    def minutos_entrega(self):
        if self.horario_entrega is None:
            return None
        return (self.horario_entrega - self.horario_pedido).total_seconds() / 60


def padronizar_texto(texto):
    """'  burger DA esquina ' -> 'Burger da Esquina'"""
    palavras = texto.lower().split()
    return " ".join(
        p if i > 0 and p in PALAVRAS_MINUSCULAS else p.capitalize() for i, p in enumerate(palavras)
    )


def padronizar_valor(texto):
    """Aceita 'R$ 32,90', '32.90', '1.234,50' e devolve float."""
    limpo = texto.replace("R$", "").strip()
    if "," in limpo:
        limpo = limpo.replace(".", "").replace(",", ".")
    try:
        valor = float(limpo)
    except ValueError:
        raise ValueError(f"Valor inválido: {texto!r}") from None
    if valor < 0:
        raise ValueError(f"Valor negativo: {texto!r}")
    return valor


def padronizar_status(texto):
    chave = texto.strip().lower()
    if chave not in STATUS_PADRAO:
        raise ValueError(f"Status desconhecido: {texto!r}")
    return STATUS_PADRAO[chave]


def padronizar_horario(texto):
    texto = texto.strip()
    if not texto:
        return None
    for formato in FORMATOS_HORARIO:
        try:
            return datetime.strptime(texto, formato)
        except ValueError:
            pass
    raise ValueError(f"Horário em formato desconhecido: {texto!r}")


def linha_para_pedido(linha):
    pedido = Pedido(
        id_pedido=linha["id_pedido"].strip().upper(),
        restaurante=padronizar_texto(linha["restaurante"]),
        prato=padronizar_texto(linha["prato"]),
        valor=padronizar_valor(linha["valor"]),
        status=padronizar_status(linha["status"]),
        horario_pedido=padronizar_horario(linha["horario_pedido"]),
        horario_entrega=padronizar_horario(linha["horario_entrega"]),
    )
    if pedido.horario_pedido is None:
        raise ValueError("Pedido sem horário")
    if pedido.status == "Entregue" and pedido.horario_entrega is None:
        raise ValueError("Pedido entregue sem horário de entrega")
    return pedido


def ler_pasta(pasta: Path):
    """Devolve (pedidos válidos, mensagens das linhas com problema)."""
    pedidos, problemas = [], []
    for arquivo in sorted(pasta.glob("*.csv")):
        with arquivo.open(encoding="utf-8") as f:
            for numero, linha in enumerate(csv.DictReader(f), start=2):
                try:
                    pedidos.append(linha_para_pedido(linha))
                except (ValueError, KeyError, AttributeError) as erro:
                    problemas.append(f"{arquivo.name}, linha {numero}: {erro}")
    return pedidos, problemas


def remover_duplicados(pedidos):
    """O mesmo pedido pode aparecer em duas exportações; fica a primeira ocorrência."""
    vistos = {}
    for pedido in pedidos:
        vistos.setdefault(pedido.id_pedido, pedido)
    return sorted(vistos.values(), key=lambda p: p.horario_pedido)
