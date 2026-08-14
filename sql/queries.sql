======================================================
    EXEMPLOS DE CONSULTAS PARA ANÁLISE DOS DADOS
======================================================


Visualiza todos os registros da tabela.

SELECT *
FROM dados_vendas;


Quantidade de vendas realizadas por estado.

SELECT
    uf_cliente,
    COUNT(*) AS total_vendas
FROM dados_vendas
GROUP BY uf_cliente
ORDER BY total_vendas DESC;


Faturamento total por categoria de produto.

SELECT
    categoria_prod,
    SUM(faturamento_total) AS faturamento
FROM dados_vendas
GROUP BY categoria_prod
ORDER BY faturamento DESC;


Calcula o ticket médio das vendas.

SELECT
    ROUND(AVG(faturamento_total), 2) AS ticket_medio
FROM dados_vendas;


Ranking dos produtos mais vendidos.

SELECT
    nome_produto,
    SUM(qtd_vendida) AS quantidade
FROM dados_vendas
GROUP BY nome_produto
ORDER BY quantidade DESC;


SELECT
    forma_pagamento,
    COUNT(*) AS total
FROM dados_vendas
GROUP BY forma_pagamento
ORDER BY total DESC;