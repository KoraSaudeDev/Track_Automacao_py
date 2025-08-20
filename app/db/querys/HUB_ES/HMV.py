from datetime import datetime
import logging
import pandas as pd
from app.service.calc_d1 import get_filtered_dates
from app.db import db


def DB():

    try:
        conn     = db.get_connection('HMSM')
        cursor   = conn.cursor()

        data     = get_filtered_dates()[0]

        SQL = """
            --  Hospital Meridional Vitória 

            -- Bloco 1: Pronto Socorro
            SELECT
                '40085' AS "ID_Cliente_Hfocus",
                a.hr_atendimento AS "data_atendimento",
                p.nm_paciente AS "name",
                p.email AS "email",
                (NVL(p.nr_ddi_celular, '55') || NVL(p.nr_ddd_celular, '') || NVL(p.nr_celular, '')) AS "phone",
                p.nr_cpf AS "cpf",
                PR.NM_PRESTADOR AS "medico",
                'PRONTO_SOCORRO_GERAL' AS "area_pesquisa",
                'Meridional Vitoria' AS "unidade",
                CASE 
                    WHEN s.cd_servico IN (40, 41) THEN 'PA_PEDIATRICO'
                    WHEN s.cd_servico IN (5, 82) THEN 'PA_GINECOLOGICO'
                    ELSE 'PA_ADULTO'
                END AS "setor"
            FROM
                dbamv.paciente p
            INNER JOIN dbamv.atendime a ON p.cd_paciente = a.cd_paciente
            INNER JOIN DBAMV.PRESTADOR PR ON A.CD_PRESTADOR = PR.CD_PRESTADOR 
            INNER JOIN dbamv.servico s ON a.cd_servico = s.cd_servico
            WHERE
                a.tp_atendimento = 'U'
                AND a.cd_tip_res NOT IN (6, 8)
                AND a.cd_multi_empresa = '2'
                AND TRUNC(a.dt_alta) = TRUNC(TO_TIMESTAMP(:data, 'YYYY-MM-DD HH24:MI:SS.FF3'))

            UNION ALL

            -- Bloco 2: Maternidade
            SELECT
                '40085' AS "ID_Cliente_Hfocus",
                a.hr_atendimento AS "data_atendimento",
                p.nm_paciente AS "name",
                p.email AS "email",
                (NVL(p.nr_ddi_celular, '55') || NVL(p.nr_ddd_celular, '') || NVL(p.nr_celular, '')) AS "phone",
                p.nr_cpf AS "cpf",
                PR.NM_PRESTADOR AS "medico",
                'MATERNIDADE' AS "area_pesquisa",
                'Meridional Vitoria' AS "unidade",
                'MATERNIDADE' AS "setor"
            FROM
                dbamv.paciente p
            INNER JOIN dbamv.atendime a ON p.cd_paciente = a.cd_paciente
            INNER JOIN DBAMV.PRESTADOR PR ON A.CD_PRESTADOR = PR.CD_PRESTADOR 
            INNER JOIN dbamv.atendime a2 ON a.cd_atendimento = a2.cd_atendimento_pai
            WHERE
                a.tp_atendimento = 'I'
                AND a.cd_mot_alt NOT IN (11, 12, 13, 51)
                AND a.cd_multi_empresa = '2'
                AND TRUNC(a.dt_alta) = TRUNC(TO_TIMESTAMP(:data, 'YYYY-MM-DD HH24:MI:SS.FF3'))

            UNION ALL

            -- Bloco 3: Internação Geral
            SELECT
                '40085' AS "ID_Cliente_Hfocus",
                a.hr_atendimento AS "data_atendimento",
                p.nm_paciente AS "name",
                p.email AS "email",
                (NVL(p.nr_ddi_celular, '55') || NVL(p.nr_ddd_celular, '') || NVL(p.nr_celular, '')) AS "phone",
                p.nr_cpf AS "cpf",
                PR.NM_PRESTADOR AS "medico",
                'INTERNACAO' AS "area_pesquisa",
                'Meridional Vitoria' AS "unidade",
                'INTERNACAO' AS "setor"
            FROM
                dbamv.paciente p
            INNER JOIN dbamv.atendime a ON p.cd_paciente = a.cd_paciente
            INNER JOIN DBAMV.PRESTADOR PR ON A.CD_PRESTADOR = PR.CD_PRESTADOR 
            WHERE
                a.tp_atendimento = 'I'
                AND a.cd_cid NOT IN ('O60','O80','O82','O84','O757','O800','O801','O809','O810','O820','O821','O822','O829','O839','O840','O842','Z380','Z382')
                AND a.cd_mot_alt NOT IN (11, 12, 13, 51)
                AND a.cd_multi_empresa = '2'
                AND TRUNC(a.dt_alta) = TRUNC(TO_TIMESTAMP(:data, 'YYYY-MM-DD HH24:MI:SS.FF3')) -- Corrigido de dt_atendimento para dt_alta para consistência com internação

            UNION ALL

            -- Bloco 4: Exames
            SELECT
                '40085' AS "ID_Cliente_Hfocus",
                a.hr_atendimento AS "data_atendimento",
                p.nm_paciente AS "name",
                p.email AS "email",
                (NVL(p.nr_ddi_celular, '55') || NVL(p.nr_ddd_celular, '') || NVL(p.nr_celular, '')) AS "phone",
                p.nr_cpf AS "cpf",
                PR.NM_PRESTADOR AS "medico",
                'EXAMES' AS "area_pesquisa",
                'Meridional Vitoria' AS "unidade",
                CASE
                    WHEN a.cd_ori_ate = 0 THEN 'HEMODINAMICA'
                    WHEN a.cd_ori_ate = 15 THEN 'LABORATORIO'
                END AS "setor"
            FROM
                dbamv.paciente p
            INNER JOIN dbamv.atendime a ON p.cd_paciente = a.cd_paciente
            INNER JOIN DBAMV.PRESTADOR PR ON A.CD_PRESTADOR = PR.CD_PRESTADOR 
            WHERE
                a.tp_atendimento = 'E'
                AND a.cd_ori_ate IN (0, 15)
                AND a.cd_multi_empresa = '2' -- Adicionado para consistência
                AND TRUNC(a.dt_atendimento) = TRUNC(TO_TIMESTAMP(:data, 'YYYY-MM-DD HH24:MI:SS.FF3'))

            UNION ALL

            -- Bloco 5: Ambulatório e Oncologia
            SELECT
                '40085' AS "ID_Cliente_Hfocus",
                a.hr_atendimento AS "data_atendimento",
                p.nm_paciente AS "name",
                p.email AS "email",
                (NVL(p.nr_ddi_celular, '55') || NVL(p.nr_ddd_celular, '') || NVL(p.nr_celular, '')) AS "phone",
                p.nr_cpf AS "cpf",
                PR.NM_PRESTADOR AS "medico",
                oa.ds_ori_ate AS "area_pesquisa", -- Define a área dinamicamente (Ambulatório/Oncologia)
                'Meridional Vitoria' AS "unidade",
                (SELECT -- Sub-select para definir o setor com base na especialidade
                    CASE 
                        WHEN e.cd_especialid NOT IN (9, 28, 22, 33) THEN oa.ds_ori_ate
                        WHEN e.cd_especialid = 28 AND oa.cd_ori_ate = 29 THEN oa.ds_ori_ate
                        ELSE e.ds_especialid
                    END 
                FROM dbamv.especialid e 
                WHERE e.cd_especialid = a.cd_especialid
                ) AS "setor"
            FROM
                dbamv.paciente p
            INNER JOIN dbamv.atendime a ON p.cd_paciente = a.cd_paciente
            INNER JOIN DBAMV.PRESTADOR PR ON A.CD_PRESTADOR = PR.CD_PRESTADOR 
            INNER JOIN dbamv.ori_ate oa ON oa.cd_ori_ate = a.cd_ori_ate
            WHERE
                oa.tp_origem = 'A'
                AND oa.cd_multi_empresa = 2
                AND oa.cd_ori_ate IN (30, 29) -- 30=AMBULATORIO, 29=ONCOLOGIA
                AND TRUNC(a.dt_atendimento) = TRUNC(TO_TIMESTAMP(:data, 'YYYY-MM-DD HH24:MI:SS.FF3'))
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
