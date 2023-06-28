from flask import Flask, render_template
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import requests
import re
import pickle
from flask import request

app = Flask(__name__)

def songsearch(id):
    client_id = '42941b21de9046c8b880147deda15f1a'
    client_secret = 'ff1daeadc5b94461b376e7599e628eaf'
    redirect_uri = 'http://localhost:8000/callback'
    client_credentials_manager = SpotifyClientCredentials(client_id=client_id, client_secret=client_secret)
    sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)
    # data = {
    # 'url': 'https://audd.tech/example.mp3',
    # 'return': 'spotify',
    # 'apitoken': 'test'
    # }
    # files = {
    # 'file': open('C://Users//praxo//Downloads//beensolong.mp3' , 'rb'),
    # }
    # result = requests.post('https://api.audd.io/', data=data, files=files)
    # x = result.text
    track_id = id
    track_id = track_id.split("track/")[1]
    print(track_id)
    track = sp.track(track_id)
    track_name = track['name']
    artist_name = track['artists'][0]['name']
    album_name = track['album']['name']
    duration_ms = track['duration_ms']
    song_name_artist = track_name + artist_name
    song = sp.search(song_name_artist, limit=5)
    audio_features = sp.audio_features(song["tracks"]["items"][0]["id"])[0]
    print(audio_features)
    return(modelrun(audio_features))

def modelrun(audio_features):
    arr=[]
    for i in audio_features.keys():
        if(i=='type'):
            break
        arr.append(audio_features[i])
    arr.append(audio_features['time_signature'])
    arr.append(audio_features['duration_ms']/60000)

    results= ['Dark Trap', 'Emo', 'HipHop', 'Pop', 'Rap', 'RnB', 'Trap Metal', 'Underground Rap', 'DnB', 'HardStyle', 'PsyTrance', 'TechHouse', 'Techno', 'Trance', 'Trap']
    loaded_model = pickle.load(open("rfc.pkl", "rb"))
    out= loaded_model.predict([arr])
    return(results[out[0]])

@app.route("/")
def hello_world():
    return render_template('index.html')

@app.route("/result", methods = ['GET','POST'])
def result():
    values = request.form.to_dict()
    pred = songsearch(values['id'])
    return render_template('result.html', pred = pred)

if __name__ == '__main__': 
   app.run()