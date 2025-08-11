from datetime import datetime
import logging
import pandas as pd
from app.service.calc_d1 import get_filtered_dates
from app.db import db
logging.basicConfig(level=logging.INFO,filename="system.log")

def DB_HMS():
    try:
        conn     = db.get_connection("HMS")
        cursor   = conn.cursor()

        data     = get_filtered_dates()[0]
        #data     = '2024-05-11 18:11:00.000'
        SQL = """-- Pacientes Externos HMS - EXTERNO HEMODINAMICA
                select
                 '40085'                        "ID_Cliente_Hfocus"
                ,a.hr_atendimento               "Data_Base" 
                ,p.nm_paciente                  "name"
                ,p.email                        "email"
                ,(NVL(p.nr_ddi_celular, '55') || NVL(p.nr_ddd_celular, '') || NVL(p.nr_celular, '')) "phone"
                ,p.nr_cpf                       "cpf"
                ,'EXAMES'                       "Area_Pesquisa"
                ,'MERIDIONAL_SERRA'             "Segmentacao_1"
                ,'HEMODINAMICA'                 "Segmentacao_2"
                from
                 dbamv.paciente    p
                ,dbamv.atendime    a

                where
                    p.cd_paciente = a.cd_paciente
                and a.tp_atendimento = 'E'
                and a.cd_ori_ate = 46 
                and to_char(a.dt_atendimento) = TRUNC(TO_TIMESTAMP(:data,'YYYY-MM-DD HH24:MI:SS.FF3'))

                UNION

                select -- Pacientes Externos HMS - EXTERNO HEMODINAMICA
                 '40085'                             "ID_Cliente_Hfocus"
                ,a.hr_atendimento               "Data_Base" 
                ,p.nm_paciente                  "name"
                ,p.email                        "email"
                ,(NVL(p.nr_ddi_celular, '55') || NVL(p.nr_ddd_celular, '') || NVL(p.nr_celular, '')) "phone"
                ,p.nr_cpf                       "cpf"
                ,'EXAMES'                        "Area_Pesquisa"
                ,'MERIDIONAL_SERRA'       "Segmentacao_1"
                ,'LABORATORIO'                 "Segmentacao_2"
                from
                 dbamv.paciente    p
                ,dbamv.atendime    a

                where
                    p.cd_paciente = a.cd_paciente
                and a.tp_atendimento = 'E'
                and a.cd_ori_ate = 7 
                and to_char(a.dt_atendimento) = TRUNC(TO_TIMESTAMP(:data,'YYYY-MM-DD HH24:MI:SS.FF3'))

                order by 9,8
                """

        cursor.execute(SQL, {'data': data})

        rows      = cursor.fetchall()
        columns   = [desc[0] for desc in cursor.description]
        df        = pd.DataFrame(rows, columns=columns)
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