import os
import json
import requests
import logging
from datetime import datetime
from app.service.calc_d1 import get_dates_reminder
logging.basicConfig(level=logging.INFO,filename="system.log")

url_api = "https://api.track.co"
ORGANIZATION_UUID = os.getenv("ORGANIZATION_UUID")
API_TOKEN = os.getenv("API_TOKEN")

def postDistribution(survey_uuid,distribution_channel,import_lines):
    url = f"{url_api}/v1/organizations/{ORGANIZATION_UUID}/distributions"
    headers = {
        "Authorization": f"Bearer {API_TOKEN}"
    }
    data = {
        "survey_uuid":survey_uuid,
        "distribution_channel":"email",
        "reminder":"whatsapp",
        "validity_at":get_dates_reminder(14),
        "reminder_at":get_dates_reminder(2),
        "import_lines":import_lines,   
        "whatsapp_reminder_template": {
            "name": "templatev1",
            "language": "pt_BR",
            "variables": ["customer.name"],
            "id_provider": "HX1a01a858bf1894eaa0053240f6a7ad84"
            },
        "whatsapp_integration_uuid": "a726be1e-7be0-4add-b983-9c0e46a693db"
 
    }
    #payload = json.dumps(data, ensure_ascii=False)
    
    try:
        response = requests.post(url, headers={**headers, "Content-Type": "application/json"}, json=data)
    
        print(f"[{datetime.now()}] Pesquisa enviada com sucesso para o email! [{response}]")
        logging.info(f"[{datetime.now()}] Pesquisa enviada com sucesso para o email! [{response}]")
        return 
    except Exception as e:
        print(logging.error(f"[{datetime.now()}] Erro na API: {e}"))
        logging.error(f"[{datetime.now()}] Erro na API: {e}")
        return 

    
def postImportLines(survey_uuid,import_lines):
   url = f"{url_api}/v1/organizations/{ORGANIZATION_UUID}/distributions/createLinkList"
   headers = {
       "Authorization": f"Bearer {API_TOKEN}"
   }
   data = {
       "survey_uuid":survey_uuid,
       "async": False,
       "shortened_link": False,
       "import_lines":import_lines,     
   }
   try:
       response = requests.request("POST",url=url,headers=headers,json=data)
       logging.info("Cliente selecionado "+str(datetime.now()))
       return response.json()
   except Exception as e:
       logging.error(f"Erro na API: {e}")
       return   
   
#def postDistributionWhatsapp(survey_uuid,distribution_channel,import_lines): 
#    url = f"{url_api}/v1/organizations/{ORGANIZATION_UUID}/distributions"
#    headers = {
#        "Authorization": f"Bearer {API_TOKEN}"
#    }   
#    data = {
#        "survey_uuid":survey_uuid,
#        "distribution_channel":distribution_channel,
#        "import_lines":import_lines,
#        "whatsapp_template": {
#            "name": "template-nome-exemplo", #nome do template
#            "language": "pt_BR", #idioma do template
#            "variables": ["customer.name", "interaction.produto"], #variáveis presentes no template
#            "id_provider": "ID do template" #id do template, solicitar ao time de suporte da Track
#        },
#            "whatsapp_integration_uuid": "a726be1e-7be0-4add-b983-9c0e46a693db"#uuid fixo da integração      
#    }
#    try:
#        response = requests.request("POST",url=url,headers=headers,json=data)
#        response.raise_for_status()
#        logging.info(f"[{datetime.now()}] Pesquisa enviada com sucesso para o Whatsapp! [{response}]")
#        return
#    except Exception as e:
#        logging.error(f"[{datetime.now()}] Erro na API: {e}")
#        return 