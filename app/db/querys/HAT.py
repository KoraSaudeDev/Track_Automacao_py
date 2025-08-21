from datetime import datetime
import logging
import pandas as pd
from app.service.calc_d1 import get_filtered_dates
from app.db import db
logging.basicConfig(level=logging.INFO,filename="system.log")

def DB():
    try:
        conn     = db.get_connection("HAT")
        cursor   = conn.cursor()

        data     = get_filtered_dates()[0]
        SQL = """
                SELECT ID_FOCUS, "data_atendimento","data_saida_alta", "name", "email", "phone","cpf", "area_pesquisa","setor","unidade", "especialidade"
                      ,"SEGMENTACAO 3", "SEGMENTACAO 4", "SEGMENTACAO 5", EXTRA_INF_SETOR, "medico", "ID_EXTERNO_PACIENTE", CD_ATENDIMENTO
                FROM (
                    SELECT ID_FOCUS, "data_atendimento","data_saida_alta", "name", "email", "phone","cpf", "area_pesquisa", "setor","unidade", "especialidade"
                          ,"SEGMENTACAO 3", "SEGMENTACAO 4", "SEGMENTACAO 5", EXTRA_INF_SETOR, "medico", "ID_EXTERNO_PACIENTE", CD_ATENDIMENTO
                          ,Dt_Alta_Medica, Hr_Atendimento
                          ,tempo, (percent_rank() over (partition by 1 order by tempo)* 100) ranking, ROW_NUMBER() over (partition by 1 order by tempo) qtde
                          ,(select count(1) from dbamv.atendime where tp_atendimento = 'U' and trunc(DT_ATENDIMENTO) = TRUNC(TO_TIMESTAMP(:data, 'YYYY-MM-DD HH24:MI:SS.FF3')) and atendime.dt_alta_medica is not null) total
                      FROM (
                      select 40094 ID_FOCUS,
                            CAST(dbamv.fnc_mv_recupera_data_hora(ATENDIME.DT_ATENDIMENTO, atendime.hr_atendimento) AS TIMESTAMP) "data_atendimento",
                            CAST(atendime.Dt_Alta_Medica AS TIMESTAMP) AS "data_saida_alta",
                            paciente.nm_paciente "name", paciente.email "email",
                            (NVL(paciente.NR_DDI_CELULAR, '55') || NVL(paciente.NR_DDD_CELULAR, '') || NVL(paciente.NR_CELULAR, '')) AS "phone",
                            paciente.NR_CPF AS "cpf",
                            'Hospital Anchieta' AS "unidade",
                            DECODE(ATENDIME.TP_ATENDIMENTO,'U','PRONTO_SOCORRO_GERAL','I','INTERNACAO','E','EXAMES','A','AMBULATORIO') "area_pesquisa",
                            SETOR.NM_SETOR "setor", ESPECIALID.DS_ESPECIALID "especialidade", NULL "SEGMENTACAO 3", NULL "SEGMENTACAO 4", NULL "SEGMENTACAO 5",
                            'PSO' EXTRA_INF_SETOR, PRESTADOR.NM_PRESTADOR "medico", PACIENTE.CD_PACIENTE "ID_EXTERNO_PACIENTE", ATENDIME.CD_ATENDIMENTO
                            ,atendime.Dt_Alta_Medica , atendime.Hr_Atendimento, trunc((atendime.Dt_Alta_Medica - atendime.Hr_Atendimento) * 24 * 60) tempo
                      from dbamv.atendime, dbamv.paciente, dbamv.setor, dbamv.ori_ate, DBAMV.ESPECIALID, DBAMV.PRESTADOR
                      WHERE paciente.cd_paciente = atendime.cd_paciente
                        AND SETOR.CD_SETOR = ORI_ATE.CD_SETOR
                        AND ORI_ATE.CD_ORI_ATE = ATENDIME.CD_ORI_ATE
                        AND ATENDIME.CD_ESPECIALID = ESPECIALID.CD_ESPECIALID
                        AND PRESTADOR.CD_PRESTADOR = ATENDIME.CD_PRESTADOR
                        and upper(paciente.email) not like ('%NAO%')
                        AND NVL(ATENDIME.CD_TIP_RES,0)  NOT IN (6,5,8,17,13,14)
                        AND TP_ATENDIMENTO = 'U'
                        and trunc(DT_ATENDIMENTO) = TRUNC(TO_TIMESTAMP(:data, 'YYYY-MM-DD HH24:MI:SS.FF3'))
                      )
                )
                -- WHERE qtde <= (total * 1)

                UNION ALL

                select 40094 ID_FOCUS,
                      CAST(dbamv.fnc_mv_recupera_data_hora(DT_ALTA, atendime.hr_alta) AS TIMESTAMP) "data_atendimento",
                      CAST(ATENDIME.DT_ALTA AS TIMESTAMP) AS "data_saida_alta",
                      paciente.nm_paciente "name", paciente.email "email",
                      (NVL(paciente.NR_DDI_CELULAR, '55') || NVL(paciente.NR_DDD_CELULAR, '') || NVL(paciente.NR_CELULAR, '')) AS "phone",
                      paciente.NR_CPF AS "cpf",
                      'Hospital Anchieta' AS "unidade",
                      DECODE(ATENDIME.TP_ATENDIMENTO,'U','PRONTO_SOCORRO_GERAL','I','INTERNACAO','E','EXAMES','A','AMBULATORIO') "area_pesquisa",
                      UNID_INT.DS_UNID_INT "setor",
                      ESPECIALID.DS_ESPECIALID "especialidade", NULL "SEGMENTACAO 3", NULL "SEGMENTACAO 4", NULL "SEGMENTACAO 5",
                      SETORES_PAC.UNIDADES_PAC EXTRA_INF_SETOR,
                      PRESTADOR.NM_PRESTADOR "medico", PACIENTE.CD_PACIENTE "ID_EXTERNO_PACIENTE", ATENDIME.CD_ATENDIMENTO
                  from dbamv.atendime, dbamv.paciente, dbamv.setor, dbamv.ori_ate, DBAMV.ESPECIALID, DBAMV.PRESTADOR, DBAMV.MOT_ALT, DBAMV.LEITO, DBAMV.UNID_INT,
                      (select CD_ATENDIMENTO,LISTAGG(DS_UNID_INT, ' / ') WITHIN GROUP (ORDER BY DS_UNID_INT) AS UNIDADES_PAC
                        from (SELECT distinct cd_atendimento, ds_unid_int
                                          FROM DBAMV.MOV_INT, DBAMV.LEITO, DBAMV.UNID_INT
                                        WHERE LEITO.CD_LEITO = MOV_INT.CD_LEITO
                                          AND LEITO.CD_UNID_INT = UNID_INT.CD_UNID_INT
                                          and cd_atendimento is not null)
                                          GROUP BY CD_ATENDIMENTO) SETORES_PAC
                WHERE paciente.cd_paciente = atendime.cd_paciente
                  AND SETOR.CD_SETOR = UNID_INT.CD_SETOR
                  AND ORI_ATE.CD_ORI_ATE = ATENDIME.CD_ORI_ATE
                  AND LEITO.CD_LEITO = ATENDIME.CD_LEITO
                  AND LEITO.CD_UNID_INT = UNID_INT.CD_UNID_INT
                  AND ATENDIME.CD_ESPECIALID = ESPECIALID.CD_ESPECIALID
                  AND PRESTADOR.CD_PRESTADOR = ATENDIME.CD_PRESTADOR
                  AND MOT_ALT.CD_MOT_ALT = ATENDIME.CD_MOT_ALT
                  AND SETORES_PAC.CD_ATENDIMENTO(+) = ATENDIME.CD_ATENDIMENTO
                  and trunc(DT_ALTA) = TRUNC(TO_TIMESTAMP(:data, 'YYYY-MM-DD HH24:MI:SS.FF3'))
                  AND MOT_ALT.TP_MOT_ALTA <> 'O'
                  AND TP_ATENDIMENTO = 'I'
                  and upper(paciente.email) not like ('%NAO%')
                  and upper(paciente.nm_paciente) NOT like ('RN%')

                UNION ALL

                --AMBULATORIO SEM ONCOLOGIA
                select 40094 ID_FOCUS,
                      CAST(dbamv.fnc_mv_recupera_data_hora(ATENDIME.DT_ATENDIMENTO, atendime.hr_atendimento) AS TIMESTAMP) "data_atendimento",
                      CAST(ATENDIME.DT_ALTA AS TIMESTAMP) AS "data_saida_alta",
                      paciente.nm_paciente "name", paciente.email "email",
                      (NVL(paciente.NR_DDI_CELULAR, '55') || NVL(paciente.NR_DDD_CELULAR, '') || NVL(paciente.NR_CELULAR, '')) AS "phone",
                      paciente.NR_CPF AS "cpf",
                      'Hospital Anchieta' AS "unidade",
                      DECODE(ATENDIME.TP_ATENDIMENTO,'U','PRONTO_SOCORRO_GERAL','I','INTERNACAO','E','EXAMES','A','AMBULATORIO') "area_pesquisa",
                      SETOR.NM_SETOR "setor",
                      ESPECIALID.DS_ESPECIALID "especialidade", NULL "SEGMENTACAO 3", NULL "SEGMENTACAO 4", NULL "SEGMENTACAO 5",
                      'AMBULATORIO' EXTRA_INF_SETOR, PRESTADOR.NM_PRESTADOR "medico", PACIENTE.CD_PACIENTE "ID_EXTERNO_PACIENTE", ATENDIME.CD_ATENDIMENTO
                  from dbamv.atendime, dbamv.paciente, dbamv.setor, dbamv.ori_ate, DBAMV.ESPECIALID, DBAMV.PRESTADOR
                WHERE paciente.cd_paciente = atendime.cd_paciente
                  AND SETOR.CD_SETOR = ORI_ATE.CD_SETOR
                  AND ORI_ATE.CD_ORI_ATE = ATENDIME.CD_ORI_ATE
                  AND ATENDIME.CD_ESPECIALID = ESPECIALID.CD_ESPECIALID
                  AND PRESTADOR.CD_PRESTADOR = ATENDIME.CD_PRESTADOR
                  and trunc(DT_ATENDIMENTO) = TRUNC(TO_TIMESTAMP(:data, 'YYYY-MM-DD HH24:MI:SS.FF3'))
                  AND TP_ATENDIMENTO = 'A'
                  and upper(paciente.email) not like ('%NAO%')
                  AND SETOR.CD_SETOR <> 637

                UNION ALL

                --AMBULATÓRIO SÓ ONCOLOGIA
                select 40094 ID_FOCUS,
                      CAST(dbamv.fnc_mv_recupera_data_hora(ATENDIME.DT_ATENDIMENTO, atendime.hr_atendimento) AS TIMESTAMP) "data_atendimento",
                      CAST(ATENDIME.DT_ALTA AS TIMESTAMP) AS "data_saida_alta", -- CORRIGIDO: Coluna na posição correta
                      paciente.nm_paciente "name", paciente.email "email",
                      (NVL(paciente.NR_DDI_CELULAR, '55') || NVL(paciente.NR_DDD_CELULAR, '') || NVL(paciente.NR_CELULAR, '')) AS "phone",
                      paciente.NR_CPF AS "cpf",
                      'Hospital Anchieta' AS "unidade",
                      'ONCOLOGIA' "area_pesquisa", -- CORRIGIDO: Coluna na posição correta
                      SETOR.NM_SETOR "setor",
                      ESPECIALID.DS_ESPECIALID "especialidade", NULL "SEGMENTACAO 3", NULL "SEGMENTACAO 4", NULL "SEGMENTACAO 5",
                      'AMBULATORIO' EXTRA_INF_SETOR, PRESTADOR.NM_PRESTADOR "medico", PACIENTE.CD_PACIENTE "ID_EXTERNO_PACIENTE", ATENDIME.CD_ATENDIMENTO
                from dbamv.atendime, dbamv.paciente, dbamv.setor, dbamv.ori_ate, DBAMV.ESPECIALID, DBAMV.PRESTADOR
                WHERE paciente.cd_paciente = atendime.cd_paciente
                  AND SETOR.CD_SETOR = ORI_ATE.CD_SETOR
                  AND ORI_ATE.CD_ORI_ATE = ATENDIME.CD_ORI_ATE
                  AND ATENDIME.CD_ESPECIALID = ESPECIALID.CD_ESPECIALID
                  AND PRESTADOR.CD_PRESTADOR = ATENDIME.CD_PRESTADOR
                  and trunc(DT_ATENDIMENTO) = TRUNC(TO_TIMESTAMP(:data, 'YYYY-MM-DD HH24:MI:SS.FF3'))
                  AND TP_ATENDIMENTO = 'A'
                  and upper(paciente.email) not like ('%NAO%')
                  AND SETOR.CD_SETOR = 637

                UNION ALL

                select 40094 ID_FOCUS,
                      CAST(dbamv.fnc_mv_recupera_data_hora(ATENDIME.DT_ATENDIMENTO, atendime.hr_atendimento) AS TIMESTAMP) "data_atendimento",
                      CAST(ATENDIME.DT_ALTA AS TIMESTAMP) AS "data_saida_alta",
                      paciente.nm_paciente "name", paciente.email "email",
                      (NVL(paciente.NR_DDI_CELULAR, '55') || NVL(paciente.NR_DDD_CELULAR, '') || NVL(paciente.NR_CELULAR, '')) AS "phone",
                      paciente.NR_CPF AS "cpf",
                      'Hospital Anchieta' AS "unidade",
                      DECODE(ATENDIME.TP_ATENDIMENTO,'U','PRONTO_SOCORRO_GERAL','I','INTERNACAO','E','EXAMES','A','AMBULATORIO') "area_pesquisa",
                      SETOR.NM_SETOR "setor",
                      ESPECIALID.DS_ESPECIALID "especialidade", NULL "SEGMENTACAO 3", NULL "SEGMENTACAO 4", NULL "SEGMENTACAO 5",
                      'EXAMES' EXTRA_INF_SETOR, PRESTADOR.NM_PRESTADOR "medico", PACIENTE.CD_PACIENTE "ID_EXTERNO_PACIENTE", ATENDIME.CD_ATENDIMENTO
                  from dbamv.atendime, dbamv.paciente, dbamv.setor, dbamv.ori_ate, DBAMV.ESPECIALID, DBAMV.PRESTADOR
                WHERE paciente.cd_paciente = atendime.cd_paciente
                  AND SETOR.CD_SETOR = ORI_ATE.CD_SETOR
                  AND ORI_ATE.CD_ORI_ATE = ATENDIME.CD_ORI_ATE
                  AND ATENDIME.CD_ESPECIALID = ESPECIALID.CD_ESPECIALID
                  AND PRESTADOR.CD_PRESTADOR = ATENDIME.CD_PRESTADOR
                  and trunc(DT_ATENDIMENTO) = TRUNC(TO_TIMESTAMP(:data, 'YYYY-MM-DD HH24:MI:SS.FF3'))
                    AND TP_ATENDIMENTO = 'E'
                  and upper(paciente.email) not like ('%NAO%')
                

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
        if cursor and conn:
            cursor.close()
            conn.close()