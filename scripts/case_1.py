import pandas as pd
from src.data_loader import retrieve_data

# Configuração global para visualização do Pandas no terminal
pd.set_option('display.max_columns', None)
pd.set_option('display.width', 1000)

def run_case_1():
    """
    Demonstração de uso da função dinâmica retrieve_data.
    Um guia rápido para que analistas de outras equipes 
    possam consumir a base de vendas sem precisar de SQL.
    """
    print("\n" + "="*55)
    print(" GUIA DE EXTRAÇÃO DE VENDAS (data_product_sales)")
    print("="*55 + "\n")
    
    # ---------------------------------------------------------
    # Exemplo 1: Filtro Completo
    # ---------------------------------------------------------
    print("--- Cenário 1: Extração Granular Exata ---")
    
    product_code = 1001
    store_code = 1
    date = ['2019-01-01', '2019-01-31']
    
    my_data = retrieve_data(product_code, store_code, date)
    
    print(f"Status: Sucesso. Retornou um DataFrame com {len(my_data.columns)} colunas.")
    print(my_data.head())

    # ---------------------------------------------------------
    # Exemplo 2: Validação da Flexibilidade (Apenas Loja)
    # ---------------------------------------------------------
    print("\n--- Cenário 2: Extração Flexível (Apenas Loja) ---")
    print("Ideal para quando o time Comercial precisa validar o total da loja, sem isolar produtos.")
    
    data_store = retrieve_data(store_code=5)
    print(data_store.head())

    # ---------------------------------------------------------
    # Exemplo 3: Bypass Total (Sem Filtros)
    # ---------------------------------------------------------
    print("\n--- Cenário 3: Extração Irrestrita (Tabela Completa) ---")
    print("Traz a tabela inteira. Atenção: em produção, isso pode consumir muita memória.")
    
    data_all = retrieve_data()
    print(data_all.head())

if __name__ == "__main__":
    run_case_1()