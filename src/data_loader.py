import os
import pandas as pd
from typing import Optional, Union, List
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.engine import Engine

# Carrega credenciais do arquivo .env na raiz
load_dotenv()

def get_db_connection() -> Engine:
    """
    Cria e retorna a engine de conexão com o banco de dados MySQL via SQLAlchemy.
    """
    user = os.getenv("DB_USER")
    password = os.getenv("DB_PASS")
    host = os.getenv("DB_HOST")
    db_name = os.getenv("DB_NAME")
    
    connection_string = f"mysql+pymysql://{user}:{password}@{host}/{db_name}"
    return create_engine(connection_string)

def retrieve_data(
    product_code: Optional[int] = None, 
    store_code: Optional[int] = None, 
    date: Optional[Union[List[str], tuple]] = None
) -> pd.DataFrame:
    """
    Extrai dados de vendas da tabela data_product_sales de forma dinâmica e segura.
    Desenvolvida para ser utilizada por múltiplos times.
    
    Args:
        product_code (int, opcional): Chave do produto.
        store_code (int, opcional): Chave da loja.
        date (list ou tuple, opcional): Range de datas. Ex: ['2019-01-01', '2019-01-31'].
        
    Returns:
        pd.DataFrame: DataFrame com os dados solicitados. Retorna DataFrame vazio em caso de falha.
    """
    engine = get_db_connection()
    
    # Schema definido conforme acesso ao banco
    query = "SELECT * FROM `looqbox-challenge`.data_product_sales WHERE 1=1"
    params = {}
    
    if product_code:
        query += " AND PRODUCT_CODE = %(p_code)s"
        params["p_code"] = product_code
    
    if store_code:
        query += " AND STORE_CODE = %(s_code)s"
        params["s_code"] = store_code
        
    if date and len(date) == 2:
        query += " AND DATE BETWEEN %(start)s AND %(end)s"
        params["start"] = date[0]
        params["end"] = date[1]
        
    try:
        # Execução segura utilizando parâmetros para evitar SQL Injection
        return pd.read_sql(query, engine, params=params)
    except Exception as e:
        # Previne a quebra de encadeamento de métodos do Pandas no código cliente
        print(f"Erro na extração: {e}")
        return pd.DataFrame()