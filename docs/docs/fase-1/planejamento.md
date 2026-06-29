# Planejamento — Fase 1

Esta página descreve a estratégia de entrega adotada para o Tech Challenge da Fase 1. O plano foi organizado seguindo o framework **CRISP-DM** (Cross-Industry Standard Process for Data Mining), metodologia amplamente adotada em projetos de ciência de dados por estruturar o trabalho de forma iterativa e orientada ao negócio.

---

## O Framework CRISP-DM

O CRISP-DM define seis fases interdependentes. O processo não é linear — os resultados de fases posteriores podem indicar a necessidade de revisitar fases anteriores, especialmente entre Avaliação e Entendimento do Negócio.

```
Business Understanding → Data Understanding → Data Preparation
        ↑                                              ↓
    Evaluation          ←       Deployment    ←   Modeling
```

---

## Etapas do Projeto

Todas as etapas da Fase 1 estão concluídas na documentação. A modelagem foi tratada como proposta de solução preditiva orientada pela EDA, conforme permitido pelo enunciado do desafio.

### 1. Problema de Negócio
*CRISP-DM: Business Understanding*

**Objetivo:** Definir com clareza o problema que está sendo resolvido, a variável-alvo e o impacto esperado para o negócio — antes de qualquer análise técnica.

Esta etapa responde às perguntas fundamentais do desafio:

- Qual problema de negócio está sendo resolvido?
- Por que o NPS é importante para um e-commerce?
- Quais áreas se beneficiam dos insights (logística, atendimento, produto, marketing)?
- Como o NPS impacta recompra, boca a boca e market share?

> A análise se restringe ao que o case e o dataset permitem inferir. Quando algo não estiver explícito, é tratado como hipótese ou limitação — não como fato.

**Resultado esperado:** Definição do problema documentada, com variável-alvo identificada e impacto de negócio descrito.

**Status:** concluído.

---

### 2. Business Canvas
*CRISP-DM: Business Understanding*

**Objetivo:** Estruturar o entendimento do negócio de forma visual e consolidada.

O Business Model Canvas mapeia o contexto do e-commerce, os problemas centrais, os stakeholders e o valor que a análise de NPS pode gerar para cada área do negócio.

> O canvas é preenchido apenas com o que o case e o dataset permitem inferir. Lacunas são registradas explicitamente como hipóteses ou limitações da análise — esse cuidado é esperado e valorizado na avaliação.

**Resultado esperado:** Canvas preenchido servindo de base para as reflexões e a narrativa da apresentação.

**Status:** concluído.

---

### 3. Reflexões do Desafio
*CRISP-DM: Business Understanding*

**Objetivo:** Conectar o problema de negócio aos impactos esperados em recompra, boca a boca, market share e áreas beneficiadas.

Esta etapa traduz o desafio em perguntas de decisão para logística, atendimento, marketing, produto e experiência do cliente.

**Resultado esperado:** Reflexões documentadas sobre por que o NPS importa e como os dados operacionais podem apoiar uma atuação preventiva.

**Status:** concluído.

---

### 4. Análise dos Dados e Hipóteses
*CRISP-DM: Data Understanding*

**Objetivo:** Compreender a base de dados disponível, levantar hipóteses e identificar relações relevantes antes da EDA formal.

Esta etapa inclui a leitura do dicionário de dados, inspeção inicial da base (tipos, dimensões, distribuições), identificação de possíveis anomalias e formulação de hipóteses sobre quais variáveis podem influenciar o NPS.

**Resultado esperado:** Lista de hipóteses documentadas para guiar a análise exploratória.

**Status:** concluído.

---

### 5. EDA — Análise Exploratória dos Dados
*CRISP-DM: Data Understanding*

**Objetivo:** Explorar os dados com foco em negócio, respondendo às perguntas do desafio com visualizações e estatísticas.

A EDA busca identificar fatores críticos para a satisfação do cliente, pontos de ruptura na experiência e perfis com NPS mais alto ou mais baixo. A análise é conduzida em notebooks Python e documentada de forma acessível para um público não técnico.

Para cada visualização, são respondidas três perguntas:

- O que esse gráfico mostra?
- Por que isso importa para o negócio?
- Qual decisão ou investigação ele sugere?

**Resultado esperado:** Notebook com análise completa, visualizações prontas para a apresentação e principais achados documentados.

**Status:** concluído.

---

### 6. Preparação dos Dados
*CRISP-DM: Data Preparation*

**Objetivo:** Preparar a base de dados para modelagem, garantindo qualidade e consistência das variáveis.

Esta etapa contempla tratamento de valores ausentes e outliers, transformações e normalização, engenharia de features e separação dos conjuntos de treino e teste.

**Resultado esperado:** Dataset limpo e pipeline de preparação documentado, pronto para alimentar o modelo.

**Status:** concluído.

---

### 7. Proposta de Solução
*CRISP-DM: Modeling*

**Objetivo:** Propor e implementar um modelo preditivo de NPS a partir dos insights da EDA.

A estratégia inclui definição da variável-alvo, seleção de features, escolha do modelo e métricas de avaliação. A abordagem pode ser regressão (prever o score) ou classificação (prever a categoria: Detrator, Neutro, Promotor).

**Resultado esperado:** Estratégia preditiva documentada, com variável-alvo, features candidatas, modelo inicial recomendado, métricas e régua de ação.

**Status:** concluído.

---

### 8. Avaliação dos Resultados
*CRISP-DM: Evaluation*

**Objetivo:** Verificar se os resultados respondem ao objetivo de negócio e documentar limitações.

Esta etapa revisita o problema definido nas etapas 1 e 2 para responder:

- Os insights da EDA respondem às perguntas do desafio?
- O modelo performa de forma satisfatória e faz sentido para o negócio?
- Quais são as limitações da análise e os riscos a comunicar?
- Quais recomendações concretas podem ser feitas para as áreas envolvidas (logística, atendimento, produto, pricing)?

Se necessário, esta fase pode indicar retorno a etapas anteriores para refinamento.

**Resultado esperado:** Validação dos resultados com registro das limitações, riscos e recomendações finais para o negócio.

**Status:** concluído.

---

### 9. Apresentação Final
*CRISP-DM: Deployment*

**Objetivo:** Consolidar todos os insumos em uma apresentação executiva e no vídeo de até 5 minutos.

Com os resultados validados, foram entregues:

- **Slides** em HTML (Reveal.js) hospedados no GitHub Pages, com storytelling gerencial voltado para público não técnico
- **Notebook final de EDA** com os gráficos e evidências que sustentam a conclusão
- **Documentação MkDocs** com todas as etapas do CRISP-DM

A entrega final é a página pública de documentação contendo, de forma acessível:

- Link do repositório GitHub
- Apresentação em HTML
- Notebooks e código
- Conclusões e recomendações principais

**Resultado esperado:** Material de apresentação, notebook final e documentação prontos para entrega.

**Status:** concluído.

---

## Visão Geral

| # | Etapa | CRISP-DM | Depende de |
|---|---|---|---|
| 1 | Problema de Negócio | Business Understanding | — |
| 2 | Business Canvas | Business Understanding | 1 |
| 3 | Reflexões do Desafio | Business Understanding | 1, 2 |
| 4 | Análise e Hipóteses | Data Understanding | 3 |
| 5 | EDA | Data Understanding | 4 |
| 6 | Preparação dos Dados | Data Preparation | 5 |
| 7 | Proposta de Solução | Modeling | 6 |
| 8 | Avaliação dos Resultados | Evaluation | 7 |
| 9 | Apresentação Final | Deployment | 8 |
