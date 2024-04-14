import pickle
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from flask import Flask, render_template, request

app = Flask(__name__)

CLIENT_ID = "cb741c54f8da4ee084dd35cf4cb02e69"
CLIENT_SECRET = "56e542d83bc04bc58acbbb0e1a87ca15"

client_credentials_manager = SpotifyClientCredentials(client_id=CLIENT_ID, client_secret=CLIENT_SECRET)
sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

music = pickle.load(open('model/df.pkl','rb'))
similarity = pickle.load(open('model/similarity.pkl','rb'))

def get_song_album_cover_url(song_name, artist_name):
    search_query = f"track:{song_name} artist:{artist_name}"
    results = sp.search(q=search_query, type="track")

    if results and results["tracks"]["items"]:
        track = results["tracks"]["items"][0]
        album_cover_url = track["album"]["images"][0]["url"]
        print(album_cover_url)
        return album_cover_url
    else:
        return "https://i.postimg.cc/0QNxYz4V/social.png"

def recommend(song):
    index = music[music['song'] == song].index[0]
    distances = sorted(list(enumerate(similarity[index])), reverse=True, key=lambda x: x[1])
    recommended_music_names = []
    recommended_music_posters = []
    for i in distances[1:6]:
        artist = music.iloc[i[0]].artist
        print(artist)
        print(music.iloc[i[0]].song)
        recommended_music_posters.append(get_song_album_cover_url(music.iloc[i[0]].song, artist))
        recommended_music_names.append(music.iloc[i[0]].song)

    return recommended_music_names,recommended_music_posters

@app.route('/', methods = ['GET', 'POST'])
def index():
    if request.method == 'POST':
        selected_movie = request.form['song']
        recommended_music_names, recommended_music_posters = recommend(selected_movie)
        return render_template('index.html', recommended_music_names=recommended_music_names, recommended_music_posters=recommended_music_posters)
    else:
        music = pickle.load(open('model/df.pkl','rb'))
        music_list = music['song'].values
        return render_template('index.html', music_list=music_list)

if __name__ == '__main__':
    app.run()