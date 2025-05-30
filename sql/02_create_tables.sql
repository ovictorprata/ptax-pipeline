CREATE TABLE IF NOT EXISTS mesa_cambio.cotacao_ptax (
    data DATE PRIMARY KEY,
    taxa_compra NUMERIC(10,4),
    taxa_venda  NUMERIC(10,4),
    retrieved_at TIMESTAMP DEFAULT now()
);

CREATE TABLE IF NOT EXISTS receita.cotacao_ptax_congelada (
    data DATE PRIMARY KEY,
    taxa_venda NUMERIC(10,4),
    travada_em DATE,               -- armazena o 1.º dia útil da virada
    retrieved_at TIMESTAMP DEFAULT now()
);
