import json
from datetime import datetime, UTC
from decimal import Decimal


def _vers_utc(date: str) -> str:
    dt = datetime.fromisoformat(date)

    if dt.tzinfo is None:
        dt = dt.replace(tzinfo=UTC)
    return dt.astimezone(UTC)


def normaliser(data: list) -> list:
    for appel in data:
        appel["horodatage"] = _vers_utc(appel["horodatage"])
        appel["tokens_entrée"] = int(appel["tokens_entrée"])
        if appel.get("tokens_sortie") is None:
            appel["tokens_sortie"] = 0
        else:
            appel["tokens_sortie"] = int(appel["tokens_sortie"])
        appel["coût"] = Decimal(appel["coût"])
    return data

def serialiser(data:list) -> list:
    for appel in data:
        appel["horodatage"] =  appel["horodatage"].isoformat()
        appel["coût"] = str(appel["coût"])
    return data

def main():

    with open("appels.json", "rb") as f:
        octets = f.read()  # bytes
        json_string = octets.decode("utf-8")  # str
        print(len(octets), len(json_string))  # 1647 et 1601
        data = json.loads(json_string)

    data = normaliser(data["appels"])
    nb_appels = len(data)
    print(f"Nombres d'appels : {nb_appels}\n ")
    somme = sum(appel["coût"] for appel in data)
    print(f"Somme des coût : {somme}\n ")
    total_tokens = sum(appel["tokens_entrée"] for appel in data) + sum(
        appel["tokens_sortie"] for appel in data
    )
    print(f"total des tokens d'entrée et sortie : {total_tokens}")
    
    with open("appels_normalisé.json", "w", encoding="utf-8") as f:
        data = serialiser(data)
        json.dump(data, f, indent=2, ensure_ascii=False)
    pass


if __name__ == "__main__":
    main()
