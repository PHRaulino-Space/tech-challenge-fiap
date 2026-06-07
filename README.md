# Tech Challenge Fase 1 — NPS Preditivo

Projeto desenvolvido como entrega do Tech Challenge da Fase 1 do programa **POSTECH AI Scientist**. O objetivo é analisar dados operacionais de um e-commerce para entender os fatores que influenciam a satisfação dos clientes, medida pelo **Net Promoter Score (NPS)**, e propor uma abordagem preditiva capaz de antecipar esse indicador antes da aplicação da pesquisa.

## Contexto

Com o crescimento acelerado do e-commerce, a empresa passou a lidar com alta variabilidade no NPS entre diferentes perfis de consumidores. O NPS atualmente é coletado apenas após o encerramento da jornada de compra, o que limita ações preventivas. Este projeto transforma dados de pedidos, logística e atendimento em insights acionáveis para as áreas de negócio.

## Estrutura do Projeto

```
├── data/
│   └── desafio_nps_fase_1.csv       <- Base de dados original do desafio
│
├── docs/                             <- Documentação MkDocs
│   ├── docs/
│   │   ├── index.md
│   │   ├── getting-started.md
│   │   └── case-nps-preditivo.md
│   └── mkdocs.yml
│
├── models/                           <- Modelos treinados e artefatos
│
├── notebooks/                        <- Jupyter Notebooks de análise
│
├── references/                       <- Materiais de referência e dicionários
│
├── reports/                          <- Relatórios e visualizações geradas
│   └── figures/
│
├── tech_challenge_fiap/            <- Código-fonte do projeto
│   ├── config.py
│   ├── dataset.py
│   ├── features.py
│   ├── plots.py
│   └── modeling/
│       ├── train.py
│       └── predict.py
│
├── pyproject.toml
├── Makefile
└── requirements.txt
```

## Base de Dados

Arquivo CSV com dados históricos de pedidos, logística e atendimento ao cliente, contendo 19 variáveis distribuídas em quatro grupos:

| Grupo | Variáveis |
|---|---|
| Cliente | `customer_id`, `customer_age`, `customer_region`, `customer_tenure_months` |
| Pedido | `order_id`, `order_value`, `items_quantity`, `discount_value`, `payment_installments` |
| Logística | `delivery_time_days`, `delivery_delay_days`, `freight_value`, `delivery_attempts` |
| Atendimento | `customer_service_contacts`, `resolution_time_days`, `complaints_count` |
| Satisfação | `nps_score`, `csat_internal_score`, `repeat_purchase_30d` |

A variável-alvo é `nps_score` (escala 0–10): detratores (0–6), neutros (7–8), promotores (9–10).

## Metodologia

1. **Entendimento do negócio** — análise da dor de negócio e impacto do NPS em recompra, boca a boca e market share.
2. **Definição da target** — avaliação conceitual da variável `nps_score` como proxy de satisfação.
3. **Análise Exploratória (EDA)** — identificação de fatores críticos, perfis de detratores e pontos de ruptura na experiência do cliente.
4. **Modelagem preditiva** *(opcional)* — proposta de modelo de classificação ou regressão para prever o NPS antes da pesquisa.

## Como Reproduzir

### Pré-requisitos

- Python 3.12
- [Poetry](https://python-poetry.org/)

### Configuração do ambiente

```bash
make setup
```

Isso instala o Poetry (se necessário), cria o ambiente virtual, instala as dependências e configura os hooks de pre-commit.

### Principais comandos

```bash
make setup       # Configura o ambiente completo
make requirements # Instala dependências
make data        # Executa o pipeline de dados
make lint        # Verifica o código com ruff
make format      # Formata o código com ruff
make test        # Executa os testes
```

### Documentação local

```bash
cd docs && mkdocs serve
```

## Tecnologias

- Python 3.12
- pandas, numpy, scikit-learn
- Jupyter Lab / Notebook
- MkDocs
- Ruff (lint e formatação)
- Poetry (gestão de dependências)
- pre-commit

## Curso

**POSTECH AI Scientist — Fase 1**
Instituição: FIAP / PosTech
