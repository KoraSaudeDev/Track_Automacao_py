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
        conn     = db.get_connection("OTO_ING")
        cursor   = conn.cursor()

        data     = get_filtered_dates()[0]
        SQL = """
            -- Bloco 1: Pacientes do Pronto Socorro (Urgência)
            SELECT
                '40085' AS "ID_CLIENTE_HFOCUS",
                A.HR_ATENDIMENTO AS "data_atendimento",
                A.HR_ALTA AS "data_saida_alta",
                A.CD_ATENDIMENTO AS "cd_atendimento",
                P.NM_PACIENTE AS "name",
                PR.NM_PRESTADOR AS "medico",
                P.EMAIL AS "email",
                (NVL(P.NR_DDI_CELULAR, '55') || NVL(P.NR_DDD_CELULAR, '') || NVL(P.NR_CELULAR, '')) AS "phone",
                P.NR_CPF AS "cpf",
                'PRONTO SOCORRO GERAL' AS "area_pesquisa",
				CASE
			        WHEN M.CD_MULTI_EMPRESA IN (8, 19, 23, 25) THEN 'Hospital Oto Santos Dumont'
			        WHEN M.CD_MULTI_EMPRESA IN (1, 2, 3, 6, 7, 12, 13, 16, 26) THEN 'Hospital Oto Aldeota'
			        WHEN M.CD_MULTI_EMPRESA IN (18) THEN 'Hospital Oto Meireles'
			        WHEN M.CD_MULTI_EMPRESA IN (10, 11) THEN 'Hospital Oto Sul'
			        WHEN M.CD_MULTI_EMPRESA IN (20, 21, 22) THEN 'Instituto De Neurologia De Goiania'
			        ELSE M.DS_RAZAO_SOCIAL
			    END AS "unidade",
                CASE 
                    WHEN A.CD_SERVICO = 5 THEN 'PA_OBSTÉTRICO'
                    WHEN A.CD_SERVICO = 40 THEN 'PA_PEDIATRICO'
                    ELSE 'PA_ADULTO'
                END AS "setor"
            FROM DBAMV.ATENDIME A
            INNER JOIN DBAMV.PACIENTE P ON A.CD_PACIENTE = P.CD_PACIENTE
            INNER JOIN DBAMV.MULTI_EMPRESAS M ON A.CD_MULTI_EMPRESA = M.CD_MULTI_EMPRESA
            INNER JOIN DBAMV.PRESTADOR PR ON A.CD_PRESTADOR = PR.CD_PRESTADOR 
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
                A.HR_ATENDIMENTO AS "data_atendimento",
                A.HR_ALTA AS "data_saida_alta",
                A.CD_ATENDIMENTO AS "cd_atendimento",
                P.NM_PACIENTE AS "name",
                PR.NM_PRESTADOR AS "medico",
                P.EMAIL AS "email",
                (NVL(P.NR_DDI_CELULAR, '55') || NVL(P.NR_DDD_CELULAR, '') || NVL(P.NR_CELULAR, '')) AS "phone",
                P.NR_CPF AS "cpf",
                CASE
                    WHEN A2.CD_ATENDIMENTO_PAI IS NOT NULL THEN 'MATERNIDADE'
                    ELSE 'INTERNACAO'
                END AS "area_pesquisa",
				CASE
			        WHEN M.CD_MULTI_EMPRESA IN (8, 19, 23, 25) THEN 'Hospital Oto Santos Dumont'
			        WHEN M.CD_MULTI_EMPRESA IN (1, 2, 3, 6, 7, 12, 13, 16, 26) THEN 'Hospital Oto Aldeota'
			        WHEN M.CD_MULTI_EMPRESA IN (18) THEN 'Hospital Oto Meireles'
			        WHEN M.CD_MULTI_EMPRESA IN (10, 11) THEN 'Hospital Oto Sul'
			        WHEN M.CD_MULTI_EMPRESA IN (20, 21, 22) THEN 'Instituto De Neurologia De Goiania'
			        ELSE M.DS_RAZAO_SOCIAL
			    END AS "unidade",
                CASE
                    WHEN A2.CD_ATENDIMENTO_PAI IS NOT NULL THEN 'MATERNIDADE'
                    ELSE 'INTERNACAO'
                END AS "setor"
            FROM DBAMV.ATENDIME A
            INNER JOIN DBAMV.PACIENTE P ON A.CD_PACIENTE = P.CD_PACIENTE
            INNER JOIN DBAMV.MULTI_EMPRESAS M ON A.CD_MULTI_EMPRESA = M.CD_MULTI_EMPRESA
            INNER JOIN DBAMV.PRESTADOR PR ON A.CD_PRESTADOR = PR.CD_PRESTADOR
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
                A.HR_ATENDIMENTO AS "data_atendimento",
                A.HR_ALTA AS "data_saida_alta",
                A.CD_ATENDIMENTO AS "cd_atendimento",
                P.NM_PACIENTE AS "name",
                PR.NM_PRESTADOR AS "medico",
                P.EMAIL AS "email",
                (NVL(P.NR_DDI_CELULAR, '55') || NVL(P.NR_DDD_CELULAR, '') || NVL(P.NR_CELULAR, '')) AS "phone",
                P.NR_CPF AS "cpf",
                'EXAMES' AS "area_pesquisa",
				CASE
			        WHEN M.CD_MULTI_EMPRESA IN (8, 19, 23, 25) THEN 'Hospital Oto Santos Dumont'
			        WHEN M.CD_MULTI_EMPRESA IN (1, 2, 3, 6, 7, 12, 13, 16, 26) THEN 'Hospital Oto Aldeota'
			        WHEN M.CD_MULTI_EMPRESA IN (18) THEN 'Hospital Oto Meireles'
			        WHEN M.CD_MULTI_EMPRESA IN (10, 11) THEN 'Hospital Oto Sul'
			        WHEN M.CD_MULTI_EMPRESA IN (20, 21, 22) THEN 'Instituto De Neurologia De Goiania'
			        ELSE M.DS_RAZAO_SOCIAL
			    END AS "unidade",
                CASE
                    WHEN A.CD_ORI_ATE = 103 THEN 'HEMODINAMICA'
                    WHEN A.CD_ORI_ATE IN (47, 22, 104, 106, 109, 19, 38, 121, 123, 21) THEN 'IMAGEM'
                    WHEN A.CD_ORI_ATE IN (13,14,16,37,35,50,88,112,125,126) THEN 'LABORATORIO'
                    WHEN A.CD_ORI_ATE IN (29, 110, 100) THEN 'ENDOSCOPIA'
                END AS "setor"
            FROM DBAMV.ATENDIME A
            INNER JOIN DBAMV.PACIENTE P ON A.CD_PACIENTE = P.CD_PACIENTE
            INNER JOIN DBAMV.MULTI_EMPRESAS M ON A.CD_MULTI_EMPRESA = M.CD_MULTI_EMPRESA
            LEFT JOIN DBAMV.PRESTADOR PR ON A.CD_PRESTADOR = PR.CD_PRESTADOR            
			WHERE
			    A.TP_ATENDIMENTO = 'E'
			    AND A.CD_ORI_ATE IN (
			        -- HEMODINAMICA
			        103,
			        -- IMAGEM
			        19, 21, 22, 38, 47, 104, 106, 109, 121, 123,
			        -- LABORATORIO
			        13, 14, 16, 35, 37, 50, 88, 112, 125, 126,
			        -- ENDOSCOPIA
			        29, 100, 110
			    )
                AND TRUNC(A.DT_ATENDIMENTO) = TRUNC(TO_TIMESTAMP(:data,'YYYY-MM-DD HH24:MI:SS.FF3'))

            UNION ALL

            -- Bloco 4: Pacientes de Ambulatório (Agrupados)
            SELECT
                '40085' AS "ID_CLIENTE_HFOCUS",
                A.HR_ATENDIMENTO AS "data_atendimento",
                A.HR_ALTA AS "data_saida_alta",
                A.CD_ATENDIMENTO AS "cd_atendimento",
                P.NM_PACIENTE AS "name",
                PR.NM_PRESTADOR AS "medico",
                P.EMAIL AS "email",
                (NVL(P.NR_DDI_CELULAR, '55') || NVL(P.NR_DDD_CELULAR, '') || NVL(P.NR_CELULAR, '')) AS "phone",
                P.NR_CPF AS "cpf",
                'AMBULATORIO' AS "area_pesquisa",
				CASE
			        WHEN M.CD_MULTI_EMPRESA IN (8, 19, 23, 25) THEN 'Hospital Oto Santos Dumont'
			        WHEN M.CD_MULTI_EMPRESA IN (1, 2, 3, 6, 7, 12, 13, 16, 26) THEN 'Hospital Oto Aldeota'
			        WHEN M.CD_MULTI_EMPRESA IN (18) THEN 'Hospital Oto Meireles'
			        WHEN M.CD_MULTI_EMPRESA IN (10, 11) THEN 'Hospital Oto Sul'
			        WHEN M.CD_MULTI_EMPRESA IN (20, 21, 22) THEN 'Instituto De Neurologia De Goiania'
			        ELSE M.DS_RAZAO_SOCIAL
			    END AS "unidade",
                CASE
                    WHEN A.CD_SER_DIS IN (9, 15, 30, 31, 33, 46) THEN S.DS_SER_DIS
                    ELSE 'AMBULATORIO_GERAL'
                END AS "setor"
            FROM DBAMV.ATENDIME A
            INNER JOIN DBAMV.PACIENTE P ON A.CD_PACIENTE = P.CD_PACIENTE
            INNER JOIN DBAMV.MULTI_EMPRESAS M ON A.CD_MULTI_EMPRESA = M.CD_MULTI_EMPRESA
            INNER JOIN DBAMV.PRESTADOR PR ON A.CD_PRESTADOR = PR.CD_PRESTADOR
            LEFT JOIN DBAMV.SER_DIS S ON A.CD_SER_DIS = S.CD_SER_DIS
            WHERE
                A.TP_ATENDIMENTO = 'A'
                AND TRUNC(A.DT_ATENDIMENTO) = TRUNC(TO_TIMESTAMP(:data,'YYYY-MM-DD HH24:MI:SS.FF3'))

            ORDER BY
                "unidade",
                "setor",
                "area_pesquisa"
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
        if cursor:
            cursor.close()
        if conn:
            conn.close()