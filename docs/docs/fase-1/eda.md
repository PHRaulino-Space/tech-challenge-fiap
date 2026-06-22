# 5. Análise Exploratória dos Dados (EDA)

*CRISP-DM: Data Understanding*

A EDA foi estruturada seguindo o **fluxo cronológico da jornada do cliente** no e-commerce — compra, entrega e atendimento — com o objetivo de isolar em qual etapa a experiência se rompe e qual o tamanho real do problema.

---

## O Ponto de Partida: 74% dos Clientes São Detratores

Antes de qualquer análise cruzada, a distribuição da base já comunica a urgência. Com **NPS médio de 4,38** — abaixo do ponto neutro (7) — a empresa não está lidando com exceções de insatisfação. Está lidando com um padrão.

| Categoria | Clientes | % da Base |
| :--- | :---: | :---: |
| **Detrator** (0–6) | 1.851 | **74,0%** |
| Neutro (7–8) | 448 | 17,9% |
| Promotor (9–10) | 201 | 8,0% |

3 em cada 4 clientes avaliariam negativamente a marca para outras pessoas. Isso não é um problema pontual de insatisfação — é o estado operacional padrão da empresa.

---

## O Mapa das Correlações

O heatmap de correlações de todas as variáveis com o NPS Score entrega um diagnóstico claro antes de qualquer análise aprofundada.

| Variável | Correlação com NPS | Grupo |
| :--- | :---: | :--- |
| `delivery_delay_days` | **-0,60** | Logística |
| `complaints_count` | **-0,50** | Atendimento |
| `customer_service_contacts` | -0,35 | Atendimento |
| `resolution_time_days` | -0,19 | Atendimento |
| `freight_value` | -0,04 | Logística |
| `delivery_attempts` | +0,03 | Logística |
| `order_value` | +0,04 | Pedido |
| `customer_age` | -0,01 | Cliente |
| `customer_tenure_months` | -0,01 | Cliente |
| Demais variáveis | ≈ 0 | Pedido / Cliente |

**O sinal está concentrado na execução pós-compra.** O momento da transação — valor do pedido, parcelas, desconto — é irrelevante para a satisfação. Perfil de cliente também.

---

## Análise por Grupo da Jornada

### Grupo Cliente — Sem Relação com o NPS

`customer_age` (-0,01) e `customer_tenure_months` (-0,01) apresentam correlação praticamente nula com o NPS. Os boxplots confirmam: as distribuições são idênticas entre Detratores, Neutros e Promotores.

A região geográfica também foi investigada — variação de apenas **0,28 pontos** de NPS entre a melhor (Sul: 4,49) e a pior região (Centro-Oeste: 4,21).

**Conclusão:** a insatisfação não discrimina perfil. Um cliente novo ou antigo, jovem ou mais velho, de qualquer região, tem a mesma chance de virar detrator. O problema não está em quem é o cliente.

---

### Grupo Pedido — Sem Relação com o NPS

Todas as variáveis — `order_value`, `items_quantity`, `discount_value` e `payment_installments` — apresentaram correlação próxima de zero. Os boxplots mostram caixas no mesmo nível para as três categorias NPS.

**Conclusão:** o momento da compra é neutro para a satisfação. Não importa o quanto o cliente gastou, quantos itens comprou ou em quantas parcelas pagou.

---

### Grupo Logística — O Sinal Mais Forte

`delivery_delay_days` apresentou correlação de **-0,60** com o NPS — o sinal mais forte de toda a análise. Os boxplots confirmam visualmente: promotores quase não têm atraso (mediana ≈ 0), enquanto detratores têm atraso consistente (mediana ≈ 2 dias, com outliers chegando a 7–8 dias).

Uma distinção importante entre as duas variáveis de prazo:

- `delivery_delay_days` (atraso vs. prometido): **-0,60**
- `delivery_time_days` (tempo total): **≈ 0,00**

Isso revela que **o cliente avalia se a empresa cumpriu o que prometeu — não quanto tempo esperou**. Um cliente que aguardou 10 dias dentro do prazo tem NPS próximo a 7. Um que aguardou 5 dias com 1 de atraso tende a avaliar abaixo de 5.

**Clientes que receberam no prazo: NPS médio de 6,86. Clientes que sofreram atraso: NPS médio de 4,07.** Diferença de 2,79 pontos.

---

### Grupo Atendimento — Sinal Moderado com Leitura Importante

| Variável | Correlação |
| :--- | :---: |
| `complaints_count` | -0,50 |
| `customer_service_contacts` | -0,35 |
| `resolution_time_days` | -0,19 |

O sinal mais fraco é `resolution_time_days` (-0,19), o que sugere que **quanto demora para resolver importa menos do que o fato de precisar acionar o suporte**. O simples ato de contatar o SAC já está associado a NPS mais baixo.

> **Limitação:** a base não permite afirmar a direção da causalidade. O cliente pode ter reclamado porque já era detrator, ou pode ter virado detrator porque o atendimento não resolveu. Ambos os cenários aparecem da mesma forma nos dados.

---

## Os Perfis de Degradação da Experiência

Com os dois sinais mais fortes identificados, criamos flags binárias:

- `teve_atraso`: recebeu fora do prazo prometido?
- `teve_contato_sac`: precisou acionar o SAC?

A combinação gera quatro perfis:

| Perfil | Clientes | % da Base | NPS Médio | % Detratores |
| :--- | :---: | :---: | :---: | :---: |
| **Sem Problemas** | 65 | 2,6% | **8,23** | 13,8% |
| **Só SAC** | 212 | 8,5% | 6,43 | 43,4% |
| **Só Atraso** | 489 | 19,6% | 5,19 | 65,2% |
| **Atraso + SAC** | 1.734 | **69,4%** | **3,76** | 82,5% |

Dois achados críticos:

1. **Apenas 65 clientes (2,6%) passaram pela jornada sem nenhum problema operacional.** A operação entrega uma experiência limpa para menos de 3% da base.
2. **69,4% estão no pior perfil.** Mais de 2 em cada 3 clientes sofreram atraso E precisaram acionar o SAC.

**Origem dos detratores por perfil:**

- Atraso + SAC: **1.431 detratores (77,3%)**
- Só Atraso: 319 (17,2%)
- Só SAC: 92 (5,0%)
- Sem Problemas: 9 (0,5%)

99,5% de todos os detratores tiveram ao menos um problema operacional identificável.

---

## Percepção vs. Comportamento — Recompra em 30 Dias

NPS é uma declaração de intenção. A recompra em 30 dias é o comportamento real.

| Categoria NPS | % Recompra em 30 dias |
| :--- | :---: |
| **Detrator** | **0,0%** |
| Neutro | 3,8% |
| **Promotor** | **100,0%** |

**O dado mais contundente da análise:** nenhum detrator voltou a comprar em 30 dias. Todos os promotores voltaram. A percepção e o comportamento estão em alinhamento perfeito — o NPS não é apenas uma pesquisa de satisfação, é um preditor direto de receita futura.

Por perfil de degradação:

| Perfil | % Recompra |
| :--- | :---: |
| Sem Problemas | 66,2% |
| Só SAC | 24,1% |
| Só Atraso | 11,5% |
| Atraso + SAC | 3,9% |

---

## Diagnóstico Regional — O Problema É Sistêmico

A distribuição de atraso por região confirma que o problema não é geográfico:

| Região | % com Atraso | Atraso Médio (dias) | NPS Médio |
| :--- | :---: | :---: | :---: |
| Sudeste | 91,0% | 2,22 | 4,37 |
| Nordeste | 90,0% | 2,19 | 4,42 |
| Centro-Oeste | 88,0% | 2,22 | 4,21 |
| Norte | 88,0% | 2,14 | 4,38 |
| Sul | 88,0% | 2,17 | 4,49 |

88 a 91% de atraso em todas as regiões, com diferença de apenas 0,28 pontos de NPS entre a melhor e a pior. **O problema é de processo — não de geografia.** Ações regionalizadas não resolvem.

---

## Tempo de Resolução — Atenua o Dano, Não o Apaga

Dentro do perfil "Atraso + SAC", o tempo de resolução do SAC ainda diferencia o NPS:

| Velocidade de Resolução | NPS Médio |
| :--- | :---: |
| Muito Rápido | 4,47 |
| Rápido | 3,86 |
| Lento | 3,53 |
| Muito Lento | 2,94 |

Amplitude de **1,53 pontos** dentro do mesmo perfil de degradação. O SAC ainda tem margem para atenuar o dano — mas não para revertê-lo. Todos os grupos permanecem na faixa de detratores.

**O ponto de intervenção eficaz é antes: no atraso.**

---

## Resumo Executivo

| Achado | Evidência |
| :--- | :--- |
| 74% dos clientes são detratores | NPS médio 4,38 — abaixo do ponto neutro |
| O problema está na operação, não no perfil | Idade, região, ticket: correlação ≈ 0 |
| Atraso na entrega é a causa raiz | `delivery_delay_days`: -0,60 |
| O problema é sistêmico, não regional | 88–91% de atraso em todas as regiões |
| Apenas 11% receberam no prazo | 277 de 2.500 clientes |
| Atraso e SAC se acumulam | 69,4% no perfil "Atraso + SAC" |
| 0% de detratores recompram | Comportamento confirma percepção |
| Resolução rápida atenua 1,53 pts | Mas não reverte a categoria de detrator |
