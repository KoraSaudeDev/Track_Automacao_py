import logging
from datetime import datetime
from apscheduler.schedulers.background import BackgroundScheduler
from app.service import track_api

logging.basicConfig(level=logging.INFO,filename="system.log")

scheduler = BackgroundScheduler()

def send_email(data, survey_uuid,template=None):
    track_api.postDistribution(survey_uuid, "email", data,template)

#def send_wpp(data, survey_uuid):
#    track_api.postDistributionWhatsapp(survey_uuid, "whatsapp", data)

def send_teste(data, survey_uuid):
    track_api.postImportLines(survey_uuid,data)

def schedule_task(task_func):
    #scheduler.add_job(task_func, 'interval', days=1)
    scheduler.add_job(task_func,'interval',seconds=120)
    
def start_hospital_scheduler(hospital, template=None, teste=None):
    def task_wrapper():
        try:
            from app.scheduler.automations import data_search
            fresh = data_search(hospital=hospital, teste=teste)
            if not fresh:
                logging.warning(f"[{datetime.now()}] - {hospital} - sem dados")
                return
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
                send_email(data, survey_uuid, template)
                print(f"{hospital} - {area} - Disparo agendado!")
        except Exception as e:
            logging.error(f"[{datetime.now()}] - Erro ao executar tarefa do hospital {hospital}: {e}")

    schedule_task(task_wrapper)

    logging.warning(f"[{datetime.now()}] - {hospital} - Disparo único por hospital agendado!")
    print(f"{hospital} - schedulers (único por hospital) iniciado")
    if not scheduler.running:
        scheduler.start()
    else:
        logging.warning("Scheduler já estava rodando, task adicionados normalmente.")
    





    
    
