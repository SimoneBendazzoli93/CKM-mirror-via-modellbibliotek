import requests


BASE_URL = "https://ehrbase.maia.dsp.se"
USERNAME = "ehrbase-user"
PASSWORD = "SuperSecretPassword"


TEMPLATE_ID = "ASHA-Echocardiography.v1"

url = f"{BASE_URL}/ehrbase/rest/openehr/v1/definition/template/adl1.4/{TEMPLATE_ID}/example"

# We pass format=FLAT so it doesn't give us the massive Canonical JSON
response = requests.get(
    url,
    params={"format": "FLAT"}, 
    headers={"Accept": "application/json"},
    auth=(USERNAME, PASSWORD),
    verify="C:/Users/simon/OneDrive - Linköpings universitet/kube/maia-dsp/ca.crt"
)

with open("ASHA-Echocardiography.v1-Example.json", "w") as f:
    f.write(response.text)