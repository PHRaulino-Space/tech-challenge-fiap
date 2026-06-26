window.EDA_DATA = {
  "summary": {
    "clientes": 2500,
    "nota_media_recomendacao": 4.38,
    "nps_oficial": -66.0,
    "pct_detratores": 74.0,
    "pct_promotores": 8.0,
    "atraso_medio": 2.19,
    "pct_com_atraso": 88.9,
    "pearson_atraso_nota": -0.597,
    "spearman_atraso_nota": -0.586,
    "pearson_reclamacoes_nota": -0.497
  },
  "npsDistribution": [
    {
      "categoria": "Detrator",
      "clientes": 1851,
      "pct": 74.0
    },
    {
      "categoria": "Neutro",
      "clientes": 448,
      "pct": 17.9
    },
    {
      "categoria": "Promotor",
      "clientes": 201,
      "pct": 8.0
    }
  ],
  "correlations": [
    {
      "variable": "delivery_delay_days",
      "pearson": -0.5972599425,
      "spearman": -0.5862168617,
      "label": "Dias de atraso",
      "group": "Logística",
      "abs_correlation": 0.5972599425
    },
    {
      "variable": "repeat_purchase_30d",
      "pearson": 0.5703242099,
      "spearman": 0.4887567804,
      "label": "Recompra 30d",
      "group": "Satisfação",
      "abs_correlation": 0.5703242099
    },
    {
      "variable": "csat_internal_score",
      "pearson": 0.5639522619,
      "spearman": 0.5608863777,
      "label": "CSAT interno",
      "group": "Satisfação",
      "abs_correlation": 0.5639522619
    },
    {
      "variable": "complaints_count",
      "pearson": -0.4967997342,
      "spearman": -0.4902615767,
      "label": "Reclamações",
      "group": "Atendimento",
      "abs_correlation": 0.4967997342
    },
    {
      "variable": "customer_service_contacts",
      "pearson": -0.350844956,
      "spearman": -0.3363852019,
      "label": "Contatos SAC",
      "group": "Atendimento",
      "abs_correlation": 0.350844956
    },
    {
      "variable": "resolution_time_days",
      "pearson": -0.191391773,
      "spearman": -0.1903295587,
      "label": "Tempo resolução",
      "group": "Atendimento",
      "abs_correlation": 0.191391773
    },
    {
      "variable": "freight_value",
      "pearson": -0.0410871899,
      "spearman": -0.0395281486,
      "label": "Frete",
      "group": "Logística",
      "abs_correlation": 0.0410871899
    },
    {
      "variable": "order_value",
      "pearson": 0.0369902843,
      "spearman": 0.0358908349,
      "label": "Valor pedido",
      "group": "Pedido",
      "abs_correlation": 0.0369902843
    },
    {
      "variable": "delivery_attempts",
      "pearson": 0.0276796286,
      "spearman": 0.0262644461,
      "label": "Tentativas",
      "group": "Logística",
      "abs_correlation": 0.0276796286
    },
    {
      "variable": "discount_value",
      "pearson": 0.0251035797,
      "spearman": 0.0115665168,
      "label": "Desconto",
      "group": "Pedido",
      "abs_correlation": 0.0251035797
    },
    {
      "variable": "payment_installments",
      "pearson": 0.0237176555,
      "spearman": 0.0266600093,
      "label": "Parcelas",
      "group": "Pedido",
      "abs_correlation": 0.0237176555
    },
    {
      "variable": "items_quantity",
      "pearson": 0.0114681959,
      "spearman": 0.0062405875,
      "label": "Itens",
      "group": "Pedido",
      "abs_correlation": 0.0114681959
    },
    {
      "variable": "customer_age",
      "pearson": -0.0099362916,
      "spearman": -0.0074406547,
      "label": "Idade",
      "group": "Cliente",
      "abs_correlation": 0.0099362916
    },
    {
      "variable": "customer_tenure_months",
      "pearson": -0.009711399,
      "spearman": -0.0116494402,
      "label": "Relacionamento",
      "group": "Cliente",
      "abs_correlation": 0.009711399
    },
    {
      "variable": "delivery_time_days",
      "pearson": 0.0009249524,
      "spearman": 0.0002985533,
      "label": "Tempo entrega",
      "group": "Logística",
      "abs_correlation": 0.0009249524
    }
  ],
  "delayBands": [
    {
      "faixa_atraso": "0 dias",
      "clientes": 277,
      "nota_media": 6.86,
      "pct_reclamou": 91.7,
      "pct_acionou_sac": 76.53,
      "recompra_30d_pct": 33.94
    },
    {
      "faixa_atraso": "1 dia",
      "clientes": 615,
      "nota_media": 5.55,
      "pct_reclamou": 100.0,
      "pct_acionou_sac": 78.54,
      "recompra_30d_pct": 14.8
    },
    {
      "faixa_atraso": "2 dias",
      "clientes": 646,
      "nota_media": 4.58,
      "pct_reclamou": 100.0,
      "pct_acionou_sac": 78.95,
      "recompra_30d_pct": 4.02
    },
    {
      "faixa_atraso": "3 dias",
      "clientes": 525,
      "nota_media": 3.44,
      "pct_reclamou": 100.0,
      "pct_acionou_sac": 76.38,
      "recompra_30d_pct": 1.14
    },
    {
      "faixa_atraso": "4-5 dias",
      "clientes": 386,
      "nota_media": 2.15,
      "pct_reclamou": 100.0,
      "pct_acionou_sac": 77.2,
      "recompra_30d_pct": 0.26
    },
    {
      "faixa_atraso": "6+ dias",
      "clientes": 51,
      "nota_media": 0.81,
      "pct_reclamou": 100.0,
      "pct_acionou_sac": 82.35,
      "recompra_30d_pct": 0.0
    }
  ],
  "delayBoxplot": [
    {
      "faixa_atraso": "0 dias",
      "low": 1.1,
      "q1": 5.5,
      "median": 6.8,
      "q3": 8.5,
      "high": 10.0,
      "clientes": 277
    },
    {
      "faixa_atraso": "1 dia",
      "low": 0.0,
      "q1": 4.1,
      "median": 5.5,
      "q3": 7.0,
      "high": 10.0,
      "clientes": 615
    },
    {
      "faixa_atraso": "2 dias",
      "low": 0.0,
      "q1": 3.1,
      "median": 4.6,
      "q3": 6.0,
      "high": 10.0,
      "clientes": 646
    },
    {
      "faixa_atraso": "3 dias",
      "low": 0.0,
      "q1": 2.1,
      "median": 3.4,
      "q3": 4.8,
      "high": 9.4,
      "clientes": 525
    },
    {
      "faixa_atraso": "4-5 dias",
      "low": 0.0,
      "q1": 0.5,
      "median": 1.9,
      "q3": 3.38,
      "high": 8.3,
      "clientes": 386
    },
    {
      "faixa_atraso": "6+ dias",
      "low": 0.0,
      "q1": 0.0,
      "median": 0.3,
      "q3": 1.35,
      "high": 4.6,
      "clientes": 51
    }
  ],
  "delayDays": [
    {
      "dias_atraso": 0,
      "clientes": 277,
      "nota_media": 6.86,
      "pct_base": 11.1
    },
    {
      "dias_atraso": 1,
      "clientes": 615,
      "nota_media": 5.55,
      "pct_base": 24.6
    },
    {
      "dias_atraso": 2,
      "clientes": 646,
      "nota_media": 4.58,
      "pct_base": 25.8
    },
    {
      "dias_atraso": 3,
      "clientes": 525,
      "nota_media": 3.44,
      "pct_base": 21.0
    },
    {
      "dias_atraso": 4,
      "clientes": 270,
      "nota_media": 2.44,
      "pct_base": 10.8
    },
    {
      "dias_atraso": 5,
      "clientes": 116,
      "nota_media": 1.48,
      "pct_base": 4.6
    },
    {
      "dias_atraso": 6,
      "clientes": 34,
      "nota_media": 1.1,
      "pct_base": 1.4
    },
    {
      "dias_atraso": 7,
      "clientes": 14,
      "nota_media": 0.29,
      "pct_base": 0.6
    },
    {
      "dias_atraso": 8,
      "clientes": 3,
      "nota_media": 0.0,
      "pct_base": 0.1
    }
  ],
  "profiles": [
    {
      "perfil_degradacao": "Sem Problemas",
      "clientes": 65,
      "nota_media": 8.23,
      "pct_detrator": 13.85,
      "recompra_30d_pct": 66.15,
      "pct_base": 2.6
    },
    {
      "perfil_degradacao": "Só Atraso",
      "clientes": 489,
      "nota_media": 5.19,
      "pct_detrator": 65.24,
      "recompra_30d_pct": 11.45,
      "pct_base": 19.6
    },
    {
      "perfil_degradacao": "Só SAC",
      "clientes": 212,
      "nota_media": 6.43,
      "pct_detrator": 43.4,
      "recompra_30d_pct": 24.06,
      "pct_base": 8.5
    },
    {
      "perfil_degradacao": "Atraso + SAC",
      "clientes": 1734,
      "nota_media": 3.76,
      "pct_detrator": 82.53,
      "recompra_30d_pct": 3.92,
      "pct_base": 69.4
    }
  ],
  "regional": [
    {
      "customer_region": "Sudeste",
      "clientes": 520,
      "nota_media": 4.37,
      "pct_com_atraso": 90.96,
      "atraso_medio": 2.22
    },
    {
      "customer_region": "Nordeste",
      "clientes": 485,
      "nota_media": 4.42,
      "pct_com_atraso": 90.1,
      "atraso_medio": 2.19
    },
    {
      "customer_region": "Norte",
      "clientes": 506,
      "nota_media": 4.38,
      "pct_com_atraso": 87.94,
      "atraso_medio": 2.14
    },
    {
      "customer_region": "Sul",
      "clientes": 521,
      "nota_media": 4.49,
      "pct_com_atraso": 87.91,
      "atraso_medio": 2.17
    },
    {
      "customer_region": "Centro-Oeste",
      "clientes": 468,
      "nota_media": 4.21,
      "pct_com_atraso": 87.61,
      "atraso_medio": 2.22
    }
  ]
};
