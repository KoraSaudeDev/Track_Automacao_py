import logging
from datetime import datetime
from app.scheduler import schedulers
from app.db.querys import ESDB

logging.basicConfig(level=logging.INFO,filename="system.log")


def data_search(hospital, uuid_amb=None, uuid_exa=None, uuid_int=None, uuid_mat=None, uuid_ps=None,uuid_onc=None):
    
    data_list = ESDB.DB(hospital)
    internacao = []
    exames = []
    maternidade = []   
    pronto_socorro = []
    ambulatorio = []
    oncologia = []

    if(data_list == None or len(data_list) == 0):
        print(f"sem dados")
        return
    for data in data_list:
        if data["Area_Pesquisa"] == "AMBULATORIO":
            ambulatorio.append({**data, "uuid": uuid_amb})
        elif data["Area_Pesquisa"] == "EXAMES":
            exames.append({**data, "uuid": uuid_exa})     
        elif data["Area_Pesquisa"] == "INTERNACAO":
            internacao.append({**data, "uuid": uuid_int})
        elif data["Area_Pesquisa"] == "MATERNIDADE":
            maternidade.append({**data, "uuid": uuid_mat})    
        elif data["Area_Pesquisa"] == "PRONTO_SOCORRO_GERAL":
            pronto_socorro.append({**data, "uuid": uuid_ps})
        elif data["Area_Pesquisa"] == "ONCOLOGIA":
           oncologia.append({**data, "uuid": uuid_onc})
    return {
        "ambulatorio": ambulatorio,
        "exames": exames,
        "internacao": internacao,
        "maternidade": maternidade,
        "pronto_socorro": pronto_socorro,
        "oncologia": oncologia  
    }


def start(hospital):

    print("Iniciando automações...")
    data = data_search(hospital=hospital,
                      uuid_amb='e0be9e84-b80e-4f4c-93ca-f947b0a182e0', 
                      uuid_exa='d1f2c3b4-a5b6-7c8d-9e0f-1a2b3c4d5e6f', 
                      uuid_int='12345678-1234-5678-1234-567812345678', 
                      uuid_mat='23456789-2345-6789-2345-678923456789',
                      uuid_ps='a0877963-76f0-4868-9444-8ba21590f676',
                      uuid_onc='a726be1e-7be0-4add-b983-9c0e46a693db'
                      )
    if data is None or len(data) == 0:
        logging.warning(f"[{datetime.now()}] - Sem dados para {hospital}")
        return

    schedulers.start_schedulers(data=data["ambulatorio"])
    schedulers.start_schedulers(data=data["exames"])
    schedulers.start_schedulers(data=data["internacao"])
    schedulers.start_schedulers(data=data["maternidade"])
    schedulers.start_schedulers(data=data["pronto_socorro"])
    schedulers.start_schedulers(data=data["oncologia"])

    