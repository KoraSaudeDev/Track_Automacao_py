import logging
from datetime import datetime
from app.scheduler import schedulers
from app.service.survey_uuid import get_survey_uuid,get_hospital,get_hospital_teste



logging.basicConfig(level=logging.INFO,filename="system.log")

def data_search(hospital,teste=None):
    
    uuid_amb = get_survey_uuid(hospital)["ambulatorio"]
    uuid_exa = get_survey_uuid(hospital)["exames"]
    uuid_int = get_survey_uuid(hospital)["internacao"]  
    uuid_mat = get_survey_uuid(hospital)["maternidade"]
    uuid_ps = get_survey_uuid(hospital)["pronto_socorro"]
    uuid_onc = get_survey_uuid(hospital)["oncologia"]
    
    dbHospital = get_hospital().get(hospital)
    if dbHospital is None:
        logging.warning(f"[{datetime.now()}] - Hospital {hospital} não encontrado.")
        return None

    data_list = dbHospital.DB()
    
    if teste is not None:
        dbHospital_teste = get_hospital_teste().get(teste)
        if dbHospital_teste is None:
            logging.warning(f"[{datetime.now()}] - Hospital de teste {teste} não encontrado.")
            return None
        data_list = dbHospital_teste.DB()

    internacao = []
    exames = []
    maternidade = []   
    pronto_socorro = []
    ambulatorio = []
    oncologia = []

    if(data_list == None or len(data_list) == 0):
        logging.warning(f"sem dados no hostpital: {hospital}")
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

def start_teste():
    data_hms = data_search(hospital="HMS",teste="HMS")
    data_hmc = data_search(hospital="HMC",teste="HMC")

    schedulers.start_schedulers(data=data_hms["ambulatorio"])
    schedulers.start_schedulers(data=data_hms["exames"])
    schedulers.start_schedulers(data=data_hms["internacao"])
    schedulers.start_schedulers(data=data_hms["maternidade"])
    schedulers.start_schedulers(data=data_hms["pronto_socorro"])
    schedulers.start_schedulers(data=data_hms["oncologia"])

    schedulers.start_schedulers(data=data_hmc["ambulatorio"])
    schedulers.start_schedulers(data=data_hmc["exames"])
    schedulers.start_schedulers(data=data_hmc["internacao"])
    schedulers.start_schedulers(data=data_hmc["maternidade"])
    schedulers.start_schedulers(data=data_hmc["pronto_socorro"])
    schedulers.start_schedulers(data=data_hmc["oncologia"])
   
    