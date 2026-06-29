# Getting Started

## Pré-requisitos

- Python 3.12
- [Poetry](https://python-poetry.org/) — gerenciador de dependências

## Configuração do ambiente

Clone o repositório e execute o comando de setup. Ele instala o Poetry (caso necessário), cria o ambiente virtual, instala as dependências e configura os hooks de pre-commit:

```bash
make setup
```

Para ativar o ambiente manualmente:

```bash
eval "$(make activate)"
# ou
poetry shell
```

## Principais comandos

| Comando | Descrição |
|---|---|
| `make setup` | Configura o ambiente completo (primeira vez) |
| `make requirements` | Instala/atualiza dependências |
| `make data` | Executa o pipeline de dados |
| `make lint` | Verifica o código com ruff |
| `make format` | Formata o código com ruff |
| `make test` | Executa os testes |
| `make clean` | Remove arquivos compilados Python |

## Base de dados

O arquivo de dados já está disponível em `data/desafio_nps_fase_1.csv`. Para reprocessá-lo via pipeline:

```bash
make data
```

## Reprodução Simples

Para reproduzir a análise sem usar o pipeline completo do projeto, basta usar o notebook final e a base original do desafio.

Arquivos necessários:

| Arquivo | Finalidade |
|---|---|
| `notebooks/eda_final.ipynb` | Notebook final da EDA |
| `data/desafio_nps_fase_1.csv` | Base de dados usada na análise |
| `data/metadados_desafio_nps_fase_1.json` | Dicionário de colunas usado para ordenar e documentar a jornada |

Passo a passo:

1. Configure o ambiente com as dependências do projeto:

```bash
make setup
```

2. Abra o Jupyter Lab:

```bash
poetry run jupyter lab
```

3. No Jupyter, abra `notebooks/eda_final.ipynb` e execute as células em ordem.

O notebook já lê os arquivos em `../data/`, então a estrutura de pastas precisa ser mantida:

```text
tech-challenge-fiap/
├── data/
│   ├── desafio_nps_fase_1.csv
│   └── metadados_desafio_nps_fase_1.json
└── notebooks/
    └── eda_final.ipynb
```

Essa é a forma mais direta de validar os gráficos, tabelas e conclusões da apresentação.

## Notebooks

Os notebooks de análise estão em `notebooks/`. Para iniciar o Jupyter Lab:

```bash
poetry run jupyter lab
```

Notebook principal da entrega:

| Arquivo | Descrição |
|---|---|
| `notebooks/eda_final.ipynb` | EDA final consolidada com os gráficos e evidências usados na apresentação |
| `notebooks/eda_final.py` | Versão Jupytext pareada do notebook final |
| `notebooks/dados.ipynb` | Notebook de exploração inicial |

Ao reproduzir a análise, considere a leitura final do projeto: o notebook parte do NPS como desfecho de satisfação, mas a conclusão operacional desloca a solução para previsão/calibração do prazo de entrega e risco de atraso.

Para regenerar o notebook final a partir do script pareado:

```bash
poetry run jupytext --to ipynb notebooks/eda_final.py -o notebooks/eda_final.ipynb
```

Para exportar a EDA final em HTML:

```bash
make eda2html
```

## Documentação local

Para servir esta documentação localmente:

```bash
cd docs && mkdocs serve
```

Acesse em `http://127.0.0.1:8000`.

Para gerar o build estático:

```bash
cd docs && mkdocs build
```
