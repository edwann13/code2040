import requests
import requests.packages.urllib3
requests.packages.urllib3.disable_warnings()

token = "c249b1c7b414ccaa5bf97c9d905e3d22"
payload = {"token": token}

#POST to server
url = "http://challenge.code2040.org/api/reverse"
r = requests.post(url, payload)

#reverse string
Rstring = ''.join(reversed(r.text)) 

#POST a dictionary with reversed string to server
payload = {"token": token, "string": Rstring}
url = "http://challenge.code2040.org/api/reverse/validate"
r = requests.post(url, payload)
