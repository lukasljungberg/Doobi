from flask import Flask, render_template, request, jsonify, send_file
import os

# Initialize Flask and pygame mixer
app = Flask(__name__)

# Global variables
songs = []
current_song_index = -1

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

@app.route('/uploads/<string:song>', methods=['GET'])
def get_song(song):
    dir = os.listdir('./uploads')
    idx = int(song)
    try:
        dir[int(song)]
    except:
        idx = (idx + 1) % (len(dir))

    return send_file('uploads/'+dir[idx])


if __name__ == "__main__":
    os.makedirs("uploads", exist_ok=True)
    app.run(debug=True)
