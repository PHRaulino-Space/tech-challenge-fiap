# 5. EDA Final — NPS Preditivo

*CRISP-DM: Data Understanding*

Esta análise exploratória percorre a jornada do cliente no e-commerce — compra, entrega e atendimento — para identificar onde a experiência se rompe e quais fatores operacionais estão mais associados ao baixo NPS.

O ponto mais importante da EDA é a **mudança de foco da solução**. O projeto começou com a hipótese natural de prever o NPS antes da pesquisa. A exploração mostrou que a ação de maior impacto não é apenas prever a nota final, mas prever e calibrar melhor a entrega, porque o atraso é o principal sinal associado à queda do NPS.

<section class="eda-hero">
  <div>
    <span class="eda-kicker">Tech Challenge · Fase 1</span>
    <h2>O problema de satisfação é operacional, sistêmico e aparece depois da compra.</h2>
    <p>
      A base mostra uma concentração extrema de detratores, atraso generalizado na entrega
      e forte associação entre falhas operacionais, acionamento do SAC e queda de recompra.
    </p>
  </div>
  <div class="eda-hero-metric">
    <strong>4,38</strong>
    <span>Nota média do score de NPS da Base</span>
  </div>
</section>

<div class="eda-metrics">
  <div><strong>2.500</strong><span>clientes analisados</span></div>
  <div><strong>74,0%</strong><span>detratores</span></div>
  <div><strong>89%</strong><span>com atraso</span></div>
  <div><strong>69,4%</strong><span>em Atraso + SAC</span></div>
</div>

---

## 1. Ponto de Partida: 74% dos Clientes São Detratores

Antes de qualquer cruzamento, a distribuição do NPS já comunica a urgência. A empresa não está lidando com casos isolados de insatisfação: **3 em cada 4 clientes estão na faixa de detratores**.

<div class="eda-chart-frame large">
  <iframe src="/assets/figures/eda-01-distribuicao-nps.html" title="Distribuição de clientes por categoria NPS"></iframe>
</div>

| Categoria | Clientes | % da Base |
| :--- | :---: | :---: |
| **Detrator** (0–6) | 1.851 | **74,0%** |
| Neutro (7–8) | 448 | 17,9% |
| Promotor (9–10) | 201 | 8,0% |

**Leitura de negócio:** com nota média do score de NPS de **4,38**, abaixo do ponto neutro, a satisfação negativa é o padrão dominante da operação.

---

## 2. Onde Está o Problema?

As correlações mostram que os sinais mais fortes não estão no perfil do cliente nem no momento da compra. Eles aparecem na **execução pós-compra**: atraso, reclamações, contatos com o SAC e tempo de resolução.

<div class="eda-chart-frame tall">
  <iframe src="/assets/figures/eda-02-correlacoes.html" title="Correlação das variáveis operacionais com NPS"></iframe>
</div>

| Variável | Correlação com NPS | Grupo |
| :--- | :---: | :--- |
| `delivery_delay_days` | **-0,60** | Logística |
| `complaints_count` | **-0,50** | Atendimento |
| `customer_service_contacts` | -0,35 | Atendimento |
| `resolution_time_days` | -0,19 | Atendimento |
| Demais variáveis | ≈ 0 | Pedido / Cliente |

**Conclusão:** idade, região, ticket, desconto, parcelas e quantidade de itens não aparecem como fatores relevantes nesta EDA. O problema está concentrado na experiência operacional depois que o pedido é confirmado.

Essa conclusão reduz o espaço de solução. Um modelo genérico de NPS baseado em perfil de cliente ou pedido teria pouca tração; a solução precisa olhar para a promessa logística.

---

## 3. Jornada do Cliente: O Que Cada Grupo Explica

A análise por grupo confirma o diagnóstico inicial. Cliente e pedido praticamente não se movem com o NPS. Logística e atendimento concentram os sinais de degradação.

<div class="eda-chart-frame xlarge">
  <iframe src="/assets/figures/eda-03-heatmaps-grupos.html" title="Heatmaps de correlação por grupo da jornada" scrolling="no"></iframe>
</div>

| Grupo | Sinal com o NPS | Principal variável |
| :--- | :--- | :--- |
| **Cliente** | Nenhum | — |
| **Pedido** | Nenhum | — |
| **Logística** | **Forte** | `delivery_delay_days` (-0,60) |
| **Atendimento** | Moderado | `complaints_count` (-0,50) |

### Interpretação por etapa

**Cliente:** `customer_age` e `customer_tenure_months` têm correlação praticamente nula. A região varia apenas **0,28 pontos** de NPS entre a melhor e a pior média regional.

**Pedido:** `order_value`, `items_quantity`, `discount_value` e `payment_installments` ficam próximos de zero. O momento da compra, isoladamente, não explica a insatisfação.

**Logística:** `delivery_delay_days` é o maior sinal da análise. A distinção é importante: `delivery_time_days` é praticamente zero, então o cliente parece reagir mais ao **descumprimento do prazo prometido** do que ao tempo total de entrega.

**Atendimento:** reclamações e contatos com o SAC estão associados a menor NPS. A base não permite afirmar causalidade, mas mostra que a necessidade de suporte acompanha experiências piores.

---

## 4. Perfis de Degradação da Experiência

Para transformar variáveis em leitura de negócio, foram criados quatro perfis a partir de duas flags:

- `teve_atraso`: cliente recebeu fora do prazo prometido.
- `teve_contato_sac`: cliente precisou acionar o atendimento.

<div class="eda-chart-grid">
  <div class="eda-chart-frame">
    <iframe src="/assets/figures/eda-04-perfis-degradacao.html" title="Nota média do score de NPS por perfil de degradação"></iframe>
  </div>
  <div class="eda-chart-frame">
    <iframe src="/assets/figures/eda-05-nps-por-perfil.html" title="Distribuição de NPS por perfil de degradação"></iframe>
  </div>
</div>

| Perfil | Clientes | % da Base | Nota Média do Score NPS | % Detratores |
| :--- | :---: | :---: | :---: | :---: |
| **Sem Problemas** | 65 | 2,6% | **8,23** | 13,8% |
| **Só Atraso** | 489 | 19,6% | 5,19 | 65,2% |
| **Só SAC** | 212 | 8,5% | 6,43 | 43,4% |
| **Atraso + SAC** | 1.734 | **69,4%** | **3,76** | 82,5% |

**Dois achados críticos:**

1. Apenas **65 clientes (2,6%)** tiveram uma jornada sem atraso e sem SAC.
2. **69,4%** da base está no pior perfil: atraso combinado com contato ao SAC.

---

## 5. De Onde Vêm os Detratores?

Quando olhamos apenas os **1.851 detratores**, a concentração no pior perfil fica ainda mais clara.

<div class="eda-chart-frame large">
  <iframe src="/assets/figures/eda-06-origem-detratores.html" title="Origem dos detratores por perfil operacional"></iframe>
</div>

| Perfil | Detratores | % dos Detratores |
| :--- | :---: | :---: |
| **Atraso + SAC** | 1.431 | **77,3%** |
| Só Atraso | 319 | 17,2% |
| Só SAC | 92 | 5,0% |
| Sem Problemas | 9 | 0,5% |

**Leitura:** 99,5% dos detratores tiveram ao menos um problema operacional identificável. O baixo NPS está fortemente associado a falhas concretas da jornada.

---

## 6. Percepção e Comportamento: Recompra em 30 Dias

O NPS deixa de ser apenas percepção quando comparado com recompra. Nesta base, a relação é extrema: **nenhum detrator recompra em 30 dias** e **todos os promotores recompram**.

<div class="eda-chart-frame large">
  <iframe src="/assets/figures/eda-07-recompra.html" title="Recompra em 30 dias por NPS e perfil de degradação"></iframe>
</div>

| Segmento | % Recompra em 30 dias |
| :--- | :---: |
| Detratores | **0,0%** |
| Neutros | 3,8% |
| Promotores | **100,0%** |
| Sem Problemas | 66,2% |
| Só SAC | 24,1% |
| Só Atraso | 11,5% |
| Atraso + SAC | 3,9% |

**Conclusão:** a insatisfação medida pelo NPS se traduz em comportamento real. Para esta base, NPS é um indicador diretamente conectado à retenção de curto prazo.

---

## 7. Diagnóstico Regional: O Problema É Sistêmico

A região não explica o problema. A taxa de atraso é alta e parecida em todo o Brasil, e a diferença de NPS entre a melhor e a pior região é pequena.

<div class="eda-chart-frame large">
  <iframe src="/assets/figures/eda-08-regional.html" title="Diagnóstico regional de atraso e NPS"></iframe>
</div>

| Região | % com Atraso | Atraso Médio (dias) | Nota Média do Score NPS |
| :--- | :---: | :---: | :---: |
| Sudeste | 91,0% | 2,22 | 4,37 |
| Nordeste | 90,0% | 2,19 | 4,42 |
| Centro-Oeste | 88,0% | 2,22 | 4,21 |
| Norte | 88,0% | 2,14 | 4,38 |
| Sul | 88,0% | 2,17 | 4,49 |

**Conclusão:** não há uma região-problema. A operação falha de forma uniforme; portanto, a resposta precisa ser sistêmica e de processo.

---

## 8. Prazo Prometido vs. Velocidade

O tempo total de entrega quase não se associa ao NPS. O que pesa é receber fora do prazo prometido.

<div class="eda-chart-frame large">
  <iframe src="/assets/figures/eda-09-prazo.html" title="Nota média do score de NPS por cumprimento do prazo prometido"></iframe>
</div>

| Status da Entrega | Clientes | Nota Média do Score NPS |
| :--- | :---: | :---: |
| **No prazo** | 277 | **6,86** |
| **Atrasado** | 2.223 | **4,07** |

**Implicação:** a empresa não precisa necessariamente prometer entregas mais rápidas; precisa cumprir o prazo prometido. Calibrar SLAs e comunicação de prazo pode ter impacto direto na satisfação.

Esse é o ponto de virada do projeto: o alvo operacional mais útil passa a ser a previsão de prazo/atraso. O NPS permanece como métrica de resultado para medir se a promessa logística mais assertiva reduz detratores.

---

## 9. Tempo de Resolução: Atenua, Mas Não Reverte

Dentro do pior perfil, "Atraso + SAC", resolver rápido ainda melhora o NPS. Mas todos os grupos continuam dentro da faixa de detratores.

<div class="eda-chart-frame large">
  <iframe src="/assets/figures/eda-10-resolucao.html" title="Tempo de resolução no perfil Atraso mais SAC"></iframe>
</div>

| Velocidade de Resolução | Clientes | Nota Média do Score NPS |
| :--- | :---: | :---: |
| Muito Rápido | 448 | 4,47 |
| Rápido | 431 | 3,86 |
| Lento | 564 | 3,53 |
| Muito Lento | 291 | 2,94 |

A amplitude de **1,53 pontos** mostra que o SAC atenua o dano, mas não recupera completamente a experiência. O ponto de intervenção mais eficaz continua sendo **prevenir o atraso**.

---

## 10. Recomendações

### Logística — Prioridade 1

- Reduzir a taxa de atraso é a ação com maior potencial de impacto no NPS.
- Calibrar prazos prometidos: cumprir o prazo vale mais que simplesmente entregar rápido.
- Atuar como problema nacional e de processo, não como correção regional pontual.

### Atendimento ao Cliente — Prioridade 2

- Acelerar resolução no primeiro contato para limitar a queda do NPS.
- Tratar clientes no perfil "Atraso + SAC" como risco alto de detração.
- Criar rotina de priorização para casos com atraso já identificado.

### Produto e CX

- Testar transparência ativa sobre status de entrega como hipótese de intervenção.
- Comunicar risco de atraso antes do cliente precisar acionar o SAC.

### Analytics e Modelo Preditivo

- Priorizar um modelo operacional de previsão de prazo/risco de atraso.
- Usar o NPS como variável de validação do impacto, não apenas como nota a ser prevista.
- Monitorar se a melhoria no cumprimento do prazo reduz detratores, contatos no SAC e perda de recompra.

---

## Resumo Executivo

| Achado | Evidência |
| :--- | :--- |
| 74% dos clientes são detratores | Nota média do score de NPS: 4,38 |
| O problema está na operação, não no perfil | Idade, região e ticket com correlação ≈ 0 |
| Atraso é o principal fator operacional associado ao baixo NPS | `delivery_delay_days`: -0,60 |
| O problema é sistêmico, não regional | 88–91% de atraso em todas as regiões |
| Apenas 11% receberam no prazo | 277 de 2.500 clientes |
| Atraso e SAC se acumulam | 69,4% no perfil "Atraso + SAC" |
| Detratores não recompram | 0% de recompra em 30 dias |
| Resolução rápida ajuda, mas não reverte | Amplitude de 1,53 ponto no pior perfil |

> **Síntese:** a empresa não tem um problema de público, preço ou região. Tem um problema operacional de promessa não cumprida. O caminho mais direto para elevar o NPS é reduzir atrasos, comunicar melhor o risco de entrega e tratar rapidamente clientes que já entraram no fluxo de SAC.

> **Troca de chave:** prever NPS ajuda a identificar risco, mas prever melhor o prazo de entrega ajuda a evitar que o risco aconteça.
