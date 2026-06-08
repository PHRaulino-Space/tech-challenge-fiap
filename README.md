# Tech Challenge — POSTECH AI Scientist

Repositório central das entregas do **Tech Challenge**, projeto integrador do programa **POSTECH AI Scientist** da FIAP. O Tech Challenge reúne, a cada fase, os conhecimentos aplicados nas disciplinas correspondentes e representa **90% da nota final** de cada fase.

**Repositório:** [github.com/PHRaulino-Space/tech-challenge-fiap](https://github.com/PHRaulino-Space/tech-challenge-fiap)

## O Projeto

O Tech Challenge é desenvolvido ao longo de **5 fases** do programa. Em cada fase, o grupo recebe um desafio aplicado que exige pensamento analítico, habilidades técnicas e comunicação orientada a negócio. Os desafios simulam cenários reais de atuação no mercado e evoluem em complexidade conforme o programa avança.

O foco não está apenas em construir modelos ou escrever código — está em **entender o problema, comunicar descobertas e propor soluções que façam sentido para o negócio**.

## Autores

| Nome | RM | E-mail |
|---|---|---|
| Paulo Henrique Almeida | RM375573 | phraulino@outlook.com |
| Gabriela Almeida | RM375633 | gabrielacmalmeida@gmail.com |

**Programa:** POSTECH AI Scientist — FIAP

## Fases do Projeto

| Fase | Tema | Status |
|---|---|---|
| Fase 1 | NPS Preditivo — Análise de satisfação em e-commerce | Em andamento |
| Fase 2 | — | Aguardando |
| Fase 3 | — | Aguardando |
| Fase 4 | — | Aguardando |
| Fase 5 | — | Aguardando |

## Fase 1 — NPS Preditivo

Com o crescimento acelerado do e-commerce, uma empresa passou a lidar com alta variabilidade no **Net Promoter Score (NPS)** entre diferentes perfis de consumidores. O NPS é coletado apenas após o encerramento da jornada de compra, o que limita ações preventivas.

**Objetivo:** analisar os fatores que influenciam a satisfação dos clientes medida pelo NPS e propor uma abordagem preditiva capaz de antecipar esse indicador antes da aplicação da pesquisa.

O projeto segue a metodologia **CRISP-DM**:

| Etapa | Fase CRISP-DM | Status |
|---|---|---|
| Business Canvas | Business Understanding | Em andamento |
| Reflexões do Desafio | Business Understanding | Em andamento |
| Análise e Hipóteses | Data Understanding | Em andamento |
| EDA | Data Understanding | Em andamento |
| Preparação dos Dados | Data Preparation | Pendente |
| Proposta de Solução | Modeling | Pendente |
| Avaliação dos Resultados | Evaluation | Pendente |
| Apresentação Final | Deployment | Pendente |

## Estrutura do Repositório

```
├── data/
│   └── desafio_nps_fase_1.csv       # Base de dados original do desafio
├── docs/                             # Documentação MkDocs
├── models/                           # Modelos treinados e artefatos
├── notebooks/                        # Jupyter Notebooks de análise
├── references/                       # Materiais de referência
├── reports/                          # Relatórios e visualizações geradas
│   └── figures/
├── tech_challenge_fiap/              # Código-fonte do projeto
│   ├── config.py
│   ├── dataset.py
│   ├── features.py
│   ├── plots.py
│   └── modeling/
│       ├── train.py
│       └── predict.py
└── tests/                            # Testes automatizados
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

A variável-alvo é `nps_score` (escala 0–10): detratores (0–6), neutros (7–8), promotores (9–10).

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
| `make test` | Executa os testes |
| `make docs` | Serve a documentação em http://127.0.0.1:8000 |

### Notebooks

```bash
poetry run jupyter lab
```

## Documentação

A documentação completa do projeto está em `docs/`, construída com MkDocs Material. Para visualizar localmente:

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
