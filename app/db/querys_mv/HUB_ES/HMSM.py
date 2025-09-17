from datetime import datetime
import logging
import pandas as pd
from app.service.calc_d1 import get_filtered_dates
from app.db import db


def DB():
    cursor = None
    conn   = None
    try:
        conn     = db.get_connection('HMSM')
        cursor   = conn.cursor()

        data     = get_filtered_dates()[0]

        SQL = """
            -- Hospital Meridional São Mateus (HMSM)

            -- Bloco 1: Pronto Socorro
            SELECT
                '40085' AS "ID_Cliente_Hfocus", a.hr_atendimento AS "data_atendimento",A.HR_ALTA AS "data_saida_alta",A.CD_ATENDIMENTO AS "cd_atendimento", p.nm_paciente AS "name",PR.NM_PRESTADOR AS "medico",
                p.email AS "email", (NVL(p.nr_ddi_celular, '55') || NVL(p.nr_ddd_celular, '') || NVL(p.nr_celular, '')) AS "phone",
                p.nr_cpf AS "cpf", 'PRONTO SOCORRO GERAL' AS "area_pesquisa", 'Hospital São Mateus' AS "unidade",
                CASE WHEN a.cd_servico = 40 THEN 'PA_PEDIATRICO' ELSE 'PA_ADULTO' END AS "setor"
            FROM dbamv.paciente p
            INNER JOIN dbamv.atendime a ON p.cd_paciente = a.cd_paciente
            INNER JOIN DBAMV.PRESTADOR PR ON A.CD_PRESTADOR = PR.CD_PRESTADOR 
            WHERE a.tp_atendimento = 'U' AND a.cd_tip_res NOT IN (6, 8) AND a.cd_servico IN (3, 23, 37, 40) AND a.cd_multi_empresa = '1' AND TRUNC(a.dt_alta) = TRUNC(TO_TIMESTAMP(:data, 'YYYY-MM-DD HH24:MI:SS.FF3'))
    		AND TRUNC(a.hr_atendimento) <= TRUNC(TO_TIMESTAMP(:data,'YYYY-MM-DD HH24:MI:SS.FF3'))	
            AND (
	      			a.HR_ALTA IS NULL
		      		OR TRUNC(a.HR_ALTA) <= TRUNC(TO_TIMESTAMP(:data,'YYYY-MM-DD HH24:MI:SS.FF3'))
				)
            UNION ALL

            -- Bloco 2: Maternidade
            SELECT
                '40085', a.hr_atendimento AS "data_atendimento",A.HR_ALTA AS "data_saida_alta",A.CD_ATENDIMENTO AS "cd_atendimento", p.nm_paciente  AS "name", p.email AS "email",PR.NM_PRESTADOR AS "medico",
                (NVL(p.nr_ddi_celular, '55') || NVL(p.nr_ddd_celular, '') || NVL(p.nr_celular, '')) AS "unidade",
                p.nr_cpf AS "cpf", 'MATERNIDADE' AS "area_pesquisa", 'Hospital São Mateus' AS "unidade", 'MATERNIDADE' AS "setor"
            FROM dbamv.paciente p
            INNER JOIN dbamv.atendime a ON p.cd_paciente = a.cd_paciente
            INNER JOIN DBAMV.PRESTADOR PR ON A.CD_PRESTADOR = PR.CD_PRESTADOR 
            INNER JOIN dbamv.atendime a2 ON a.cd_atendimento = a2.cd_atendimento_pai
            WHERE a.tp_atendimento = 'I' AND a.cd_mot_alt NOT IN (11, 12, 13, 51) AND a.cd_multi_empresa = '1' AND TRUNC(a.dt_alta) = TRUNC(TO_TIMESTAMP(:data, 'YYYY-MM-DD HH24:MI:SS.FF3'))
    		AND TRUNC(a.hr_atendimento) <= TRUNC(TO_TIMESTAMP(:data,'YYYY-MM-DD HH24:MI:SS.FF3'))		
            AND (
	      			a.HR_ALTA IS NULL
		      		OR TRUNC(a.HR_ALTA) <= TRUNC(TO_TIMESTAMP(:data,'YYYY-MM-DD HH24:MI:SS.FF3'))
				)
            UNION ALL

            -- Bloco 3: Internação Geral
            SELECT
                '40085', a.hr_atendimento  AS "data_atendimento",A.HR_ALTA AS "data_saida_alta",A.CD_ATENDIMENTO AS "cd_atendimento", p.nm_paciente AS "name", p.email AS "email",PR.NM_PRESTADOR AS "medico",
                (NVL(p.nr_ddi_celular, '55') || NVL(p.nr_ddd_celular, '') || NVL(p.nr_celular, '')) AS "phone",
                p.nr_cpf AS "cpf", 'INTERNACAO'AS "area_pesquisa", 'Hospital São Mateus' AS "unidade" , 'INTERNACAO' AS "setor"
            FROM dbamv.paciente p
            INNER JOIN dbamv.atendime a ON p.cd_paciente = a.cd_paciente
            INNER JOIN DBAMV.PRESTADOR PR ON A.CD_PRESTADOR = PR.CD_PRESTADOR 
            WHERE a.tp_atendimento = 'I'
            AND a.cd_cid NOT IN ('O60','O80','O82','O84','O757','O800','O801','O809','O810','O820','O821','O822','O829','O839','O840','O842','Z380','Z382')
            AND a.cd_mot_alt NOT IN (11, 12, 13, 51) AND a.cd_multi_empresa = '1' AND TRUNC(a.dt_alta) = TRUNC(TO_TIMESTAMP(:data, 'YYYY-MM-DD HH24:MI:SS.FF3'))
    		AND TRUNC(a.hr_atendimento) <= TRUNC(TO_TIMESTAMP(:data,'YYYY-MM-DD HH24:MI:SS.FF3'))		
            AND (
	      			a.HR_ALTA IS NULL
		      		OR TRUNC(a.HR_ALTA) <= TRUNC(TO_TIMESTAMP(:data,'YYYY-MM-DD HH24:MI:SS.FF3'))
				)
            UNION ALL

            -- Bloco 4: Hospital Dia e Ambulatório
            SELECT
                '40085', a.hr_atendimento  AS "data_atendimento",A.HR_ALTA AS "data_saida_alta",A.CD_ATENDIMENTO AS "cd_atendimento", p.nm_paciente AS "name", p.email AS "email",PR.NM_PRESTADOR AS "medico",
                (NVL(p.nr_ddi_celular, '55') || NVL(p.nr_ddd_celular, '') || NVL(p.nr_celular, '')) AS "phone",
                p.nr_cpf AS "cpf", 'INTERNACAO'AS "area_pesquisa", 'Hospital São Mateus' AS "unidade" , 'INTERNACAO' AS "setor"
            FROM dbamv.paciente p
            INNER JOIN dbamv.atendime a ON p.cd_paciente = a.cd_paciente
            INNER JOIN DBAMV.PRESTADOR PR ON A.CD_PRESTADOR = PR.CD_PRESTADOR 
            WHERE a.tp_atendimento = 'E' AND a.cd_ori_ate = 7 AND a.cd_multi_empresa = '1' AND TRUNC(a.dt_atendimento) = TRUNC(TO_TIMESTAMP(:data, 'YYYY-MM-DD HH24:MI:SS.FF3'))
    		AND TRUNC(a.hr_atendimento) <= TRUNC(TO_TIMESTAMP(:data,'YYYY-MM-DD HH24:MI:SS.FF3'))		
            AND (
	      			a.HR_ALTA IS NULL
		      		OR TRUNC(a.HR_ALTA) <= TRUNC(TO_TIMESTAMP(:data,'YYYY-MM-DD HH24:MI:SS.FF3'))
				)
            UNION ALL

            SELECT
                '40085', a.hr_atendimento AS "data_atendimento",A.HR_ALTA AS "data_saida_alta",A.CD_ATENDIMENTO AS "cd_atendimento", p.nm_paciente AS "name", p.email AS "email",PR.NM_PRESTADOR AS "medico",
                (NVL(p.nr_ddi_celular, '55') || NVL(p.nr_ddd_celular, '') || NVL(p.nr_celular, '')) AS "phone",
                p.nr_cpf AS "cpf", 'AMBULATORIO' AS "area_pesquisa", 'Hospital São Mateus' AS "unidade",
                CASE WHEN s.cd_ser_dis IN (9, 22, 33, 34, 46, 62) THEN s.ds_ser_dis ELSE 'GERAL_AMBULATORIO' END AS "setor"
            FROM dbamv.paciente p
            INNER JOIN dbamv.atendime a ON p.cd_paciente = a.cd_paciente
            INNER JOIN dbamv.ser_dis s ON a.cd_ser_dis = s.cd_ser_dis
            INNER JOIN DBAMV.PRESTADOR PR ON A.CD_PRESTADOR = PR.CD_PRESTADOR 
            WHERE a.tp_atendimento = 'A' AND a.cd_ori_ate <> 6 AND s.cd_ser_dis NOT IN (17, 18, 32) AND a.cd_multi_empresa = '1' AND TRUNC(a.dt_atendimento) = TRUNC(TO_TIMESTAMP(:data, 'YYYY-MM-DD HH24:MI:SS.FF3'))
    		AND TRUNC(a.hr_atendimento) <= TRUNC(TO_TIMESTAMP(:data,'YYYY-MM-DD HH24:MI:SS.FF3'))		
            AND (
	      			a.HR_ALTA IS NULL
		      		OR TRUNC(a.HR_ALTA) <= TRUNC(TO_TIMESTAMP(:data,'YYYY-MM-DD HH24:MI:SS.FF3'))
				)
            UNION ALL

            -- Bloco 5: Exames
            SELECT
                '40085', a.hr_atendimento AS "data_atendimento",A.HR_ALTA AS "data_saida_alta",A.CD_ATENDIMENTO AS "cd_atendimento", p.nm_paciente AS "name", p.email AS "email",PR.NM_PRESTADOR AS "medico",
                (NVL(p.nr_ddi_celular, '55') || NVL(p.nr_ddd_celular, '') || NVL(p.nr_celular, '')) AS "phone",
                p.nr_cpf AS "cpf", 'EXAMES' AS "area_pesquisa", 'Hospital São Mateus' AS "unidade",
                CASE WHEN a.cd_ori_ate = 10 THEN 'HEMODINAMICA' WHEN a.cd_ori_ate = 5 THEN 'IMAGEM' WHEN a.cd_ori_ate = 4 THEN 'LABORATORIO' END AS "setor"
            FROM dbamv.paciente p
            INNER JOIN dbamv.atendime a ON p.cd_paciente = a.cd_paciente
            INNER JOIN DBAMV.PRESTADOR PR ON A.CD_PRESTADOR = PR.CD_PRESTADOR 
            WHERE a.tp_atendimento = 'E' AND a.cd_ori_ate IN (10, 5, 4) AND a.cd_multi_empresa = '1' AND TRUNC(a.dt_atendimento) = TRUNC(TO_TIMESTAMP(:data, 'YYYY-MM-DD HH24:MI:SS.FF3'))
    		AND TRUNC(a.hr_atendimento) <= TRUNC(TO_TIMESTAMP(:data,'YYYY-MM-DD HH24:MI:SS.FF3'))		
            AND (
	      			a.HR_ALTA IS NULL
		      		OR TRUNC(a.HR_ALTA) <= TRUNC(TO_TIMESTAMP(:data,'YYYY-MM-DD HH24:MI:SS.FF3'))
				)
            UNION ALL

            -- Bloco 6: Oncologia
            SELECT
                '40085', a.hr_atendimento AS "data_atendimento",A.HR_ALTA AS "data_saida_alta",A.CD_ATENDIMENTO AS "cd_atendimento", p.nm_paciente AS "name", p.email AS "email",PR.NM_PRESTADOR AS "medico",
                (NVL(p.nr_ddi_celular, '55') || NVL(p.nr_ddd_celular, '') || NVL(p.nr_celular, '')) AS "phone",
                p.nr_cpf AS "cpf", 'ONCOLOGIA' AS "area_pesquisa", 'Hospital São Mateus' AS "unidade", 'ONCOLOGIA' AS "setor"
            FROM dbamv.paciente p
            INNER JOIN dbamv.atendime a ON p.cd_paciente = a.cd_paciente
            INNER JOIN DBAMV.PRESTADOR PR ON A.CD_PRESTADOR = PR.CD_PRESTADOR 
            WHERE a.tp_atendimento = 'A' AND a.cd_ori_ate = 6 AND a.cd_multi_empresa = '1' AND TRUNC(a.dt_atendimento) = TRUNC(TO_TIMESTAMP(:data, 'YYYY-MM-DD HH24:MI:SS.FF3'))
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
        datas_saida = pd.to_datetime(df["data_saida_alta"], errors="coerce")
        df["data_saida_alta"] = datas_saida.apply(lambda x: x.strftime("%Y-%m-%d %H:%M:%S") if not pd.isna(x) else None)
        datas_aten = pd.to_datetime(df["data_atendimento"], errors="coerce")
        df["data_atendimento"] = datas_aten.apply(lambda x: x.strftime("%Y-%m-%d %H:%M:%S") if not pd.isna(x) else None)
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
