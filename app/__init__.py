import os
from flask import Flask
from flask_cors import CORS
from .routes.api_router import track_bp
from app.scheduler import automations

#HUB ES:
#HMS - MERIDIONAL SERRA
#HPC - MERIDIONAL PRAIA DA COSTA
#HMV - MERIDIONAL VITORIA
#HMC - MERIDIONAL CARIACICA
#HSF - HOSPITAL SÃO FRANCISCO
#HSL - HOSPITAL SÃO LUIZ
#HMSM - MERIDIONAL SÃO MATEUS

automations.start('HMS')
automations.start('HMC')
automations.start('HPC')
automations.start('HMSM')
automations.start('HMV')
automations.start('HSL')
automations.start('HSF')
#automations.start('OTO_ING')
automations.start('HAT')
automations.start('HAC')
automations.start('HPM_HST')
automations.start('HSMC')

#automations.start_teste('HMS')
#automations.start_teste('HMC')

def create_app():
    app = Flask(__name__)
    
    app.register_blueprint(track_bp)
    
    return app