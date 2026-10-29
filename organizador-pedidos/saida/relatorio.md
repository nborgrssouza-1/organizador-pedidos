# Relatório de pedidos

Gerado em 29/10/2026 18:35.

## Visão geral

- Linhas lidas: **628** (duplicadas removidas: 27; com problema: 9)
- Pedidos únicos: **592**
- Faturamento (entregues): **R$ 21.225,30**
- Ticket médio: **R$ 39,53**
- Tempo médio de entrega: **38 min**
- Entregas atrasadas (> 45 min): **30%**
- Taxa de cancelamento: **9%**

## Por restaurante

| Restaurante | Pedidos | Faturamento | Ticket médio | Tempo médio | Atrasos | Cancelamentos |
|---|---|---|---|---|---|---|
| Burger da Esquina | 148 | R$ 4.674,60 | R$ 34,89 | 38 min | 31% | 9% |
| Marmitaria Sabor Caseiro | 148 | R$ 3.534,60 | R$ 26,38 | 38 min | 32% | 9% |
| Pizzaria Bella Massa | 148 | R$ 7.048,70 | R$ 53,00 | 38 min | 30% | 10% |
| Sushi Kento | 148 | R$ 5.967,40 | R$ 43,88 | 37 min | 26% | 8% |

## Pratos mais vendidos

| # | Prato | Pedidos |
|---|---|---|
| 1 | Pizza Calabresa | 53 |
| 2 | X-burger | 51 |
| 3 | Temaki Salmão | 49 |
| 4 | Marmita Fit | 48 |
| 5 | Combo 20 Peças | 48 |

## Linhas com problema (ignoradas)

- pedidos_burger.csv, linha 31: Status desconhecido: 'a caminho?'
- pedidos_burger.csv, linha 61: Valor inválido: 'trinta reais'
- pedidos_marmitaria.csv, linha 18: Valor inválido: 'trinta reais'
- pedidos_marmitaria.csv, linha 58: Status desconhecido: 'a caminho?'
- pedidos_pizzaria.csv, linha 57: Status desconhecido: 'a caminho?'
- pedidos_pizzaria.csv, linha 132: Valor inválido: 'trinta reais'
- pedidos_sushi.csv, linha 14: Status desconhecido: 'a caminho?'
- pedidos_sushi.csv, linha 50: Valor inválido: 'trinta reais'
- pedidos_sushi.csv, linha 136: Valor inválido: 'trinta reais'

## Tempo economizado

| | Tempo |
|---|---|
| Manual (estimado) | 2h 57min |
| Com o script (medido) | 76 ms |
| Economia por execução | 2h 57min |
| Economia por mês (30 execuções) | 88.5 horas |

Estimativa manual: 15s por linha × 628 linhas + 20 min para montar o resumo.
