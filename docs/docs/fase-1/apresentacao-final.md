# 8. Apresentação Final

*CRISP-DM: Deployment*

Visão consolidada do case NPS Preditivo com base no Business Canvas — primeira entrega da Fase 1.

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
