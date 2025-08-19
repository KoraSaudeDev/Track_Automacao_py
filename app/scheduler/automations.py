import logging
from datetime import datetime
from app.scheduler import schedulers
from app.db.querys import ESDB,ING_OTO,HAT
from app.db.querys.HUB_ES import HMC, HMS, HPC, HMV, HSF, HSL, HMSM

logging.basicConfig(level=logging.INFO,filename="system.log")


def data_search(hospital, uuid_amb=None, uuid_exa=None, uuid_int=None, uuid_mat=None, uuid_ps=None,uuid_onc=None):
    
    if hospital in 'HMS':
        dbHospital = HMS
    elif hospital == 'HMC':
        dbHospital = HMC
    elif hospital == 'HPC':
        dbHospital = HPC
    elif hospital == 'HMV':
        dbHospital = HMV
    elif hospital == 'HSF':
        dbHospital = HSF
    elif hospital == 'HSL':
        dbHospital = HMSM
    elif hospital == 'HMSM':
        dbHospital = HSL
    elif hospital == 'OTO_ING':
        dbHospital = ING_OTO
    elif hospital == 'HAT':
        dbHospital = HAT

    data_list = dbHospital.DB()
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
        if data["area_pesquisa"] == "AMBULATORIO":
            ambulatorio.append({**data, "uuid": uuid_amb})
        elif data["area_pesquisa"] == "EXAMES":
            exames.append({**data, "uuid": uuid_exa})     
        elif data["area_pesquisa"] == "INTERNACAO":
            internacao.append({**data, "uuid": uuid_int})
        elif data["area_pesquisa"] == "MATERNIDADE":
            maternidade.append({**data, "uuid": uuid_mat})    
        elif data["area_pesquisa"] == "PRONTO_SOCORRO_GERAL":
            pronto_socorro.append({**data, "uuid": uuid_ps})
        elif data["area_pesquisa"] == "ONCOLOGIA":
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
                      uuid_amb='913ef30e-6e75-45b6-acdd-eb78e1bb4626', 
                      uuid_exa='ed7bd007-0dd9-4b0d-9e08-c0dbf2cdfb3c', 
                      uuid_int='2a2b33c5-a390-47c7-8914-48a396ced12b', 
                      uuid_mat='291ac361-6ee5-4054-9a53-22653fbf2728',
                      uuid_ps='a0877963-76f0-4868-9444-8ba21590f676',
                      uuid_onc='0eced015-e625-4381-9ae3-1ecaf6bf5320'
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

    