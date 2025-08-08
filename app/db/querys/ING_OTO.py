from app.service.calc_d1 import get_filtered_dates
from app.db import db
import pandas as pd

conn     = db.get_connection("OTO_ING")
cursor   = conn.cursor()

#data     = get_filtered_dates()[0]
data     = '2024-05-16 18:11:00.000'

def DB_ING_OTO():

    SQL = """SELECT -- PACIENTES PS GRUPO OTO
    
    '40085'                        "ID_CLIENTE_HFOCUS"
    ,A.HR_ATENDIMENTO               "DATA_BASE" 
    ,P.NM_PACIENTE                  "NOME_COMPLETO_PACIENTE"
    ,P.EMAIL                        "E-MAIL"
    ,P.NR_FONE                      "TELEFONE_RESIDENCIAL"
    ,(NVL(p.nr_ddi_celular, '55') || NVL(p.nr_ddd_celular, '') || NVL(p.nr_celular, '')) "Telefone_Celular"
    ,P.NR_CELULAR                   "TELEFONE_CELULAR"
    ,P.NR_CPF                       "CPF"
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
    ,P.NM_PACIENTE                  "NOME_COMPLETO_PACIENTE"
    ,P.EMAIL                        "E-MAIL"
    ,P.NR_FONE                      "TELEFONE_RESIDENCIAL"
    ,(NVL(p.nr_ddi_celular, '55') || NVL(p.nr_ddd_celular, '') || NVL(p.nr_celular, '')) "Telefone_Celular"
    ,P.NR_CELULAR                   "TELEFONE_CELULAR"
    ,P.NR_CPF                       "CPF"
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
    ,P.NM_PACIENTE                  "NOME_COMPLETO_PACIENTE"
    ,P.EMAIL                        "E-MAIL"
    ,P.NR_FONE                      "TELEFONE_RESIDENCIAL"
    ,(NVL(p.nr_ddi_celular, '55') || NVL(p.nr_ddd_celular, '') || NVL(p.nr_celular, '')) "Telefone_Celular"
    ,P.NR_CELULAR                   "TELEFONE_CELULAR"
    ,P.NR_CPF                       "CPF"
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



    ORDER BY 9, 10, 8"""

    cursor.execute(SQL, {'data': data})

    df        = pd.DataFrame(cursor.fetchall(),  columns=[col[0] for col in cursor.description])
    dict_data = df[["NOME_COMPLETO_PACIENTE", "Telefone_Celular", "CPF", "E-MAIL"]].to_dict(orient='records')

    return dict_data