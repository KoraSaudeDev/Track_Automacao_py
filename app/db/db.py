import cx_Oracle
from app.config import Config

def get_connection():
    try:
        dsn_tns = cx_Oracle.makedsn(Config.DB_HOST, Config.DB_PORT, service_name=Config.DB_NAME)
        conn = cx_Oracle.connect(user=Config.DB_USERNAME, password=Config.DB_PASSWORD, dsn=dsn_tns)
        print("Banco conectado!")
        return conn
    except Exception as e:
        print(f"Erro ao conectar ao banco: {e}")
        return