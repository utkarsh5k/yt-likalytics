import pandas as pd
import sys

from apiclient.discovery import build
from apiclient.errors import HttpError
from oauth2client.tools import argparser

import channel_details as cd

API_KEY = "AIzaSyBYq7UXn9VnF9JOLKEDHgU0N0u0U_zw3ps"
API_NAME = "youtube"
API_VERSION = "v3"

query = "vNZyEwipG28"

def gather(search_query):
    argparser.add_argument("--v", help="Search term", default=search_query)
    argparser.add_argument("--max-results", help="Max results", default=10)
    arguments = argparser.parse_args()
    options = arguments

    youtube = build(API_NAME, API_VERSION, developerKey=API_KEY)

    search_response = youtube.search().list(
      q=options.v,
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
    try:
        dataframe.drop(['license', 'licensedContent', 'dimension', 'thumbnails', 'v_title', 'uploadStatus', 'defaultLanguage'], axis=1, inplace=True)
    except ValueError:
        dataframe.drop(['license', 'licensedContent', 'dimension', 'thumbnails', 'v_title', 'uploadStatus'], axis=1, inplace=True)
    dataframe.drop(['caption', 'embeddable'], axis=1, inplace=True)
    print dataframe

def main(argv):
    gather(argv)

if __name__ == "__main__":
   main(sys.argv[1])

