from datetime import datetime
import logging
import pandas as pd
from app.service.calc_d1 import get_filtered_dates
from app.db import db


def DB():

    try:
        conn     = db.get_connection('HMV')
        cursor   = conn.cursor()

        data     = get_filtered_dates()[0]
        #data     = '2024-05-10 18:11:00.000'
        #data     = '2013-04-29 00:00:00.000'
        SQL = """
            SELECT
            '40085' AS "ID_Cliente_Hfocus",
            a.hr_atendimento AS "Data_Base",
            p.nm_paciente AS "Nome_Completo_Paciente",
            p.email AS "E-mail",
            p.nr_fone AS "Telefone_Residencial",
            p.nr_celular AS "Telefone_Celular",
            p.nr_cpf AS "CPF",
            'PRONTO_SOCORRO_GERAL' AS "Area_Pesquisa",
            'Meridional Vitória' AS "Segmentacao_1",
            CASE
                WHEN s.cd_servico IN (3, 4, 15, 23, 37, 38) THEN 'PA_ADULTO'
                WHEN s.cd_servico IN (40, 41) THEN 'PA_PEDIATRICO'
                WHEN s.cd_servico IN (5, 82) THEN 'PA_GINECOLOGICO'
            END AS "Segmentacao_2"
        FROM
            dbamv.paciente p
        JOIN
            dbamv.atendime a ON p.cd_paciente = a.cd_paciente
        JOIN
            dbamv.servico s ON a.cd_servico = s.cd_servico
        WHERE
            a.tp_atendimento = 'U'
            AND a.cd_tip_res NOT IN (6, 8)
            AND a.cd_multi_empresa = '2'
            AND s.cd_servico IN (3, 4, 15, 23, 37, 38, 40, 41, 5, 82)
            AND TRUNC(a.dt_alta) = TRUNC(TO_TIMESTAMP(:data,'YYYY-MM-DD HH24:MI:SS.FF3'))

        UNION ALL

        SELECT
            '40085' AS "ID_Cliente_Hfocus",
            CASE
                WHEN a.dt_atendimento IS NOT NULL AND a.hr_atendimento IS NOT NULL THEN TO_CHAR(a.dt_atendimento, 'dd/mm/yyyy') || ' ' || TO_CHAR(a.hr_atendimento, 'hh24:mi:ss')
                ELSE a.hr_atendimento
            END AS "Data_Base",
            p.nm_paciente AS "Nome_Completo_Paciente",
            p.email AS "E-mail",
            p.nr_fone AS "Telefone_Residencial",
            p.nr_celular AS "Telefone_Celular",
            p.nr_cpf AS "CPF",
            'MATERNIDADE' AS "Area_Pesquisa",
            'Meridional Vitória' AS "Segmentacao_1",
            'MATERNIDADE' AS "Segmentacao_2"
        FROM
            dbamv.paciente p
        JOIN
            dbamv.atendime a ON p.cd_paciente = a.cd_paciente
        JOIN
            dbamv.atendime a2 ON a.CD_ATENDIMENTO = a2.CD_ATENDIMENTO_PAI
        WHERE
            a.tp_atendimento = 'I'
            AND a.cd_mot_alt NOT IN ('11', '12', '13', '51')
            AND a.cd_multi_empresa = '2'
            AND TRUNC(a.dt_alta) = TRUNC(TO_TIMESTAMP(:data,'YYYY-MM-DD HH24:MI:SS.FF3'))

        UNION ALL

        SELECT
            '40085' AS "ID_Cliente_Hfocus",
            a.hr_atendimento AS "Data_Base",
            p.nm_paciente AS "Nome_Completo_Paciente",
            p.email AS "E-mail",
            p.nr_fone AS "Telefone_Residencial",
            p.nr_celular AS "Telefone_Celular",
            p.nr_cpf AS "CPF",
            'INTERNACAO' AS "Area_Pesquisa",
            'Meridional Vitória' AS "Segmentacao_1",
            'INTERNACAO' AS "Segmentacao_2"
        FROM
            dbamv.paciente p
        JOIN
            dbamv.atendime a ON p.cd_paciente = a.cd_paciente
        WHERE
            a.tp_atendimento = 'I'
            AND a.CD_CID NOT IN ('O60', 'O80', 'O82', 'O84', 'O757', 'O800', 'O801', 'O809', 'O810', 'O820', 'O821', 'O822', 'O829', 'O839', 'O840', 'O842', 'Z380', 'Z382')
            AND a.cd_mot_alt NOT IN ('11', '12', '13', '51')
            AND a.cd_multi_empresa = '2'
            AND TRUNC(a.dt_atendimento) = TRUNC(TO_TIMESTAMP(:data,'YYYY-MM-DD HH24:MI:SS.FF3'))

        UNION ALL

        SELECT
            '40085' AS "ID_Cliente_Hfocus",
            a.hr_atendimento AS "Data_Base",
            p.nm_paciente AS "Nome_Completo_Paciente",
            p.email AS "E-mail",
            p.nr_fone AS "Telefone_Residencial",
            p.nr_celular AS "Telefone_Celular",
            p.nr_cpf AS "CPF",
            'EXAMES' AS "Area_Pesquisa",
            'Meridional Vitória' AS "Segmentacao_1",
            CASE
                WHEN a.cd_ori_ate = 0 THEN 'HEMODINAMICA'
                WHEN a.cd_ori_ate = 15 THEN 'LABORATORIO'
            END AS "Segmentacao_2"
        FROM
            dbamv.paciente p
        JOIN
            dbamv.atendime a ON p.cd_paciente = a.cd_paciente
        WHERE
            a.tp_atendimento = 'E'
            AND a.cd_ori_ate IN (0, 15)
            AND TRUNC(a.dt_atendimento) = TRUNC(TO_TIMESTAMP(:data,'YYYY-MM-DD HH24:MI:SS.FF3'))
            
        UNION ALL

        SELECT
            '40085' AS ID_CLIENTE_HFOCUS,
            A.HR_ATENDIMENTO AS DATA_BASE,
            P.NM_PACIENTE AS NOME_COMPLETO_PACIENTE,
            P.EMAIL AS EMAIL,
            P.NR_FONE AS TELEFONE_RESIDENCIAL,
            P.NR_CELULAR AS TELEFONE_CELULAR,
            P.NR_CPF AS CPF,
            OA.DS_ORI_ATE AS AREA_PESQUISA,
            'Meridional Vitória' AS SEGMENTACAO_1,
            CASE
                WHEN e.CD_ESPECIALID IN (9, 28, 22, 33) AND e.CD_ESPECIALID <> 28 THEN e.DS_ESPECIALID
                WHEN e.CD_ESPECIALID = 28 AND OA.CD_ORI_ATE = 29 THEN OA.DS_ORI_ATE
                ELSE OA.DS_ORI_ATE
            END AS SEGMENTACAO_2
        FROM
            dbamv.paciente p
        JOIN
            dbamv.atendime a ON p.cd_paciente = a.cd_paciente
        JOIN
            dbamv.ori_ate oa ON oa.CD_ORI_ATE = a.CD_ORI_ATE
        LEFT JOIN
            dbamv.especialid e ON e.CD_ESPECIALID = a.CD_ESPECIALID
        WHERE
            oa.CD_ORI_ATE IN (30, 29)
            AND oa.TP_ORIGEM = 'A'
            AND oa.CD_MULTI_EMPRESA = 2
            AND TRUNC(a.DT_ATENDIMENTO) = TRUNC(TO_TIMESTAMP(:data,'YYYY-MM-DD HH24:MI:SS.FF3'))

        ORDER BY 9, 10, 8;
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
