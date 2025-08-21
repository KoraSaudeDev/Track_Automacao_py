import os
import cx_Oracle
cx_Oracle.init_oracle_client(lib_dir=os.getenv("ORACLE_CLIENT_PATH"))

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
                                  
        print("Banco conectado!")
        return conn
    except Exception as e:
        print(f"Erro ao conectar ao banco: {e}")
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
                                  
        print("Banco conectado!")
        return conn
    except Exception as e:
        print(f"Erro ao conectar ao banco: {e}")
        return