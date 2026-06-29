# 7. Proposta de Solução

*CRISP-DM: Modeling*

A solução proposta é um sistema de **NPS preditivo orientado a risco de detração**. O objetivo não é apenas estimar uma nota, mas identificar clientes com maior probabilidade de se tornarem detratores enquanto ainda existe tempo para intervenção operacional.

---

## Problema de Modelagem

A EDA mostrou que a base é fortemente concentrada em detratores:

| Categoria | Clientes | % da base |
|---|---:|---:|
| Detrator | 1.851 | 74,0% |
| Neutro | 448 | 17,9% |
| Promotor | 201 | 8,0% |

Por isso, a formulação recomendada é:

> **Classificar clientes em risco de detração**, priorizando a identificação correta dos detratores.

Em uma primeira versão, o problema pode ser simplificado para classificação binária:

- **Risco alto:** Detrator (`nps_score <= 6`)
- **Risco baixo/médio:** Neutro ou Promotor (`nps_score >= 7`)

Essa abordagem é mais acionável para o negócio, porque separa clientes que exigem intervenção imediata daqueles que podem seguir no fluxo normal.

---

## Features Prioritárias

A seleção inicial vem diretamente da EDA:

| Variável | Evidência | Prioridade |
|---|---|---|
| `delivery_delay_days` | Correlação -0,60 com NPS | Alta |
| `complaints_count` | Correlação -0,50 com NPS | Alta |
| `customer_service_contacts` | Correlação -0,35 com NPS | Alta |
| `resolution_time_days` | Correlação -0,19 com NPS | Média |
| `delivery_time_days` | Correlação ≈ 0 isoladamente | Baixa isolada, útil em interação com atraso |
| `customer_region` | NPS varia só 0,28 ponto entre regiões | Baixa |
| Pedido e perfil do cliente | Correlações próximas de zero | Baixa |

As variáveis derivadas `teve_atraso`, `teve_contato_sac` e `perfil_degradacao` devem ser testadas como features interpretáveis. Elas resumem bem o acúmulo de falhas da jornada:

| Perfil | NPS médio | % detratores | % recompra 30d |
|---|---:|---:|---:|
| Sem Problemas | 8,23 | 13,8% | 66,2% |
| Só Atraso | 5,19 | 65,2% | 11,5% |
| Só SAC | 6,43 | 43,4% | 24,1% |
| Atraso + SAC | 3,76 | 82,5% | 3,9% |

---

## Modelo Inicial Recomendado

Para a primeira versão, a recomendação é começar com modelos simples e explicáveis:

| Modelo | Por que usar |
|---|---|
| Regressão Logística | Baseline interpretável para Detrator vs. Não Detrator |
| Árvore de Decisão | Fácil tradução em regras operacionais |
| Random Forest | Captura interações sem perder robustez |

O baseline mínimo deve ser comparado contra a regra trivial de prever todos como detratores. Como essa regra já teria **74,0% de acurácia**, o modelo só agrega valor se melhorar a qualidade da priorização operacional, não apenas a acurácia.

---

## Métricas de Avaliação

As métricas devem refletir o custo de negócio:

| Métrica | Motivo |
|---|---|
| Recall de detratores | Reduz o risco de deixar passar clientes críticos |
| Precision de detratores | Evita acionar clientes demais sem necessidade |
| F1-score da classe detrator | Equilibra recall e precision |
| Matriz de confusão | Mostra erros operacionais de forma clara |
| PR-AUC | Mais adequada que ROC-AUC em bases desbalanceadas |

A acurácia pode ser reportada, mas não deve ser usada como métrica principal.

---

## Estratégia Operacional

A saída do modelo deve ser uma régua de ação, não apenas uma classe prevista.

| Faixa de risco | Critério sugerido | Ação |
|---|---|---|
| Alto | Atraso + SAC ou alta probabilidade de detração | Priorização pelo SAC e comunicação ativa |
| Médio | Atraso sem SAC ou SAC sem atraso | Mensagem preventiva e monitoramento |
| Baixo | Sem atraso e sem SAC | Fluxo normal |

O principal ganho de negócio está em antecipar a atuação nos clientes em risco antes que o NPS seja coletado.

---

## Recomendações de Intervenção

### Logística

- Reduzir atraso é a ação com maior potencial de impacto.
- Calibrar o prazo prometido: a EDA mostrou que cumprir o prazo pesa mais que simplesmente entregar rápido.
- Tratar o problema como sistêmico, porque a taxa de atraso é alta em todas as regiões.

### Atendimento

- Priorizar clientes com atraso e contato no SAC.
- Reduzir tempo de resolução para atenuar o dano.
- Criar playbook específico para o perfil "Atraso + SAC".

### Experiência do Cliente

- Comunicar risco de atraso antes do cliente precisar acionar o SAC.
- Testar mensagens proativas com prazo atualizado e opção de suporte.
- Medir se a transparência reduz reclamações e melhora recompra.

---

## Evolução Recomendada

1. Implementar baseline de classificação binária Detrator vs. Não Detrator.
2. Validar a importância das features contra os achados da EDA.
3. Definir limiar de risco com foco em recall de detratores.
4. Criar um painel operacional com clientes em risco alto.
5. Testar intervenções em experimento controlado antes de escalar.

A modelagem deve ser tratada como parte de um ciclo de melhoria operacional: prever o risco só gera valor se houver ação concreta antes da pesquisa de NPS.
