#!/usr/bin/python
import vk_api
import time
import json


from apiclient.discovery import build
from apiclient.errors import HttpError
from oauth2client.tools import argparser

DEVELOPER_KEY = "AIzaSyCxRChRkk5DRLixKE0ntOzdDYZ9SbGKE_M"
YOUTUBE_API_SERVICE_NAME = "youtube"
YOUTUBE_API_VERSION = "v3"

info_file = 'channelInfo.json'
backup_info_file = 'channelInfo.txt'

my_app_id = -174558140
user_login = '+79885487241'
user_password = '271640893199a'
key = '6626073545b4d3e8149869778c7afee0c853f3fc4a825110d53b2ba35b9d2ec9cd470985197ceacd74e80'

def vk_auth(login, password, token):
    vk = vk_api.VkApi(login, password, token)
    vk.auth()

    return vk

def youtube_search(options, channel):
  youtube = build(YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_VERSION,
    developerKey=DEVELOPER_KEY)

  # Call the search.list method to retrieve results matching the specified
  # query term.
  search_response = youtube.search().list(
    type="video",
    part="id,snippet",
    maxResults=5,
    channelId=channel,
    order="date"
  ).execute()

  search_videos = []

  # Merge video ids
  for search_result in search_response.get("items", []):
    search_videos.append(search_result["id"]["videoId"])
  video_ids = ",".join(search_videos)

  # Call the videos.list method to retrieve location details for each video.
  video_response = youtube.videos().list(
    id=video_ids,
    part='snippet, recordingDetails'
  ).execute()


  # Add each result to the list, and then display the list of matching videos.
  for video_result in video_response.get("items", []):
    videoTitles.append("%s" % (video_result["snippet"]["title"]))
    videoURLs.append("%s" % (video_result["id"]))


 
vk = vk_auth(user_login, user_password, key)
vk_api = vk.get_api()

c = 0
while c  == 0:
    c += 1
    print('New cicle')
    try:
        f = open(info_file, mode = 'r')
    except:
        f = open(info_file, mode = 'w')
        f.close
        
    try:
        f_data = json.load(f)
        for item in f_data:
            print(item)
    except:
        f_data = {}
        f.close
        f = open(backup_info_file, mode = 'r')
        fr = [line.rstrip() for line in f]
        for line in fr:
            f_data[line] = ''
            print(line)
        
    f.close


    f = open('channelInfo.json', 'w')
    for key, value in f_data.items():
        videoTitles = []
        videoURLs = []
        args = argparser.parse_args()
        youtube_search(args, key)    
        i = 0
        if value == videoURLs[0]:
            print('На этом канале нет новых видео')
        else:
            f_data[key] = videoURLs[0]
            message_vk = ""
            while i < len(videoTitles):
                message_vk += "\n" + videoTitles[i] + "\n" + "http://www.youtube.com/watch?v=" + videoURLs[i] + "\n"
                i+=1
            vk_api.wall.post(owner_id = my_app_id, message = message_vk)
    fr = json.dumps(f_data)
    f.write(fr)
    f.close
    #time.sleep(300)
