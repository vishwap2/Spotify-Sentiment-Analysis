from io import BytesIO
import flask
from flask import Flask, render_template, request
import spotipy
from spotipy import SpotifyOAuth
from analysis import buildClassifier
from genius import determineLabel
from figure import labelFreqFig
from io import BytesIO
import base64
import config

app = Flask(__name__) # referencing this file
app.secret_key = config.SECRET_KEY

classifier = None

@app.route('/')
def index():
    return render_template('index.html') # knows to look in template folder

@app.route('/results/', methods=['POST'])
def results():
    classifier = buildClassifier()
    id = request.form['text']
    if id.isspace():
        flask.abort(400)
    #classifier = flask.session['classifier']
    # Spotipy Songs Retrieval
    scope = "user-library-read"

    sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=config.SPOTIFY_CLIENT_ID, 
    client_secret=config.SPOTIFY_CLIENT_SECRET, redirect_uri=config.SPOTIFY_REDIRECT_URI, scope=scope))

    # Map Song And Artist To Label
    output = dict()
    tracks = sp.playlist_items(id)
    for song in tracks['items']:
        track_name = song['track']['name']
        track_artists = ""
        for artist in song['track']['artists']:
            track_artists += " " + artist['name']
        # Genius Lyrics Retrieval - Stop Words and Punctuation Removal
        label = determineLabel(track_name, track_artists, classifier)
        key = track_name + " by" + track_artists
        output[key] = label
    #context = {"songs": output}
    fig = labelFreqFig(output)
    buf = BytesIO()
    fig.savefig(buf, format='png')
    img = base64.b64encode(buf.getbuffer()).decode("ascii")
    #return render_template('results/index.html', **context)
    return f"<img src='data:image/png;base64,{img}'/>"
    

if __name__ == "__main__":
    app.run(debug=True)