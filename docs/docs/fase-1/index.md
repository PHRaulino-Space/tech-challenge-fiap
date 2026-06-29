# Fase 1 — NPS Preditivo

## Contexto

Com o crescimento acelerado do e-commerce, uma empresa passou a lidar com alta variabilidade no **Net Promoter Score (NPS)** entre diferentes perfis de consumidores. O NPS é coletado apenas após o encerramento da jornada de compra, o que limita a capacidade da empresa de antecipar problemas e atuar de forma preventiva.

Este desafio propõe transformar dados operacionais — pedidos, logística e atendimento — em insights acionáveis para orientar decisões estratégicas e melhorar a experiência do cliente.

## Objetivo

Analisar os fatores que influenciam a satisfação dos clientes medida pelo NPS e propor uma abordagem preditiva capaz de agir antes da pesquisa.

Ao longo da EDA houve uma **mudança importante de foco**: a pergunta inicial parecia ser "como prever a nota de NPS antes do cliente responder?". Os dados mostraram que prever a nota, isoladamente, seria menos útil do que atacar a causa operacional mais forte: **o descumprimento do prazo prometido**. Por isso, a solução final passa a priorizar a previsão/calibração do prazo de entrega e do risco de atraso, usando o NPS como métrica de impacto na experiência.

Em outras palavras: o `nps_score` continua sendo o desfecho analisado, mas o alvo operacional da solução passa a ser **prever melhor a entrega para evitar a formação de detratores**.

## Links Úteis da Fase 1

| Material | Link |
|---|---|
| EDA final | [Abrir EDA](eda.md) |
| Apresentação HTML | [Abrir slides](slides.html) |
| Apresentação PDF | [Baixar PDF](<Tech Challenge _ NPS e atraso na entrega.pdf>){ download } |
| Vídeo executivo | [Assistir no YouTube](https://youtu.be/eodKtPdOVdg) |
| Página da apresentação | [Abrir apresentação final](apresentacao-final.md) |
| Notebook final | [Abrir no GitHub](https://github.com/PHRaulino-Space/tech-challenge-fiap/blob/main/notebooks/eda_final.ipynb) |
| Como reproduzir | [Ver instruções](getting-started.md) |
| Avaliação da entrega | [Ver checklist](avaliacao-entrega.md) |

## Requisitos do Desafio

| # | Entrega | Obrigatório |
|---|---|---|
| 1 | Entendimento do negócio | Sim |
| 2 | Definição da variável-alvo | Sim |
| 3 | Análise Exploratória dos Dados (EDA) | Sim |
| 4 | Reflexão e implementação de modelo preditivo | Opcional |

## Conteúdo desta Fase

- [Case — Descrição completa do desafio](case-nps-preditivo.md)
- [Problema de Negócio](problema-negocio.md)
- [Business Canvas](business-canvas.md)
- [Reflexões do Desafio](reflexoes.md)
- [Análise e Hipóteses](analise-hipoteses.md)
- [EDA — Análise Exploratória dos Dados](eda.md)
- [Preparação dos Dados](preparacao-dados.md)
- [Proposta de Solução](proposta-solucao.md)
- [Avaliação dos Resultados](avaliacao.md)
- [Apresentação Final](apresentacao-final.md)
- [Como Reproduzir](getting-started.md)

## Entregáveis

- Repositório GitHub com código organizado (notebooks e/ou scripts)
- Material de apresentação em slides (storytelling gerencial para público não técnico)
- Vídeo executivo de até 5 minutos

## Status da Entrega

| Etapa | Status |
|---|---|
| Problema de negócio | Concluído |
| Business Canvas | Concluído |
| Reflexões do desafio | Concluído |
| Análise e hipóteses | Concluído |
| EDA final | Concluído |
| Preparação dos dados | Concluído |
| Proposta de solução | Concluído |
| Avaliação dos resultados | Concluído |
| Apresentação final | Concluído |
