# Organizador de Pedidos de Delivery

Programa em Python que automatiza o fechamento diário de pedidos: junta as planilhas exportadas por vários restaurantes, corrige os dados bagunçados, remove pedidos repetidos e gera um relatório com os principais indicadores do dia. Também calcula quanto tempo a automação economiza em comparação com fazer tudo à mão.

## O problema

Todo dia, alguém da operação precisa:

1. Abrir a planilha de cada restaurante.
2. Copiar tudo para uma planilha única.
3. Corrigir valores (`R$ 32,90`, `32.90`, `32,9`), status (`Entregue`, `FINALIZADO`, `concluído`) e horários em formatos diferentes.
4. Procurar e apagar pedidos exportados duas vezes.
5. Calcular faturamento, ticket médio, tempo de entrega, atrasos e cancelamentos por restaurante.
6. Montar o resumo e o ranking dos pratos mais vendidos.

É uma tarefa repetitiva e lenta, em que é fácil errar.

## A solução

```
entrada/*.csv  ──►  leitura e limpeza  ──►  remoção de duplicados  ──►  métricas  ──►  saida/
                    (pedidos/leitura.py)                                (metricas.py)  ├─ pedidos_organizados.csv
                                                                                       └─ relatorio.md
```

Linhas com erro (por exemplo, valor `"trinta reais"`) não interrompem o programa. Elas são listadas no relatório com o nome do arquivo e o número da linha, para que alguém corrija na origem.

## Tempo economizado

Resultado com os dados de exemplo (4 restaurantes, 628 linhas):

| | Tempo |
|---|---|
| Manual (estimado) | ~2h 57min |
| Com o script (medido) | menos de 0,1 segundo |
| Economia por mês (30 fechamentos) | **~88 horas** |

A estimativa do tempo manual considera 15 segundos por linha (copiar, corrigir e conferir) mais 20 minutos para montar o resumo. Esses números ficam em [`pedidos/economia.py`](pedidos/economia.py) e podem ser ajustados depois de cronometrar a tarefa real. O tempo do script é medido de verdade a cada execução.

Veja o relatório gerado: [saida/relatorio.md](saida/relatorio.md)

## Como rodar

Só precisa do Python 3.10 ou mais recente, sem instalar nenhuma biblioteca.

```bash
python3 gerar_exemplos.py          # cria planilhas de exemplo em entrada/
python3 main.py                    # organiza e gera o relatório em saida/
python3 -m unittest discover -v    # roda os testes automatizados
```

Opções:

```bash
python3 gerar_exemplos.py 6 1000             # 6 restaurantes com 1000 pedidos cada
python3 main.py --entrada minhas_planilhas --saida resultados
```

## Estrutura do código

| Arquivo | Responsabilidade |
|---|---|
| `main.py` | Comando de terminal: junta as etapas e mede o tempo |
| `pedidos/leitura.py` | Lê os CSVs, padroniza cada campo e remove duplicados |
| `pedidos/metricas.py` | Calcula faturamento, ticket médio, atrasos, cancelamentos e top pratos |
| `pedidos/relatorio.py` | Gera o CSV limpo e o relatório em Markdown |
| `pedidos/economia.py` | Compara o tempo manual com o automatizado |
| `tests/test_pedidos.py` | Testes automatizados com `unittest` |
| `gerar_exemplos.py` | Cria dados de exemplo com problemas reais de formatação |

## O que pratiquei

- Leitura e escrita de CSV com a biblioteca padrão (`csv`, `pathlib`)
- Limpeza e padronização de dados (valores em reais, datas, textos)
- `dataclasses` e `@property` para modelar pedidos e indicadores
- Tratamento de erros sem interromper o processamento
- Linha de comando com `argparse`
- Testes automatizados com `unittest`
- Código separado em módulos com responsabilidades claras
