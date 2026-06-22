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

# %% [raw]
# ---
# title: "EDA Final — NPS Preditivo"
# subtitle: "O Que os Dados Revelam sobre a Satisfação do Cliente"
# author: "Paulo Henrique Raulino"
# date: today
# format:
#   html:
#     toc: true
#     code-fold: true
#     embed-resources: true
# ---

# %% [markdown]
# # EDA Final — NPS Preditivo: O Que os Dados Revelam
#
# > **Pergunta central:** quais fatores operacionais realmente influenciam a satisfação
# > do cliente e como a empresa pode agir de forma proativa antes da pesquisa de NPS?
#
# Esta análise percorre a jornada do cliente — compra, entrega e atendimento — para
# identificar onde a experiência se rompe e qual o tamanho real do problema.

# %%

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import plotly.io as pio

from plotly.subplots import make_subplots

pio.renderers.default = "notebook_connected"
pd.set_option("display.max_colwidth", None)

metadados_colunas = pd.read_json("../data/metadados_desafio_nps_fase_1.json")
colunas_ordenadas = sorted(
    metadados_colunas.keys(), key=lambda col: metadados_colunas[col].get("ordem_jornada", 99)
)
df = pd.read_csv("../data/desafio_nps_fase_1.csv")[colunas_ordenadas]
df["nps_categoria"] = pd.cut(
    df["nps_score"], bins=[-0.1, 6, 8, 10], labels=["Detrator", "Neutro", "Promotor"]
)

categorias = ["Detrator", "Neutro", "Promotor"]
cores = {"Detrator": "#ef4444", "Neutro": "#f97316", "Promotor": "#0284c7"}

df["teve_atraso"] = df["delivery_delay_days"] > 0
df["teve_contato_sac"] = df["customer_service_contacts"] > 0
df["entregou_no_prazo"] = df["delivery_delay_days"] <= 0

ordem_degradacao = ["Sem Problemas", "Só Atraso", "Só SAC", "Atraso + SAC"]
df["perfil_degradacao"] = df.apply(
    lambda r: (
        "Atraso + SAC"
        if r["teve_atraso"] and r["teve_contato_sac"]
        else "Só Atraso"
        if r["teve_atraso"]
        else "Só SAC"
        if r["teve_contato_sac"]
        else "Sem Problemas"
    ),
    axis=1,
)
df["perfil_degradacao"] = pd.Categorical(
    df["perfil_degradacao"], categories=ordem_degradacao, ordered=True
)

cores_degradacao = {
    "Sem Problemas": "#0284c7",
    "Só Atraso": "#f97316",
    "Só SAC": "#f97316",
    "Atraso + SAC": "#ef4444",
}

# %% [markdown]
# ## 1. O Ponto de Partida: 74% dos Clientes São Detratores
#
# Antes de qualquer análise cruzada, o primeiro dado já comunica a urgência do problema.
# A base não está distribuída de forma equilibrada entre as três categorias de NPS —
# ela pende estruturalmente para detratores.
#
# Com NPS médio de **4,38** — abaixo do ponto neutro (7) — a empresa não está lidando
# com exceções de insatisfação. Está lidando com um padrão: **3 em cada 4 clientes
# avaliariam negativamente a marca para outras pessoas**.

# %%
dist_nps = df["nps_categoria"].value_counts().reindex(categorias)
dist_nps_pct = (dist_nps / dist_nps.sum() * 100).round(1)
labels_dist = [f"{n:,}<br><sub>{p}%</sub>" for n, p in zip(dist_nps.values, dist_nps_pct.values)]

fig = px.bar(
    dist_nps,
    x=dist_nps.index,
    y=dist_nps.values,
    labels={"x": "Categoria NPS", "y": "Clientes"},
    title="Distribuição de Clientes por Categoria NPS",
    color=dist_nps.index,
    color_discrete_map=cores,
    text=labels_dist,
)
fig.update_traces(textposition="outside", textfont_size=13)
fig.update_layout(showlegend=False, title_x=0.5, height=420)
fig.show()

# %% [markdown]
# ## 2. Onde Está o Problema? As Correlações Apontam o Caminho
#
# Antes de explorar grupo a grupo, o heatmap de correlações de todas as variáveis
# operacionais com o NPS já entrega um mapa de prioridades.
#
# O sinal é concentrado: **duas variáveis operacionais respondem por quase toda a
# variação observada no NPS** — e ambas estão na execução pós-compra, não no momento
# da transação.

# %%
cols_corr = [
    "delivery_delay_days",
    "complaints_count",
    "customer_service_contacts",
    "resolution_time_days",
    "delivery_time_days",
    "freight_value",
    "delivery_attempts",
    "order_value",
    "discount_value",
    "payment_installments",
    "items_quantity",
    "customer_age",
    "customer_tenure_months",
    "nps_score",
]
corr_geral = df[cols_corr].corr()[["nps_score"]].drop("nps_score").sort_values("nps_score")

fig = px.bar(
    corr_geral,
    x="nps_score",
    y=corr_geral.index,
    orientation="h",
    title="Correlação de Todas as Variáveis Operacionais com o NPS Score",
    labels={"nps_score": "Correlação com NPS", "y": "Variável"},
    color="nps_score",
    color_continuous_scale=["#ef4444", "#f5f5f5", "#0284c7"],
    color_continuous_midpoint=0,
    text=corr_geral["nps_score"].round(2),
)
fig.update_traces(textposition="outside")
fig.update_layout(
    title_x=0.5,
    height=520,
    xaxis_range=[-0.75, 0.75],
    coloraxis_showscale=False,
)
fig.show()

# %% [markdown]
# **O que os dados mostram:**
#
# | Variável | Correlação | Grupo |
# | :--- | :---: | :--- |
# | `delivery_delay_days` | **-0,60** | Logística |
# | `complaints_count` | -0,50 | Atendimento |
# | `customer_service_contacts` | -0,35 | Atendimento |
# | `resolution_time_days` | -0,19 | Atendimento |
# | Todas as demais | ≈ 0 | Pedido / Cliente |
#
# **O que isso significa para o negócio:** o problema não está em quem é o cliente,
# nem no que ele comprou. Está na execução operacional — entrega e atendimento.
# O momento da transação (valor do pedido, parcelas, desconto) é irrelevante
# para a satisfação.

# %% [markdown]
# ## 3. A Análise Grupo a Grupo — Mapeando a Jornada
#
# A análise segue o fluxo cronológico da experiência do cliente. Para cada grupo,
# um heatmap de correlação e boxplots por categoria NPS revelam se aquele ponto
# da jornada influencia a satisfação.

# %%
fig = make_subplots(
    rows=2,
    cols=2,
    subplot_titles=[
        "Grupo Cliente",
        "Grupo Pedido",
        "Grupo Logística",
        "Grupo Atendimento",
    ],
)

grupos = {
    (1, 1): ["customer_age", "customer_tenure_months", "nps_score"],
    (1, 2): [
        "order_value",
        "items_quantity",
        "discount_value",
        "payment_installments",
        "nps_score",
    ],
    (2, 1): [
        "delivery_time_days",
        "delivery_delay_days",
        "freight_value",
        "delivery_attempts",
        "nps_score",
    ],
    (2, 2): ["customer_service_contacts", "resolution_time_days", "complaints_count", "nps_score"],
}

for (row, col), cols in grupos.items():
    corr_m = df[cols].corr()
    fig.add_trace(
        go.Heatmap(
            z=corr_m.values,
            x=corr_m.columns.tolist(),
            y=corr_m.index.tolist(),
            colorscale="RdBu_r",
            zmin=-1,
            zmax=1,
            text=corr_m.round(2).values,
            texttemplate="%{text}",
            showscale=False,
        ),
        row=row,
        col=col,
    )

fig.update_layout(
    title="Heatmaps de Correlação por Grupo da Jornada",
    title_x=0.5,
    height=700,
)
fig.show()

# %% [markdown]
# **Resultado consolidado da análise por grupo:**
#
# | Grupo | Sinal com o NPS | Principal variável |
# | :--- | :--- | :--- |
# | **Cliente** | Nenhum | — |
# | **Pedido** | Nenhum | — |
# | **Logística** | **Forte** | `delivery_delay_days` (-0,60) |
# | **Atendimento** | Moderado | `complaints_count` (-0,50) |
#
# A insatisfação não discrimina perfil de cliente nem valor de compra.
# Ela está concentrada na execução operacional — especificamente no que acontece
# depois que o pedido é confirmado.

# %% [markdown]
# ## 4. Os Quatro Perfis de Degradação da Experiência
#
# Com os dois sinais mais fortes identificados (`delivery_delay_days` e
# `customer_service_contacts`), criamos perfis binários que segmentam cada cliente
# pelo que de fato aconteceu com sua jornada.
#
# O resultado revela uma **escada de degradação** — cada problema acumulado
# empurra o NPS para baixo de forma consistente.

# %%
nps_por_perfil = (
    df.groupby("perfil_degradacao", observed=True)["nps_score"].mean().round(2).reset_index()
)

fig = px.bar(
    nps_por_perfil,
    x="perfil_degradacao",
    y="nps_score",
    color="perfil_degradacao",
    color_discrete_map=cores_degradacao,
    text="nps_score",
    title="NPS Médio por Perfil de Degradação da Experiência",
    labels={"perfil_degradacao": "Perfil", "nps_score": "NPS Médio"},
    category_orders={"perfil_degradacao": ordem_degradacao},
)
fig.update_traces(textposition="outside")
fig.update_layout(showlegend=False, title_x=0.5, height=430, yaxis_range=[0, 10])
fig.show()

# %% [markdown]
# | Perfil | Clientes | NPS Médio | % Detratores |
# | :--- | :---: | :---: | :---: |
# | **Sem Problemas** | 65 (2,6%) | **8,23** | 13,8% |
# | **Só SAC** | 212 (8,5%) | 6,43 | 43,4% |
# | **Só Atraso** | 489 (19,6%) | 5,19 | 65,2% |
# | **Atraso + SAC** | 1.734 (69,4%) | **3,76** | 82,5% |
#
# Dois achados críticos nesta tabela:
#
# 1. **Apenas 65 clientes (2,6%) passaram pela jornada sem nenhum problema operacional.**
#    Isso significa que a operação entrega uma experiência limpa para menos de 3%
#    da base. O problema não é exceção — é a regra.
#
# 2. **69,4% dos clientes estão no pior perfil possível (Atraso + SAC).**
#    Mais de 2 em cada 3 clientes sofreram atraso E precisaram acionar o SAC.
#    O NPS médio desse grupo é 3,76 — dentro da faixa de detratores.

# %%
dist = (
    df.groupby(["perfil_degradacao", "nps_categoria"], observed=True)
    .size()
    .unstack(fill_value=0)
    .reindex(ordem_degradacao)[["Detrator", "Neutro", "Promotor"]]
)
dist_pct = dist.div(dist.sum(axis=1), axis=0) * 100

fig = go.Figure()
for cat in ["Promotor", "Neutro", "Detrator"]:
    fig.add_trace(
        go.Bar(
            name=cat,
            x=dist_pct.index.tolist(),
            y=dist_pct[cat].tolist(),
            marker_color=cores[cat],
            text=(dist_pct[cat].round(1).astype(str) + "%").tolist(),
            textposition="inside",
        )
    )
fig.update_layout(
    barmode="stack",
    title="Distribuição de NPS por Perfil de Degradação",
    title_x=0.5,
    yaxis_title="% de Clientes",
    height=450,
    legend_title="Categoria NPS",
)
fig.show()

# %% [markdown]
# ## 5. De Onde Vêm os Detratores?
#
# Olhando os **1.851 detratores** da base pelo ângulo do perfil de degradação,
# a concentração é ainda mais evidente.

# %%
det = (
    df[df["nps_categoria"] == "Detrator"]["perfil_degradacao"]
    .value_counts()
    .reindex(ordem_degradacao)
    .fillna(0)
    .astype(int)
    .reset_index()
)
det.columns = ["perfil_degradacao", "detratores"]
det["pct"] = (det["detratores"] / det["detratores"].sum() * 100).round(1)
det["label"] = det["detratores"].astype(str) + "\n(" + det["pct"].astype(str) + "%)"

fig = px.bar(
    det,
    x="perfil_degradacao",
    y="detratores",
    color="perfil_degradacao",
    color_discrete_map=cores_degradacao,
    text="label",
    title="Origem dos Detratores — Quebra por Perfil de Degradação",
    labels={"perfil_degradacao": "Perfil", "detratores": "Detratores"},
    category_orders={"perfil_degradacao": ordem_degradacao},
)
fig.update_traces(textposition="outside")
fig.update_layout(showlegend=False, title_x=0.5, height=430)
fig.show()

# %% [markdown]
# **77,3% de todos os detratores vêm do perfil "Atraso + SAC".**
# Os 9 detratores do perfil "Sem Problemas" (0,5%) representam a variação natural
# do indicador — clientes que dariam NPS baixo independente da operação.
#
# O restante — **99,5% dos detratores** — teve ao menos um problema operacional
# identificável durante a jornada.

# %% [markdown]
# ## 6. O Comportamento Confirma a Percepção
#
# NPS é uma declaração de intenção. A recompra em 30 dias é o comportamento real.
# Quando os dois se alinham perfeitamente, a análise ganha credibilidade máxima.

# %%
rec_nps = (
    df.groupby("nps_categoria", observed=True)["repeat_purchase_30d"]
    .mean()
    .mul(100)
    .round(1)
    .reindex(categorias)
    .reset_index()
)
rec_nps.columns = ["nps_categoria", "pct_recompra"]
rec_nps["label"] = rec_nps["pct_recompra"].astype(str) + "%"

rec_perf = (
    df.groupby("perfil_degradacao", observed=True)["repeat_purchase_30d"]
    .mean()
    .mul(100)
    .round(1)
    .reset_index()
)
rec_perf.columns = ["perfil_degradacao", "pct_recompra"]
rec_perf["label"] = rec_perf["pct_recompra"].astype(str) + "%"

fig = make_subplots(
    rows=1,
    cols=2,
    subplot_titles=["Por Categoria NPS", "Por Perfil de Degradação"],
)

fig.add_trace(
    go.Bar(
        x=rec_nps["nps_categoria"],
        y=rec_nps["pct_recompra"],
        text=rec_nps["label"],
        textposition="outside",
        marker_color=[cores[c] for c in categorias],
        showlegend=False,
    ),
    row=1,
    col=1,
)

fig.add_trace(
    go.Bar(
        x=rec_perf["perfil_degradacao"],
        y=rec_perf["pct_recompra"],
        text=rec_perf["label"],
        textposition="outside",
        marker_color=[cores_degradacao[p] for p in ordem_degradacao],
        showlegend=False,
    ),
    row=1,
    col=2,
)

fig.update_layout(
    title="% de Recompra em 30 dias",
    title_x=0.5,
    height=440,
    yaxis_range=[0, 110],
    yaxis2_range=[0, 110],
)
fig.update_xaxes(categoryorder="array", categoryarray=categorias, row=1, col=1)
fig.update_xaxes(categoryorder="array", categoryarray=ordem_degradacao, row=1, col=2)
fig.show()

# %% [markdown]
# **O dado mais contundente da análise:**
#
# - **Detratores: 0% de recompra em 30 dias.** Zero. Nenhum cliente que avaliou
#   negativamente voltou a comprar no período.
# - **Promotores: 100% de recompra.** Todos os clientes satisfeitos voltaram.
# - **Neutros: 3,8%** — próximos do comportamento de detratores.
#
# A percepção e o comportamento estão em alinhamento perfeito. Isso valida a
# análise e reforça o NPS como indicador acionável — não apenas uma pesquisa
# de satisfação, mas um preditor direto de receita futura.

# %% [markdown]
# ## 7. O NPS Interno (CSAT) Confirma o Diagnóstico
#
# O indicador interno de satisfação (CSAT) acompanha o NPS em todos os perfis,
# validando que a percepção capturada externamente está alinhada com o que a
# empresa mede internamente.

# %%
csat_nps = (
    df.groupby("perfil_degradacao", observed=True)
    .agg(nps_medio=("nps_score", "mean"), csat_medio=("csat_internal_score", "mean"))
    .round(2)
    .reset_index()
)

fig = make_subplots(rows=1, cols=2, subplot_titles=["NPS Médio", "CSAT Interno Médio"])
for col_idx, (col, ymax) in enumerate([("nps_medio", 10), ("csat_medio", 10)], start=1):
    for _, row in csat_nps.iterrows():
        fig.add_trace(
            go.Bar(
                x=[row["perfil_degradacao"]],
                y=[row[col]],
                marker_color=cores_degradacao[row["perfil_degradacao"]],
                text=[str(row[col])],
                textposition="outside",
                showlegend=False,
            ),
            row=1,
            col=col_idx,
        )

fig.update_layout(
    title="NPS vs CSAT Interno por Perfil de Degradação",
    title_x=0.5,
    height=440,
)
fig.update_xaxes(categoryorder="array", categoryarray=ordem_degradacao)
fig.update_yaxes(range=[0, 10])
fig.show()

# %% [markdown]
# Os dois indicadores contam a mesma história e na mesma ordem de magnitude.
# Não há divergência entre o que o cliente declara (NPS) e o que a empresa
# mede internamente (CSAT) — o diagnóstico é consistente.

# %% [markdown]
# ## 8. O Problema Não É Geográfico — É Sistêmico
#
# A análise individual de `customer_region` mostrou variação de apenas **0,28 pontos**
# de NPS entre a melhor (Sul: 4,49) e a pior região (Centro-Oeste: 4,21).
# Mas a pergunta mais precisa é outra: certas regiões concentram mais atrasos?
# Se sim, o problema regional seria uma consequência logística, não demográfica.

# %%
atraso_reg = (
    df.groupby("customer_region")
    .agg(
        nps_medio=("nps_score", "mean"),
        pct_atraso=("teve_atraso", lambda x: x.mean() * 100),
        atraso_medio=("delivery_delay_days", "mean"),
    )
    .round(2)
    .reset_index()
    .sort_values("pct_atraso", ascending=False)
)

fig = make_subplots(
    rows=1,
    cols=3,
    subplot_titles=["% com Atraso", "Atraso Médio (dias)", "NPS Médio"],
)

for col_idx, col in enumerate(["pct_atraso", "atraso_medio", "nps_medio"], start=1):
    fig.add_trace(
        go.Bar(
            x=atraso_reg["customer_region"],
            y=atraso_reg[col],
            text=atraso_reg[col].round(2).astype(str),
            textposition="outside",
            marker_color="#ef4444" if col != "nps_medio" else "#0284c7",
            showlegend=False,
        ),
        row=1,
        col=col_idx,
    )

fig.update_layout(
    title="Diagnóstico Regional: Atraso e NPS por Região",
    title_x=0.5,
    height=430,
)
fig.show()

# %% [markdown]
# **O diagnóstico regional é inequívoco: o problema é sistêmico.**
#
# - % de clientes com atraso: varia de **88% a 91%** — homogêneo em todo o Brasil
# - Atraso médio: entre **2,14 e 2,22 dias** — sem diferença prática entre regiões
# - NPS médio: diferença de apenas **0,28 pontos** entre melhor e pior região
#
# Não existe uma região "problema". A logística falha de forma uniforme em todo
# o território. Isso descarta ações regionalizadas como solução — o problema
# precisa de uma resposta sistêmica e de processo.

# %% [markdown]
# ## 9. A Escada de Prazo: Cumprir o Prometido Vale Mais que Entregar Rápido
#
# O heatmap mostrou que `delivery_delay_days` (-0,60) pesa muito mais no NPS do
# que `delivery_time_days` (≈ 0,00). Para confirmar com dados diretos: clientes
# que receberam no prazo têm NPS de **6,86** — quase 3 pontos acima dos que
# sofreram atraso (NPS **4,07**).
#
# Dos 2.500 clientes da base, apenas **277 (11%)** receberam dentro do prazo prometido.

# %%
h2 = (
    df.groupby("entregou_no_prazo")["nps_score"]
    .agg(nps_medio="mean", n="count")
    .round(2)
    .reset_index()
)
h2["label"] = h2["entregou_no_prazo"].map({True: "No Prazo", False: "Atrasado"})
h2["n_label"] = h2["nps_medio"].astype(str) + "<br><sub>n=" + h2["n"].astype(str) + "</sub>"

fig = px.bar(
    h2,
    x="label",
    y="nps_medio",
    color="label",
    color_discrete_map={"No Prazo": "#0284c7", "Atrasado": "#ef4444"},
    text="n_label",
    title="NPS Médio: Entregou no Prazo vs Atrasado",
    labels={"label": "", "nps_medio": "NPS Médio"},
)
fig.update_traces(textposition="outside", textfont_size=13)
fig.update_layout(showlegend=False, title_x=0.5, height=420, yaxis_range=[0, 10])
fig.show()

# %% [markdown]
# **Implicação para o negócio:** a empresa não precisa necessariamente entregar
# mais rápido — precisa entregar **dentro do prazo que prometeu**. Um cliente que
# aguarda 10 dias dentro do prazo tem NPS próximo a 7. Um que aguarda 5 dias
# com 1 de atraso tende a avaliar abaixo de 5.
#
# Isso sugere que calibrar melhor os prazos prometidos pode ter impacto imediato
# no NPS — sem necessidade de investimento em velocidade logística.

# %% [markdown]
# ## 10. Resolução Rápida Atenua o Dano — Mas Não o Apaga
#
# Dentro do perfil mais crítico ("Atraso + SAC"), o tempo de resolução do SAC
# ainda diferencia o NPS. Isso responde a uma pergunta importante: **o dano está
# completamente feito quando o cliente aciona o SAC, ou ainda há recuperação possível?**

# %%
df_as = df[df["perfil_degradacao"] == "Atraso + SAC"].copy()
df_as["faixa_resolucao"] = pd.qcut(
    df_as["resolution_time_days"],
    q=4,
    labels=["Muito Rápido", "Rápido", "Lento", "Muito Lento"],
    duplicates="drop",
)
res = (
    df_as.groupby("faixa_resolucao", observed=True)["nps_score"]
    .agg(nps_medio="mean", n="count")
    .round(2)
    .reset_index()
)
res["label"] = res["nps_medio"].astype(str) + "<br><sub>n=" + res["n"].astype(str) + "</sub>"

fig = px.bar(
    res,
    x="faixa_resolucao",
    y="nps_medio",
    text="label",
    title='Tempo de Resolução vs NPS — apenas perfil "Atraso + SAC"',
    labels={"faixa_resolucao": "Velocidade de Resolução", "nps_medio": "NPS Médio"},
    color="nps_medio",
    color_continuous_scale=["#ef4444", "#f97316", "#0284c7"],
    color_continuous_midpoint=df_as["nps_score"].mean(),
)
fig.update_traces(textposition="outside")
fig.update_layout(title_x=0.5, height=430, yaxis_range=[0, 10], coloraxis_showscale=False)
fig.show()

# %% [markdown]
# **Resultado:** existe uma variação de **1,53 pontos** entre a resolução mais
# rápida (NPS 4,47) e a mais lenta (NPS 2,94) dentro do mesmo perfil de degradação.
#
# Isso significa que o SAC ainda tem margem para atenuar o dano — mas não para
# revertê-lo. Um cliente que sofreu atraso E esperou muito pelo SAC sai com NPS
# próximo de 3; um que foi resolvido rapidamente sai com NPS próximo de 4,5.
# Ambos são detratores. **O ponto de intervenção eficaz é antes — no atraso.**

# %% [markdown]
# ## 11. Conclusões e Recomendações
#
# ### O que os dados provam
#
# | Achado | Evidência |
# | :--- | :--- |
# | 74% dos clientes são detratores | Base pende estruturalmente para insatisfação |
# | O problema está na operação, não no perfil | Idade, região, ticket: correlação ≈ 0 com NPS |
# | Atraso na entrega é a causa raiz | `delivery_delay_days`: -0,60 — sinal mais forte |
# | O problema é sistêmico, não regional | 88–91% de atraso em todas as regiões |
# | Apenas 11% das entregas chegam no prazo | 2.223 de 2.500 clientes sofreram atraso |
# | Atraso e SAC se acumulam | 69,4% estão no pior perfil (Atraso + SAC) |
# | Comportamento confirma percepção | 0% de detratores recompram; 100% de promotores recompram |
# | Resolução rápida atenua, não reverte | 1,53 pts de amplitude dentro do pior perfil |
#
# ### Recomendações por área
#
# **Logística (prioridade 1):**
# - Reduzir a taxa de atraso é a ação de maior impacto possível no NPS
# - Calibrar os prazos prometidos: entregar dentro do prazo vale mais que entregar rápido
# - O problema é nacional — a solução precisa ser de processo, não regionalizada
#
# **Atendimento ao Cliente (prioridade 2):**
# - Investir em velocidade de resolução no primeiro contato
# - A cada quartil de lentidão, o NPS cai mais ~0,5 ponto mesmo dentro do pior perfil
# - O SAC não reverte detratores, mas pode limitar a queda para os menos engajados
#
# **Produto e CX:**
# - Transparência ativa sobre o status da entrega pode reduzir o volume de contatos
#   ao SAC — o cliente que sabe o que está acontecendo aciona menos o suporte
#
# **Analytics e Modelo Preditivo:**
# - `delivery_delay_days` e `complaints_count` são os dois features mais candidatos
#   a um modelo de classificação de risco de detração
# - Com 69,4% da base no pior perfil, o modelo precisa ser calibrado para não
#   ser trivialmente majoritário (prever "Detrator" para todos daria 74% de acurácia)

# %%
resumo_final = pd.DataFrame(
    {
        "Perfil": ordem_degradacao,
        "Clientes": [65, 489, 212, 1734],
        "% da Base": ["2,6%", "19,6%", "8,5%", "69,4%"],
        "NPS Médio": [8.23, 5.19, 6.43, 3.76],
        "% Detratores": ["13,8%", "65,2%", "43,4%", "82,5%"],
        "% Recompra 30d": ["66,2%", "11,5%", "24,1%", "3,9%"],
    }
)
resumo_final
