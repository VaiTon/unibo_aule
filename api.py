import requests

HOST = "https://apache.prod.up.cineca.it"

AULE_ENDPOINT = HOST + "/api/Aule/getAulePerCalendarioPubblico"
CALENDARIO_ENDPOINT = HOST + "/api/Impegni/getImpegniCalendarioPubblico"


client = requests.session()
client.headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.149 Safari/537.36"
}
