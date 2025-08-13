from datetime import datetime
import logging
import pandas as pd
from app.service.calc_d1 import get_filtered_dates
from app.db import db


def DB(db_mv):
    if db_mv == 'HMS':
        hospital = 'MERIDIONAL_SERRA'
    elif db_mv == 'HMC':
        hospital = 'MERIDIONAL_CARIACICA'   
    elif db_mv == 'HPC':
        hospital = 'MERIDIONAL_PRAIA_DA_COSTA'
    elif db_mv == 'HMV':
        hospital = 'MERIDIONAL_VITORIA'
    elif db_mv == 'HSF':
        hospital = 'HOSPITAL_SÃO_FRANCISCO'
    elif db_mv == 'HSL':
        hospital = 'HOSPITAL_SÃO_LUIZ'
    elif db_mv == 'HMSM':
        hospital = 'HOSPITAL_SÃO_MATEUS'

    try:
        conn     = db.get_connection(db_mv)
        cursor   = conn.cursor()

        data     = get_filtered_dates()[0]
        #data     = '2024-05-10 18:11:00.000'
        #data     = '2013-04-29 00:00:00.000'
        SQL = """
            -- Bloco 1: Pacientes de Ambulatório, Oncologia e Hospital Dia (tp_atendimento = 'A')
            SELECT
                '40085' AS "ID_Cliente_Hfocus",
                A.HR_ATENDIMENTO AS "Data_Base",
                P.NM_PACIENTE AS "name",
                P.EMAIL AS "email",
                (NVL(P.NR_DDI_CELULAR, '55') || NVL(P.NR_DDD_CELULAR, '') || NVL(P.NR_CELULAR, '')) AS "phone",
                P.NR_CPF AS "cpf",
                CASE
                    WHEN A.CD_ORI_ATE IN (6, 18, 27) THEN 'ONCOLOGIA'
                    WHEN A.CD_ORI_ATE = 9 THEN 'HOSPITAL_DIA'
                    ELSE 'AMBULATORIO'
                END AS "Area_Pesquisa",
                :hospital AS "Segmentacao_1",
                CASE
                    WHEN A.CD_ORI_ATE IN (6, 18, 27) THEN 'ONCOLOGIA'
                    WHEN A.CD_ORI_ATE = 9 THEN 'INTERNACAO'
                    WHEN A.CD_SER_DIS IN (6, 2, 3, 76, 85, 30, 51, 11) THEN S.DS_SER_DIS
                    ELSE 'GERAL_AMBULATORIO'
                END AS "Segmentacao_2"
            FROM
                DBAMV.ATENDIME A
            INNER JOIN DBAMV.PACIENTE P ON A.CD_PACIENTE = P.CD_PACIENTE
            LEFT JOIN DBAMV.SER_DIS S ON A.CD_SER_DIS = S.CD_SER_DIS
            WHERE
                A.TP_ATENDIMENTO = 'A'
                AND TRUNC(A.DT_ATENDIMENTO) = TRUNC(TO_TIMESTAMP(:data, 'YYYY-MM-DD HH24:MI:SS.FF3'))
            
            UNION ALL
            
            -- Bloco 2: Pacientes de Exames Externos (tp_atendimento = 'E')
            SELECT
                '40085' AS "ID_Cliente_Hfocus",
                A.HR_ATENDIMENTO AS "Data_Base",
                P.NM_PACIENTE AS "name",
                P.EMAIL AS "email",
                (NVL(P.NR_DDI_CELULAR, '55') || NVL(P.NR_DDD_CELULAR, '') || NVL(P.NR_CELULAR, '')) AS "phone",
                P.NR_CPF AS "cpf",
                'EXAMES' AS "Area_Pesquisa",
                :hospital AS "Segmentacao_1",
                CASE
                    WHEN A.CD_ORI_ATE = 46 THEN 'HEMODINAMICA'
                    WHEN A.CD_ORI_ATE = 7 THEN 'LABORATORIO'
                END AS "Segmentacao_2"
            FROM
                DBAMV.ATENDIME A
            INNER JOIN DBAMV.PACIENTE P ON A.CD_PACIENTE = P.CD_PACIENTE
            WHERE
                A.TP_ATENDIMENTO = 'E'
                AND A.CD_ORI_ATE IN (46, 7)
                AND TRUNC(A.DT_ATENDIMENTO) = TRUNC(TO_TIMESTAMP(:data, 'YYYY-MM-DD HH24:MI:SS.FF3'))
            
            UNION ALL
            
            -- Bloco 3: Pacientes Internados (Geral e Maternidade) (tp_atendimento = 'I')
            SELECT
                '40085' AS "ID_Cliente_Hfocus",
                A.HR_ATENDIMENTO AS "Data_Base",
                P.NM_PACIENTE AS "name",
                P.EMAIL AS "email",
                (NVL(P.NR_DDI_CELULAR, '55') || NVL(P.NR_DDD_CELULAR, '') || NVL(P.NR_CELULAR, '')) AS "phone",
                P.NR_CPF AS "cpf",
                CASE
                    WHEN A2.CD_ATENDIMENTO_PAI IS NOT NULL THEN 'MATERNIDADE'
                    ELSE 'INTERNACAO'
                END AS "Area_Pesquisa",
                :hospital AS "Segmentacao_1",
                CASE
                    WHEN A2.CD_ATENDIMENTO_PAI IS NOT NULL THEN 'MATERNIDADE'
                    ELSE 'INTERNACAO'
                END AS "Segmentacao_2"
            FROM
                DBAMV.ATENDIME A
            INNER JOIN DBAMV.PACIENTE P ON A.CD_PACIENTE = P.CD_PACIENTE
            -- LEFT JOIN para identificar se o atendimento é um atendimento "pai" (mãe na maternidade)
            LEFT JOIN DBAMV.ATENDIME A2 ON A.CD_ATENDIMENTO = A2.CD_ATENDIMENTO_PAI
            WHERE
                A.TP_ATENDIMENTO = 'I'
                AND A.CD_MOT_ALT NOT IN (6, 7, 9, 17, 18, 19, 20, 21, 22)
                -- Lógica para incluir Maternidade OU Internação Geral (que não seja da maternidade)
                AND (
                    A2.CD_ATENDIMENTO_PAI IS NOT NULL -- Condição da Maternidade
                    OR 
                    (A.CD_ATENDIMENTO_PAI IS NULL AND A.CD_CID NOT IN ('O60','O80','O82','O84','O757','O800','O801','O809','O810','O820','O821','O822','O829','O839','O840','O842','Z380','Z382')) -- Condição de Internação Geral
                )
                AND TRUNC(A.DT_ALTA) = TRUNC(TO_TIMESTAMP(:data, 'YYYY-MM-DD HH24:MI:SS.FF3'))
            
            UNION ALL
            
            -- Bloco 4: Pacientes de Pronto Socorro (tp_atendimento = 'U')
            SELECT DISTINCT 
                '40085' AS "ID_Cliente_Hfocus",
                A.HR_ATENDIMENTO AS "Data_Base",
                P.NM_PACIENTE AS "name",
                P.EMAIL AS "email",
                (NVL(P.NR_DDI_CELULAR, '55') || NVL(P.NR_DDD_CELULAR, '') || NVL(P.NR_CELULAR, '')) AS "phone",
                P.NR_CPF AS "cpf",
                'PRONTO_SOCORRO_GERAL' AS "Area_Pesquisa",
                :hospital AS "Segmentacao_1",
                CASE
                    WHEN A.CD_SERVICO = 1 THEN 'PA_OBSTÉTRICO'
                    WHEN A.CD_SERVICO = 27 THEN 'PA_PEDIATRICO'
                    ELSE 'PA_ADULTO'
                END AS "Segmentacao_2"
            FROM
                DBAMV.ATENDIME A
            INNER JOIN DBAMV.PACIENTE P ON A.CD_PACIENTE = P.CD_PACIENTE
            WHERE
                A.TP_ATENDIMENTO = 'U'
                AND A.CD_TIP_RES NOT IN (1, 4, 11)
                AND TRUNC(A.DT_ALTA) = TRUNC(TO_TIMESTAMP(:data, 'YYYY-MM-DD HH24:MI:SS.FF3'))
            
            ORDER BY
                "Segmentacao_2", "Segmentacao_1"

        """
        cursor.execute(SQL, {'hospital': hospital, 'data': data})

        rows      = cursor.fetchall()
        columns   = [desc[0] for desc in cursor.description]
        df        = pd.DataFrame(rows, columns=columns)
        df["Data_Base"] = pd.to_datetime(df["Data_Base"]).dt.strftime("%Y-%m-%d %H:%M:%S")
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
