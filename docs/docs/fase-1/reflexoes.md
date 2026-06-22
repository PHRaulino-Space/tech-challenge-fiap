# 3. Reflexões do Desafio

*CRISP-DM: Business Understanding*

---

## Qual problema de negócio está sendo resolvido?

Hoje a empresa só enxerga o NPS depois que a jornada do cliente terminou. Isso significa que qualquer ação para reverter um detrator — desconto, contato proativo, melhoria no atendimento — só acontece depois do estrago feito. Não há espaço para prevenção.

O problema que estamos resolvendo é exatamente esse: **identificar preventivamente quais clientes têm mais chance de se tornar detratores**, a partir dos dados operacionais gerados durante a própria jornada de compra, antes que a pesquisa de NPS seja aplicada.

Com isso, a empresa passa de uma postura reativa — "o cliente avaliou mal, agora o que fazemos?" — para uma postura proativa: "esse cliente está no caminho de virar detrator, o que podemos fazer agora?"

---

## Por que o NPS é importante para um e-commerce?

O NPS mede o quanto um cliente recomendaria os serviços da empresa para outras pessoas. No e-commerce, onde a experiência do cliente é o principal diferencial competitivo, esse indicador tem peso direto em três frentes:

**Recompra:** um cliente satisfeito tem muito mais chance de voltar a comprar. Um detrator, além de não voltar, pode migrar para um concorrente.

**Boca a boca:** um promotor traz novos clientes por recomendação espontânea — sem custo de aquisição. Um detrator faz o caminho inverso e pode afastar potenciais compradores.

**Market share:** em mercados competitivos como o e-commerce, a fidelização acontece onde o cliente se sente ouvido e bem atendido. NPS baixo de forma persistente é um sinal de que a empresa está perdendo terreno para a concorrência.

---

## Quais áreas se beneficiam desses insights?

Toda a cadeia operacional se beneficia, mas algumas áreas têm impacto mais direto:

**Logística:** entender quais variáveis de entrega mais frustram o cliente permite priorizar melhorias — seja no prazo prometido, na comunicação de atrasos ou na redução de tentativas de entrega mal-sucedidas.

**Atendimento ao cliente (SAC):** saber que clientes com mais contatos no SAC tendem a ter NPS mais baixo permite agir de forma mais resolutiva no primeiro contato, reduzindo o atrito.

**Marketing:** os achados da análise podem orientar campanhas e comunicações — por exemplo, para perfis de cliente ou regiões onde a satisfação é historicamente mais baixa.

**Produto e experiência:** insights sobre o que gera e o que não gera insatisfação podem guiar melhorias na jornada de compra, na navegabilidade e na comunicação de expectativas.

---

## O que os dados confirmam até agora

A base conta com 2.500 clientes e 19 variáveis distribuídas em quatro grupos da jornada: Cliente, Pedido, Logística e Atendimento.

O primeiro dado relevante já aparece antes de qualquer análise cruzada: **a média do NPS na base é 4.38** — abaixo do ponto neutro (7), o que indica que a base pende estruturalmente para detratores. Não estamos lidando com casos isolados de insatisfação, mas com um padrão.

A análise exploratória, conduzida seguindo o fluxo cronológico da jornada do cliente, mostrou que:

- **Perfil do cliente** (idade, tempo de relacionamento, região) não tem relação relevante com o NPS. A insatisfação não discrimina quem é o cliente.
- **O momento da compra** (valor do pedido, itens, desconto, parcelas) também não move o NPS de forma individual. O problema não está na etapa da compra.
- **Logística** é onde o sinal começa a aparecer — `delivery_delay_days` apresenta correlação de -0.6 com o NPS, a mais forte observada até agora. Clientes promotores quase não têm atraso; detratores têm atraso consistente.

Isso direciona a investigação para as etapas operacionais da jornada — logística e atendimento — como os principais fatores que influenciam a satisfação.
