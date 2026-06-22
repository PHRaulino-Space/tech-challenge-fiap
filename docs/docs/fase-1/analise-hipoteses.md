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

A base conta com **74,0% de detratores** — NPS médio de 4,38, abaixo do ponto neutro (7). A empresa não está lidando com casos isolados de insatisfação; está lidando com um padrão estrutural.

| Categoria | Clientes | % |
| :--- | :---: | :---: |
| Detrator | 1.851 | 74,0% |
| Neutro | 448 | 17,9% |
| Promotor | 201 | 8,0% |

---

## Metodologia da EDA

A análise exploratória foi estruturada seguindo o **ciclo de vida cronológico da jornada do cliente**, com o objetivo de isolar em qual etapa a experiência começa a se degradar.

Para cada grupo de variáveis, a análise combina:

1. **Heatmap de correlação** — triagem rápida para identificar quais variáveis têm relação linear com o NPS Score
2. **Boxplots por categoria NPS** — detalhamento visual da distribuição entre Detratores, Neutros e Promotores

---

## O Que a EDA Revelou

### Grupo Cliente — Sem Relação com o NPS

`customer_age`: -0,01 | `customer_tenure_months`: -0,01

As distribuições são praticamente idênticas entre as três categorias. A região geográfica também não diferencia: NPS médio varia apenas 0,28 pontos entre a melhor (Sul: 4,49) e a pior região (Centro-Oeste: 4,21).

**Conclusão:** a insatisfação não discrimina perfil. O problema não está em quem é o cliente.

---

### Grupo Pedido — Sem Relação com o NPS

`order_value`: +0,04 | `items_quantity`: +0,01 | `discount_value`: +0,03 | `payment_installments`: +0,02

Todas as correlações próximas de zero. Boxplots com caixas no mesmo nível para as três categorias.

**Conclusão:** o momento da compra é neutro para a satisfação. O problema está em outro ponto da jornada.

---

### Grupo Logística — Sinal Mais Forte da Base

`delivery_delay_days`: **-0,60** | `delivery_time_days`: 0,00 | `freight_value`: -0,04 | `delivery_attempts`: +0,03

O sinal de `delivery_delay_days` é o mais forte de toda a análise. A distinção entre as duas variáveis de prazo é um achado crítico: o cliente avalia **se a empresa cumpriu o que prometeu**, não quanto tempo esperou.

- Clientes que receberam no prazo: **NPS médio 6,86** (n=277)
- Clientes que sofreram atraso: **NPS médio 4,07** (n=2.223)

Dos 2.500 clientes, apenas **11% (277) receberam dentro do prazo prometido.**

**Conclusão:** o atraso na entrega é o principal fator de insatisfação da base. É também o candidato mais forte para feature do modelo preditivo.

---

### Grupo Atendimento — Sinal Moderado

`complaints_count`: **-0,50** | `customer_service_contacts`: -0,35 | `resolution_time_days`: -0,19

As três variáveis têm relação com o NPS, cada uma com intensidade diferente. `resolution_time_days` é o sinal mais fraco, sugerindo que o fato de precisar acionar o suporte pesa mais do que o tempo de resolução.

**Conclusão:** o ato de contatar o SAC já está associado a NPS mais baixo — independente do tempo de resolução.

---

## Perfis de Degradação — Análise Combinada

Cruzando as duas variáveis de maior sinal (`delivery_delay_days` e `customer_service_contacts`) como flags binárias, emergem quatro perfis:

| Perfil | Clientes | % Base | NPS Médio | % Detratores | % Recompra |
| :--- | :---: | :---: | :---: | :---: | :---: |
| **Sem Problemas** | 65 | 2,6% | 8,23 | 13,8% | 66,2% |
| **Só SAC** | 212 | 8,5% | 6,43 | 43,4% | 24,1% |
| **Só Atraso** | 489 | 19,6% | 5,19 | 65,2% | 11,5% |
| **Atraso + SAC** | 1.734 | 69,4% | 3,76 | 82,5% | 3,9% |

**Os achados mais relevantes:**

1. **Apenas 2,6% dos clientes** passaram pela jornada sem nenhum problema operacional
2. **69,4% estão no pior perfil** — a combinação dos dois problemas domina a base
3. **77,3% dos detratores** vêm do perfil "Atraso + SAC"
4. **0% de detratores recompram** — comportamento confirma percepção com precisão cirúrgica

---

## Diagnóstico Regional

O problema não é geográfico. A taxa de atraso varia de 88% a 91% em todas as regiões, com diferença de NPS de apenas 0,28 pontos entre a melhor e a pior. O problema é sistêmico — de processo, não de geografia.

---

## Hipóteses Testadas

### H1 — Ticket Alto Protege Contra o Atraso?

Clientes de alto valor do pedido toleram mais o atraso, ou são mais exigentes?

**O que analisar:** NPS médio por faixa de ticket (tercis) × teve_atraso. Se as linhas convergirem nos tickets mais altos, clientes premium são mais tolerantes.

---

### H2 — Cumprimento do Prazo Vale Mais que Velocidade de Entrega

**Resultado confirmado:** cumprir o prazo prometido (-0,60) pesa muito mais que o tempo total de entrega (≈ 0,00). Clientes no prazo têm NPS 6,86; atrasados têm NPS 4,07.

A análise por quartil de tempo de entrega × prazo confirma: mesmo entregas lentas que chegaram no prazo têm NPS consistentemente superior às que chegaram mais rápido mas com atraso.

---

### H3 — Frete e Desconto Como Amortecedores da Insatisfação

Entre clientes que sofreram atraso, frete baixo ou desconto alto (acima da mediana) atenua o impacto no NPS?

**O que analisar:** NPS médio por combinação de faixa de frete × nível de desconto, filtrando apenas clientes com atraso.

---

## Resolução Dentro do Pior Perfil

Entre clientes do perfil "Atraso + SAC", o tempo de resolução ainda diferencia o NPS:

| Velocidade | NPS Médio |
| :--- | :---: |
| Muito Rápido | 4,47 |
| Rápido | 3,86 |
| Lento | 3,53 |
| Muito Lento | 2,94 |

Amplitude de **1,53 pontos**. O SAC atenua o dano mas não o reverte — todos os grupos permanecem na faixa de detratores. O ponto de intervenção eficaz é o atraso, não a velocidade do SAC.

---

## Limitações e Premissas

### O NPS como Desfecho Final da Jornada

O case não especifica em qual momento exato o NPS é coletado. **Premissa adotada:** o `nps_score` é tratado como o desfecho final — a avaliação do cliente depois de ter passado por todas as etapas.

### Causalidade vs. Correlação

A base não permite afirmar a direção da causalidade nas variáveis de atendimento. O cliente pode ter reclamado porque já era detrator, ou pode ter virado detrator porque o atendimento não resolveu. Para as recomendações de negócio, essa distinção importa — mas não altera a leitura das correlações.

### Mediação Atraso → SAC

A hipótese de cascata (atraso causa contato com SAC) foi verificada: 76,5% dos clientes sem atraso também contataram o SAC vs. 78,0% dos com atraso — diferença pequena. A reclamação formal, porém, atinge 91,7% dos sem atraso vs. 100% dos com atraso. O SAC parece ter causas parcialmente independentes do atraso; a narrativa de cascata se aplica melhor às reclamações formais.
