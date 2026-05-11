import requests


BASE_URL = "https://ehrbase.maia.dsp.se"
USERNAME = "ehrbase-user"
PASSWORD = "SuperSecretPassword"


# 1. Read the file as a string, using 'utf-8-sig' to strip the invisible BOM
with open("ASHA-Echocardiography.v1.opt", "r", encoding="utf-8-sig") as f:
    xml_content = f.read()

# 2. Encode it back to clean UTF-8 bytes for the request
clean_data = xml_content.encode('utf-8')
response = requests.post(f"{BASE_URL}/ehrbase/rest/openehr/v1/definition/template/adl1.4", headers={"Content-Type": "application/xml"}, auth=(USERNAME, PASSWORD), data=clean_data, verify="C:/Users/simon/OneDrive - Linköpings universitet/kube/maia-dsp/ca.crt")
print(response.status_code)
print(response.text)

response = requests.get(f"{BASE_URL}/ehrbase/rest/openehr/v1/definition/template/adl1.4", headers={"Accept": "application/json"}, auth=(USERNAME, PASSWORD), verify="C:/Users/simon/OneDrive - Linköpings universitet/kube/maia-dsp/ca.crt")
print(response.json())




# Create an EHR
#response = requests.post(f"{BASE_URL}/ehrbase/rest/openehr/v1/ehr", headers={"Accept": "application/json", "Prefer": "return=representation"}, auth=(USERNAME, PASSWORD))
#print(response.json())

#ehr_id = response.json()["ehr_id"]["value"]
#print(f"EHR ID: {ehr_id}")



# Add the exact templateId to the query parameters
#url = f"{BASE_URL}/ehrbase/rest/openehr/v1/ehr/{ehr_id}/composition?format=FLAT&templateId=ImagingRequest"

#response = requests.post(
#    url, 
#    headers={
#        "Content-Type": "application/json", 
#        "Accept": "application/json"
 #   }, 
 #   auth=(USERNAME, PASSWORD), 
 #   data=open("ImagingRequest.json", "rb").read()
#)

#print(f"Status Code: {response.status_code}")
#print(response.text)