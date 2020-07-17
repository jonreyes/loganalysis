#!/usr/bin/env python3
import os
import re
import operator
import csv
os.system("cat syslog.log > temp.log")
f = open("temp.log","r+")
errors = []
userstats = {}
m = []
for line in f.readlines():
	match = re.search("(INFO|ERROR).*\(.*\)",line).group()
	type = re.search("(INFO|ERROR)",match).group()
	message = match.split(" ")[1:]
	numbermatch = re.search("\[.*\]",match)
	number = None
	if numbermatch:
		number = numbermatch.group()
	username = re.search("\(.*\)",match).group()
	print(type)
	if number:
		message.pop(message.index(number))
	message.pop(message.index(username))
	message = " ".join(message)
	print(message)
	print(number)
	#print(username)
	if type == "ERROR":
		errors.append(message)
	username = username[1:len(username)-1]
	print(username)
	userstats[username] = {"INFO":0,"ERROR":0}
	m.append(match)
f.close()
errorcount = {}
for error in errors:
	errorcount[error] = 0
for error in errors:
	errorcount[error] += 1
errorcount = sorted(errorcount.items(),key=operator.itemgetter(1),reverse=True)
with open("error_message.csv","w",newline="") as em_file:
	writer = csv.writer(em_file)
	writer.writerow(["Error","Count"])
	for key,value in errorcount:
		writer.writerow([key,value])
em_file.close()
for item in m:
	type = re.search("(INFO|ERROR)",item).group()
	username = re.search("\(.*\)",item).group()
	username = username[1:len(username)-1]
	userstats[username][type] += 1
userstats = sorted(userstats.items())
with open("user_statistics.csv","w",newline="") as us_file:
	writer = csv.writer(us_file)
	writer.writerow(["Username","INFO","ERROR"])
	for item in userstats:
		username = item[0]
		ic = item[1]["INFO"]
		ec = item[1]["ERROR"]
		writer.writerow([username,ic,ec])
us_file.close()
