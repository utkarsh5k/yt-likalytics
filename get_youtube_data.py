import pandas as pd

from apiclient.discovery import build
from apiclient.errors import HttpError
from oauth2client.tools import argparser

import channel_details as cd

API_KEY = "AIzaSyBYq7UXn9VnF9JOLKEDHgU0N0u0U_zw3ps" 
API_NAME = "youtube"
API_VERSION = "v3"

search_queries = ["Manchester United", "Proximity", "Ed Sheeran", "Selena Gomez", "Chelsea FC",
                "Mortal Kombat", "Call of Duty", "WWE", "Conor McGregor", "AIB", "TVF", "EIC", "SNG", 
                "Graham Norton", "Jimmy Fallon", "Jimmy Kimmel", "Ellen DeGeneres", "Barack Obama"
                "Donald Trump", "Hillary Clinton", "Pokemon Go", "Battlefield", "League of Legends", 
                "Khan Academy", "TED", "GTA", "Deepika Padukone", "Pirates of the Caribbean", "Ranveer Singh",
                "Koffee with Karan", "Ranbir Kapoor", "Kareena Kapoor", "Priyanka Chopra", "Chainsmokers", 
                "Marvel", "Batman", "Superman", "Avengers", "Kenny Sebastian", "Denver Broncos",
                "New England Patriots", "Arsenal", "Manchester City", 
                "Tottenham Hotspurs", "Brexit", "Sia", "One Republic", "Wolverine", "Star Wars", "DoTA",
                "Dangal", "Salman Khan", "Shah Rukh Khan"]

def gather(search_query):
    argparser.add_argument("--q", help="Search term", default=search_query)
    argparser.add_argument("--max-results", help="Max results", default=50)
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
    	channel_details = cd.get_all_data(temp_res['channelId'])
    	res.append(temp_res)
        temp_res.update(channel_details)

    dataframe = pd.DataFrame.from_dict(res)
    # drop useless columns from dataframe
    try:
        dataframe.drop(['license', 'licensedContent', 'dimension', 'thumbnails', 'v_title', 'uploadStatus', 'defaultLanguage'], axis=1, inplace=True)
    except ValueError:
        dataframe.drop(['license', 'licensedContent', 'dimension', 'thumbnails', 'v_title', 'uploadStatus'], axis=1, inplace=True)
    """
    below columns can be manipulated into being features
    """
    dataframe.drop(['caption', 'embeddable'], axis=1, inplace=True)
    names = dataframe.columns.values
    f = open("test.csv", "a")
    dataframe.to_csv(path_or_buf=f, encoding='utf-8')
    f.close()


for query in search_queries:
    gather(query)

