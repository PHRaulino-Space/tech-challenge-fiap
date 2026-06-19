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

### 1. Business Canvas
*CRISP-DM: Business Understanding*

**Objetivo:** Estruturar o entendimento do negócio de forma visual e consolidada antes de qualquer análise de dados.

O Business Model Canvas será utilizado para mapear o contexto do e-commerce, os problemas centrais, os stakeholders envolvidos e o valor que a análise de NPS pode gerar para cada área do negócio (logística, atendimento, produto, estratégia).

**Resultado esperado:** Canvas preenchido servindo de base para as reflexões e a narrativa da apresentação.

---

### 2. Reflexões do Desafio
*CRISP-DM: Business Understanding*

**Objetivo:** Responder às perguntas de negócio propostas no desafio com raciocínio crítico e orientado a resultado.

Com o Canvas como apoio, serão desenvolvidas as reflexões sobre:

- Qual problema de negócio está sendo resolvido
- Por que o NPS é importante para o e-commerce
- Quais áreas se beneficiam dos insights
- Como o NPS impacta recompra, boca a boca e market share
- Qual variável representa a satisfação do cliente e por que ela foi escolhida

**Resultado esperado:** Linha de raciocínio documentada, pronta para compor o relatório e os slides.

---

### 3. Análise dos Dados e Hipóteses
*CRISP-DM: Data Understanding*

**Objetivo:** Compreender a base de dados disponível, levantar hipóteses e identificar relações relevantes antes da EDA formal.

Esta etapa inclui a leitura do dicionário de dados, inspeção inicial da base (tipos, dimensões, distribuições), identificação de possíveis anomalias e formulação de hipóteses sobre quais variáveis podem influenciar o NPS.

**Resultado esperado:** Lista de hipóteses documentadas para guiar a análise exploratória.

---

### 4. EDA — Análise Exploratória dos Dados
*CRISP-DM: Data Understanding*

**Objetivo:** Explorar os dados com foco em negócio, respondendo às perguntas do desafio com visualizações e estatísticas.

A EDA buscará identificar:

- Fatores mais críticos para a satisfação do cliente
- O que mais gera detratores
- Pontos de ruptura na experiência do cliente
- Perfis de clientes com NPS mais alto ou mais baixo

A análise será conduzida em notebooks Python e documentada de forma acessível para um público não técnico.

**Resultado esperado:** Notebook com análise completa e visualizações prontas para uso na apresentação.

---

### 5. Preparação dos Dados
*CRISP-DM: Data Preparation*

**Objetivo:** Preparar a base de dados para modelagem, garantindo qualidade e consistência das variáveis.

Esta etapa contempla:

- Tratamento de valores ausentes e outliers
- Transformações e normalização de variáveis
- Engenharia de features relevantes para o modelo
- Definição e separação dos conjuntos de treino e teste

**Resultado esperado:** Dataset limpo e pipeline de preparação documentado, pronto para alimentar o modelo.

---

### 6. Proposta de Solução
*CRISP-DM: Modeling*

**Objetivo:** Avaliar a viabilidade de um modelo preditivo de NPS e, se aplicável, propor e implementar uma solução.

A partir dos insights da EDA, será avaliado se faz sentido construir um modelo preditivo (regressão ou classificação) e descrita a estratégia adotada: definição da variável-alvo, seleção de features, escolha do modelo e métricas de avaliação.

> Esta etapa é opcional conforme o enunciado do desafio, mas será desenvolvida se os dados e o tempo permitirem.

**Resultado esperado:** Proposta documentada e, se implementada, pipeline de modelo em Python.

---

### 7. Avaliação dos Resultados
*CRISP-DM: Evaluation*

**Objetivo:** Verificar se os resultados — analíticos e/ou do modelo — respondem ao objetivo de negócio antes de seguir para a apresentação.

Esta etapa revisita o entendimento do negócio definido nas etapas 1 e 2 para responder:

- Os insights da EDA respondem às perguntas do desafio?
- O modelo (se implementado) performa de forma satisfatória e faz sentido para o negócio?
- Há limitações ou riscos que precisam ser comunicados?

Se necessário, esta fase pode indicar um retorno a etapas anteriores para refinamento.

**Resultado esperado:** Validação dos resultados com registro das limitações e dos riscos da análise.

---

### 8. Apresentação Final
*CRISP-DM: Deployment*

**Objetivo:** Consolidar todos os insumos em uma apresentação executiva e no vídeo de até 5 minutos.

Com os resultados validados, serão montados:

- **Slides** com storytelling gerencial voltado para público não técnico
- **Vídeo executivo** de até 5 minutos apresentando o problema, os insights e as recomendações

**Resultado esperado:** Material de apresentação finalizado e vídeo gravado, prontos para entrega.

---

## Visão Geral

| # | Etapa | CRISP-DM | Depende de |
|---|---|---|---|
| 1 | Business Canvas | Business Understanding | — |
| 2 | Reflexões do Desafio | Business Understanding | 1 |
| 3 | Análise e Hipóteses | Data Understanding | 2 |
| 4 | EDA | Data Understanding | 3 |
| 5 | Preparação dos Dados | Data Preparation | 4 |
| 6 | Proposta de Solução | Modeling | 5 |
| 7 | Avaliação dos Resultados | Evaluation | 6 |
| 8 | Apresentação Final | Deployment | 7 |
