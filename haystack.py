import ast
import requests
import requests.packages.urllib3
requests.packages.urllib3.disable_warnings()

def findIndex(needle):
	"""Finds the index of a NEEDLE
	Iterates throught a dictionary, to find at which index
	contains the NEEDLE

	Args:
		needle (str): A String, represents our target within the
			the dictionary

	Returns:
		index (int): the index where the NEEDLE was found, if
			not found then return Zero.
	"""
	index = 0
	for key, value in dictionary.iteritems():
		if (value == needle):
			return index
		index += 1
	return index

#Request POST from server
token = "c249b1c7b414ccaa5bf97c9d905e3d22"
payload = {"token": token}
url = "http://challenge.code2040.org/api/haystack"
r = requests.post(url, payload)


#convert Response obj to a Python dictionary
dictionary = r.text
dictionary = ast.literal_eval(dictionary)

#Extract content of key-value pair, "needle", from the dic.
needle = dictionary["needle"]

#Find index of the needle
needleIndex = findIndex(needle)

#Post Result
payload = {"token": token, "needle": needleIndex}
url = "http://challenge.code2040.org/api/haystack/validate"
r = requests.post(url, payload)

print r.text
