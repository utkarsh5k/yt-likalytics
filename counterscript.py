# encoding=utf8
import sys
import json
import csv
import pandas as pd

reload(sys)
sys.setdefaultencoding('utf8')

cntr = []
with open('hottrends.json') as json_data:
	json_object = json.load(json_data)
	csv_file = pd.read_csv('data.csv', header = 0)
	csvcols = csv_file.loc[: , "tags"]		
  	with open('data.csv','rb') as csv_file:
		csvfile = pd.read_csv(csv_file)
		for csvrow in csvfile.loc[:, "tags"]:
			csvrow = str(csvrow)
			csvrow =csvrow[1:len(str(csvrow))-1]
			if csvrow is " ":
				continue
			for csvitem in csvrow.split(", "):
				counter = 0
				if csvitem is " ":
					break
				else:
					for jsonrow in json_object:
						for jsonitem in json_object[jsonrow]:
							if csvitem in jsonitem:
								counter = counter +1
			if counter == 505:
				counter = 0
			cntr.append(counter)
csvfile['tagsCounter'] = cntr
csvfile.to_csv('new.csv')

blacklist = ["i", "am", "the", "because", "this", "that", "those", "a", "an", "though", "in", "so", "and", "ok", 
			"these", "if", "you", "us", "again", "after", "no", "not", "be", "have", "may", "see", "call", "good",
			"new", "first", "last", "few", "bad", "able", "in", "as", "just", "now", "to", "for", "with", "on",
			"at", "by", "bye", "over", "out", "nor", "like", "once", "one", "two", "last", "next", "million",
			"four", "five", "eight", "nine", "ten", "seven", "hi", "hello", "why", "no", "yeah", "oh", "wow",
			"ah", "it", "for", "will", "my", "get", "go", "like", "him", "year", "its", "also", "day", "1", "2", 
			"3", "4", "5", "6", "7", "8", "9"]
cntr = []
with open('hottrends.json') as json_data:
	json_object = json.load(json_data)
	csv_file = pd.read_csv('new.csv', header = 0)
	csvcols = csv_file.loc[: , "tags"]		
  	with open('new.csv','rb') as csv_file:
		csvfile = pd.read_csv(csv_file)
		for csvrow in csvfile.loc[:, "channelTitle"]:
			csvrow = str(csvrow)
			if csvrow is " ":
				continue
			for csvitem in csvrow.split(" "):
				counter = 0
				if csvitem is "":
					break
				else:
					for jsonrow in json_object:
						for jsonitem in json_object[jsonrow]:
							if csvitem in jsonitem:
								if csvitem not in blacklist:
									counter = counter+1
			if counter == 505:
				counter = 0
			cntr.append(counter)
csvfile['channelTitleCounter'] = cntr
csvfile.to_csv('new.csv')			