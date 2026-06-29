# 9. Apresentação Final

*CRISP-DM: Deployment*

Visão consolidada do case NPS Preditivo, conectando Business Canvas, hipóteses, EDA, preparação dos dados, proposta de solução e avaliação final.

## Materiais da Entrega

| Material | Link |
|---|---|
| Apresentação executiva | [Abrir em tela cheia](slides.html) |
| EDA final | [Notebook consolidado](https://github.com/PHRaulino-Space/tech-challenge-fiap/blob/main/notebooks/eda_final.ipynb) |
| Script pareado do notebook | [eda_final.py](https://github.com/PHRaulino-Space/tech-challenge-fiap/blob/main/notebooks/eda_final.py) |
| Página de EDA na documentação | [EDA Final](eda.md) |

## Mensagem Central

A análise demonstra que o baixo NPS da base não é explicado por perfil de cliente, região, ticket, desconto ou forma de pagamento. O problema aparece na execução operacional pós-compra, principalmente no descumprimento do prazo prometido e no acúmulo de atendimento.

Principais evidências usadas na apresentação:

| Achado | Evidência |
|---|---|
| Base majoritariamente detratora | 74,0% detratores; NPS médio 4,38 |
| Atraso é o maior sinal | `delivery_delay_days`: correlação -0,60 |
| Atendimento reforça a degradação | `complaints_count`: -0,50; `customer_service_contacts`: -0,35 |
| Problema é sistêmico | 88% a 91% de atraso em todas as regiões |
| Pior perfil domina a base | 69,4% em "Atraso + SAC" |
| Detratores não retornam | 0,0% de recompra em 30 dias |

## Slides

<div class="slides-embed">
  <iframe
    id="slides-frame"
    src="../slides.html"
    title="Apresentação — NPS Preditivo"
    allow="fullscreen"
    allowfullscreen
    tabindex="0"
  ></iframe>
  <a
    href="../slides.html"
    data-md-ignore
    target="_blank"
    rel="noopener noreferrer"
    class="slides-fullscreen-btn"
    onclick="var f=document.getElementById('slides-frame');if(f.requestFullscreen){event.preventDefault();f.requestFullscreen();}else if(f.webkitRequestFullscreen){event.preventDefault();f.webkitRequestFullscreen();}"
  >&#x26F6; Tela cheia</a>
</div>

<script>
  (function () {
    var frame = document.getElementById("slides-frame");
    if (!frame) return;

    function focusSlides() {
      frame.focus();
      if (frame.contentWindow) {
        frame.contentWindow.focus();
      }
    }

    frame.addEventListener("load", focusSlides);
    frame.addEventListener("mouseenter", focusSlides);
    frame.addEventListener("click", focusSlides);

    document.addEventListener("keydown", function (event) {
      var reveal = frame.contentWindow && frame.contentWindow.Reveal;
      if (!reveal) return;

      if (event.key === "ArrowRight" || event.key === "PageDown" || event.key === " ") {
        event.preventDefault();
        reveal.next();
      }

      if (event.key === "ArrowLeft" || event.key === "PageUp") {
        event.preventDefault();
        reveal.prev();
      }

      if (event.key === "Home") {
        event.preventDefault();
        reveal.slide(0);
      }

      if (event.key === "End") {
        event.preventDefault();
        reveal.slide(Number.MAX_SAFE_INTEGER);
      }
    });
  })();
</script>

> Use as setas do teclado para navegar entre os slides. Pressione `F` para tela cheia nativa no Reveal.js.
