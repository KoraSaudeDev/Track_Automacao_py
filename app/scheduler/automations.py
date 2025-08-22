import logging
from datetime import datetime
from app.scheduler import schedulers
from app.db.querys_mv import ING_OTO,HAT
from app.service.survey_uuid import get_survey_uuid
from app.db.querys_mv.HUB_ES import HMC, HMS, HPC, HMV, HSF, HSL, HMSM
from app.db.querys_tasy import HAC,HPM_HST,HSMC

logging.basicConfig(level=logging.INFO,filename="system.log")

def data_search(hospital):
    
    uuid_amb = get_survey_uuid(hospital)["ambulatorio"]
    uuid_exa = get_survey_uuid(hospital)["exames"]
    uuid_int = get_survey_uuid(hospital)["internacao"]  
    uuid_mat = get_survey_uuid(hospital)["maternidade"]
    uuid_ps = get_survey_uuid(hospital)["pronto_socorro"]
    uuid_onc = get_survey_uuid(hospital)["oncologia"]
    
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
        dbHospital = HSL
    elif hospital == 'HMSM':
        dbHospital = HMSM
    elif hospital == 'OTO_ING':
        dbHospital = ING_OTO
    elif hospital == 'HAT':
        dbHospital = HAT
    elif hospital == 'HAC':
        dbHospital = HAC 
    elif hospital == 'HPM_HST':
        dbHospital = HPM_HST
    elif hospital == 'HSMC':    
        dbHospital = HSMC
 

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
        elif data["area_pesquisa"] == "PRONTO SOCORRO GERAL":
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

    data = data_search(hospital=hospital)
    if data is None or len(data) == 0:
        logging.warning(f"[{datetime.now()}] - Sem dados para {hospital}")
        return

    schedulers.start_schedulers(data=data["ambulatorio"])
    schedulers.start_schedulers(data=data["exames"])
    schedulers.start_schedulers(data=data["internacao"])
    schedulers.start_schedulers(data=data["maternidade"])
    schedulers.start_schedulers(data=data["pronto_socorro"])
    schedulers.start_schedulers(data=data["oncologia"])

    