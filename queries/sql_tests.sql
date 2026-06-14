-- 1. 10 produtos com maior valor de venda
SELECT PRODUCT_COD, PRODUCT_NAME, PRODUCT_VAL
FROM `looqbox-challenge`.data_product
ORDER BY PRODUCT_VAL DESC, PRODUCT_NAME ASC
LIMIT 10;

-- 2. Seções associadas aos departamentos BEBIDAS e PADARIA
SELECT DISTINCT DEP_NAME, SECTION_NAME
FROM `looqbox-challenge`.data_product
WHERE DEP_NAME IN ('BEBIDAS', 'PADARIA')
ORDER BY DEP_NAME, SECTION_NAME;

-- 3. Total de vendas por área de negócio no Q1 2019
SELECT 
    S.BUSINESS_NAME, 
    ROUND(SUM(V.SALES_VALUE), 2) AS TOTAL_SALES
FROM `looqbox-challenge`.data_store_cad S
JOIN `looqbox-challenge`.data_store_sales V ON S.STORE_CODE = V.STORE_CODE
WHERE V.DATE BETWEEN '2019-01-01' AND '2019-03-31'
GROUP BY S.BUSINESS_NAME
ORDER BY TOTAL_SALES DESC;