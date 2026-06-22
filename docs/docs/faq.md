# Perguntas Frequentes (FAQ)

Dúvidas gerais sobre a entrega do Tech Challenge.

---

## Formato da Apresentação

**Posso entregar a apresentação em HTML (Reveal.js) hospedada no GitHub Pages?**

Sim, como documentação e material complementar é válido. Porém, para evitar qualquer problema de formato na entrega, recomenda-se também gerar uma versão em **PDF ou PPTX** da apresentação final. Assim você mantém o HTML como uma versão navegável, mas entrega também em um formato mais tradicional e fácil de avaliar.

---

## Business Model Canvas

**Devo restringir o Canvas ao que o case e o dataset permitem inferir?**

Sim, o raciocínio está correto. Não é necessário inventar informações que o case não fornece. Quando algo não estiver explícito — como logística interna ou terceirizada — trate como uma **hipótese ou limitação da análise**. Por exemplo: *"a base indica impacto de variáveis logísticas na satisfação, mas não permite afirmar se a operação é interna ou terceirizada"*. Esse tipo de cuidado é muito bem visto.

**Esse raciocínio se aplica às demais etapas (EDA, modelagem, avaliação)?**

Sim. Ater-se ao que o dataset e o case permitem inferir é a postura correta em todas as etapas. Quando houver lacunas, explicite-as como hipóteses ou limitações da análise.

---

## Vídeo de Apresentação

**Posso subir o vídeo no YouTube como "não listado"?**

Sim. Use **não listado** (unlisted). Evite deixar como privado, pois pode gerar problemas de acesso no momento da correção.

**O vídeo precisa mostrar os integrantes apresentando, ou pode ser gravação de tela com narração?**

O vídeo pode ser uma **gravação da tela com narração usando os slides**. Não há necessidade obrigatória de aparecer a webcam. Se quiser usar OBS Studio com webcam em miniatura no canto, também é válido.

---

## Planejamento com CRISP-DM

**Existe alguma etapa que ainda não mapeamos no planejamento?**

O uso do CRISP-DM como estrutura é adequado. Além das etapas técnicas, é importante deixar claro:

- Definição do **problema de negócio**
- Definição da **variável target** (ex.: NPS)
- **Hipóteses principais** a investigar
- **Limitações** dos dados
- Principais **achados da EDA**
- **Recomendações finais** para as áreas envolvidas

Isso conecta a parte técnica com o storytelling gerencial.

---

## Formato e Conteúdo da Documentação

**O formato de documentação no GitHub Pages (MkDocs) é aceito?**

Sim, o formato está interessante e pode ajudar bastante. Tome cuidado para a entrega final **não depender apenas da navegação da página**. Deixe tudo fácil de encontrar: link do repositório, apresentação, vídeo, notebooks/códigos e conclusões principais.

**A entrega final pode ser a página pública contendo todos os artefatos?**

Sim, desde que contenha: link do repositório, apresentação, vídeo, notebooks/códigos e conclusões principais — todos acessíveis sem depender da hierarquia de navegação.

---

## EDA e Visualizações

**Posso mostrar gráficos diretamente na documentação com conclusões?**

Sim, e esse é o caminho correto. O mais importante é não deixar o gráfico solto. Para cada visualização, inclua sempre:

- **O que esse gráfico mostra?**
- **Por que isso importa para o negócio?**
- **Qual decisão ou investigação ele sugere?**

---

## Checklist Geral da Entrega

Além do que já foi mapeado, certifique-se de incluir com clareza:

- [ ] Definição do problema de negócio
- [ ] Definição da variável target / NPS
- [ ] Tratamento e preparação dos dados
- [ ] EDA com hipóteses e achados
- [ ] Principais insights
- [ ] Limitações da análise
- [ ] Recomendações para as áreas envolvidas (logística, atendimento, produto, pricing etc.)
- [ ] Apresentação em PDF ou PPTX (além do HTML)
- [ ] Vídeo no YouTube como não listado
- [ ] Repositório público com notebooks e código

!!! tip "Dica"
    Não sofistique demais o formato a ponto de deixar a mensagem principal menos clara. O mais importante é que a entrega **conte uma boa história com os dados** e mostre como os achados ajudam o negócio.
