from datetime import datetime
import logging
import pandas as pd
from app.service.calc_d1 import get_filtered_dates
from app.db import db
logging.basicConfig(level=logging.INFO,filename="system.log")

def DB_ING_OTO():
    try:
        conn     = db.get_connection("OTO_ING")
        cursor   = conn.cursor()

        data     = get_filtered_dates()[0]
        #data     = '2024-05-00 18:11:00.000'
        SQL = """SELECT -- PACIENTES PS GRUPO OTO

        '40085'                        "ID_CLIENTE_HFOCUS"
        ,A.HR_ATENDIMENTO               "DATA_BASE" 
        ,P.NM_PACIENTE                  "name"
        ,P.EMAIL                        "email"
        ,(NVL(p.nr_ddi_celular, '55') || NVL(p.nr_ddd_celular, '') || NVL(p.nr_celular, '')) "phone"
        ,P.NR_CPF                       "cpf"
        ,'PRONTO_SOCORRO_GERAL'         "AREA_PESQUISA"
        ,M.DS_MULTI_EMPRESA             "SEGMENTACAO_1"
        ,'PA_OBSTÉTRICO'                "SEGMENTACAO_2"

        FROM
        DBAMV.PACIENTE    P
        ,DBAMV.ATENDIME    A
        ,DBAMV.SERVICO     S
        , DBAMV.MULTI_EMPRESAS M


        WHERE
            P.CD_PACIENTE = A.CD_PACIENTE
        AND A.TP_ATENDIMENTO = 'U'
        AND A.CD_TIP_RES NOT IN (SELECT TP.CD_TIP_RES FROM DBAMV.TIP_RES TP WHERE TP.SN_OBITO = 'S')
        AND A.CD_SERVICO = S.CD_SERVICO
        AND A.CD_SERVICO = 5 -- GINECOLOGIA
        AND A.CD_MULTI_EMPRESA = M.CD_MULTI_EMPRESA
        AND TO_CHAR(A.DT_ALTA) = TRUNC(TO_TIMESTAMP(:data, 'YYYY-MM-DD HH24:MI:SS.FF3'))


        UNION ALL

        SELECT -- PACIENTES PS GRUPO OTO

        '40085'                        "ID_CLIENTE_HFOCUS"
        ,A.HR_ATENDIMENTO               "DATA_BASE" 
        ,P.NM_PACIENTE                  "name"
        ,P.EMAIL                        "email"
        ,(NVL(p.nr_ddi_celular, '55') || NVL(p.nr_ddd_celular, '') || NVL(p.nr_celular, '')) "phone"
        ,P.NR_CPF                       "cpf"
        ,'PRONTO_SOCORRO_GERAL'         "AREA_PESQUISA"
        ,M.DS_MULTI_EMPRESA             "SEGMENTACAO_1"
        ,'PA_PEDIATRICO'                "SEGMENTACAO_2"

        FROM
        DBAMV.PACIENTE    P
        ,DBAMV.ATENDIME    A
        ,DBAMV.SERVICO     S
        , DBAMV.MULTI_EMPRESAS M


        WHERE
            P.CD_PACIENTE = A.CD_PACIENTE
        AND A.TP_ATENDIMENTO = 'U'
        AND A.CD_TIP_RES NOT IN (SELECT TP.CD_TIP_RES FROM DBAMV.TIP_RES TP WHERE TP.SN_OBITO = 'S')
        AND A.CD_SERVICO = S.CD_SERVICO
        AND A.CD_SERVICO = 40 -- PEDIATRIA
        AND A.CD_MULTI_EMPRESA = M.CD_MULTI_EMPRESA
        AND TO_CHAR(A.DT_ALTA) = TRUNC(TO_TIMESTAMP(:data, 'YYYY-MM-DD HH24:MI:SS.FF3'))

        UNION ALL

        SELECT -- PACIENTES PS GRUPO OTO

        '40085'                        "ID_CLIENTE_HFOCUS"
        ,A.HR_ATENDIMENTO               "DATA_BASE" 
        ,P.NM_PACIENTE                  "name"
        ,P.EMAIL                        "email"
        ,(NVL(p.nr_ddi_celular, '55') || NVL(p.nr_ddd_celular, '') || NVL(p.nr_celular, '')) "phone"
        ,P.NR_CPF                       "cpf"
        ,'PRONTO_SOCORRO_GERAL'         "AREA_PESQUISA"
        ,M.DS_MULTI_EMPRESA             "SEGMENTACAO_1"
        ,'PA_ADULTO'                    "SEGMENTACAO_2"

        FROM
        DBAMV.PACIENTE    P
        ,DBAMV.ATENDIME    A
        ,DBAMV.SERVICO     S
        , DBAMV.MULTI_EMPRESAS M


        WHERE
            P.CD_PACIENTE = A.CD_PACIENTE
        AND A.TP_ATENDIMENTO = 'U'
        AND A.CD_TIP_RES NOT IN (SELECT TP.CD_TIP_RES FROM DBAMV.TIP_RES TP WHERE TP.SN_OBITO = 'S')
        AND A.CD_SERVICO = S.CD_SERVICO
        AND A.CD_SERVICO NOT IN (5, 40) -- NÃO TRAZER GINECOLOGIA E PEDIATRIA 
        AND A.CD_MULTI_EMPRESA = M.CD_MULTI_EMPRESA
        AND TO_CHAR(A.DT_ALTA) = TRUNC(TO_TIMESTAMP(:data, 'YYYY-MM-DD HH24:MI:SS.FF3'))



        ORDER BY 9, 8"""

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