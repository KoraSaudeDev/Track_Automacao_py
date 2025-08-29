from app.db.querys_mv.HUB_ES import HMC, HMS, HPC, HMV, HSF, HSL, HMSM
from app.db.querys_mv import ING_OTO,HAT
from app.db.querys_tasy import HAC,HPM_HST,HSMC
import app.db.teste as teste

def get_survey_uuid(hospital):
    if hospital == 'HMC':
        return{
            "internacao": "c117421c-8e1f-4bef-a989-3cb1268fcab1",
            "ambulatorio": "1358ad90-a68d-4bf1-8dac-db91e83b8764",
            "exames": "04765111-5c0f-42fe-b393-aff88d0fc256",
            "oncologia": "ed6bc8b8-fc41-4da9-bf57-b3a2f0b36f66",
            "pronto_socorro": "a6536898-7b56-4bf4-a915-efd7e102ef2a",
            "maternidade": "05499245-9f15-4c0e-bde0-8162bbbc5497"
        }

    elif hospital == 'HMS':
        return{
            "internacao": "8c3a2b98-10ab-4abd-a426-89d34d3d997d",
            "ambulatorio": "583d2b47-1363-4cf9-b88c-4be4c0014442",
            "exames": "bc0b7fdd-251e-4c86-b5ef-69f59b9d929b",
            "oncologia": "420072ca-b16c-4542-90c1-807df10de0ed",
            "pronto_socorro": "bbce4d04-8964-4079-b7b0-794d55f6e310",
            "maternidade": "fd5a9832-1591-43d3-9bc2-152f654bd3d6"
        }

    elif hospital == 'HMV':
        return{
            "internacao": "6db17ddd-49ed-4cdc-aa06-816732b2861a",
            "ambulatorio": "c3dfc880-3cd4-4e65-b902-cdacb24c7b50",
            "exames": "330ea217-dd82-4aea-aaa6-1c1b186fa1ab",
            "oncologia": "054aa1cd-4e57-4a7d-a781-623552068299",
            "pronto_socorro": "2b53c258-5b6b-43ac-bb0b-f4d2de34fe32",
            "maternidade": "7859c123-9b0a-4899-8d4a-ff0d8564a8f8"
        }


    elif hospital == 'HPC':
        return{
            "internacao": "06a391b6-6cda-4911-8fd6-9b3f7a7b895b",
            "ambulatorio": "df7ef61d-1859-4d97-8f23-4bc8f09ebbbd",
            "exames": "3e115a0e-f2f6-4dbf-a80c-8a24276acbc5",
            "oncologia": "e1781a74-a3c6-4281-bcd7-24fd01e79df5",
            "pronto_socorro": "36452ce8-75c4-4c71-90fd-e82a96822895",
            "maternidade": "582599e1-4e25-490d-b2ac-f43be9744040"
        }


    elif hospital == 'HSF':
        return{
            "internacao": "f938e052-0a65-4fe6-a941-3574dc155273",
            "ambulatorio": "07c0dc0a-cf27-470f-8e5c-52e8597df106",
            "exames": "66b25d71-aba9-4e74-9fc7-08f03bdf908a",
            "oncologia": "6ddc29db-db6d-4420-a89b-407aeb8b3e04",
            "pronto_socorro": "a73f7919-6f77-4fda-aa27-e4fbce7a0701",
            "maternidade": "f80c0cca-5d6e-46c1-a799-5bfec45a51d6"
        }


    elif hospital == 'HSL':
        return{
            "internacao": "db77f9d2-7b13-4558-81a4-98ffbe501eba",
            "ambulatorio": "7ae3c90e-a23f-44d0-9252-db0eed60c510",
            "exames": "4b69fc81-af23-495f-9824-2922bebc8636",
            "oncologia": "07692245-4ab3-4d5e-ac5d-d55fb4401e89",
            "pronto_socorro": "7ec7999c-12f9-464f-8db8-d25b33af1231",
            "maternidade": "e1df9d2f-2019-445a-92cd-97acc2468041"
        }


    elif hospital == 'HMSM':
        return{
            "internacao": "7f00b996-08f5-43d3-a8a2-569821b75d84",
            "ambulatorio": "1b1e5cc5-08ba-49fc-9933-c9a16a4b7137",
            "exames": "05ec62dd-ba7e-4da6-8aa5-2d94ffe4dea7",
            "oncologia": "cdb633e5-f4ce-43d1-8386-25e6025004d0",
            "pronto_socorro": "fc56c622-f268-4427-8ab3-128b76f5fc05",
            "maternidade": "4e05ff7d-8dd8-48ce-b71f-f027d8211f98"
        }
    else:
        return {
            "ambulatorio": None,
            "exames": None,
            "internacao": None,
            "maternidade": None,
            "pronto_socorro": None,
            "oncologia": None
        }

def get_hospital():
    hospitais = {
        "HMS": HMS,
        "HMC": HMC,
        "HPC": HPC,
        "HMV": HMV,
        "HSF": HSF,
        "HSL": HSL,
        "HMSM": HMSM,
        "OTO_ING": ING_OTO,
        "HAT": HAT,
        "HAC": HAC,
        "HPM_HST": HPM_HST,
        "HSMC": HSMC
    }
    return hospitais
    
def get_hospital_teste():
    hospitais_teste = {
        "HMS": teste.HMS,
        "HMC": teste.HMC,
        }
    return hospitais_teste

def get_template(hospital):
    if hospital in ['HMS','HMC','HPC','HMV','HSF','HSL','HMSM']:
        return {
            "template_invite_hash":"sCrfzj",   
            "template_expired_hash":"2StHdo",
            "template_thanks_hash":"NO5dtr"
        }

