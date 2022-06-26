import datetime
from typing import Dict

import dateutil.parser
import tzlocal

import calendario
from api import AULE_ENDPOINT, client


def aule() -> list:
    return client.post(
        AULE_ENDPOINT,
        json={
            "linkCalendarioId": "5e9996a228a649001237296d",
            "clienteId": "5ad08435b6ca5357dbac609e",
            "auleIds": [],
            "edificiIds": [],
        },
    ).json()


def aule_libere(
    time: datetime.datetime = datetime.datetime.now(tzlocal.get_localzone()),
) -> Dict:

    aule_lst = aule()
    aule_lst.sort(key=lambda aula: aula["descrizione"])

    impegni = calendario.impegni_calendario(date=time.date())

    free_aule_map = {aula["id"]: aula for aula in aule_lst}
    impegni_map = {aula["id"]: None for aula in aule_lst}

    for impegno in impegni:

        start_time = dateutil.parser.isoparse(impegno["dataInizio"])
        end_time = dateutil.parser.isoparse(impegno["dataFine"])

        # If the impegno is in the future or in the past, skip it
        if time > end_time:
            continue
        elif time < start_time:
            for risorsa in impegno["risorse"]:

                if "aula" in risorsa:
                    matching_aula = free_aule_map.get(risorsa["aula"]["id"], None)

                    if matching_aula:
                        impegni_map[matching_aula["descrizione"]] = impegno

        for risorsa in impegno["risorse"]:
            if "aula" in risorsa:

                matching_aula = free_aule_map.get(risorsa["aula"]["id"], None)

                if matching_aula:
                    try:
                        free_aule_map.pop(matching_aula["descrizione"])
                        impegni_map.pop(matching_aula["descrizione"])
                    except KeyError:
                        pass

    return free_aule_map, impegni_map
