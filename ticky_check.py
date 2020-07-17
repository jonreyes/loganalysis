#!/usr/bin/env python3
import os
import re
import operator
os.system("cat syslog.log > temp.log")
f = open("temp.log","r+")
errors = []
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
	print(username)
	if type == "ERROR":
		errors.append(message)
f.close()
errorcount = {}
for error in errors:
	errorcount[error] = 0
for error in errors:
	errorcount[error] += 1
print(sorted(errorcount.items(),key=operator.itemgetter(1),reverse=True))

