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
        conn     = db.get_connection("HAT")
        cursor   = conn.cursor()

        data     = get_filtered_dates()[0]
        SQL = """
          SELECT
              40094                                                               AS id_focus,

              CAST(
                  CASE
                      WHEN a.tp_atendimento = 'I' THEN dbamv.fnc_mv_recupera_data_hora(a.dt_alta, a.hr_alta)
                      ELSE dbamv.fnc_mv_recupera_data_hora(a.dt_atendimento, a.hr_atendimento)
                  END
              AS TIMESTAMP)                                                       AS "data_atendimento",

              CAST(a.dt_alta AS TIMESTAMP)                                        AS "data_saida_alta",
              p.nm_paciente                                                       AS "name",
              p.email                                                             AS "email",
              (NVL(p.nr_ddi_celular, '55') || NVL(p.nr_ddd_celular, '') || NVL(p.nr_celular, '')) AS "phone",
              p.nr_cpf                                                            AS "cpf",
              'Hospital Anchieta'                                                 AS "unidade",

              CASE
                  WHEN a.tp_atendimento = 'A' AND s.cd_setor = 637 THEN 'ONCOLOGIA'
                  WHEN a.tp_atendimento = 'U' THEN 'PRONTO_SOCORRO_GERAL'
                  WHEN a.tp_atendimento = 'I' THEN 'INTERNACAO'
                  WHEN a.tp_atendimento = 'E' THEN 'EXAMES'
                  WHEN a.tp_atendimento = 'A' THEN 'AMBULATORIO'
                  ELSE a.tp_atendimento
              END                                                                 AS "area_pesquisa",

              CASE
                  WHEN a.tp_atendimento = 'I' THEN ui.ds_unid_int
                  ELSE s.nm_setor
              END                                                                 AS "setor",

              pr.nm_prestador                                                     AS "medico",
              a.cd_atendimento													AS "cd_atendimento"

          FROM dbamv.atendime a
          JOIN dbamv.paciente p               ON p.cd_paciente = a.cd_paciente
          JOIN dbamv.ori_ate oa               ON oa.cd_ori_ate = a.cd_ori_ate
          JOIN dbamv.setor s                  ON s.cd_setor = oa.cd_setor
          JOIN dbamv.especialid e             ON e.cd_especialid = a.cd_especialid
          JOIN dbamv.prestador pr             ON pr.cd_prestador = a.cd_prestador
          LEFT JOIN dbamv.mot_alt ma          ON ma.cd_mot_alt = a.cd_mot_alt
          LEFT JOIN dbamv.leito l             ON l.cd_leito = a.cd_leito
          LEFT JOIN dbamv.unid_int ui         ON l.cd_unid_int = ui.cd_unid_int
          LEFT JOIN (
              SELECT
                  cd_atendimento,
                  LISTAGG(ds_unid_int, ' / ') WITHIN GROUP (ORDER BY ds_unid_int) AS unidades_pac
              FROM (
                  SELECT DISTINCT
                      mov_int.cd_atendimento,
                      unid_int.ds_unid_int
                  FROM dbamv.mov_int
                  JOIN dbamv.leito ON leito.cd_leito = mov_int.cd_leito
                  JOIN dbamv.unid_int ON leito.cd_unid_int = unid_int.cd_unid_int
                  WHERE mov_int.cd_atendimento IS NOT NULL
              )
              GROUP BY cd_atendimento
          ) spc  ON spc.cd_atendimento = a.cd_atendimento

          WHERE
              UPPER(p.email) NOT LIKE '%NAO%'
              AND (
                  -- Regra 1: Pronto Socorro (U)
                  (a.tp_atendimento = 'U' AND TRUNC(a.dt_atendimento) = TRUNC(TO_TIMESTAMP(:data, 'YYYY-MM-DD HH24:MI:SS.FF3')) AND NVL(a.cd_tip_res, 0) NOT IN (6, 5, 8, 17, 13, 14))
                  -- Regra 2: Internação (I)
                  OR (a.tp_atendimento = 'I' AND TRUNC(a.dt_alta) = TRUNC(TO_TIMESTAMP(:data, 'YYYY-MM-DD HH24:MI:SS.FF3')) AND ma.tp_mot_alta <> 'O' AND UPPER(p.nm_paciente) NOT LIKE 'RN%')
                  -- Regra 3: Ambulatório SEM Oncologia (A)
                  OR (a.tp_atendimento = 'A' AND TRUNC(a.dt_atendimento) = TRUNC(TO_TIMESTAMP(:data, 'YYYY-MM-DD HH24:MI:SS.FF3')) AND s.cd_setor <> 637)
                  -- Regra 4: Ambulatório SÓ Oncologia (A)
                  OR (a.tp_atendimento = 'A' AND TRUNC(a.dt_atendimento) = TRUNC(TO_TIMESTAMP(:data, 'YYYY-MM-DD HH24:MI:SS.FF3')) AND s.cd_setor = 637)
                  -- Regra 5: Exames (E)
                  OR (a.tp_atendimento = 'E' AND TRUNC(a.dt_atendimento) = TRUNC(TO_TIMESTAMP(:data, 'YYYY-MM-DD HH24:MI:SS.FF3'))
              ))
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
        if cursor:
            cursor.close()
        if conn:
            conn.close()