from flask import Flask, render_template, request, jsonify, send_file, Response
import os
import json
# Initialize Flask and pygame mixer
app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/add_songs', methods=['POST'])
def add_songs():
    file = request.files.getlist("song")[0]
    cover = request.files.getlist("cover")[0]
    artist = request.form.get("artist")
    genre = request.form.get("genre")
    obj = {}
    file_path = os.path.join("uploads/songs", file.filename)
    file.save(file_path)
    obj['file_path'] = file_path
    obj['artist'] = artist
    obj['genre'] = genre
    cover_path = os.path.join("uploads/covers", cover.filename)
    cover.save(cover_path)
    obj['cover_path'] = cover_path
    with open('uploads/objects/'+file.filename+artist+'.json', 'w') as fp:
        json.dump(obj, fp)
    return Response(200)

@app.route('/uploads/songs/<string:song>', methods=['GET'])
def get_song(song):
    dir = os.listdir('./uploads/songs')
    idx = int(song)
    try:
        dir[int(song)]
    except:
        idx = (idx + 1) % (len(dir))

    return send_file('uploads/songs/'+dir[idx])


if __name__ == "__main__":
    os.makedirs("uploads", exist_ok=True)
    app.run(debug=True)
