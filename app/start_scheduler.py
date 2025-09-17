from app.scheduler import automations
from app.scheduler import schedulers


#HUB ES:
#HMS - MERIDIONAL SERRA
#HPC - MERIDIONAL PRAIA DA COSTA
#HMV - MERIDIONAL VITORIA
#HMC - MERIDIONAL CARIACICA
#HSF - HOSPITAL SÃO FRANCISCO
#HSL - HOSPITAL SÃO LUIZ
#HMSM - MERIDIONAL SÃO MATEUS

def start_all():
    #hub_es = ['HMS','HMC','HPC','HMV','HSF','HSL','HMSM']
    #ign_oto = ['OTOA', 'OTOSD', 'OTOM', 'OTOS',"ING",]
    #ign_outros = ['HAT','HAC','HPM_HST','HSMC',"ENCORE"]
    
    hospitals = ['HMS','HMC','HPC',
                 'HMSM','HMV','HSL',
                 'HSF','OTOA','OTOSD', 
                 'OTOM','OTOS','HAT',
                 'HAC','HPM','HST','HSMC',
                 "ING","ENCORE"]

    schedulers.schedule_task(hospital=hospitals)

def start_all_teste():
    hospitals = ['HMS','HMC']
    schedulers.schedule_task(hospital=hospitals,teste=hospitals)

