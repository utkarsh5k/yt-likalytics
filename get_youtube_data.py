import pandas as pd
import matplotlib as mpl

from apiclient.discovery import build
from apiclient.errors import HttpError
from oauth2client.tools import argparser

API_KEY = "AIzaSyBYq7UXn9VnF9JOLKEDHgU0N0u0U_zw3ps" 
API_NAME = "youtube"
API_VERSION = "v3"


argparser.add_argument("--q", help="Search term", default="Manchester United")
argparser.add_argument("--max-results", help="Max results", default=25)
arguments = argparser.parse_args()
options = arguments

youtube = build(API_NAME, API_VERSION, developerKey=API_KEY)

search_response = youtube.search().list(
	q=options.q,
	type="video",
	part="id,snippet",
	maxResults=options.max_results
).execute()

videos = {}

for search_result in search_response.get("items", []):
    if search_result["id"]["kind"] == "youtube#video":
    	videos[search_result["id"]["videoId"]] = search_result["snippet"]["title"]

s = ','.join(videos.keys())

videos_list_response = youtube.videos().list(
	id=s,
	part='id,statistics,snippet,status,contentDetails'
).execute()

res = []
for i in videos_list_response['items']:
	temp_res = dict(v_id = i['id'], v_title = videos[i['id']])
	temp_res.update(i['statistics'])
	temp_res.update(i['status'])
	temp_res.update(i['contentDetails'])
	temp_res.update(i['snippet'])
	res.append(temp_res)

dataframe = pd.DataFrame.from_dict(res)
dataframe.drop(['license', 'licensedContent', 'embeddable'], axis=1, inplace=True)
# print dataframe
names = dataframe.columns.values 
print names
