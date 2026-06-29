# 1. Problema de Negócio

*CRISP-DM: Business Understanding*

---

## Contexto

> Com o crescimento acelerado do e-commerce nacional, temos o cenário de uma empresa que passou a lidar com um volume cada vez maior de pedidos, entregas e interações com clientes. Esse crescimento trouxe ganhos importantes de escala, mas também revelou desafios relevantes na experiência do cliente, especialmente refletidos na alta variabilidade do Net Promoter Score (NPS) entre diferentes perfis de consumidores. A área de Experiência do Cliente percebeu que, mesmo com indicadores operacionais aparentemente semelhantes, alguns clientes se tornam promotores da marca, enquanto outros se tornam detratores.
>
> Essa diferença levanta uma questão central para o negócio: **quais fatores operacionais realmente influenciam a satisfação do cliente e como a empresa pode agir de forma proativa para melhorar a experiência antes mesmo da aplicação da pesquisa de NPS?**
>
> Atualmente, o NPS é coletado apenas após o encerramento da jornada de compra, o que limita a capacidade da empresa de antecipar problemas, priorizar ações corretivas e atuar de forma preventiva. Nesse contexto, surge a necessidade de transformar dados operacionais — como informações de pedidos, logística e atendimento — em insights acionáveis, capazes de orientar decisões estratégicas e operacionais.

---

## Qual problema de negócio está sendo resolvido?

Hoje a empresa só enxerga o NPS depois que a jornada do cliente terminou. Isso significa que qualquer ação para reverter um detrator só acontece depois do estrago feito — sem espaço para prevenção.

O objetivo é identificar preventivamente quais clientes têm mais chance de se tornar detratores, a partir dos dados operacionais gerados durante a própria jornada de compra, antes que a pesquisa de NPS seja aplicada. Com isso, a empresa pode agir de forma proativa para mudar o desfecho antes que ele aconteça.

### A troca de chave revelada pela EDA

No início do projeto, a leitura natural do desafio era tratar o `nps_score` como a variável-alvo principal de um modelo preditivo: estimar a nota ou a categoria do cliente antes da pesquisa. A análise exploratória mostrou um caminho mais acionável.

O NPS baixo não se distribui aleatoriamente entre perfis de cliente, regiões ou tipos de pedido. Ele aparece fortemente associado ao **atraso na entrega** e ao **descumprimento do prazo prometido**. Portanto, a pergunta de negócio evoluiu:

| Antes da EDA | Depois da EDA |
|---|---|
| Como prever o NPS antes da pesquisa? | Como prever e calibrar melhor o prazo de entrega para evitar a queda do NPS? |
| Alvo analítico: `nps_score` | Alvo operacional: risco de atraso / prazo realista de entrega |
| Ação depois do risco de detração | Ação antes da quebra da promessa logística |

Essa mudança não abandona o NPS. O NPS passa a ser o **indicador de validação do impacto**: se a empresa melhora a previsão de prazo, reduz atrasos e comunica melhor o risco, a expectativa é observar menos detratores e maior recompra.

---

## Por que o NPS é importante para um e-commerce?

O NPS mede o quanto um cliente recomendaria os serviços da empresa para outras pessoas. Além de indicar satisfação, ele impacta diretamente o crescimento do negócio em três frentes:

**Recompra:** um cliente satisfeito tem mais chance de voltar a comprar. Um detrator, além de não voltar, pode migrar para um concorrente.

**Boca a boca:** um promotor traz novos clientes por recomendação espontânea, sem custo de aquisição. Um detrator faz o caminho inverso.

**Market share:** no e-commerce, onde a concorrência é acirrada, a fidelização acontece onde o cliente se sente ouvido e bem atendido. NPS baixo de forma persistente é um sinal de perda de terreno para a concorrência.

---

## Quais áreas poderiam se beneficiar desses insights?

Toda a cadeia operacional se beneficia, mas com impactos distintos por área:

**Logística:** entender quais variáveis de entrega mais frustram o cliente permite priorizar melhorias — seja no prazo prometido, na comunicação de atrasos ou na redução de tentativas mal-sucedidas.

**Atendimento ao cliente (SAC):** identificar que clientes com mais contatos no SAC tendem a ter NPS mais baixo permite agir de forma mais resolutiva no primeiro contato, reduzindo o atrito.

**Marketing:** os achados podem orientar campanhas e comunicações para perfis de cliente ou regiões onde a satisfação é historicamente mais baixa.

**Produto e experiência:** insights sobre o que gera insatisfação podem guiar melhorias na jornada de compra, na navegabilidade e na comunicação de expectativas com o cliente.

---

## Como o NPS impacta o negócio

- **Recompra:** clientes promotores têm maior propensão a comprar novamente e a aumentar o ticket médio ao longo do tempo
- **Boca a boca:** promotores recomendam espontaneamente, reduzindo o custo de aquisição de novos clientes
- **Market share:** em e-commerce, a experiência é o principal diferencial — clientes com boa experiência fidelizam onde se sentem ouvidos

---

## Quais indicadores de mercado poderiam complementar essa análise?

A base de dados disponível permite uma análise robusta do comportamento interno, mas alguns indicadores externos e complementares enriqueceriam as conclusões:

**Churn rate:** a taxa de cancelamento ou abandono da plataforma complementa o NPS — um cliente que vira detrator e não retorna em 30 dias pode já estar no caminho do churn. A base já conta com `repeat_purchase_30d`, que é um proxy desse comportamento.

**CAC (Custo de Aquisição de Cliente):** saber quanto custa adquirir um novo cliente ajuda a dimensionar o impacto financeiro de perder um detrator — e reforça o argumento de investir em retenção antes da perda.

**LTV (Lifetime Value):** o valor que um cliente gera ao longo do tempo permite priorizar ações — um cliente de alto LTV em risco de virar detrator merece intervenção diferente de um cliente de primeira compra.

**Benchmark de NPS do setor:** comparar o NPS médio da empresa com a média do e-commerce brasileiro dá contexto para avaliar se o problema é grave ou esperado para o setor. Com média de 4.38 na base, a posição provavelmente está abaixo do mercado.

**SLA de entrega dos concorrentes:** se o mercado entrega em 3 dias e a empresa entrega em 7, o cliente já chega com expectativa calibrada pela concorrência — o que amplifica o impacto de qualquer atraso adicional.
