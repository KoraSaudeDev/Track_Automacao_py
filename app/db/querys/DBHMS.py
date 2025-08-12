from datetime import datetime
import logging
import pandas as pd
from app.service.calc_d1 import get_filtered_dates
from app.db import db

def DB():
    try:
        conn     = db.get_connection("HMS")
        cursor   = conn.cursor()

        #data     = get_filtered_dates()[0]
        data     = '2024-05-10 18:11:00.000'
        SQL01 = """select -- Pacientes Ambulatório HMS
                 '40085'                             "ID_Cliente_Hfocus"
                ,a.hr_atendimento               "Data_Base" 
                ,p.nm_paciente                  "name"
                ,p.email                        "email"
                ,(NVL(p.nr_ddi_celular, '55') || NVL(p.nr_ddd_celular, '') || NVL(p.nr_celular, '')) "phone"
                ,p.nr_cpf                       "cpf"
                ,'AMBULATORIO'                  "Area_Pesquisa"
                ,'MERIDIONAL_SERRA'             "Segmentacao_1"
                ,s.ds_ser_dis                   "Segmentacao_2"
                from
                 dbamv.paciente    p
                ,dbamv.atendime    a
                ,dbamv.ser_dis     s
                where
                    p.cd_paciente = a.cd_paciente
                and a.tp_atendimento = 'A'
                and a.cd_ser_dis = s.cd_ser_dis
                and s.cd_ser_dis in (6,2,3,76,85,30,51,11)
                --and a.cd_tip_res not in (6,17,21)
                and to_char(a.dt_atendimento) = TRUNC(TO_TIMESTAMP(:data,'YYYY-MM-DD HH24:MI:SS.FF3'))

                UNION

                select -- Pacientes Ambulatório HMS
                 '40085'                             "ID_Cliente_Hfocus"
                ,a.hr_atendimento               "Data_Base" 
                ,p.nm_paciente                  "name"
                ,p.email                        "email"
                ,(NVL(p.nr_ddi_celular, '55') || NVL(p.nr_ddd_celular, '') || NVL(p.nr_celular, '')) "phone"
                ,p.nr_cpf                       "cpf"
                ,'AMBULATORIO'                  "Area_Pesquisa"
                ,'MERIDIONAL_SERRA'             "Segmentacao_1"
                ,'GERAL_AMBULATORIO'            "Segmentacao_2"
                from
                 dbamv.paciente    p
                ,dbamv.atendime    a
                ,dbamv.ser_dis     s
                where
                    p.cd_paciente = a.cd_paciente
                and a.tp_atendimento = 'A'
                and a.cd_ser_dis = s.cd_ser_dis
                and s.cd_ser_dis not in (6,2,3,76,85,30,51,11)
                --and a.cd_tip_res not in (6,17,21)
                and to_char(a.dt_atendimento) = TRUNC(TO_TIMESTAMP(:data,'YYYY-MM-DD HH24:MI:SS.FF3'))
         """
        SQL02 = """-- Pacientes Externos HMS - EXTERNO HEMODINAMICA
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
                """
        SQL03 = """
                select -- Pacientes Internados Com Alta Diferente de óbito
                 '40085'                             "ID_Cliente_Hfocus"
                ,a.hr_atendimento               "Data_Base" 
                ,p.nm_paciente                  "Nome_Completo_Paciente"
                ,p.email                        "E-mail"
                ,(NVL(p.nr_ddi_celular, '55') || NVL(p.nr_ddd_celular, '') || NVL(p.nr_celular, '')) "phone"
                ,p.nr_cpf                       "CPF"
                ,'INTERNACAO'                   "Area_Pesquisa"
                ,'MERIDIONAL_SERRA'             "Segmentacao_1"
                ,'INTERNACAO'                   "Segmentacao_2"

                from
                 dbamv.paciente    p
                ,dbamv.atendime    a

                where
                    p.cd_paciente = a.cd_paciente
                and a.tp_atendimento = 'I'
                and a.CD_CID not in ('O60','O80','O82','O84','O757','O800','O801','O809','O810','O820','O821','O822','O829','O839','O840','O842','Z380','Z382')
                and a.cd_atendimento_pai is null
                and a.cd_mot_alt not in (6,7,9,17,18,19,20,21,22)
                and trunc(a.dt_alta) = TRUNC(TO_TIMESTAMP(:data,'YYYY-MM-DD HH24:MI:SS.FF3'))

                union

                select -- Pacientes Externos HMS - EXTERNO CC AMB
                 '40085'                             "ID_Cliente_Hfocus"
                ,a.hr_atendimento               "Data_Base" 
                ,p.nm_paciente                  "Nome_Completo_Paciente"
                ,p.email                        "E-mail"
                ,(NVL(p.nr_ddi_celular, '55') || NVL(p.nr_ddd_celular, '') || NVL(p.nr_celular, '')) "phone"
                ,p.nr_cpf                       "CPF"
                ,'HOSPITAL_DIA'                 "Area_Pesquisa"
                ,'MERIDIONAL_SERRA'             "Segmentacao_1"
                ,'INTERNACAO'                   "Segmentacao_2"

                from
                 dbamv.paciente    p
                ,dbamv.atendime    a

                where
                    p.cd_paciente = a.cd_paciente
                and a.tp_atendimento = 'A'
                and a.cd_ori_ate = 9
                and trunc(a.dt_atendimento) = TRUNC(TO_TIMESTAMP(:data,'YYYY-MM-DD HH24:MI:SS.FF3'))
        """
        SQL04 = """
            select -- Pacientes Internados Maternidade HMSM
             '40085'                        "ID_Cliente_Hfocus"
            ,a.hr_atendimento               "Data_Base" 
            ,p.nm_paciente                  "name"
            ,p.email                        "email"
            ,(NVL(p.nr_ddi_celular, '55') || NVL(p.nr_ddd_celular, '') || NVL(p.nr_celular, '')) "phone"
            ,p.nr_cpf                       "cpf"
            ,'MATERNIDADE'                  "Area_Pesquisa"
            ,'MERIDIONAL_SERRA'             "Segmentacao_1"
            ,'MATERNIDADE'                  "Segmentacao_2"
            from
             dbamv.paciente    p
            ,dbamv.atendime    a
            ,dbamv.atendime    a2

            where
                p.cd_paciente = a.cd_paciente
            and a.tp_atendimento = 'I'
            and a.cd_mot_alt not in (6,7,9,17,18,19,20,21,22)
            and a.CD_ATENDIMENTO = a2.CD_ATENDIMENTO_PAI
            and to_char(a.DT_alta) = TRUNC(TO_TIMESTAMP(:data,'YYYY-MM-DD HH24:MI:SS.FF3'))
         """
        SQL05 = """
                select distinct-- Pacientes PS HMS
                 '40085'                        "ID_Cliente_Hfocus"
                ,a.hr_atendimento               "Data_Base" 
                ,p.nm_paciente                  "name"
                ,p.email                        "email"
                ,(NVL(p.nr_ddi_celular, '55') || NVL(p.nr_ddd_celular, '') || NVL(p.nr_celular, '')) "phone"
                ,p.nr_cpf                       "cpf"
                ,'PRONTO_SOCORRO_GERAL'         "Area_Pesquisa"
                ,'MERIDIONAL_SERRA'             "Segmentacao_1"
                ,'PA_OBSTÉTRICO'                "Segmentacao_2"

                from
                 dbamv.paciente    p
                ,dbamv.atendime    a
                ,dbamv.servico     s
                where
                    p.cd_paciente = a.cd_paciente
                and a.tp_atendimento = 'U'
                and a.cd_Servico = s.cd_servico
                and a.cd_servico = 1
                and a.cd_tip_res not in (1,4,11)
                and to_char(a.dt_alta) = TRUNC(TO_TIMESTAMP(:data,'YYYY-MM-DD HH24:MI:SS.FF3'))

                UNION

                select distinct-- Pacientes PS HMS
                 '40085'                         "ID_Cliente_Hfocus"
                ,a.hr_atendimento               "Data_Base" 
                ,p.nm_paciente                  "name"
                ,p.email                        "email"
                ,(NVL(p.nr_ddi_celular, '55') || NVL(p.nr_ddd_celular, '') || NVL(p.nr_celular, '')) "phone"
                ,p.nr_cpf                       "cpf"
                ,'PRONTO_SOCORRO_GERAL'         "Area_Pesquisa"
                ,'MERIDIONAL_SERRA'             "Segmentacao_1"
                ,'PA_PEDIATRICO'                "Segmentacao_2"

                from
                 dbamv.paciente    p
                ,dbamv.atendime    a
                ,dbamv.servico     s
                where
                    p.cd_paciente = a.cd_paciente
                and a.tp_atendimento = 'U'
                and a.cd_Servico = s.cd_servico
                and a.cd_servico = 27
                and a.cd_tip_res not in (1,4,11)
                and to_char(a.dt_alta) = TRUNC(TO_TIMESTAMP(:data,'YYYY-MM-DD HH24:MI:SS.FF3'))

                UNION

                select distinct-- Pacientes PS HMS
                 '40085'                         "ID_Cliente_Hfocus"
                ,a.hr_atendimento               "Data_Base" 
                ,p.nm_paciente                  "name"
                ,p.email                        "email"
                ,(NVL(p.nr_ddi_celular, '55') || NVL(p.nr_ddd_celular, '') || NVL(p.nr_celular, '')) "phone"
                ,p.nr_cpf                       "cpf"
                ,'PRONTO_SOCORRO_GERAL'         "Area_Pesquisa"
                ,'MERIDIONAL_SERRA'             "Segmentacao_1"
                ,'PA_ADULTO'                    "Segmentacao_2"

                from
                 dbamv.paciente    p
                ,dbamv.atendime    a
                ,dbamv.servico     s
                where
                    p.cd_paciente = a.cd_paciente
                and a.tp_atendimento = 'U'
                and a.cd_Servico = s.cd_servico
                and a.cd_servico not in (1,27)
                and a.cd_tip_res not in (1,4,11)
                and to_char(a.dt_alta) = TRUNC(TO_TIMESTAMP(:data,'YYYY-MM-DD HH24:MI:SS.FF3'))
                """
        SQL = f"""
        {SQL01}
        UNION
        {SQL02}
        UNION
        {SQL03}
        UNION
        {SQL04}
        UNION
        {SQL05}
        ORDER BY 9,8
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
        if cursor is not None:
            cursor.close()
        if conn is not None:
            conn.close()
