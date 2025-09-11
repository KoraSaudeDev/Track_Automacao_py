import logging
from datetime import datetime
from apscheduler.schedulers.background import BackgroundScheduler
from app.scheduler.automations import data_search
from app.service.survey_uuid import  get_template
from app.service import track_api

logging.basicConfig(level=logging.INFO,filename="system.log")

scheduler = BackgroundScheduler()

def send_email(data, survey_uuid,template=None):
    track_api.postDistribution(survey_uuid, "email", data,template)

#def send_wpp(data, survey_uuid):
#    track_api.postDistributionWhatsapp(survey_uuid, "whatsapp", data)

def send_teste(data, survey_uuid):
    track_api.postImportLines(survey_uuid,data)

def start_hospital_scheduler(hospital, template=None, teste=None):
        try:
            if hospital is None or len(hospital) == 0:
                hospital = ['HMS','HMC','HPC',
                 'HMSM','HMV','HSL',
                 'HSF','OTOA','OTOSD', 
                 'OTOM','OTOS','HAT',
                 'HAC','HPM_HST','HSMC',
                 "ING","ENCORE"]
                
            for h in hospital:
                fresh = data_search(hospital=h, teste=teste)
                template = get_template(h)
                if not fresh:
                    logging.warning(f"[{datetime.now()}] - {h} - sem dados")
                    continue
                for area in [
                    "ambulatorio",
                    "exames",
                    "internacao",
                    "maternidade",
                    "pronto_socorro",
                    "oncologia",
                ]:
                    data = fresh.get(area) if isinstance(fresh, dict) else None
                    if not data:
                        continue
                    survey_uuid = data[0]['uuid']
                    #send_email(data, survey_uuid, template)
                    print(f"{h} - {area} - {survey_uuid} - Disparo agendado!")
        except Exception as e:
            logging.error(f"[{datetime.now()}] - Erro ao executar tarefa do hospital {h}: {e}")



def schedule_task(hospital, template=None, teste=None):
    #scheduler.add_job(task_func, 'interval', days=1)
    scheduler.add_job(start_hospital_scheduler,'interval',seconds=600,kwargs={"hospital":hospital,"template":template,"teste":teste})
    if not scheduler.running:
        scheduler.start()
    else:
        logging.warning("Scheduler já estava rodando, task adicionados normalmente.")




    
    
