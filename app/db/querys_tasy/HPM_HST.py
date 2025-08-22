from datetime import datetime
import logging
import pandas as pd
from app.service.calc_d1 import get_filtered_dates
from app.db import db
logging.basicConfig(level=logging.INFO,filename="system.log")

def DB():
    try:
        conn     = db.get_connection_tasy("HPM_HST")
        cursor   = conn.cursor()

        data     = get_filtered_dates()[0]

        SQL = """
            SELECT 
                '40085' AS ID_Cliente_Hfocus,
                a.DT_ENTRADA AS "data_atendimento",
                a.DT_ALTA AS "data_saida_alta",
                b.NM_PESSOA_FISICA AS "name",
                b.DS_EMAIL_CCIH AS "email",
                m.NM_PESSOA_FISICA AS "medico",
                (NVL(b.NR_DDI_CELULAR, '55') || NVL(b.NR_DDD_CELULAR, '') || NVL(b.NR_TELEFONE_CELULAR, '')) AS "phone",
                b.NR_CPF AS "cpf",
                
                CASE
                    WHEN a.ie_tipo_atendimento = 3 THEN 'PRONTO SOCORRO GERAL'
                    WHEN a.ie_tipo_atendimento = 1 THEN 'INTERNACAO'
                    WHEN a.ie_tipo_atendimento = 7 THEN 'INTERNACAO'
                    WHEN a.nr_atendimento IN (151, 164, 271, 269) THEN 'ONCOLOGIA'
                    WHEN a.ie_tipo_atendimento = 8 AND a.nr_atendimento NOT IN (151, 164, 271, 269) THEN 'AMBULATORIO'
                    WHEN a.nr_atendimento = 154 THEN 'AMBULATORIO'
                END AS "area_pesquisa",
                
                CASE 
                    WHEN a.cd_Estabelecimento IN (1, 71) THEN 'Hospital Palmas Medical' 
                    WHEN a.cd_Estabelecimento = 81 THEN 'Hospital Santa Thereza'
                END AS "unidade",
                
                CASE
                    WHEN a.ie_tipo_atendimento = 3 THEN 'PA_ADULTO'
                    WHEN a.ie_tipo_atendimento IN (1, 7) THEN 'INTERNACAO'
                    WHEN a.ie_tipo_atendimento = 8 AND a.nr_atendimento NOT IN (151, 164, 271, 269) THEN 'GERAL_AMBULATORIO'
                    WHEN a.nr_atendimento = 154 THEN 'GERAL_AMBULATORIO'
                    WHEN a.nr_atendimento IN (151, 164, 271, 269) THEN 'ONCOLOGIA'
                END AS "setor"
                
            FROM 
                TASY.atendimento_paciente a
            INNER JOIN TASY.pessoa_fisica b ON a.CD_PESSOA_FISICA = b.cd_pessoa_fisica
            INNER JOIN TASY.pessoa_fisica m ON a.CD_MEDICO_RESP = m.CD_PESSOA_FISICA
            WHERE 
                
                TRUNC(A.DT_ALTA) = TRUNC(TO_TIMESTAMP(:data, 'YYYY-MM-DD HH24:MI:SS.FF3')) 
                AND a.dt_cancelamento IS NULL
                AND a.cd_estabelecimento IN (1, 71, 81)
                AND a.cd_motivo_alta NOT IN (18, 13, 9, 7, 16, 15)
        """

        cursor.execute(SQL, {'data': data})

        rows      = cursor.fetchall()
        columns   = [desc[0] for desc in cursor.description]
        df        = pd.DataFrame(rows, columns=columns)
        df["data_saida_alta"] = pd.to_datetime(df["data_saida_alta"]).dt.strftime("%Y-%m-%d %H:%M:%S")
        df["data_atendimento"] = pd.to_datetime(df["data_atendimento"]).dt.strftime("%Y-%m-%d %H:%M:%S")
        dict_data = df.to_dict(orient='records')

        return dict_data
    except Exception as e:
        logging.error(f"[{datetime.now()}] Erro ao aplicar a  query {__name__}: {e}")
        print(f"[{datetime.now()}] Erro ao aplicar a  query {__name__}: {e}")
        return None
    finally:
        if cursor and conn:
            cursor.close()
            conn.close()

