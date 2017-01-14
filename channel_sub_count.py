import requests

API_KEY = "AIzaSyBYq7UXn9VnF9JOLKEDHgU0N0u0U_zw3ps"
channel_id = "UCM9KEEuzacwVlkt9JfJad7g"

url = "https://www.googleapis.com/youtube/v3/channels?part=statistics&id=" + channel_id + "&key=" + API_KEY
response = requests.get(url)
data = response.json()
print data

"""
extract needed channel ids from csv file and run for them and add to data file
subscriberCount, videoCount, viewCount
"""