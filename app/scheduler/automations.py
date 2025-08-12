from app.scheduler import schedulers
from app.db.querys import DBHMS

def teste():
    data = [
    {
        "name":"Carlos souza",
        "email":"Car850075@gmailxxx.com",
        "phone":"55961102204",
        "cpf":"01010101"
    },
    {
        "name":"Carlos souza",
        "email":"Ca850075@gmailxxx.com",
        "phone":"55961102204",
        "cpf":"02020202"
    },
    {
        "name":"Carlos souza",
        "email":"Ca8500075@gmailxxx.com",
        "phone":"55961102204",
        "cpf":"03030303"
    }
    ]
    return data

def data_search(db_query, uuid_amb, uuid_exa, uuid_int, uuid_mat, uuid_ps):
    internacao = []
    exames = []
    maternidade = []   
    pronto_socorro = []
    ambulatorio = []
    data_list = db_query.DB()
    for data in data_list:
        if data["Area_Pesquisa"] == "AMBULATORIO":
            ambulatorio.append({**data, "uuid": uuid_amb})
        elif data["Area_Pesquisa"] == "EXAMES":
            exames.append({**data, "uuid": uuid_exa})     
        elif data["Area_Pesquisa"] == "INTERNACAO":
            internacao.append({**data, "uuid": uuid_int})
        elif data["Area_Pesquisa"] == "MATERNIDADE":
            maternidade.append({**data, "uuid": uuid_mat})    
        elif data["Area_Pesquisa"] == "PRONTO_SOCORRO_GERAL":
            pronto_socorro.append({**data, "uuid": uuid_ps})
    return {
        "ambulatorio": ambulatorio,
        "exames": exames,
        "internacao": internacao,
        "maternidade": maternidade,
        "pronto_socorro": pronto_socorro
    }




def start(hospital):
    if hospital == 'HMS':
        db_query = DBHMS
    print("Iniciando automações...")
    data = data_search(db_query=db_query,
                      uuid_amb='e0be9e84-b80e-4f4c-93ca-f947b0a182e0', 
                      uuid_exa='d1f2c3b4-a5b6-7c8d-9e0f-1a2b3c4d5e6f', 
                      uuid_int='12345678-1234-5678-1234-567812345678', 
                      uuid_mat='23456789-2345-6789-2345-678923456789',
                      uuid_ps='34567890-3456-7890-3456-789034567890')

    #schedulers.start_schedulers(data=data["ambulatorio"])
    #schedulers.start_schedulers(data=data["exames"])
    #schedulers.start_schedulers(data=data["internacao"])
    schedulers.start_schedulers(data=data["maternidade"])
    #schedulers.start_schedulers(data=data["pronto_socorro"])

    