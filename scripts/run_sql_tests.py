import pandas as pd
from src.data_loader import get_db_connection

def run_queries():
    engine = get_db_connection()
    
    query1 = """
    SELECT PRODUCT_COD, PRODUCT_NAME, PRODUCT_VAL
    FROM `looqbox-challenge`.data_product
    ORDER BY PRODUCT_VAL DESC, PRODUCT_NAME ASC
    LIMIT 10;
    """
    
    query2 = """
    SELECT DISTINCT DEP_NAME, SECTION_NAME
    FROM `looqbox-challenge`.data_product
    WHERE DEP_NAME IN ('BEBIDAS', 'PADARIA')
    ORDER BY DEP_NAME, SECTION_NAME;
    """
    
    query3 = """
    SELECT 
        S.BUSINESS_NAME, 
        ROUND(SUM(V.SALES_VALUE), 2) AS TOTAL_SALES
    FROM `looqbox-challenge`.data_store_cad S
    JOIN `looqbox-challenge`.data_store_sales V ON S.STORE_CODE = V.STORE_CODE
    WHERE V.DATE BETWEEN '2019-01-01' AND '2019-03-31'
    GROUP BY S.BUSINESS_NAME
    ORDER BY TOTAL_SALES DESC;
    """
    
    print("\n--- Resultado Query 1 (Top 10 Produtos) ---")
    print(pd.read_sql(query1, engine).to_string(index=False))
    
    print("\n--- Resultado Query 2 (Seções Bebidas/Padaria) ---")
    print(pd.read_sql(query2, engine).to_string(index=False))
    
    print("\n--- Resultado Query 3 (Vendas Q1 2019) ---")
    print(pd.read_sql(query3, engine).to_string(index=False))

if __name__ == "__main__":
    run_queries()