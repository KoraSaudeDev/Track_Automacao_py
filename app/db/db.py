import os
import logging
import cx_Oracle
from dotenv import load_dotenv
load_dotenv()
cx_Oracle.init_oracle_client(lib_dir=os.getenv("ORACLE_CLIENT_PATH"))

logging.basicConfig(level=logging.INFO,filename="system.log")

def get_connection(db_alias):
    try:
        users   = os.getenv("DB_USERNAME")
        passwd  = os.getenv("DB_PASSWORD")
        db_host = os.getenv(f"DB_{db_alias}_HOST")
        db_port = os.getenv(f"DB_{db_alias}_PORT")
        db_name = os.getenv(f"DB_{db_alias}_NAME")

        dsn_tns = cx_Oracle.makedsn(db_host,
                                    int(db_port),
                                     service_name=db_name
                                     )
        
        conn = cx_Oracle.connect(user=users,
                                  password=passwd, 
                                  dsn=dsn_tns)
                                  
        logging.info("Banco conectado! MV ")
        return conn
    except Exception as e:
        logging.error(f"Erro ao conectar ao banco MV: {e}") 
        return

def get_connection_tasy(db_alias):
    try:
        users   = os.getenv("DB_USERNAME_TASY")
        passwd  = os.getenv("DB_PASSWORD_TASY")
        db_host = os.getenv(f"DB_{db_alias}_HOST")
        db_port = os.getenv(f"DB_{db_alias}_PORT")
        db_name = os.getenv(f"DB_{db_alias}_NAME")

        dsn_tns = cx_Oracle.makedsn(db_host,
                                    int(db_port),
                                     service_name=db_name
                                     )
        
        conn = cx_Oracle.connect(user=users,
                                  password=passwd, 
                                  dsn=dsn_tns)
                                  
        logging.info("Banco conectado! TASY ")
        return conn
    except Exception as e:
        logging.error(f"Erro ao conectar ao banco TASY: {e}")
        return