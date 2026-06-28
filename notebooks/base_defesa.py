# ---
# jupyter:
#   jupytext:
#     text_representation:
#       extension: .py
#       format_name: percent
#       format_version: '1.3'
#       jupytext_version: 1.19.3
#   kernelspec:
#     display_name: tech-challenge-fiap-OMreDBxv-py3.12
#     language: python
#     name: python3
# ---

# %% [markdown]
# # Base de defesa — NPS Preditivo
#
# Este arquivo concentra a preparação mínima para iniciar as análises da defesa:
#
# - leitura do dataset da fase 1;
# - leitura e organização dos metadados;
# - ordenação das colunas pela jornada do cliente;
# - criação da categoria de NPS;
# - montagem da tabela básica de documentação e estatísticas.
#
# O formato segue o padrão Jupytext `percent`, permitindo executar o arquivo como
# notebook ou como script Python.

# %%
import json

from pathlib import Path

import pandas as pd
import plotly.express as px

# %% [markdown]
# ## Caminhos e constantes

# %%
BASE_DIR = Path(__file__).resolve().parents[1]
DATA_DIR = BASE_DIR / "data"
DATASET_PATH = DATA_DIR / "desafio_nps_fase_1.csv"
METADATA_PATH = DATA_DIR / "metadados_desafio_nps_fase_1.json"

CATEGORIAS_NPS = ["Detrator", "Neutro", "Promotor"]
CORES_NPS = {
    "Detrator": "#ef4444",
    "Neutro": "#f97316",
    "Promotor": "#0284c7",
}


# %% [markdown]
# ## Funções de preparação


# %%
def carregar_metadados(path: Path = METADATA_PATH) -> pd.DataFrame:
    """Carrega o dicionario de metadados das colunas."""
    return pd.read_json(path)


def ordenar_colunas_por_jornada(metadados_colunas: pd.DataFrame) -> list[str]:
    """Ordena as colunas conforme a etapa da jornada do cliente."""
    return sorted(
        metadados_colunas.keys(),
        key=lambda col: metadados_colunas[col].get("ordem_jornada", 99),
    )


def carregar_dataset(
    dataset_path: Path = DATASET_PATH,
    metadata_path: Path = METADATA_PATH,
) -> tuple[pd.DataFrame, pd.DataFrame, list[str]]:
    """Carrega o dataset, ordena colunas pela jornada e cria a categoria NPS."""
    metadados_colunas = carregar_metadados(metadata_path)
    colunas_ordenadas = ordenar_colunas_por_jornada(metadados_colunas)

    base = pd.read_csv(dataset_path)[colunas_ordenadas]
    base["nps_categoria"] = pd.cut(
        base["nps_score"],
        bins=[-0.1, 6, 8, 10],
        labels=CATEGORIAS_NPS,
    )

    return base, metadados_colunas, colunas_ordenadas


def separar_colunas_por_tipo(metadados_colunas: pd.DataFrame) -> tuple[list[str], list[str]]:
    """Separa variaveis quantitativas e qualitativas conforme os metadados."""
    cols_quant = [col for col, meta in metadados_colunas.items() if meta["tipo"] == "quantitativa"]
    cols_qual = [col for col, meta in metadados_colunas.items() if meta["tipo"] == "qualitativa"]

    return cols_quant, cols_qual


def montar_tabela_metadados(
    base: pd.DataFrame,
    metadados_colunas: pd.DataFrame,
) -> pd.DataFrame:
    """Monta a visao basica do dataset com estatisticas e metadados por coluna."""
    cols_quant, cols_qual = separar_colunas_por_tipo(metadados_colunas)

    infos_quant = base[cols_quant].describe().T
    for campo in ["descricao", "grupo", "tipo", "natureza", "ordem_jornada"]:
        infos_quant[campo] = infos_quant.index.map(
            lambda col: metadados_colunas.get(col, {}).get(
                campo,
                99 if campo == "ordem_jornada" else "-",
            )
        )

    infos_quant["dtype"] = infos_quant.index.map(lambda col: base[col].dtype)
    infos_quant["nulos"] = infos_quant.index.map(lambda col: base[col].isnull().sum())
    infos_quant["count"] = infos_quant.index.map(lambda col: base[col].count())

    colunas_base = [
        "descricao",
        "grupo",
        "ordem_jornada",
        "tipo",
        "natureza",
        "dtype",
        "nulos",
        "count",
    ]
    demais_colunas = [col for col in infos_quant.columns if col not in colunas_base]
    infos_quant = infos_quant[colunas_base + demais_colunas]

    infos_qual = pd.DataFrame(
        {
            col: {
                "descricao": metadados_colunas[col]["descricao"],
                "grupo": metadados_colunas[col]["grupo"],
                "ordem_jornada": metadados_colunas[col].get("ordem_jornada", 99),
                "tipo": metadados_colunas[col]["tipo"],
                "natureza": metadados_colunas[col]["natureza"],
                "dtype": base[col].dtype,
                "nulos": base[col].isnull().sum(),
                "count": base[col].count(),
            }
            for col in cols_qual
        }
    ).T
    infos_qual = infos_qual[colunas_base]

    return pd.concat([infos_quant, infos_qual], axis=0).sort_values("ordem_jornada").fillna("-")


def preparar_base_defesa() -> dict[str, object]:
    """Disponibiliza os objetos basicos para iniciar as analises."""
    base, metadados, colunas_ordenadas = carregar_dataset()
    cols_quant, cols_qual = separar_colunas_por_tipo(metadados)
    infos = montar_tabela_metadados(base, metadados)

    return {
        "df": base,
        "metadados_colunas": metadados,
        "colunas_ordenadas": colunas_ordenadas,
        "cols_quant": cols_quant,
        "cols_qual": cols_qual,
        "df_infos": infos,
        "categorias": CATEGORIAS_NPS,
        "cores": CORES_NPS,
    }


def gerar_json_highcharts(configuracao: dict) -> str:
    """Converte uma configuracao de grafico Highcharts para JSON formatado."""
    return json.dumps(configuracao, ensure_ascii=False, indent=2)


def gerar_highcharts_boxplot(
    base: pd.DataFrame,
    categoria_col: str,
    valor_col: str,
    categorias: list[str],
    titulo: str,
    eixo_y: str,
) -> dict:
    """Gera configuracao Highcharts para boxplot por categoria."""
    dados_boxplot = []

    for categoria in categorias:
        serie = base.loc[base[categoria_col] == categoria, valor_col].dropna()
        resumo = serie.quantile([0, 0.25, 0.5, 0.75, 1]).round(2)
        dados_boxplot.append(resumo.tolist())

    return {
        "chart": {"type": "boxplot"},
        "title": {"text": titulo},
        "xAxis": {"categories": categorias, "title": {"text": "Faixa de atraso"}},
        "yAxis": {"title": {"text": eixo_y}},
        "series": [
            {
                "name": eixo_y,
                "data": dados_boxplot,
            }
        ],
    }


def gerar_highcharts_linha(
    base: pd.DataFrame,
    categoria_col: str,
    series_cols: list[str],
    titulo: str,
    eixo_y: str,
) -> dict:
    """Gera configuracao Highcharts para linhas com uma serie por coluna numerica."""
    categorias = base[categoria_col].astype(str).tolist()

    return {
        "chart": {"type": "line"},
        "title": {"text": titulo},
        "xAxis": {"categories": categorias, "title": {"text": "Faixa de atraso"}},
        "yAxis": {"title": {"text": eixo_y}},
        "series": [
            {
                "name": coluna.replace("_", " ").title(),
                "data": base[coluna].round(2).tolist(),
            }
            for coluna in series_cols
        ],
    }


# %% [markdown]
# ## Objetos prontos para análise

# %%
objetos_base = preparar_base_defesa()

df = objetos_base["df"]
metadados_colunas = objetos_base["metadados_colunas"]
colunas_ordenadas = objetos_base["colunas_ordenadas"]
cols_quant = objetos_base["cols_quant"]
cols_qual = objetos_base["cols_qual"]
df_infos = objetos_base["df_infos"]
categorias = objetos_base["categorias"]
cores = objetos_base["cores"]

# %% [markdown]
# ## Boxplot — NPS por faixas de atraso
#
# Este gráfico compara a distribuição do `nps_score` entre pedidos entregues no prazo
# e pedidos com diferentes níveis de atraso.

# %%
faixas_atraso = [-0.1, 0, 2, 5, df["delivery_delay_days"].max()]
rotulos_faixas_atraso = [
    "Sem atraso",
    "1-2 dias",
    "3-5 dias",
    "6+ dias",
]

df_nps_atraso = df.copy()
df_nps_atraso["faixa_atraso"] = pd.cut(
    df_nps_atraso["delivery_delay_days"],
    bins=faixas_atraso,
    labels=rotulos_faixas_atraso,
    include_lowest=True,
)

fig_nps_por_faixa_atraso = px.box(
    df_nps_atraso,
    x="faixa_atraso",
    y="nps_score",
    color="faixa_atraso",
    category_orders={"faixa_atraso": rotulos_faixas_atraso},
    labels={
        "faixa_atraso": "Faixa de atraso",
        "nps_score": "Score NPS",
    },
    title="Distribuição do score NPS por faixas de atraso na entrega",
    points="outliers",
)

fig_nps_por_faixa_atraso.update_layout(
    showlegend=False,
    title_x=0.5,
    xaxis_title="Dias de atraso na entrega",
    yaxis_title="Score NPS",
)

fig_nps_por_faixa_atraso.show()

# %% [markdown]
# ### Dados do boxplot em JSON para Highcharts

# %%
highcharts_nps_por_faixa_atraso = gerar_highcharts_boxplot(
    base=df_nps_atraso,
    categoria_col="faixa_atraso",
    valor_col="nps_score",
    categorias=rotulos_faixas_atraso,
    titulo="Distribuição do score NPS por faixas de atraso na entrega",
    eixo_y="Score NPS",
)

json_highcharts_nps_por_faixa_atraso = gerar_json_highcharts(highcharts_nps_por_faixa_atraso)

print(json_highcharts_nps_por_faixa_atraso)

# %% [markdown]
# ## Linha — média e mediana do NPS por faixas de atraso
#
# Este gráfico resume a tendência central do `nps_score` em cada faixa de atraso,
# permitindo comparar a média e a mediana da satisfação.

# %%
nps_resumo_faixa_atraso = (
    df_nps_atraso.groupby("faixa_atraso", observed=False)["nps_score"]
    .agg(media="mean", mediana="median")
    .reset_index()
)

nps_resumo_faixa_atraso_longo = nps_resumo_faixa_atraso.melt(
    id_vars="faixa_atraso",
    value_vars=["media", "mediana"],
    var_name="medida",
    value_name="nps_score",
)

fig_nps_media_mediana_por_faixa_atraso = px.line(
    nps_resumo_faixa_atraso_longo,
    x="faixa_atraso",
    y="nps_score",
    color="medida",
    markers=True,
    category_orders={"faixa_atraso": rotulos_faixas_atraso},
    labels={
        "faixa_atraso": "Faixa de atraso",
        "nps_score": "Score NPS",
        "medida": "Medida",
    },
    title="Média e mediana do score NPS por faixas de atraso na entrega",
)

fig_nps_media_mediana_por_faixa_atraso.update_layout(
    title_x=0.5,
    xaxis_title="Dias de atraso na entrega",
    yaxis_title="Score NPS",
)

fig_nps_media_mediana_por_faixa_atraso.show()

# %% [markdown]
# ### Dados da linha em JSON para Highcharts

# %%
highcharts_nps_media_mediana_por_faixa_atraso = gerar_highcharts_linha(
    base=nps_resumo_faixa_atraso,
    categoria_col="faixa_atraso",
    series_cols=["media", "mediana"],
    titulo="Média e mediana do score NPS por faixas de atraso na entrega",
    eixo_y="Score NPS",
)

json_highcharts_nps_media_mediana_por_faixa_atraso = gerar_json_highcharts(
    highcharts_nps_media_mediana_por_faixa_atraso
)

json_highcharts_nps_media_mediana_por_faixa_atraso

# %% [markdown]
# ## Barras — atraso x reclamação
#
# Este gráfico compara o percentual de pedidos com reclamação formal entre pedidos
# entregues com e sem atraso.

# %%
df_atraso_reclamacao = df.copy()
df_atraso_reclamacao["status_atraso"] = (
    df_atraso_reclamacao["delivery_delay_days"]
    .gt(0)
    .map(
        {
            False: "Sem atraso",
            True: "Com atraso",
        }
    )
)
df_atraso_reclamacao["teve_reclamacao"] = df_atraso_reclamacao["complaints_count"].gt(0)

rotulos_status_atraso = ["Sem atraso", "Com atraso"]

atraso_reclamacao_resumo = (
    df_atraso_reclamacao.groupby("status_atraso", observed=False)
    .agg(
        pedidos=("order_id", "count"),
        pedidos_com_reclamacao=("teve_reclamacao", "sum"),
        percentual_reclamacao=("teve_reclamacao", "mean"),
    )
    .reindex(rotulos_status_atraso)
    .reset_index()
)
atraso_reclamacao_resumo["percentual_reclamacao"] *= 100
atraso_reclamacao_resumo["texto_percentual"] = atraso_reclamacao_resumo[
    "percentual_reclamacao"
].map(lambda valor: f"{valor:.1f}%")

fig_atraso_reclamacao = px.bar(
    atraso_reclamacao_resumo,
    x="status_atraso",
    y="percentual_reclamacao",
    color="status_atraso",
    text="texto_percentual",
    category_orders={"status_atraso": rotulos_status_atraso},
    color_discrete_map={
        "Sem atraso": "#0284c7",
        "Com atraso": "#ef4444",
    },
    labels={
        "status_atraso": "Status de atraso",
        "percentual_reclamacao": "% de pedidos com reclamação",
    },
    title="Percentual de reclamações entre pedidos com e sem atraso",
)

fig_atraso_reclamacao.update_layout(
    showlegend=False,
    title_x=0.5,
    xaxis_title="Status de atraso",
    yaxis_title="% de pedidos com reclamação",
    yaxis_ticksuffix="%",
    yaxis_range=[0, 105],
)
fig_atraso_reclamacao.update_traces(
    textposition="outside",
    hovertemplate=(
        "<b>%{x}</b><br>"
        "Pedidos com reclamação: %{customdata[0]}<br>"
        "Total de pedidos: %{customdata[1]}<br>"
        "% com reclamação: %{y:.1f}%<extra></extra>"
    ),
    customdata=atraso_reclamacao_resumo[["pedidos_com_reclamacao", "pedidos"]].to_numpy(),
)

fig_atraso_reclamacao.show()

# %% [markdown]
# ### Dados das barras em JSON para Highcharts

# %%
highcharts_atraso_reclamacao = {
    "chart": {"type": "column"},
    "title": {"text": "Percentual de reclamações entre pedidos com e sem atraso"},
    "xAxis": {
        "categories": rotulos_status_atraso,
        "title": {"text": "Status de atraso"},
    },
    "yAxis": {
        "min": 0,
        "max": 100,
        "title": {"text": "% de pedidos com reclamação"},
        "labels": {"format": "{value}%"},
    },
    "tooltip": {
        "pointFormat": (
            "Pedidos com reclamação: <b>{point.com_reclamacao}</b><br>"
            "Total de pedidos: <b>{point.total}</b><br>"
            "% com reclamação: <b>{point.y:.1f}%</b>"
        )
    },
    "plotOptions": {
        "column": {
            "dataLabels": {
                "enabled": True,
                "format": "{point.y:.1f}%",
            }
        }
    },
    "series": [
        {
            "name": "% com reclamação",
            "colorByPoint": True,
            "data": [
                {
                    "name": linha["status_atraso"],
                    "y": round(linha["percentual_reclamacao"], 2),
                    "color": "#0284c7" if linha["status_atraso"] == "Sem atraso" else "#ef4444",
                    "com_reclamacao": int(linha["pedidos_com_reclamacao"]),
                    "total": int(linha["pedidos"]),
                }
                for _, linha in atraso_reclamacao_resumo.iterrows()
            ],
        }
    ],
}

json_highcharts_atraso_reclamacao = gerar_json_highcharts(highcharts_atraso_reclamacao)

print(json_highcharts_atraso_reclamacao)

# %% [markdown]
# ## Barras — reclamações formais por faixas de atraso
#
# Este gráfico compara a média de reclamações formais (`complaints_count`) entre
# faixas de atraso.

# %%
reclamacoes_nps_faixa_atraso = (
    df_nps_atraso.groupby("faixa_atraso", observed=False)
    .agg(
        media_reclamacoes=("complaints_count", "mean"),
    )
    .reset_index()
)

fig_reclamacoes_nps_por_faixa_atraso = px.bar(
    reclamacoes_nps_faixa_atraso,
    x="faixa_atraso",
    y="media_reclamacoes",
    color="faixa_atraso",
    text=reclamacoes_nps_faixa_atraso["media_reclamacoes"].map(lambda valor: f"{valor:.2f}"),
    category_orders={"faixa_atraso": rotulos_faixas_atraso},
    color_discrete_map={
        "Sem atraso": "#0284c7",
        "1-2 dias": "#f97316",
        "3-5 dias": "#ef4444",
        "6+ dias": "#7f1d1d",
    },
    labels={
        "faixa_atraso": "Faixa de atraso",
        "media_reclamacoes": "Média de reclamações formais",
    },
    title="Média de reclamações formais por faixas de atraso na entrega",
)

fig_reclamacoes_nps_por_faixa_atraso.update_layout(
    showlegend=False,
    title_x=0.5,
    xaxis_title="Dias de atraso na entrega",
    yaxis_title="Média de reclamações formais",
)
fig_reclamacoes_nps_por_faixa_atraso.update_traces(
    textposition="outside",
    selector={"type": "bar"},
)

fig_reclamacoes_nps_por_faixa_atraso.show()

# %% [markdown]
# ### Dados das barras em JSON para Highcharts

# %%
highcharts_reclamacoes_nps_por_faixa_atraso = {
    "chart": {"type": "column"},
    "title": {"text": "Média de reclamações formais por faixas de atraso na entrega"},
    "xAxis": {
        "categories": rotulos_faixas_atraso,
        "title": {"text": "Faixa de atraso"},
    },
    "yAxis": {
        "title": {"text": "Média de reclamações formais"},
        "min": 0,
    },
    "tooltip": {"pointFormat": "Média de reclamações: <b>{point.y:.2f}</b>"},
    "plotOptions": {
        "column": {
            "dataLabels": {
                "enabled": True,
                "format": "{point.y:.2f}",
            }
        },
    },
    "series": [
        {
            "name": "Média de reclamações formais",
            "data": reclamacoes_nps_faixa_atraso["media_reclamacoes"].round(2).tolist(),
            "color": "#ef4444",
        }
    ],
}

json_highcharts_reclamacoes_nps_por_faixa_atraso = gerar_json_highcharts(
    highcharts_reclamacoes_nps_por_faixa_atraso
)

print(json_highcharts_reclamacoes_nps_por_faixa_atraso)

# %% [markdown]
# ## Barras — recompra em 30 dias por faixas de atraso
#
# Este gráfico compara o percentual de pedidos com recompra em até 30 dias
# (`repeat_purchase_30d`) entre pedidos entregues no prazo e pedidos com diferentes
# níveis de atraso.

# %%
recompra_faixa_atraso = (
    df_nps_atraso.groupby("faixa_atraso", observed=False)
    .agg(
        pedidos=("order_id", "count"),
        pedidos_com_recompra=("repeat_purchase_30d", "sum"),
        percentual_recompra=("repeat_purchase_30d", "mean"),
    )
    .reset_index()
)
recompra_faixa_atraso["percentual_recompra"] *= 100
recompra_faixa_atraso["texto_percentual"] = recompra_faixa_atraso["percentual_recompra"].map(
    lambda valor: f"{valor:.1f}%"
)

fig_recompra_por_faixa_atraso = px.bar(
    recompra_faixa_atraso,
    x="faixa_atraso",
    y="percentual_recompra",
    color="faixa_atraso",
    text="texto_percentual",
    category_orders={"faixa_atraso": rotulos_faixas_atraso},
    color_discrete_map={
        "Sem atraso": "#0284c7",
        "1-2 dias": "#f97316",
        "3-5 dias": "#ef4444",
        "6+ dias": "#7f1d1d",
    },
    labels={
        "faixa_atraso": "Faixa de atraso",
        "percentual_recompra": "% de pedidos com recompra em 30 dias",
    },
    title="Percentual de recompra em 30 dias por faixas de atraso na entrega",
)

fig_recompra_por_faixa_atraso.update_layout(
    showlegend=False,
    title_x=0.5,
    xaxis_title="Dias de atraso na entrega",
    yaxis_title="% de pedidos com recompra em 30 dias",
    yaxis_ticksuffix="%",
    yaxis_range=[0, 100],
)
fig_recompra_por_faixa_atraso.update_traces(
    textposition="outside",
    hovertemplate=(
        "<b>%{x}</b><br>"
        "Pedidos com recompra: %{customdata[0]}<br>"
        "Total de pedidos: %{customdata[1]}<br>"
        "% com recompra: %{y:.1f}%<extra></extra>"
    ),
    customdata=recompra_faixa_atraso[["pedidos_com_recompra", "pedidos"]].to_numpy(),
)

fig_recompra_por_faixa_atraso.show()

# %% [markdown]
# ### Dados das barras em JSON para Highcharts

# %%
highcharts_recompra_por_faixa_atraso = {
    "chart": {"type": "column"},
    "title": {"text": "Percentual de recompra em 30 dias por faixas de atraso na entrega"},
    "xAxis": {
        "categories": rotulos_faixas_atraso,
        "title": {"text": "Faixa de atraso"},
    },
    "yAxis": {
        "min": 0,
        "max": 100,
        "title": {"text": "% de pedidos com recompra em 30 dias"},
        "labels": {"format": "{value}%"},
    },
    "tooltip": {
        "pointFormat": (
            "Pedidos com recompra: <b>{point.com_recompra}</b><br>"
            "Total de pedidos: <b>{point.total}</b><br>"
            "% com recompra: <b>{point.y:.1f}%</b>"
        )
    },
    "plotOptions": {
        "column": {
            "dataLabels": {
                "enabled": True,
                "format": "{point.y:.1f}%",
            }
        }
    },
    "series": [
        {
            "name": "% com recompra em 30 dias",
            "colorByPoint": True,
            "data": [
                {
                    "name": linha["faixa_atraso"],
                    "y": round(linha["percentual_recompra"], 2),
                    "color": {
                        "Sem atraso": "#0284c7",
                        "1-2 dias": "#f97316",
                        "3-5 dias": "#ef4444",
                        "6+ dias": "#7f1d1d",
                    }[linha["faixa_atraso"]],
                    "com_recompra": int(linha["pedidos_com_recompra"]),
                    "total": int(linha["pedidos"]),
                }
                for _, linha in recompra_faixa_atraso.iterrows()
            ],
        }
    ],
}

json_highcharts_recompra_por_faixa_atraso = gerar_json_highcharts(
    highcharts_recompra_por_faixa_atraso
)

print(json_highcharts_recompra_por_faixa_atraso)
