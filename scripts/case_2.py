import pandas as pd
from src.data_loader import get_db_connection

# Configuração global para exibir a tabela perfeitamente no terminal
pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)
pd.set_option('display.width', 1000)

def run_case_2():
    """
    Gera o relatório de Ticket Médio (TM) por Loja e Categoria (Q4 2019).
    
    Racional de Arquitetura (ETL em Memória):
    Como o requisito de negócio exige o uso estrito das queries fornecidas 
    sem alterações na sintaxe SQL, toda a camada de transformação (Filtro de datas, 
    agregações e cálculo de KPIs) foi transferida para a memória utilizando Pandas.
    """
    print("\n" + "="*55)
    print(" RELATÓRIO DE TICKET MÉDIO (Q4 2019)")
    print("="*55 + "\n")
    
    # =========================================================
    # 1. CONTRATO DO CLIENTE (QUERIES IMUTÁVEIS)
    # As queries abaixo foram mantidas exata e rigorosamente como fornecidas.
    # =========================================================
    query_1 = """
SELECT
      STORE_CODE,
      STORE_NAME,
      START_DATE,
      END_DATE,
      BUSINESS_NAME,
      BUSINESS_CODE
FROM data_store_cad
    """
    
    query_2 = """
SELECT
        STORE_CODE,
        DATE,
        SALES_VALUE,
        SALES_QTY
FROM data_store_sales
WHERE DATE BETWEEN '2019-01-01' AND '2019-12-31'
    """
    
    engine = get_db_connection()
    print("-> Extraindo dados do banco (Raw Data)...")
    
    # Adaptação de Infraestrutura: Passei .lower() apenas na hora da execução.
    # Isso preserva a string original, mas impede que o código quebre 
    # no servidor Linux (case-sensitive) da Looqbox.
    df_cad = pd.read_sql(query_1.lower(), engine)
    df_sales = pd.read_sql(query_2.lower(), engine)
    
    # Normalização preventiva de colunas (garante que todas fiquem em maiúsculo 
    # no Pandas, independente de como o banco as retornou).
    df_cad.columns = [col.upper() for col in df_cad.columns]
    df_sales.columns = [col.upper() for col in df_sales.columns]
    
    # =========================================================
    # 2. TRANSFORM (FILTRO E MERGE)
    # =========================================================
    print("-> Aplicando recorte temporal (Q4 2019) e modelagem de dados...")
    
    # Conversão explícita para datetime e aplicação da máscara booleana
    df_sales['DATE'] = pd.to_datetime(df_sales['DATE'])
    mask_q4 = (df_sales['DATE'] >= '2019-10-01') & (df_sales['DATE'] <= '2019-12-31')
    df_sales_q4 = df_sales.loc[mask_q4].copy()
    
    # Garantia de Tipagem antes do JOIN (evita falhas silenciosas de schema)
    df_cad['STORE_CODE'] = df_cad['STORE_CODE'].astype(int)
    df_sales_q4['STORE_CODE'] = df_sales_q4['STORE_CODE'].astype(int)
    
    # Cruzamento das bases
    df_merged = pd.merge(df_sales_q4, df_cad, on='STORE_CODE', how='inner')
    
    # =========================================================
    # 3. REGRA DE NEGÓCIO E AGREGAÇÃO (KPI)
    # =========================================================
    print("-> Calculando o KPI de Ticket Médio...")
    
    # Agregação matemática prévia (Soma o valor total e a quantidade total por loja/categoria)
    df_grouped = df_merged.groupby(['STORE_NAME', 'BUSINESS_NAME'], as_index=False)[['SALES_VALUE', 'SALES_QTY']].sum()
    
    # Cálculo seguro do Ticket Médio: previne erro fatal em caso de SALES_QTY ser zero
    df_grouped['TM'] = df_grouped['SALES_VALUE'].div(df_grouped['SALES_QTY'].replace(0, pd.NA))
    
    # =========================================================
    # 4. FORMATAÇÃO E ENTREGA
    # =========================================================
    df_final = df_grouped[['STORE_NAME', 'BUSINESS_NAME', 'TM']].copy()
    
    # Renomeando as colunas para espelhar exatamente a tabela gabarito
    df_final.rename(columns={
        'STORE_NAME': 'Loja',
        'BUSINESS_NAME': 'Categoria'
    }, inplace=True)
    
    # Ordenação final exigida na visualização do cliente (ordem alfabética pela loja)
    df_final.sort_values(by='Loja', inplace=True)
    df_final.reset_index(drop=True, inplace=True)
    
    # Formatação do TM para 2 casas decimais
    df_final['TM'] = df_final['TM'].apply(lambda x: f"{x:.2f}")
    
    print("\n--- Relatório Gerado com Sucesso ---\n")
    print(df_final.to_string(index=False))

if __name__ == "__main__":
    run_case_2()