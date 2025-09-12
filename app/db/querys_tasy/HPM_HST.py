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
        conn     = db.get_connection_tasy("HPM_HST")
        cursor   = conn.cursor()

        data     = get_filtered_dates()[0]

        SQL = """
            select '40085'
            ID_Cliente_Hfocus,
            a.DT_ENTRADA AS "data_atendimento",
            a.DT_ALTA AS "data_saida_alta",
            a.NR_ATENDIMENTO AS "cd_atendimento",
            m.NM_PESSOA_FISICA AS "medico",
            tasy.obter_nome_paciente(a.nr_atendimento) AS "name",
            tasy.obter_email_pf_hpm(a.cd_pessoa_fisica) AS "email",
            ('55' || ltrim(replace( translate(tasy.obter_telefone_pf(a.cd_pessoa_fisica, 12),translate(tasy.obter_telefone_pf(a.cd_pessoa_fisica, 12), '1234567890', ' '),' '),' ', ''))) AS "phone",
            tasy.obter_cpf_pessoa_fisica(a.cd_pessoa_fisica)"cpf",
                    case
                    when a.ie_tipo_atendimento = 3 then 'PRONTO_SOCORRO_GERAL'
                    when a.ie_tipo_atendimento = 1 then 'INTERNACAO'
                    when a.ie_tipo_atendimento = 7 then 'INTERNACAO'
                    when tasy.obter_primeiro_setor_atend(a.nr_atendimento,'C') IN (151, 164,271,269) then 'ONCOLOGIA'
                    when a.ie_tipo_atendimento = 8 and tasy.obter_primeiro_setor_atend(a.nr_atendimento,'C') not IN (151, 164,271,269) then 'AMBULATORIO'
                    when tasy.obter_primeiro_setor_atend(a.nr_atendimento,'C') IN 154 then 'AMBULATORIO'
                    end "area_pesquisa",
                    case 
                        when a.cd_Estabelecimento in (1,71) then 'Hospital Palmas Medical' 
                        when a.cd_Estabelecimento in 81 then 'Hospital Santa Thereza'
                    end 
                    AS "unidade",
                    case
                        when a.ie_tipo_atendimento = 3 THEN 'PA_ADULTO'
                    when a.ie_tipo_atendimento = 1 THEN 'INTERNACAO'
                    when a.ie_tipo_atendimento = 7 then 'INTERNACAO'
                    when a.ie_tipo_atendimento = 8 and tasy.obter_primeiro_setor_atend(a.nr_atendimento,'C') not IN (151, 164,271,269)  then 'GERAL_AMBULATORIO'
                    when tasy.obter_primeiro_setor_atend(a.nr_atendimento,'C') IN 154 then 'GERAL_AMBULATORIO'
                    when tasy.obter_primeiro_setor_atend(a.nr_atendimento,'C') IN (151, 164,271,269) then 'ONCOLOGIA'
                    END AS "setor"
                        FROM 
            TASY.atendimento_paciente a
            INNER JOIN TASY.pessoa_fisica m ON a.CD_MEDICO_RESP = m.CD_PESSOA_FISICA
            where trunc(a.DT_ALTA)>= TRUNC(TO_TIMESTAMP(:data, 'YYYY-MM-DD HH24:MI:SS.FF3')) -3
            and  trunc(a.DT_ALTA) < TRUNC(TO_TIMESTAMP(:data, 'YYYY-MM-DD HH24:MI:SS.FF3'))
            and a.dt_cancelamento is null
            and a.cd_estabelecimento in (1,71,81)
            and   a.cd_motivo_alta not in (18,13,9,7,16,15)
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

