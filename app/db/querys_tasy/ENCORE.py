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
                '40085' as ID_Cliente_Hfocus, 
                a.nr_atendimento AS "cd_atendimento",
                a.DT_ENTRADA AS "data_atendimento",
                a.DT_ALTA AS "data_saida_alta",
                a.NM_MEDICO AS "medico",
                a.NM_PACIENTE as "name",
                UPPER(USUARIO_PRINCIPAL.obter_compl_pf(a.CD_PESSOA_FISICA,1,'M')) AS "email",
                '55' || REGEXP_REPLACE(USUARIO_PRINCIPAL.obter_telefone_pf(a.cd_pessoa_fisica, 12), '[^0-9]', '') AS "phone",
                a.NR_CPF as "cpf",
                CASE 
                    WHEN a.nr_seq_classificacao = 1 THEN 'AMBULATORIO'
                    WHEN a.nr_seq_classificacao <> 1 THEN 'EXAMES'
                    ELSE 'OUTROS' 
                END AS "area_pesquisa",
                USUARIO_PRINCIPAL.obter_nome_fantasia_estab(a.cd_estabelecimento) AS "unidade",
                CASE 
                    WHEN a.nr_seq_classificacao = 1 THEN 'AMBULATORIO'
                    WHEN a.cd_setor_atendimento = 357 THEN 'LABORATORIO'
                    WHEN a.cd_setor_atendimento IN (353, 354, 365, 405) THEN 'IMAGEM'
                    WHEN a.cd_setor_atendimento IN (369, 370, 355) THEN 'EXAMES'
                    ELSE 'OUTROS' 
                END AS "setor"
            FROM 
                USUARIO_PRINCIPAL.atendimento_paciente_v a
            WHERE 
                a.dt_entrada BETWEEN TRUNC(SYSDATE - 1) AND TRUNC(SYSDATE) - 1 / 86400
                AND a.ie_tipo_atendimento NOT IN (1, 3)
                AND a.dt_cancelamento IS NULL
                AND a.cd_estabelecimento = 21
            UNION
            SELECT 
                '40085' as ID_Cliente_Hfocus, 
                a.nr_atendimento AS "cd_atendimento",
                a.DT_ENTRADA AS "data_atendimento",
                a.DT_ALTA AS "data_saida_alta",
                a.NM_MEDICO AS "medico",
                a.NM_PACIENTE as "name",
                UPPER(USUARIO_PRINCIPAL.obter_compl_pf(a.CD_PESSOA_FISICA,1,'M')) AS "email",
                '55' || REGEXP_REPLACE(USUARIO_PRINCIPAL.obter_telefone_pf(a.cd_pessoa_fisica, 12), '[^0-9]', '') AS "phone",
                a.NR_CPF as "cpf",
                'EXAMES' AS "area_pesquisa",
                USUARIO_PRINCIPAL.obter_nome_fantasia_estab(21) AS "unidade",
                'HEMODINAMICA' AS "setor"
            FROM 
                USUARIO_PRINCIPAL.atendimento_paciente_v a
            WHERE 
                a.dt_alta BETWEEN TRUNC(SYSDATE - 1) AND TRUNC(SYSDATE)
                AND a.ie_tipo_atendimento = 8
                AND a.dt_cancelamento IS NULL
                AND a.cd_estabelecimento IN (1, 2, 4)
                AND a.cd_motivo_alta NOT IN (7, 8, 9, 10, 16, 23)
            UNION
            SELECT 
                '40085' as ID_Cliente_Hfocus, 
                a.nr_atendimento AS "cd_atendimento",
                a.DT_ENTRADA AS "data_atendimento",
                a.DT_ALTA AS "data_saida_alta",
                a.NM_MEDICO AS "medico",
                a.NM_PACIENTE as "name",
                UPPER(USUARIO_PRINCIPAL.obter_compl_pf(a.CD_PESSOA_FISICA,1,'M')) AS "email",
                '55' || REGEXP_REPLACE(USUARIO_PRINCIPAL.obter_telefone_pf(a.cd_pessoa_fisica, 12), '[^0-9]', '') AS "phone",
                a.NR_CPF as "cpf",
                'INTERNACAO' AS "area_pesquisa",
                USUARIO_PRINCIPAL.obter_nome_fantasia_estab(a.cd_estabelecimento) AS "unidade",
                'INTERNACAO' AS "setor"
            FROM 
                USUARIO_PRINCIPAL.atendimento_paciente_v a
            WHERE 
                a.dt_alta BETWEEN TRUNC(SYSDATE - 2) AND TRUNC(SYSDATE - 1)
                AND a.ie_tipo_atendimento = 1
                AND a.dt_cancelamento IS NULL
                AND a.cd_estabelecimento = 21
                AND a.cd_motivo_alta NOT IN (7, 8, 9, 10, 16, 23)
            UNION
            SELECT 
                '40085' as ID_Cliente_Hfocus, 
                a.nr_atendimento AS "cd_atendimento",
                a.DT_ENTRADA AS "data_atendimento",
                a.DT_ALTA AS "data_saida_alta",
                a.NM_MEDICO AS "medico",
                a.NM_PACIENTE as "name",
                UPPER(USUARIO_PRINCIPAL.obter_compl_pf(a.CD_PESSOA_FISICA,1,'M')) AS "email",
                '55' || REGEXP_REPLACE(USUARIO_PRINCIPAL.obter_telefone_pf(a.cd_pessoa_fisica, 12), '[^0-9]', '') AS "phone",
                a.NR_CPF as "cpf",
                'PRONTO_SOCORRO_GERAL' AS "area_pesquisa",
                USUARIO_PRINCIPAL.obter_nome_fantasia_estab(a.cd_estabelecimento) AS "unidade",
                'PA ADULTO' AS "setor"
            FROM 
                USUARIO_PRINCIPAL.atendimento_paciente_v a
            WHERE 
                a.dt_alta BETWEEN TRUNC(SYSDATE - 1) AND TRUNC(SYSDATE)
                AND a.ie_tipo_atendimento = 3
                AND a.dt_cancelamento IS NULL
                AND a.cd_estabelecimento = 21
                AND a.cd_motivo_alta NOT IN (7, 8, 9, 10, 16, 23)
                AND a.cd_pessoa_fisica NOT IN (
                    SELECT k.cd_pessoa_fisica 
                    FROM USUARIO_PRINCIPAL.atendimento_paciente k 
                    WHERE k.ie_tipo_atendimento = 1 
                    AND k.dt_entrada BETWEEN TRUNC(SYSDATE - 2) AND TRUNC(SYSDATE)
                )
            ORDER BY 1, 2, 7, 9
        """

        #cursor.execute(SQL, {'data': data})

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

