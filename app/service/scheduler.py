from apscheduler.schedulers.background import BackgroundScheduler

def schedule_task(task):
    scheduler = BackgroundScheduler()
    scheduler.add_job(task,'interval',days=1)
    #scheduler.add_job(task,'interval',seconds=60)
    print("O job ta rodando!!")
    scheduler.start()