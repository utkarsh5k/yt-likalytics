import requests

API_KEY = "AIzaSyBYq7UXn9VnF9JOLKEDHgU0N0u0U_zw3ps"
channel_id = "UCM9KEEuzacwVlkt9JfJad7g"

def get_all_data(channel_id):
	url = "https://www.googleapis.com/youtube/v3/channels?part=statistics&id=" + channel_id + "&key=" + API_KEY
	response = requests.get(url)
	data = response.json()
	items = data['items'][0]
	statistics = items['statistics']
	channel_view_count = statistics['viewCount']
	channel_subscriber_count = statistics['subscriberCount']
	channel_video_count = statistics['videoCount']
	return {'channel_view_count': channel_view_count, 'channel_video_count': channel_video_count, 'channel_subscriber_count': channel_subscriber_count}
