from datetime import *
import pandas as pd

f = open("data.csv", "r")
df = pd.read_csv(f)

time_now = datetime.now()

timings = []

def time_up():
	for index, row in df.iterrows():
		sample = str(row['publishedAt'])
		sample = sample[0:len(sample)-5]
		sample = datetime.strptime(str(sample),'%Y-%m-%dT%H:%M:%S')
		uptime = (time_now - sample).total_seconds() / 3600
		round(uptime, 2)
		timings.append(uptime)
	df['uptime'] = hits
	f = open("test.csv", "a")
	df.to_csv(path_or_buf=f, encoding='utf-8')
	f.close()

time_up()