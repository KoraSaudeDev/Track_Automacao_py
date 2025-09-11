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
        conn     = db.get_connection_tasy("HAC")
        cursor   = conn.cursor()

        data     = get_filtered_dates()[0]

        SQL = """
        -- HFOCUS SEGMENTADO (NPS)--
            select '40085' as ID_Cliente_Hfocus, 
            a.DT_ENTRADA AS "data_atendimento",
            a.DT_ALTA AS "data_saida_alta",
            a.NR_ATENDIMENTO AS "cd_atendimento",
            a.NM_MEDICO AS "medico",
            a.NM_PACIENTE as "name",
            b.DS_EMAIL_CCIH AS "email",
            (NVL(b.NR_DDI_CELULAR, '55') || NVL(b.NR_DDD_CELULAR, '') || NVL(b.NR_TELEFONE_CELULAR, '')) AS "phone",
            a.NR_CPF as "cpf",
            'INTERNACAO' "area_pesquisa",
            'Hospital São Francisco DF' AS "unidade",
            'INTERNACAO' AS "setor"
            
            from 
            TASY.atendimento_paciente_v a,
            TASY.pessoa_fisica b,
            TASY.SETOR_ATENDIMENTO c
            
            where 1 = 1
            
        
            AND TRUNC(A.DT_ALTA) = TRUNC(TO_TIMESTAMP(:data, 'YYYY-MM-DD HH24:MI:SS.FF3'))    
            
            and a.CD_PESSOA_FISICA = b.cd_pessoa_fisica
            and A.ds_setor_internacao = C.DS_SETOR_ATENDIMENTO
            AND A.IE_TIPO_ATENDIMENTO IN (1)
            and a.dt_cancelamento is NULL
            --AND b.IE_PERM_SMS_EMAIL = 'S'
            and a.CD_MOTIVO_ALTA not in (7,16,30,21,26,27,28)
            AND C.CD_SETOR_ATENDIMENTO <> 54
                
            
            -----Maternidade----------------------------
            UNION ALL
            select '40085' as ID_Cliente_Hfocus, 
            a.DT_ENTRADA AS "data_atendimento",
            a.DT_ALTA AS "data_saida_alta",
            a.NR_ATENDIMENTO AS "cd_atendimento",
            a.NM_MEDICO AS "medico",
            a.NM_PACIENTE as "name",
            b.DS_EMAIL_CCIH AS "email",
            (NVL(b.NR_DDI_CELULAR, '55') || NVL(b.NR_DDD_CELULAR, '') || NVL(b.NR_TELEFONE_CELULAR, '')) AS "phone",
            a.NR_CPF as "cpf",
            'MATERNIDADE' "area_pesquisa",
            'Hospital São Francisco DF' AS "unidade",
            'MATERNIDADE' AS "setor"
            
            from 
            TASY.atendimento_paciente_v a,
            TASY.pessoa_fisica b,
            TASY.SETOR_ATENDIMENTO c
            
            where 1 = 1
            
            AND TRUNC(A.DT_ALTA) = TRUNC(TO_TIMESTAMP(:data, 'YYYY-MM-DD HH24:MI:SS.FF3'))    
            and a.CD_PESSOA_FISICA = b.cd_pessoa_fisica
            and A.ds_setor_internacao = C.DS_SETOR_ATENDIMENTO
            AND A.DT_ALTA IS NOT NULL
            AND A.IE_TIPO_ATENDIMENTO IN (1)
            and a.dt_cancelamento is null
            and a.CD_MOTIVO_ALTA not in (7,16,30,21,26,27,28)
            AND C.CD_SETOR_ATENDIMENTO = 54

            
            ---PRONTO SOCORRO----
            UNION ALL
            
            select '40085' as ID_Cliente_Hfocus, 
            a.DT_ENTRADA AS "data_atendimento",
            a.DT_ALTA AS "data_saida_alta",
            a.NR_ATENDIMENTO AS "cd_atendimento",
            a.NM_MEDICO AS "medico",
            a.NM_PACIENTE as "name",
            b.DS_EMAIL_CCIH AS "email",
            (NVL(b.NR_DDI_CELULAR, '55') || NVL(b.NR_DDD_CELULAR, '') || NVL(b.NR_TELEFONE_CELULAR, '')) AS "phone",
            a.NR_CPF as "cpf",
            'PRONTO SOCORRO GERAL' as "area_pesquisa",
            'Hospital São Francisco DF' AS "unidade",
            decode(A.IE_CLINICA,13,'PA_GINECOLOGICO',10,'PA_PEDIATRICO',4,'PA_PEDIATRICO','PA_ADULTO') AS "setor"
            from 
            TASY.atendimento_paciente_v a,
            TASY.pessoa_fisica b
            where 1 = 1
            
            AND TRUNC(A.DT_ALTA) = TRUNC(TO_TIMESTAMP(:data, 'YYYY-MM-DD HH24:MI:SS.FF3'))
            and a.CD_PESSOA_FISICA = b.cd_pessoa_fisica
            AND A.DT_ALTA IS NOT NULL
            AND A.IE_TIPO_ATENDIMENTO IN (3)
            and a.dt_cancelamento is null
            and a.CD_MOTIVO_ALTA not in (7,16,30,21,26,27,28)
            
            --------ATENDIMENTO AMBULATORIAL------------
            UNION ALL 
            
            select '40085' as ID_Cliente_Hfocus, 
            a.DT_ENTRADA AS "data_atendimento",
            a.DT_ALTA AS "data_saida_alta",
            a.NR_ATENDIMENTO AS "cd_atendimento",
            a.NM_MEDICO AS "medico",
            a.NM_PACIENTE as "name",
            b.DS_EMAIL_CCIH AS "email",
            (NVL(b.NR_DDI_CELULAR, '55') || NVL(b.NR_DDD_CELULAR, '') || NVL(b.NR_TELEFONE_CELULAR, '')) AS "phone",
            a.NR_CPF as "cpf",
            'AMBULATORIO' AS "area_pesquisa",
            'Hospital São Francisco DF' AS "unidade",
            'AMBULATORIO_GERAL' as "setor"
            from 
            TASY.atendimento_paciente_v a,
            TASY.pessoa_fisica b
            where 1 = 1
        
            AND TRUNC(A.DT_ALTA) = TRUNC(TO_TIMESTAMP(:data, 'YYYY-MM-DD HH24:MI:SS.FF3'))
            
            and a.CD_PESSOA_FISICA = b.cd_pessoa_fisica
            AND A.DT_ALTA IS NOT NULL
            and a.dt_cancelamento is null
            AND A.IE_TIPO_ATENDIMENTO IN (8)
            and a.CD_MOTIVO_ALTA not in (7,16,30,21,26,27,28)
            
            ------------Exames-------------------
            
            UNION ALL 
            
            select '40085' as ID_Cliente_Hfocus, 
            a.DT_ENTRADA AS "data_atendimento",
            a.DT_ALTA AS "data_saida_alta",
            a.NR_ATENDIMENTO AS "cd_atendimento",
            a.NM_MEDICO AS "medico",
            a.NM_PACIENTE as "name",
            b.DS_EMAIL_CCIH AS "email",
            (NVL(b.NR_DDI_CELULAR, '55') || NVL(b.NR_DDD_CELULAR, '') || NVL(b.NR_TELEFONE_CELULAR, '')) AS "phone",
            a.NR_CPF as "cpf",
            'EXAMES' as "area_pesquisa",
            'Hospital São Francisco DF' AS "unidade",
            decode(a.nr_seq_classificacao,2,'IMAGEM',6,'LABORATORIO',14,'LABORATORIO','16','IMAGEM') AS "setor"
            from 
            TASY.atendimento_paciente_v a,
            TASY.pessoa_fisica b
            where 1 = 1
            
            AND TRUNC(A.DT_ALTA) = TRUNC(TO_TIMESTAMP(:data, 'YYYY-MM-DD HH24:MI:SS.FF3'))
            
            and a.CD_PESSOA_FISICA = b.cd_pessoa_fisica
            AND A.DT_ALTA IS NOT NULL
            and a.dt_cancelamento is null
            AND A.IE_TIPO_ATENDIMENTO IN (7)
            and a.CD_MOTIVO_ALTA not in (7,16,30,21,26,27,28)
            AND A.nr_seq_classificacao IS NOT NULL
            ORDER BY 3,9
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

