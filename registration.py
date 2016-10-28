import requests
import requests.packages.urllib3
import json
requests.packages.urllib3.disable_warnings()

token = "c249b1c7b414ccaa5bf97c9d905e3d22"
github = "https://github.com/edwann13/code2040.git"

payload = {"token": token, "github": github}

url = 'http://challenge.code2040.org/api/register'

r = requests.post(url, params=payload)
