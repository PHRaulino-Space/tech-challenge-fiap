# Tech Challenge Fase 1 — Case NPS Preditivo

Tech Challenge é o projeto que englobará os conhecimentos obtidos em todas as disciplinas da fase. Esta é uma atividade que, em princípio, deve ser desenvolvida em grupo. É importante atentar-se ao prazo de entrega, pois trata-se de uma atividade obrigatória, uma vez que sua pontuação se refere a 90% da nota final.

> **Nota sobre a solução adotada:** o enunciado original propõe refletir sobre um modelo capaz de prever o NPS antes da pesquisa. A EDA desenvolvida neste projeto mostrou que a ação mais útil para o negócio é anterior à nota: prever melhor o prazo de entrega e o risco de atraso. Por isso, a documentação mantém o NPS como desfecho de satisfação, mas apresenta a previsão de entrega como solução operacional principal.

Com o crescimento acelerado do e-commerce nacional, temos o cenário de uma empresa que passou a lidar com um volume cada vez maior de pedidos, entregas e interações com clientes. Esse crescimento trouxe ganhos importantes de escala, mas também revelou desafios relevantes na experiência do cliente, especialmente refletidos na alta variabilidade do Net Promoter Score (NPS) entre diferentes perfis de consumidores. A área de Experiência do Cliente percebeu que, mesmo com indicadores operacionais aparentemente semelhantes, alguns clientes se tornam promotores da marca, enquanto outros se tornam detratores.

Essa diferença levanta uma questão central para o negócio: **quais fatores operacionais realmente influenciam a satisfação do cliente e como a empresa pode agir de forma proativa para melhorar a experiência antes mesmo da aplicação da pesquisa de NPS?**

Atualmente, o NPS é coletado apenas após o encerramento da jornada de compra, o que limita a capacidade da empresa de antecipar problemas, priorizar ações corretivas e atuar de forma preventiva. Nesse contexto, surge a necessidade de transformar dados operacionais, como informações de pedidos, logística e atendimento, em insights acionáveis, capazes de orientar decisões estratégicas e operacionais.

É nesse cenário que você, como cientista de dados, é acionado(a). Seu papel não é apenas analisar dados ou construir modelos, mas traduzir informações técnicas em recomendações claras para o negócio, apoiando áreas como logística, atendimento, produto e estratégia na melhoria contínua da experiência do cliente.

Ao longo deste desafio, você deverá explorar os dados disponíveis, compreender o comportamento dos clientes, identificar padrões relevantes e comunicar suas conclusões de forma estruturada e acessível. Mais do que buscar a "melhor métrica" ou o "modelo mais complexo", o foco está em entendimento do problema, pensamento analítico e storytelling com dados, simulando um cenário real de atuação no mercado.

Você deverá atender os seguintes requisitos nesse desafio:

## Requisitos

### 1. Entendimento do Negócio

Ness**pensamena primeira etapa, queremos exercitar o seu to analítico**, não código. Nos traga a resposta para as seguintes perguntas de negócio:

- Qual problema de negócio está sendo resolvido?
- Por que o NPS é importante para um e-commerce?
- Quais áreas poderiam se beneficiar desses insights? Exemplos: logística, atendimento, pricing, produto etc.

Além do entendimento do negócio, inclua uma reflexão (não precisa de dados externos obrigatórios):

Como o NPS impacta:

- Recompra;
- Boca a boca;
- Market share em e-commerce.

Quais indicadores de mercado poderiam complementar essa análise? Exemplos: benchmarks de NPS, SLA logístico, concorrência.

### 2. Definição da Target

Qual é o alvo desse problema de negócio? Nessa segunda etapa queremos uma avaliação de **entendimento conceitual**, não técnico.

- Qual variável representa a satisfação do cliente?
- Por que ela foi escolhida?
- Em que momento da jornada essa informação é coletada?
- Existe algum risco de usar essa variável de forma inadequada?

### 3. Análise Exploratória dos Dados (EDA)

Realize uma análise exploratória com foco em **negócio**, não só estatística. Responda:

- Quais fatores parecem mais críticos para a satisfação?
- O que mais gera detratores?
- Existe algum "ponto de ruptura" na experiência do cliente?
- Que tipo de cliente tende a ter NPS mais alto ou mais baixo?

Imagine que você está explicando isso para **um(a) gerente de operações que não entende estatística.**

### 4. Reflexão sobre Modelo Preditivo *(opcional)*

Como forma de preparação para as próximas fases do curso, este desafio propõe uma reflexão prática sobre **como a Ciência de Dados pode ser utilizada para antecipar a satisfação do cliente**.

A partir da dor de negócio apresentada neste case, reflita sobre como um **modelo preditivo** poderia apoiar a empresa a prever o NPS antes da aplicação da pesquisa. Considere diferentes abordagens possíveis, como:

- Um **modelo de regressão**, para estimar a nota de NPS em uma escala contínua;
- Um **modelo de classificação**, para categorizar clientes, por exemplo, em satisfeitos e insatisfeitos.

Descreva qual estratégia você adotaria para resolver esse problema utilizando dados e Inteligência Artificial, justificando suas escolhas do ponto de vista técnico e **de negócio**.

Caso opte por implementar a solução, apresente uma proposta de modelo aplicada em **Python**, explicando de forma clara:

- A definição da variável alvo;
- A seleção e preparação das variáveis de entrada;
- A lógica de separação dos dados (quando aplicável);
- A escolha do modelo;
- A forma de avaliação dos resultados;
- E como essa solução poderia ser utilizada na prática pela empresa.

> **Este desafio (4) é opcional e tem como objetivo ampliar a maturidade analítica e técnica, sem impacto negativo para quem optar por não realizá-lo.**

## Base de Dados

Acesse o arquivo CSV com dados históricos de pedidos, entregas e interações com o atendimento ao cliente.

Exemplos de informações disponíveis:

- Dados do pedido (valor, quantidade de itens, forma de pagamento);
- Dados logísticos (tempo de entrega, atraso, tentativas);
- Dados de atendimento (contatos, tempo de resolução);
- Indicadores internos de negócio.

### Dicionário de Dados

| Variável | Descrição |
|---|---|
| `customer_id` | Identificador único do cliente |
| `order_id` | Identificador único do pedido |
| `customer_age` | Idade do cliente |
| `customer_region` | Região geográfica do cliente |
| `customer_tenure_months` | Tempo de relacionamento do cliente com a empresa (em meses) |
| `order_value` | Valor total do pedido |
| `items_quantity` | Quantidade de itens no pedido |
| `discount_value` | Valor de desconto aplicado ao pedido |
| `payment_installments` | Número de parcelas do pagamento |
| `delivery_time_days` | Tempo total de entrega (em dias) |
| `delivery_delay_days` | Quantidade de dias de atraso na entrega |
| `freight_value` | Valor do frete |
| `delivery_attempts` | Número de tentativas de entrega |
| `customer_service_contacts` | Número de contatos do cliente com o atendimento |
| `resolution_time_days` | Tempo para resolução de problemas (em dias) |
| `complaints_count` | Número de reclamações registradas pelo cliente |
| `repeat_purchase_30d` | Indica se houve recompra em até 30 dias após o pedido (0 = não, 1 = sim) |
| `csat_internal_score` | Score interno de satisfação do cliente |
| `nps_score` | Nota de satisfação do cliente (NPS), variando de 0 a 10, coletada após a experiência de compra |

## Formato da Entrega

### Repositório no GitHub

Enviar o link de um repositório público contendo:

- Todo o tratamento e preparação da base de dados;
- Análise exploratória (EDA);
- Modelo preditivo e toda a pipeline da construção, caso opte em fazer o desafio.

**Boas práticas obrigatórias:**

- Código organizado em notebooks e/ou scripts;
- Uso de nomes de variáveis claros e padronizados;
- Comentários explicando trechos relevantes do código;
- Estrutura de pastas clara (ex.: `data/`, `notebooks/`, `models/`, `reports/`);
- README explicando:
    - Objetivo do projeto;
    - Descrição da base de dados;
    - Metodologia utilizada;
    - Como reproduzir os resultados.

O repositório deve permitir que qualquer pessoa consiga entender e reproduzir a análise.

### Material de Apresentação do Storytelling Gerencial

Elabore um material de apresentação em formato de **slides**, direcionado a um **público não técnico** (gestores, líderes de negócio ou stakeholders). O objetivo não é explicar códigos ou modelos matemáticos, mas **contar a história dos dados** e apoiar a tomada de decisão.

A apresentação deve responder, de forma clara e visual, aos seguintes pontos:

- **Contexto do problema de negócio** — Explique brevemente o cenário do e-commerce, o desafio relacionado à satisfação dos clientes e por que esse problema é relevante para a empresa.
- **Pergunta que a análise busca responder** — Descreva qual foi a principal pergunta orientadora do trabalho. (Caso tenha optado pelo desafio do modelo preditivo, apresente também a pergunta que o modelo busca responder.)
- **Principais insights da análise exploratória (EDA)** — Destaque os achados mais relevantes obtidos a partir da análise dos dados, priorizando aqueles que ajudam a explicar variações no NPS.
- **Fatores que mais impactam a satisfação do cliente** — Apresente quais variáveis ou aspectos da operação (entrega, atendimento, pedido etc.) se mostraram mais importantes para a satisfação do cliente, utilizando uma linguagem simples e exemplos quando possível.
- **Recomendações práticas para o negócio** — A partir dos insights obtidos, proponha ações concretas que a empresa poderia priorizar para melhorar a experiência do cliente.
- **Limitações e riscos da estratégia** — Aponte, de forma honesta e objetiva, as principais limitações da análise e os cuidados que a empresa deve ter ao utilizar esses resultados para tomada de decisão.

**O foco deve ser em storytelling com dados, e não em detalhes técnicos.**

### Vídeo Executivo (até 5 minutos)

Gravar um vídeo de no máximo 5 minutos, no qual:

- Pelo menos um integrante do grupo apresente o projeto;
- A apresentação seja feita em linguagem executiva;
- Sejam destacados:
    - O problema de negócio;
    - A solução proposta;
    - Os principais insights;
    - Como o modelo pode apoiar decisões reais.

**O vídeo deve simular uma apresentação para liderança ou stakeholders.**

---

Boa sorte e não deixe de chamar os professores da Fase 1 para discutir sobre seu trabalho!
