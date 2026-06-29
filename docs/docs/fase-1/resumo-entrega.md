# Resumo da Entrega — Fase 1

Esta página reúne as principais informações da entrega para uma leitura rápida pelos avaliadores.

## Acesso Rápido

| Material | Link |
|---|---|
| Apresentação HTML | [Abrir slides](slides.html) |
| Apresentação PDF | [Baixar PDF](<Tech Challenge _ NPS e atraso na entrega.pdf>){ download } |
| Vídeo executivo | [Assistir no YouTube](https://youtu.be/eodKtPdOVdg) |
| EDA final | [Abrir página de EDA](eda.md) |
| Notebook final | [Abrir no GitHub](https://github.com/PHRaulino-Space/tech-challenge-fiap/blob/main/notebooks/eda_final.ipynb) |
| Como reproduzir | [Ver instruções](getting-started.md) |
| Avaliação da entrega | [Ver checklist](avaliacao-entrega.md) |

---

## Mensagem Central

O desafio começou com a pergunta: **como antecipar a satisfação do cliente medida pelo NPS?**

A EDA mostrou que a resposta mais acionável não é apenas prever a nota final. O principal fator associado ao baixo score de NPS é o **descumprimento do prazo prometido de entrega**. Por isso, a solução proposta desloca o foco:

| Leitura inicial | Conclusão após a EDA |
|---|---|
| Prever a nota de NPS antes da pesquisa | Prever/calibrar melhor o prazo de entrega e o risco de atraso |
| `nps_score` como alvo direto | `nps_score` como desfecho e métrica de impacto |
| Ação quando o cliente já está em risco | Ação antes da quebra da promessa logística |

**Síntese:** NPS é o termômetro da experiência; atraso é a alavanca operacional.

---

## Números-Chave

| Indicador | Resultado |
|---|---:|
| Clientes analisados | 2.500 |
| Detratores | 1.851 (74,0%) |
| Promotores | 201 (8,0%) |
| Nota média do score de NPS | 4,38 |
| Clientes com atraso | 2.223 (88,9%) |
| Clientes no perfil "Atraso + SAC" | 1.734 (69,4%) |
| Detratores vindos de "Atraso + SAC" | 1.431 (77,3%) |
| Recompra de detratores em 30 dias | 0,0% |
| Recompra de promotores em 30 dias | 100,0% |

---

## Principais Achados

| Achado | Evidência | Implicação |
|---|---|---|
| Perfil do cliente não explica o baixo score | Idade, região e tempo de relacionamento têm correlação próxima de zero | Não é um problema de segmentação demográfica |
| Pedido não explica a insatisfação | Valor, desconto, itens e parcelas têm correlação próxima de zero | A solução não está em pricing ou promoções |
| Logística é o maior sinal | `delivery_delay_days` tem correlação -0,60 com `nps_score` | A prioridade é cumprimento de prazo |
| Atendimento reforça a degradação | Reclamações e contatos ao SAC têm correlação negativa com o score | SAC deve atuar como recuperação, não como solução principal |
| O problema é sistêmico | Atraso varia de 88% a 91% nas regiões | Não é uma correção regional pontual |
| Cumprir prazo importa mais que velocidade | `delivery_time_days` ≈ 0; atraso tem forte relação negativa | Prometer prazo realista é mais importante que prometer prazo curto |

---

## Conclusão Analítica

A empresa não tem um problema concentrado em perfil de cliente, região, valor de pedido ou desconto. O problema aparece depois da compra, na execução operacional.

O ponto de ruptura é a promessa logística: clientes que recebem fora do prazo prometido têm nota média do score de NPS muito inferior aos clientes que recebem no prazo.

| Status da entrega | Clientes | Nota média do score de NPS |
|---|---:|---:|
| No prazo | 277 | 6,86 |
| Atrasado | 2.223 | 4,07 |

---

## Solução Proposta

A solução recomendada é um sistema de **previsão e calibração de prazo de entrega**, com duas camadas:

| Camada | Objetivo | Uso prático |
|---|---|---|
| Previsão de prazo | Estimar prazo de entrega mais realista | Melhorar promessa feita ao cliente |
| Risco de atraso | Identificar pedidos com maior chance de descumprir o prazo | Priorizar operação e comunicação proativa |

O NPS continua sendo usado como métrica final de validação: se a empresa melhora a previsão de prazo e reduz atrasos, espera-se queda no percentual de detratores e aumento de recompra.

---

## Recomendações de Negócio

### Logística

- Calibrar prazos prometidos com base em risco real de atraso.
- Tratar atraso como problema sistêmico, não regional.
- Priorizar pedidos com maior chance de quebrar o SLA prometido.

### Atendimento

- Atuar proativamente nos clientes com atraso previsto.
- Priorizar clientes do perfil "Atraso + SAC".
- Reduzir tempo de resolução para atenuar o dano quando o atraso já aconteceu.

### Experiência do Cliente

- Comunicar risco de atraso antes que o cliente precise abrir reclamação.
- Testar mensagens transparentes de atualização de prazo.
- Medir impacto em detratores e recompra.

---

## Limitações

| Limitação | Impacto |
|---|---|
| A análise é correlacional | Não prova causalidade estatística |
| Não há data de cada evento | Limita avaliação temporal precisa |
| Não há CEP, transportadora, rota ou centro de distribuição | Limita um modelo produtivo de previsão de prazo |
| `repeat_purchase_30d` ocorre depois da experiência | Deve ser usado como validação, não como feature preditiva inicial |
| Modelo não foi implementado em produção | A entrega traz proposta de solução, conforme item opcional do case |

---

## Entregáveis Disponíveis

| Entrega | Status | Link |
|---|---|---|
| Entendimento do negócio | Concluído | [Problema de Negócio](problema-negocio.md) |
| Business Canvas | Concluído | [Business Canvas](business-canvas.md) |
| Análise e hipóteses | Concluído | [Análise e Hipóteses](analise-hipoteses.md) |
| EDA final | Concluído | [EDA](eda.md) |
| Preparação dos dados | Concluído | [Preparação dos Dados](preparacao-dados.md) |
| Proposta de solução | Concluído | [Proposta de Solução](proposta-solucao.md) |
| Avaliação dos resultados | Concluído | [Avaliação](avaliacao.md) |
| Apresentação final | Concluído | [Apresentação Final](apresentacao-final.md) |
| Vídeo executivo | Concluído | [YouTube](https://youtu.be/eodKtPdOVdg) |

---

## Veredito

A entrega atende aos requisitos obrigatórios do case e apresenta uma conclusão acionável para negócio. O principal valor está na clareza da análise: o baixo score de NPS é tratado como efeito de uma falha operacional mensurável, e a recomendação final aponta para uma solução preventiva baseada em previsão de prazo e gestão de risco de atraso.
