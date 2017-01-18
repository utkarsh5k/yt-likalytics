import pandas as pd

f = open("data.csv", "r")
df = pd.read_csv(f)

blacklist = ["I", "am", "the", "on", "in", "why", "what", "as", "if", "else", "because",
             "what", "why", "that", "there", "into", "about", "for", "with", "does", "him",
             "her", "they"]

def add_col():
	hits = []
	for index, row in df.iterrows():
		match_title = str(row['title'])
		match_title = match_title.split(' ')
		title_hits = 0
		for mt in match_title:
			if mt not in blacklist:
				with open("india24.txt") as f:
					title_hits = title_hits + f.read().lower().count(mt.lower())
				with open("uk24.txt") as f:
					title_hits = title_hits + f.read().lower().count(mt.lower())
				with open("usa24.txt") as f:
					title_hits = title_hits + f.read().lower().count(mt.lower())
		hits.append(title_hits)
	df['title_hits'] = hits
	f = open("test.csv", "a")
	df.to_csv(path_or_buf=f, encoding='utf-8')
	f.close()

def get_hits(d):
	hits = []
	for index, row in d.iterrows():
		match_title = str(row['title'])
		match_title = match_title.split(' ')
		title_hits = 0
		for mt in match_title:
			if mt not in blacklist:
				with open("india24.txt") as f:
					title_hits = title_hits + f.read().lower().count(mt.lower())
				with open("uk24.txt") as f:
					title_hits = title_hits + f.read().lower().count(mt.lower())
				with open("usa24.txt") as f:
					title_hits = title_hits + f.read().lower().count(mt.lower())
		hits.append(title_hits)
	return hits

add_col()
