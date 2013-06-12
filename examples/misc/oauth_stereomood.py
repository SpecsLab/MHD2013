from __future__ import unicode_literals
import requests
from requests_oauthlib import OAuth1
import ssi_interface as ssi
import sensor_reader as sr
import json
import time
import numpy as np
import sys
from urlparse import parse_qs


client_key = ''  # your client_key here
client_secret = '' # your client_secret here
port = "/dev/tty.usbmodem411"
baudrate = 115200
board_id = 'board1' # your board here
ssi_server_address = "0.0.0.0"

state = "unknown"


start_recording = False
start_recording_promp = raw_input('ready to record? [y/n]')


if start_recording_promp == 'y':
    start_recording = True

    sensor = sr.SensorReader(port,baudrate)
    ssi_send = ssi.SSI_interface_Sender(board_id, ssi_server_address)
    ssi_receive_arousal = ssi.SSI_interface_Receiver(board_id,"receive_gsr_arousal")

    time.sleep(1)


else:
    sys.exit(1)


if start_recording == True:

    arousal_values = []
    time_start_recording = time.time()
    time_end_recording = 0 

    while (time_end_recording - time_start_recording)<=10:
    
        # ecg = sensor.data[0]
        # ssi_send.send_to_SSI(self, data, "send_ecg")

        # gsr = sensor.data[1]
        # ssi_send.send_to_SSI(self, data, "send_gsr")
        
        # airflow = sensor.data[2]
        # ssi_send.send_to_SSI(self, data, "send_air")


        if (time_end_recording - time_start_recording > 5):      
          arousal_t = ssi_receive_arousal.datapack["receive_gsr_arousal"][6]
          arousal_values.append(arousal_t)
          
          print "recording ... ", arousal_t


        time_end_recording = time.time()

 
mean_arousal = np.mean(np.array(arousal_values),0)

if mean_arousal<=0.25:
    state = "relaxed"

elif mean_arousal>0.25 and mean_arousal<=0.50:
    state = "calm"

elif mean_arousal>0.50 and mean_arousal<=0.75:
    state = "excited"

elif mean_arousal>0.75:
    state = "crazy"


print "it seems you are feeling "+state
generate_playlist_promp = raw_input('do you want to generate a playlist on stereomood? [y/n]')

if generate_playlist_promp != 'y':
    sys.exit(1)


oauth = OAuth1(client_key, client_secret=client_secret)
request_token_url = 'http://www.stereomood.com/api/oauth/request_token'
r = requests.post(url=request_token_url, auth=oauth)

#print r.content

credentials = parse_qs(r.content)
resource_owner_key = credentials.get('oauth_token')[0]
resource_owner_secret = credentials.get('oauth_token_secret')[0]
authorize_url = 'http://www.stereomood.com/api/oauth/authorize?oauth_token='
authorize_url = authorize_url + resource_owner_key
print 'Please go here and authorize,', authorize_url
verifier = raw_input('Please input the verifier')


oauth = OAuth1(client_key,
                   client_secret=client_secret,
                   resource_owner_key=resource_owner_key,
                   resource_owner_secret=resource_owner_secret,
                   verifier=verifier)
access_token_url = 'http://www.stereomood.com/api/oauth/access_token'
r = requests.post(url=access_token_url, auth=oauth)
credentials = parse_qs(r.content)
resource_owner_key = credentials.get('oauth_token')[0]
resource_owner_secret = credentials.get('oauth_token_secret')[0]


oauth = OAuth1(client_key,
                   client_secret=client_secret,
                   resource_owner_key=resource_owner_key,
                   resource_owner_secret=resource_owner_secret)
url = 'http://www.stereomood.com/api/search.json?q='+state+'&type=mood'
r_songs = requests.get(url=url, auth=oauth)

json_r_songs = json.loads(r_songs.content)
songs_ids = []
for s in json_r_songs["songs"]:
    songs_ids.append(s["id"])

#print songs_ids

playlist_name = "feel"+state
playlist_create_url = "http://www.stereomood.com/api/user/playlists/playlist.json?name="+playlist_name
r_playlist_create = requests.post(url=playlist_create_url, auth=oauth)

json_id_playlist = json.loads(r_playlist_create.content)

print "playlist "+playlist_name+" created!"

playlist_id = json_id_playlist["id"]

song_add_url = "http://www.stereomood.com/api/user/playlists/song/"+playlist_id+".json?songid="

for i in range(0,10):
    r_add_song = requests.post(url=song_add_url+songs_ids[i], auth=oauth)
    print r_add_song.content
    time.sleep(1)

print "end of the story!"


