import pandas as pd
import sys
import numpy as np

from sklearn.externals import joblib

from apiclient.discovery import build
from apiclient.errors import HttpError
from oauth2client.tools import argparser

import video_title_hits as vth
import channel_details as cd
import durate as dr

API_KEY = "AIzaSyBYq7UXn9VnF9JOLKEDHgU0N0u0U_zw3ps"
API_NAME = "youtube"
API_VERSION = "v3"

def gather(search_query):
    argparser.add_argument("--v", help="Search term", default=search_query)
    argparser.add_argument("--max-results", help="Max results", default=1)
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
    predict(dataframe)

def predict(df):
    liker = joblib.load('likes.pkl')

    df['title_hits'] = vth.get_hits(df)
    df['timing'] = dr.times(df)[0]

    privacyOptions = ['public', 'private', 'unlisted', 'localized']
    df.privacyStatus = df.privacyStatus.replace(to_replace=df.privacyStatus[~df.privacyStatus.isin(privacyOptions)], value='unlisted')
    
    def_map_dict = {'hd':720, 'sd':240}
    df.definition = df.definition.map(def_map_dict)

    privacy_map_dict = {'public':3, 'unlisted':1, 'private': 0}
    df.privacyStatus = df.privacyStatus.map(privacy_map_dict)

    df['projection'].fillna('none', inplace=True)
    projection_dict = {'rectangular': 2, '360': 1, 'none': 0}
    df.projection = df.projection.map(projection_dict)

    df['liveBroadcastContent'].fillna('unspecified', inplace=True)
    live_dict = {'live': 2, 'none': 1, 'unspecified': 0}
    df.liveBroadcastContent = df.liveBroadcastContent.map(live_dict)

    df.drop(['channelId', 'channelTitle', 'description', 'duration', 'localized', 'publicStatsViewable', 'publishedAt', 'tags', 'title', 'v_id'], axis=1, inplace=True)
    df[['categoryId','channel_subscriber_count', 'channel_view_count', 'channel_video_count', 'commentCount', 'definition', 'dislikeCount', 'favoriteCount', 'likeCount', 'liveBroadcastContent', 'privacyStatus', 'projection', 'viewCount', 'title_hits', 'timing']] = df[['categoryId','channel_subscriber_count', 'channel_view_count', 'channel_video_count', 'commentCount', 'definition', 'dislikeCount', 'favoriteCount', 'likeCount', 'liveBroadcastContent', 'privacyStatus', 'projection', 'viewCount', 'title_hits', 'timing']].astype(float)

    df = df[np.isfinite(df['likeCount'])]
    df['commentCount'].fillna(0, inplace = True)

    df_to_np = {
    'categoryId': 0,
    'channel_subscriber_count': 1,
    'channel_video_count': 2,
    'channel_view_count': 3,
    'commentCount': 4,
    'definition': 5,
    'dislikeCount': 6,              
    'favoriteCount': 7,              
    'likeCount': 8,                   
    'liveBroadcastContent': 9,       
    'privacyStatus': 10,              
    'projection': 11,                  
    'viewCount': 12,                   
    'title_hits': 13,                  
    'timing': 14
    }

    npdata = df.as_matrix()

    y = npdata[:,8]
    X = np.delete(npdata, np.s_[8:9], axis = 1)

    print liker.predict(X)

def main(argv):
    # print argv
    gather(str(argv))

if __name__ == '__main__':
   main(sys.argv[1])

