import requests


BASE_URL = "https://ehrbase.maia.dsp.se"
USERNAME = "ehrbase-user"
PASSWORD = "SuperSecretPassword"
TEMPLATE_ID = "ASHA-Echocardiography.v1"

# Create an EHR
response = requests.post(f"{BASE_URL}/ehrbase/rest/openehr/v1/ehr", headers={"Accept": "application/json", "Prefer": "return=representation"}, auth=(USERNAME, PASSWORD), verify="C:/Users/simon/OneDrive - Linköpings universitet/kube/maia-dsp/ca.crt")
print(response.json())

ehr_id = response.json()["ehr_id"]["value"]
print(f"EHR ID: {ehr_id}")



# Add the exact templateId to the query parameters
url = f"{BASE_URL}/ehrbase/rest/openehr/v1/ehr/{ehr_id}/composition?format=FLAT&templateId={TEMPLATE_ID}"

response = requests.post(
    url, 
    headers={
        "Content-Type": "application/json", 
        "Accept": "application/json"
    }, 
    auth=(USERNAME, PASSWORD), 
    data=open("ASHA-Echocardiography.v1-Example.json", "rb").read(),
    verify="C:/Users/simon/OneDrive - Linköpings universitet/kube/maia-dsp/ca.crt"
)

print(f"Status Code: {response.status_code}")
print(response.text)