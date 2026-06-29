# Entrega — Tech Challenge Fase 1

## Identificação

**Projeto:** Tech Challenge — POSTECH AI Scientist / FIAP
**Fase:** 1 — NPS Preditivo
**Tema:** Análise de satisfação em e-commerce
**Aluno:** Paulo Henrique Almeida — RM375573
**Repositório:** <https://github.com/PHRaulino-Space/tech-challenge-fiap>
**Documentação publicada:** <https://phraulino-space.github.io/tech-challenge-fiap/>

---

## Contexto da Entrega

O desafio propõe analisar dados operacionais de um e-commerce para entender quais fatores influenciam a satisfação do cliente, medida pela nota de NPS (`nps_score`), e refletir sobre uma abordagem preditiva capaz de apoiar decisões antes da aplicação da pesquisa.

A análise foi estruturada com base no CRISP-DM, passando por entendimento do negócio, definição da variável-alvo, análise exploratória, preparação dos dados, proposta de solução, avaliação e apresentação executiva.

Durante a EDA, houve uma mudança importante na formulação da solução: o projeto começou com a pergunta "como prever o NPS antes da pesquisa?", mas os dados mostraram que a ação mais útil para o negócio é anterior à nota. O principal fator associado ao baixo score de NPS foi o atraso na entrega, especialmente o descumprimento do prazo prometido.

Por isso, a solução final recomenda priorizar **previsão/calibração de prazo de entrega e risco de atraso**, usando o NPS como métrica de impacto da experiência.

---

## Links Principais para Avaliação

| Material | Link |
|---|---|
| Documentação completa | <https://phraulino-space.github.io/tech-challenge-fiap/> |
| Resumo único da entrega | <https://phraulino-space.github.io/tech-challenge-fiap/fase-1/resumo-entrega/> |
| Visão geral da Fase 1 | <https://phraulino-space.github.io/tech-challenge-fiap/fase-1/> |
| EDA final | <https://phraulino-space.github.io/tech-challenge-fiap/fase-1/eda/> |
| Apresentação em HTML | <https://phraulino-space.github.io/tech-challenge-fiap/fase-1/slides.html> |
| Apresentação em PDF | <https://phraulino-space.github.io/tech-challenge-fiap/fase-1/Tech%20Challenge%20_%20NPS%20e%20atraso%20na%20entrega.pdf> |
| Vídeo executivo | <https://youtu.be/eodKtPdOVdg> |
| Notebook final de EDA | <https://github.com/PHRaulino-Space/tech-challenge-fiap/blob/main/notebooks/eda_final.ipynb> |
| Script pareado do notebook | <https://github.com/PHRaulino-Space/tech-challenge-fiap/blob/main/notebooks/eda_final.py> |
| Como reproduzir | <https://phraulino-space.github.io/tech-challenge-fiap/fase-1/getting-started/> |
| Avaliação/checklist da entrega | <https://phraulino-space.github.io/tech-challenge-fiap/fase-1/avaliacao-entrega/> |

---

## Principais Achados

| Achado | Evidência |
|---|---|
| A base é majoritariamente detratora | 74,0% dos clientes são detratores |
| Perfil do cliente não explica o baixo score | Idade, região e tempo de relacionamento têm baixa associação com o score |
| Pedido não explica a insatisfação | Valor, desconto, quantidade de itens e parcelas têm baixa associação |
| Atraso é o maior sinal operacional | `delivery_delay_days` tem correlação -0,60 com `nps_score` |
| Cumprir prazo importa mais que velocidade | `delivery_time_days` tem correlação próxima de zero; atraso derruba o score |
| O problema é sistêmico | Atrasos variam de 88% a 91% nas regiões |
| Recompra valida o impacto | Detratores tiveram 0,0% de recompra em 30 dias |

---

## Conclusão Executiva

A empresa não tem um problema concentrado em perfil de cliente, preço, desconto ou região. O problema aparece depois da compra, na execução operacional da entrega e no atendimento.

O ponto de ruptura mais relevante é a promessa logística não cumprida. A recomendação final é construir uma capacidade analítica para prever prazo de entrega e risco de atraso, permitindo comunicação proativa e priorização operacional antes que o cliente vire detrator.

Em resumo:

**NPS é o termômetro da experiência. Atraso é a alavanca operacional. Previsão de prazo é a solução mais acionável.**

---

## Estrutura da Documentação

| Etapa | Link |
|---|---|
| Problema de Negócio | <https://phraulino-space.github.io/tech-challenge-fiap/fase-1/problema-negocio/> |
| Business Canvas | <https://phraulino-space.github.io/tech-challenge-fiap/fase-1/business-canvas/> |
| Reflexões do Desafio | <https://phraulino-space.github.io/tech-challenge-fiap/fase-1/reflexoes/> |
| Análise e Hipóteses | <https://phraulino-space.github.io/tech-challenge-fiap/fase-1/analise-hipoteses/> |
| EDA | <https://phraulino-space.github.io/tech-challenge-fiap/fase-1/eda/> |
| Preparação dos Dados | <https://phraulino-space.github.io/tech-challenge-fiap/fase-1/preparacao-dados/> |
| Proposta de Solução | <https://phraulino-space.github.io/tech-challenge-fiap/fase-1/proposta-solucao/> |
| Avaliação dos Resultados | <https://phraulino-space.github.io/tech-challenge-fiap/fase-1/avaliacao/> |
| Apresentação Final | <https://phraulino-space.github.io/tech-challenge-fiap/fase-1/apresentacao-final/> |

---

## Observação sobre o Modelo Preditivo

O item de modelo preditivo é opcional no enunciado. Esta entrega apresenta uma proposta de solução preditiva baseada nos achados da EDA, mas não implementa um modelo produtivo.

A proposta recomenda duas camadas:

1. **Previsão de prazo de entrega:** estimar um prazo mais realista por pedido.
2. **Classificação de risco de atraso:** identificar pedidos com maior chance de descumprir o prazo prometido.

O `nps_score` permanece como desfecho analítico e métrica de validação da experiência.
