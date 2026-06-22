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

from plotly.subplots import make_subplots

# %% [markdown]
# ### Questão central de negócio
#
# > quais fatores operacionais realmente influenciam a satisfação do cliente e como a empresa pode agir de forma proativa para melhorar a experiência antes mesmo da aplicação da pesquisa de NPS?

# %% [markdown]
# ### Entendimento do negócio:
#
# nessa primeira etapa, queremos exercitar o seu pensamento analítico, não código. Nos traga a resposta para as seguintes perguntas de negócio:
#
# - [ ] Qual problema de negócio está sendo resolvido?
# - [ ] Por que o NPS é importante para um e-commerce?
# - [ ] Quais áreas poderiam se beneficiar desses insights? Exemplos: logística, atendimento, pricing, produto etc.

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
# ### Criando uma visão geral do dataset com a documentação das colunas dos dados

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

fig = px.bar(
    dist_nps,
    x=dist_nps.index,
    y=dist_nps.values,
    labels={"x": "Categoria NPS", "y": "Clientes"},
    title="Distribuição de Clientes por Categoria NPS",
    color=dist_nps.index,
    color_discrete_map={"Detrator": "#ef4444", "Neutro": "#f97316", "Promotor": "#0284c7"},
    text=dist_nps.values,
)
fig.update_traces(textposition="outside")
fig.update_layout(showlegend=False, title_x=0.5)
fig.show()

# %% [markdown]
# ## Metodologia: Análise Baseada na Jornada do Cliente
#
# Para que esta Análise Exploratória (EDA) reflita a realidade do negócio, estruturamos a investigação seguindo o **ciclo de vida cronológico** da experiência do cliente no e-commerce. O objetivo é isolar em qual etapa do fluxo a experiência começa a se degradar, identificando os pontos de ruptura que impactam o NPS final.
#
# A análise seguirá quatro etapas consecutivas:
#
# 1. **O Momento da Compra (Expectativa):** Análise do impacto financeiro inicial (`order_value`, `discount_value`, `payment_installments`).
# 2. **A Logística e Entrega (A Espera):** Investigação do limite de tolerância do cliente com prazos e falhas (`delivery_time_days`, `delivery_delay_days`, `delivery_attempts`).
# 3. **O Atendimento (O SOS):** Avaliação da capacidade do suporte em reverter atritos operacionais (`customer_service_contacts`, `resolution_time_days`).
# 4. **O Desfecho (Retenção):** Cruzamento da percepção final (`nps_score`) com o comportamento real de recompra de 30 dias (`repeat_purchase_30d`).
#
# > **Premissa de Negócio:** Mapear a jornada de forma cronológica nos permite transformar dados operacionais frios em uma história visual e acionável para tomada de decisão.

# %% [markdown]
# ### 📊 Análise por Grupo: Operação vs. Alvo (Satisfação)
#
# Para identificar quais fatores operacionais mais impactam o nosso alvo, dividiremos as análises cruzando cada grupo de dados diretamente com a satisfação do cliente.
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
# ### Grupo Cliente — NPS médio por Região

# %%
nps_por_regiao = (
    df.groupby("customer_region")["nps_score"].mean().reset_index().sort_values("nps_score")
)

fig = px.bar(
    nps_por_regiao,
    x="customer_region",
    y="nps_score",
    title="NPS Score Médio por Região",
    labels={"customer_region": "Região", "nps_score": "NPS Score Médio"},
    text=nps_por_regiao["nps_score"].round(2),
    color="nps_score",
    color_continuous_scale="RdBu",
)
fig.update_traces(textposition="outside")
fig.update_layout(showlegend=False, title_x=0.5, coloraxis_showscale=False)
fig.show()

# %% [markdown]
# ### Conclusão — Grupo Cliente
#
# O heatmap mostra correlações praticamente nulas: `customer_age` com -0.01 e
# `customer_tenure_months` com 0.03. O sinal é ainda mais fraco do que o grupo Pedido.
#
# O que isso confirma: **a insatisfação não discrimina perfil de cliente.** Não importa
# se o cliente é novo ou antigo, jovem ou mais velho — a chance de se tornar detrator
# é a mesma. O problema não está em quem é o cliente.
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
# *(A preencher após análise dos gráficos)*

# %% [markdown]
# ---
# ## Hipóteses para Análises Futuras
#
# A partir do que foi observado até aqui na EDA, surgem três hipóteses que merecem
# investigação mais aprofundada — seja em análises multivariadas ou na etapa de modelagem.
#
# ---
#
# ### Hipótese 1 — O valor do produto influencia a tolerância do cliente
#
# Clientes que compraram produtos mais caros têm mais tolerância a variáveis que degradam
# a experiência (como atraso na entrega ou múltiplas tentativas de entrega)?
#
# A lógica: quem investiu mais numa compra pode estar mais motivado a esperar ou
# a tolerar pequenos problemas operacionais. Ou o contrário — pode ser mais exigente
# justamente por ter pago mais.
#
# **O que analisar:** cruzar `order_value` com `delivery_delay_days` segmentado por
# `nps_categoria` — ver se o impacto do atraso no NPS é diferente em compras de alto valor.
#
# ---
#
# ### Hipótese 2 — Expectativa de prazo vs. realidade
#
# Se o cliente foi prometido 5 dias e recebeu em 8, ele provavelmente vira detrator.
# Mas se foi prometido 8 dias e recebeu em 8, ele continuaria detrator?
#
# A ideia é que o `delivery_delay_days` (dias de atraso em relação ao prometido) pode
# ser mais determinante para o NPS do que o `delivery_time_days` (tempo total de entrega).
# Um cliente que espera mais, mas recebe dentro do prazo, pode ter uma experiência melhor
# do que um cliente que espera menos mas foi surpreendido pelo atraso.
#
# **O que analisar:** comparar o peso de `delivery_delay_days` vs `delivery_time_days`
# sobre o NPS — já temos correlações distintas entre os dois no heatmap.
#
# ---
#
# ### Hipótese 3 — Frete e desconto como amortecedores da insatisfação
#
# Um frete mais baixo ou um desconto maior na compra reduz a sensibilidade do cliente
# às variáveis que degradam a experiência? Ou seja — se eu compensei o cliente no bolso,
# ele tende a tolerar mais um atraso ou um problema no atendimento?
#
# **O que analisar:** cruzar `freight_value` e `discount_value` com `delivery_delay_days`
# e `nps_categoria` — ver se clientes com frete baixo ou desconto alto que sofreram
# atraso têm NPS melhor do que clientes sem essas compensações.
