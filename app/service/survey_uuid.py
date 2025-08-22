from app.db.querys_mv.HUB_ES import HMC, HMS, HPC, HMV, HSF, HSL, HMSM
from app.db.querys_mv import ING_OTO,HAT
from app.db.querys_tasy import HAC,HPM_HST,HSMC

def get_survey_uuid(hospital):
    if hospital in 'HMS':
        return {
            "ambulatorio": "1358ad90-a68d-4bf1-8dac-db91e83b8764",
            "exames": "04765111-5c0f-42fe-b393-aff88d0fc256",
            "internacao": "c117421c-8e1f-4bef-a989-3cb1268fcab1",
            "maternidade": "05499245-9f15-4c0e-bde0-8162bbbc5497",
            "pronto_socorro": "a6536898-7b56-4bf4-a915-efd7e102ef2a",
            "oncologia": "ed6bc8b8-fc41-4da9-bf57-b3a2f0b36f66"
        }
    elif hospital == 'HMC':
        return {
            "ambulatorio": "583d2b47-1363-4cf9-b88c-4be4c0014442",
            "exames": "bc0b7fdd-251e-4c86-b5ef-69f59b9d929b",
            "internacao": "8c3a2b98-10ab-4abd-a426-89d34d3d997d",
            "maternidade": "fd5a9832-1591-43d3-9bc2-152f654bd3d6",
            "pronto_socorro": "bbce4d04-8964-4079-b7b0-794d55f6e310",
            "oncologia": "420072ca-b16c-4542-90c1-807df10de0ed"
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
    


