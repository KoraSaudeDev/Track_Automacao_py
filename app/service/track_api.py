import os
import requests
from datetime import datetime
from dotenv import load_dotenv 
from flask import jsonify



url_api = "https://api.track.co"
ORGANIZATION_UUID = os.getenv("ORGANIZATION_UUI")
API_TOKEN = os.getenv("API_TOKEN")

def getSurveys():
    url = f"{url_api}/v1/organizations/{ORGANIZATION_UUID}/surveys"
    headers = {
        "Authorization": f"Bearer {API_TOKEN}"
    }
    response = requests.request("GET",url,headers=headers)
    try:
        return response.json()
    except Exception as e:
        return print(f"Erro na API: {e}")

def postDistribution(survey_uuid,distribution_channel,import_lines):
    url = f"{url_api}/v1/organizations/{ORGANIZATION_UUID}/distributions"
    headers = {
        "Authorization": f"Bearer {API_TOKEN}"
    }
    data = {
        "survey_uuid":survey_uuid,
        "distribution_channel":distribution_channel,
        "import_lines":import_lines     
    }
    
    response = requests.request("POST",url=url,headers=headers,json=data)
    try:
        response.raise_for_status()
        return print("Pesquisa enviada com sucesso para o email! "+str(datetime.now()))
    except Exception as e:
        return print("Erro: " + e)

def postDistributionWhatsapp(survey_uuid,distribution_channel,import_lines): 
    url = f"{url_api}/v1/organizations/{ORGANIZATION_UUID}/distributions"
    headers = {
        "Authorization": f"Bearer {API_TOKEN}"
    }   
    data = {
        "survey_uuid":survey_uuid,
        "distribution_channel":distribution_channel,
        "import_lines":import_lines,
        "whatsapp_template": {
            "name": "template-nome-exemplo", #nome do template
            "language": "pt_BR", #idioma do template
            "variables": ["customer.name", "interaction.produto"], #variáveis presentes no template
            "id_provider": "ID do template" #id do template, solicitar ao time de suporte da Track
        },
            "whatsapp_integration_uuid": "a726be1e-7be0-4add-b983-9c0e46a693db"#uuid fixo da integração      
    }
    response = requests.request("POST",url=url,headers=headers,json=data)
    try:
        response.raise_for_status()
        return print("Pesquisa enviada com sucesso para o Whatsapp! "+str(datetime.now()))
    except Exception as e:
        return print("Erro: " + e)
    
