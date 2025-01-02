from flask import Flask, render_template, request, jsonify
import os
from pygame import mixer

# Initialize Flask and pygame mixer
app = Flask(__name__)
mixer.init()

# Global variables
songs = []
current_song_index = -1
is_paused = False

# Helper functions
def play_song():
    global current_song_index
    if current_song_index >= 0 and current_song_index < len(songs):
        mixer.music.load(songs[current_song_index])
        mixer.music.play()

def stop_song():
    mixer.music.stop()

def pause_song():
    global is_paused
    if is_paused:
        mixer.music.unpause()
        is_paused = False
    else:
        mixer.music.pause()
        is_paused = True

@app.route('/')
def index():
    return render_template('index.html', songs=songs)

@app.route('/add_songs', methods=['POST'])
def add_songs():
    global songs
    uploaded_files = request.files.getlist("files")
    for file in uploaded_files:
        file_path = os.path.join("uploads", file.filename)
        file.save(file_path)
        songs.append(file_path)
    return jsonify({"status": "success", "songs": [os.path.basename(song) for song in songs]})

@app.route('/play', methods=['POST'])
def play():
    global current_song_index
    current_song_index = int(request.form['index'])
    play_song()
    return jsonify({"status": "playing", "song": os.path.basename(songs[current_song_index])})

@app.route('/pause', methods=['POST'])
def pause():
    pause_song()
    return jsonify({"status": "paused" if is_paused else "playing"})

@app.route('/stop', methods=['POST'])
def stop():
    stop_song()
    return jsonify({"status": "stopped"})

if __name__ == "__main__":
    os.makedirs("uploads", exist_ok=True)
    app.run(debug=True)
