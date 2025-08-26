from datetime import datetime
import logging
import pandas as pd
from io import StringIO


def DB():
    try:
        csv_data = """
            ID_Cliente_Hfocus,data_atendimento,name,email,medico,phone,cpf,area_pesquisa,unidade,setor,uuid
            40085,2024-05-01 12:58:00.000,ADRIANA DAUM MACHADO,adriana.machado@korasaude.com.br,ANDERSON BARBOSA LOUREIRO,5527988188950,124,AMBULATORIO,Meridional Serra,CLINICA GERAL,1358ad90-a68d-4bf1-8dac-db91e83b8764
            40085,2024-05-04 20:43:03.000,CARLOS AUGUSTO SOUZA,carlos.souza@korasaude.com.br,LIA MARCIA MASSINI CANEDO,5596992009957,125,INTERNACAO,Meridional Serra,INTERNACAO,c117421c-8e1f-4bef-a989-3cb1268fcab1
            40085,2024-05-10 12:57:15.000,HENRIQUE RIBAS,henrique.ribas@korasaude.com.br,ANDERSON BARBOSA LOUREIRO,5561999241372,127,EXAMES,Meridional Serra,LABORATORIO,04765111-5c0f-42fe-b393-aff88d0fc256
            40085,2024-05-08 22:47:08.000,KARINA BANDEIRA,karina.bandeira@redemeridional.com.br,FERNANDA BENTO DE OLIVEIRA,5527981385866,130,MATERNIDADE,Meridional Serra,MATERNIDADE,05499245-9f15-4c0e-bde0-8162bbbc5497
            40085,2024-05-09 01:54:56.000,HUGO PASCOAL,hugo.silva@korasaude.com.br,FABIANA LOPES MONTEIRO,5581997480664,131,ONCOLOGIA,Meridional Serra,ONCOLOGIA,ed6bc8b8-fc41-4da9-bf57-b3a2f0b36f66
            40085,2024-05-10 15:39:25.000,VALERIA FRACAROLI,valeria.fracaroli@korasaude.com.br,EDUARDO LUCHI,5527999862526,133,AMBULATORIO,Meridional Serra,INTERNACAO,1358ad90-a68d-4bf1-8dac-db91e83b8764
            """
        df = pd.read_csv(StringIO(csv_data),dtype=str)

        json_str = df.to_dict(orient="records")
        print(f"[{datetime.now()}] querie de teste aplicada {__name__}")
        return json_str
    except Exception as e:
        print(f"[{datetime.now()}] Erro ao aplicar a  query de teste {__name__}: {e}")
        return None


