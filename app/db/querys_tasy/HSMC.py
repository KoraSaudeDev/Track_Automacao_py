from datetime import datetime
import logging
import pandas as pd
from app.service.calc_d1 import get_filtered_dates
from app.db import db
logging.basicConfig(level=logging.INFO,filename="system.log")

def DB():
    cursor = None
    conn   = None
    try:
        conn     = db.get_connection_tasy("HSMC")
        cursor   = conn.cursor()

        data     = get_filtered_dates()[0]

        SQL = """
            select '40085'ID_Cliente_Hfocus,
            a.DT_ENTRADA AS "data_atendimento",
            a.DT_ALTA AS "data_saida_alta",
            b.NM_PESSOA_FISICA AS "name",
            b.DS_EMAIL_CCIH AS "email",
            m.NM_PESSOA_FISICA AS "medico",
            (NVL(b.NR_DDI_CELULAR, '55') || NVL(b.NR_DDD_CELULAR, '') || NVL(b.NR_TELEFONE_CELULAR, '')) AS "phone",
            b.NR_CPF AS "cpf",
                    case
                    when a.ie_tipo_atendimento = 3 then 'PRONTO SOCORRO GERAL'
                    when a.ie_tipo_atendimento = 1 then 'INTERNACAO'
                    when a.ie_tipo_atendimento = 7 then 'INTERNACAO'
                    when a.ie_tipo_atendimento = 8 and a.nr_atendimento = 148 then 'ONCOLOGIA'
                --   when a.ie_tipo_atendimento = 8 and a.nr_atendimento LIKE 'C%' and a.nr_atendimento = 148 then 'ONCOLOGIA'
                    when a.ie_tipo_atendimento = 8 then 'AMBULATORIO'
                    end "area_pesquisa",
                    'Hospital Sao Mateus Cuiabá' AS "unidade",
                    case
                        when a.ie_tipo_atendimento = 3 THEN 'PA_ADULTO'
                    when a.ie_tipo_atendimento = 1 THEN 'INTERNACAO'
                    when a.ie_tipo_atendimento = 7 then 'INTERNACAO'
                    when a.ie_tipo_atendimento = 8 and a.nr_atendimento = 148 then 'ONCOLOGIA'
                    -- when a.ie_tipo_atendimento = 8 and a.nr_atendimento LIKE 'C%' and a.nr_atendimento = 148 then 'ONCOLOGIA'
                    when a.ie_tipo_atendimento = 8 then 'GERAL_AMBULATORIO'
                    END "setor"
            FROM 
                TASY.atendimento_paciente a
            INNER JOIN TASY.pessoa_fisica b ON a.CD_PESSOA_FISICA = b.cd_pessoa_fisica
            INNER JOIN TASY.pessoa_fisica m ON a.CD_MEDICO_RESP = m.CD_PESSOA_FISICA
            where 
            TRUNC(A.DT_ALTA) = TRUNC(TO_TIMESTAMP(:data, 'YYYY-MM-DD HH24:MI:SS.FF3')) 
            and a.dt_cancelamento is null
            and  a.cd_motivo_alta not in (18,24,7,22)
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

