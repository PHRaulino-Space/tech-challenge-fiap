# AGENTS.md

Context file for LLM agents working in this repository. Read this before making any changes.

---

## What This Project Is

**Tech Challenge — POSTECH AI Scientist (FIAP)**

Academic project developed across **5 phases** of the POSTECH AI Scientist program. Each phase presents an applied data science challenge worth 90% of the phase grade. This repository centralizes all deliverables across all phases.

**Author:**
- Paulo Henrique Almeida — RM375573 — phraulino@outlook.com

---

## Current State

Only **Phase 1** is active. Phases 2–5 are placeholders.

**Phase 1 — NPS Preditivo:** Analyze operational data from an e-commerce company to understand factors influencing customer satisfaction (NPS) and propose a predictive approach to anticipate NPS before the survey is applied.

The project follows the **CRISP-DM** methodology:

| Step | CRISP-DM Phase | Status |
|---|---|---|
| 1. Business Canvas | Business Understanding | In progress |
| 2. Reflexões do Desafio | Business Understanding | In progress |
| 3. Análise e Hipóteses | Data Understanding | In progress |
| 4. EDA | Data Understanding | In progress |
| 5. Preparação dos Dados | Data Preparation | Pending |
| 6. Proposta de Solução | Modeling | Pending |
| 7. Avaliação dos Resultados | Evaluation | Pending |
| 8. Apresentação Final | Deployment | Pending |

---

## Repository Structure

```
tech-challenge-fiap/
├── data/
│   └── desafio_nps_fase_1.csv      # Phase 1 dataset — do not modify
├── docs/                            # MkDocs documentation (see Docs section)
├── models/                          # Trained model artifacts
├── notebooks/
│   └── dados.ipynb                  # Main analysis notebook
├── references/                      # Reference materials and data dictionaries
├── reports/
│   └── figures/                     # Generated visualizations
├── tech_challenge_fiap/             # Python package (source code)
│   ├── config.py                    # Project paths and configuration
│   ├── dataset.py                   # Data loading and pipeline
│   ├── features.py                  # Feature engineering
│   ├── plots.py                     # Reusable plot functions
│   └── modeling/
│       ├── train.py                 # Model training
│       └── predict.py               # Inference
├── tests/                           # Test suite
├── AGENTS.md                        # This file
├── Makefile                         # Common commands
└── pyproject.toml                   # Dependencies and project metadata
```

---

## Tech Stack

| Tool | Purpose |
|---|---|
| Python 3.12 | Runtime |
| Poetry | Dependency management |
| pandas / numpy | Data manipulation |
| scikit-learn | Modeling |
| Jupyter Lab | Notebooks |
| MkDocs Material | Documentation site |
| Ruff | Linting and formatting |
| pytest | Tests |
| pre-commit | Git hooks |

---

## Common Commands

```bash
make setup          # First-time setup: Poetry, venv, deps, pre-commit hooks
make requirements   # Install/update dependencies
make docs           # Serve documentation locally at http://127.0.0.1:8000
make data           # Run data pipeline (dataset.py)
make lint           # Check code with ruff
make format         # Format code with ruff
make test           # Run test suite
make clean          # Remove compiled Python files
```

---

## Dataset — Phase 1

File: `data/desafio_nps_fase_1.csv`

19 variables across four groups:

| Group | Variables |
|---|---|
| Customer | `customer_id`, `customer_age`, `customer_region`, `customer_tenure_months` |
| Order | `order_id`, `order_value`, `items_quantity`, `discount_value`, `payment_installments` |
| Logistics | `delivery_time_days`, `delivery_delay_days`, `freight_value`, `delivery_attempts` |
| Support | `customer_service_contacts`, `resolution_time_days`, `complaints_count` |
| Satisfaction | `nps_score`, `csat_internal_score`, `repeat_purchase_30d` |

Target variable: `nps_score` (0–10) — detractors (0–6), neutrals (7–8), promoters (9–10).

---

## Documentation Structure

MkDocs Material site located in `docs/`. Source files are in `docs/docs/`.

```
docs/docs/
├── index.md                      # Home — project overview, authors, phase map
├── fase-1/
│   ├── index.md                  # Phase 1 overview
│   ├── planejamento.md           # Delivery plan (CRISP-DM)
│   ├── case-nps-preditivo.md     # Challenge description
│   ├── business-canvas.md        # Step 1
│   ├── reflexoes.md              # Step 2
│   ├── analise-hipoteses.md      # Step 3
│   ├── eda.md                    # Step 4
│   ├── preparacao-dados.md       # Step 5
│   ├── proposta-solucao.md       # Step 6
│   ├── avaliacao.md              # Step 7
│   ├── apresentacao-final.md     # Step 8
│   └── getting-started.md        # Reproduction instructions
├── fase-2/ to fase-5/            # Placeholders — not in nav yet
└── assets/extra.css              # Custom styles
```

To add a future phase to the nav, edit `docs/mkdocs.yml` under the `nav` key.

---

## Conventions

- **Language:** code and variable names in English; documentation, comments, and notebooks in Portuguese (pt-BR).
- **Formatting:** always run `make format` before committing.
- **Dependencies:** add packages via `poetry add <package>`, never edit `requirements.txt` directly — it is generated.
- **Notebooks:** keep notebooks in `notebooks/`. Reusable logic extracted to `tech_challenge_fiap/`.
- **Data:** never commit raw data files to the repository. `data/` is gitignored except for the original challenge file.
- **Models:** save artifacts to `models/`. Large binaries should not be committed.
- **Docs:** pages are written in Markdown. Run `make docs` to preview before pushing.
