from sqlalchemy import create_engine, text
import os
from dotenv import load_dotenv

load_dotenv()

# Conecta ao banco especificado
conn_str = f"mysql+pymysql://{os.getenv('DB_USER')}:{os.getenv('DB_PASS')}@{os.getenv('DB_HOST')}/{os.getenv('DB_NAME')}"
engine = create_engine(conn_str)

with engine.connect() as conn:
    # Este comando lista todas as tabelas dentro do banco
    res = conn.execute(text("SHOW TABLES;"))
    print("Tabelas encontradas:", [r[0] for r in res])