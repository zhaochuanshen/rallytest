from datetime import timedelta
from datetime import datetime
import pytz
import json
import csv
import dateutil.parser
from pprint import pprint

json_data=open('rally.json')

data = json.load(json_data)
json_data.close()
i = 0
result = {}
Feb1st = datetime(2012, 02, 01, 00, 00, 00,0,  pytz.utc)
Mar1st = datetime(2012, 03, 01, 00, 00, 00,0,  pytz.utc)
for x in data:
	yourdate = dateutil.parser.parse( x['_ValidTo'] )
	mydate = dateutil.parser.parse( x['_ValidFrom'] )
	if mydate > yourdate: # the data is wrong, start time is after finish time
		print 'error! start time is after finish time!'
		continue
	if yourdate < Feb1st or mydate > Mar1st:
		# finish time is before Feb 1st, or start time after March 1st, no contribution to Feb
		continue
	if mydate < Feb1st: # only consider Feb, so take start time as Feb 1st
		mydate = Feb1st
	if yourdate > Mar1st: # only consider Feb, so take finish time as Mar 1st
		yourdate = Mar1st
	c = yourdate - mydate
	if x['ObjectID'] in result:
		result[x['ObjectID']] += c
	else:
		result[x['ObjectID']] =  c 
	
print 'results!!!!!'
print 'results are also stored in solution1.csv'
f = open("solution1.csv", "w")
w = csv.writer(f)
for key, value in result.items():
	print key, value
	w.writerow([key, value])

f.close()
print len(result)
