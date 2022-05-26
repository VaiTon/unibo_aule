import datetime
from typing import List

from api import client


def impegni_calendario(
    aule: List[str] = [], date: datetime.date = datetime.date.today()
):
    return client.post(
        "https://apache.prod.up.cineca.it/api/Impegni/getImpegniCalendarioPubblico",
        json={
            "mostraImpegniAnnullati": True,
            "mostraIndisponibilitaTotali": True,
            "linkCalendarioId": "5e9996a228a649001237296d",
            "clienteId": "5ad08435b6ca5357dbac609e",
            "pianificazioneTemplate": False,
            "auleIds": aule,
            "limitaRisultati": False,
            "dataInizio": date.isoformat(),
            "dataFine": (date + datetime.timedelta(days=1)).isoformat(),
        },
    ).json()
