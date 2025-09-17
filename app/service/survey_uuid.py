from app.db.querys_mv.HUB_ES import HMC, HMS, HPC, HMV, HSF, HSL, HMSM
from app.db.querys_mv.ING_OTO import OTOA, OTOSD, OTOM, OTOS,ING
from app.db.querys_mv import HAT
from app.db.querys_tasy import HAC,HSMC,ENCORE, HST, HPM
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
    elif hospital == 'HAT':
        return{
            "internacao": "8aa8e296-6871-4afb-9063-85a4be25df4d",
            "ambulatorio": "bce35180-ab7b-46c6-9055-aac2aa457f0c",
            "exames": "0039a905-ece4-41ba-aae3-eb80e6010e26",
            "oncologia": "ab17cb9b-fa18-4d6b-8142-89975bb2e3c9",
            "pronto_socorro": "9bc7d067-5f37-4435-ae5b-590c89e3fb15",
            "maternidade": "22bb1c13-e98c-4d16-b8ef-c12cde347df6"
        }
    elif hospital == 'OTOA':
        return {
            "internacao": "8d609058-7d82-481e-bf3f-c03df1d9a679",
            "ambulatorio": "8f1493d9-68b7-4f54-a247-057d67bd2216",
            "exames": "a1893a04-2492-4163-8ffb-68eab4058312",
            "oncologia": "38636e0e-bea4-4fec-8388-5d86760d859f",
            "pronto_socorro": "a75f7b2c-0660-4cec-9832-217fa914bfbb",
            "maternidade": "17d4a4a4-4271-483a-946d-3e672ad6a47a"
        }

    elif hospital == 'OTOSD':
        return {
            "internacao": "4d37e739-e846-4dcc-96d9-60d665b02472",
            "ambulatorio": "7dea4b1b-d802-43d6-8a28-c8872e245724",
            "exames": "17f9ddff-d497-447d-a777-1a288f98186d",
            "oncologia": "8a1bd6fc-bb76-4493-a7fb-e233b289331f",
            "pronto_socorro": "615b4b3d-d8a2-4902-ad48-0b6deee123a9",
            "maternidade": "454cda53-9322-4cfd-b72c-0986685b76b5"
        }

    elif hospital == 'OTOM':
        return {
            "internacao": "f406dc48-9203-43b1-8c0f-3f351af26f24",
            "ambulatorio": "1343ca4e-6a22-44c4-9073-60fc9f8c3db7",
            "exames": "d7ea2f08-8f46-48de-a451-bb7432511db2",
            "oncologia": "495867ea-5101-4d51-87dc-5ddba4b95b08",
            "pronto_socorro": "fba67744-18fb-44ee-96a9-09a179263ed4",
            "maternidade": "981bbbb0-8520-4551-9865-35b0a45a81a0"
        }

    elif hospital == 'OTOS':
        return {
            "internacao": "34c0cdce-ab35-4244-9514-75f7991c7512",
            "ambulatorio": "8f07db8c-09f5-444f-a974-731d8cce8bf7",
            "exames": "60c683d3-d6b8-4fce-b71b-98515b0abcf7",
            "pronto_socorro": "26da24e0-0a69-4da7-9ffb-63c2f34de843",
            "oncologia": None,
            "maternidade":None
        }
    
    elif hospital == 'ING':
        return {
            "internacao": "234239f5-cdaa-4db8-8bd2-f45e290fa896",
            "ambulatorio": "a8135a20-c59d-4f95-b923-38c69a0f9d99",
            "exames": "26f128f8-769c-416f-b6c0-1747d04129e6",
            "oncologia": "72cca428-0dda-4a9b-b231-d5a65f877c26",
            "pronto_socorro": "383fb6ab-bf3a-4b47-9874-9a07bdfe7cf9",
            "maternidade": "2b84ca2e-c4e3-445d-b485-b9492d31855c"
        }

    elif hospital == 'ENCORE':
        return {
            "internacao": "85a7972b-6c1f-49a1-908d-ffa22968f910",
            "ambulatorio": "b466f014-aa1c-42b2-9e43-5286a9167b9d",
            "exames": "01233aed-5330-40ff-93ab-4d455fef1623",
            "oncologia": "b0728a22-22f9-4b4c-86ae-2a19903628f4",
            "pronto_socorro": "07f9aa97-44b9-42d2-ba0f-a2fef26741f1",
            "maternidade": "27c8847f-7b6e-4f7f-bd02-b04ec2f6b983"
        }

    elif hospital == 'HSMC':
        return {
            "internacao": "18b941ae-1999-4c69-a7a4-91e46dad2e0c",
            "ambulatorio": "4ef6b4af-055b-4457-a172-9d2d8964c7d1",
            "exames": "a66db0fb-1f6b-4a2b-8d61-2f2cb20ca208",
            "oncologia": "e7f6a827-94e6-4d3f-a296-fe06dc1aa0be",
            "pronto_socorro": "bcbacc3f-0476-4c04-b77a-e1cd58e07560",
            "maternidade": "fbca8a3c-7707-473d-8784-672ef3318ce2"
        }

    elif hospital == 'HAC':
        return {
            "internacao": "64ee1339-9348-4ab3-b1b5-945dbaf0c03f",
            "ambulatorio": "76174ced-d30a-424d-bb16-37fd7541a1dd",
            "exames": "d64a68cf-930f-4ea3-bc62-b3862bb66836",
            "oncologia": "a1e006a5-c1fb-42ba-8e9d-abdf00f9b803",
            "pronto_socorro": "3ce2424f-8d1a-44ef-ba46-cf93877002db",
            "maternidade": "6d3f1bcc-f0e5-42bf-a51a-0cee515bbd01"
        }

    elif hospital == 'HPM':
        return {
            "internacao": "2442176b-a6b1-422b-b022-996863e1ddce",
            "ambulatorio": "14133bcc-3b23-4687-a6ce-3b95552991a0",
            "exames": "d2a63406-f7b6-47e1-842c-21ba168aa4b2",
            "oncologia": "83881774-9e15-4064-8eca-109e4631a1b4",
            "pronto_socorro": "64ff4519-2bf1-4173-9e11-9b915c6a80fb",
            "maternidade": "bd83c443-fcfd-43e1-b84b-7f7270393e7f"
        }

    elif hospital == 'HST':
        return {
            "internacao": "df5078f3-833c-405d-af94-966a6a2aea2b",
            "ambulatorio": "b6540194-2ff0-4653-9582-68162eb775f3",
            "exames": "9f984468-6681-409f-b72f-45a5ff626a9b",
            "oncologia": "c55e36cf-39fa-4bed-9ef7-53f483be3244",
            "pronto_socorro": "d9659af0-79a2-48b4-9098-9a6deefb9524",
            "maternidade": "f4b33df5-b9fb-4a36-ae07-2270adf471ca"
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
        "HAT": HAT,
        "HAC": HAC,
        "HST": HST,
        "HPM": HPM,
        "HSMC": HSMC,
        "OTOA": OTOA,
        "OTOSD": OTOSD, 
        "OTOM": OTOM,
        "OTOS": OTOS,
        "ING": ING,
        "ENCORE":ENCORE 

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
            "template_thanks_hash":"NO5dtr",
            "wpp_name":"templatemeridional",
            "id_provider":"HXe9f93f4a14efe94040ed057d46c12e42"
        }
    elif hospital in ["OTOA", "OTOSD", "OTOM", "OTOS"]:
        return {
            "template_invite_hash":"5YpcLj",   
            "template_expired_hash":"Lm1Alr",
            "template_thanks_hash":"GKza0K",
            "wpp_name":None,
            "id_provider":None
        }
    elif hospital in ['ING']:
        return {
            "template_invite_hash":"SQq3Dz",   
            "template_expired_hash":"nCV90X",
            "template_thanks_hash":"d7cv2m",
            "wpp_name":None,
            "id_provider":None
        }

