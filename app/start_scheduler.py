from app.scheduler import automations

#HUB ES:
#HMS - MERIDIONAL SERRA
#HPC - MERIDIONAL PRAIA DA COSTA
#HMV - MERIDIONAL VITORIA
#HMC - MERIDIONAL CARIACICA
#HSF - HOSPITAL SÃO FRANCISCO
#HSL - HOSPITAL SÃO LUIZ
#HMSM - MERIDIONAL SÃO MATEUS

def start_all():
    hospitals = ['HMS','HMC','HPC',
                 'HMSM','HMV','HSL',
                 'HSF','OTO_ING',
                 'HAT','HAC','HPM_HST',
                 'HSMC']

    for autom in hospitals:
        automations.start(autom)

def start_all_teste():
    hospitals = ['HMS','HMC']

    for autom in hospitals:
        automations.start_teste(autom)

