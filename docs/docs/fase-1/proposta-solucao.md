# 7. Proposta de Solução

*CRISP-DM: Modeling*

A proposta final é um sistema de **previsão e calibração de prazo de entrega**, orientado pela relação entre atraso e NPS revelada na EDA.

Essa é a principal troca de chave do projeto. A pergunta inicial era: "como prever o NPS antes da pesquisa?". A análise mostrou que a pergunta mais acionável é: **como prever melhor a entrega para evitar que o cliente vire detrator?**

O NPS continua sendo essencial, mas muda de papel: deixa de ser apenas uma nota a ser prevista e passa a ser o indicador que valida se a operação logística está entregando uma experiência melhor.

---

## Formulação do Problema

A EDA mostrou três pontos decisivos:

| Evidência | Interpretação |
|---|---|
| `delivery_delay_days` tem correlação -0,60 com NPS | O atraso é o maior sinal operacional da base |
| `delivery_time_days` tem correlação ≈ 0 com NPS | O cliente não reage apenas ao tempo total, mas ao prazo prometido |
| Entregas no prazo têm NPS 6,86; atrasadas têm NPS 4,07 | Cumprir a promessa muda a percepção |

Por isso, a modelagem recomendada passa a ter dois níveis:

| Camada | Pergunta | Alvo |
|---|---|---|
| Operacional | Qual prazo de entrega é mais realista para este pedido? | `delivery_time_days` ou prazo estimado |
| Risco de atraso | Este pedido tende a chegar fora do prazo prometido? | `entregou_no_prazo` / `delivery_delay_days` |
| Experiência | A melhoria logística reduziu detratores? | `nps_score`, `nps_categoria`, recompra |

Na prática, o modelo principal deve apoiar a promessa logística. O NPS entra como métrica de negócio para medir se a promessa mais assertiva reduz insatisfação.

---

## Alvo Operacional Recomendado

A solução pode começar por uma das duas formulações abaixo.

| Formulação | Alvo | Uso |
|---|---|---|
| Regressão de prazo | Estimar dias de entrega | Definir prazo prometido mais realista |
| Classificação de atraso | Prever no prazo vs. atrasado | Priorizar pedidos com risco e comunicação proativa |

Como a base atual já contém `delivery_time_days` e `delivery_delay_days`, ela permite simular essa lógica. Para produção, seria necessário enriquecer a base com variáveis disponíveis no momento da promessa, como CEP, distância, transportadora, centro de distribuição, estoque, calendário e histórico por rota.

---

## Features Candidatas

### Disponíveis no momento do pedido

- `customer_region`
- `customer_tenure_months`
- `order_value`
- `items_quantity`
- `discount_value`
- `payment_installments`
- `freight_value`

Essas variáveis podem apoiar uma primeira estimativa, mas provavelmente não bastam para um modelo robusto de prazo. A ausência de rota, transportadora e localização detalhada é uma limitação importante.

### Disponíveis durante ou depois da jornada

- `delivery_attempts`
- `customer_service_contacts`
- `resolution_time_days`
- `complaints_count`
- `delivery_delay_days`

Essas variáveis são úteis para uma camada de monitoramento e recuperação, mas não devem ser usadas para prometer o prazo inicial se ainda não existem no momento do checkout.

---

## Arquitetura Recomendada

| Etapa | Saída | Ação de negócio |
|---|---|---|
| Previsão de prazo | Prazo estimado por pedido | Prometer prazo mais realista |
| Previsão de atraso | Probabilidade de descumprir o prazo | Priorizar operação e comunicação |
| Monitoramento da jornada | Sinais de degradação | Acionar SAC antes da reclamação |
| Validação por NPS | NPS, detratores e recompra | Medir impacto da melhoria |

Essa arquitetura é mais forte do que prever o NPS diretamente, porque permite agir antes da insatisfação se consolidar.

---

## Modelos Iniciais

| Objetivo | Modelos candidatos | Métricas |
|---|---|---|
| Estimar prazo de entrega | Regressão Linear, Random Forest Regressor, Gradient Boosting | MAE, RMSE, erro por região |
| Classificar risco de atraso | Regressão Logística, Árvore de Decisão, Random Forest Classifier | Recall de atrasos, precision, F1, matriz de confusão |
| Explicar impacto em NPS | Regressão/árvore interpretável sobre NPS | Importância de variáveis, comparação por segmentos |

O primeiro baseline deve ser simples e interpretável. A meta não é ter o modelo mais complexo, mas melhorar a promessa operacional e reduzir a diferença entre prazo prometido e prazo real.

---

## Régua de Ação

| Risco previsto | Situação | Ação recomendada |
|---|---|---|
| Baixo | Prazo estimado confiável | Fluxo normal |
| Médio | Possível atraso leve | Prometer prazo conservador e monitorar |
| Alto | Alta chance de atraso | Ajustar prazo, priorizar pedido e comunicar cliente |
| Crítico | Atraso provável + SAC/reclamação | Atendimento proativo e recuperação da experiência |

O foco é evitar que o cliente descubra o problema sozinho. A comunicação antecipada não elimina o atraso, mas reduz a quebra de expectativa.

---

## Como Medir Sucesso

O sucesso da solução deve ser avaliado em duas camadas.

### Métricas operacionais

- Redução do erro médio de previsão do prazo.
- Aumento do percentual de pedidos entregues no prazo prometido.
- Redução de pedidos no perfil "Atraso + SAC".
- Redução de contatos e reclamações relacionadas à entrega.

### Métricas de experiência

- Redução do percentual de detratores.
- Aumento do NPS médio dos pedidos com risco logístico.
- Aumento de recompra em 30 dias.
- Redução da diferença de NPS entre entregas no prazo e atrasadas.

---

## Conclusão da Proposta

A solução final não descarta o NPS preditivo; ela o reposiciona. Prever NPS ajuda a medir risco, mas a EDA mostrou que o risco nasce principalmente da promessa logística não cumprida.

Por isso, a recomendação é construir primeiro uma capacidade de **prever prazo e risco de atraso**. Depois, medir se essa capacidade reduz detratores, melhora recompra e torna o NPS menos reativo.
