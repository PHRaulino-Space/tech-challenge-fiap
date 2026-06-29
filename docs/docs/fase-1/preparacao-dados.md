# 6. Preparação dos Dados

*CRISP-DM: Data Preparation*

Esta etapa transforma a base original do desafio em uma visão analítica pronta para EDA e para uma futura modelagem preditiva de risco de detração. A preparação foi mantida simples e auditável, porque o dataset já chega estruturado, sem valores nulos e com variáveis operacionais diretamente interpretáveis.

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

A variável-alvo principal é `nps_score`, usada de duas formas:

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

Para uma proposta preditiva, as variáveis candidatas devem estar disponíveis antes ou durante a jornada, sem depender do resultado final de satisfação.

### Variáveis candidatas

- `customer_age`
- `customer_region`
- `customer_tenure_months`
- `order_value`
- `items_quantity`
- `discount_value`
- `payment_installments`
- `delivery_time_days`
- `delivery_delay_days`
- `freight_value`
- `delivery_attempts`
- `customer_service_contacts`
- `resolution_time_days`
- `complaints_count`

### Variáveis que não devem entrar como preditoras

- `nps_score`: é o alvo.
- `nps_categoria`: é derivada do alvo.
- `csat_internal_score`: mede satisfação e pode vazar informação equivalente ao alvo.
- `repeat_purchase_30d`: é comportamento posterior à experiência, útil para validação de negócio, mas não para prever NPS antes da pesquisa.

---

## Tratamento para Modelagem

Para um pipeline de modelagem, a preparação recomendada é:

| Tipo de variável | Tratamento |
|---|---|
| Numéricas | Padronização apenas para modelos sensíveis à escala |
| Categóricas | One-hot encoding para `customer_region` |
| Binárias derivadas | Manter como 0/1 |
| Alvo categórico | Classificação em Detrator, Neutro e Promotor ou classificação binária Detrator vs. Não Detrator |

Como a classe detratora domina a base, a separação treino/teste deve ser **estratificada**. Métricas como acurácia isolada não são suficientes: prever todos os clientes como detratores já atingiria 74,0% de acerto aparente.

---

## Riscos de Vazamento

O principal cuidado é temporal: a solução proposta deve prever o risco antes da aplicação da pesquisa de NPS. Portanto, variáveis disponíveis apenas depois do encerramento da jornada precisam ser tratadas com cautela.

| Variável | Risco | Decisão |
|---|---|---|
| `csat_internal_score` | Pode ser outro indicador de satisfação final | Não usar como feature principal |
| `repeat_purchase_30d` | Ocorre depois do NPS | Usar apenas como evidência de impacto |
| `complaints_count` | Pode ocorrer durante ou após a jornada | Usar somente se operacionalmente disponível antes da pesquisa |
| `resolution_time_days` | Só existe quando houve atendimento | Pode exigir imputação ou indicador de ausência de SAC |

---

## Resultado da Preparação

A base preparada permite sustentar três entregas:

1. **EDA final:** análise da jornada, gráficos e tabelas usados na apresentação.
2. **Recomendação operacional:** priorização de atraso, SAC e comunicação proativa.
3. **Proposta de modelo:** classificação de risco de detração com foco em recall de detratores.

O notebook final consolidado é [notebooks/eda_final.ipynb](https://github.com/PHRaulino-Space/tech-challenge-fiap/blob/main/notebooks/eda_final.ipynb).
