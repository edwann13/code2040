from __future__ import division
from calendar import monthrange
from dateutil.parser import parse
import ast
import requests
import json
import requests.packages.urllib3
import numpy as np
requests.packages.urllib3.disable_warnings()

def conversion(sec, time):
	"""
	Convert SEC into: minutes, hours, days, months, and years.
		Returns a tuple, (seconds, minutes, hours, days, months, years)

	Args:
		sec (int): Number of seconds that is going to be converted.

		time (datetime): A Converted ISO 8601 into a Python datetime obj,
			required in order to account for leap years, and varying days
			in a month.

	Returns:
		timeTuple (tuple): a tuple that contains all the converted ratios
			(seconds, minutes, hours, days, months, years) for the given SEC.
	"""
	minute = sec / 60
	hour = minute / 60
	day = hour / 24

	# monthrange, for varying days in a month (leap year)
	month = day / (monthrange(time.year, time.month)[1])
	
	year = month / 12
	timeTuple = (sec, minute, hour, day, month, year)

	return timeTuple

def trickleD(SS, MM, HH, dd, mm, y, time):
	"""
	Increments TIME's attributes by SS, MM, HH, dd, mm, y. Assumption is that
		the values will come from function conversion, the largest temporal term 
		will be modified, and its "remainder" will be converted to a smaller 
		succesively smaller term until the conversion reaches the smallest temporal term. 

	Args:
		SS (int): seconds, SS is the convention for ISO 8601

		MM (int): minutes, MM is the convention for ISO 8601

		HH (int): hours, HH is the convention for ISO 8601

		dd (int): days, dd is the convention for ISO 8601

		mm (int): months, mm is the convention for ISO 8601

		y (int): years, y is the convention for ISO 8601

		time (datetime): A Converted ISO 8601 into a Python datetime obj,
			required in order to account for leap years, and varying days
			in a month.
	Returns:
		(tuple): returns a tuple with the modied values that are going
			update the attributes: seconds, minutes, hours, days, months,
			and years.
	"""
	if (y >= 1):
		year = int(y)
		remainder = y - int(y)
		mm = remainder * 12
	else:
		y = 0

	if (mm >= 1): # mod 12
		remainder = mm - int(mm)
		dd = remainder * monthrange(time.year, time.month)[1]
		mm = int(month)
	else:
		mm = 0

	if (dd >= 1): #mod dep
		HH = (dd - int(dd)) * 24
		dd = int(dd)
	else:
		dd = 0

	if (HH >= 1): #mod 24
		remainder = HH - int(HH)
		MM = remainder * 60
		HH = int(HH)
	else:
		HH = 0

	if (MM >= 1): #mod 60
		remainder = MM - int(MM)
		SS = remainder * 60
		MM = int(MM)
		SS = int(SS)
	else:
		MM = 0
		SS = int(SS)

	return (SS, MM, HH, dd, mm, y)

def trickleU(SS, MM, HH, dd, mm, y, time):
	"""
	Convert values that are over the range, into a larger temporal
		term, i.e 61 min is equivalent to 1hr and 1 min. Converting
		in order to satisfy ISO 8601 standard definition.

	Args:
		SS (int): seconds, SS is the convention for ISO 8601

		MM (int): minutes, MM is the convention for ISO 8601

		HH (int): hours, HH is the convention for ISO 8601

		dd (int): days, dd is the convention for ISO 8601

		mm (int): months, mm is the convention for ISO 8601

		y (int): years, y is the convention for ISO 8601

		time (datetime): A Converted ISO 8601 into a Python datetime obj,
			required in order to account for leap years, and varying days
			in a month.
	Returns:
		(tuple): returns a tuple with the modied values that are going
			update the attributes: seconds, minutes, hours, days, months,
			and years.
	"""
	if(SS >= 60):
		minute = SS // 60
		SS = SS % 60
		MM = MM + minute

	if (MM >= 60):
		hour = MM // 60
		MM = MM % 60
		HH = HH + hour

	if (HH > 23):
		day = HH // 24
		HH = HH % 24
		dd = dd + day
	
	if (dd > monthrange(time.year, time.month)[1]):
		month = dd // monthrange(time.year, time.month)[1]
		dd = dd % monthrange(time.year, time.month)[1]
		mm = mm + month

	if (mm > 12):
		year = mm // 12
		mm = mm % 12
		y = y + year



def modDate(datetime, SS, MM, HH, dd, mm, y):
	"""
	Create modified DATETIME attributes, in order to create
		a new DATETIME obj. Adds old attributes with new attributes. 

	Args:
		SS (int): seconds, SS is the convention for ISO 8601

		MM (int): minutes, MM is the convention for ISO 8601

		HH (int): hours, HH is the convention for ISO 8601

		dd (int): days, dd is the convention for ISO 8601

		mm (int): months, mm is the convention for ISO 8601

		y (int): years, y is the convention for ISO 8601

		datetime (datetime): A Converted ISO 8601 into a Python datetime obj,
			required in order to account for leap years, and varying days
			in a month.
	Returns:
		(tuple): returns a tuple with the modied values that are going
			update the attributes: seconds, minutes, hours, days, months,
			and years.
	"""
	year = datetime.year + y
	month = datetime.month + mm
	day = datetime.day + dd
	hour = datetime.hour + HH
	minute = datetime.minute + MM
	second = int(datetime.second + SS)


	SS, MM, HH, dd, mm, y = trickleU(second, minute,\
								hour, day, month, year, datetime)


	datetime.replace(second=SS, minute=MM, hour=HH)
	datetime.replace(day=dd, month=mm, year=y)

	# new case
	return (SS, MM, HH, dd, mm, y)

#Request POST from the server
token = "c249b1c7b414ccaa5bf97c9d905e3d22"
payload = {"token": token}
url = "http://challenge.code2040.org/api/dating"
r = requests.post(url, payload)

#convert json into a python dictionary
data = json.loads(r.text)

#extract data
tStamp = data['datestamp']
seconds = data['interval']

#parse ISO 8601 into a DATETIME obj
date = parse(tStamp, ignoretz=True)


#conversion and modification of a DATETIME obj
SS, MM, HH, dd, mm, y = conversion(seconds, date)
SS, MM, HH, dd, mm, y = trickleD(SS, MM, HH, dd, mm, y, date)
SS, MM, HH, dd, mm, y = modDate(date, SS, MM, HH, dd, mm, y)

#Create a new DATETIME obj with new paramaters
date2 = date.replace(second=SS, minute=MM, hour=HH, day=dd, month=mm, year=y)

#convert DATETIME into ISO 8601 format
iso = date2.isoformat() + "Z"

# POST ISO to the server
payload = {'token': token, 'datestamp': iso}
url = "http://challenge.code2040.org/api/dating/validate"
r = requests.post(url, payload)
print (r.text)



