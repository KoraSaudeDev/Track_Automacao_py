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
    scheduler.add_job(task_func,'interval',seconds=60)
    
def start_schedulers(hospital, area, template=None, teste=None):
    # A cada execução, buscar dados atualizados do banco
    def task_wrapper():
        try:
            from app.scheduler.automations import data_search
            fresh = data_search(hospital=hospital, teste=teste)
            if not fresh or area not in fresh:
                logging.warning(f"[{datetime.now()}] - {hospital} - {area} - sem dados")
                return
            data = fresh[area]
            if not data:
                logging.warning(f"[{datetime.now()}] - {hospital} - {area} - sem dados")
                return
            survey_uuid = data[0]['uuid']
            send_email(data, survey_uuid, template)
        except Exception as e:
            logging.error(f"[{datetime.now()}] - Erro ao executar tarefa {hospital} - {area}: {e}")

    schedule_task(task_wrapper)

    logging.warning(f"[{datetime.now()}] - {hospital} - {area} - Disparo agendado!")
    print(f"{hospital} - {area} -  schedulers iniciado")
    if not scheduler.running:
        scheduler.start()
    else:
        logging.warning("Scheduler já estava rodando, task adicionados normalmente.")
    





    
    
