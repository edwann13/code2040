import ast
import requests
import json
import requests.packages.urllib3
import numpy as np
requests.packages.urllib3.disable_warnings()

def arrayPrefix(prefix, array):
	"""
	Compares every string in ARRAY with PREFIX, returns a new
	list with strings that DON'T contain the PREFIX.

	Args:
		prefix (str): Prefix that we will be using for comparison
			in the ARRAY

		array (list): Contains all the words that we want to compare
			against PREFIX

	Returns:
		preList (list): A new list that contains strings from ARRAY 
			that did not contain the prefix PREFIX.
	"""
	preList = list()
	times = 0
	for entry in array:
		cut = len(prefix)
		if (not prefix == entry[0: cut]):
			preList.append(entry)
			times = times + 1 
	return preList

#Request dictionary
token = "c249b1c7b414ccaa5bf97c9d905e3d22"
payload = {"token": token}
url = "http://challenge.code2040.org/api/prefix"
r = requests.post(url, payload)

#Convert Requests (json) into a python dictionary, and extract data
obj = json.loads(r.text)
prefix = obj["prefix"]
array = obj["array"]

#Generate new array, with 
pArray = arrayPrefix(prefix, array)

#POST data
payload = {'token': token, 'array': pArray}
url = "http://challenge.code2040.org/api/prefix/validate"
r = requests.post(url, json = payload)

#Confirm Step
print (r.text)

