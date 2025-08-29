from datetime import datetime
import logging
import pandas as pd
from io import StringIO


def DB():
    try:
        csv_data = """
            ID_Cliente_Hfocus,data_atendimento,name,email,medico,phone,cpf,area_pesquisa,unidade,setor
            40085,2024-05-01 11:46:00.000,HUGO PIMENTEL XAVIER,hugo.xavier@korasaude.com.br,THARCISIO GE DE OLIVEIRA,5527999076977,123,AMBULATORIO,Meridional Cariacica,CLINICA GERAL
            40085,2024-05-06 19:46:07.000,DANIEL TANNURI ANDRADE,daniel.andrade@korasaude.com.br,LUIS HENRIQUE BARBOSA BORGES,5527992315665,126,INTERNACAO,Meridional Cariacica,INTERNACAO
            40085,2024-05-10 06:05:02.000,LUCIANA GOMES GASTALDI,luciana.gastaldi@korasaude.com.br,GUSTAVO MIRANDA VIEIRA,5527998193577,128,INTERNACAO,Meridional Cariacica,INTERNACAO
            40085,2024-05-10 12:24:06.000,PEDRO LUCAS DE SOUZA,pedro.souza@korasaude.com.br,THARCISIO GE DE OLIVEIRA,5585986460402,129,PRONTO SOCORRO GERAL,Meridional Cariacica,PA_ADULTO
            40085,2024-05-06 23:12:22.000,RAFAEL GARBELINI,rafaelgarbelini@indecx.com.br,ULYSSES CAUS BATISTA,5531997522569,132,INTERNACAO,Meridional Cariacica,INTERNACAO
            40085,2024-05-09 09:20:58.000,GEOVANA BARCELLOS RODY,geovana.barcellos@korasaude.com.br,LIA MARCIA MASSINI CANEDO,5527997191631,134,INTERNACAO,Meridional Cariacica,INTERNACAO
            """
        df = pd.read_csv(StringIO(csv_data),dtype=str)

        json_str = df.to_dict(orient="records")
        print(f"[{datetime.now()}] querie de teste aplicada {__name__}")
        return json_str
    except Exception as e:
        print(f"[{datetime.now()}] Erro ao aplicar a  query de teste {__name__}: {e}")
        return None


