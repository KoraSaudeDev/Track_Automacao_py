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
        conn     = db.get_connection_tasy("ENCORE")
        cursor   = conn.cursor()

        data     = get_filtered_dates()[0]

        SQL = """
                SELECT 
                '40085' AS id_cliente,
                a.DT_ENTRADA AS "data_atendimento",
                a.DT_ALTA AS "data_saida_alta",
                a.NM_MEDICO AS "medico",
                a.NM_PACIENTE as "name",
                b.DS_EMAIL_CCIH AS "email",
                (NVL(b.NR_DDI_CELULAR, '55') || NVL(b.NR_DDD_CELULAR, '') || NVL(b.NR_TELEFONE_CELULAR, '')) AS "phone",
                a.NR_CPF as "cpf",
                CASE 
                    WHEN a.nr_seq_classificacao = 1 THEN 'AMBULATORIO'
                    WHEN a.nr_seq_classificacao <> 1 THEN 'EXAMES'
                    ELSE 'OUTROS' 
                END AS "area_pesquisa",
                'Hospital Encore' AS "unidade",
                CASE 
                    WHEN a.nr_seq_classificacao = 1 THEN 'AMBULATORIO'
                    WHEN a.cd_setor_atendimento = 357 THEN 'LABORATORIO'
                    WHEN a.cd_setor_atendimento IN (353, 354, 365, 405) THEN 'IMAGEM'
                    WHEN a.cd_setor_atendimento IN (369, 370, 355) THEN 'EXAMES'
                    ELSE 'OUTROS' 
                END AS "setor"
            FROM 
                USUARIO_PRINCIPAL.atendimento_paciente_v a,
                USUARIO_PRINCIPAL.pessoa_fisica b
            WHERE 
                TRUNC(A.DT_ALTA) = TRUNC(TO_TIMESTAMP(:data, 'YYYY-MM-DD HH24:MI:SS.FF3'))  
                AND a.CD_PESSOA_FISICA = b.cd_pessoa_fisica
                AND a.ie_tipo_atendimento NOT IN (1, 3)
                AND a.dt_cancelamento IS NULL
                AND a.cd_estabelecimento = 21
            UNION
            SELECT 
                '40085' AS id_cliente,
                a.DT_ENTRADA AS "data_atendimento",
                a.DT_ALTA AS "data_saida_alta",
                a.NM_MEDICO AS "medico",
                a.NM_PACIENTE as "name",
                b.DS_EMAIL_CCIH AS "email",
                (NVL(b.NR_DDI_CELULAR, '55') || NVL(b.NR_DDD_CELULAR, '') || NVL(b.NR_TELEFONE_CELULAR, '')) AS "phone",
                a.NR_CPF as "cpf",
                'EXAMES' AS "area_pesquisa",
                'Hospital Encore' AS "unidade",
                'HEMODINAMICA' AS "setor"
            FROM 
                USUARIO_PRINCIPAL.atendimento_paciente_v a,
                USUARIO_PRINCIPAL.pessoa_fisica b
            WHERE 
                TRUNC(A.DT_ALTA) = TRUNC(TO_TIMESTAMP(:data, 'YYYY-MM-DD HH24:MI:SS.FF3')) 
                AND a.CD_PESSOA_FISICA = b.cd_pessoa_fisica
                AND a.ie_tipo_atendimento = 8
                AND a.dt_cancelamento IS NULL
                AND a.cd_estabelecimento IN (1, 2, 4)
                AND a.cd_motivo_alta NOT IN (7, 8, 9, 10, 16, 23)
            UNION
            SELECT 
                '40085' AS id_cliente,
                a.DT_ENTRADA AS "data_atendimento",
                a.DT_ALTA AS "data_saida_alta",
                a.NM_MEDICO AS "medico",
                a.NM_PACIENTE as "name",
                b.DS_EMAIL_CCIH AS "email",
                (NVL(b.NR_DDI_CELULAR, '55') || NVL(b.NR_DDD_CELULAR, '') || NVL(b.NR_TELEFONE_CELULAR, '')) AS "phone",
                a.NR_CPF as "cpf",
                'INTERNACAO' AS "area_pesquisa",
                'Hospital Encore' AS "unidade",
                'INTERNACAO' AS "setor"
            FROM 
                USUARIO_PRINCIPAL.atendimento_paciente_v a,
                USUARIO_PRINCIPAL.pessoa_fisica b
            WHERE 
                TRUNC(A.DT_ALTA) = TRUNC(TO_TIMESTAMP(:data, 'YYYY-MM-DD HH24:MI:SS.FF3')) 
                AND a.CD_PESSOA_FISICA = b.cd_pessoa_fisica
                AND a.ie_tipo_atendimento = 1
                AND a.dt_cancelamento IS NULL
                AND a.cd_estabelecimento = 21
                AND a.cd_motivo_alta NOT IN (7, 8, 9, 10, 16, 23)
            UNION
            SELECT 
                '40085' AS id_cliente,
                a.DT_ENTRADA AS "data_atendimento",
                a.DT_ALTA AS "data_saida_alta",
                a.NM_MEDICO AS "medico",
                a.NM_PACIENTE as "name",
                b.DS_EMAIL_CCIH AS "email",
                (NVL(b.NR_DDI_CELULAR, '55') || NVL(b.NR_DDD_CELULAR, '') || NVL(b.NR_TELEFONE_CELULAR, '')) AS "phone",
                a.NR_CPF as "cpf",
                'PRONTO ATENDIMENTO' AS "area_pesquisa",
                'Hospital Encore' AS "unidade",
                'PA ADULTO' AS "setor"
            FROM 
                USUARIO_PRINCIPAL.atendimento_paciente_v a,
                USUARIO_PRINCIPAL.pessoa_fisica b
            WHERE 
                    TRUNC(A.DT_ALTA) = TRUNC(TO_TIMESTAMP(:data, 'YYYY-MM-DD HH24:MI:SS.FF3')) 
                AND a.CD_PESSOA_FISICA = b.cd_pessoa_fisica
                AND a.ie_tipo_atendimento = 3
                AND a.dt_cancelamento IS NULL
                AND a.cd_estabelecimento = 21
                AND a.cd_motivo_alta NOT IN (7, 8, 9, 10, 16, 23)
                AND a.cd_pessoa_fisica NOT IN (
                    SELECT k.cd_pessoa_fisica 
                    FROM USUARIO_PRINCIPAL.atendimento_paciente k 
                    WHERE k.ie_tipo_atendimento = 1 
                    AND k.dt_entrada = TRUNC(TO_TIMESTAMP(:data, 'YYYY-MM-DD HH24:MI:SS.FF3')) 
                )
            ORDER BY 1, 2, 7, 9
        """

        cursor.execute(SQL, {'data': data})

        rows      = cursor.fetchall()
        columns   = [desc[0] for desc in cursor.description]
        df        = pd.DataFrame(rows, columns=columns)
        df["data_saida_alta"] = pd.to_datetime(df["data_saida_alta"]).dt.strftime("%Y-%m-%d %H:%M:%S")
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

