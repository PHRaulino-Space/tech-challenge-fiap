# 6. Preparação dos Dados

*CRISP-DM: Data Preparation*

Esta etapa transforma a base original do desafio em uma visão analítica pronta para EDA e para uma futura solução preditiva de prazo/risco de atraso. A preparação foi mantida simples e auditável, porque o dataset já chega estruturado, sem valores nulos e com variáveis operacionais diretamente interpretáveis.

A preparação também registra a troca de chave do projeto: o `nps_score` continua sendo o desfecho de satisfação, mas a solução mais acionável passa a mirar a **previsão do prazo de entrega e do risco de atraso**.

---

## Base Utilizada

| Item | Descrição |
|---|---|
| Arquivo original | `data/desafio_nps_fase_1.csv` |
| Registros | 2.500 clientes/pedidos |
| Variáveis originais | 19 |
| Metadados | `data/metadados_desafio_nps_fase_1.json` |
| Notebook final | `notebooks/eda_final.ipynb` |

A base original não foi modificada. Todas as transformações foram feitas em memória nos notebooks, preservando o arquivo entregue no desafio.

---

## Validações de Qualidade

Antes das análises, foram verificadas as condições mínimas para uso da base:

- **Integridade:** não foram identificados valores nulos nas variáveis do dataset.
- **Tipagem:** variáveis numéricas, categóricas e binárias foram interpretadas conforme o dicionário de metadados.
- **Ordenação da jornada:** as colunas foram reorganizadas pela ordem da experiência do cliente, facilitando a leitura por etapa: cliente, pedido, logística, atendimento e satisfação.
- **Escala do alvo:** `nps_score` foi mantido na escala original de 0 a 10.

Como a EDA tem objetivo explicativo e acadêmico, não foram aplicadas remoções de outliers nem imputações artificiais. Alterar esses pontos poderia mascarar justamente os eventos operacionais críticos que explicam a insatisfação.

---

## Variável-Alvo

Na leitura inicial do desafio, a variável-alvo principal era `nps_score`, usada de duas formas:

| Uso | Tratamento | Finalidade |
|---|---|---|
| Contínuo | Nota de 0 a 10 | Correlações, médias e comparação entre grupos |
| Categórico | Detrator, Neutro, Promotor | Leitura de negócio e proposta de classificação |

Critério de categorização:

| Categoria | Faixa |
|---|---:|
| Detrator | 0 a 6 |
| Neutro | 7 a 8 |
| Promotor | 9 a 10 |

Essa categorização revelou forte desbalanceamento: **74,0% da base é composta por detratores**.

Após a EDA, a preparação passa a separar dois tipos de alvo:

| Tipo de alvo | Variável | Papel no projeto |
|---|---|---|
| Alvo analítico | `nps_score` / `nps_categoria` | Medir o desfecho da experiência e validar impacto |
| Alvo operacional | `delivery_delay_days`, `entregou_no_prazo` ou prazo estimado de entrega | Antecipar a quebra da promessa logística |

Essa separação evita uma interpretação fraca da solução. Prever NPS é útil para diagnóstico; prever entrega é mais útil para intervenção.

---

## Features Derivadas

Para conectar os dados operacionais à narrativa de negócio, foram criadas variáveis auxiliares simples e interpretáveis.

| Feature | Regra | Uso |
|---|---|---|
| `nps_categoria` | Classe derivada de `nps_score` | Segmentação de satisfação |
| `teve_atraso` | `delivery_delay_days > 0` | Identificar quebra do prazo prometido |
| `entregou_no_prazo` | `delivery_delay_days <= 0` | Comparar cumprimento de SLA |
| `teve_contato_sac` | `customer_service_contacts > 0` | Identificar acionamento de suporte |
| `perfil_degradacao` | Combinação de atraso e SAC | Medir acúmulo de falhas na jornada |
| `faixa_resolucao` | Quartis de `resolution_time_days` dentro do pior perfil | Avaliar se velocidade de resolução atenua o dano |

Os quatro perfis de degradação foram:

| Perfil | Definição | Clientes | NPS médio |
|---|---|---:|---:|
| Sem Problemas | Sem atraso e sem SAC | 65 | 8,23 |
| Só Atraso | Atraso sem contato com SAC | 489 | 5,19 |
| Só SAC | SAC sem atraso | 212 | 6,43 |
| Atraso + SAC | Atraso com contato ao SAC | 1.734 | 3,76 |

Essa engenharia de features foi decisiva para transformar correlações isoladas em leitura de jornada.

---

## Seleção Inicial de Variáveis

Para uma proposta preditiva, as variáveis candidatas devem estar disponíveis antes ou durante a jornada, sem depender do resultado final de satisfação. Como a solução final se desloca para prazo/atraso, as variáveis precisam ser separadas por momento de disponibilidade.

### Variáveis candidatas para previsão no momento do pedido

- `customer_age`
- `customer_region`
- `customer_tenure_months`
- `order_value`
- `items_quantity`
- `discount_value`
- `payment_installments`
- `freight_value`

Essas variáveis são candidatas a estimar um prazo mais realista antes da entrega acontecer.

### Variáveis candidatas para monitoramento durante a jornada

- `delivery_time_days`
- `delivery_delay_days`
- `delivery_attempts`
- `customer_service_contacts`
- `resolution_time_days`
- `complaints_count`

Essas variáveis ajudam a monitorar risco de degradação depois que a jornada já começou. Para prever o prazo no checkout, elas não devem ser usadas se ainda não estiverem disponíveis.

### Variáveis que não devem entrar como preditoras

- `nps_score`: é o alvo analítico e não deve ser usado como preditor.
- `nps_categoria`: é derivada do alvo analítico.
- `csat_internal_score`: mede satisfação e pode vazar informação equivalente ao alvo.
- `repeat_purchase_30d`: é comportamento posterior à experiência, útil para validação de negócio, mas não para prever prazo ou NPS antes da jornada terminar.

---

## Tratamento para Modelagem

Para um pipeline de modelagem de prazo/atraso, a preparação recomendada é:

| Tipo de variável | Tratamento |
|---|---|
| Numéricas | Padronização apenas para modelos sensíveis à escala |
| Categóricas | One-hot encoding para `customer_region` |
| Binárias derivadas | Manter como 0/1 |
| Alvo de prazo | Regressão para estimar dias de entrega ou dias de atraso |
| Alvo de atraso | Classificação binária: no prazo vs. atrasado |

Como a base tem alta incidência de atraso, a separação treino/teste deve preservar a proporção de entregas no prazo e atrasadas. Métricas como acurácia isolada não são suficientes: o modelo precisa ser avaliado pela capacidade de identificar atrasos relevantes e pela redução do erro de previsão de prazo.

---

## Riscos de Vazamento

O principal cuidado é temporal: a solução proposta deve prever prazo/risco antes que a promessa logística seja quebrada. Portanto, variáveis disponíveis apenas depois da entrega ou depois do contato com SAC não podem ser usadas em um modelo de promessa inicial.

| Variável | Risco | Decisão |
|---|---|---|
| `csat_internal_score` | Pode ser outro indicador de satisfação final | Não usar como feature principal |
| `repeat_purchase_30d` | Ocorre depois do NPS | Usar apenas como evidência de impacto |
| `delivery_delay_days` | Só é conhecido depois da comparação com o prazo prometido | Usar como alvo ou monitoramento, não como feature inicial |
| `complaints_count` | Pode ocorrer durante ou após a jornada | Usar somente para monitoramento, não para promessa inicial |
| `resolution_time_days` | Só existe quando houve atendimento | Usar somente na camada de recuperação da experiência |

---

## Resultado da Preparação

A base preparada permite sustentar três entregas:

1. **EDA final:** análise da jornada, gráficos e tabelas usados na apresentação.
2. **Recomendação operacional:** priorização de atraso, calibração de prazo e comunicação proativa.
3. **Proposta de modelo:** previsão de prazo/risco de atraso, usando NPS e recompra como métricas de impacto.

O notebook final consolidado é [notebooks/eda_final.ipynb](https://github.com/PHRaulino-Space/tech-challenge-fiap/blob/main/notebooks/eda_final.ipynb).
