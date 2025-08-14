from datetime import datetime
import logging
import pandas as pd
from app.service.calc_d1 import get_filtered_dates
from app.db import db
logging.basicConfig(level=logging.INFO,filename="system.log")

def DB(hospital = None):
    try:
        conn     = db.get_connection("OTO_ING")
        cursor   = conn.cursor()

        data     = get_filtered_dates()[0]
        #data     = '2024-05-11 18:11:00.000'
        SQL = """
            -- Bloco 1: Pacientes do Pronto Socorro (Urgência)
            SELECT
                '40085' AS "ID_CLIENTE_HFOCUS",
                A.HR_ATENDIMENTO AS "Data_Base",
                P.NM_PACIENTE AS "NOME_COMPLETO_PACIENTE",
                P.EMAIL AS "E-MAIL",
                (NVL(P.NR_DDI_CELULAR, '55') || NVL(P.NR_DDD_CELULAR, '') || NVL(P.NR_CELULAR, '')) AS "PHONE",
                P.NR_CPF AS "CPF",
                'PRONTO_SOCORRO_GERAL' AS "area_pesquisa",
                M.DS_MULTI_EMPRESA AS "Segmentacao_1",
                CASE 
                    WHEN A.CD_SERVICO = 5 THEN 'PA_OBSTÉTRICO'
                    WHEN A.CD_SERVICO = 40 THEN 'PA_PEDIATRICO'
                    ELSE 'PA_ADULTO'
                END AS "Segmentacao_2"
            FROM DBAMV.ATENDIME A
            INNER JOIN DBAMV.PACIENTE P ON A.CD_PACIENTE = P.CD_PACIENTE
            INNER JOIN DBAMV.MULTI_EMPRESAS M ON A.CD_MULTI_EMPRESA = M.CD_MULTI_EMPRESA
            WHERE
                A.TP_ATENDIMENTO = 'U'
                AND TRUNC(A.DT_ALTA) = TRUNC(TO_TIMESTAMP(:data,'YYYY-MM-DD HH24:MI:SS.FF3'))
                AND NOT EXISTS (
                    SELECT 1 FROM DBAMV.TIP_RES TP WHERE TP.CD_TIP_RES = A.CD_TIP_RES AND TP.SN_OBITO = 'S'
                )

            UNION ALL

            -- Bloco 2: Pacientes Internados (Maternidade e Outros)
            SELECT
                '40085' AS "ID_CLIENTE_HFOCUS",
                A.HR_ATENDIMENTO AS "Data_Base",
                P.NM_PACIENTE AS "NOME_COMPLETO_PACIENTE",
                P.EMAIL AS "E-MAIL",
                (NVL(P.NR_DDI_CELULAR, '55') || NVL(P.NR_DDD_CELULAR, '') || NVL(P.NR_CELULAR, '')) AS "PHONE",
                P.NR_CPF AS "CPF",
                CASE
                    WHEN A2.CD_ATENDIMENTO_PAI IS NOT NULL THEN 'MATERNIDADE'
                    ELSE 'INTERNACAO'
                END AS "area_pesquisa",
                M.DS_MULTI_EMPRESA AS "Segmentacao_1",
                CASE
                    WHEN A2.CD_ATENDIMENTO_PAI IS NOT NULL THEN 'MATERNIDADE'
                    ELSE 'INTERNACAO'
                END AS "Segmentacao_2"
            FROM DBAMV.ATENDIME A
            INNER JOIN DBAMV.PACIENTE P ON A.CD_PACIENTE = P.CD_PACIENTE
            INNER JOIN DBAMV.MULTI_EMPRESAS M ON A.CD_MULTI_EMPRESA = M.CD_MULTI_EMPRESA
            LEFT JOIN DBAMV.ATENDIME A2 ON A.CD_ATENDIMENTO = A2.CD_ATENDIMENTO_PAI
            WHERE
                A.TP_ATENDIMENTO = 'I'
                AND TRUNC(A.DT_ALTA) = TRUNC(TO_TIMESTAMP(:data,'YYYY-MM-DD HH24:MI:SS.FF3'))
                AND (
                    (A2.CD_ATENDIMENTO_PAI IS NOT NULL)
                    OR
                    (
                        A.CD_CID NOT IN ('O60','O80','O82','O84','O757','O800','O801','O809','O810','O820','O821','O822','O829','O839','O840','O842','Z380','Z382')
                        AND NOT EXISTS (SELECT 1 FROM DBAMV.MOT_ALT MA WHERE MA.CD_MOT_ALT = A.CD_MOT_ALT AND MA.TP_MOT_ALTA = 'O')
                    )
                )

            UNION ALL

            -- Bloco 3: Pacientes de Exames (Agrupados)
            SELECT
                '40085' AS "ID_CLIENTE_HFOCUS",
                A.HR_ATENDIMENTO AS "Data_Base",
                P.NM_PACIENTE AS "NOME_COMPLETO_PACIENTE",
                P.EMAIL AS "E-MAIL",
                (NVL(P.NR_DDI_CELULAR, '55') || NVL(P.NR_DDD_CELULAR, '') || NVL(P.NR_CELULAR, '')) AS "PHONE",
                P.NR_CPF AS "CPF",
                'EXAMES' AS "area_pesquisa",
                M.DS_MULTI_EMPRESA AS "Segmentacao_1",
                CASE
                    WHEN A.CD_ORI_ATE = 103 THEN 'HEMODINAMICA'
                    WHEN A.CD_ORI_ATE IN (47, 22, 104, 106, 109) THEN 'IMAGEM'
                    WHEN A.CD_ORI_ATE = 16 THEN 'LABORATORIO'
                    WHEN A.CD_ORI_ATE IN (29, 110, 100) THEN 'ENDOSCOPIA'
                END AS "Segmentacao_2"
            FROM DBAMV.ATENDIME A
            INNER JOIN DBAMV.PACIENTE P ON A.CD_PACIENTE = P.CD_PACIENTE
            INNER JOIN DBAMV.MULTI_EMPRESAS M ON A.CD_MULTI_EMPRESA = M.CD_MULTI_EMPRESA
            WHERE
                A.TP_ATENDIMENTO = 'E'
                AND A.CD_ORI_ATE IN (103, 47, 22, 104, 106, 109, 16, 29, 110, 100)
                AND TRUNC(A.DT_ATENDIMENTO) = TRUNC(TO_TIMESTAMP(:data,'YYYY-MM-DD HH24:MI:SS.FF3'))

            UNION ALL

            -- Bloco 4: Pacientes de Ambulatório (Agrupados)
            SELECT
                '40085' AS "ID_CLIENTE_HFOCUS",
                A.HR_ATENDIMENTO AS "Data_Base",
                P.NM_PACIENTE AS "NOME_COMPLETO_PACIENTE",
                P.EMAIL AS "E-MAIL",
                (NVL(P.NR_DDI_CELULAR, '55') || NVL(P.NR_DDD_CELULAR, '') || NVL(P.NR_CELULAR, '')) AS "PHONE",
                P.NR_CPF AS "CPF",
                'AMBULATORIO' AS "area_pesquisa",
                M.DS_MULTI_EMPRESA AS "Segmentacao_1",
                CASE
                    WHEN A.CD_SER_DIS IN (9, 15, 30, 31, 33, 46) THEN S.DS_SER_DIS
                    ELSE 'AMBULATORIO_GERAL'
                END AS "Segmentacao_2"
            FROM DBAMV.ATENDIME A
            INNER JOIN DBAMV.PACIENTE P ON A.CD_PACIENTE = P.CD_PACIENTE
            INNER JOIN DBAMV.MULTI_EMPRESAS M ON A.CD_MULTI_EMPRESA = M.CD_MULTI_EMPRESA
            LEFT JOIN DBAMV.SER_DIS S ON A.CD_SER_DIS = S.CD_SER_DIS
            WHERE
                A.TP_ATENDIMENTO = 'A'
                AND TRUNC(A.DT_ATENDIMENTO) = TRUNC(TO_TIMESTAMP(:data,'YYYY-MM-DD HH24:MI:SS.FF3'))

            ORDER BY
                "Segmentacao_1",
                "Segmentacao_2",
                "area_pesquisa"
        """

        cursor.execute(SQL, {'data': data})

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
        if cursor and conn:
            cursor.close()
            conn.close()