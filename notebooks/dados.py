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

# %%
from collections import OrderedDict

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import plotly.io as pio

from plotly.subplots import make_subplots

pio.renderers.default = "notebook_connected"

# %% [markdown]
# # EDA — NPS Preditivo no E-commerce
#
# Este notebook registra a análise exploratória da fase 1 do Tech Challenge. A pergunta
# central é:
#
# > Quais fatores operacionais influenciam a satisfação do cliente e como a empresa pode
# > agir de forma proativa antes da aplicação da pesquisa de NPS?
#
# A investigação parte de uma hipótese simples: o NPS não é afetado apenas pelo perfil
# do cliente ou pelo valor da compra. Em um e-commerce, a satisfação tende a ser
# construída ao longo da jornada — expectativa de compra, entrega, atendimento e
# desfecho. Por isso, a análise está organizada para descobrir em qual etapa essa
# experiência começa a se deteriorar.
#
# **Nota metodológica:** para fins exploratórios, a nota individual da pergunta NPS
# (`nps_score`, escala 0–10) será usada como variável contínua nas análises de
# correlação e tendência. O NPS oficial, calculado como `% promotores - % detratores`,
# será usado apenas para classificação e leitura geral da base.

# %% [markdown]
# ## Entendimento do negócio
#
# O problema de negócio é antecipar clientes com maior risco de baixa satisfação para
# permitir ações corretivas antes que a experiência termine em uma nota ruim de NPS.
#
# Para um e-commerce, o NPS importa porque resume a disposição do cliente em recomendar
# a empresa depois de uma experiência de compra. Quando a nota cai, o impacto pode
# aparecer em recompra, reputação, custo de atendimento e priorização operacional.
#
# Áreas que podem se beneficiar diretamente:
#
# - **Logística:** priorização de pedidos com risco de atraso e revisão de rotas/prazos.
# - **Atendimento:** identificação de casos que precisam de contato preventivo.
# - **Pricing e promoções:** avaliação se descontos ou frete reduzem insatisfação.
# - **CRM/retenção:** segmentação de clientes com maior risco de churn ou baixa recompra.

# %%
## Config Pandas
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

# %% [markdown]
# ### Visão geral do dataset e documentação das colunas

# %%
# Separar variáveis quantitativas e qualitativas
cols_quant = [col for col, meta in metadados_colunas.items() if meta["tipo"] == "quantitativa"]
cols_qual = [col for col, meta in metadados_colunas.items() if meta["tipo"] == "qualitativa"]

# Calcula as estatísticas descritivas APENAS para as quantitativas
df_infos_quant = df[cols_quant].describe().T

# Adiciona metadados às quantitativas
df_infos_quant["descricao"] = df_infos_quant.index.map(
    lambda col: metadados_colunas.get(col, {}).get("descricao", "—")
)
df_infos_quant["grupo"] = df_infos_quant.index.map(
    lambda col: metadados_colunas.get(col, {}).get("grupo", "—")
)
df_infos_quant["tipo"] = df_infos_quant.index.map(
    lambda col: metadados_colunas.get(col, {}).get("tipo", "—")
)
df_infos_quant["natureza"] = df_infos_quant.index.map(
    lambda col: metadados_colunas.get(col, {}).get("natureza", "—")
)
# Adiciona a informação de linhas vazias por coluna
df_infos_quant["nulos"] = df_infos_quant.index.map(lambda col: df[col].isnull().sum())
# Adiciona o tipo de dado real da coluna
df_infos_quant["dtype"] = df_infos_quant.index.map(lambda col: df[col].dtype)
# Adiciona o count calculado para todas as variáveis (embora já esteja no describe, garantimos a coluna)
df_infos_quant["count"] = df_infos_quant.index.map(lambda col: df[col].count())
# Adiciona a ordem da jornada do cliente
df_infos_quant["ordem_jornada"] = df_infos_quant.index.map(
    lambda col: metadados_colunas.get(col, {}).get("ordem_jornada", 99)
)

cols_novas_quant = [
    "descricao",
    "grupo",
    "ordem_jornada",
    "tipo",
    "natureza",
    "dtype",
    "nulos",
    "count",
] + [
    col
    for col in df_infos_quant.columns
    if col
    not in ["descricao", "grupo", "ordem_jornada", "tipo", "natureza", "dtype", "nulos", "count"]
]
df_infos_quant = df_infos_quant[cols_novas_quant]

# Para qualitativas, mostrar os metadados, tipo de dado e count
df_infos_qual = pd.DataFrame(
    OrderedDict(
        [
            (
                col,
                {
                    "descricao": metadados_colunas[col]["descricao"],
                    "grupo": metadados_colunas[col]["grupo"],
                    "ordem_jornada": metadados_colunas[col].get("ordem_jornada", 99),
                    "tipo": metadados_colunas[col]["tipo"],
                    "natureza": metadados_colunas[col]["natureza"],
                    "dtype": df[col].dtype,
                    "nulos": df[col].isnull().sum(),
                    "count": df[col].count(),
                },
            )
            for col in cols_qual
        ]
    )
).T

cols_novas_qual = [
    "descricao",
    "grupo",
    "ordem_jornada",
    "tipo",
    "natureza",
    "dtype",
    "nulos",
    "count",
]
df_infos_qual = df_infos_qual[cols_novas_qual]

# Concatena: primeiro quantitativas, depois qualitativas (ordenadas pelo tipo)
df_infos = pd.concat([df_infos_quant, df_infos_qual], axis=0)

# Exibe resultado ordenado pela jornada do cliente
df_infos = df_infos.sort_values("ordem_jornada").fillna("—")

df_infos

# %% [markdown]
# ### Amostra por categoria de NPS
#
# Antes de qualquer análise, uma inspeção visual de 5 clientes de cada categoria
# ajuda a desenvolver intuição sobre o perfil de cada grupo.

# %%
pd.concat(
    [
        df[df["nps_categoria"] == cat].sample(5, random_state=42)
        for cat in ["Detrator", "Neutro", "Promotor"]
    ]
).reset_index(drop=True)

# %% [markdown]
# ### Distribuição do NPS
#
# Antes de qualquer análise cruzada, entender como a base está dividida entre as categorias
# é o ponto de partida — e já revela um insight importante de negócio.

# %%
dist_nps = df["nps_categoria"].value_counts().reindex(["Detrator", "Neutro", "Promotor"])
dist_nps_pct = (dist_nps / dist_nps.sum() * 100).round(1)
nps_oficial = (dist_nps_pct["Promotor"] - dist_nps_pct["Detrator"]).round(1)
labels_dist = [f"{n:,}<br><sub>{p}%</sub>" for n, p in zip(dist_nps.values, dist_nps_pct.values)]

fig = px.bar(
    dist_nps,
    x=dist_nps.index,
    y=dist_nps.values,
    labels={"x": "Categoria NPS", "y": "Clientes"},
    title="Distribuição de Clientes por Categoria NPS",
    color=dist_nps.index,
    color_discrete_map={"Detrator": "#ef4444", "Neutro": "#f97316", "Promotor": "#0284c7"},
    text=labels_dist,
)
fig.update_traces(textposition="outside", textfont_size=13)
fig.update_layout(showlegend=False, title_x=0.5)
fig.show()

# %%
pd.DataFrame(
    {
        "metric": ["% Promotores", "% Detratores", "NPS oficial"],
        "valor": [dist_nps_pct["Promotor"], dist_nps_pct["Detrator"], nps_oficial],
    }
)

# %% [markdown]
# A distribuição é fortemente desbalanceada, com predominância de detratores. Para uma
# leitura acadêmica, isso deve ser tratado como ressalva metodológica: a base pode
# representar um recorte com maior concentração de experiências problemáticas, algum
# viés de resposta ou um filtro operacional anterior. A análise segue válida como EDA,
# mas conclusões preditivas precisam considerar esse desequilíbrio.

# %% [markdown]
# ## Metodologia: análise baseada na jornada do cliente
#
# Para que a análise reflita a realidade do negócio, a investigação segue o ciclo de
# vida cronológico da experiência do cliente. O objetivo é localizar em qual etapa
# a experiência começa a se degradar e quais sinais podem ser usados em uma proposta
# preditiva.
#
# A leitura será feita em duas camadas:
#
# 1. **Análise por grupo da jornada:** cliente, pedido, logística e atendimento contra o NPS.
# 2. **Análises combinadas:** cruzamentos entre atraso, SAC, região, recompra e perfis de degradação.
#
# > **Premissa de negócio:** se o NPS é o resultado final da jornada, os sinais mais
# > úteis são aqueles que aparecem antes ou durante a degradação da experiência.

# %% [markdown]
# ### Mapa da análise por grupo: operação vs. satisfação
#
# Primeiro, cada grupo é analisado separadamente contra o `nps_score` e a categoria
# de NPS. Essa etapa funciona como filtro: variáveis com pouca relação individual
# não são descartadas definitivamente, mas perdem prioridade como explicação principal.
#
# | Grupo Analisado | Variáveis Operacionais | Alvo de Negócio |
# | :--- | :--- | :--- |
# | **1. Cliente** | `customer_age`, `customer_region`, `customer_tenure_months`... | `nps_score` / Categoria |
# | **2. Pedido** | `order_value`, `discount_value`, `payment_installments`... | `nps_score` / Categoria |
# | **3. Logística** | `delivery_time_days`, `delivery_delay_days`, `delivery_attempts`... | `nps_score` / Categoria |
# | **4. Atendimento**| `customer_service_contacts`, `resolution_time_days`... | `nps_score` / Categoria |

# %% [markdown]
# ### Grupo Cliente — Heatmap de Correlação
#
# Variáveis quantitativas do perfil do cliente cruzadas com o NPS Score.
# `customer_region` é categórica e será analisada separadamente nos boxplots.

# %%
cols_heatmap_cliente = ["customer_age", "customer_tenure_months", "nps_score"]
corr_matrix_cliente = df[cols_heatmap_cliente].corr()

fig = px.imshow(
    corr_matrix_cliente,
    title="Correlação: Variáveis do Cliente vs NPS Score",
    color_continuous_scale="RdBu_r",
    text_auto=".2f",
    zmin=-1,
    zmax=1,
    labels=dict(color="Correlação"),
)
fig.update_layout(width=500, height=450, title_x=0.5)
fig.show()

# %% [markdown]
# ### Grupo Cliente — Boxplot por categoria NPS

# %%
variaveis_cliente = {
    "customer_age": "Idade do Cliente",
    "customer_tenure_months": "Tempo de Relacionamento (meses)",
}

fig = make_subplots(rows=1, cols=2, subplot_titles=list(variaveis_cliente.values()))

for i, (col, label) in enumerate(variaveis_cliente.items()):
    for cat in categorias:
        fig.add_trace(
            go.Box(
                y=df[df["nps_categoria"] == cat][col],
                name=cat,
                marker_color=cores[cat],
                showlegend=(i == 0),
            ),
            row=1,
            col=i + 1,
        )

fig.update_layout(
    title="Grupo Cliente — Distribuição por Categoria NPS",
    title_x=0.5,
    height=450,
    boxmode="group",
)
fig.show()

# %% [markdown]
# ### Conclusão — Grupo Cliente
#
# O heatmap mostra correlações praticamente nulas: `customer_age` com -0.01 e
# `customer_tenure_months` com 0.03. O sinal é ainda mais fraco do que o grupo Pedido.
#
# A região geográfica também foi investigada — o nota média de recomendação por região variou apenas
# 0.28 pontos entre a menor (Centro-Oeste: 4.21) e a maior (Sul: 4.49). Diferença
# sem relevância prática para o negócio.
#
# O que isso confirma: **a insatisfação não discrimina perfil de cliente.** Não importa
# se o cliente é novo ou antigo, jovem ou mais velho, ou de qual região do Brasil —
# a chance de se tornar detrator é a mesma. O problema não está em quem é o cliente.
#
# Assim como no grupo Pedido, essa análise não chegou ao objetivo de identificar
# o que gera detratores — mas cumpriu um papel importante: **eliminamos com dados
# mais uma hipótese**. Perfil de cliente não é o nosso problema.
#
# A investigação segue para os grupos onde o problema provavelmente está:
# Logística e Atendimento.

# %% [markdown]
# ### Grupo Pedido — Heatmap de Correlação

# %%
cols_heatmap = [
    "payment_installments",
    "items_quantity",
    "order_value",
    "discount_value",
    "nps_score",
]
corr_matrix = df[cols_heatmap].corr()

fig = px.imshow(
    corr_matrix,
    title="Correlação: Variáveis do Pedido vs NPS Score",
    color_continuous_scale="RdBu_r",
    text_auto=".2f",
    zmin=-1,
    zmax=1,
    labels=dict(color="Correlação"),
)
fig.update_layout(
    width=700,
    height=600,
    title_x=0.5,
)
fig.show()

# %% [markdown]
# ### Grupo Pedido — Boxplot por categoria NPS
#
# Visão consolidada das 4 variáveis do grupo Pedido cruzadas com a categoria NPS.
# O heatmap já sinalizou correlações próximas de zero — os boxplots confirmam visualmente.

# %%

variaveis_pedido = {
    "order_value": "Valor do Pedido (R$)",
    "items_quantity": "Qtd. de Itens",
    "discount_value": "Valor do Desconto (R$)",
    "payment_installments": "Parcelas",
}

fig = make_subplots(rows=2, cols=2, subplot_titles=list(variaveis_pedido.values()))

for i, (col, label) in enumerate(variaveis_pedido.items()):
    row, col_pos = divmod(i, 2)
    for cat in categorias:
        fig.add_trace(
            go.Box(
                y=df[df["nps_categoria"] == cat][col],
                name=cat,
                marker_color=cores[cat],
                showlegend=(i == 0),
            ),
            row=row + 1,
            col=col_pos + 1,
        )

fig.update_layout(
    title="Grupo Pedido — Distribuição por Categoria NPS",
    title_x=0.5,
    height=600,
    boxmode="group",
)
fig.show()

# %% [markdown]
# ### Conclusão — Grupo Pedido
#
# O heatmap e os boxplots mostram a mesma coisa: nenhuma variável do grupo Pedido
# tem relação relevante com o NPS — `order_value`, `items_quantity`, `discount_value`
# e `payment_installments` todas com correlação próxima de zero.
#
# **O momento da compra não é o problema.** Não importa o quanto o cliente gastou,
# quantos itens comprou ou em quantas parcelas pagou — isso individualmente não move
# o NPS para cima nem para baixo.
#
# > ⚠️ **Ressalva:** isso não significa que essas variáveis são irrelevantes para sempre.
# > A análise aqui é individual e linear. Uma combinação — como um pedido de alto valor
# > com atraso na entrega — pode amplificar a insatisfação de forma que só aparece
# > na modelagem multivariada.
#
# Por enquanto, o que os dados confirmam é que **o problema está em outro ponto da jornada**.

# %% [markdown]
# ### Grupo Logística — Heatmap de Correlação

# %%
cols_heatmap_logistica = [
    "delivery_time_days",
    "delivery_delay_days",
    "freight_value",
    "delivery_attempts",
    "nps_score",
]
corr_matrix_logistica = df[cols_heatmap_logistica].corr()

fig = px.imshow(
    corr_matrix_logistica,
    title="Correlação: Variáveis de Logística vs NPS Score",
    color_continuous_scale="RdBu_r",
    text_auto=".2f",
    zmin=-1,
    zmax=1,
    labels=dict(color="Correlação"),
)
fig.update_layout(width=700, height=600, title_x=0.5)
fig.show()

# %% [markdown]
# ### Grupo Logística — Boxplot por categoria NPS

# %%
variaveis_logistica = {
    "delivery_time_days": "Tempo de Entrega (dias)",
    "delivery_delay_days": "Atraso na Entrega (dias)",
    "freight_value": "Valor do Frete (R$)",
    "delivery_attempts": "Tentativas de Entrega",
}

fig = make_subplots(rows=2, cols=2, subplot_titles=list(variaveis_logistica.values()))

for i, (col, label) in enumerate(variaveis_logistica.items()):
    row, col_pos = divmod(i, 2)
    for cat in categorias:
        fig.add_trace(
            go.Box(
                y=df[df["nps_categoria"] == cat][col],
                name=cat,
                marker_color=cores[cat],
                showlegend=(i == 0),
            ),
            row=row + 1,
            col=col_pos + 1,
        )

fig.update_layout(
    title="Grupo Logística — Distribuição por Categoria NPS",
    title_x=0.5,
    height=600,
    boxmode="group",
)
fig.show()

# %% [markdown]
# ### Conclusão — Grupo Logística
#
# O heatmap e os boxplots revelam o sinal mais forte observado em toda a análise:
#
# - `delivery_delay_days`: -0.60 — correlação mais alta de todo o projeto
# - `delivery_time_days`: -0.38 — sinal relevante, mas bem abaixo do atraso
# - `delivery_attempts`: -0.22 — sinal moderado
# - `freight_value`: -0.04 — praticamente nulo
#
# Nos boxplots, a separação entre categorias é visualmente clara e diferente de tudo
# que vimos nos grupos anteriores. Promotores quase não têm atraso — mediana próxima
# de zero. Detratores têm atraso consistente — mediana em torno de 2 dias, com
# outliers chegando a 7–8 dias. As caixas mal se sobrepõem.
#
# A distinção entre as duas variáveis de prazo é um achado importante de negócio:
# `delivery_delay_days` (atraso em relação ao prometido) pesa muito mais no NPS do
# que `delivery_time_days` (tempo total de entrega). Isso indica que **o cliente
# não está avaliando quanto tempo esperou — está avaliando se a empresa cumpriu
# o que prometeu**. Um cliente que espera 10 dias dentro do prazo prometido pode
# ter NPS melhor do que um que esperou 5 dias e recebeu com 1 dia de atraso.
#
# **Conclusão principal:** o atraso na entrega é o principal fator de insatisfação
# identificado na base. A relação é forte o suficiente para ser o candidato número
# um a feature no modelo preditivo — e para orientar ações imediatas de logística.

# %% [markdown]
# ### Aprofundamento — O que os dias de atraso explicam?
#
# Como `delivery_delay_days` é o sinal mais forte da jornada, a análise aprofunda duas
# perguntas:
#
# 1. O atraso se relaciona com quais outras variáveis da base?
# 2. A partir de quantos dias o atraso começa a aparecer em reclamação, SAC e queda de NPS?
#
# Essa etapa é importante para separar dois usos diferentes da variável: explicar a
# **queda da nota** e tentar explicar o **início da reclamação**.

# %%
cols_correlacao_atraso = [
    col for col in df.select_dtypes(include="number").columns if col != "delivery_delay_days"
]

corr_atraso = (
    df[["delivery_delay_days"] + cols_correlacao_atraso]
    .corr(method="pearson")["delivery_delay_days"]
    .drop("delivery_delay_days")
    .reset_index()
)
corr_atraso.columns = ["variavel", "correlacao_pearson"]
corr_atraso_spearman = (
    df[["delivery_delay_days"] + cols_correlacao_atraso]
    .corr(method="spearman")["delivery_delay_days"]
    .drop("delivery_delay_days")
    .reset_index()
)
corr_atraso_spearman.columns = ["variavel", "correlacao_spearman"]
corr_atraso = corr_atraso.merge(corr_atraso_spearman, on="variavel")
corr_atraso["grupo"] = corr_atraso["variavel"].map(
    lambda col: metadados_colunas.get(col, {}).get("grupo", "Derivada")
)
corr_atraso = corr_atraso.sort_values("correlacao_pearson")

fig = px.bar(
    corr_atraso,
    x="correlacao_pearson",
    y="variavel",
    orientation="h",
    color="grupo",
    text="correlacao_pearson",
    title="Correlação de Pearson: Dias de Atraso com Outras Variáveis",
    labels={
        "correlacao_pearson": "Correlação de Pearson com delivery_delay_days",
        "variavel": "",
        "grupo": "Grupo",
    },
)
fig.add_vline(x=0, line_width=1, line_color="#334155")
fig.update_traces(texttemplate="%{x:.2f}", textposition="outside", cliponaxis=False)
fig.update_xaxes(range=[-1, 1], zeroline=True)
fig.update_layout(height=650, title_x=0.5, margin=dict(l=180, r=80))
fig.show()

# %%
corr_atraso[["variavel", "grupo", "correlacao_pearson", "correlacao_spearman"]].sort_values(
    "correlacao_pearson"
)

# %% [markdown]
# A leitura principal se mantém quando trocamos Pearson por Spearman. Para
# `delivery_delay_days`, as duas correlações ficam próximas e negativas, o que reforça
# que a relação entre atraso e nota de recomendação não depende apenas de uma suposição
# linear forte. Isso é útil porque dias de atraso e nota NPS são variáveis discretas.

# %% [markdown]
# ### Reclamação, SAC e nota por intensidade do atraso
#
# A pergunta original era: “a partir de quantos dias de atraso o cliente começa a
# reclamar?”. Os dados mostram uma resposta menos direta: a reclamação já é alta mesmo
# com zero dias de atraso. Por isso, além de olhar reclamação, comparamos também SAC,
# nota média de recomendação e recompra.

# %%
df["teve_atraso"] = df["delivery_delay_days"] > 0
df["reclamou"] = df["complaints_count"] > 0
df["acionou_sac"] = df["customer_service_contacts"] > 0

atraso_por_dia = (
    df.groupby("delivery_delay_days")
    .agg(
        pedidos=("order_id", "count"),
        nota_media_recomendacao=("nps_score", "mean"),
        pct_reclamou=("reclamou", lambda serie: serie.mean() * 100),
        pct_acionou_sac=("acionou_sac", lambda serie: serie.mean() * 100),
        contatos_sac_medios=("customer_service_contacts", "mean"),
        reclamacoes_medias=("complaints_count", "mean"),
        recompra_30d_pct=("repeat_purchase_30d", lambda serie: serie.mean() * 100),
    )
    .round(2)
)

atraso_por_dia

# %%
faixas_atraso = [-0.1, 0, 1, 2, 3, 5, df["delivery_delay_days"].max()]
labels_faixas_atraso = ["0 dias", "1 dia", "2 dias", "3 dias", "4-5 dias", "6+ dias"]

df["faixa_atraso"] = pd.cut(
    df["delivery_delay_days"],
    bins=faixas_atraso,
    labels=labels_faixas_atraso,
    include_lowest=True,
)

atraso_por_faixa = (
    df.groupby("faixa_atraso", observed=True)
    .agg(
        pedidos=("order_id", "count"),
        nota_media_recomendacao=("nps_score", "mean"),
        pct_reclamou=("reclamou", lambda serie: serie.mean() * 100),
        pct_acionou_sac=("acionou_sac", lambda serie: serie.mean() * 100),
        contatos_sac_medios=("customer_service_contacts", "mean"),
        reclamacoes_medias=("complaints_count", "mean"),
        recompra_30d_pct=("repeat_purchase_30d", lambda serie: serie.mean() * 100),
    )
    .round(2)
)

atraso_por_faixa

# %%
metricas_atraso = atraso_por_faixa.reset_index()

fig = make_subplots(
    rows=2,
    cols=1,
    shared_xaxes=True,
    vertical_spacing=0.12,
    subplot_titles=[
        "Reclamação e acionamento do SAC por faixa de atraso",
        "Nota média de recomendação por faixa de atraso",
    ],
)

fig.add_trace(
    go.Scatter(
        x=metricas_atraso["faixa_atraso"],
        y=metricas_atraso["pct_reclamou"],
        mode="lines+markers+text",
        name="% Reclamou",
        text=metricas_atraso["pct_reclamou"].map(lambda valor: f"{valor:.1f}%"),
        textposition="top center",
        line=dict(color="#ef4444", width=3),
    ),
    row=1,
    col=1,
)
fig.add_trace(
    go.Scatter(
        x=metricas_atraso["faixa_atraso"],
        y=metricas_atraso["pct_acionou_sac"],
        mode="lines+markers+text",
        name="% Acionou SAC",
        text=metricas_atraso["pct_acionou_sac"].map(lambda valor: f"{valor:.1f}%"),
        textposition="bottom center",
        line=dict(color="#f97316", width=3),
    ),
    row=1,
    col=1,
)
fig.add_trace(
    go.Scatter(
        x=metricas_atraso["faixa_atraso"],
        y=metricas_atraso["nota_media_recomendacao"],
        mode="lines+markers+text",
        name="Nota média",
        text=metricas_atraso["nota_media_recomendacao"].map(lambda valor: f"{valor:.2f}"),
        textposition="top center",
        line=dict(color="#0284c7", width=3),
    ),
    row=2,
    col=1,
)

fig.update_yaxes(title_text="% de clientes", range=[0, 105], row=1, col=1)
fig.update_yaxes(title_text="Nota média de recomendação", range=[0, 10], row=2, col=1)
fig.update_layout(
    title="Efeito dos Dias de Atraso em Reclamação, SAC e Nota de Recomendação",
    title_x=0.5,
    height=700,
    legend=dict(orientation="h", y=1.08, x=0.5, xanchor="center"),
)
fig.show()

# %%
fig = px.box(
    df,
    x="faixa_atraso",
    y="nps_score",
    color="faixa_atraso",
    title="Distribuição da Nota de Recomendação por Faixa de Atraso",
    labels={
        "faixa_atraso": "Faixa de atraso",
        "nps_score": "Nota de recomendação (0–10)",
    },
    color_discrete_sequence=px.colors.qualitative.Set2,
)
fig.update_layout(showlegend=False, title_x=0.5, height=500, yaxis_range=[0, 10])
fig.show()

# %%
fig = px.bar(
    metricas_atraso,
    x="faixa_atraso",
    y="pedidos",
    text="pedidos",
    title="Volume de Pedidos por Faixa de Atraso",
    labels={"faixa_atraso": "Faixa de atraso", "pedidos": "Pedidos"},
    color="faixa_atraso",
    color_discrete_sequence=px.colors.qualitative.Set2,
)
fig.update_traces(textposition="outside")
fig.update_layout(showlegend=False, title_x=0.5, yaxis_title="Pedidos")
fig.show()

# %%
volume_atraso_por_dia = (
    df["delivery_delay_days"]
    .value_counts()
    .sort_index()
    .rename_axis("dias_atraso")
    .reset_index(name="clientes")
)
volume_atraso_por_dia["pct_base_total"] = (
    volume_atraso_por_dia["clientes"] / len(df) * 100
).round(1)
volume_atraso_por_dia["rotulo"] = volume_atraso_por_dia.apply(
    lambda linha: f"{linha['clientes']}<br>{linha['pct_base_total']:.1f}%", axis=1
)

fig = px.bar(
    volume_atraso_por_dia,
    x="dias_atraso",
    y="clientes",
    text="rotulo",
    title="Clientes por Dias de Atraso e Participação na Base Total",
    labels={
        "dias_atraso": "Dias de atraso",
        "clientes": "Clientes",
    },
    color="pct_base_total",
    color_continuous_scale="Blues",
)
fig.update_traces(textposition="outside")
fig.update_xaxes(dtick=1)
fig.update_layout(title_x=0.5, coloraxis_colorbar_title="% da base")
fig.show()

# %% [markdown]
# ### Leitura — atraso não inicia a reclamação, mas derruba o NPS
#
# O resultado muda a interpretação inicial. `complaints_count` não é uma boa variável
# para descobrir quando a reclamação começa, porque mesmo pedidos sem atraso já têm
# alta presença de reclamações. Isso sugere que parte das reclamações pode vir de
# outros problemas da experiência ou da própria construção da base.
#
# O padrão mais consistente está no NPS: conforme os dias de atraso aumentam, a nota
# média cai de forma progressiva. Assim, o atraso parece explicar melhor a **severidade
# da insatisfação** do que o início da reclamação.
#
# Para uma solução preditiva, isso muda o foco: em vez de tentar prever apenas se o
# cliente vai reclamar, a empresa deveria prever risco e severidade de atraso. Pedidos
# com risco de atraso acima de 1 dia já merecem ação preventiva; estimativas acima de
# 3 dias devem ser tratadas como casos críticos de experiência.

# %% [markdown]
# ### Grupo Atendimento — Heatmap de Correlação

# %%
cols_heatmap_atendimento = [
    "customer_service_contacts",
    "resolution_time_days",
    "complaints_count",
    "nps_score",
]
corr_matrix_atendimento = df[cols_heatmap_atendimento].corr()

fig = px.imshow(
    corr_matrix_atendimento,
    title="Correlação: Variáveis de Atendimento vs NPS Score",
    color_continuous_scale="RdBu_r",
    text_auto=".2f",
    zmin=-1,
    zmax=1,
    labels=dict(color="Correlação"),
)
fig.update_layout(width=600, height=500, title_x=0.5)
fig.show()

# %% [markdown]
# ### Grupo Atendimento — Boxplot por categoria NPS

# %%
variaveis_atendimento = {
    "customer_service_contacts": "Contatos com o SAC",
    "resolution_time_days": "Tempo de Resolução (dias)",
    "complaints_count": "Reclamações Formais",
}

fig = make_subplots(rows=1, cols=3, subplot_titles=list(variaveis_atendimento.values()))

for i, (col, label) in enumerate(variaveis_atendimento.items()):
    for cat in categorias:
        fig.add_trace(
            go.Box(
                y=df[df["nps_categoria"] == cat][col],
                name=cat,
                marker_color=cores[cat],
                showlegend=(i == 0),
            ),
            row=1,
            col=i + 1,
        )

fig.update_layout(
    title="Grupo Atendimento — Distribuição por Categoria NPS",
    title_x=0.5,
    height=450,
    boxmode="group",
)
fig.show()

# %% [markdown]
# ### Conclusão — Grupo Atendimento
#
# O heatmap e os boxplots mostram que as três variáveis do grupo têm relação com o NPS,
# cada uma com intensidade diferente:
#
# - `complaints_count`: -0.50 — o sinal mais forte do grupo
# - `customer_service_contacts`: -0.35 — sinal relevante
# - `resolution_time_days`: -0.19 — sinal mais fraco, mas presente
#
# Nos boxplots, as caixas dos Detratores estão consistentemente mais altas que as dos
# Promotores nas três variáveis — comportamento diferente de tudo que vimos nos grupos
# Cliente e Pedido.
#
# Uma leitura importante: `resolution_time_days` tem o menor sinal, o que sugere que
# **quanto demora para resolver importa menos do que o fato de precisar acionar o suporte**.
# O simples ato de contatar o SAC ou registrar uma reclamação já está associado a um
# NPS mais baixo — independente do tempo de resolução.
#
# > ⚠️ **Limitação:** a base não permite afirmar a direção da causalidade. O cliente pode
# > ter reclamado porque já era detrator, ou pode ter virado detrator porque o atendimento
# > não resolveu. Ambos os cenários aparecem da mesma forma nos dados. Nesta análise,
# > o NPS é tratado como o desfecho final da jornada.
#
# <hr>
#
# ## Encerramento da Análise Individual
#
# A primeira camada da análise — cada grupo da jornada cruzado com o NPS — mostra uma
# hierarquia clara de importância:
#
# | Grupo | Sinal com o NPS | Principal variável |
# | :--- | :--- | :--- |
# | Cliente | Nenhum | — |
# | Pedido | Nenhum | — |
# | Logística | Forte | `delivery_delay_days` (-0.60) |
# | Atendimento | Moderado | `complaints_count` (-0.50) |
#
# **O que os dados confirmam:** o problema não está em quem é o cliente nem no que ele
# comprou. O ponto de ruptura está na execução operacional, principalmente no atraso
# da entrega. Reclamações e contatos com o SAC aparecem como sinais fortes, mas devem
# ser interpretados com cuidado: eles podem ser consequência da experiência ruim, não
# necessariamente a causa inicial.
#
# A próxima etapa complementa essa visão com **análises multivariadas**, cruzando variáveis
# de grupos diferentes para entender cenários combinados: atraso com SAC, ticket alto,
# desconto, frete, região, recompra e tempo de relacionamento.

# %% [markdown]
# <hr>
# ## Análise Multivariada — Perfis de Degradação da Experiência
#
# A análise individual mostrou que `delivery_delay_days` e `customer_service_contacts`
# são os dois sinais mais fortes da base. A próxima pergunta natural é:
# **o que acontece quando esses dois problemas se combinam?**
#
# Para isso, criamos duas flags binárias:
#
# - `teve_atraso`: o cliente recebeu fora do prazo prometido? (`delivery_delay_days > 0`)
# - `teve_contato_sac`: o cliente precisou acionar o SAC? (`customer_service_contacts > 0`)
#
# A combinação das duas gera **quatro perfis de degradação da experiência** —
# do melhor para o pior cenário:
#
# | Perfil | Atraso | SAC |
# | :--- | :---: | :---: |
# | Sem Problemas | ✗ | ✗ |
# | Só Atraso | ✓ | ✗ |
# | Só SAC | ✗ | ✓ |
# | Atraso + SAC | ✓ | ✓ |

# %%
ordem_degradacao = ["Sem Problemas", "Só Atraso", "Só SAC", "Atraso + SAC"]

df["teve_atraso"] = df["delivery_delay_days"] > 0
df["teve_contato_sac"] = df["customer_service_contacts"] > 0

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

# %%
nota_media_recomendacao = (
    df.groupby("perfil_degradacao", observed=True)["nps_score"].mean().reset_index()
)
contagem = df["perfil_degradacao"].value_counts().reindex(ordem_degradacao)

cores_degradacao = {
    "Sem Problemas": "#0284c7",
    "Só Atraso": "#f97316",
    "Só SAC": "#f97316",
    "Atraso + SAC": "#ef4444",
}

fig = px.bar(
    nota_media_recomendacao,
    x="perfil_degradacao",
    y="nps_score",
    color="perfil_degradacao",
    color_discrete_map=cores_degradacao,
    text=nota_media_recomendacao["nps_score"].round(2),
    title="Nota média de recomendação por Perfil de Degradação da Experiência",
    labels={"perfil_degradacao": "Perfil", "nps_score": "Nota média de recomendação"},
    category_orders={"perfil_degradacao": ordem_degradacao},
)
fig.update_traces(textposition="outside")
fig.update_layout(showlegend=False, title_x=0.5, height=420, yaxis_range=[0, 10])
fig.show()

# %% [markdown]
# ### Distribuição das categorias NPS por perfil de degradação

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
    xaxis_title="Perfil",
    height=450,
    legend_title="Categoria NPS",
)
fig.show()

# %% [markdown]
# ### Conclusão — Perfis de Degradação
#
# Os dois gráficos confirmam e quantificam o que a análise individual já sinalizava:
#
# - **Sem Problemas:** nota média de recomendação mais alto e maior proporção de Promotores —
#   base de referência para o que a operação entrega quando funciona bem
# - **Só Atraso / Só SAC:** queda relevante no nota média de recomendação, com proporção de
#   Detratores já majoritária — cada problema isolado já degrada a experiência
# - **Atraso + SAC:** queda mais acentuada — a combinação dos dois problemas
#   concentra a maior proporção de Detratores da base
#
# O achado central é que **os dois problemas se acumulam** — não é um ou outro,
# é uma escalada de degradação. Clientes que enfrentam atraso E precisam acionar
# o SAC têm a pior experiência da base. Isso sugere que o SAC, na maioria dos casos,
# é acionado como consequência do atraso — e não resolve o problema de origem.
#
# > **Implicação para o negócio:** reduzir o atraso na entrega provavelmente
# > reduz também o volume de contatos no SAC. O problema não são dois — é um,
# > com efeito em cascata.

# %% [markdown]
# ### Zoom nos Detratores — De onde vêm?
#
# Com os perfis criados, podemos responder uma pergunta mais cirúrgica:
# **entre os clientes que já viraram detratores, qual foi a origem do problema?**
#
# Essa visão é relevante para priorização operacional — não basta saber que atraso
# e SAC degradam a experiência; precisamos saber qual combinação concentra o maior
# volume de detratores na base.

# %%
df_detratores = df[df["nps_categoria"] == "Detrator"]

dist_det = (
    df_detratores["perfil_degradacao"]
    .value_counts()
    .reindex(ordem_degradacao)
    .fillna(0)
    .astype(int)
    .reset_index()
)
dist_det.columns = ["perfil_degradacao", "detratores"]
dist_det["pct"] = (dist_det["detratores"] / dist_det["detratores"].sum() * 100).round(1)
dist_det["label"] = dist_det["detratores"].astype(str) + " (" + dist_det["pct"].astype(str) + "%)"

fig = px.bar(
    dist_det,
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
fig.update_layout(showlegend=False, title_x=0.5, height=420)
fig.show()

# %% [markdown]
# <hr>
# ## Interação: Perfil de Degradação × Tempo de Relacionamento
#
# A análise individual mostrou que `customer_tenure_months` não tem efeito direto
# sobre o NPS. Mas isso não significa que tenure seja irrelevante — pode ser que
# ele **modere o efeito do atraso e do SAC**.
#
# A pergunta é: um cliente novo que sofre atraso reage da mesma forma que um cliente
# antigo? Se as linhas divergirem conforme a degradação aumenta, a resposta é não —
# e esse é um insight acionável de retenção.
#
# Faixas de tenure criadas:
# - **< 6 meses** — cliente recente, ainda formando percepção da marca
# - **6–24 meses** — cliente em consolidação
# - **24+ meses** — cliente estabelecido, com histórico de relacionamento

# %%
bins_tenure = [-1, 6, 24, df["customer_tenure_months"].max()]
labels_tenure = ["< 6 meses", "6–24 meses", "24+ meses"]
cores_tenure = {"< 6 meses": "#7c3aed", "6–24 meses": "#0891b2", "24+ meses": "#059669"}

df["faixa_tenure"] = pd.cut(df["customer_tenure_months"], bins=bins_tenure, labels=labels_tenure)

interacao = (
    df.groupby(["perfil_degradacao", "faixa_tenure"], observed=True)["nps_score"]
    .mean()
    .round(2)
    .reset_index()
)

fig = px.line(
    interacao,
    x="perfil_degradacao",
    y="nps_score",
    color="faixa_tenure",
    color_discrete_map=cores_tenure,
    markers=True,
    title="Interação: Perfil de Degradação × Tempo de Relacionamento",
    labels={
        "perfil_degradacao": "Perfil de Degradação",
        "nps_score": "Nota média de recomendação",
        "faixa_tenure": "Tempo de Relacionamento",
    },
    category_orders={"perfil_degradacao": ordem_degradacao},
)
fig.update_traces(line_width=2.5, marker_size=9)
fig.update_layout(title_x=0.5, height=450, yaxis_range=[0, 10])
fig.show()

# %% [markdown]
# ### Como interpretar
#
# - **Linhas paralelas** → tenure não modera o efeito; clientes novos e antigos reagem
#   igual ao atraso e ao SAC
# - **Linhas que divergem da esquerda para a direita** → a degradação penaliza mais
#   um grupo específico; o ângulo de queda revela quem perdoa menos
# - **Linhas que cruzam** → o efeito inverte dependendo do perfil — por exemplo,
#   clientes antigos são mais tolerantes sem problema, mas mais críticos quando há atraso

# %%
# Tabela de suporte: nota média de recomendação e contagem por célula
interacao_tabela = (
    df.groupby(["perfil_degradacao", "faixa_tenure"], observed=True)["nps_score"]
    .agg(nota_media_recomendacao="mean", n="count")
    .round(2)
    .reset_index()
)
interacao_tabela

# %% [markdown]
# <hr>
# ## Hipótese 1 — Ticket alto protege contra o atraso?
#
# O valor do pedido não tem correlação direta com o NPS, mas pode moderar o efeito
# do atraso. Clientes que investiram mais numa compra perdoam mais — ou exigem mais?
#
# Dividimos `order_value` em tercis para comparar como o NPS cai com o atraso
# em cada faixa de ticket.

# %%
df["faixa_ticket"] = pd.qcut(
    df["order_value"],
    q=3,
    labels=["Ticket Baixo", "Ticket Médio", "Ticket Alto"],
)

h1 = (
    df.groupby(["faixa_ticket", "teve_atraso"], observed=True)["nps_score"]
    .mean()
    .round(2)
    .reset_index()
)
h1["teve_atraso"] = h1["teve_atraso"].map({True: "Com Atraso", False: "Sem Atraso"})

fig = px.line(
    h1,
    x="faixa_ticket",
    y="nps_score",
    color="teve_atraso",
    color_discrete_map={"Com Atraso": "#ef4444", "Sem Atraso": "#0284c7"},
    markers=True,
    text="nps_score",
    title="H1 — Nota média de recomendação por Faixa de Ticket × Atraso na Entrega",
    labels={
        "faixa_ticket": "Faixa de Ticket",
        "nps_score": "Nota média de recomendação",
        "teve_atraso": "",
    },
)
fig.update_traces(line_width=2.5, marker_size=10, textposition="top center")
fig.update_layout(title_x=0.5, height=430, yaxis_range=[0, 10])
fig.show()

# %% [markdown]
# **Como ler:** se as linhas convergirem em tickets mais altos — a distância entre
# "Com Atraso" e "Sem Atraso" encolhe — clientes de alto valor são mais tolerantes.
# Se divergirem, são mais exigentes. Se forem paralelas, o ticket não modera o efeito.

# %% [markdown]
# <hr>
# ## Hipótese 2 — Quebra de prazo importa mais que tempo total de entrega?
#
# O heatmap já mostrou que `delivery_delay_days` (-0.60) pesa muito mais no NPS
# do que `delivery_time_days` (-0.38). A hipótese é que o cliente avalia se a empresa
# cumpriu o que prometeu — não quanto tempo ele esperou.
#
# Para testar isso, criamos uma visão de expectativa:
#
# - pedidos sem atraso: `total_dias_entrega = delivery_time_days`
# - pedidos com atraso: `total_dias_entrega = dias_previstos_entrega + delivery_delay_days`
# - `flag_atraso = 1` quando `delivery_delay_days > 0`
#
# A comparação fica mais justa porque olhamos clientes com o mesmo total de dias, mas
# experiências diferentes: uma entrega que já estava prometida para 7 dias versus uma
# entrega prometida para 5 dias e entregue com 2 dias de atraso.

# %%
df["flag_atraso"] = (df["delivery_delay_days"] > 0).astype(int)
df["status_prazo"] = df["flag_atraso"].map({0: "Sem atraso", 1: "Com atraso"})
df["dias_previstos_entrega"] = df["delivery_time_days"]
df["total_dias_entrega"] = df["dias_previstos_entrega"] + df["delivery_delay_days"].where(
    df["flag_atraso"].eq(1),
    0,
)

h2 = (
    df.groupby(["total_dias_entrega", "status_prazo"], observed=True)
    .agg(
        pedidos=("order_id", "count"),
        nps_medio=("nps_score", "mean"),
        atraso_medio_dias=("delivery_delay_days", "mean"),
        pct_promotor=("nps_score", lambda serie: (serie >= 9).mean() * 100),
        pct_detrator=("nps_score", lambda serie: (serie <= 6).mean() * 100),
    )
    .round(2)
    .reset_index()
)

# Mantém dias com volume mínimo para evitar leitura guiada por grupos muito pequenos.
h2_plot = h2[h2["pedidos"] >= 5].copy()

fig = px.line(
    h2_plot,
    x="total_dias_entrega",
    y="nps_medio",
    color="status_prazo",
    color_discrete_map={"Sem atraso": "#0284c7", "Com atraso": "#ef4444"},
    markers=True,
    text="nps_medio",
    custom_data=["pedidos", "atraso_medio_dias", "pct_promotor", "pct_detrator"],
    title="H2 — Mesmo total de dias, NPS diferente quando há quebra de expectativa",
    labels={
        "total_dias_entrega": "Total de dias até a entrega",
        "nps_medio": "Nota média de recomendação",
        "status_prazo": "",
    },
)
fig.update_traces(
    line_width=2.5,
    marker_size=10,
    textposition="top center",
    hovertemplate=(
        "Total de dias: %{x}<br>"
        "Nota média: %{y:.2f}<br>"
        "Pedidos: %{customdata[0]}<br>"
        "Atraso médio: %{customdata[1]:.1f} dias<br>"
        "% promotores: %{customdata[2]:.1f}%<br>"
        "% detratores: %{customdata[3]:.1f}%<extra></extra>"
    ),
)
fig.update_xaxes(dtick=1)
fig.update_layout(title_x=0.5, height=480, yaxis_range=[0, 10])
fig.show()

# %%
h2_comparacao = h2_plot.pivot(
    index="total_dias_entrega",
    columns="status_prazo",
    values=["pedidos", "nps_medio", "atraso_medio_dias", "pct_promotor", "pct_detrator"],
)
h2_comparacao.columns = [
    f"{metrica}_{status.lower().replace(' ', '_')}" for metrica, status in h2_comparacao.columns
]
h2_comparacao = h2_comparacao.dropna().reset_index()
h2_comparacao["gap_nps_sem_vs_com_atraso"] = (
    h2_comparacao["nps_medio_sem_atraso"] - h2_comparacao["nps_medio_com_atraso"]
).round(2)
h2_comparacao.sort_values("total_dias_entrega")

# %% [markdown]
# **Como ler:** se, no mesmo total de dias, a linha "Sem atraso" ficar acima da linha
# "Com atraso", o problema não é apenas esperar mais. É a quebra de expectativa.
#
# Exemplo observado na base: no total de 7 dias, pedidos sem atraso ficam com nota média
# de recomendação próxima de promotor/neutro, enquanto pedidos que chegaram a 7 dias
# por causa de atraso ficam concentrados em detratores. Isso confirma que **cumprir
# o prazo prometido importa mais do que entregar rápido em termos absolutos**.

# %% [markdown]
# <hr>
# ## Hipótese 3 — Frete baixo e desconto amortecem a insatisfação?
#
# Quando o cliente já sofreu atraso, um frete mais barato ou um desconto maior
# ameniza o impacto no NPS? Testamos isso filtrando apenas os clientes com atraso
# e cruzando faixa de frete × presença de desconto.

# %%
frete_mediana = df["freight_value"].median()
desconto_mediana = df["discount_value"].median()
df["frete_baixo"] = df["freight_value"] <= frete_mediana
df["desconto_alto"] = df["discount_value"] > desconto_mediana

ordem_h3 = [
    "Frete Baixo\nDesconto Baixo",
    "Frete Baixo\nDesconto Alto",
    "Frete Alto\nDesconto Baixo",
    "Frete Alto\nDesconto Alto",
]

df_atr = df[df["teve_atraso"]].copy()
df_atr["perfil_financeiro"] = df_atr.apply(
    lambda r: (
        ("Frete Baixo" if r["frete_baixo"] else "Frete Alto")
        + "\n"
        + ("Desconto Alto" if r["desconto_alto"] else "Desconto Baixo")
    ),
    axis=1,
)

h3 = (
    df_atr.groupby("perfil_financeiro")["nps_score"]
    .agg(nota_media_recomendacao="mean", n="count")
    .round(2)
    .reindex(ordem_h3)
    .reset_index()
)
h3["label"] = h3["nota_media_recomendacao"].astype(str) + "\n(n=" + h3["n"].astype(str) + ")"

fig = px.bar(
    h3,
    x="perfil_financeiro",
    y="nota_media_recomendacao",
    text="label",
    title="H3 — Nota média de recomendação entre Clientes com Atraso: Frete × Desconto",
    labels={"perfil_financeiro": "", "nota_media_recomendacao": "Nota média de recomendação"},
    color="nota_media_recomendacao",
    color_continuous_scale=["#ef4444", "#f97316", "#0284c7"],
    color_continuous_midpoint=df_atr["nps_score"].mean(),
)
fig.update_traces(textposition="outside")
fig.update_layout(
    title_x=0.5,
    height=430,
    yaxis_range=[0, 10],
    coloraxis_showscale=False,
)
fig.show()

# %% [markdown]
# **Como ler:** se clientes com frete baixo ou com desconto tiverem NPS
# consistentemente maior dentro do grupo de atrasados, frete e desconto funcionam
# como amortecedores. Se os valores forem parecidos entre os grupos, a compensação
# financeira não é suficiente para recuperar a satisfação perdida pelo atraso.

# %% [markdown]
# <hr>
# ## Percepção vs. Comportamento — Recompra e CSAT por Perfil de Degradação
#
# Até aqui medimos **percepção** (NPS). Agora checamos se o **comportamento real**
# (recompra em 30 dias) e o **indicador interno** (CSAT) contam a mesma história.
#
# A pergunta central: um cliente do perfil "Atraso + SAC" ainda volta a comprar?
# Se sim, isso revela algo importante — dependência do produto, falta de alternativa,
# ou uma operação ruim que não derruba a preferência pela marca.

# %%
recompra = (
    df.groupby("perfil_degradacao", observed=True)["repeat_purchase_30d"]
    .mean()
    .mul(100)
    .round(1)
    .reset_index()
)
recompra.columns = ["perfil_degradacao", "pct_recompra"]
recompra["label"] = recompra["pct_recompra"].astype(str) + "%"

fig = px.bar(
    recompra,
    x="perfil_degradacao",
    y="pct_recompra",
    color="perfil_degradacao",
    color_discrete_map=cores_degradacao,
    text="label",
    title="% de Recompra em 30 dias por Perfil de Degradação",
    labels={"perfil_degradacao": "Perfil", "pct_recompra": "% Recompra"},
    category_orders={"perfil_degradacao": ordem_degradacao},
)
fig.update_traces(textposition="outside")
fig.update_layout(showlegend=False, title_x=0.5, height=420, yaxis_range=[0, 100])
fig.show()

# %%
recompra_nps = (
    df.groupby("nps_categoria", observed=True)["repeat_purchase_30d"]
    .mean()
    .mul(100)
    .round(1)
    .reindex(categorias)
    .reset_index()
)
recompra_nps.columns = ["nps_categoria", "pct_recompra"]
recompra_nps["label"] = recompra_nps["pct_recompra"].astype(str) + "%"

fig = px.bar(
    recompra_nps,
    x="nps_categoria",
    y="pct_recompra",
    color="nps_categoria",
    color_discrete_map=cores,
    text="label",
    title="% de Recompra em 30 dias por Categoria NPS",
    labels={"nps_categoria": "Categoria NPS", "pct_recompra": "% Recompra"},
    category_orders={"nps_categoria": categorias},
)
fig.update_traces(textposition="outside")
fig.update_layout(showlegend=False, title_x=0.5, height=420, yaxis_range=[0, 100])
fig.show()

# %% [markdown]
# ### NPS vs CSAT interno — os dois indicadores concordam?

# %%
comparacao = (
    df.groupby("perfil_degradacao", observed=True)
    .agg(nota_media_recomendacao=("nps_score", "mean"), csat_medio=("csat_internal_score", "mean"))
    .round(2)
    .reset_index()
)

fig = make_subplots(
    rows=1,
    cols=2,
    subplot_titles=["Nota média de recomendação", "CSAT Interno Médio"],
    shared_yaxes=False,
)

for col_idx, (col, title) in enumerate(
    [
        ("nota_media_recomendacao", "Nota média de recomendação"),
        ("csat_medio", "CSAT Interno Médio"),
    ],
    start=1,
):
    for _, row in comparacao.iterrows():
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
    title="Percepção do Cliente: NPS vs CSAT por Perfil de Degradação",
    title_x=0.5,
    height=450,
    barmode="group",
)
fig.update_xaxes(categoryorder="array", categoryarray=ordem_degradacao)
fig.show()

# %% [markdown]
# ### Conclusão — Percepção vs. Comportamento
#
# Esta análise fecha o ciclo da EDA cruzando o que o cliente **diz** (NPS e CSAT)
# com o que ele **faz** (recompra).
#
# Três leituras possíveis para o perfil "Atraso + SAC":
#
# - **Recompra cai junto com o NPS** → experiência ruim afasta o cliente de forma
#   consistente — percepção e comportamento estão alinhados
# - **Recompra se mantém mesmo com NPS baixo** → o cliente está insatisfeito mas
#   continua comprando; pode indicar dependência do produto, falta de concorrência
#   ou que a barreira de troca ainda é alta — insight relevante para a estratégia
#   de retenção
# - **NPS e CSAT divergem** → o indicador interno não está capturando a insatisfação
#   real do cliente; risco de tomada de decisão com dados enganosos

# %% [markdown]
# <hr>
# ## Região vs. Perfil de Degradação — O problema logístico é regional?
#
# A análise individual mostrou que `customer_region` não tem efeito direto sobre o NPS
# — variação de apenas 0.28 pontos entre regiões. Mas essa leitura pode estar escondendo
# um mecanismo indireto: **certas regiões podem concentrar mais atrasos**, e são esses
# atrasos que derrubam o NPS, não a região em si.
#
# Se Norte e Nordeste, por exemplo, tiverem proporcionalmente mais clientes no perfil
# "Atraso + SAC" do que Sul e Sudeste, o problema é **logístico-regional** — acionável
# para o time de operações com rotas e SLAs específicos por geografia.

# %%
dist_regional = (
    df.groupby(["customer_region", "perfil_degradacao"], observed=True)
    .size()
    .unstack(fill_value=0)
    .reindex(columns=ordem_degradacao)
)
dist_regional_pct = dist_regional.div(dist_regional.sum(axis=1), axis=0).mul(100).round(1)

fig = go.Figure()
cores_deg_lista = [cores_degradacao[p] for p in ordem_degradacao]
for perfil, cor in zip(ordem_degradacao, cores_deg_lista):
    fig.add_trace(
        go.Bar(
            name=perfil,
            x=dist_regional_pct.index.tolist(),
            y=dist_regional_pct[perfil].tolist(),
            marker_color=cor,
            text=(dist_regional_pct[perfil].astype(str) + "%").tolist(),
            textposition="inside",
        )
    )

fig.update_layout(
    barmode="stack",
    title="Distribuição de Perfis de Degradação por Região",
    title_x=0.5,
    yaxis_title="% de Clientes",
    xaxis_title="Região",
    height=450,
    legend_title="Perfil",
)
fig.show()

# %% [markdown]
# ### Severidade do atraso por região

# %%
atraso_regional = (
    df.groupby("customer_region")
    .agg(
        pct_com_atraso=("teve_atraso", lambda x: x.mean() * 100),
        atraso_medio_dias=("delivery_delay_days", "mean"),
        nota_media_recomendacao=("nps_score", "mean"),
    )
    .round(2)
    .reset_index()
    .sort_values("pct_com_atraso", ascending=False)
)

fig = make_subplots(
    rows=1,
    cols=2,
    subplot_titles=["% de Clientes com Atraso", "Atraso Médio (dias)"],
)

for col_idx, col in enumerate(["pct_com_atraso", "atraso_medio_dias"], start=1):
    fig.add_trace(
        go.Bar(
            x=atraso_regional["customer_region"],
            y=atraso_regional[col],
            text=atraso_regional[col].astype(str),
            textposition="outside",
            marker_color="#ef4444",
            showlegend=False,
        ),
        row=1,
        col=col_idx,
    )

fig.update_layout(title="Severidade do Atraso por Região", title_x=0.5, height=420)
fig.show()

# %%
atraso_regional

# %% [markdown]
# ### Conclusão — Diagnóstico Regional
#
# Esta análise separa dois mecanismos que a leitura direta de NPS por região mistura:
#
# - **Se regiões com NPS mais baixo também concentram mais perfis "Atraso + SAC":**
#   o problema não é regional no sentido demográfico — é logístico. O time de
#   operações pode agir com SLAs diferenciados, rotas prioritárias ou comunicação
#   proativa de prazo para as regiões mais expostas ao atraso
#
# - **Se a distribuição de perfis for homogênea entre regiões:** a logística falha
#   igualmente em todo o Brasil, e o foco deve ser sistêmico — não regionalizado
#
# Em ambos os casos, o achado é acionável: ou prioriza-se uma região, ou
# confirma-se que o problema é de processo e não de geografia.

# %% [markdown]
# <hr>
# ## Verificação de Mediação — Atraso causa contato com o SAC?
#
# A conclusão dos perfis de degradação afirmou que "o SAC, na maioria dos casos,
# é acionado como consequência do atraso". Antes de virar narrativa final,
# vale checar com números: clientes que sofreram atraso têm proporção
# significativamente maior de contato com o SAC do que os que não sofreram?
#
# Se sim, a hipótese de cascata se confirma. Se não, a frase precisa ser suavizada.

# %%
mediacao = (
    df.groupby("teve_atraso")
    .agg(
        pct_contatou_sac=("customer_service_contacts", lambda x: (x > 0).mean() * 100),
        media_contatos=("customer_service_contacts", "mean"),
        pct_reclamou=("complaints_count", lambda x: (x > 0).mean() * 100),
        media_reclamacoes=("complaints_count", "mean"),
        n=("nps_score", "count"),
    )
    .round(2)
    .reset_index()
)
mediacao["teve_atraso"] = mediacao["teve_atraso"].map({True: "Com Atraso", False: "Sem Atraso"})

fig = make_subplots(
    rows=1,
    cols=2,
    subplot_titles=["% que Contatou o SAC", "% que Registrou Reclamação"],
)

for col_idx, col in enumerate(["pct_contatou_sac", "pct_reclamou"], start=1):
    fig.add_trace(
        go.Bar(
            x=mediacao["teve_atraso"],
            y=mediacao[col],
            text=(mediacao[col].astype(str) + "%"),
            textposition="outside",
            marker_color=["#0284c7", "#ef4444"],
            showlegend=False,
        ),
        row=1,
        col=col_idx,
    )

fig.update_layout(
    title="Mediação: Clientes com Atraso Acionam Mais o SAC?",
    title_x=0.5,
    height=420,
    yaxis_range=[0, 100],
    yaxis2_range=[0, 100],
)
fig.show()

# %%
sac_por_nps = (
    df.groupby(["nps_categoria", "teve_atraso"], observed=True)
    .agg(
        pct_contatou_sac=("customer_service_contacts", lambda x: (x > 0).mean() * 100),
        pct_reclamou=("complaints_count", lambda x: (x > 0).mean() * 100),
    )
    .round(1)
    .reset_index()
)
sac_por_nps["teve_atraso"] = sac_por_nps["teve_atraso"].map(
    {True: "Com Atraso", False: "Sem Atraso"}
)
sac_por_nps["grupo"] = (
    sac_por_nps["nps_categoria"].astype(str) + " / " + sac_por_nps["teve_atraso"]
)

ordem_grupos_sac = [f"{cat} / {atr}" for cat in categorias for atr in ["Sem Atraso", "Com Atraso"]]
cores_grupos_sac = {f"{cat} / Sem Atraso": cores[cat] for cat in categorias} | {
    f"{cat} / Com Atraso": cores[cat] for cat in categorias
}

fig = make_subplots(
    rows=1,
    cols=2,
    subplot_titles=["% que Contatou o SAC", "% que Registrou Reclamação"],
)

for col_idx, col in enumerate(["pct_contatou_sac", "pct_reclamou"], start=1):
    for atraso, pattern in [("Sem Atraso", ""), ("Com Atraso", "/")]:
        subset = sac_por_nps[sac_por_nps["teve_atraso"] == atraso]
        fig.add_trace(
            go.Bar(
                name=atraso,
                x=subset["nps_categoria"],
                y=subset[col],
                text=(subset[col].astype(str) + "%"),
                textposition="outside",
                marker_color=[cores[c] for c in subset["nps_categoria"]],
                marker_pattern_shape=pattern,
                showlegend=(col_idx == 1),
            ),
            row=1,
            col=col_idx,
        )

fig.update_layout(
    barmode="group",
    title="Contato com SAC e Reclamações por Categoria NPS × Atraso",
    title_x=0.5,
    height=450,
    yaxis_range=[0, 100],
    yaxis2_range=[0, 100],
    legend_title="",
)
fig.show()

# %%
mediacao

# %% [markdown]
# **Interpretação:** se a diferença entre "Com Atraso" e "Sem Atraso" for grande
# (ex: 60% vs 20% de contato ao SAC), a afirmação de cascata está sustentada pelos
# dados. Se a diferença for pequena, o contato ao SAC tem causas independentes do
# atraso e a narrativa precisa ser ajustada.

# %% [markdown]
# <hr>
# ## Tentativas de Entrega — Modo de Falha Independente?
#
# `delivery_attempts` é o único indicador logístico que não foi cruzado dentro
# do perfil de degradação. A pergunta é: existem clientes com múltiplas tentativas
# de entrega **mas sem atraso**? Se sim, isso é um terceiro tipo de problema
# operacional — distinto do atraso em prazo.
#
# - **Atraso** → problema de transportadora, rota ou capacidade
# - **Múltiplas tentativas sem atraso** → problema de cadastro, endereço ou
#   comunicação com o cliente; a encomenda chega no prazo mas não encontra o destinatário
#
# A causa raiz e a ação corretiva são completamente diferentes.

# %%
limiar_tentativas = df["delivery_attempts"].median()

df["muitas_tentativas"] = df["delivery_attempts"] > limiar_tentativas

ordem_quadrantes = [
    "Sem Atraso\nPoucas Tentativas",
    "Sem Atraso\nMuitas Tentativas",
    "Com Atraso\nPoucas Tentativas",
    "Com Atraso\nMuitas Tentativas",
]

df["quadrante_entrega"] = df.apply(
    lambda r: (
        ("Com Atraso" if r["teve_atraso"] else "Sem Atraso")
        + "\n"
        + ("Muitas Tentativas" if r["muitas_tentativas"] else "Poucas Tentativas")
    ),
    axis=1,
)

quadrantes = (
    df.groupby("quadrante_entrega")["nps_score"]
    .agg(nota_media_recomendacao="mean", n="count")
    .round(2)
    .reindex(ordem_quadrantes)
    .reset_index()
)
quadrantes["label"] = (
    quadrantes["nota_media_recomendacao"].astype(str) + "\n(n=" + quadrantes["n"].astype(str) + ")"
)

cores_quadrantes = {
    "Sem Atraso\nPoucas Tentativas": "#0284c7",
    "Sem Atraso\nMuitas Tentativas": "#f97316",
    "Com Atraso\nPoucas Tentativas": "#f97316",
    "Com Atraso\nMuitas Tentativas": "#ef4444",
}

fig = px.bar(
    quadrantes,
    x="quadrante_entrega",
    y="nota_media_recomendacao",
    color="quadrante_entrega",
    color_discrete_map=cores_quadrantes,
    text="label",
    title="Tentativas de Entrega × Atraso — NPS por Quadrante",
    labels={"quadrante_entrega": "", "nota_media_recomendacao": "Nota média de recomendação"},
    category_orders={"quadrante_entrega": ordem_quadrantes},
)
fig.update_traces(textposition="outside")
fig.update_layout(showlegend=False, title_x=0.5, height=440, yaxis_range=[0, 10])
fig.show()

# %% [markdown]
# **Interpretação:** o quadrante crítico é "Sem Atraso + Muitas Tentativas".
# Se esse grupo tiver NPS relevantemente baixo e n significativo, confirma-se
# que múltiplas tentativas de entrega são um modo de falha **independente** do atraso —
# com causa raiz diferente (cadastro/comunicação) e ação corretiva diferente
# (melhoria no processo de confirmação de endereço e aviso ao cliente antes da entrega).

# %% [markdown]
# <hr>
# ## Tempo de Resolução dentro do Perfil "Atraso + SAC"
#
# `resolution_time_days` foi o sinal mais fraco do grupo Atendimento (-0.19).
# Mas a pergunta mais precisa é: **dentro do grupo que já está no pior cenário**
# (atraso + acionou o SAC), o tempo de resolução ainda diferencia o NPS?
#
# Se sim → resolver rápido ainda salva parte da experiência mesmo no pior caso
# Se não → o dano já está feito antes de qualquer resolução; a prioridade é
# prevenir o atraso, não acelerar o SAC

# %%
df_atraso_sac = df[df["perfil_degradacao"] == "Atraso + SAC"].copy()

df_atraso_sac["faixa_resolucao"] = pd.qcut(
    df_atraso_sac["resolution_time_days"],
    q=4,
    labels=["Muito Rápido", "Rápido", "Lento", "Muito Lento"],
    duplicates="drop",
)

resolucao = (
    df_atraso_sac.groupby("faixa_resolucao", observed=True)["nps_score"]
    .agg(nota_media_recomendacao="mean", n="count")
    .round(2)
    .reset_index()
)
resolucao["label"] = (
    resolucao["nota_media_recomendacao"].astype(str) + "\n(n=" + resolucao["n"].astype(str) + ")"
)

fig = px.bar(
    resolucao,
    x="faixa_resolucao",
    y="nota_media_recomendacao",
    text="label",
    title='Tempo de Resolução vs NPS — apenas perfil "Atraso + SAC"',
    labels={
        "faixa_resolucao": "Velocidade de Resolução",
        "nota_media_recomendacao": "Nota média de recomendação",
    },
    color="nota_media_recomendacao",
    color_continuous_scale=["#ef4444", "#f97316", "#0284c7"],
    color_continuous_midpoint=df_atraso_sac["nps_score"].mean(),
)
fig.update_traces(textposition="outside")
fig.update_layout(
    title_x=0.5,
    height=430,
    yaxis_range=[0, 10],
    coloraxis_showscale=False,
)
fig.show()

# %% [markdown]
# **Interpretação:** se as barras forem aproximadamente planas — sem diferença
# relevante entre "Muito Rápido" e "Muito Lento" — o NPS já estava comprometido
# antes do atendimento, e o tempo de resolução não recupera a experiência.
# Isso fecha com elegância a hipótese de cascata: **o ponto de intervenção eficaz
# é o atraso, não a velocidade do SAC**.

# %% [markdown]
# <hr>
# ## Síntese final da EDA
#
# A história que emerge dos dados é consistente:
#
# 1. **Perfil do cliente e características do pedido não explicam a queda do NPS.**
#    Idade, região, tempo de relacionamento, valor do pedido, desconto e parcelamento
#    não mostram relação individual relevante com a satisfação.
#
# 2. **A logística é o principal ponto de ruptura da jornada.**
#    `delivery_delay_days` é a variável mais associada à queda do NPS. O cliente parece
#    reagir mais ao descumprimento do prazo prometido do que ao tempo total de espera.
#
# 3. **O atraso não explica bem o início da reclamação, mas explica a severidade da
#    insatisfação.** A base mostra reclamações altas mesmo com zero dias de atraso.
#    Ainda assim, a nota média de NPS cai progressivamente conforme os dias de atraso
#    aumentam.
#
# 4. **SAC e reclamações funcionam como sinais de degradação da experiência.**
#    Quando atraso e SAC aparecem juntos, o NPS se deteriora de forma mais intensa.
#    Porém, acelerar a resolução depois do pior cenário parece menos promissor do que
#    prevenir o atraso.
#
# **Implicação para a solução preditiva:** o caminho mais acionável não é prever apenas
# a nota de NPS no final, mas antecipar o risco e a severidade do atraso. Pedidos com
# risco de atraso devem acionar intervenção logística e comunicação proativa antes que
# a experiência vire detratora.

# %% [markdown]
# <hr>
# ## Distribuições condicionadas — atraso e reclamações
#
# Como fechamento da análise, vale olhar os dois recortes de forma direta:
#
# - entre clientes que tiveram atraso, quantas reclamações foram registradas?
# - entre clientes que reclamaram, quantos dias de atraso ocorreram?
#
# Essa leitura ajuda a separar volume de ocorrência de severidade operacional.

# %%
clientes_com_atraso = df[df["teve_atraso"]].copy()

reclamacoes_clientes_atrasados = (
    clientes_com_atraso["complaints_count"]
    .value_counts()
    .sort_index()
    .rename_axis("reclamacoes")
    .reset_index(name="clientes")
)
reclamacoes_clientes_atrasados["pct_clientes_atrasados"] = (
    reclamacoes_clientes_atrasados["clientes"] / len(clientes_com_atraso) * 100
).round(1)
reclamacoes_clientes_atrasados["rotulo"] = reclamacoes_clientes_atrasados.apply(
    lambda row: f"{row['clientes']:,}<br><sub>{row['pct_clientes_atrasados']}%</sub>",
    axis=1,
)

fig = px.bar(
    reclamacoes_clientes_atrasados,
    x="reclamacoes",
    y="clientes",
    text="rotulo",
    title="Reclamações entre Clientes que Tiveram Atraso",
    labels={
        "reclamacoes": "Quantidade de reclamações",
        "clientes": "Clientes com atraso",
    },
    color="pct_clientes_atrasados",
    color_continuous_scale=["#0284c7", "#f97316", "#ef4444"],
)
fig.update_traces(textposition="outside")
fig.update_layout(title_x=0.5, height=430, coloraxis_showscale=False)
fig.show()

# %%
cruzamento_atraso_reclamacao = (
    df.assign(
        status_atraso=df["teve_atraso"].map({True: "Com atraso", False: "Sem atraso"}),
        status_reclamacao=df["reclamou"].map({True: "Com reclamação", False: "Sem reclamação"}),
    )
    .groupby(["status_atraso", "status_reclamacao"])
    .size()
    .reset_index(name="clientes")
)
cruzamento_atraso_reclamacao["pct_base"] = (
    cruzamento_atraso_reclamacao["clientes"] / len(df) * 100
).round(1)
cruzamento_atraso_reclamacao["rotulo"] = cruzamento_atraso_reclamacao.apply(
    lambda row: f"{row['clientes']:,}<br><sub>{row['pct_base']}% da base</sub>",
    axis=1,
)

fig = px.bar(
    cruzamento_atraso_reclamacao,
    x="status_atraso",
    y="clientes",
    color="status_reclamacao",
    text="rotulo",
    title="Cruzamento entre Atraso e Reclamação",
    labels={
        "status_atraso": "",
        "clientes": "Clientes",
        "status_reclamacao": "",
    },
    category_orders={
        "status_atraso": ["Sem atraso", "Com atraso"],
        "status_reclamacao": ["Sem reclamação", "Com reclamação"],
    },
    color_discrete_map={
        "Sem reclamação": "#0284c7",
        "Com reclamação": "#ef4444",
    },
)
fig.update_traces(textposition="inside")
fig.update_layout(
    barmode="stack",
    title_x=0.5,
    height=430,
    legend_title="",
)
fig.show()

# %%
resumo_atraso_reclamacao = pd.DataFrame(
    {
        "pergunta": [
            "Clientes com atraso que abriram reclamação",
            "Clientes com reclamação que também tiveram atraso",
        ],
        "percentual": [
            df.loc[df["teve_atraso"], "reclamou"].mean() * 100,
            df.loc[df["reclamou"], "teve_atraso"].mean() * 100,
        ],
        "clientes": [
            df[df["teve_atraso"] & df["reclamou"]].shape[0],
            df[df["reclamou"] & df["teve_atraso"]].shape[0],
        ],
        "base_comparacao": [
            df["teve_atraso"].sum(),
            df["reclamou"].sum(),
        ],
    }
).round({"percentual": 1})

fig = px.bar(
    resumo_atraso_reclamacao,
    x="pergunta",
    y="percentual",
    text=resumo_atraso_reclamacao.apply(
        lambda row: (
            f"{row['percentual']}%<br><sub>{row['clientes']:,}/{row['base_comparacao']:,}</sub>"
        ),
        axis=1,
    ),
    title="Atraso e Reclamação: Relações Condicionais",
    labels={"pergunta": "", "percentual": "% dos clientes"},
    color="pergunta",
    color_discrete_sequence=["#f97316", "#ef4444"],
)
fig.update_traces(textposition="outside")
fig.update_layout(title_x=0.5, height=430, showlegend=False, yaxis_range=[0, 100])
fig.show()

# %%
clientes_com_reclamacao = df[df["reclamou"]].copy()

atrasos_clientes_reclamaram = (
    clientes_com_reclamacao["delivery_delay_days"]
    .value_counts()
    .sort_index()
    .rename_axis("dias_atraso")
    .reset_index(name="clientes")
)
atrasos_clientes_reclamaram["pct_clientes_com_reclamacao"] = (
    atrasos_clientes_reclamaram["clientes"] / len(clientes_com_reclamacao) * 100
).round(1)
atrasos_clientes_reclamaram["rotulo"] = atrasos_clientes_reclamaram.apply(
    lambda row: f"{row['clientes']:,}<br><sub>{row['pct_clientes_com_reclamacao']}%</sub>",
    axis=1,
)

fig = px.bar(
    atrasos_clientes_reclamaram,
    x="dias_atraso",
    y="clientes",
    text="rotulo",
    title="Atrasos entre Clientes que Registraram Reclamações",
    labels={
        "dias_atraso": "Dias de atraso",
        "clientes": "Clientes com reclamação",
    },
    color="pct_clientes_com_reclamacao",
    color_continuous_scale=["#0284c7", "#f97316", "#ef4444"],
)
fig.update_traces(textposition="outside")
fig.update_layout(title_x=0.5, height=430, coloraxis_showscale=False)
fig.show()

# %%
df["faixa_contatos_sac"] = (
    df["customer_service_contacts"]
    .clip(upper=4)
    .map(
        {
            0: "0 contatos",
            1: "1 contato",
            2: "2 contatos",
            3: "3 contatos",
            4: "4+",
        }
    )
)

ordem_contatos_sac = ["0 contatos", "1 contato", "2 contatos", "3 contatos", "4+"]

fig = px.box(
    df,
    x="faixa_contatos_sac",
    y="delivery_delay_days",
    color="faixa_contatos_sac",
    category_orders={"faixa_contatos_sac": ordem_contatos_sac},
    title="Dias de Atraso por Quantidade de Contatos no SAC",
    labels={
        "faixa_contatos_sac": "Quantidade de contatos no SAC",
        "delivery_delay_days": "Dias de atraso",
    },
    color_discrete_sequence=["#0284c7", "#38bdf8", "#f97316", "#fb7185", "#ef4444"],
    points="outliers",
)
fig.update_layout(title_x=0.5, height=460, showlegend=False)
fig.show()

# %%
heatmap_atraso_sac = (
    df.groupby(["delivery_delay_days", "faixa_contatos_sac"], observed=True)
    .size()
    .reset_index(name="clientes")
    .pivot(index="delivery_delay_days", columns="faixa_contatos_sac", values="clientes")
    .reindex(columns=ordem_contatos_sac)
    .fillna(0)
    .astype(int)
)

fig = px.imshow(
    heatmap_atraso_sac,
    text_auto=True,
    aspect="auto",
    title="Clientes por Dias de Atraso e Quantidade de Contatos no SAC",
    labels={
        "x": "Quantidade de contatos no SAC",
        "y": "Dias de atraso",
        "color": "Clientes",
    },
    color_continuous_scale=["#f8fafc", "#38bdf8", "#f97316", "#ef4444"],
)
fig.update_layout(title_x=0.5, height=520)
fig.update_xaxes(side="top")
fig.show()
