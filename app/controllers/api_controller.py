from flask import Flask, jsonify
from app.service import track_api


def getSurveys():
    return track_api.getSurveys()

def postDistribution():
   survey_uuid  = "e0be9e84-b80e-4f4c-93ca-f947b0a182e0"
   import_lines = [
        {
            "name":"Carlos souza",
            "email":"Car850075@gmail.com",
            "phone":"55961102204",
            "cpf":"01010101"
        }
   ]
   return track_api.postDistribution(survey_uuid,"email",import_lines)

def postDistributionWhatsapp():
    survey_uuid  = "e0be9e84-b80e-4f4c-93ca-f947b0a182e0"
    import_lines = [
        {
            "name":"Carlos souza",
            "email":"Car850075@gmail.com",
            "phone":"55961102204",
            "cpf":"01010101"
        }
   ]
    