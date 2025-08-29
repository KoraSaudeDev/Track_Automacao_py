from datetime import datetime
import logging
import pandas as pd
from app.service.calc_d1 import get_filtered_dates
from app.db import db


def DB():
    cursor = None
    conn   = None
    try:
        conn     = db.get_connection('HMS')
        cursor   = conn.cursor()

        data     = get_filtered_dates()[0]

        SQL = """
			SELECT 
			    '40085' AS "ID_Cliente_Hfocus",
			    A.HR_ATENDIMENTO AS "data_atendimento",
			    A.HR_ALTA AS "data_saida_alta",
			    P.NM_PACIENTE AS "name",
			    P.EMAIL AS "email",
			    PR.NM_PRESTADOR AS "medico",
			    (NVL(P.NR_DDI_CELULAR, '55') || NVL(P.NR_DDD_CELULAR, '') || NVL(P.NR_CELULAR, '')) AS "phone",
			    P.NR_CPF AS "cpf",
			    'Meridional Serra' AS "unidade",
			
			    CASE
			        WHEN A.TP_ATENDIMENTO = 'A' AND A.CD_ORI_ATE = 21 THEN 'ONCOLOGIA'
			        WHEN A.TP_ATENDIMENTO = 'E' THEN 'EXAMES'
			        WHEN A.TP_ATENDIMENTO = 'I' THEN 'INTERNACAO'
			        WHEN A.TP_ATENDIMENTO = 'A' AND A.CD_ORI_ATE = 9 THEN 'INTERNACAO'
			        WHEN A.TP_ATENDIMENTO = 'A' AND A.CD_SER_DIS IS NOT NULL THEN 'AMBULATORIO'
			        WHEN A.TP_ATENDIMENTO = 'U' THEN 'PRONTO_SOCORRO_GERAL'
			        ELSE 'OUTROS'
			    END AS "area_pesquisa",
			    
			    CASE
			        WHEN A.TP_ATENDIMENTO = 'A' AND A.CD_ORI_ATE = 21 THEN 'ONCOLOGIA'
			        WHEN A.TP_ATENDIMENTO = 'E' AND A.CD_ORI_ATE = 46 THEN 'HEMODINAMICA'
			        WHEN A.TP_ATENDIMENTO = 'E' AND A.CD_ORI_ATE = 7 THEN 'LABORATORIO'
			        WHEN A.TP_ATENDIMENTO = 'I' THEN 'INTERNACAO'
			        WHEN A.TP_ATENDIMENTO = 'A' AND A.CD_ORI_ATE = 9 THEN 'INTERNACAO'
			        WHEN A.TP_ATENDIMENTO = 'A' AND A.CD_SER_DIS IN (6,2,3,76,85,30,51,11) THEN S.DS_SER_DIS
			        WHEN A.TP_ATENDimento = 'A' AND A.CD_SER_DIS NOT IN (6,2,3,76,85,30,51,11) THEN 'GERAL_AMBULATORIO'
			        WHEN A.TP_ATENDIMENTO = 'U' AND A.CD_SERVICO = 1 THEN 'PA_OBSTÉTRICO'
			        WHEN A.TP_ATENDIMENTO = 'U' AND A.CD_SERVICO = 27 THEN 'PA_PEDIATRICO'
			        WHEN A.TP_ATENDIMENTO = 'U' THEN 'PA_ADULTO'
			        ELSE 'NAO_DEFINIDO'
			    END AS "setor"
			    
			FROM
			    DBAMV.ATENDIME A
			INNER JOIN 
			    DBAMV.PACIENTE P ON A.CD_PACIENTE = P.CD_PACIENTE
			INNER JOIN 
			    DBAMV.PRESTADOR PR ON A.CD_PRESTADOR = PR.CD_PRESTADOR
			LEFT JOIN 
			    DBAMV.SER_DIS S ON A.CD_SER_DIS = S.CD_SER_DIS
			    
			WHERE
			    (
			        (A.TP_ATENDIMENTO IN ('A', 'E') AND TRUNC(A.DT_ATENDIMENTO) = TRUNC(TO_TIMESTAMP(:data, 'YYYY-MM-DD HH24:MI:SS.FF3')))
			        OR
			        (A.TP_ATENDIMENTO IN ('I', 'U') AND TRUNC(A.DT_ALTA) = TRUNC(TO_TIMESTAMP(:data, 'YYYY-MM-DD HH24:MI:SS.FF3')))
			    )
			    AND (
			        -- ONCOLOGIA
			        (A.TP_ATENDIMENTO = 'A' AND A.CD_ORI_ATE = 21)
			        -- EXAMES (HEMODINAMICA E LABORATORIO)
			        OR (A.TP_ATENDIMENTO = 'E' AND A.CD_ORI_ATE IN (46, 7))
			        -- INTERNAÇÃO
			        OR (A.TP_ATENDIMENTO = 'I' AND A.CD_ATENDIMENTO_PAI IS NULL AND A.CD_CID NOT IN ('O60','O80','O82','O84','O757','O800','O801','O809','O810','O820','O821','O822','O829','O839','O840','O842','Z380','Z382') AND A.CD_MOT_ALT NOT IN (6,7,9,17,18,19,20,21,22))
			        -- HOSPITAL DIA
			        OR (A.TP_ATENDIMENTO = 'A' AND A.CD_ORI_ATE = 9)
			        -- AMBULATÓRIO
			        OR (A.TP_ATENDIMENTO = 'A' AND A.CD_SER_DIS IS NOT NULL AND A.CD_ORI_ATE NOT IN (21,9))
			        -- PRONTO SOCORRO
			        OR (A.TP_ATENDIMENTO = 'U' AND A.CD_TIP_RES NOT IN (1, 4, 11))
			    )
			
			   UNION ALL
			    
				select 
				 '40085'                        "ID_Cliente_Hfocus",
				A.HR_ATENDIMENTO AS "data_atendimento",
				A.HR_ALTA AS "data_saida_alta",
				P.NM_PACIENTE AS "name",
				P.EMAIL AS "email",
				PR.NM_PRESTADOR AS "medico",
				(NVL(P.NR_DDI_CELULAR, '55') || NVL(P.NR_DDD_CELULAR, '') || NVL(P.NR_CELULAR, '')) AS "phone",
				P.NR_CPF					 AS "cpf",
				'Meridional Serra'           AS "unidade",
				'MATERNIDADE'                AS "area_pesquisa",
				'MATERNIDADE'                AS "setor"
				from
				 dbamv.paciente    p
				,dbamv.atendime    a
				,dbamv.atendime    a2
				,DBAMV.PRESTADOR PR
				
				where
				    p.cd_paciente = a.cd_paciente
				AND A.CD_PRESTADOR = PR.CD_PRESTADOR
				and a.tp_atendimento = 'I'
				and a.cd_mot_alt not in (6,7,9,17,18,19,20,21,22)
				and a.CD_ATENDIMENTO = a2.CD_ATENDIMENTO_PAI
				and TRUNC(A.DT_ALTA) = TRUNC(TO_TIMESTAMP(:data, 'YYYY-MM-DD HH24:MI:SS.FF3'))
				       
				ORDER BY
				    "setor", "unidade"
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
