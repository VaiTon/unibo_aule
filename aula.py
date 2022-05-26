import datetime
from copy import copy

import dateutil.parser
import tzlocal

import calendario
from api import client


def aule() -> list:
    return client.post(
        "https://apache.prod.up.cineca.it/api/Aule/getAulePerCalendarioPubblico",
        json={
            "linkCalendarioId": "5e9996a228a649001237296d",
            "clienteId": "5ad08435b6ca5357dbac609e",
            "auleIds": [],
            "edificiIds": [],
        },
    ).json()


def aule_libere(
    time: datetime.datetime = datetime.datetime.now(tzlocal.get_localzone()),
):

    a = aule()
    impegni = calendario.impegni_calendario(date=time.date())

    aule_libere = copy(a)

    for impegno in impegni:

        start_time = dateutil.parser.isoparse(impegno["dataInizio"])
        end_time = dateutil.parser.isoparse(impegno["dataFine"])

        # If the impegno is in the future or in the past, skip it
        if time < start_time or time > end_time:
            continue

        for risorsa in impegno["risorse"]:
            if "aula" in risorsa:

                aula = [
                    aula for aula in aule_libere if aula["id"] == risorsa["aula"]["id"]
                ]
                if aula:
                    try:
                        aule_libere.remove(aula[0])
                    except ValueError:
                        pass

    aule_libere.sort(key=lambda x: x["descrizione"])
    return aule_libere
