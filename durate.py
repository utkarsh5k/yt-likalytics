import pandas as pd

f = open("data.csv", "r")
df = pd.read_csv(f)

def times(data):
	dura = []
	for index, row in df.iterrows():
		text = str(row['duration'])
		txt = work(text)
		dura.append(txt)
	return dura

def add_to_df():
	dura = []
	for index, row in df.iterrows():
		text = str(row['duration'])
		txt = work(text)
		dura.append(txt)
	df['timing'] = dura
	close()	

def work(input):
	input = input.strip('PT')
	num = 0
	output = 0
	if 'H' in input:
		ans = input.split('H')
		output = output + int(ans[0])*3600
		if 'M' in ans[1]:
			ans1 = ans[1].split('M')
			output = output + int(ans1[0])*60
			if 'S' in ans1[1]:
				ans2 = ans1[1].split('S')
				output = output + int(ans2[0])
				return output
				exit(1)

	if 'H' in input:
		ans = input.split('H')
		output = output + int(ans[0])*3600
		if 'M' in ans[1]:
			ans1 = ans[1].split('M')
			output = output + int(ans1[0])*60
			return output

	if 'H' in input:
		output = 0
		ans = input.split('H')
		output = output + int(ans[0])*3600
		if 'S' in ans[1]:
			ans1 = ans[1].split('S')
			output = output + int(ans1[0])
			return output
			exit(1)

	if 'M' in input:
			output = 0
			ans1 = input.split('M')
			output = output + int(ans1[0])*60
			if 'S' in ans1[1]:
				ans2 = ans1[1].split('S')
				output = output + int(ans2[0])
				return output
				exit(1)

	if 'S' in input:
		output = 0
		ans2 = input.split('S')
		output = output + int(ans2[0])
		return output
		exit(1)

	return output

def close():
	f = open("test.csv", "a")
	df.to_csv(path_or_buf=f, encoding='utf-8')
	f.close()

add_to_df()
