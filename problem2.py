from datetime import timedelta
from datetime import datetime
import csv
import pytz
import json
import dateutil.parser
from pprint import pprint
def getdays(datetime1, datetime2):
	weekends = [6,7]
	days = (datetime2.date() - datetime1.date() ).days 
	noofweeks = days / 7 
	extradays = days % 7
	startday = datetime1.isoweekday();
	days = days - (noofweeks * 2 )
	for weekend in weekends:
		if(startday==weekend):
			days = days - 1;
		else:
			if(weekend >= startday):
				if(startday+extradays >= weekend):
					days = days - 1 ;
				else:
					if(7-startday+extradays>=weekend):
						days = days - 1 ;
	return days + 1

def gethours(datetime1, datetime2):
	#this method calculate how many businesshours between time 1 and time 2
	d =timedelta (days = 1)
	date1 = datetime1 + d
	date2 = datetime2 - d
	businesshours = (getdays(date1, date2) ) * 8
	#first it calculate how any businessdays from the day after time1 to the day before time2
	# it might give a negative (or 0) value, but this is still correct in the way I wrote
	result = timedelta(hours = businesshours)
	if (datetime1.isoweekday() != 6 and datetime1.isoweekday() != 7):
	#if datetime1 is not weekend, we need to calculate its contribution
		date1e = datetime (datetime1.year,datetime1.month,datetime1.day, 17, 0, 0, 0, pytz.utc)
		date1s = datetime (datetime1.year,datetime1.month,datetime1.day, 9, 0, 0, 0, pytz.utc)
		if (datetime1 < date1s):
			datetime1 = date1s
		if (date1e > datetime1): # then add the contribution of business hour from time1
			# if date1e < datetime1, means the start time is after 5:00pm of that day
			#no contribution!
			result += date1e - datetime1
	if (datetime2.isoweekday() != 6 and datetime2.isoweekday() != 7):
	#if datetime2 is not weekend, we need to calculate its contribution
		date2s = datetime (datetime2.year,datetime2.month,datetime2.day, 9, 0, 0, 0, pytz.utc)
		date2e = datetime (datetime2.year,datetime2.month,datetime2.day, 17, 0, 0, 0, pytz.utc)
		if (datetime2 > date2e):
			datetime2 = date2e
		if (date2s < datetime2):
			#if date2s > datetime2, means the start time is after 5:00pm of that day
			#no contribution!
			result += datetime2 - date2s # then the contribution of business hour from time2
	return result

json_data=open('rally.json')

data = json.load(json_data)
json_data.close()
i = 0
result = {}
Feb1st = datetime(2012, 02, 01, 00, 00, 00,0,  pytz.utc)
Mar1st = datetime(2012, 03, 01, 00, 00, 00,0,  pytz.utc)
for x in data:
#	print x
	enddate = dateutil.parser.parse( x['_ValidTo'] )
	startdate = dateutil.parser.parse( x['_ValidFrom'] )
	if enddate < startdate:
		print 'error! finish time is before start time'
		continue
	if enddate < Feb1st or startdate > Mar1st: 
		#finish time is before Feb 1st, or start time after March 1st, no contribution to Feb
		continue
	if startdate < Feb1st: 
		# if startdate or enddate is out of Feb, set it as beginning or end of feb,respectively
		startdate = Feb1st
	if enddate > Mar1st:
		enddate = Mar1st
	c = gethours(startdate, enddate)
	if x['ObjectID'] in result:
		result[x['ObjectID']] += c
	else:
		result[x['ObjectID']] =  c

z = timedelta(hours = 0)
print 'results are also stored in solution2.csv'
f = open("solution2.csv", "w")
w = csv.writer(f)
for key, value in result.items():
	if value != z:
		print key, '->',value
		w.writerow([key, value])
		
f.close()

print 'Please note that here 1 day means 24 hours'
print 'for example: 5264035969 -> 2 days, 6:42:34.494000'
print 'indicating job 5264035969 has 24*2 + 6:42:34.494000 = 54 hours 42 minutes 34.494 seconds of businesshours in Feburary!'

print 'another example: 5125515773 -> 7 days, 0:00:00'
print 'indicating 5125515773 has 24*7 = 168 businesss hours in Feburary!'

