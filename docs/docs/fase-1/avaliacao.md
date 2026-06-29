# 8. Avaliação dos Resultados

*CRISP-DM: Evaluation*

A avaliação final verifica se a análise respondeu ao problema de negócio: entender quais fatores operacionais influenciam o NPS e propor uma forma de agir antes que o cliente vire detrator.

O principal resultado da avaliação é a mudança explícita de foco: a previsão direta do NPS é útil como diagnóstico, mas a solução mais acionável é prever/calibrar o prazo de entrega, porque o atraso é o fator operacional mais associado à insatisfação.

---

## Resposta ao Problema de Negócio

O problema inicial era que a empresa só conhecia o NPS depois do encerramento da jornada, tarde demais para agir preventivamente. A EDA mostrou que existem sinais operacionais claros antes ou durante essa jornada.

| Pergunta | Resposta encontrada |
|---|---|
| O baixo NPS está ligado ao perfil do cliente? | Não. Idade, região e tempo de relacionamento têm correlação próxima de zero. |
| O pedido explica a insatisfação? | Não. Valor, desconto, itens e parcelamento quase não se associam ao NPS. |
| Onde a experiência se rompe? | Na execução pós-compra: entrega e atendimento. |
| Qual variável tem maior sinal? | `delivery_delay_days`, com correlação -0,60. |
| O problema é regional? | Não. Atrasos variam de 88% a 91% em todas as regiões. |
| O NPS se conecta a comportamento real? | Sim. Detratores tiveram 0,0% de recompra em 30 dias. |
| Qual deve ser o alvo operacional da solução? | Previsão de prazo/risco de atraso, com NPS como métrica de impacto. |

---

## Evidências Principais

| Achado | Evidência |
|---|---|
| Base dominada por insatisfação | 74,0% detratores e NPS médio 4,38 |
| Atraso é o principal fator operacional | `delivery_delay_days`: correlação -0,60 |
| Atendimento também sinaliza degradação | `complaints_count`: -0,50; `customer_service_contacts`: -0,35 |
| Cumprir o prazo importa mais que velocidade | No prazo: NPS 6,86; atrasado: NPS 4,07 |
| Problema é sistêmico | 88% a 91% de atraso em todas as regiões |
| Atraso + SAC concentra o dano | 69,4% da base e 77,3% dos detratores |
| Recompra valida o impacto | 0,0% dos detratores recompraram em 30 dias |
| SAC atenua, mas não reverte | Resolução rápida melhora 1,53 ponto no pior perfil, ainda em faixa detratora |

---

## Avaliação das Hipóteses

| Hipótese | Status | Justificativa |
|---|---|---|
| Perfil do cliente explica variação do NPS | Rejeitada | Correlações praticamente nulas e baixa variação regional. |
| Pedido, preço ou desconto explicam satisfação | Rejeitada | Variáveis de pedido ficaram próximas de zero. |
| Cumprimento do prazo pesa mais que tempo total | Confirmada | Atraso tem correlação -0,60; tempo total de entrega ≈ 0. |
| Atendimento está associado ao baixo NPS | Confirmada | Reclamações e contatos ao SAC têm sinais relevantes. |
| O problema é regional | Rejeitada | Taxa de atraso homogênea entre regiões. |
| NPS tem relação com recompra | Confirmada | Detratores não recompraram; promotores recompraram 100%. |

---

## Avaliação da Troca de Chave

| Dimensão | Antes da EDA | Depois da EDA |
|---|---|---|
| Pergunta principal | Como prever a nota de NPS? | Como prever melhor a entrega para evitar baixo NPS? |
| Variável de referência | `nps_score` | `delivery_delay_days`, `entregou_no_prazo`, prazo estimado |
| Papel do NPS | Alvo direto do modelo | Métrica final de experiência |
| Ponto de ação | Cliente já em risco de detração | Promessa logística antes da frustração |
| Área prioritária | CX/Analytics | Logística, CX e Atendimento |

A mudança é justificável porque a EDA mostrou que perfil, região e pedido quase não explicam NPS. O que explica é a quebra da promessa operacional. Portanto, a solução deve mirar a promessa, não apenas a nota.

---

## Limitações

### Correlação não é causalidade

A análise mostra associação forte entre atraso, atendimento e NPS, mas não prova causalidade estatística. Ainda assim, os achados são operacionalmente úteis porque indicam onde agir.

### Momento exato das variáveis

O dataset não informa a data de cada evento. Para um modelo produtivo, seria necessário garantir que cada feature esteja disponível antes da pesquisa de NPS.

### Desbalanceamento da base

Com 74,0% de detratores, métricas ingênuas podem enganar em um modelo direto de NPS. No modelo operacional de atraso, o mesmo cuidado vale para a classe "atrasado": a avaliação deve priorizar recall de atrasos relevantes, erro médio de prazo e calibragem da probabilidade de atraso.

### Recorte da base

A base pode representar um período ou contexto com alta concentração de problemas operacionais. As conclusões devem ser validadas em novas amostras antes de virar política definitiva.

### Variáveis ausentes

O dataset não traz produto, categoria, transportadora, CEP, distância, centro de distribuição, prazo prometido original, canal de atendimento, custo de intervenção ou histórico completo do cliente. Essas variáveis são especialmente importantes para transformar a proposta de previsão de prazo em um modelo produtivo.

---

## Recomendações Finais

### Prioridade 1 — Logística

Construir previsão de prazo mais realista e calibrar prazos prometidos. A análise mostra que a frustração vem mais do descumprimento do prazo do que do tempo total de entrega.

### Prioridade 2 — Atendimento

Priorizar clientes no perfil "Atraso + SAC". A resolução rápida atenua a queda do NPS, mas não reverte totalmente o dano.

### Prioridade 3 — Comunicação Proativa

Avisar sobre risco de atraso antes do cliente acionar o SAC. Essa intervenção pode reduzir reclamações, ansiedade e contatos reativos.

### Prioridade 4 — Analytics

Implementar um modelo de previsão de prazo/risco de atraso e usar NPS, detratores e recompra como métricas de validação do impacto.

---

## Conclusão

A análise confirma que o baixo NPS não é um problema demográfico nem comercial. É um problema operacional, concentrado em promessa de entrega não cumprida e atendimento. A solução deve combinar previsão de prazo, comunicação proativa e recuperação rápida quando o atraso já aconteceu.

Assim, o projeto parte de NPS preditivo, mas chega a uma recomendação mais prática: **prever melhor a entrega para prevenir a queda do NPS**.
