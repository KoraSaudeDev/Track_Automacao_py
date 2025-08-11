from app.scheduler import schedulers
from app.db.querys.HMS import ambulatorio, exames, internacao, maternidade

def teste():
    data = [
    {
        "name":"Carlos souza",
        "email":"Car850075@gmail.com",
        "phone":"55961102204",
        "cpf":"01010101"
    },
    {
        "name":"Carlos souza",
        "email":"Ca850075@gmail.com",
        "phone":"55961102204",
        "cpf":"02020202"
    },
    {
        "name":"Carlos souza",
        "email":"Ca8500075@gmail.com",
        "phone":"55961102204",
        "cpf":"02020202"
    }
    ]
    return data

def start():
    schedulers.start_schedulers(data=teste(), survey_uuid="e0be9e84-b80e-4f4c-93ca-f947b0a182e0")