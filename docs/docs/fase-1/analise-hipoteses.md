# 4. Análise e Hipóteses

*CRISP-DM: Data Understanding*

---

## Visão Geral da Base

A base de dados conta com **2.500 registros** e **19 variáveis**, sem valores nulos. As variáveis estão distribuídas em quatro grupos que seguem o fluxo cronológico da jornada do cliente:

| Grupo | Variáveis | Papel na análise |
|---|---|---|
| Cliente | `customer_age`, `customer_region`, `customer_tenure_months` | Perfil de quem compra |
| Pedido | `order_value`, `items_quantity`, `discount_value`, `payment_installments` | O que foi comprado |
| Logística | `delivery_time_days`, `delivery_delay_days`, `freight_value`, `delivery_attempts` | O que aconteceu com a entrega |
| Atendimento | `customer_service_contacts`, `resolution_time_days`, `complaints_count` | Se o cliente precisou de suporte |

A variável-alvo é o `nps_score` (escala 0–10), segmentado em três categorias de negócio:

- **Detrator:** 0 a 6
- **Neutro:** 7 a 8
- **Promotor:** 9 a 10

---

## Primeiro Achado — Distribuição do NPS

Antes de qualquer análise cruzada, a distribuição da base já revela um dado relevante: a **média do NPS é 4.38**, abaixo do ponto neutro. A base pende estruturalmente para detratores — não estamos diante de casos isolados, mas de um padrão.

Isso reforça a urgência do problema: a empresa não está lidando com exceções de insatisfação, está lidando com a maioria dos seus clientes insatisfeitos.

---

## Metodologia da EDA

A análise exploratória foi estruturada seguindo o **ciclo de vida cronológico da jornada do cliente**, com o objetivo de isolar em qual etapa a experiência começa a se degradar.

Para cada grupo de variáveis, a análise combina dois tipos de visualização:

1. **Heatmap de correlação** — triagem rápida para identificar quais variáveis têm alguma relação linear com o NPS Score
2. **Boxplots por categoria NPS** — detalhamento visual para entender como a distribuição de cada variável se comporta entre Detratores, Neutros e Promotores

Para cada gráfico, são respondidas três perguntas: o que ele mostra, por que isso importa para o negócio, e qual decisão ou investigação ele sugere.

---

## O que a EDA revelou até agora

### Grupo Cliente — sem relação com o NPS

`customer_age` apresentou correlação de -0.01 e `customer_tenure_months` de 0.03 com o NPS Score. Os boxplots confirmam: as distribuições são praticamente idênticas entre Detratores, Neutros e Promotores.

**Conclusão:** a insatisfação não discrimina perfil. Um cliente novo ou antigo, jovem ou mais velho, tem a mesma chance de virar detrator. O problema não está em quem é o cliente.

### Grupo Pedido — sem relação com o NPS

Todas as variáveis do grupo — `order_value`, `items_quantity`, `discount_value` e `payment_installments` — apresentaram correlação próxima de zero com o NPS. Os boxplots mostram caixas no mesmo nível para as três categorias.

**Conclusão:** o momento da compra é neutro para a satisfação. Não importa o quanto o cliente gastou, quantos itens comprou ou em quantas parcelas pagou — isso individualmente não move o NPS.

### Grupo Logística — primeiro sinal relevante

`delivery_delay_days` apresentou correlação de **-0.6** com o NPS Score — o sinal mais forte observado até agora. Os boxplots confirmam visualmente: promotores quase não têm atraso (mediana próxima de zero), enquanto detratores têm atraso consistente (mediana em torno de 2 dias, com outliers chegando a 7-8 dias).

**Conclusão:** o atraso na entrega é o principal fator identificado até agora. Quanto maior o atraso, menor o NPS — e a relação é clara o suficiente para ser um candidato forte a feature no modelo preditivo.

---

## Hipóteses para Investigação Aprofundada

A partir dos achados da EDA, três hipóteses foram levantadas para investigação nas próximas etapas:

### Hipótese 1 — O valor do produto influencia a tolerância ao atraso

Clientes que compraram produtos mais caros têm mais tolerância a variáveis que degradam a experiência, como atraso na entrega? Ou são mais exigentes justamente por terem investido mais?

**O que analisar:** cruzar `order_value` com `delivery_delay_days` segmentado por `nps_categoria` — ver se o impacto do atraso no NPS é diferente em compras de alto valor.

### Hipótese 2 — Expectativa de prazo vs. realidade

`delivery_delay_days` mede o atraso em relação ao prazo prometido. Se o cliente foi prometido 5 dias e recebeu em 8, provavelmente vira detrator. Mas se foi prometido 8 dias e recebeu em 8, ele seria detrator mesmo assim?

A hipótese é que a quebra de expectativa importa mais do que o tempo total de entrega — e o heatmap já mostra que `delivery_delay_days` (-0.6) tem correlação mais forte com o NPS do que `delivery_time_days`.

**O que analisar:** comparar o peso das duas variáveis sobre o NPS e verificar se clientes que receberam no prazo, mesmo que tardio, têm NPS melhor.

### Hipótese 3 — Frete e desconto como amortecedores da insatisfação

Um frete mais baixo ou um desconto maior reduz a sensibilidade do cliente às variáveis operacionais que degradam a experiência? Ou seja — compensar o cliente no bolso ajuda a absorver um atraso ou um problema no atendimento?

**O que analisar:** cruzar `freight_value` e `discount_value` com `delivery_delay_days` e `nps_categoria` — ver se clientes com frete baixo ou desconto alto que sofreram atraso têm NPS melhor do que clientes sem essas compensações.

---

## Próximos Passos

A investigação segue para o **Grupo Atendimento** (`customer_service_contacts`, `resolution_time_days`, `complaints_count`), que junto com a Logística é onde o problema provavelmente se concentra. Em seguida, as hipóteses acima serão testadas como análises multivariadas e, posteriormente, como features do modelo preditivo.
