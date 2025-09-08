from datetime import datetime
import logging
import pandas as pd
from app.service.calc_d1 import get_filtered_dates
from app.db import db


def DB_SUB():
    cursor = None
    conn   = None
    try:
        conn     = db.get_connection('HSL')
        cursor   = conn.cursor()

        data     = get_filtered_dates()[0]


        SQL = """
            SELECT    
                '40085', a.hr_atendimento AS "data_atendimento",A.HR_ALTA AS "data_saida_alta",A.CD_ATENDIMENTO AS "cd_atendimento", p.nm_paciente AS "name", p.email AS "email",PR.NM_PRESTADOR AS "medico",
                (NVL(p.nr_ddi_celular, '55') || NVL(p.nr_ddd_celular, '') || NVL(p.nr_celular, '')) AS "phone",
                p.nr_cpf AS "cpf", 'EXAMES' AS "area_pesquisa", 'Meridional Praia Da Costa' AS "unidade",
                CASE WHEN a.cd_ori_ate = 8 THEN 'LABORATORIO' END  AS "setor"
            FROM dbamv.paciente p
            INNER JOIN dbamv.atendime a ON p.cd_paciente = a.cd_paciente
            INNER JOIN DBAMV.PRESTADOR PR ON A.CD_PRESTADOR = PR.CD_PRESTADOR 
            WHERE a.tp_atendimento = 'E' AND a.cd_ori_ate = 8 AND TRUNC(a.dt_atendimento) = TRUNC(TO_TIMESTAMP(:data,'YYYY-MM-DD HH24:MI:SS.FF3'))
    		AND TRUNC(a.hr_atendimento) <= TRUNC(TO_TIMESTAMP(:data,'YYYY-MM-DD HH24:MI:SS.FF3'))		
            AND (
	      			a.HR_ALTA IS NULL
		      		OR TRUNC(a.HR_ALTA) <= TRUNC(TO_TIMESTAMP(:data,'YYYY-MM-DD HH24:MI:SS.FF3'))
				)    
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
        if cursor is not None:
            cursor.close()
        if conn is not None:
            conn.close()
