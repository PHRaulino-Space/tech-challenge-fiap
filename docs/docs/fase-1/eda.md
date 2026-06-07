# Análise Exploratória — EDA

## Distribuição do NPS

<div style="position:relative; width:100%; height:380px;">
  <canvas id="chart-nps"></canvas>
</div>

<script src="https://cdn.jsdelivr.net/npm/chart.js@4.4.3/dist/chart.umd.min.js"></script>
<script>
  (function () {
    var ctx = document.getElementById("chart-nps").getContext("2d");

    new Chart(ctx, {
      type: "bar",
      data: {
        labels: ["Detratores (0–6)", "Neutros (7–8)", "Promotores (9–10)"],
        datasets: [{
          label: "Clientes",
          data: [1340, 870, 2290],
          backgroundColor: ["#ef444499", "#f97316aa", "#0284c7bb"],
          borderColor:     ["#ef4444",   "#f97316",   "#0284c7"],
          borderWidth: 2,
          borderRadius: 12,
          borderSkipped: false
        }]
      },
      options: {
        responsive: true,
        maintainAspectRatio: false,
        plugins: {
          legend: { display: false },
          tooltip: {
            backgroundColor: "#1a1a2e",
            titleColor: "#38bdf8",
            bodyColor: "#ffffff",
            borderColor: "#0284c7",
            borderWidth: 1,
            padding: 12,
            cornerRadius: 8,
            displayColors: false,
            callbacks: {
              title: function (items) { return items[0].label; },
              label: function (item) { return "  Clientes: " + item.raw.toLocaleString("pt-BR"); }
            }
          }
        },
        scales: {
          x: {
            grid: { display: false },
            ticks: { font: { size: 13 } }
          },
          y: {
            grid: { color: "rgba(128,128,128,0.12)" },
            ticks: { font: { size: 12 } },
            beginAtZero: true
          }
        },
        animation: {
          duration: 800,
          easing: "easeOutQuart"
        }
      }
    });
  })();
</script>
