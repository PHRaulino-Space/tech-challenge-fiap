# Tech Challenge — POSTECH AI Scientist

Repositório central das entregas do **Tech Challenge**, projeto integrador do programa **POSTECH AI Scientist** da FIAP. O Tech Challenge reúne, a cada fase, os conhecimentos aplicados nas disciplinas correspondentes e representa **90% da nota final** de cada fase.

**Repositório:** [github.com/PHRaulino-Space/tech-challenge-fiap](https://github.com/PHRaulino-Space/tech-challenge-fiap)

**Documentação publicada:** [phraulino-space.github.io/tech-challenge-fiap](https://phraulino-space.github.io/tech-challenge-fiap/)

## O Projeto

O Tech Challenge é desenvolvido ao longo de **5 fases** do programa. Em cada fase, o grupo recebe um desafio aplicado que exige pensamento analítico, habilidades técnicas e comunicação orientada a negócio. Os desafios simulam cenários reais de atuação no mercado e evoluem em complexidade conforme o programa avança.

O foco não está apenas em construir modelos ou escrever código — está em **entender o problema, comunicar descobertas e propor soluções que façam sentido para o negócio**.

## Autores

| Nome | RM | E-mail |
|---|---|---|
| Paulo Henrique Almeida | RM375573 | phraulino@outlook.com |

**Programa:** POSTECH AI Scientist — FIAP

## Fases do Projeto

| Fase | Tema | Status |
|---|---|---|
| Fase 1 | NPS Preditivo — Análise de satisfação em e-commerce | Concluída |
| Fase 2 | — | Aguardando |
| Fase 3 | — | Aguardando |
| Fase 4 | — | Aguardando |
| Fase 5 | — | Aguardando |

## Fase 1 — NPS Preditivo

Com o crescimento acelerado do e-commerce, uma empresa passou a lidar com alta variabilidade no **Net Promoter Score (NPS)** entre diferentes perfis de consumidores. O NPS é coletado apenas após o encerramento da jornada de compra, o que limita ações preventivas.

**Objetivo:** analisar os fatores que influenciam a satisfação dos clientes medida pelo NPS e propor uma abordagem preditiva capaz de agir antes da aplicação da pesquisa.

A EDA provocou uma mudança importante na formulação da solução: o `nps_score` permanece como desfecho de satisfação, mas o alvo operacional recomendado passa a ser a previsão/calibração do prazo de entrega e do risco de atraso. A razão é direta: atraso foi o fator mais associado ao baixo NPS, enquanto perfil do cliente e variáveis do pedido tiveram pouca relação com a nota.

### Links rápidos da entrega

| Material | Link |
|---|---|
| Documentação pública | [Abrir documentação](https://phraulino-space.github.io/tech-challenge-fiap/) |
| Resumo da entrega | [Abrir resumo](https://phraulino-space.github.io/tech-challenge-fiap/fase-1/resumo-entrega/) |
| Visão geral da Fase 1 | [Abrir visão geral](https://phraulino-space.github.io/tech-challenge-fiap/fase-1/) |
| EDA final | [Abrir EDA](https://phraulino-space.github.io/tech-challenge-fiap/fase-1/eda/) |
| Apresentação HTML | [Abrir slides](https://phraulino-space.github.io/tech-challenge-fiap/fase-1/slides.html) |
| Apresentação PDF | [Baixar PDF](https://phraulino-space.github.io/tech-challenge-fiap/fase-1/Tech%20Challenge%20_%20NPS%20e%20atraso%20na%20entrega.pdf) |
| Vídeo executivo | [Assistir no YouTube](https://youtu.be/eodKtPdOVdg) |
| Apresentação final | [Abrir página](https://phraulino-space.github.io/tech-challenge-fiap/fase-1/apresentacao-final/) |
| Notebook final | [Abrir notebook](https://github.com/PHRaulino-Space/tech-challenge-fiap/blob/main/notebooks/eda_final.ipynb) |
| Script pareado do notebook | [Abrir eda_final.py](https://github.com/PHRaulino-Space/tech-challenge-fiap/blob/main/notebooks/eda_final.py) |
| Como reproduzir | [Ver instruções](https://phraulino-space.github.io/tech-challenge-fiap/fase-1/getting-started/) |
| Avaliação da entrega | [Ver checklist](https://phraulino-space.github.io/tech-challenge-fiap/fase-1/avaliacao-entrega/) |

### Principais resultados

| Achado | Evidência |
|---|---|
| A base é majoritariamente detratora | 74,0% dos clientes são detratores |
| O problema não está em perfil ou pedido | Idade, região, ticket, desconto e parcelas têm baixa associação com o score |
| Atraso é o maior sinal operacional | `delivery_delay_days` tem correlação -0,60 com `nps_score` |
| Cumprir o prazo importa mais que velocidade | `delivery_time_days` ≈ 0; atraso derruba a nota média do score |
| O problema é sistêmico | Taxa de atraso varia de 88% a 91% entre regiões |
| Recompra valida o impacto | Detratores tiveram 0,0% de recompra em 30 dias |

O projeto segue a metodologia **CRISP-DM**:

| Etapa | Fase CRISP-DM | Status |
|---|---|---|
| Problema de Negócio | Business Understanding | Concluído |
| Business Canvas | Business Understanding | Concluído |
| Reflexões do Desafio | Business Understanding | Concluído |
| Análise e Hipóteses | Data Understanding | Concluído |
| EDA | Data Understanding | Concluído |
| Preparação dos Dados | Data Preparation | Concluído |
| Proposta de Solução | Modeling | Concluído |
| Avaliação dos Resultados | Evaluation | Concluído |
| Apresentação Final | Deployment | Concluído |

## Estrutura do Repositório

```
├── data/
│   └── desafio_nps_fase_1.csv       # Base de dados original do desafio
├── docs/                             # Documentação MkDocs
├── models/                           # Artefatos de modelos, quando houver
├── notebooks/                        # Jupyter Notebooks de análise
├── references/                       # Materiais de referência
├── reports/                          # Relatórios e visualizações geradas
│   └── figures/
├── tech_challenge_fiap/              # Código-fonte e base para pipelines
│   ├── config.py
│   ├── dataset.py
│   ├── features.py
│   ├── plots.py
│   └── modeling/
│       ├── train.py
│       └── predict.py
└── tests/                            # Estrutura inicial de testes
```

## Base de Dados

Arquivo: `data/desafio_nps_fase_1.csv` — 19 variáveis em quatro grupos:

| Grupo | Variáveis |
|---|---|
| Cliente | `customer_id`, `customer_age`, `customer_region`, `customer_tenure_months` |
| Pedido | `order_id`, `order_value`, `items_quantity`, `discount_value`, `payment_installments` |
| Logística | `delivery_time_days`, `delivery_delay_days`, `freight_value`, `delivery_attempts` |
| Atendimento | `customer_service_contacts`, `resolution_time_days`, `complaints_count` |
| Satisfação | `nps_score`, `csat_internal_score`, `repeat_purchase_30d` |

A variável-alvo analítica é `nps_score` (escala 0–10): detratores (0–6), neutros (7–8), promotores (9–10). Para a proposta final, o alvo operacional passa a ser previsão de prazo/risco de atraso, usando NPS e recompra como métricas de impacto.

## Como Reproduzir

### Pré-requisitos

- Python 3.12
- [Poetry](https://python-poetry.org/)

### Configuração

```bash
git clone https://github.com/PHRaulino-Space/tech-challenge-fiap.git
cd tech-challenge-fiap
make setup
```

### Principais comandos

| Comando | Descrição |
|---|---|
| `make setup` | Configura o ambiente completo (primeira vez) |
| `make requirements` | Instala/atualiza dependências |
| `make data` | Executa o pipeline de dados |
| `make lint` | Verifica o código com ruff |
| `make format` | Formata o código com ruff |
| `make test` | Executa a suíte de testes (estrutura inicial) |
| `make docs` | Serve a documentação em http://127.0.0.1:8000 |

### Notebooks

```bash
poetry run jupyter lab
```

## Documentação

A documentação completa está publicada em:

[https://phraulino-space.github.io/tech-challenge-fiap/](https://phraulino-space.github.io/tech-challenge-fiap/)

O código-fonte da documentação está em `docs/`, construída com MkDocs Material. Para visualizar localmente:

```bash
make docs
```

Ou, diretamente:

```bash
cd docs && mkdocs serve
```

## Tecnologias

- Python 3.12, Poetry
- pandas, numpy, scikit-learn
- Jupyter Lab
- MkDocs Material
- Ruff, pytest, pre-commit
- Data Science
