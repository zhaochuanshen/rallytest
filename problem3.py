from datetime import timedelta
from datetime import datetime
import csv
import pytz
import json
import dateutil.parser
from pprint import pprint
def getdays(datetime1, datetime2):
	# the comments of this method and the method gethours(time1, time2) can be found in
	# problem2.py
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
	d =timedelta (days = 1)
	date1 = datetime1 + d
	date2 = datetime2 - d
	businesshours = (getdays(date1, date2) ) * 8
	result = timedelta(hours = businesshours)
	if (datetime1.isoweekday() != 6 and datetime1.isoweekday() != 7):
		date1e = datetime (datetime1.year,datetime1.month,datetime1.day, 17, 0, 0, 0, pytz.utc)
		date1s = datetime (datetime1.year,datetime1.month,datetime1.day, 9, 0, 0, 0, pytz.utc)
		if (datetime1 < date1s):
			datetime1 = date1s
		if (date1e > datetime1):
			result += date1e - datetime1
	if (datetime2.isoweekday() != 6 and datetime2.isoweekday() != 7):
		date2s = datetime (datetime2.year,datetime2.month,datetime2.day, 9, 0, 0, 0, pytz.utc)
		date2e = datetime (datetime2.year,datetime2.month,datetime2.day, 17, 0, 0, 0, pytz.utc)
		if (datetime2 > date2e):
			datetime2 = date2e
		if (date2s < datetime2):
			result += datetime2 - date2s
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
	if enddate < Feb1st:
		continue
	if startdate < Feb1st:
		startdate = Feb1st
	if enddate > Mar1st:
		enddate = Mar1st
	c = gethours(startdate, enddate)
	if x['ScheduleState'] in result:
		result[x['ScheduleState']] += c
	else:
		result[x['ScheduleState']] =  c
	
print 'results!!!!!'
z = timedelta(hours = 0)
print 'results are also stored in solution3.csv'
f = open("solution3.csv", "w")
w = csv.writer(f)
for key, value in result.items():
	if value != z:
		print key,'->' ,value
		w.writerow([key, value])
	
		
f.close()

print 'just like the solution in problem 2:'
print 'Please note there 1 day means 24 hours'
print 'for example: Released -> 175 days, 0:00:00 '
print 'indicate that 175*24 = 4200 businesshours in total with "Released" in Feburary!'
