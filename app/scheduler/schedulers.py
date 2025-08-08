from apscheduler.schedulers.background import BackgroundScheduler
from app.service import track_api

scheduler = BackgroundScheduler()

def send_email(data, survey_uuid):
    track_api.postDistribution(survey_uuid, "email", data)

def send_wpp(data, survey_uuid):
    track_api.postDistributionWhatsapp(survey_uuid, "whatsapp", data)

def schedule_task(task_func):
    scheduler.add_job(task_func, 'interval', days=1)
    #scheduler.add_job(task,'interval',seconds=60)
    
def start_schedulers(data, survey_uuid):
    schedule_task(lambda: send_email(data, survey_uuid))
    schedule_task(lambda: send_wpp(data, survey_uuid))
    print("Tarefa agendada")
    scheduler.start()
    





    
    
