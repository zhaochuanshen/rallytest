#here I include two more methods, getdays1() and gethours1()
#they are doing the same thing as getdays() and gethours()
#however, they are easier to understand
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

def getdays1(datetime1, datetime2):
	days = (datetime2.date() - datetime1.date() ).days 
	days = days + 1
	noofweeks = days / 7 
	startday = datetime1.isoweekday()
	endday = datetime2.isoweekday()
	if (days > noofweeks * 7):
		if (endday < startday):
			endday += 7
		if (startday <= 6):
			if (endday >= 7):
				days = days - 2
			else:
				if (endday >= 6):
					days = days -1
		else:
			if (startday <= 7 and endday >=7 ):
				days = days -1
	days = days -noofweeks*2
	return days

def gethours1(datetime1, datetime2):
	#this method calculate how many businesshours between time 1 and time 2
	d =timedelta (days = 1)
	date1 = datetime1 + d
	date2 = datetime2 - d
	if (date1.date() <= date2.date()):
		businesshours = (getdays1(date1, date2) ) * 8
	else:
		businesshours = 0
	#first it calculate how any businessdays from the day after time1 to the day before time2
	# getdays1() is the same as before, but now it can not return a negative or 0 value 
	result = timedelta(hours = businesshours)
	if (datetime1.isoweekday() <=5 and datetime1.date() == datetime2.date()):
		datee = datetime (datetime1.year,datetime1.month,datetime1.day, 17, 0, 0, 0, pytz.utc)
		dates = datetime (datetime1.year,datetime1.month,datetime1.day, 9, 0, 0, 0, pytz.utc)
		if (datetime2 <= dates):
			return result
		if (datetime1 < dates):
			datetime1 = dates
		if (datetime2 > datee):
			datetime2 = datee
		result += datetime2 - datetime1
		return result

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
dudu = {}
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
	d = gethours1 (startdate, enddate)
	if x['ScheduleState'] in result:
		result[x['ScheduleState']] += c
		dudu[x['ScheduleState']] += d
	else:
		result[x['ScheduleState']] =  c
		dudu[x['ScheduleState']] =  d


	
print 'results!!!!!'
z = timedelta(hours = 0)
print 'results are also stored in solution3.csv'
f = open("solution3.csv", "w")
w = csv.writer(f)
for key, value in result.items():
	if value != z:
		print key,'->' ,value
		w.writerow([key, value])

print 'results calculated by the new methods, getdays1() and gethours1()'
for key in result.keys():
	print key, '->',dudu[key] 

print 'you can compare results above with the results before. They are the same!' 
# the following code check the difference between them. no error comes about!
for key in result.keys():
	if key not in dudu:
		print 'error!!!!!!!!'
	if result[key] != dudu[key]:
		print 'error!!!'

for key in dudu.keys():
	if key not in result:
		print 'error!!!!!!!!'
	if result[key] != dudu[key]:
		print 'error!'	
		
f.close()

print 'just like the solution in problem 2:'
print 'Please note there 1 day means 24 hours'
print 'for example: Released -> 175 days, 0:00:00 '
print 'indicate that 175*24 = 4200 businesshours in total with "Released" in Feburary!'
