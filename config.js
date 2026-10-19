/* CONFIGURAÇÕES DA LOJA — Maison Caramela Bolsas (arquivo PÚBLICO: nunca coloque senha, token ou dados de clientes aqui) */
window.LOJA_CONFIG = {
  nomeLoja: "Maison Caramela Bolsas",
  whatsappNumber: "5541991064167",
  // Servidor de pagamento (Cloudflare Worker próprio desta loja: os pedidos não se misturam com as outras lojas)
  apiPagamento: "https://maison-caramela-bolsas-pagamento.cwbmodafitness.workers.dev",
  vendasAtivas: true,
  freteGratisAcima: 299.90,   // o servidor manda o valor oficial
  fretePesoPecaKg: 0.9,
  freteEmbalagemKg: 0.2,
  // Estimativa por região (só usada se o frete em tempo real não responder)
  freteTabela: {
    local:      { nome: "Curitiba e região metropolitana", pac: { preco: 18.90, prazo: [3, 5], kgAdicional: 3 }, sedex: { preco: 22.90, prazo: [1, 2], kgAdicional: 4 } },
    pr:         { nome: "Interior do Paraná", pac: { preco: 22.90, prazo: [4, 7], kgAdicional: 4 }, sedex: { preco: 32.90, prazo: [2, 3], kgAdicional: 6 } },
    sul_sp:     { nome: "SC, RS e SP", pac: { preco: 25.90, prazo: [5, 8], kgAdicional: 5 }, sedex: { preco: 41.90, prazo: [2, 4], kgAdicional: 8 } },
    sudeste_co: { nome: "RJ, MG, ES e Centro-Oeste (DF, GO, MS, MT)", pac: { preco: 31.90, prazo: [6, 10], kgAdicional: 6 }, sedex: { preco: 56.90, prazo: [3, 5], kgAdicional: 11 } },
    nordeste:   { nome: "Nordeste", pac: { preco: 41.90, prazo: [8, 13], kgAdicional: 8 }, sedex: { preco: 79.90, prazo: [3, 7], kgAdicional: 16 } },
    norte:      { nome: "Norte", pac: { preco: 48.90, prazo: [10, 16], kgAdicional: 10 }, sedex: { preco: 99.90, prazo: [4, 9], kgAdicional: 20 } }
  },
  cidade: "Curitiba – PR",
  textoEnvio: "Enviamos para todo o Brasil (Correios, Jadlog, JeT, Loggi); dúvidas e trocas pelo WhatsApp."
};
