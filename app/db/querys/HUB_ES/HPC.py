from datetime import datetime
import logging
import pandas as pd
from app.service.calc_d1 import get_filtered_dates
from app.db import db


def DB():

    try:
        conn     = db.get_connection('HPC')
        cursor   = conn.cursor()

        data     = get_filtered_dates()[0]
        #data     = '2024-05-10 18:11:00.000'
        #data     = '2013-04-29 00:00:00.000'
        SQL = """
            -- Hospital Meridional Praia da Costa

            -- Bloco 1: Pronto Socorro
            SELECT
                '40085' AS "ID_Cliente_Hfocus", a.hr_atendimento AS "data_atendimento", p.nm_paciente AS "name",
                p.email AS "email", (NVL(p.nr_ddi_celular, '55') || NVL(p.nr_ddd_celular, '') || NVL(p.nr_celular, '')) AS "phone",
                p.nr_cpf AS "cpf", 'PRONTO_SOCORRO_GERAL' AS "area_pesquisa", 'Meridional Praia Da Costa' AS "unidade",
                CASE WHEN a.cd_servico IN (3) THEN 'PA_PEDIATRICO' WHEN a.cd_servico IN (2) THEN 'PA_OBSTETRICO' ELSE 'PA_ADULTO' END AS "setor"
            FROM dbamv.paciente p
            INNER JOIN dbamv.atendime a ON p.cd_paciente = a.cd_paciente
            WHERE a.tp_atendimento = 'U' AND a.cd_tip_res NOT IN (6, 17, 20) AND a.cd_servico IN (4, 7, 3, 2) AND TRUNC(a.dt_alta) = TRUNC(TO_TIMESTAMP(:data,'YYYY-MM-DD HH24:MI:SS.FF3'))

            UNION ALL

            -- Bloco 2: Maternidade
            SELECT
                '40085', a.hr_atendimento, p.nm_paciente, p.email AS "email",
                (NVL(p.nr_ddi_celular, '55') || NVL(p.nr_ddd_celular, '') || NVL(p.nr_celular, '')),
                p.nr_cpf, 'MATERNIDADE', 'Meridional Praia Da Costa', 'MATERNIDADE'
            FROM dbamv.paciente p
            INNER JOIN dbamv.atendime a ON p.cd_paciente = a.cd_paciente
            INNER JOIN dbamv.atendime a2 ON a.cd_atendimento = a2.cd_atendimento_pai
            WHERE a.tp_atendimento = 'I' AND a.cd_mot_alt NOT IN (24, 25, 36) AND TRUNC(a.dt_alta) = TRUNC(TO_TIMESTAMP(:data,'YYYY-MM-DD HH24:MI:SS.FF3'))

            UNION ALL

            -- Bloco 3: Internação Geral
            SELECT
                '40085', a.hr_atendimento, p.nm_paciente, p.email AS "email",
                (NVL(p.nr_ddi_celular, '55') || NVL(p.nr_ddd_celular, '') || NVL(p.nr_celular, '')),
                p.nr_cpf, 'INTERNACAO', 'Meridional Praia Da Costa', 'INTERNACAO'
            FROM dbamv.paciente p
            INNER JOIN dbamv.atendime a ON p.cd_paciente = a.cd_paciente
            WHERE a.tp_atendimento = 'I'
            AND a.cd_cid NOT IN ('O60','O80','O82','O84','O757','O800','O801','O809','O810','O820','O821','O822','O829','O839','O840','O842','Z380','Z382')
            AND a.cd_mot_alt NOT IN (24, 25, 36) AND TRUNC(a.dt_alta) = TRUNC(TO_TIMESTAMP(:data,'YYYY-MM-DD HH24:MI:SS.FF3'))

            UNION ALL

            -- Bloco 4: Hospital Dia e Ambulatório
            SELECT
                '40085', a.hr_atendimento, p.nm_paciente, p.email AS "email",
                (NVL(p.nr_ddi_celular, '55') || NVL(p.nr_ddd_celular, '') || NVL(p.nr_celular, '')),
                p.nr_cpf, 'HOSPITAL_DIA', 'Meridional Praia Da Costa', 'INTERNACAO'
            FROM dbamv.paciente p
            INNER JOIN dbamv.atendime a ON p.cd_paciente = a.cd_paciente
            WHERE a.tp_atendimento = 'E' AND a.cd_ori_ate = 22 AND TRUNC(a.dt_atendimento) = TRUNC(TO_TIMESTAMP(:data,'YYYY-MM-DD HH24:MI:SS.FF3'))

            UNION ALL

            SELECT
                '40085', a.hr_atendimento, p.nm_paciente, p.email AS "email",
                (NVL(p.nr_ddi_celular, '55') || NVL(p.nr_ddd_celular, '') || NVL(p.nr_celular, '')),
                p.nr_cpf, 'AMBULATORIO', 'Meridional Praia Da Costa',
                CASE WHEN a.cd_ser_dis IN (6, 14, 17, 20) THEN s.ds_ser_dis ELSE 'GERAL_AMBULATORIO' END
            FROM dbamv.paciente p
            INNER JOIN dbamv.atendime a ON p.cd_paciente = a.cd_paciente
            INNER JOIN dbamv.ser_dis s ON a.cd_ser_dis = s.cd_ser_dis
            WHERE a.tp_atendimento = 'A' AND a.cd_ori_ate <> 1 AND a.cd_ser_dis NOT IN (32, 40) AND TRUNC(a.dt_atendimento) = TRUNC(TO_TIMESTAMP(:data,'YYYY-MM-DD HH24:MI:SS.FF3'))

            UNION ALL

            -- Bloco 5: Exames
            SELECT
                '40085', a.hr_atendimento, p.nm_paciente, p.email AS "email",
                (NVL(p.nr_ddi_celular, '55') || NVL(p.nr_ddd_celular, '') || NVL(p.nr_celular, '')),
                p.nr_cpf, 'EXAMES', 'Meridional Praia Da Costa',
                CASE WHEN a.cd_ori_ate IN (2, 15) THEN 'IMAGEM' WHEN a.cd_ori_ate = 20 THEN 'LABORATORIO' END
            FROM dbamv.paciente p
            INNER JOIN dbamv.atendime a ON p.cd_paciente = a.cd_paciente
            WHERE a.tp_atendimento = 'E' AND a.cd_ori_ate IN (2, 15, 20) AND TRUNC(a.dt_atendimento) = TRUNC(TO_TIMESTAMP(:data,'YYYY-MM-DD HH24:MI:SS.FF3'))

            UNION ALL

            -- Bloco 6: Oncologia
            SELECT
                '40085', a.hr_atendimento, p.nm_paciente, p.email AS "email",
                (NVL(p.nr_ddi_celular, '55') || NVL(p.nr_ddd_celular, '') || NVL(p.nr_celular, '')),
                p.nr_cpf, 'ONCOLOGIA', 'Meridional Praia Da Costa', 'ONCOLOGIA'
            FROM dbamv.paciente p
            INNER JOIN dbamv.atendime a ON p.cd_paciente = a.cd_paciente
            WHERE a.tp_atendimento = 'A' AND a.cd_ori_ate = 1 AND TRUNC(a.dt_atendimento) = TRUNC(TO_TIMESTAMP(:data,'YYYY-MM-DD HH24:MI:SS.FF3'))
        """
        cursor.execute(SQL, {'data': data})

        rows      = cursor.fetchall()
        columns   = [desc[0] for desc in cursor.description]
        df        = pd.DataFrame(rows, columns=columns)
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
